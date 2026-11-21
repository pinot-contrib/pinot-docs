# Pinot docs catch-up — 2026-11-21 UTC

Reconciled 62 post-checkpoint master merges; 19 docs PRs merged and linked upstream, 43 skipped, 0 pending. Checkpoint: 2026-11-20T21:54:13Z.

IntentLab continued triggering, but its two latest inspected sessions only showed the kickoff prompt. The last durable checkpoint was 2026-11-14T02:52:16Z ([upstream #20167](https://github.com/apache/pinot/pull/20167), [docs #1182](https://github.com/pinot-contrib/pinot-docs/pull/1182)). Neither schedule was changed.

Coverage: GitHub merged timestamps matched the 62 first-parent Apache Pinot master changes through `92468bf3d1`. Local docs validation passed with zero broken links and 10 existing anchor warnings; merged follow-ups passed four hosted checks at their exact heads.

Slack: One catch-up summary delivered (HTTP 200).

## Triage decisions

- [#20111](https://github.com/apache/pinot/pull/20111) — Reject startReplaceSegments forceCleanup over a concurrently completed entry. Concurrency guard for replace-segments cleanup; no request or recovery-procedure change.
- [#19776](https://github.com/apache/pinot/pull/19776) — Upload realtime segment metadata tar to deep store and keep it in Deleted_Segments. Merged [#1185](https://github.com/pinot-contrib/pinot-docs/pull/1185); [upstream comment](https://github.com/apache/pinot/pull/19776#issuecomment-7056269146)
- [#20162](https://github.com/apache/pinot/pull/20162) — Count filtered and dropped stream rows on their own meters. Merged [#1183](https://github.com/pinot-contrib/pinot-docs/pull/1183); [upstream comment](https://github.com/apache/pinot/pull/20162#issuecomment-7056238608)
- [#20267](https://github.com/apache/pinot/pull/20267) — Bump bouncycastle.version from 1.86 to 1.87. Dependency update only; no documented user-facing change.
- [#20270](https://github.com/apache/pinot/pull/20270) — Bump org.apache.maven:apache-maven from 3.10.0 to 3.10.1. Dependency update only; no documented user-facing change.
- [#20273](https://github.com/apache/pinot/pull/20273) — Bump com.azure:azure-sdk-bom from 1.3.9 to 1.3.10. Dependency update only; no documented user-facing change.
- [#20269](https://github.com/apache/pinot/pull/20269) — Bump org.jline:jline from 4.5.0 to 4.7.0. Dependency update only; no documented user-facing change.
- [#20272](https://github.com/apache/pinot/pull/20272) — Bump org.apache.fory:fory-json from 1.7.7 to 1.7.8. Dependency update only; no documented user-facing change.
- [#20274](https://github.com/apache/pinot/pull/20274) — Bump software.amazon.awssdk:bom from 2.57.12 to 2.59.0. Dependency update only; no documented user-facing change.
- [#20268](https://github.com/apache/pinot/pull/20268) — Bump wire.version from 7.1.2 to 7.2.1. Dependency update only; no documented user-facing change.
- [#20271](https://github.com/apache/pinot/pull/20271) — Bump org.apache.maven:maven-core from 3.10.0 to 3.10.1. Dependency update only; no documented user-facing change.
- [#20247](https://github.com/apache/pinot/pull/20247) — Fix compatibility verifier readiness and preserve startup diagnostics. Compatibility verification harness and diagnostics only.
- [#20249](https://github.com/apache/pinot/pull/20249) — Retune the bulk primitive-array thresholds to 96 values for reads and 256 for writes. Internal serialization threshold tuning; no configuration or wire contract change.
- [#20260](https://github.com/apache/pinot/pull/20260) — Fix idle-permit race in PrioritySchedulerTest. Test synchronization only.
- [#20171](https://github.com/apache/pinot/pull/20171) — Fix shared time boundary strategy state across logical table requests. Corrects shared planner state for logical table requests; no time-boundary contract change.
- [#20137](https://github.com/apache/pinot/pull/20137) — Let stream decoders ask the consumer to retry a message instead of dropping it. Merged [#1184](https://github.com/pinot-contrib/pinot-docs/pull/1184); [upstream comment](https://github.com/apache/pinot/pull/20137#issuecomment-7056246052)
- [#20266](https://github.com/apache/pinot/pull/20266) — Keep the upsert out-of-order flag non-null under null handling. Restores the existing documented boolean out-of-order flag under null handling.
- [#20261](https://github.com/apache/pinot/pull/20261) — Keep FORCE_OVERWRITE partial-upsert columns null when the update is null. Restores the already documented FORCE_OVERWRITE semantics for incoming nulls.
- [#20278](https://github.com/apache/pinot/pull/20278) — Fix flaky latency assertions in QueryRoutingTest. Flaky test assertion fix only.
- [#20281](https://github.com/apache/pinot/pull/20281) — Fix Kafka startup script race in schema registry tests. Kafka startup script race in schema registry tests only.
- [#20010](https://github.com/apache/pinot/pull/20010) — Share the per-table ZK metadata read and deep-store listing in RetentionManager. Retention manager internal caching; no retention configuration or policy change.
- [#20287](https://github.com/apache/pinot/pull/20287) — Bump io.github.hakky54:ayza-bom from 10.1.0 to 10.1.1. Dependency update only; no documented user-facing change.
- [#19775](https://github.com/apache/pinot/pull/19775) — Mask stream credentials in StreamConfig#toString() and table add/update logs. Masks credentials in logging; no change to stream credential configuration.
- [#20286](https://github.com/apache/pinot/pull/20286) — Bump software.amazon.awssdk:bom from 2.59.0 to 2.59.1. Dependency update only; no documented user-facing change.
- [#20289](https://github.com/apache/pinot/pull/20289) — Bump org.codehaus.mojo:versions-maven-plugin from 2.25.1 to 2.25.2. Dependency update only; no documented user-facing change.
- [#20099](https://github.com/apache/pinot/pull/20099) — Count only table-serving brokers in the MSE query throttler and run oversize queries alone. Merged [#1189](https://github.com/pinot-contrib/pinot-docs/pull/1189); [upstream comment](https://github.com/apache/pinot/pull/20099#issuecomment-7056268215)
- [#20277](https://github.com/apache/pinot/pull/20277) — Fix MSE literal folding regressions from #19948. Restores existing MSE literal and cast semantics; no new syntax or operator action.
- [#18758](https://github.com/apache/pinot/pull/18758) — Add dictionary-based TEXT index option (buildOnDictionary). Merged [#1190](https://github.com/pinot-contrib/pinot-docs/pull/1190); [upstream comment](https://github.com/apache/pinot/pull/18758#issuecomment-7056267920)
- [#20279](https://github.com/apache/pinot/pull/20279) — Make the realtime multi-value limit configurable. Merged [#1191](https://github.com/pinot-contrib/pinot-docs/pull/1191); [upstream comment](https://github.com/apache/pinot/pull/20279#issuecomment-7056267607)
- [#20288](https://github.com/apache/pinot/pull/20288) — Bump com.github.luben:zstd-jni from 1.5.7-26 to 1.5.7-28. Dependency update only; no documented user-facing change.
- [#20262](https://github.com/apache/pinot/pull/20262) — Do not fail the query when the server has not set up the table and all segments are optional. Corrects internal optional-segment handling; no new setting or query syntax.
- [#20282](https://github.com/apache/pinot/pull/20282) — Fix offline upsert integration test readiness. Offline upsert integration test readiness only.
- [#20091](https://github.com/apache/pinot/pull/20091) — Add an option to resolve GROUP BY names to SELECT aliases before columns in MSE. Merged [#1192](https://github.com/pinot-contrib/pinot-docs/pull/1192); [upstream comment](https://github.com/apache/pinot/pull/20091#issuecomment-7056267241)
- [#19887](https://github.com/apache/pinot/pull/19887) — Gate ingestion Groovy compilation without blocking query Groovy. Merged [#1193](https://github.com/pinot-contrib/pinot-docs/pull/1193); [upstream comment](https://github.com/apache/pinot/pull/19887#issuecomment-7056266893)
- [#20280](https://github.com/apache/pinot/pull/20280) — Add a routing customizer hook to the time-series broker path. Protected time-series broker extension hook; no OSS deployment setting or query contract change.
- [#20244](https://github.com/apache/pinot/pull/20244) — Allow sun.misc.Unsafe memory access on JDK 24+ and warn when Netty runs without it. Merged [#1188](https://github.com/pinot-contrib/pinot-docs/pull/1188); [upstream comment](https://github.com/apache/pinot/pull/20244#issuecomment-7056268521)
- [#20307](https://github.com/apache/pinot/pull/20307) — Bump org.codehaus.plexus:plexus-xml from 3.1.0 to 3.1.1. Dependency update only; no documented user-facing change.
- [#20308](https://github.com/apache/pinot/pull/20308) — Bump org.webjars:swagger-ui from 5.34.1 to 5.35.0. Dependency update only; no documented user-facing change.
- [#20302](https://github.com/apache/pinot/pull/20302) — Enable the Java Vector API in Pinot Docker images. Merged [#1200](https://github.com/pinot-contrib/pinot-docs/pull/1200); [upstream comment](https://github.com/apache/pinot/pull/20302#issuecomment-7056264681)
- [#20039](https://github.com/apache/pinot/pull/20039) — Emit a minion subtask queue-stall gauge that a long but draining job does not trip. Merged [#1194](https://github.com/pinot-contrib/pinot-docs/pull/1194); [upstream comment](https://github.com/apache/pinot/pull/20039#issuecomment-7056266555)
- [#20296](https://github.com/apache/pinot/pull/20296) — Prevent Lucene class initialization deadlock during server startup. Lucene startup deadlock fix; no operator action or new option.
- [#19873](https://github.com/apache/pinot/pull/19873) — Reject MSE mailbox streams and stage plans that reach the wrong server. Internal MSE transport validation; no supported protocol use or operator action changes.
- [#20136](https://github.com/apache/pinot/pull/20136) — Verify broker hostname when the Java client uses a custom SSLContext. Merged [#1195](https://github.com/pinot-contrib/pinot-docs/pull/1195); [upstream comment](https://github.com/apache/pinot/pull/20136#issuecomment-7056266184)
- [#20304](https://github.com/apache/pinot/pull/20304) — Require patched OpenJDK in Pinot container builds. Container build and CI patch-level enforcement. The upstream Docker README already covers the changed build requirements.
- [#20305](https://github.com/apache/pinot/pull/20305) — Add scope-aware discovery of referenced table identifiers. Internal SQL table-reference discovery helper; no supported SQL syntax change.
- [#20299](https://github.com/apache/pinot/pull/20299) — Use mmap for final immutable HNSW merges by default. Merged [#1196](https://github.com/pinot-contrib/pinot-docs/pull/1196); [upstream comment](https://github.com/apache/pinot/pull/20299#issuecomment-7056265874)
- [#20306](https://github.com/apache/pinot/pull/20306) — Bump org.roaringbitmap:RoaringBitmap from 1.6.29 to 1.6.30. Dependency update only; no documented user-facing change.
- [#19536](https://github.com/apache/pinot/pull/19536) — Batch match-all and sorted document-ID iteration. Batch iterator performance optimization with unchanged results.
- [#20309](https://github.com/apache/pinot/pull/20309) — Bump org.codehaus.plexus:plexus-utils from 4.1.0 to 4.2.0. Dependency update only; no documented user-facing change.
- [#20285](https://github.com/apache/pinot/pull/20285) — Do not abort a pauseless commit on the FSM deadline after commit start. Internal pauseless commit deadline handling; no change to user-facing controls or recovery steps.
- [#20315](https://github.com/apache/pinot/pull/20315) — Bump org.apache.httpcomponents.core5:httpcore5 from 5.4.4 to 5.5. Dependency update only; no documented user-facing change.
- [#20058](https://github.com/apache/pinot/pull/20058) — Add instance capabilities to the Helix instance config. Internal Helix capability advertisement groundwork; the built-in capability registry is empty.
- [#20301](https://github.com/apache/pinot/pull/20301) — Reject partial upsert and out-of-order record handling on new pauseless tables. Merged [#1197](https://github.com/pinot-contrib/pinot-docs/pull/1197); [upstream comment](https://github.com/apache/pinot/pull/20301#issuecomment-7056265588)
- [#20106](https://github.com/apache/pinot/pull/20106) — Recheck partition history before starting upsert and dedup consumers. Correctness fix in upsert/dedup consumer admission and partition readiness; no new configuration or operator steps.
- [#20312](https://github.com/apache/pinot/pull/20312) — Add pinot.minion.instance.dataDir config and deprecate un-prefixed dataDir. Merged [#1198](https://github.com/pinot-contrib/pinot-docs/pull/1198); [upstream comment](https://github.com/apache/pinot/pull/20312#issuecomment-7056265302)
- [#20293](https://github.com/apache/pinot/pull/20293) — Support GROUP BY ARRAY_TO_MV in every MSE stage with a new MV aggregate. Merged [#1186](https://github.com/pinot-contrib/pinot-docs/pull/1186); [upstream comment](https://github.com/apache/pinot/pull/20293#issuecomment-7056271198)
- [#19235](https://github.com/apache/pinot/pull/19235) — Honor cluster ingestion Groovy policy during schema validation. Merged [#1199](https://github.com/pinot-contrib/pinot-docs/pull/1199); [upstream comment](https://github.com/apache/pinot/pull/19235#issuecomment-7056265002)
- [#20092](https://github.com/apache/pinot/pull/20092) — Read lookup join dimension columns by their table names. Merged [#1187](https://github.com/pinot-contrib/pinot-docs/pull/1187); [upstream comment](https://github.com/apache/pinot/pull/20092#issuecomment-7056268858)
- [#20325](https://github.com/apache/pinot/pull/20325) — Bump io.github.hakky54:ayza-bom from 10.1.1 to 10.1.2. Dependency update only; no documented user-facing change.
- [#20323](https://github.com/apache/pinot/pull/20323) — Bump software.amazon.awssdk:bom from 2.59.1 to 2.59.2. Dependency update only; no documented user-facing change.
- [#20324](https://github.com/apache/pinot/pull/20324) — Bump at.yawk.lz4:lz4-java from 1.14.0 to 1.14.1. Dependency update only; no documented user-facing change.
- [#20319](https://github.com/apache/pinot/pull/20319) — Extract SQL query options without parsing the executable statement. Merged [#1201](https://github.com/pinot-contrib/pinot-docs/pull/1201); [upstream comment](https://github.com/apache/pinot/pull/20319#issuecomment-7056264352)

## Codex takeover — 2026-11-21T03:03:55.295Z

- [Upstream #20336](https://github.com/apache/pinot/pull/20336) → [docs #1202](https://github.com/pinot-contrib/pinot-docs/pull/1202), merged after four exact-head hosted checks passed and linked upstream ([upstream comment](https://github.com/apache/pinot/pull/20336#issuecomment-7056343266)).
- Resume boundary: `2026-11-21T03:01:28Z`. Reconciled GitHub merge inventory against the first-parent master history.
- Local validation passed: 0 broken file links, 10 existing anchor warnings.
- Slack: Summary delivered (HTTP 200).

## Hourly check — 2026-11-21T04:07:03.980Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-21T03:01:28Z`.

## Hourly OPEN_STRUCT follow-up — 2026-11-21T05:13:08.760Z

- [Upstream #20300](https://github.com/apache/pinot/pull/20300) → [docs #1203](https://github.com/pinot-contrib/pinot-docs/pull/1203), merged after all four hosted checks passed; linked upstream ([upstream comment](https://github.com/apache/pinot/pull/20300#issuecomment-7057755897)).
- Documented dotted sparse JSON lookup, literal-key precedence, and typed sparse conversion. Local validation passed: zero broken file links and 10 existing anchor warnings.
- Reconciled the sole new merge against first-parent master. Checkpoint: `2026-11-21T04:18:54Z`.
- Slack: Summary delivered (HTTP 200).

## Hourly check — 2026-11-21T06:10:35.094Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-21T04:18:54Z`.

## Hourly MSE OPEN_STRUCT follow-up — 2026-11-21T07:09:47.163Z

- [Upstream #20303](https://github.com/apache/pinot/pull/20303) → [docs #1204](https://github.com/pinot-contrib/pinot-docs/pull/1204), merged after all four hosted checks passed; linked upstream ([upstream comment](https://github.com/apache/pinot/pull/20303#issuecomment-7059069733)).
- Documented multi-stage OPEN_STRUCT queries, literal key lookups, and declared versus undeclared SQL types. Local validation passed: zero broken file links and 10 existing anchor warnings.
- Reconciled the sole new merge against first-parent master. Checkpoint: `2026-11-21T06:19:30Z`.
- Slack: Summary delivered (HTTP 200).

## Hourly check — 2026-11-21T08:05:37.155Z

No post-checkpoint merges or pending follow-ups; no docs PRs created and no Slack summary sent. Checkpoint remains `2026-11-21T06:19:30Z`.
