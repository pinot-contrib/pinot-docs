---
description: Pinot controller API reference.
---

# Controller API Examples

The controller exposes the administrative API surface for cluster, schema, table, segment, tenant, and database operations. The detailed request and response examples live here instead of in the user guide so the reference tree can act as the canonical endpoint index.

## Endpoint Families

| Family | Representative endpoints |
| --- | --- |
| Cluster | `GET /cluster/configs`, `POST /cluster/configs`, `DELETE /cluster/configs/{configName}`, `GET /cluster/info` |
| Health and leadership | `GET /health`, `GET /leader/tables` |
| Query validation | `POST /validateMultiStageQuery`, `POST /query/tableNames` |
| Schema | `GET /schemas`, `GET /schemas/{schemaName}`, `POST /schemas`, `PUT /schemas/{schemaName}`, `DELETE /schemas/{schemaName}` |
| Table | `GET /tables`, `POST /tables`, `PUT /tables/{tableName}`, `DELETE /tables/{tableName}`, `POST /tableConfigs/validate` |
| Logical tables | `GET /logicalTables`, `POST /logicalTables`, `PUT /logicalTables/{tableName}`, `DELETE /logicalTables/{tableName}` |
| Segments | `GET /segments/{tableName}/invalidPartitionMetadata`, `POST /segments/{tableName}/reload`, `GET /segments/segmentReloadStatus/{jobId}`, `GET /segments/{tableNameWithType}/needReload` |
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

**Request**

```
curl -X POST "http://localhost:9000/tables/myTable/rebalance?type=OFFLINE&dryRun=true&preChecks=true" \
  -H "accept: application/json"
```

## Ingestion

### POST /tables/\<tableName>/pauseConsumption

Pause real-time consumption for a table.

**Request**

```
curl -X POST "http://localhost:9000/tables/myTable/pauseConsumption" -H "accept: application/json"
```

### POST /tables/\<tableName>/resumeConsumption

Resume real-time consumption for a table.

**Request**

```
curl -X POST "http://localhost:9000/tables/myTable/resumeConsumption" -H "accept: application/json"
```

## Other Notable APIs (1.4.0)

The following APIs were added or enhanced in Pinot 1.4.0. Refer to Swagger for complete request/response details.

| Endpoint                                          | Method | Description                                                             |
| ------------------------------------------------- | ------ | ----------------------------------------------------------------------- |
| `/tables/{tableName}/badSegments`                 | GET    | Returns bad segments grouped by partition ID                            |
| `/tables/{tableName}/removeIngestionMetrics`       | POST   | Removes stale ingestion metrics for a table                             |
| `/debug/serverRoutingStats`                       | GET    | Returns server routing stats as JSON (previously returned a string)     |
| `/tables/{tableName}/idealstate`                  | GET    | Now accepts optional `segmentNames` parameter to filter results         |
| `/tables/{tableName}/externalview`                | GET    | Now accepts optional `segmentNames` parameter to filter results         |
| `/tenants/{tenantName}/tables`                    | GET    | Now supports `withTableProperties` parameter for richer tenant info     |
| `/query_range`                                    | GET/POST | Prometheus-compatible time series query endpoint (Beta)                |

{% hint style="info" %}
For the complete and interactive list of all controller APIs, refer to the Swagger UI at `http://<controller-host>:<port>/help`. For a categorized overview of every endpoint documented on this site, see the main [API Reference](./).
{% endhint %}
