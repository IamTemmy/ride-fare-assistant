# Decision log

Short, dated entries. Newest at top. Records *what we decided and why* so the
reasoning survives.

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
