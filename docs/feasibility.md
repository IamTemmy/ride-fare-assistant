# Feasibility: can we collect Lyft fares automatically and safely?

**Status:** Stage 0 (data-source discovery). This document is the deliverable.
**Question that gates the whole project:** is there an authorized or reasonably
safe way to obtain the fare — ideally the *personalized* fare, including the
dip and Wait & Save — with little or no manual effort?

**Short answer:** No authorized automated source exists for your *personalized*
live fare. A fully-automatic system can only be built on a *modeled* fare, which
is generic and will not see your specific dip. Capturing your real fare requires
you to have the app open; the most it can be reduced to is a low-friction
capture (screenshot -> OCR, or on-device screen reading) at that moment.

---

## The three "fares" — they are not the same problem

The word "fare" hides three different things with three different feasibilities.
Keeping them separate is the whole insight.

| "Fare" | What it is | Auto-collect? | Lawful? | Sees your dip / Wait & Save? |
|---|---|---|---|---|
| Route distance + time | Geometry of the trip | Yes | Yes (maps APIs) | n/a (input, not price) |
| **Modeled** fare | base + per-mile + per-min + surge guess, from published rate cards | Yes | Yes | **No** — generic estimate |
| **Personalized** fare | the number in *your* app: promos, dips, Wait & Save | Only via your session | No (see ToS) | Yes |

Consequence: **a zero-effort system can only be built on the modeled fare, and
the modeled fare structurally cannot catch "yours just dropped to $7."**

---

## Options considered

### A. Official Lyft developer API — CLOSED
The public developer API (developer.lyft.com) that once returned cost estimates
is discontinued and not accepting new applications. Official SDKs (Go, Node,
iOS) are marked deprecated and unsupported. Verdict: **dead end.**

### B. Lyft Concierge / Business API — WRONG TOOL
Still exists, but gated behind a business relationship and built for
organizations dispatching rides *on behalf of clients*, priced to the business.
It does not expose consumer promos, personalized dips, or Wait & Save (those are
tied to a consumer account). Verdict: **does not provide the data we care about.**

### C. Third-party fare APIs / aggregators — MODELED ONLY
Tools like RideWise, RideGuru, Payfair, FareEstimate work and are lawful, but
they compute from *published rate cards*, not live personalized quotes (their own
disclaimers say so: "an estimate, not a live quote"). Older open-source repos
that hit a real Lyft endpoint depend on developer credentials that can no longer
be issued. Verdict: **useful for the modeled fare, useless for the personal dip.**

### D. Automating your logged-in app (headless API / UI automation) — UNSAFE
This is the only route that would surface your *personalized* fare + Wait & Save.
It is also automated access to an authenticated service:
- ToS: app terms broadly prohibit automated / bulk access; the "public data"
  scraping defense (hiQ v. LinkedIn) does **not** extend to data behind a login.
- Enforcement: Lyft runs automated fraud/abuse detection and ToS enforcement;
  high-frequency polling of your session is exactly what that catches.
- Risk asset: the account being banned is the one you depend on for transport.
Verdict: **off the table.** (Not detailing circumvention; the point is that it
is the wrong trade regardless of technique.)

### E. On-device passive screen reading (Android Accessibility service) — GRAY
Middle path: a service on *your own device* reads whatever fare is on screen
*while you use the app normally*. No automated requests to Lyft's servers — the
only traffic is your own human-paced use. Meaningfully lower risk than (D)
because nothing is driving the app in a loop.
Caveats: still requires you to open the app; Accessibility is a powerful,
sensitive permission; and whether it brushes ToS needs an explicit read of the
current consumer Terms (open task T3 below). Verdict: **most promising
low-friction path, but unresolved — investigate before relying on it.**

### F. Voluntary screenshot -> OCR — SAFE FALLBACK
You screenshot the fare screen and hand the image to the tool, which OCRs the
ride types, prices, wait time, and stamps the time. Fully lawful (you provide
your own data voluntarily; no automated access to Lyft). Friction: one share/tap
when you're already looking at the app. Verdict: **the safe fallback**, and the
one to prototype first (see experiments/extract_from_screenshot.py).

---

## The friction ladder (honest ranking)

From "does everything for you" to "you type it in":

1. **Modeled fare, fully autonomous** — no action from you, but never sees your
   real dip. Good for *learning cheap windows* and *deciding when to ping you*.
2. **On-device passive capture (E)** — you open the app when pinged (you'd do
   that anyway to book); the fare is read locally, no typing. *Unresolved ToS.*
3. **Screenshot -> OCR (F)** — you open the app + one share. *Safe.*
4. **Manual typing** — rejected by you, correctly.

There is **no rung** that both (a) sees your personalized dip and (b) needs zero
action from you and (c) is safe. That rung requires (D). Accepting that boundary
is the key design decision.

---

## Recommended architecture (given the boundary)

A **hybrid**:
- **Autonomous layer:** maps API for route info + modeled fare on a schedule ->
  learn each route's cheap windows -> **ping you when it's historically a good
  time to look.** Needs nothing from you day to day.
- **Capture layer:** when you open the app (ideally because we pinged you), grab
  your *real* fare with near-zero friction — screenshot->OCR now (F), on-device
  reader later if T3 clears (E). This enriches the dataset with true personalized
  fares over time and sharpens the model.

What this can honestly promise: *"For your campus route, weekday early-afternoon
is usually your cheapest window — go look now."* Plus a growing record of your
actual fares. What it **cannot** promise: an autonomous alert about your specific
$7 dip with zero action. That version isn't lawfully buildable.

---

## Open discovery tasks (before writing MVP code)

- **T1 — Modeled-fare accuracy.** How close is a rate-card estimate to your real
  fare on 2–3 of your routes? Collect a handful of paired (modeled, actual)
  points and measure the gap. If it's wildly off, the autonomous layer is weak.
- **T2 — OCR reliability.** Does extract_from_screenshot.py reliably pull all
  fields off a real Lyft screenshot (multiple ride types, Wait & Save row)?
- **T3 — Terms read for (E).** Read the *current consumer* Lyft Terms of Service
  and note the exact automated-access / interference clauses. Decide whether an
  on-device Accessibility reader is defensible or off-limits.
- **T4 — Route/maps provider.** Pick one (OpenRouteService / Mapbox / Google /
  OSRM) on cost + coverage for your city. See experiments/route_info.py.

Only after T1–T2 (and T3 if pursuing E) do we commit to MVP code.
