---
description: Reload a table segment in Apache Pinot.
---

# Reload a table segment

When Pinot writes data to segments in a table, it saves those segments to a deep store location specified in your [table configuration](../reference/configuration-reference/table.md), such as a storage drive or Amazon S3 bucket.

{% hint style="info" %}
If a **new column is added to your table or schema configuration during ingestion**, incorrect data may appear in the consuming segment(s). To ensure accurate values are reloaded, see how to [add a new column during ingestion](../build-with-pinot/ingestion/ingestion-level-transformations.md#add-a-new-column-during-ingestion).&#x20;
{% endhint %}

## Use the Pinot Controller API to reload segments

Pinot exposes three reload-related controller endpoints:

```
POST /segments/{tableName}/reload
POST /segments/{tableName}/{segmentName}/reload
GET /segments/segmentReloadStatus/{jobId}
```

The reload requests are asynchronous. Pinot returns a reload job ID, and you can poll that job ID until the reload finishes.

### Reload all segments in a table

To reload all segments for a table, use:

```
POST /segments/{tableName}/reload
```

`tableName` can be either a typed table name such as `myTable_OFFLINE`, or a raw table name such as `myTable`.

Supported query parameters:

| Parameter | Description |
| --- | --- |
| `type` | Optional table type filter when the path uses a raw table name. Supported values are `OFFLINE` and `REALTIME`. |
| `forceDownload` | Re-download immutable segments from deep store before reloading. Defaults to `false`. |
| `targetInstance` | Send reload messages only to the specified server instance. |
| `instanceToSegmentsMap` | JSON map of server instance to segment list. When present, Pinot reloads only the listed segments on the listed servers. |

Example:

```bash
curl -X POST "http://localhost:9000/segments/baseballStats/reload?type=OFFLINE&forceDownload=true" \
  -H "accept: application/json"
```

When `forceDownload=true` and you pass a raw table name without a type, Pinot automatically limits the request to the `OFFLINE` table because forced deep-store download is only supported for immutable segments.

If you use `instanceToSegmentsMap`, URL-encode the JSON map and send it as a query parameter.

Typical response:

```json
{
  "status": "{\"baseballStats_OFFLINE\":{\"numMessagesSent\":\"24\",\"reloadJobId\":\"6b2f9d35-0d3f-4ef5-91db-f77cb6fdd1c0\",\"reloadJobMetaZKStorageStatus\":\"SUCCESS\"}}"
}
```

The `status` field is a JSON string keyed by table name. Each table entry includes the submitted `reloadJobId`, the number of reload messages sent to servers, and whether Pinot successfully persisted job metadata in ZooKeeper.

### Reload segments in a time range

To reload only segments whose time column falls within a specified time window, use the optional `startTimestamp` and `endTimestamp` query parameters:

```
POST /segments/{tableName}/reload?startTimestamp=<ms>&endTimestamp=<ms>
```

This approach is significantly more efficient than reloading the entire table when you only need to reload recent data.

Supported query parameters (in addition to the standard `type`, `forceDownload`, and `targetInstance`):

| Parameter | Type | Description |
| --- | --- | --- |
| `startTimestamp` | long | Start of the time window in milliseconds since epoch (inclusive). Segments are selected if their time range overlaps with `[startTimestamp, endTimestamp)`. |
| `endTimestamp` | long | End of the time window in milliseconds since epoch (exclusive). |
| `excludeOverlapping` | boolean | When `true`, only reload segments whose time range is fully contained within `[startTimestamp, endTimestamp)`. When `false` (default), also reload segments that partially overlap the window. |

**Prerequisites:**
- The table must have a time column defined in its table configuration.
- Segments without time metadata will not match a time window and will not be reloaded.

**Examples:**

Reload segments in a one-month window:

```bash
curl -X POST "http://localhost:9000/segments/baseballStats/reload?startTimestamp=1740787200000&endTimestamp=1743465600000" \
  -H "accept: application/json"
```

Reload only segments fully contained within the window (no partial overlaps):

```bash
curl -X POST "http://localhost:9000/segments/baseballStats/reload?startTimestamp=1740787200000&endTimestamp=1743465600000&excludeOverlapping=true" \
  -H "accept: application/json"
```

Combine with other parameters (e.g., force download and target a specific instance):

```bash
curl -X POST "http://localhost:9000/segments/baseballStats/reload?type=OFFLINE&forceDownload=true&startTimestamp=1740787200000&endTimestamp=1743465600000" \
  -H "accept: application/json"
```

Time-range filtering is supported on both the table-level endpoint (`POST /segments/{tableName}/reload`) and the segment-level endpoint (`POST /segments/{tableName}/{segmentName}/reload`).

Added in Pinot 1.6.


### Reload one segment

To reload a single segment from a table, use:

```
POST /segments/{tableName}/{segmentName}/reload
```

Supported query parameters:

| Parameter | Description |
| --- | --- |
| `forceDownload` | Re-download the segment from deep store before reloading. Defaults to `false`. |
| `targetInstance` | Reload the segment only on the specified server instance. |

Example:

```bash
curl -X POST "http://localhost:9000/segments/baseballStats_OFFLINE/baseballStats_2026-04-01_0/reload?targetInstance=Server_localhost_8098" \
  -H "accept: application/json"
```

Typical response:

```json
{
  "status": "Submitted reload job id: 4f947c6f-8f51-4dbf-b4e7-a8f4f446ce88, sent 1 reload messages. Job meta ZK storage status: SUCCESS"
}
```

If the table path omits the type suffix, Pinot derives the table type from the segment name.

### Check reload job status

To check the progress of a submitted reload job, use the `reloadJobId` returned by either reload endpoint:

```bash
curl -X GET "http://localhost:9000/segments/segmentReloadStatus/6b2f9d35-0d3f-4ef5-91db-f77cb6fdd1c0" \
  -H "accept: application/json"
```

Typical response:

```json
{
  "status": "IN_PROGRESS",
  "timeElapsedInMinutes": 0.6,
  "estimatedTimeRemainingInMinutes": 1.4,
  "totalSegmentCount": 24,
  "successCount": 10,
  "totalServersQueried": 6,
  "totalServerCallsFailed": 0,
  "failureCount": 0,
  "metadata": {
    "jobId": "6b2f9d35-0d3f-4ef5-91db-f77cb6fdd1c0"
  },
  "segmentReloadFailures": []
}
```

### Check whether a table needs reload

Before reloading, you can ask Pinot whether any servers think the table needs reload:

```bash
curl -X GET "http://localhost:9000/segments/baseballStats_OFFLINE/needReload?verbose=true" \
  -H "accept: application/json"
```

This endpoint requires a typed table name. With `verbose=true`, Pinot includes per-server decisions:

```json
{
  "needReload": true,
  "serverToSegmentsCheckReloadList": {
    "instance123": {
      "needReload": true,
      "instanceId": "instance123"
    }
  }
}
```

## Use the Pinot Admin Console to reload segments

To use the Pinot Admin Console, do the following:

1. From the left navigation menu, select **Cluster Manager**.
2. Under **TENANTS**, select the **Tenant Name**.
3. From the list of tables in the tenant, select the **Table Name**.
4. Do one of the following:
   * To reload all segments, under **OPERATIONS**, click **Reload All Segments**.
   * To reload a specific segment, under **SEGMENTS**, select the **Segment Name**, and then in the new **OPERATIONS** section, select **Reload Segment**.
