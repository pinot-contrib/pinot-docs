# pinot-docs automation — durable state branch

This orphan branch (`automation-state`) holds the durable state for the scheduled
automation that converts newly merged `apache/pinot` PRs into `pinot-contrib/pinot-docs`
follow-up PRs (routine `rt_r0leJefO3D`).

**It is intentionally detached from docs content and must never be merged into `latest`.**

## Contract
- Contains **no operational secrets** — no API tokens, no Slack webhook. Those live only
  in the routine runtime and are never committed here.
- `automation-state.json` is the machine-readable source of truth: the merged-at checkpoint
  and the processed-PR ledger.
- `automation-memory.md` is the human-readable running log.
- `scheduled/pinot-docs-update-<YYYY-MM-DD>.md` are per-day run reports (UTC dates).

## Rules
- Never reset or backfill before `last_processed_merged_at`.
- Advance the checkpoint only after completed outcomes or explicit non-relevance decisions,
  never past unprocessed or failed work.
- Updates are made via the GitHub contents/git-data API from the scheduled runner.