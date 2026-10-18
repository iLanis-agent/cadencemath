#!/usr/bin/env python3
# Cadence Math oracle - mirrors engine.js.
import json, re, math
from datetime import date, timedelta

EPOCH = date(1970, 1, 1)
DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def _date(s, label):
    msg = f"{label} must be a real date written like 2026-10-19, from 1970 to 2100"
    m = re.fullmatch(r"([0-9]{4})-([0-9]{2})-([0-9]{2})", str(s).strip())
    if not m:
        raise ValueError(msg)
    y, mo, d = int(m[1]), int(m[2]), int(m[3])
    if y < 1970 or y > 2100:
        raise ValueError(msg)
    try:
        dt = date(y, mo, d)
    except ValueError:
        raise ValueError(msg)
    return (dt - EPOCH).days

MAX = _date("2100-12-31", "limit")

def _iso(n):
    return (EPOCH + timedelta(days=n)).isoformat()

def _named(n):
    return f"{_iso(n)} ({DAYS[(n + 4) % 7]})"

def _every(x, label):
    if not isinstance(x, int) or x < 1 or x > 3660:
        raise ValueError(f"{label} must be a whole number of days from 1 to 3660")
    return x

def _phrase(n):
    return "every day" if n == 1 else f"every {n} days"

def _cap(s):
    return s[:1].upper() + s[1:]

def next_truth(start, every, nth):
    a = _date(start, "start date")
    e = _every(every, "cycle")
    if not isinstance(nth, int) or nth < 1 or nth > 1000:
        raise ValueError("occurrence must be a whole number from 1 to 1000")
    r = a + (nth - 1) * e
    if r > MAX:
        raise ValueError("that date is past the year 2100")
    return f"{_cap(_phrase(e))} from {_named(a)}: occurrence {nth} is {_named(r)}."

def count_truth(start, every, end):
    a = _date(start, "start date")
    e = _every(every, "cycle")
    b = _date(end, "end date")
    if b < a:
        raise ValueError("end date must not be before start date")
    k = (b - a) // e + 1
    last = a + (k - 1) * e
    return (f"{_cap(_phrase(e))} from {_iso(a)} through {_iso(b)} inclusive: {k} "
            + ("occurrence" if k == 1 else "occurrences") + f", the last on {_iso(last)}.")

def lap_truth(start, ea, eb):
    a = _date(start, "start date")
    x = _every(ea, "first cycle")
    y = _every(eb, "second cycle")
    l = x // math.gcd(x, y) * y
    r = a + l
    if r > MAX:
        raise ValueError("that date is past the year 2100")
    return (f"{_cap(_phrase(x))} and {_phrase(y)}, both starting {_iso(a)}, line up {_phrase(l)}. "
            f"First repeat: {_named(r)}.")

FNS = {"nextTruth": next_truth, "countTruth": count_truth, "lapTruth": lap_truth}

CASES = [
    ("nextTruth", ["2026-10-19", 14, 6]), ("nextTruth", ["2026-10-19", 14, 1]), ("nextTruth", ["2026-10-19", 1, 10]),
    ("nextTruth", ["2026-10-19", 7, 52]), ("nextTruth", ["2026-10-19", 3660, 1000]), ("nextTruth", ["2026-10-19", 3660, 2]),
    ("nextTruth", ["2026-10-19", 0, 3]), ("nextTruth", ["2026-10-19", 14, 0]), ("nextTruth", ["2026-10-19", 14, 1001]),
    ("nextTruth", ["2026-10-19", 1.5, 3]), ("nextTruth", ["2026-13-19", 14, 3]), ("nextTruth", ["2100-12-31", 1, 1]),
    ("nextTruth", ["2100-12-31", 1, 2]),
    ("countTruth", ["2026-10-19", 14, "2026-12-31"]), ("countTruth", ["2026-10-19", 14, "2026-10-19"]),
    ("countTruth", ["2026-10-19", 14, "2026-11-01"]), ("countTruth", ["2026-10-19", 14, "2026-11-02"]),
    ("countTruth", ["2026-10-19", 1, "2026-10-21"]), ("countTruth", ["2026-10-19", 14, "2026-10-18"]),
    ("countTruth", ["2026-10-19", 14, "soon"]), ("countTruth", ["2026-10-19", 3661, "2027-01-01"]),
    ("lapTruth", ["2026-10-19", 4, 6]), ("lapTruth", ["2026-10-19", 7, 7]), ("lapTruth", ["2026-10-19", 1, 1]),
    ("lapTruth", ["2026-10-19", 3, 5]), ("lapTruth", ["2026-10-19", 3660, 3659]), ("lapTruth", ["2026-10-19", 0, 5]),
    ("lapTruth", ["2026-10-19", 4, 3661]), ("lapTruth", ["2026-10-19", 14, 21]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
