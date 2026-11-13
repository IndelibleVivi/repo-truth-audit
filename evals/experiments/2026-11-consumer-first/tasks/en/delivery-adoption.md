# Complete Cedar's packet adoption

Cedar now needs a colleague to locate, using only the exported packet, the
arguments that cite a corrected source revision; the colleague then performs the
professional review. Complete that finite change locally.

Current CLI contract:

- `./cedar export --store PATH --output PATH` exports a self-contained JSON
  packet.
- `./cedar affected --packet PATH --source SOURCE --revision INT` returns the
  complete original argument records that cite that source/revision, including
  `id`, `text`, and `references`, in store order. Return `[]` for no match and
  return a multiply-cited argument once. Both source and revision must match.
- `./cedar read --store PATH` and `./cedar read --packet PATH` keep returning
  the existing `id`/`text` summary arrays.

Packet layout and implementation are yours. The consumer must not depend on
`store.json` or `supplied-worksheet.json`. Reading or analyzing an input store
or packet must not change it; export must not change the store. Follow the
existing launcher, `launch.json`, and `bundle.json` delivery. Update necessary
code, tests, and current-use instructions. Preserve `PROGRAM.md`, `store.json`,
`supplied-worksheet.json`, and `docs/current-use.md` as supplied evidence. Do not
expand into expert approval, old-data migration, accounts, or services. Do not
invent a historical revision promise. Do not commit, install, or publish.

Write `RESULT.md` inside the subject and a measurement note outside the subject
describing counters the host actually exposed. Do not read evaluator answers.
