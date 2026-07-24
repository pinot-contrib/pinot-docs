# Schema Evolution

Schema evolution occurs over time. As business requirements evolve, and data formats or structures need to change, use Pinot to keep your schemas up-to-date. If you're just starting out with schemas in Pinot, see how to [create a new schema](../../basics/components/table/schema.md#creating-a-schema) for a Pinot table.&#x20;

In this tutorial, you'll learn how to add a new column to your schema, load data to the updated schema, run a query to test the updated schema, and backfill data.

{% hint style="info" %}
Pinot only supports adding new columns to a schema. To drop a column or change the column name or data type, you must create a new table.
{% endhint %}

## Prerequisites

Before you get started, you must have a Pinot cluster up and running, and a `baseballStats` table (created when you set up a Pinot cluster using the Quickstart option). For more information, see how to [start running Pinot and set up a cluster using the Quickstart](../../basics/getting-started/README.md) option.

## **Add a new column to your schema**

1.  Fetch the existing schema using the controller API:

    ```sh
    $ curl localhost:9000/schemas/baseballStats > baseballStats.schema
    ```
2. Edit the `baseballStats.schema` file to include a new column at the end of the schema. For example, here we're adding a new column called `yearsOfExperience` with a `dataType` of `INT` and `defaultNullValue` of `1`.

{% code title="baseballStats.schema" %}
```markup
{
  "schemaName" : "baseballStats",
  "dimensionFieldSpecs" : [ {
  
    ...
    
    }, {
    "name" : "yearsOfExperience",
    "dataType" : "INT",
    "defaultNullValue": 1
  } ]
}
```
{% endcode %}

3. Update the schema using the following command:

{% tabs %}
{% tab title="pinot-admin.sh" %}
```
bin/pinot-admin.sh AddSchema -schemaFile baseballStats.schema -exec
```
{% endtab %}

{% tab title="curl" %}
```
$ curl -F schemaName=@baseballStats.schema localhost:9000/schemas
```
{% endtab %}
{% endtabs %}

## Reload table segments

After you add the new column to your schema, reload the table segments so completed segments expose the new field and realtime consumers pick up the schema on a fresh consuming segment.

1. (Real-time tables) Keep `pinot.server.instance.reload.consumingSegment` at its default `true` (see [Server config](../../reference/configuration-reference/server.md)) so reload requests a force commit for consuming segments when consistency mode allows it. Servers then seal the current mutable segment asynchronously and start a new consumer with the latest schema/table config. You can also call `POST /tables/{tableName}/forceCommit` explicitly and poll it; see the [force commit API](../../reference/api-reference/controller-api.md#post-tablestablenameforcecommit).
2. To ensure the new `baseballStats` column shows up on completed segments, reload the table — **replace** the sample `reloadJobId` below with yours when polling status:

**Command**&#x20;

```
$ curl -X POST localhost:9000/segments/baseballStats/reload
```

**Response**

```
{"baseballStats_OFFLINE":{"reloadJobId":"c3989a04-9fd1-46af-85e8-00f484759ef2","reloadJobMetaZKStorageStatus":"SUCCESS","numMessagesSent":"3"}}
```

This triggers a reload operation on each of the servers hosting the table's segments. The API response has a `reloadJobId` that you can use to monitor the status of the reload operation using the segment reload status API.&#x20;

{% hint style="info" %}
Reloading a segment shouldn't impact in-flight queries. New segments are reloaded to replace existing segments only after an existing segment isn't serving any in-flight queries.
{% endhint %}

**Command**

```
$ curl -X GET localhost:9000/segments/segmentReloadStatus/c3989a04-9fd1-46af-85e8-00f484759ef2
```

**Response**

```
{
  "estimatedTimeRemainingInMinutes": 0,
  "timeElapsedInMinutes": 0.17655,
  "totalServersQueried": 3,
  "successCount": 12,
  "totalSegmentCount": 12,
  "totalServerCallsFailed": 0,
  "metadata": {
    "jobId": "c3989a04-9fd1-46af-85e8-00f484759ef2",
    "messageCount": "3",
    "submissionTimeMs": "1661753088066",
    "jobType": "RELOAD_ALL_SEGMENTS",
    "tableName": "baseballStats_OFFLINE"
  }
}
```

{% hint style="info" %}
* For real-time **consuming** segments, reload is performed as a **force commit** when `pinot.server.instance.reload.consumingSegment` is true: the current consuming segment is committed as immutable, and a new consuming segment starts with the updated table config and schema.
* Not every column add requires `pauseConsumption`. Plain default-only columns usually need schema update + reload/forceCommit. **Ingestion transform** changes are safer with a pause boundary or an immediate forceCommit so no consumer keeps the old transform plan. See the [schema evolution decision table](../../build-with-pinot/data-modeling/schema-evolution.md#decision-table-add-a-column-on-an-existing-table).
* Upsert and dedup keep table-level (cross-segment) metadata inside the server table data manager. Allowed partial-upsert strategy changes require a controlled server restart and are not retroactive. Core identity and ordering settings are immutable; create a new table and reingest instead of relying on reload or restart. Adding a null-default column on a full-upsert table still follows the reload/forceCommit path above; partial-upsert tables and upsert tables with out-of-order handling configured restrict force commit unless consuming-segment consistency mode allows it.
* In some cases, for example if the transform function evaluation fails or references a column that isn't part of the segment being reloaded, the reload operation may not successfully apply the transform. The reload status API can still report success while querying the new column fails — check server reload logs.
{% endhint %}

## **Query and backfill data**

1. After reloading the segments, run the the following to query the new column:

**Command**

```
$ bin/pinot-admin.sh PostQuery \
  -queryType sql \
  -brokerPort 8000 \
  -query "select playerID, yearsOfExperience from baseballStats limit 10" 2>/dev/null
```

**Response**

```
Executing command: PostQuery -brokerHost 192.168.86.234 -brokerPort 8000 -queryType sql -query select playerID, yearsOfExperience from baseballStats limit 10
Result: {"resultTable":{"dataSchema":{"columnNames":["playerID","yearsOfExperience"],"columnDataTypes":["STRING","INT"]},"rows":[["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aaronha01",1],["aaronha01",1],["aaronha01",1]]},"exceptions":[],"numServersQueried":1,"numServersResponded":1,"numSegmentsQueried":1,"numSegmentsProcessed":1,"numSegmentsMatched":1,"numConsumingSegmentsQueried":0,"numDocsScanned":10,"numEntriesScannedInFilter":0,"numEntriesScannedPostFilter":20,"numGroupsLimitReached":false,"totalDocs":97889,"timeUsedMs":3,"segmentStatistics":[],"traceInfo":{},"minConsumingFreshnessTimeMs":0}
```

2. As you can see, the query returns the `defaultNullValue` for the newly added column. To populate this column with real values, re-run the batch ingestion job for the past datesBackfill data.

{% hint style="warning" %}
Backfilling data does not work for real-time tables. You can convert a real-time table to a hybrid table by adding an offline table that uses the same counterpart, and then backfilling the offline table to fill in values for the newly added column. For more information, see [hybrid tables](../../basics/components/table/README.md#hybrid-table).
{% endhint %}

