---
description: All user APIs available in Pinot
---

# Controller API Reference

The full up-to-date list of APIs can be viewed on Swagger.

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

Application-level query quotas allow you to limit the queries per second (QPS) issued by different applications connecting to Pinot, regardless of which tables or databases they query. Applications are identified by the `applicationName` query option. For more details on how application quotas interact with table and database quotas, see [Query Quotas](../user-guide-query/query-quotas.md).

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

Get the configuration of a specific logical table.

**Request**

```
curl -X GET "http://localhost:9000/logicalTables/logicalEvents" -H "accept: application/json"
```

**Response**

```
{
  "tableName": "logicalEvents",
  "physicalTableNames": [
    "events_REALTIME",
    "events_2024_OFFLINE",
    "events_2023_OFFLINE"
  ],
  "brokerTenant": "DefaultTenant",
  "logicalTableConfig": { ... }
}
```

### POST /logicalTables

Create a new logical table. The physical tables referenced must already exist. All physical tables must share a compatible schema.

**Request**

```
curl -X POST "http://localhost:9000/logicalTables" \
  -H "Content-Type: application/json" \
  -d '{
    "tableName": "logicalEvents",
    "physicalTableNames": [
      "events_REALTIME",
      "events_2024_OFFLINE"
    ],
    "brokerTenant": "DefaultTenant"
  }'
```

**Response**

```
{
  "status": "Successfully created logical table: logicalEvents"
}
```

### PUT /logicalTables/\<tableName>

Update an existing logical table, for example to add or remove physical tables.

**Request**

```
curl -X PUT "http://localhost:9000/logicalTables/logicalEvents" \
  -H "Content-Type: application/json" \
  -d '{
    "tableName": "logicalEvents",
    "physicalTableNames": [
      "events_REALTIME",
      "events_2024_OFFLINE",
      "events_2023_OFFLINE"
    ],
    "brokerTenant": "DefaultTenant"
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
For the complete and most current list of all controller APIs, always refer to the Swagger UI at `http://<controller-host>:<port>/help`.
{% endhint %}
