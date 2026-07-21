# ride-fare-assistant

A personal tool to spend less on rideshare without babysitting the app.

**The problem:** rideshare fares swing a lot for the same route (dynamic pricing
+ personalized promos + Wait & Save). Opening the app repeatedly to catch a good
price is the chore this project wants to remove.

**Current phase: Stage 0 — data-source discovery.** We are *not* building the
full app yet. The one question that decides whether this project is even
possible is: *can the fare be collected automatically and safely?* That is being
investigated before any `log.py` or database is written.

Read [`docs/feasibility.md`](docs/feasibility.md) first — it's the actual output
of this phase.

## What we've established

- No authorized automated source exists for your **personalized** live fare
  (the dip + Wait & Save). See feasibility doc, options A–D.
- A **modeled** fare (from published rate cards) *can* be collected automatically
  and lawfully, but it's generic — it won't see your specific dip.
- Direction: a **hybrid** — autonomous modeled-fare tracking to learn cheap
  windows and ping you when to look, plus a low-friction capture of your *real*
  fare (screenshot->OCR first) when you open the app.

## Repo layout (discovery-shaped, deliberately small)

```
ride-fare-assistant/
├── docs/
│   ├── feasibility.md   # the investigation + verdicts (start here)
│   ├── decisions.md     # running log of decisions and why
│   └── schema.md        # agreed data schema, as a design note (not code yet)
└── experiments/         # small spikes to answer open tasks T1–T4
    ├── route_info.py
    └── extract_from_screenshot.py
```

Directories appear when a file needs a home — not before. No empty
`app/ models/ collectors/` placeholders.

## Open tasks

Tracked at the bottom of `docs/feasibility.md` (T1–T4). MVP coding is gated
behind T1 (modeled-fare accuracy) and T2 (OCR reliability).

## Status

Stage 0, in progress. Nothing here books rides or accesses Lyft automatically.
