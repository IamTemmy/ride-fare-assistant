# Data schema (design note)

Agreed shape for a single fare observation. Written here as a design reference —
**not yet implemented as code**, because collection method is still open (Stage 0).
When we build storage, SQLite is the intended target (queryable by route + time).

## `observation`

| field | type | notes |
|---|---|---|
| `id` | int | autoincrement |
| `timestamp` | text (ISO 8601 + tz) | backbone of every "when is it cheap" query |
| `route_id` | text | stable label for a pickup->dropoff pair, e.g. `home_to_campus` |
| `ride_type` | text | Standard, XL, Lux, ... — kept separate; they move differently |
| `quoted_price` | real | the standard fare shown |
| `wait_save_price` | real, nullable | Wait & Save fare if offered |
| `wait_save_minutes` | int, nullable | wait window for that price |
| `pickup_eta_min` | int, nullable | proxy for how tight supply is |
| `surge_flag` | int (0/1) | Prime Time / surge indicated |
| `source` | text | `modeled` \| `ocr` \| `on_device` \| `manual` — trust/provenance |

Derive `day_of_week` and `hour` at query time from `timestamp`; don't store them.

## `route` (lookup)

| field | type | notes |
|---|---|---|
| `route_id` | text | primary key |
| `pickup` | text | label or coords |
| `dropoff` | text | label or coords |
| `distance_km` | real | from maps API, cached |
| `typical_duration_min` | real | from maps API, cached |

## Baseline / "unusually low" (analysis, later)

- Bucket = `route_id` x day_type (weekday/weekend) x coarse time block.
- v1 flag: `current < mean * (1 - threshold)`, threshold ~0.15–0.20 (percent drop;
  works with little data).
- v2 flag: `current < mean - 1*std` (z-score; adapts to route volatility).
- Cold start: no alerts until a bucket has ~5–8 observations.
