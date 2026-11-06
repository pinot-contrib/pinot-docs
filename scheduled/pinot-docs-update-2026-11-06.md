# Pinot docs automation — 2026-11-06 (UTC)

## Run run-20261106T000127Z-opus48-927

- **Model:** Opus 4.8 (claude-opus-4-8), IntentLab scheduled hourly triage.
- **Result:** 1 docs-relevant PR processed → 1 docs PR created and merged.

### Preflight
- GitHub auth: `xiangfu0` (GH_TOKEN; rate_limit=15000 confirms authenticated).
- Access: apache/pinot = write (comment-capable); pinot-contrib/pinot-docs = admin (push/merge-capable).
- pinot checkout clean on master; docs cloned to /workspace/pinot-docs on `latest`, clean.
- Durable store (`automation-state` branch) read OK. Lock + lease both released on entry; no concurrent run. Lock acquired via Contents API CAS and released in the final state commit.

### Coverage / reconciliation
- Incoming checkpoint: `2026-11-05T20:06:50Z`.
- Merged apache/pinot PRs strictly after checkpoint: **1** — #20112 @ `2026-11-05T23:14:56Z`.
- Triple-verified: search/issues `merged:>cp`=1; pulls API newest merged=#20112; apache/master HEAD `0a53497f`=#20112. Full coverage, no gaps.

### Decisions
| Upstream PR | Decision | Docs PR | Notes |
|---|---|---|---|
| [#20112](https://github.com/apache/pinot/pull/20112) — Consolidate Kafka ingestion on the Kafka 4 plugin | docs_created | [#1165](https://github.com/pinot-contrib/pinot-docs/pull/1165) (merged) | Kafka 3.0 plugin removed; Kafka 4 is the sole connector and default |

### Docs change detail (#20112 → docs #1165)
Verified against merged code, not just the PR description:
- `StreamConfig.DEFAULT_CONSUMER_FACTORY_CLASS_NAME_STRING` now points to `kafka40` (default when consumer factory unset).
- `PluginManager` aliases old factory class names (`impl.kafka2`, `kafka20`, `impl.kafka3`, `kafka30`) and plugin names (`pinot-kafka-2.0`, `pinot-kafka-3.0`) directly to Kafka 4 (aliases not chained); stored table configs unchanged.
- `KafkaConfigUtils` translates `auto.include.jmx.reporter` → `metric.reporters` (preserving Kafka 3 JMX behavior) and aliases the removed `OAuthBearerLoginCallbackHandler`.
- Kafka 4 client supports brokers **2.1+** (corrected the prior docs claim of "4.0+"); OAuth sources require the `org.apache.kafka.sasl.oauthbearer.allowed.urls` JVM allowlist.

Pages updated:
- `build-with-pinot/ingestion/stream-ingestion/kafka-connector-versions.md`
- `build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md`

### Validation
- `git diff --check`: clean.
- `scripts/validate-docs.py --summary-only`: **PASS** (638 files, 3563 links). 10 pre-existing broken-anchor warnings, all in unrelated files; none introduced here, and the new internal anchor resolves.
- Docs PR #1165 checks: Validate changed docs PASS, Full docs audit PASS, GitBook ×2 PASS.

### Outcome
- Docs PR #1165 squash-merged (merge `cf148970`, `2026-11-06T00:06:09Z`).
- Upstream comment: https://github.com/apache/pinot/pull/20112#issuecomment-6672872414
- **Checkpoint advanced** `2026-11-05T20:06:50Z` → `2026-11-05T23:14:56Z`.
- Ledger 73 → 74 entries. Slack summary sent (new docs PR). State/memory/report persisted via Contents API CAS; lock + lease released.
