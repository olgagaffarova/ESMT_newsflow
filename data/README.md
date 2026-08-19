# Generated data

The collector creates these files automatically:

- `news.csv` — deduplicated articles retained for 365 days;
- `collector_status.csv` — result of the latest collection attempt;
- `run_state.json` — timestamp used to distinguish the first backfill from later incremental runs.

Do not create these files manually. The first successful GitHub Actions run will add them.

