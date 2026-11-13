# Fix the range parser in the selected CLI

The supplied small CLI parses inclusive ranges such as `3-5`. Its existing tests
cover the happy path, but the application currently mishandles descending ranges.
Make the parser return the integers in each valid inclusive range in ascending
order, so `3-5` yields `3,4,5` and `5-3` also yields `3,4,5`. Preserve the
existing rejection of zero and negative bounds, and reject nonnumeric text.
Accept a single positive integer. Preserve the current JSON output for valid
input and the current nonzero error behavior for invalid input.

Fix the bug through the selected entry and the declared bundle. Add a focused
regression check that exercises the final application contract. Do not add a
framework, change unrelated files, commit, install, or publish.

Write `RESULT.md` inside the subject and a measurement note outside the subject
describing counters the host actually exposed. Do not read evaluator answers.
