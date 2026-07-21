"""
Spike (T2): turn a Lyft screenshot into structured fields with near-zero effort.

This is the SAFE capture path (option F in feasibility.md): you voluntarily hand
the tool your own screenshot; nothing accesses Lyft automatically. Goal of the
spike: see how reliably plain OCR pulls ride types, prices, Wait & Save minutes,
and a timestamp off a real screen.

Approach here: Tesseract OCR + simple regexes. This is the cheap first pass.
If accuracy is poor on real screenshots (small text, overlapping UI), the more
robust route is a vision model that reads the image directly — worth trying as a
follow-up, but start cheap.

Usage:
    python extract_from_screenshot.py path/to/lyft_screenshot.png

NOTE: not validated here (no real screenshot on hand). The regexes are a
starting point and will need tuning to Lyft's actual layout.
"""
import json
import re
import sys
from datetime import datetime, timezone

try:
    import pytesseract
    from PIL import Image
except ImportError:
    sys.exit("pip install pytesseract pillow  (and install the tesseract binary)")

PRICE = re.compile(r"\$\s?(\d+(?:\.\d{2})?)")
WAIT_SAVE = re.compile(r"wait\s*(?:&|and)?\s*save", re.I)
MINUTES = re.compile(r"(\d+)\s*min", re.I)
# Ride-type labels seen in the Lyft UI; extend as needed.
RIDE_TYPES = ["Wait & Save", "Standard", "Lyft XL", "Extra Comfort", "Lux", "Preferred"]


def ocr(path: str) -> str:
    return pytesseract.image_to_string(Image.open(path))


def parse(text: str) -> dict:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    ride_types = [rt for rt in RIDE_TYPES if any(rt.lower() in ln.lower() for ln in lines)]
    prices = [float(m) for m in PRICE.findall(text)]
    wait_save_present = bool(WAIT_SAVE.search(text))
    wait_min = int(MINUTES.search(text).group(1)) if MINUTES.search(text) else None
    return {
        # timestamp = when captured, not shown on screen. Good enough: user
        # screenshots near the moment they're deciding.
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "ride_types_detected": ride_types,
        "prices_detected": prices,          # review order/mapping against the image
        "wait_save_present": wait_save_present,
        "wait_save_minutes": wait_min,
        "_raw_text": text,                  # keep for debugging the regexes
    }


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python extract_from_screenshot.py <image>")
    result = parse(ocr(sys.argv[1]))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
