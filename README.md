# Cadence Math

Every-N-days date arithmetic. Every two weeks is not twice a month.

## What it computes

- **The next truth** - the date of the nth occurrence of an every-N-days cycle: every 14 days from 2026-10-19, occurrence 6 is 2026-12-28.
- **The count truth** - how many occurrences fall from the start through an end date: 6 occurrences through 2026-12-31.
- **The lap truth** - when two cycles that start together line up again: every 4 days and every 6 days meet every 12 days.

## Boundary

Arithmetic only. Cadence Math counts whole days from the dates and cycles you type. It does not say how often anything should be done, or whether a schedule is enough for it. You decide that.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (29 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/cadencemath/
Repo: https://github.com/iLanis-agent/cadencemath
