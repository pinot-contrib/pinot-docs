# Consistent Push and Rollback

{% hint style="info" %}
**Original design doc**: [https://docs.google.com/document/d/1PUy4wSUPFyEWEW3a88Mipdug3cPj4EpV\_\_lx-BVUTYk/edit?usp=sharing](https://docs.google.com/document/d/1PUy4wSUPFyEWEW3a88Mipdug3cPj4EpV\_\_lx-BVUTYk/edit?usp=sharing)

**Issue**: [https://github.com/apache/pinot/issues/7813](https://github.com/apache/pinot/issues/7813)
{% endhint %}

### Motivation

#### Data Consistency

Pinot supports atomic update on segment level, which means that when data consisting of multiple segments are pushed to a table, as segments are replaced one at a time, queries to the broker during this upload phase may produce inconsistent result due to interleaving of old and new data.

#### Data Rollback

Furthermore, Pinot currently does not support data rollback features. In case of a bad data push, the table owner needs to re-run the flow with the previous data and re-ingest data to Pinot. This end-to-end process can take hours and the Pinot table can potentially be in a bad state during this long period.

The consistent push and rollback protocol allows a user to **atomically switch between data snapshots and rollback to the previous data in the case of a bad data push**. For complete motivation and reasoning, refer to the design doc above. Currently, we only support **OFFLINE table REFRESH use cases**.

### How this works

Segment lineage data structure has been introduced in Zookeeper (under the path `<cluster_name>/PROPERTYSTORE/SEGMENT_LINEAGE/<table_name>`) for keeping track of which segments have been replaced by which new set of segments, as well as corresponding state and timestamp.

```
{
  "id": "<table_name>",
  "simpleFields": {},
  "mapFields": {},
  "listFields": {
    "<segment_lineage_entry_id>": [
      "<segmentsFrom_list>",
      "<segmentsTo_list>",
      "<state>",
      "<timestamp>"
    ]
  }
}
```

When broker answers queries from the users, it will go through the lineage entries and only route to the segments in `segmentsFrom` for those in "IN\_PROGRESS" or "REVERTED" state and the segments in `segmentsTo` for those in "COMPLETED" state, therefore preserving data snapshot atomicity.

Below are the APIs available on the controller to invoke the segment replacement protocol.

1. `startReplaceSegments`: Signifies to the controller that a replacement protocol is about to atomically replace `segmentsFrom`, a source list of segments, by `segmentsTo` , a target list of segments, which then persists a segment lineage entry with "IN PROGRESS" state to Zookeeper and returns its ID.
2. `endReplaceSegments`: Ends the replacement protocol associated with the segment lineage entry ID passed in as a parameter by changing the state to "COMPLETED".
3. `revertReplaceSegments`: Reverts the replacement protocol associated with the segment lineage entry ID passed in as a parameter by changing the state to "REVERTED".

However, we don't typically expect users to invoke these APIs directly.

Instead, consistent push is built into batch ingestion jobs (**currently only supported for the standalone execution framework**).

### How to set up Ingestion Job with Consistent Push

**Step 0:** Adjust the table [storage quota](../reference/configuration-reference/table.md#quota) to 2x that of the original amount. See [#implications-of-enabling-consistent-push](consistent-push-and-rollback.md#implications-of-enabling-consistent-push "mention") for more details.

**Step 1:** Set up config for your OFFLINE, REFRESH table. Enable `consistentDataPush` under IngestionConfig -> BatchIngestionConfig.

```
"tableName": "myTable_OFFLINE",
"tableType": "OFFLINE",
...
...
"ingestionConfig": {
  "batchIngestionConfig": {
    "segmentIngestionType": "REFRESH",
     "segmentIngestionFrequency": "DAILY", // or HOURLY
     "consistentDataPush": true
  }
}
```

**Step 2:** Execute the job by following instructions for[#executing-the-job](../tutorials/data-ingestion/batch-data-ingestion-in-practice.md#executing-the-job "mention").

### How to trigger Data Rollback

**Step 0**: Identify the segment lineage entry ID corresponding to the segment swap that would like to be rolled back by using the `/lineage` REST API to list segment lineage.

**Step 1**: Use the `revertReplaceSegments` REST API to rollback data.

**Step 2**: As a sanity check, use the `/lineage` REST API again to ensure that the corresponding lineage entry is in "REVERTED" state.

### Cleanup

Retention manager manages the cleanup of segments as well as segment lineage data.

On a high level, the cleanup logic is as follows:

1. Cleanup unused segments: For entries in "COMPLETED" state, we remove segments in `segmentsFrom` after the replaced segments retention period has elapsed. For entries in "REVERTED" or "IN\_PROGRESS" state whose timestamp exceeds the lineage entry cleanup retention period, we remove segments in `segmentsTo`.
2. Once all segments in step 1 are cleaned up, we remove the lineage entry.

The cleanup is usually handled in 2 cycles.

Cleanup regarding `startReplaceSegment` API:

1. We proactively remove the first snapshot if the client side is pushing the 3rd snapshot, so we are not exceeding the 2x disk space.
2. If the previous push fails in the middle (IN\_PROGRESS/REVERTED state), we also clean up the `segmentsTo`.

{% hint style="info" %}
While a lineage entry is still live, Pinot keeps lineage-locked segments on the lineage-managed cleanup path and rejects the generic segment delete flow for them by default. If you need the legacy delete behavior during an incident, set `controller.lineage.exclusive.delete.enabled=false` on the controller. Otherwise, finish or revert the lineage entry and let the normal lineage cleanup cycle remove the segments when they become eligible.
{% endhint %}

#### Configurable Retention Periods

By default, `lineageEntryCleanupRetentionPeriod` is 1 day for all tables. `replacedSegmentsRetentionPeriod` defaults to 1 day for `REFRESH` tables and 4 hours for other replacement flows such as `APPEND` tables. You can override both values in the table config under `segmentsConfig` (the `validationConfig` section):

| Property | Description | Default |
|----------|-------------|---------|
| `replacedSegmentsRetentionPeriod` | How long replaced (source) segments are preserved after a lineage entry reaches "COMPLETED" state before Pinot deletes them. Pinot honors this setting for every replacement flow that writes a completed lineage entry. The default is `1d` for `REFRESH` tables and `4h` for other table types. Set it to `0s` if you explicitly want the next retention pass to delete replaced segments immediately. | `1d` for `REFRESH`, `4h` otherwise |
| `lineageEntryCleanupRetentionPeriod` | How long stale "IN\_PROGRESS" or "REVERTED" lineage entries (and their destination segments) are kept before being cleaned up. | `1d` |

Values are human-readable period strings (e.g. `1d`, `12h`, `7d`). Setting `replacedSegmentsRetentionPeriod` to `0s` eliminates the grace window and replaced segments will be deleted on the next retention pass after the lineage is completed.

Example table config snippet:

```json
{
  "tableName": "myTable_OFFLINE",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "365",
    "replacedSegmentsRetentionPeriod": "2d",
    "lineageEntryCleanupRetentionPeriod": "12h"
  },
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "REFRESH",
      "segmentIngestionFrequency": "DAILY",
      "consistentDataPush": true
    }
  }
}
```

### Implications of enabling Consistent Push

1. Enabling consistent push can lead to up to 2x storage usage (assuming data size between snapshots are roughly equivalent) since at any time, we are potentially keeping both replacing and replaced segments.
2. Typically, for the REFRESH use case, users would directly replace segments by uploading segments of the same name. With consistent push, however, a timestamp is injected as the segment name postfix in order to differentiate between replacing and to be replaced segments. The older segments will be cleaned up by the Retention manager after the configured `replacedSegmentsRetentionPeriod` from when the consistent push happened. If you do not set that property, the default is **1 day** for `REFRESH` tables and **4 hours** for other replacement flows.
3. Currently, there is no way to disable consistent push for a table with consistent push enabled, due to the unique segment postfix issue mentioned above. Users will need to create a new table until support for disabling consistent push in-place is implemented.
4. If the push job fails for any reason, the job will rollback all the uploaded segments (`revertReplaceSegments`) to maintain data equivalence prior to the push.
