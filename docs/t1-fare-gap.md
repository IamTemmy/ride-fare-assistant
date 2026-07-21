# T1 — Modeled vs. actual fare gap

**Goal:** find out how close a *modeled* fare (what the autonomous watcher would
compute from rate cards) is to the *actual* fare you see in the Lyft app. This
one measurement decides whether the "when to look" watcher is worth building.

**Why it matters:** the watcher can only ever know the modeled fare. If modeled
tracks reality within a few percent, its "good time to look now" pings are
trustworthy. If it's wildly off, the autonomous layer is weak and we rethink
before writing any watcher code.

## How to fill this in

When you're about to take a ride you were taking anyway:

1. Open Lyft, note the **actual** Standard fare it shows you (and Wait & Save if offered).
2. Get a **modeled** estimate for the same route at the same moment. For T1 this
   can just be a rate-card comparison site (e.g. a Lyft fare calculator) — you're
   only checking rough agreement, not building anything yet.
3. Add a row below. Takes ~30 seconds.

Aim for ~10–15 rows across different times/days (some rush hour, some quiet) so
you see the gap under different conditions, not just one.

## Observations

| # | date | time | day | route | modeled $ | actual $ | gap $ | gap % | surge? | wait&save $ | notes |
|---|------|------|-----|-------|-----------|----------|-------|-------|--------|-------------|-------|
| 1 |      |      |     | campus→home |     |     |     |     |     |     |     |
| 2 |      |      |     | home→campus |     |     |     |     |     |     |     |
| 3 |      |      |     |       |     |     |     |     |     |     |     |
| 4 |      |      |     |       |     |     |     |     |     |     |     |
| 5 |      |      |     |       |     |     |     |     |     |     |     |
| 6 |      |      |     |       |     |     |     |     |     |     |     |
| 7 |      |      |     |       |     |     |     |     |     |     |     |
| 8 |      |      |     |       |     |     |     |     |     |     |     |
| 9 |      |      |     |       |     |     |     |     |     |     |     |
| 10|      |      |     |       |     |     |     |     |     |     |     |

- **gap $** = actual − modeled  •  **gap %** = gap $ ÷ actual × 100
- **surge?** = was Prime Time / a surge indicator showing?

## Reading the results (decide after ~10–15 rows)

- **Typical gap under ~10–15%, and modeled moves the same direction as actual**
  (up at rush hour, down when quiet) → modeled is a usable signal. **Build the
  watcher.**
- **Gaps often 25%+, or modeled flat while actual swings** → modeled misses the
  dynamic part that matters. **Don't build the watcher yet;** lean on the
  screenshot-capture path and revisit.
- **Watch surge rows especially** — that's where modeled estimates drift most,
  and where a wrong "good time to look" ping would be most annoying.

Record the verdict as a new entry in `decisions.md` when you've got enough rows.
