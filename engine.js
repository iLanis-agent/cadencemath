// Cadence Math engine - every-N-days date arithmetic.
// Mirrored by oracle.py; keep the op order identical.
// Cycles are counted in whole days, never months. The first date counts as occurrence 1.

var _DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

function _date(s, label) {
  var m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(String(s).trim());
  var msg = label + " must be a real date written like 2026-10-19, from 1970 to 2100";
  if (!m) throw new Error(msg);
  var y = parseInt(m[1], 10), mo = parseInt(m[2], 10), d = parseInt(m[3], 10);
  if (y < 1970 || y > 2100) throw new Error(msg);
  var t = Date.UTC(y, mo - 1, d);
  var c = new Date(t);
  if (c.getUTCFullYear() !== y || c.getUTCMonth() !== mo - 1 || c.getUTCDate() !== d) throw new Error(msg);
  return t / 86400000;
}

var _MAX = _date("2100-12-31", "limit");

function _iso(n) {
  return new Date(n * 86400000).toISOString().slice(0, 10);
}

function _named(n) {
  return _iso(n) + " (" + _DAYS[(n + 4) % 7] + ")";
}

function _every(x, label) {
  if (!Number.isInteger(x) || x < 1 || x > 3660) throw new Error(label + " must be a whole number of days from 1 to 3660");
  return x;
}

function _phrase(n) {
  return n === 1 ? "every day" : "every " + n + " days";
}

function _cap(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function _gcd(a, b) {
  while (b) { var t = a % b; a = b; b = t; }
  return a;
}

// The next truth: the date of the nth occurrence of an every-N-days cycle.
function nextTruth(start, every, nth) {
  var a = _date(start, "start date");
  var e = _every(every, "cycle");
  if (!Number.isInteger(nth) || nth < 1 || nth > 1000) throw new Error("occurrence must be a whole number from 1 to 1000");
  var r = a + (nth - 1) * e;
  if (r > _MAX) throw new Error("that date is past the year 2100");
  return _cap(_phrase(e)) + " from " + _named(a) + ": occurrence " + nth + " is " + _named(r) + ".";
}

// The count truth: how many occurrences fall on or before an end date.
function countTruth(start, every, end) {
  var a = _date(start, "start date");
  var e = _every(every, "cycle");
  var b = _date(end, "end date");
  if (b < a) throw new Error("end date must not be before start date");
  var k = Math.floor((b - a) / e) + 1;
  var last = a + (k - 1) * e;
  return _cap(_phrase(e)) + " from " + _iso(a) + " through " + _iso(b) + " inclusive: " + k +
    (k === 1 ? " occurrence" : " occurrences") + ", the last on " + _iso(last) + ".";
}

// The lap truth: when two cycles that start together line up again.
function lapTruth(start, everyA, everyB) {
  var a = _date(start, "start date");
  var x = _every(everyA, "first cycle");
  var y = _every(everyB, "second cycle");
  var l = x / _gcd(x, y) * y;
  var r = a + l;
  if (r > _MAX) throw new Error("that date is past the year 2100");
  return _cap(_phrase(x)) + " and " + _phrase(y) + ", both starting " + _iso(a) + ", line up " + _phrase(l) +
    ". First repeat: " + _named(r) + ".";
}
