# Decision log

Short, dated entries. Newest at top. Records *what we decided and why* so the
reasoning survives.

## D4 — Project not pursued (Stage 0 outcome: NO-GO)
**Decision:** Stop the project at the end of Stage 0. Do not build the watcher
or MVP.
**Why:** The feature that made this worth building was a personalized low-fare
alert — "your fare just dropped, book now." That requires the live, in-app,
account-personalized fare, which has no lawful automated source (see
feasibility.md, options A–D): the public API is closed, the Business API is the
wrong scope, third-party tools are modeled-only, and automating the logged-in
session violates Lyft's ToS and risks the account. The only lawful autonomous
signal is the *modeled* rate-card fare, which is a coarse baseline, not the
personalized dip. A single real observation confirmed the gap: on a ~4.3 mi
route, RideGuru modeled ≈ $11.97 while the app showed $9.91 Standard / $7.91
Wait & Save at 21:17 — the modeled baseline could flag "this hour tends to run
cheap," but never the specific live price that was the goal. That coarser
"go look now" signal was judged not worth building for personal use.
**Outcome:** This repo stands as a completed feasibility study, not an
abandoned build. The engineering reasoning in feasibility.md is the deliverable.
**Reversal condition:** revisit only if a lawful, low-effort source of the
personalized fare becomes available (e.g. a first-party consumer API), which
would remove the core blocker.

## D3 — Gate MVP behind data-source discovery
**Decision:** Do not write `log.py` / the database until the data-source
question is resolved. Structure the repo around investigation first.
**Why:** The fare is the most important input. Building storage and analysis
around a data source that turns out to be unsafe or unavailable is wasted work.

## D2 — Manual typing is not the final system
**Decision:** Rule out a workflow that requires manually reading and typing
fares as the steady-state design. Manual entry is at most a temporary
validation step for T1.
**Why:** The project's purpose is to remove the chore of monitoring prices. A
system that needs manual logging every time defeats it. Low-friction capture
(screenshot->OCR, or on-device reading) replaces it.

## D1 — Split "fare" into three problems
**Decision:** Treat route info, modeled fare, and personalized fare as separate
data sources with separate feasibility.
**Why:** They have very different answers. Conflating them led earlier plans to
assume an autonomous personalized-fare feed exists — it doesn't. See
feasibility.md.

## D0 — Personalized live fare has no lawful automated source
**Decision:** Accept that the autonomous "alert me about my personal dip"
version is not lawfully buildable; design the hybrid around that boundary.
**Why:** Public API closed; Business API is wrong scope; third-party tools are
modeled-only; automating the logged-in session violates ToS and risks the
account. Evidence in feasibility.md.
