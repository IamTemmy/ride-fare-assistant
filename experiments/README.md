# Experiments (spikes)

Small, throwaway scripts to answer the open discovery tasks in
`../docs/feasibility.md`. Not production code. Each maps to a task.

| spike | answers | needs |
|---|---|---|
| `route_info.py` | T4 — pick a maps/route provider | an API key (env var) |
| `extract_from_screenshot.py` | T2 — is OCR reliable on a real Lyft screenshot? | Tesseract + a real screenshot |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r ../requirements.txt
# extract_from_screenshot.py also needs the tesseract binary:
#   macOS:  brew install tesseract
#   Ubuntu: sudo apt-get install tesseract-ocr
```

## Notes
- These have not been run end-to-end here (no live keys, no real screenshot).
  Treat them as starting points to validate, not finished tools.
- For T1 (modeled-fare accuracy) there is no spike yet — it's a data-collection
  task: gather a handful of (modeled estimate, actual in-app fare) pairs on your
  real routes and eyeball the gap before trusting the autonomous layer.
