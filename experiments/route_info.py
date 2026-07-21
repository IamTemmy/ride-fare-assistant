"""
Spike (T4): get route distance + duration from a maps/routing provider.

This is the lawful, effortless part of the data pipeline — route geometry never
requires touching Lyft. Goal of the spike: confirm a provider gives usable
distance/time for your city, then pick one on cost + coverage.

Default here: OpenRouteService (free tier, key required). Swap in Mapbox,
Google, or a self-/public-hosted OSRM if you prefer — the shape is the same.

Usage:
    export ORS_API_KEY=your_key_here
    python route_info.py 32.2988,-90.1848 32.3643,-90.2075
    #                    <start lat,lng>   <end lat,lng>

NOTE: not run end-to-end here (no key). Validate before relying on it.
"""
import os
import sys
import requests

ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def parse_latlng(s: str):
    lat, lng = (float(x) for x in s.split(","))
    return lat, lng


def get_route(start, end, api_key):
    # ORS expects [lng, lat] order.
    body = {"coordinates": [[start[1], start[0]], [end[1], end[0]]]}
    r = requests.post(
        ORS_URL,
        json=body,
        headers={"Authorization": api_key, "Content-Type": "application/json"},
        timeout=15,
    )
    r.raise_for_status()
    summary = r.json()["routes"][0]["summary"]
    meters = summary["distance"]
    seconds = summary["duration"]
    return {
        "distance_km": round(meters / 1000, 2),
        "distance_mi": round(meters / 1609.34, 2),
        "duration_min": round(seconds / 60, 1),
    }


def main():
    key = os.environ.get("ORS_API_KEY")
    if not key:
        sys.exit("Set ORS_API_KEY (get a free key at openrouteservice.org).")
    if len(sys.argv) != 3:
        sys.exit("Usage: python route_info.py <lat,lng> <lat,lng>")
    start = parse_latlng(sys.argv[1])
    end = parse_latlng(sys.argv[2])
    print(get_route(start, end, key))


if __name__ == "__main__":
    main()
