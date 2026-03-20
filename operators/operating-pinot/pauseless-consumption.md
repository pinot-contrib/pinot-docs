---
description: Operate and monitor pauseless consumption for real-time tables in Apache Pinot.
---

# Pauseless Consumption

## Overview

In the standard Apache Pinot real-time ingestion architecture, data consumption pauses while the previous segment is being built and uploaded to deep store. Depending on segment size and cluster load, this build-and-upload phase can take several minutes, creating a gap during which the most recent data is not available for queries.

Pauseless consumption, introduced in Pinot 1.4.0, eliminates this gap by allowing servers to continue ingesting data into a new segment while the previous segment is still being built and uploaded. This parallel processing approach significantly reduces the latency between data ingestion and query availability.

{% hint style="info" %}
Pauseless consumption is different from the [Pause ingestion based on resource utilization](pause-ingestion-based-on-resource-utilization.md) feature, which pauses and resumes ingestion based on disk usage thresholds.
{% endhint %}

## How it works

### Standard commit protocol

In the standard commit protocol, the server follows this sequence:

1. Consume data into a mutable segment until a threshold is reached.
2. Build the segment (convert from mutable to immutable format).
3. Send `COMMIT_START` to the controller.
4. Upload the segment to deep store.
5. Send `COMMIT_END_METADATA` to the controller.
6. Begin consuming into a new segment.

During steps 2 through 5, **no new data is consumed**, causing a delay in data freshness.

### Pauseless commit protocol

With pauseless consumption enabled, the sequence changes to:

1. Consume data into a mutable segment until a threshold is reached.
2. Send `COMMIT_START` to the controller.
3. The controller creates ZK metadata for a new consuming segment and updates the ideal state so that the committing segment is marked `ONLINE` and the new segment is marked `CONSUMING`.
4. The server immediately begins consuming into the new segment.
5. In parallel, the server builds and uploads the previous segment.
6. Send `COMMIT_END_METADATA` to the controller to finalize.

Because the new consuming segment is created at `COMMIT_START` (before the build and upload), the server can ingest data continuously without pausing.

For non-committing replicas, the controller responds with `KEEP` instead of `HOLD` after `COMMIT_START`, allowing those replicas to continue ingestion as well.

## Prerequisites

Before enabling pauseless consumption, ensure the following:

* **Peer segment download scheme is configured.** Pauseless consumption requires `peerSegmentDownloadScheme` to be set in the table configuration. This is enforced by validation and is necessary because segments may be marked `ONLINE` in the ideal state before they are uploaded to deep store. Slow replicas rely on peer download to fetch the segment from the committing server.

* **Pinot version 1.4.0 or later.** Pauseless consumption is not available in earlier versions.

## Enabling pauseless consumption

To enable pauseless consumption on a REALTIME table, set `pauselessConsumptionEnabled` to `true` in the `streamIngestionConfig` section of the table configuration:

```json
{
  "tableName": "myTable_REALTIME",
  "tableType": "REALTIME",
  "ingestionConfig": {
    "streamIngestionConfig": {
      "streamConfigMaps": [
        {
          "stream.kafka.topic.name": "myTopic",
          "stream.kafka.broker.list": "kafka:9092",
          "stream.kafka.consumer.type": "lowlevel",
          "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
          "realtime.segment.flush.threshold.rows": "500000"
        }
      ],
      "pauselessConsumptionEnabled": true
    }
  },
  "segmentsConfig": {
    "peerSegmentDownloadScheme": "http"
  }
}
```

{% hint style="warning" %}
You must set `peerSegmentDownloadScheme` (for example, `"http"` or `"https"`) in `segmentsConfig`. Table creation or update will fail validation if pauseless consumption is enabled without this setting.
{% endhint %}

## Configuration options

### Segment flush thresholds

Pauseless consumption supports the same segment flush thresholds as standard real-time ingestion:

| Configuration | Description |
|---|---|
| `realtime.segment.flush.threshold.rows` | Number of rows after which the segment is committed. |
| `realtime.segment.flush.threshold.time` | Time duration after which the segment is committed (for example, `1h`, `30m`). |
| `realtime.segment.flush.threshold.segment.size` | Target segment size. When set, Pinot automatically tunes the row threshold based on previous segment sizes. |

### Size-based threshold

Pinot 1.4.0 also added support for a size-based flush threshold that works with pauseless consumption. When `realtime.segment.flush.threshold.segment.size` is configured, the `FlushThresholdUpdater` updates statistics from committing segments and computes the threshold for new consuming segments. This allows pauseless tables to automatically tune their flush thresholds based on actual segment sizes.

## Disaster recovery

Pauseless consumption introduces new failure scenarios because segments can be marked `ONLINE` in the ideal state before they have been built and uploaded. If the committing server crashes during the build or upload phase, and no other replica has the segment, the segment enters an `ERROR` state with no data on disk.

### Recoverable failures

Failures where at least one server still has the segment data on disk are handled automatically by the `RealtimeSegmentValidationManager`. This covers scenarios such as upload failures and incomplete commit protocol executions. The validation manager identifies which step of the commit protocol failed and takes corrective action.

### Non-recoverable failures (reingestion)

When no server has the segment on disk, Pinot can recover by re-ingesting the data from the upstream source (for example, Kafka). The reingestion flow works as follows:

1. The `RealtimeSegmentValidationManager` detects an `ERROR` segment with no completed replica.
2. The controller selects an alive server from the ideal state for that segment.
3. The controller calls `POST /reingestSegment` on the selected server with the table name and segment name.
4. The server re-consumes data from the stream for the offset range of the failed segment, builds the segment, and uploads it.
5. The controller copies the segment to deep store, updates ZK metadata to `DONE`, and resets the segment to `ONLINE`.

### Disaster recovery modes

For tables with dedup or upsert enabled, reingestion may conflict with data consistency requirements. Dedup tables require strictly ordered ingestion, and re-ingesting a past segment can violate this constraint. To handle this, Pinot provides a `DisasterRecoveryMode` setting in `streamIngestionConfig`:

```json
{
  "ingestionConfig": {
    "streamIngestionConfig": {
      "pauselessConsumptionEnabled": true,
      "disasterRecoveryMode": "DEFAULT"
    }
  }
}
```

| Mode | Behavior |
|---|---|
| `DEFAULT` | Skips the disaster recovery (reingestion) job for dedup and upsert tables, prioritizing data consistency over availability. Failed segments must be resolved manually. |
| `ALWAYS` | Always runs the disaster recovery job, even for dedup and upsert tables. This prioritizes availability over strict dedup/upsert metadata correctness. Use this when fast recovery from data loss is more important than temporary dedup inconsistency. |

{% hint style="info" %}
When using `ALWAYS` mode with dedup tables, dedup metadata may be temporarily inconsistent until a full metadata rebuild is performed after recovery.
{% endhint %}

## Observability

### Metrics

The following metrics have been added for monitoring pauseless consumption:

| Metric | Type | Description |
|---|---|---|
| `pauselessConsumptionEnabled` | Gauge (Server, Controller) | Indicates whether pauseless consumption is enabled. Useful for verifying the feature is active. |
| `segmentBuildFailures` | Counter | Tracks segment build failures during the commit process. In standard ingestion, build failures halt consumption and are immediately visible. In pauseless mode, ingestion continues even after a build failure, so this metric is essential for detecting issues. |
| `reingestionFailures` | Counter | Tracks failures during the reingestion (disaster recovery) process. Applicable only to pauseless tables. |
| `segmentsInErrorState` | Gauge | Number of segments currently in ERROR state. Helps identify segments that need recovery. |
| `segmentsMissingDownloadUrl` | Gauge | Number of segments without a download URL in ZK metadata. Indicates `COMMIT_END_METADATA` failures where the segment was built but the metadata was not finalized. |

### Key things to monitor

* **Segment build failures**: Since ingestion continues after a build failure in pauseless mode, monitor `segmentBuildFailures` to detect problems that would otherwise go unnoticed.
* **Error segments**: Watch `segmentsInErrorState` to identify segments that require manual intervention or reingestion.
* **Reingestion failures**: Monitor `reingestionFailures` to ensure disaster recovery is functioning correctly.
* **Missing download URLs**: A high count of `segmentsMissingDownloadUrl` may indicate systemic issues with the commit protocol.

## Compatibility with upsert and dedup tables

Pauseless consumption is compatible with upsert and dedup tables, with the following considerations:

* **Upsert tables**: Pauseless consumption works with upsert tables. During the build and upload phase, the consuming segment and the committing segment can coexist, and upsert metadata is maintained correctly.
* **Dedup tables**: Pauseless consumption works with dedup tables, but reingestion is disabled by default (`DEFAULT` disaster recovery mode) because dedup requires in-order consumption. Re-ingesting a segment out of order could produce incorrect dedup results. Set `disasterRecoveryMode` to `ALWAYS` if you need automatic disaster recovery at the cost of temporary dedup inconsistency.
* **Partial upsert tables**: Consumption during build is also supported for partial upsert tables.

{% hint style="warning" %}
For dedup tables with pauseless consumption, if a disaster occurs and reingestion is disabled (the default), you may need to perform a manual bulk delete of affected segments and restart ingestion. This is operationally heavy but preserves dedup correctness.
{% endhint %}

## Rebalance considerations

When rebalancing pauseless tables, exercise caution with the following settings:

* **`downtime=true`**: If a segment has not yet been uploaded to deep store and its only replica is moved, the data is permanently lost. Avoid using `downtime=true` on pauseless tables unless you understand the risk.
* **`minAvailableReplicas=0`**: Similar to `downtime=true`, setting this to `0` can result in data loss for segments that exist only in memory on a single server.
* **Replication factor of 1**: With a single replica, any server failure before upload completion causes irrecoverable data loss. Consider using a replication factor of at least 2 for pauseless tables.

Pinot 1.4.0 includes pre-checks that warn operators about these risky configurations during rebalance operations.

## Troubleshooting

### Segments stuck in COMMITTING state

If a segment remains in `COMMITTING` state for an extended period, the server may have failed during the build or upload phase. The `RealtimeSegmentValidationManager` periodic task will detect and attempt to resolve this automatically.

### Segments in ERROR state

Segments in `ERROR` state with no completed replica on any server indicate a non-recoverable failure. If `disasterRecoveryMode` is set to `DEFAULT` for a dedup or upsert table, these segments will not be automatically recovered. Options include:

1. Set `disasterRecoveryMode` to `ALWAYS` to enable automatic reingestion (with the caveat of temporary metadata inconsistency for dedup/upsert tables).
2. Manually delete the affected segments and allow Pinot to re-create them.

### Slow replicas and segment download

Non-committing replicas rely on downloading the segment from the committing server or deep store. Pauseless consumption implements a waited download mechanism that repeatedly checks for the download URL in ZK metadata and attempts peer download. If downloads are consistently slow, consider:

* Increasing the download timeout.
* Ensuring `peerSegmentDownloadScheme` is configured correctly.
* Verifying network connectivity between servers.

## Rollback procedure

To disable pauseless consumption and revert to standard ingestion:

1. Update the table configuration to set `pauselessConsumptionEnabled` to `false`:

```json
{
  "ingestionConfig": {
    "streamIngestionConfig": {
      "pauselessConsumptionEnabled": false
    }
  }
}
```

2. Apply the updated table configuration using the Pinot controller API:

```bash
curl -X PUT "http://<controller>:<port>/tables/myTable_REALTIME" \
  -H "Content-Type: application/json" \
  -d @table-config.json
```

3. Wait for currently committing segments to complete their commit cycle. New segments will follow the standard commit protocol.

4. Verify that the `pauselessConsumptionEnabled` metric reports `0` on all servers hosting the table.

{% hint style="info" %}
Rollback does not require a server restart. The change takes effect for new segment commits after the table configuration is updated.
{% endhint %}

## References

* [Pauseless Consumption Design Document](https://docs.google.com/document/d/1d-xttk7sXFIOqfyZvYw5W_KeGS6Ztmi8eYevBcCrT_c/edit?tab=t.0)
* [Pauseless ingestion without failure scenarios #14741](https://github.com/apache/pinot/pull/14741)
* [Handle failure scenarios without DR #14798](https://github.com/apache/pinot/pull/14798)
* [Disaster Recovery with Reingestion #14920](https://github.com/apache/pinot/pull/14920)
* [Disaster Recovery modes for Pauseless #16071](https://github.com/apache/pinot/pull/16071)
* [Metrics for pauseless observability #15384](https://github.com/apache/pinot/pull/15384)
* [Compatibility for Pauseless Dedup and Upsert #15383](https://github.com/apache/pinot/pull/15383)
* [Size-based threshold for pauseless consumption #15347](https://github.com/apache/pinot/pull/15347)
* [Validations for Pauseless Tables #15567](https://github.com/apache/pinot/pull/15567)
