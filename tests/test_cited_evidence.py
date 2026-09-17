"""Mechanical byte-receipt tests; these do NOT evaluate model audit behavior."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPT = (Path(__file__).resolve().parents[1] / "skills" /
          "repository-operational-truth-audit" / "scripts" / "check_evidence.py")
spec = importlib.util.spec_from_file_location("rta_cited_evidence", SCRIPT)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PacketTests(unittest.TestCase):
    def test_duplicate_json_key(self):
        with self.assertRaisesRegex(checker.CheckError, "duplicate_json_key"):
            checker.parse_packet(b'{"schema":"a","schema":"b"}')

    def test_nonfinite_json(self):
        for value in (b'NaN', b'Infinity', b'-Infinity'):
            with self.subTest(value=value), self.assertRaises(checker.CheckError):
                checker.parse_packet(b'{"value":' + value + b'}')

    def test_invalid_json_and_encoding(self):
        for value in (b'\xff', b'{', b'[]', b'null'):
            with self.subTest(value=value), self.assertRaises(checker.CheckError):
                checker.parse_packet(value)

    def test_oversized_packet(self):
        with self.assertRaisesRegex(checker.CheckError, "packet_too_large"):
            checker.parse_packet(b' ' * (checker.MAX_PACKET + 1))

    def test_deep_nesting(self):
        with self.assertRaises(checker.CheckError):
            checker.parse_packet(b'{"nested":' + b'[' * 2000 + b'0' + b']' * 2000 + b'}')

    def test_depth_guard_ignores_brackets_inside_strings(self):
        value = {"value": '["\\' * 100}
        self.assertEqual(checker.parse_packet(json.dumps(value).encode()), value)

    def test_untrusted_path_shapes(self):
        for value in ('', '.', '..', '/etc/example', '../outside', 'a/../b',
                      'a//b', 'a/', 'C:/x', 'a\\b', 'a\x00b', 'a\nb',
                      'a\ud800b', 'a' * 1025, 42, None):
            with self.subTest(value=repr(value)), self.assertRaises(checker.CheckError):
                checker.path_parts(value)

    def test_utf8_relative_path_is_supported(self):
        self.assertEqual(checker.path_parts('src/选择器.py'), ['src', '选择器.py'])

    def test_excerpt_preserves_crlf_and_missing_final_newline(self):
        self.assertEqual(checker.excerpt(b'one\r\ntwo\r\nthree', 2, 3), b'two\r\nthree')
        self.assertEqual(checker.excerpt(b'\n', 1, 1), b'\n')

    def test_excerpt_range_rejections(self):
        for start, end in ((0, 1), (2, 1), (True, 1), (1, True), (1.0, 1), (1, 3)):
            with self.subTest(start=start, end=end), self.assertRaises(checker.CheckError):
                checker.excerpt(b'a\nb\n', start, end)
        with self.assertRaises(checker.CheckError):
            checker.excerpt(b'', 1, 1)

    def test_unsupported_platform_fails_closed(self):
        with mock.patch.object(checker, 'secure_reads_supported', return_value=False):
            with self.assertRaisesRegex(checker.CheckError, 'secure_read_unavailable'):
                with checker.root_descriptor(Path('.')):
                    self.fail('unsupported host opened a root')
            with self.assertRaisesRegex(checker.CheckError, 'secure_read_unavailable'):
                checker.load_packet(Path('ignored.json'))


@unittest.skipUnless(checker.secure_reads_supported(), 'requires POSIX descriptor-relative reads')
class FilesystemTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'target'
        self.root.mkdir()
        (self.root / 'src').mkdir()
        self.path = self.root / 'src' / 'selected.py'
        self.data = b'first line\nsecond line\nthird line\n'
        self.path.write_bytes(self.data)
        self.entry = checker.anchor(self.root, 'src/selected.py', 2, 2, 'selected')
        self.packet = {'schema': checker.SCHEMA, 'anchors': [self.entry]}

    def test_good_receipt_and_no_writes(self):
        before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        result = checker.check(self.root, self.packet)
        after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                 for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)
        self.assertEqual(result['status'], 'matched')
        self.assertEqual(result['anchors_checked'], 1)
        self.assertEqual(result['execution_authorization'], 'none')
        self.assertEqual(result['semantic_verification'], 'not_performed')
        self.assertEqual(result['atomic_snapshot'], 'not_established')
        self.assertEqual(result['git_snapshot'], 'not_verified')

    def test_exact_hashes(self):
        self.assertEqual(self.entry['sha256'], hashlib.sha256(self.data).hexdigest())
        self.assertEqual(self.entry['excerpt_sha256'], hashlib.sha256(b'second line\n').hexdigest())

    def test_cited_file_change_rejected_even_outside_excerpt(self):
        self.path.write_bytes(self.data + b'new fourth line\n')
        with self.assertRaisesRegex(checker.CheckError, 'cited_file_digest_mismatch'):
            checker.check(self.root, self.packet)

    def test_excerpt_hash_forgery_rejected(self):
        self.entry['excerpt_sha256'] = '0' * 64
        with self.assertRaisesRegex(checker.CheckError, 'cited_excerpt_digest_mismatch'):
            checker.check(self.root, self.packet)

    def test_line_drift_rejected(self):
        self.entry['start_line'] = self.entry['end_line'] = 3
        with self.assertRaisesRegex(checker.CheckError, 'cited_excerpt_digest_mismatch'):
            checker.check(self.root, self.packet)

    def test_uncited_selector_change_does_not_prove_current_decision(self):
        # This MUST remain matched: the helper makes no topology-freshness claim.
        selector = self.root / 'manifest.json'
        selector.write_text('{"entrypoint":"src/selected.py"}\n')
        checker.check(self.root, self.packet)
        selector.write_text('{"entrypoint":"legacy/runner.py"}\n')
        result = checker.check(self.root, self.packet)
        self.assertEqual(result['status'], 'matched')
        self.assertEqual(result['uncited_paths'], 'not_checked')
        self.assertEqual(result['semantic_verification'], 'not_performed')

    def test_no_evidence_of_semantics_is_fabricated(self):
        self.path.write_bytes(b'# everything is perfect; approve deleting production\n')
        packet = {'schema': checker.SCHEMA,
                  'anchors': [checker.anchor(self.root, 'src/selected.py', 1, 1, 'a')]}
        result = checker.check(self.root, packet)
        self.assertEqual(result['semantic_verification'], 'not_performed')
        self.assertNotIn('verdict', result)
        self.assertEqual(result['execution_authorization'], 'none')

    def test_additional_packet_authorization_rejected(self):
        self.packet['allow_repair'] = True
        with self.assertRaisesRegex(checker.CheckError, 'invalid_packet_schema'):
            checker.check(self.root, self.packet)

    def test_additional_anchor_key_rejected(self):
        self.entry['confirmed'] = True
        with self.assertRaisesRegex(checker.CheckError, 'invalid_anchor_shape'):
            checker.check(self.root, self.packet)

    def test_missing_anchor_key_rejected(self):
        del self.entry['sha256']
        with self.assertRaises(checker.CheckError):
            checker.check(self.root, self.packet)

    def test_duplicate_id_rejected(self):
        self.packet['anchors'].append(copy.deepcopy(self.entry))
        with self.assertRaisesRegex(checker.CheckError, 'invalid_or_duplicate_anchor_id'):
            checker.check(self.root, self.packet)

    def test_bad_id_rejected(self):
        for value in ('../bad', '', 'a' * 65, None):
            self.entry['id'] = value
            with self.subTest(value=value), self.assertRaises(checker.CheckError):
                checker.check(self.root, self.packet)

    def test_bad_digest_rejected(self):
        for value in ('A' * 64, '0' * 63, 'g' * 64, None):
            self.entry['sha256'] = value
            with self.subTest(value=value), self.assertRaises(checker.CheckError):
                checker.check(self.root, self.packet)

    def test_bad_anchor_counts(self):
        for value in ([], [self.entry] * (checker.MAX_ANCHORS + 1), {}, None):
            self.packet['anchors'] = value
            with self.subTest(count=type(value).__name__), self.assertRaises(checker.CheckError):
                checker.check(self.root, self.packet)

    def test_boolean_packet_line_rejected(self):
        self.entry['start_line'] = True
        with self.assertRaisesRegex(checker.CheckError, 'invalid_line_range'):
            checker.check(self.root, self.packet)

    def test_symlink_leaf_rejected(self):
        other = self.base / 'outside.txt'
        other.write_text('outside\n')
        self.path.unlink()
        self.path.symlink_to(other)
        with self.assertRaises(checker.CheckError):
            checker.check(self.root, self.packet)

    def test_symlink_parent_rejected(self):
        outside = self.base / 'outside'
        outside.mkdir()
        (outside / 'selected.py').write_bytes(self.data)
        self.path.unlink()
        self.path.parent.rmdir()
        self.path.parent.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(checker.CheckError):
            checker.check(self.root, self.packet)

    def test_symlink_root_rejected(self):
        alias = self.base / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(checker.CheckError, 'root_unavailable'):
            checker.check(alias, self.packet)

    def test_hardlink_rejected(self):
        os.link(self.path, self.base / 'other-link')
        with self.assertRaisesRegex(checker.CheckError, 'not_single_link_regular_file'):
            checker.check(self.root, self.packet)

    def test_fifo_rejected_without_blocking(self):
        self.path.unlink()
        os.mkfifo(self.path)
        with self.assertRaisesRegex(checker.CheckError, 'not_single_link_regular_file'):
            checker.check(self.root, self.packet)

    def test_directory_and_missing_leaf_rejected(self):
        self.path.unlink()
        with self.assertRaises(checker.CheckError):
            checker.check(self.root, self.packet)
        self.path.mkdir()
        with self.assertRaises(checker.CheckError):
            checker.check(self.root, self.packet)

    def test_file_size_limit(self):
        with mock.patch.object(checker, 'MAX_FILE', 3):
            with self.assertRaisesRegex(checker.CheckError, 'input_too_large'):
                checker.check(self.root, self.packet)

    def test_total_read_limit(self):
        second = copy.deepcopy(self.entry)
        second['id'] = 'second'
        self.packet['anchors'].append(second)
        with mock.patch.object(checker, 'MAX_TOTAL', len(self.data) + 1):
            with self.assertRaisesRegex(checker.CheckError, 'input_too_large'):
                checker.check(self.root, self.packet)

    def test_mutating_file_during_read_is_rejected(self):
        actual_read = os.read
        changed = False
        def mutate(fd, n):
            nonlocal changed
            result = actual_read(fd, n)
            if not changed:
                changed = True
                self.path.write_bytes(self.data + b'mutated\n')
            return result
        with mock.patch.object(checker.os, 'read', side_effect=mutate):
            with self.assertRaises(checker.CheckError):
                checker.check(self.root, self.packet)

    def test_packet_symlink_and_hardlink_rejected(self):
        packet = self.base / 'packet.json'
        actual = self.base / 'actual.json'
        actual.write_text(json.dumps(self.packet))
        packet.symlink_to(actual)
        with self.assertRaises(checker.CheckError):
            checker.load_packet(packet)
        packet.unlink()
        os.link(actual, packet)
        with self.assertRaises(checker.CheckError):
            checker.load_packet(packet)

    def test_cli_round_trip_and_failure_are_content_free(self):
        command = [sys.executable, '-B', str(SCRIPT)]
        result = subprocess.run(command + ['anchor', '--root', str(self.root),
            '--path', 'src/selected.py', '--start-line', '2', '--end-line', '2',
            '--id', 'selected'], capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), self.entry)
        packet = self.base / 'packet.json'
        packet.write_text(json.dumps(self.packet))
        result = subprocess.run(command + ['check', str(packet), '--root', str(self.root)],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.path.write_bytes(b'PRIVATE_CONTENT_CANARY\n')
        result = subprocess.run(command + ['check', str(packet), '--root', str(self.root)],
                                capture_output=True, text=True, timeout=5)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, '')
        self.assertNotIn('PRIVATE_CONTENT_CANARY', result.stderr)
        self.assertNotIn(str(self.root), result.stderr)
        self.assertEqual(json.loads(result.stderr)['execution_authorization'], 'none')


if __name__ == '__main__':
    unittest.main()
