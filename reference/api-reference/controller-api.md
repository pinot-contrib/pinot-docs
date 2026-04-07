---
description: Pinot controller API reference.
---

# Controller API Examples

The controller exposes the administrative API surface for cluster, schema, table, segment, tenant, and database operations. The detailed request and response examples live here instead of in the user guide so the reference tree can act as the canonical endpoint index.

## Endpoint Families

| Family | Representative endpoints |
| --- | --- |
| Cluster | `GET /cluster/configs`, `POST /cluster/configs`, `DELETE /cluster/configs/{configName}`, `GET /cluster/configs/groovy/staticAnalyzerConfig`, `POST /cluster/configs/groovy/staticAnalyzerConfig`, `GET /cluster/configs/groovy/staticAnalyzerConfig/default`, `GET /cluster/info` |
| Health and leadership | `GET /health`, `GET /leader/tables` |
| Query validation | `POST /validateMultiStageQuery`, `POST /query/tableNames` |
| Schema | `GET /schemas`, `GET /schemas/{schemaName}`, `POST /schemas`, `PUT /schemas/{schemaName}`, `DELETE /schemas/{schemaName}` |
| Table | `GET /tables`, `POST /tables`, `PUT /tables/{tableName}`, `DELETE /tables/{tableName}`, `POST /tableConfigs/validate` |
| Logical tables | `GET /logicalTables`, `POST /logicalTables`, `PUT /logicalTables/{tableName}`, `DELETE /logicalTables/{tableName}` |
| Segments | `GET /segments/{tableName}/invalidPartitionMetadata`, `POST /segments/{tableName}/reload`, `POST /segments/{tableNameWithType}/uploadFromServerToDeepstore`, `POST /segments/reingested`, `DELETE /deleteSegmentsFromSequenceNum/{tableNameWithType}`, `GET /segments/segmentReloadStatus/{jobId}`, `GET /segments/{tableNameWithType}/needReload` |
| Tenant and instance management | `GET /tenants`, `GET /tenants/{tenantName}`, `GET /instances`, `POST /instances` |

## Swagger UI

The controller hosts the interactive Swagger UI at `http://<controller-host>:<port>/help`. Use it to confirm exact request shapes before issuing destructive calls.

## Operational Examples

```bash
curl -X GET "http://localhost:9000/cluster/configs" -H "accept: application/json"
```

```bash
curl -X DELETE "http://localhost:9000/tables/baseballStats?retention=0d" -H "accept: application/json"
```

```bash
curl -X GET "http://localhost:9000/schemas/baseballStats" -H "accept: application/json"
```

## What this page covered

- The controller endpoint families and their top-level responsibilities.
- The interactive Swagger UI location.
- A few representative request examples for the most common admin flows.

## Next step

If you are about to modify cluster state, use the Swagger UI or the original controller examples page to confirm parameters before running the request.

## Related pages

- [API Reference](README.md)
- [Controller Admin API](controller-admin-api.md)
- [Broker Query API](query-api.md)
- [Broker gRPC API](broker-grpc-api.md)
---
description: Detailed curl examples for commonly used controller endpoints.
---

# Controller API Examples

This page provides detailed `curl` request and response examples for commonly used controller endpoints. For a categorized overview of all Pinot APIs, see the main [API Reference](./).

{% hint style="info" %}
The complete and interactive list of every controller endpoint is available in the Swagger UI at `http://<controller-host>:<port>/help`. For a visual walkthrough of the Swagger UI, see [Controller Admin API](controller-admin-api.md).
{% endhint %}

## Query Validation

### POST /validateMultiStageQuery

Compile one or more SQL statements with the multi-stage engine without executing them. Pinot returns one validation result per input query, in the same order that the queries were submitted.

Use `sql` for a single statement:

```bash
curl -X POST "http://localhost:9000/validateMultiStageQuery" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sql":"SELECT * FROM mytable"}'
```

Use `sqls` for batch validation:

```bash
curl -X POST "http://localhost:9000/validateMultiStageQuery" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"sqls":["SELECT COUNT(*) FROM mytable","SELECT invalidColumn FROM mytable"]}'
```

**Response**

```json
[
  {
    "compiledSuccessfully": true,
    "errorMessage": null,
    "errorCode": null,
    "sql": "SELECT * FROM mytable"
  }
]
```

Each response object contains:

- `compiledSuccessfully`: whether Pinot compiled the query successfully
- `errorMessage`: compiler error text on failure, otherwise `null`
- `errorCode`: Pinot query error code on failure, otherwise `null`
- `sql`: the input SQL string for that result

For static validation, you can also send `tableConfigs` and `schemas` so the controller compiles against the provided table metadata instead of the controller's ZooKeeper-backed table cache. `logicalTableConfigs` and `ignoreCase` are also accepted for this static-cache path. When populating `tableConfigs` and `schemas`, use the same JSON objects returned by `GET /tables/{tableName}` and `GET /schemas/{schemaName}`.

## Cluster

### GET /cluster/configs

List all the cluster configs. These are fetched from Zookeeper from the CONFIGS/CLUSTER/\<clusterName> znode.

**Request**

```
curl -X GET "http://localhost:9000/cluster/configs" -H "accept: application/json"
```

**Response**&#x20;

```
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```

### POST /cluster/configs

Post new configs to cluster. These will get stored in the same znode as above i.e. CONFIGS/CLUSTER/\<clusterName>. These properties are appended to the existing properties if keys are new, else they will be updated if key already exists.&#x20;

**Request**

```
curl -X POST "http://localhost:9000/cluster/configs" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"pinot.helix.instance.state.maxStateTransitions\" : \"20\", \"custom.cluster.prop\": \"foo\"}"
```

**Response**&#x20;

```
{
  "status": "Updated cluster config."
}
```

### DELETE /cluster/configs

Delete a cluster config.&#x20;

**Request**

```
curl -X DELETE "http://localhost:9000/cluster/configs/custom.cluster.prop" 
```

**Response**&#x20;

```
{
  "status": "Deleted cluster config: custom.cluster.prop"
}
```

### Groovy static analysis configs

Pinot stores Groovy static analysis settings as cluster configs. These configs are keyed by:

- `pinot.groovy.all.static.analyzer`
- `pinot.groovy.ingestion.static.analyzer`
- `pinot.groovy.query.static.analyzer`

The ingestion-specific and query-specific configs override `pinot.groovy.all.static.analyzer` for their respective contexts. `POST /cluster/configs/groovy/staticAnalyzerConfig` rejects any other top-level config key.

Each config value is a JSON object with these fields:

- `allowedReceivers`
- `allowedImports`
- `allowedStaticImports`
- `disallowedMethodNames`
- `methodDefinitionAllowed`

### GET /cluster/configs/groovy/staticAnalyzerConfig

Return the currently configured Groovy static analyzer configs, keyed by cluster config name.

**Request**

```bash
curl -X GET "http://localhost:9000/cluster/configs/groovy/staticAnalyzerConfig" -H "accept: application/json"
```

**Response**

```json
{
  "pinot.groovy.all.static.analyzer": {
    "allowedReceivers": [
      "java.lang.String",
      "java.lang.Math",
      "java.util.List",
      "java.lang.Object",
      "java.util.Map"
    ],
    "allowedImports": [
      "java.lang.Math",
      "java.util.List",
      "java.lang.String",
      "java.util.Map"
    ],
    "allowedStaticImports": [
      "java.lang.Math",
      "java.util.List",
      "java.lang.String",
      "java.util.Map"
    ],
    "disallowedMethodNames": [
      "execute",
      "invoke"
    ],
    "methodDefinitionAllowed": false
  }
}
```

### POST /cluster/configs/groovy/staticAnalyzerConfig

Update one or more Groovy static analyzer configs. The request body is a map keyed by one or more of the three supported config names listed above.

**Request**

```bash
curl -X POST "http://localhost:9000/cluster/configs/groovy/staticAnalyzerConfig" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "pinot.groovy.ingestion.static.analyzer": {
      "allowedReceivers": [
        "java.lang.String",
        "java.lang.Math",
        "java.util.List",
        "java.lang.Object",
        "java.util.Map"
      ],
      "allowedImports": [
        "java.lang.Math",
        "java.util.List",
        "java.lang.String",
        "java.util.Map"
      ],
      "allowedStaticImports": [
        "java.lang.Math",
        "java.util.List",
        "java.lang.String",
        "java.util.Map"
      ],
      "disallowedMethodNames": [
        "execute",
        "invoke"
      ],
      "methodDefinitionAllowed": false
    }
  }'
```

**Response**

```json
{
  "status": "Updated Groovy Static Analyzer config."
}
```

### GET /cluster/configs/groovy/staticAnalyzerConfig/default

Return Pinot's built-in default Groovy static analyzer config. Use this endpoint to fetch a full sample payload before editing cluster overrides.

**Request**

```bash
curl -X GET "http://localhost:9000/cluster/configs/groovy/staticAnalyzerConfig/default" \
  -H "accept: application/json"
```

**Response**

```json
{
  "pinot.groovy.all.static.analyzer": {
    "allowedReceivers": [
      "java.lang.String",
      "java.lang.Math",
      "java.util.List",
      "java.lang.Object",
      "java.util.Map"
    ],
    "allowedImports": [
      "java.lang.Math",
      "java.util.List",
      "java.lang.String",
      "java.util.Map"
    ],
    "allowedStaticImports": [
      "java.lang.Math",
      "java.util.List",
      "java.lang.String",
      "java.util.Map"
    ],
    "disallowedMethodNames": [
      "execute",
      "invoke"
    ],
    "methodDefinitionAllowed": false
  }
}
```

### GET /cluster/info

Gets cluster related info, such as cluster name

**Request**

```
curl -X GET "http://localhost:9000/cluster/info" -H "accept: application/json"
```

**Response**&#x20;

```
{
  "clusterName": "QuickStartCluster"
}
```

## Health

### GET /health

Check controller health. Status are OK or WebApplicationException with ServiceUnavailable and message

**Request**

```
curl -X GET "http://localhost:9000/health" -H "accept: text/plain"
```

**Response**

```
OK
```

## Leader

### GET /leader/tables&#x20;

Gets the leader resource map, which shows the tables that are mapped to each leader.

**Request**

```
curl -X GET "http://localhost:9000/leader/tables" -H "accept: application/json"
```

**Response**

{% code overflow="wrap" %}
```
{
  "leadControllerEntryMap": {
    "leadControllerResource_0": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_1": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_2": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_3": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_4": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_5": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_6": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_7": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "baseballStats_OFFLINE"
      ]
    },
    "leadControllerResource_8": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "dimBaseballTeams_OFFLINE",
        "starbucksStores_OFFLINE"
      ]
    },
    "leadControllerResource_9": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "billing_OFFLINE"
      ]
    },
    "leadControllerResource_10": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_11": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_12": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_13": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "githubComplexTypeEvents_OFFLINE"
      ]
    },
    "leadControllerResource_14": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_15": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "githubEvents_OFFLINE"
      ]
    },
    "leadControllerResource_16": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_17": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_18": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_19": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "airlineStats_OFFLINE"
      ]
    },
    "leadControllerResource_20": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_21": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_22": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_23": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    }
  },
  "leadControllerResourceEnabled": true
}
```
{% endcode %}

### GET /leader/tables/\<tableName>

Gets the leaders for the specific table

**Request**

```
curl -X GET "http://localhost:9000/leader/tables/baseballStats" -H "accept: application/json"
```

**Response**

```
{
  "leadControllerEntryMap": {
    "leadControllerResource_7": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "baseballStats"
      ]
    }
  },
  "leadControllerResourceEnabled": true
}
```

## Table

### GET /debug/tables/\<tableName>

Debug information for the table, which includes metadata and error status about segments, ingestion, servers and brokers of the table

**Request**

```
curl -X GET "http://localhost:9000/debug/tables/baseballStats?type=OFFLINE&verbosity=0" -H "accept: application/json"
```

**Response**

```
[
  {
    "tableName": "baseballStats_OFFLINE",
    "numSegments": 1,
    "numServers": 1,
    "numBrokers": 1,
    "segmentDebugInfos": [],
    "serverDebugInfos": [],
    "brokerDebugInfos": [],
    "tableSize": {
      "reportedSize": "3 MB",
      "estimatedSize": "3 MB"
    },
    "ingestionStatus": {
      "ingestionState": "HEALTHY",
      "errorMessage": ""
    }
  }
]
```

## Application Quotas

Application-level query quotas allow you to limit the queries per second (QPS) issued by different applications connecting to Pinot, regardless of which tables or databases they query. Applications are identified by the `applicationName` query option. For more details on how application quotas interact with table and database quotas, see [Query Quotas](../../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md).

### GET /applicationQuotas

Get all application QPS quotas. Returns a map of application names to their configured QPS quota values. Returns an empty map if no application quotas have been configured.

**Request**

```
curl -X GET "http://localhost:9000/applicationQuotas" -H "accept: application/json"
```

**Response**

```json
{
  "myApp": 500.0,
  "etlPipeline": 200.0
}
```

### GET /applicationQuotas/\{appName\}

Get the QPS quota for a specific application. If a quota has been explicitly set for the given application, that value is returned. Otherwise, the cluster-level default application quota (`applicationMaxQueriesPerSecond`) is returned. Returns `null` if neither is configured.

**Request**

```
curl -X GET "http://localhost:9000/applicationQuotas/myApp" -H "accept: application/json"
```

**Response**

```json
500.0
```

### POST /applicationQuotas/\{appName\}

Create or update the QPS quota for a specific application. The `maxQueriesPerSecond` query parameter specifies the new quota value. To remove a previously configured quota for an application (falling back to the cluster default), omit the `maxQueriesPerSecond` parameter or leave it empty.

**Request**

```
curl -X POST "http://localhost:9000/applicationQuotas/myApp?maxQueriesPerSecond=500" \
  -H "accept: application/json"
```

**Response**

```json
{
  "status": "Query quota for application myApp successfully updated"
}
```

To remove an application-specific quota:

```
curl -X POST "http://localhost:9000/applicationQuotas/myApp" \
  -H "accept: application/json"
```

## Segments

### GET /segments/\{tableName\}/invalidPartitionMetadata

Return a map of segment name to raw partition metadata JSON for segments whose partition metadata is invalid.

Use this endpoint when you need to find segments whose stored partition metadata cannot be trusted for partition-based routing or validation.

**Request**

```bash
curl -X GET "http://localhost:9000/segments/myTable/invalidPartitionMetadata?type=OFFLINE" \
  -H "accept: application/json"
```

You can optionally scope the validation to a single partition column:

```bash
curl -X GET "http://localhost:9000/segments/myTable/invalidPartitionMetadata?type=OFFLINE&partitionColumn=memberId" \
  -H "accept: application/json"
```

**Behavior**

* Without `partitionColumn`, Pinot treats `null` partition metadata as valid and returns segments whose metadata is malformed or where any column maps to more than one partition.
* With `partitionColumn`, Pinot validates only that column and treats `null` metadata, malformed metadata, missing column metadata, or multiple partitions for the column as invalid.

**Response**

```json
{
  "seg2": "{\"columnPartitionMap\":{\"memberId\":{\"functionName\":\"Modulo\",\"numPartitions\":4,\"partitions\":[0,1]}}}",
  "seg3": "not-valid-json"
}
```

### POST /segments/\{tableName\}/reload

Submit an asynchronous reload job for every segment in a table. The controller accepts either a table name with a type suffix such as `myTable_OFFLINE`, or a raw table name such as `myTable`.

Use the optional query parameters to scope the request:

| Parameter | Type | Description |
| --- | --- | --- |
| `type` | string | Optional table type filter when the path uses a raw table name. Supported values are `OFFLINE` and `REALTIME`. |
| `forceDownload` | boolean | Re-download immutable segments from deep store before reloading. Defaults to `false`. |
| `targetInstance` | string | Send reload messages only to a specific server instance. |
| `instanceToSegmentsMap` | string | JSON map of server instance to segment list. When present, this overrides `targetInstance` and reloads only the listed segments on the listed servers. |

When `forceDownload=true` and the path uses a raw table name without a type, Pinot restricts the reload to the `OFFLINE` table because forced deep-store download is only supported for immutable segments.

**Request**

```bash
curl -X POST "http://localhost:9000/segments/myTable/reload?type=OFFLINE&forceDownload=true" \
  -H "accept: application/json"
```

If you use `instanceToSegmentsMap`, URL-encode the JSON map and send it as a query parameter.

**Response**

```json
{
  "status": "{\"myTable_OFFLINE\":{\"numMessagesSent\":\"24\",\"reloadJobId\":\"6b2f9d35-0d3f-4ef5-91db-f77cb6fdd1c0\",\"reloadJobMetaZKStorageStatus\":\"SUCCESS\"}}"
}
```

The `status` string is itself a JSON object keyed by table name. Each entry includes the submitted `reloadJobId`, the number of server reload messages sent, and whether Pinot persisted job metadata in ZooKeeper for later status checks.

### POST /segments/\{tableName\}/\{segmentName\}/reload

Submit an asynchronous reload job for a single segment. If the table path omits the type suffix, Pinot derives the table type from the segment name.

**Query parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `forceDownload` | boolean | Re-download the segment from deep store before reloading. Defaults to `false`. |
| `targetInstance` | string | Reload the segment only on a specific server instance. |

**Request**

```bash
curl -X POST "http://localhost:9000/segments/myTable_OFFLINE/myTable_0/reload?targetInstance=Server_localhost_8098" \
  -H "accept: application/json"
```

**Response**

```json
{
  "status": "Submitted reload job id: 4f947c6f-8f51-4dbf-b4e7-a8f4f446ce88, sent 1 reload messages. Job meta ZK storage status: SUCCESS"
}
```

### POST /segments/\{tableNameWithType\}/uploadFromServerToDeepstore

Queue one or more realtime segments for upload from an online server replica into deep store. This is useful when a segment is missing from deep store or when you need to force a re-upload. The endpoint only accepts realtime tables with a type suffix such as `myTable_REALTIME`.

| Query parameter | Type | Meaning |
| --- | --- | --- |
| `segmentNames` | string list | Segment names to upload. When omitted or empty, Pinot returns success without queueing any uploads. |
| `forceMode` | boolean | When `false` (default), upload only when Pinot decides the deep-store copy is missing. When `true`, re-upload even if deep store already has a copy. |

**Request**

```bash
curl -X POST "http://localhost:9000/segments/myTable_REALTIME/uploadFromServerToDeepstore?segmentNames=myTable__0__0__20251120T0000Z&segmentNames=myTable__1__0__20251120T0000Z&forceMode=true" \
  -H "accept: application/json"
```

**Response**

```json
{
  "status": "Successfully queued 2 segment(s) for force upload to deep store for table: myTable_REALTIME"
}
```

If the table is not realtime, Pinot returns `400 Bad Request`. If named segments are missing from ZooKeeper metadata, Pinot skips them and only queues the segments it can resolve. When no segments remain after resolution, Pinot returns a success response saying there are no segments to upload.

### POST /segments/reingested

Finalize a reingested realtime segment upload. Pinot uses this endpoint during pauseless disaster recovery after a server has rebuilt a failed LLC segment and uploaded the segment tarball into the segment store.

This endpoint only accepts realtime-table uploads in metadata mode. Operators usually do not call it directly; the server's reingestion flow calls it after `POST /reingestSegment/{segmentName}` finishes rebuilding the segment.

| Query parameter | Type | Meaning |
| --- | --- | --- |
| `tableName` | string | Required raw table name. Pinot resolves the realtime table internally. |

| Required header | Value |
| --- | --- |
| `UPLOAD_TYPE` | `METADATA` |
| `DOWNLOAD_URI` | URI of the reingested segment tarball already copied to the segment store |
| `COPY_SEGMENT_TO_DEEP_STORE` | `true` |

**Request**

```bash
curl -X POST "http://localhost:9000/segments/reingested?tableName=myTable" \
  -H "UPLOAD_TYPE: METADATA" \
  -H "DOWNLOAD_URI: s3://my-bucket/myTable/myTable__0__17__20250320T1530Z.tmp.tar.gz" \
  -H "COPY_SEGMENT_TO_DEEP_STORE: true" \
  -F "file=@myTable__0__17__20250320T1530Z.metadata.tar.gz"
```

The multipart body contains one segment metadata tarball. Pinot reads the segment metadata from that tarball, updates the download URI, and marks the realtime segment as complete.

**Response**

```json
{
  "status": "Successfully uploaded reingested segment: myTable__0__17__20250320T1530Z of table: myTable_REALTIME"
}
```

### DELETE /deleteSegmentsFromSequenceNum/\{tableNameWithType\}

Delete a contiguous tail of LLC segments per partition for a pauseless realtime table. For each input segment, Pinot finds that segment's partition and deletes every segment in the same partition whose sequence number is greater than or equal to the oldest supplied segment for that partition.

Use this endpoint during manual pauseless recovery when a failed segment build or upload left later segments inconsistent and you need Pinot to recreate them from the stream.

| Query parameter | Type | Meaning |
| --- | --- | --- |
| `segments` | string list | Required LLC segment names. Pinot treats the oldest supplied segment in each partition as the deletion starting point. |
| `dryRun` | boolean | When `true`, Pinot returns the per-partition deletion plan without deleting anything. When `false`, Pinot performs the deletion. |
| `force` | boolean | When `false`, Pinot requires the table to be realtime, pauseless-enabled, and currently paused. When `true`, Pinot bypasses the pauseless-enabled and paused-state checks. |

**Request**

Preview the deletion plan first:

```bash
curl -X DELETE "http://localhost:9000/deleteSegmentsFromSequenceNum/myTable_REALTIME?segments=myTable__0__17__20250320T1530Z&dryRun=true" \
  -H "accept: application/json"
```

Apply the deletion after you have paused ingestion and verified the target partitions:

```bash
curl -X DELETE "http://localhost:9000/deleteSegmentsFromSequenceNum/myTable_REALTIME?segments=myTable__0__17__20250320T1530Z&dryRun=false" \
  -H "accept: application/json"
```

**Response**

```json
{
  "tableName": "myTable_REALTIME",
  "dryRun": true,
  "partitions": {
    "0": {
      "segmentsToDelete": [
        "myTable__0__17__20250320T1530Z",
        "myTable__0__18__20250320T1540Z"
      ],
      "oldestSegment": "myTable__0__17__20250320T1530Z",
      "latestSegment": "myTable__0__18__20250320T1540Z",
      "segmentCount": 2
    }
  },
  "message": "Dry run completed. Segments identified for deletion but not actually deleted."
}
```

Pinot skips segment names that are no longer present in the ideal state. For operational safety, run the endpoint once with `dryRun=true` and only rerun with `dryRun=false` after you verify the per-partition segment list.

### GET /segments/segmentReloadStatus/\{jobId\}

Fetch the current status for a previously submitted reload job.

**Request**

```bash
curl -X GET "http://localhost:9000/segments/segmentReloadStatus/6b2f9d35-0d3f-4ef5-91db-f77cb6fdd1c0" \
  -H "accept: application/json"
```

**Response**

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

The typed response tracks overall progress, estimated completion time, job metadata, and any per-segment failures Pinot has collected so far.

### GET /segments/\{tableNameWithType\}/needReload

Ask every server hosting a typed table whether any of its segments need a reload. This endpoint requires a table name with type suffix such as `myTable_OFFLINE` or `myTable_REALTIME`.

**Query parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `verbose` | boolean | Include per-server reload decisions in the response. Defaults to `false`. |

**Request**

```bash
curl -X GET "http://localhost:9000/segments/myTable_OFFLINE/needReload?verbose=true" \
  -H "accept: application/json"
```

**Response**

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

Without `verbose=true`, Pinot still returns the top-level `needReload` flag but leaves `serverToSegmentsCheckReloadList` empty.

### PUT /tables/\<tableName>

Update the config for an existing typed table.

**Query parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `validationTypesToSkip` | string | Comma-separated validation types to skip during table-config validation. |
| `force` | boolean | Defaults to `false`. When `true`, Pinot still applies backward-incompatible upsert or dedup config changes that it would otherwise reject. Use only for controlled migrations. |

By default, Pinot returns `400 Bad Request` for backward-incompatible changes on existing upsert or dedup tables. The protected fields include upsert comparison columns, hash function, mode, out-of-order settings, partial-upsert strategies, dedup hash function, dedup time column, and the table time column when Pinot is using it as the default comparison or dedup time column. The safest path for those changes is still to create a new table and reingest the data.

**Request**

```bash
curl -X PUT "http://localhost:9000/tables/myTable_REALTIME?force=true" \
  -H "Content-Type: application/json" \
  -d @table-config.json
```

**Response**

```json
{
  "status": "Table config updated for myTable_REALTIME"
}
```

### PUT /tableConfigs/\<tableName>

Update a combined `TableConfigs` payload for the raw table name. Pinot uses this endpoint when you want to update schema-linked offline and realtime table configs together.

**Query parameters**

| Parameter | Type | Description |
| --- | --- | --- |
| `validationTypesToSkip` | string | Comma-separated validation types to skip during validation. |
| `reload` | boolean | Defaults to `false`. When `true`, Pinot reloads the table if the schema update is backward compatible. |
| `forceTableSchemaUpdate` | boolean | Defaults to `false`. When `true`, Pinot forces both the schema update and the included table-config updates even when they would normally be rejected as backward incompatible. This is intended for exceptional cases and should be used with caution. |

The same upsert and dedup compatibility checks described above apply to the realtime or offline configs inside the `TableConfigs` payload. Without `forceTableSchemaUpdate=true`, Pinot rejects those backward-incompatible changes with `400 Bad Request`.

**Request**

```bash
curl -X PUT "http://localhost:9000/tableConfigs/myTable?forceTableSchemaUpdate=true" \
  -H "Content-Type: application/json" \
  -d @table-configs.json
```

**Response**

```json
{
  "status": "TableConfigs updated for myTable"
}
```


### DELETE /tables/\<tableName>

Deletes a table from the cluster. By default, deleted segments are moved to a _Deleted Segments_ area and retained for a configurable period (controlled by `controller.deleted.segments.retentionInDays`, default 7 days) before being permanently removed. This allows recovery if the deletion was accidental.

You can override this behavior by passing the `retention` query parameter to specify a custom retention period for the deleted segments. Setting `retention=0d` deletes segments immediately, bypassing the default retention period entirely.

**Query Parameters**

| Parameter  | Type   | Required | Description                                                                                                              |
| ---------- | ------ | -------- | ------------------------------------------------------------------------------------------------------------------------ |
| `type`     | string | No       | Table type (`OFFLINE` or `REALTIME`). If not specified, both types are deleted if they exist.                             |
| `retention`| string | No       | Retention period for deleted segments (e.g., `0d` for immediate deletion, `1d` for one day). Overrides the cluster default. |

**Request (default behavior)**

```
curl -X DELETE "http://localhost:9000/tables/baseballStats" -H "accept: application/json"
```

**Request (immediate deletion)**

```
curl -X DELETE "http://localhost:9000/tables/baseballStats?retention=0d" -H "accept: application/json"
```

**Response**

```
{
  "status": "Tables: [baseballStats_OFFLINE] deleted"
}
```

{% hint style="warning" %}
Setting `retention=0d` permanently deletes all segments immediately with no possibility of recovery. Use this option only when you are certain the data is no longer needed, such as during development, testing, or cleaning up temporary tables.
{% endhint %}

{% hint style="info" %}
For large tables, the default delete operation may time out because it copies segments to the deleted-segments area. Using `retention=0d` bypasses this copy step, which can help avoid timeouts.
{% endhint %}

### DELETE /schemas/\<schemaName>

Deletes a schema from the cluster. A schema can only be deleted if no tables are currently using it. If a table still references the schema, the delete request will fail.

To delete both a table and its schema in a single workflow, first delete the table using `DELETE /tables/<tableName>`, then delete the schema using this endpoint.

**Request**

```
curl -X DELETE "http://localhost:9000/schemas/baseballStats" -H "accept: application/json"
```

**Response**

```
{
  "status": "Schema baseballStats deleted"
}
```

{% hint style="info" %}
In the Pinot Data Explorer UI, you can delete both the table and its schema together by checking the **Delete Schema** option in the delete table dialog. The UI will delete the table first and then automatically delete the associated schema.
{% endhint %}

## Table Config Validation

{% hint style="info" %}
Enhanced in Pinot 1.4.0 with cluster-aware validations (see [PR #16675](https://github.com/apache/pinot/pull/16675))
{% endhint %}

### POST /tableConfigs/validate

Validates a table configuration before you create or update a table. This endpoint now performs cluster-aware validations by default, catching errors like missing tenant tags or unavailable minion instances that previously only surfaced during table creation.

The endpoint checks:
- Schema and table config consistency
- Tenant assignment validity (do instances with the required tags exist?)
- Minion instance availability (if task configs reference minion)
- Active task conflicts

**Request**

```
curl -X POST "http://localhost:9000/tableConfigs/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "tableName": "myTable",
    "tableType": "OFFLINE",
    "segmentsConfig": { ... },
    "tenants": {
      "broker": "DefaultTenant",
      "server": "DefaultTenant"
    },
    "tableIndexConfig": { ... },
    ...
  }'
```

**Parameters**

| Parameter                  | Type  | Description                                                                 |
| -------------------------- | ----- | --------------------------------------------------------------------------- |
| `validationTypesToSkip`    | query | Comma-separated list of validation types to skip (e.g., `TENANT,MINION_INSTANCES`) |

The supported validation types that can be skipped are: `TENANT`, `MINION_INSTANCES`, `ACTIVE_TASKS`.

**Response**

On success, returns the validated config. On failure, returns an error message describing the validation issue.

```
{
  "unrecognizedProperties": {},
  "tableConfig": { ... },
  "schema": { ... }
}
```

## Minion Task APIs

### GET /tasks/\<taskType>/taskcounts

Returns a map from parent task name to aggregated subtask counts for the given minion task type.

**Query Parameters**

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `state` | string | No | Filter by one or more comma-separated Helix task states such as `IN_PROGRESS`, `FAILED`, or `COMPLETED`. The filter applies to the parent task state, not to the per-subtask counters returned in the response. |
| `table` | string | No | Filter to parent tasks that have at least one subtask for the specified table name with type, such as `myTable_OFFLINE`. |

**Request**

```bash
curl -X GET "http://localhost:9000/tasks/SegmentGenerationAndPushTask/taskcounts?state=IN_PROGRESS,FAILED&table=myTable_OFFLINE" \
  -H "accept: application/json"
```

**Response**

```json
{
  "Task_SegmentGenerationAndPushTask_12345": {
    "total": 4,
    "completed": 1,
    "running": 2,
    "waiting": 0,
    "error": 1,
    "unknown": 0,
    "dropped": 0,
    "timedOut": 0,
    "aborted": 0
  }
}
```

Each response value is a subtask-count summary for one parent task. The counters represent the number of subtasks in each result bucket, while `state` only controls which parent tasks are included in the map.

## Logical Table Management

{% hint style="info" %}
Added in Pinot 1.4.0
{% endhint %}

Logical tables provide a unified view over multiple physical tables (REALTIME and OFFLINE). A query against a logical table internally scans all of its underlying physical tables, similar to a SQL VIEW with UNION semantics. This is useful for scaling large tables, performing ALTER TABLE workflows like Kafka topic reconfiguration, and managing time-based data layouts.

### GET /logicalTables

List all logical table names in the cluster.

**Request**

```
curl -X GET "http://localhost:9000/logicalTables" -H "accept: application/json"
```

**Response**

```
["logicalEvents", "logicalOrders"]
```

### GET /logicalTables/\<tableName>

Get the configuration of a specific logical table. The response body is the logical table config JSON.

**Request**

```
curl -X GET "http://localhost:9000/logicalTables/logicalEvents" -H "accept: application/json"
```

**Response**

```
{
  "tableName": "logicalEvents",
  "physicalTableConfigMap": {
    "events_2024_OFFLINE": {},
    "events_2023_OFFLINE": {}
  },
  "brokerTenant": "DefaultTenant",
  "refOfflineTableName": "events_2024_OFFLINE"
}
```

### POST /logicalTables

Create a new logical table. The request body is a logical table config. The physical tables referenced must already exist, and all physical tables must share a compatible schema.

**Request**

```
curl -X POST "http://localhost:9000/logicalTables" \
  -H "Content-Type: application/json" \
  -d '{
    "tableName": "logicalEvents",
    "physicalTableConfigMap": {
      "events_REALTIME": {},
      "events_2024_OFFLINE": {}
    },
    "brokerTenant": "DefaultTenant",
    "refOfflineTableName": "events_2024_OFFLINE",
    "refRealtimeTableName": "events_REALTIME",
    "timeBoundaryConfig": {
      "boundaryStrategy": "min",
      "parameters": {
        "includedTables": ["events_2024_OFFLINE"]
      }
    }
  }'
```

**Response**

```
{
  "status": "Successfully created logical table: logicalEvents"
}
```

### PUT /logicalTables/\<tableName>

Update an existing logical table by sending the full logical table config, for example to add or remove physical tables.

**Request**

```
curl -X PUT "http://localhost:9000/logicalTables/logicalEvents" \
  -H "Content-Type: application/json" \
  -d '{
    "tableName": "logicalEvents",
    "physicalTableConfigMap": {
      "events_REALTIME": {},
      "events_2024_OFFLINE": {},
      "events_2023_OFFLINE": {}
    },
    "brokerTenant": "DefaultTenant",
    "refOfflineTableName": "events_2024_OFFLINE",
    "refRealtimeTableName": "events_REALTIME",
    "timeBoundaryConfig": {
      "boundaryStrategy": "min",
      "parameters": {
        "includedTables": ["events_2024_OFFLINE"]
      }
    }
  }'
```

**Response**

```
{
  "status": "Successfully updated logical table: logicalEvents"
}
```

### DELETE /logicalTables/\<tableName>

Delete a logical table. This does not delete the underlying physical tables.

**Request**

```
curl -X DELETE "http://localhost:9000/logicalTables/logicalEvents" -H "accept: application/json"
```

**Response**

```
{
  "status": "Successfully deleted logical table: logicalEvents"
}
```


## Rebalance

{% hint style="info" %}
Enhanced in Pinot 1.4.0 with dry-run summary mode, pre-checks, and disk utilization info
{% endhint %}

### POST /tables/\<tableName>/rebalance

Trigger a rebalance for a table. In 1.4.0, this API gained several new capabilities:

- **Dry-run summary mode**: Pass `dryRun=true` to get a summary of what the rebalance would do without making any changes.
- **Pre-checks**: Pass `preChecks=true` to run validation checks (replica group info, disk utilization) before executing the rebalance.
- **Disk utilization threshold override**: Use `diskUtilizationThresholdOverride` to customize the threshold for the disk utilization pre-check.
- **Tenant info**: The rebalance response now includes tenant information.
- **minimizeDataMovement**: Pass `minimizeDataMovement=true` to reduce the amount of data moved during the rebalance.

{% hint style="warning" %}
**Nullable Response Fields**: Some fields in the RebalanceResult API response may be `null` depending on the table type (offline vs realtime) and the rebalance configuration options used. When checking rebalance results programmatically, always null-check response fields before using them.
{% endhint %}

**Request**

```
curl -X POST "http://localhost:9000/tables/myTable/rebalance?type=OFFLINE&dryRun=true&preChecks=true" \
  -H "accept: application/json"
```

## Ingestion

### POST /tables/\<tableName>/pauseConsumption

Pause real-time consumption for a table.

| Query parameter | Type | Meaning |
| --- | --- | --- |
| `comment` | string | Optional comment stored with the administrative pause state. |
| `batchSize` | integer | Maximum number of consuming segments Pinot commits at once while pausing. Defaults to queueing all consuming segments in one batch. |
| `batchStatusCheckIntervalSec` | integer | How often, in seconds, the controller checks whether the current pause batch has finished committing. Default: `5`. |
| `batchStatusCheckTimeoutSec` | integer | How long, in seconds, the controller waits for a pause batch to finish before failing the request. Default: `180`. |

For realtime tables with many partitions, use the batch parameters to spread the commit work across smaller pause batches instead of asking every consuming segment to commit at once. Pinot returns `400 Bad Request` if any batch parameter is non-positive.

**Request**

```
curl -X POST "http://localhost:9000/tables/myTable/pauseConsumption" -H "accept: application/json"
```

Example with batching:

```bash
curl -X POST "http://localhost:9000/tables/myTable/pauseConsumption?comment=maintenance&batchSize=50&batchStatusCheckIntervalSec=5&batchStatusCheckTimeoutSec=180" \
  -H "accept: application/json"
```

### POST /tables/\<tableName>/resumeConsumption

Resume real-time consumption for a table.

| Query parameter | Type | Meaning |
| --- | --- | --- |
| `comment` | string | Optional comment stored with the administrative resume state. |
| `consumeFrom` | string | Optional resume offset policy. Use `lastConsumed` to continue from the offsets stored in Pinot metadata, `smallest` to restart from the earliest available offsets, or `largest` to restart from the latest available offsets. Default: `lastConsumed`. |

**Request**

```
curl -X POST "http://localhost:9000/tables/myTable/resumeConsumption" -H "accept: application/json"
```

Example with an administrative comment and an explicit resume policy:

```bash
curl -X POST "http://localhost:9000/tables/myTable/resumeConsumption?comment=maintenance-complete&consumeFrom=smallest" \
  -H "accept: application/json"
```

### GET /tables/\<tableName>/pauseStatus

Return the current pause state for a realtime table together with the currently consuming segments.

**Request**

```bash
curl -X GET "http://localhost:9000/tables/myTable/pauseStatus" -H "accept: application/json"
```

**Response fields**

| Field | Type | Meaning |
| --- | --- | --- |
| `pauseFlag` | boolean | Whether Pinot currently considers the realtime table paused. |
| `consumingSegments` | array of strings | Segment names that are still in the consuming state when the status is fetched. |
| `reasonCode` | string | Pause reason code, such as `ADMINISTRATIVE` for operator-driven pauses or `STORAGE_QUOTA_EXCEEDED` for automatic storage-quota pauses. |
| `comment` | string | Stored administrative or automatic pause comment. If no explicit comment was stored, Pinot returns a default paused or unpaused message. |
| `timestamp` | string | Stored pause-state timestamp from the controller metadata. |

**Example response**

```json
{
  "pauseFlag": true,
  "consumingSegments": [
    "myTable__0__12__20250610T2140Z",
    "myTable__1__12__20250610T2140Z"
  ],
  "reasonCode": "ADMINISTRATIVE",
  "comment": "maintenance",
  "timestamp": "<stored pause-state timestamp>"
}
```

### GET /tables/\<tableName>/badLLCSegmentsPerPartition

Return the bad LLC segments for a realtime table, grouped by partition ID. Pinot sorts the segment names within each partition by increasing sequence number, which makes this endpoint useful before calling repair workflows such as `deleteSegmentsFromSequenceNum`.

**Request**

```bash
curl -X GET "http://localhost:9000/tables/myTable/badLLCSegmentsPerPartition" \
  -H "accept: application/json"
```

**Response**

```json
{
  "0": [
    "myTable__0__12__20250610T2140Z",
    "myTable__0__13__20250610T2200Z"
  ],
  "1": [
    "myTable__1__7__20250610T2145Z"
  ]
}
```

If Pinot finds no bad LLC segments, it returns an empty JSON object.

## Other Notable APIs (1.4.0)

The following APIs were added or enhanced in Pinot 1.4.0. Refer to Swagger for complete request/response details.

| Endpoint                                          | Method | Description                                                             |
| ------------------------------------------------- | ------ | ----------------------------------------------------------------------- |
| `/tables/{tableName}/badLLCSegmentsPerPartition`  | GET    | Returns bad LLC segments grouped by partition ID                        |
| `/tables/{tableName}/removeIngestionMetrics`       | POST   | Removes stale ingestion metrics for a table                             |
| `/debug/serverRoutingStats`                       | GET    | Returns server routing stats as JSON (previously returned a string)     |
| `/tables/{tableName}/idealstate`                  | GET    | Now accepts optional `segmentNames` parameter to filter results         |
| `/tables/{tableName}/externalview`                | GET    | Now accepts optional `segmentNames` parameter to filter results         |
| `/tenants/{tenantName}/tables`                    | GET    | Now supports `withTableProperties` parameter for richer tenant info     |
| `/query_range`                                    | GET/POST | Prometheus-compatible time series query endpoint (Beta)                |

{% hint style="info" %}
For the complete and interactive list of all controller APIs, refer to the Swagger UI at `http://<controller-host>:<port>/help`. For a categorized overview of every endpoint documented on this site, see the main [API Reference](./).
{% endhint %}
