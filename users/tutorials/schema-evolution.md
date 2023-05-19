# Schema Evolution

Schema evolution occurs over time. As business requirements evolve, and data formats or structures need to change, use Pinot to keep your schemas up-to-date. If you're just starting out with schemas in Pinot, see how to [create a new schema](https://docs.pinot.apache.org/basics/components/schema#creating-a-schema) for a Pinot table.&#x20;

In this tutorial, you'll learn how to add a new column to your schema, load data to the updated schema, run a query to test the updated schema, and backfill data.

{% hint style="info" %}
Pinot only supports adding new columns to a schema. To drop a column or change the column name or data type, you must create a new table.
{% endhint %}

## Prerequisites

Before you get started, you must have a Pinot cluster up and running, and a `baseballStats` table (created when you set up a Pinot cluster using the Quickstart option). For more information, see how to [start running Pinot and set up a cluster using the Quickstart](https://docs.pinot.apache.org/basics/getting-started#running-pinot) option.

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

After you add the new column to your schema, reload the consuming segments.

1. (Real-time tables only): Open [Server config](https://docs.pinot.apache.org/configuration-reference/server), and set `pinot.server.instance.reload.consumingSegment` to `true`.
2. To ensure the `baseballStats` column shows up, run the following command to reload the table segments--**be sure to replace** **the accurate** `reloadJobId` **for your schema:**

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
* For real-time consuming segments, the reload is performed as force commit, which commits the current consuming segment and loads it as an immutable segment. A new consuming segment is created after the current one is committed, and picks up the changes in the table config and schema.
* Upsert and dedup config change cannot be applied via reload because they will change the table level (cross segments) metadata management. To apply these changes, server needs to be restarted.
* In some cases, for example, if the transform function evaluation fails or references a column that isn't part of the segment being reloaded, the reload operation may not succesfully apply the transform. In these cases, the reload status API will still report sucess, but querying the new columns may not work. Review server reload logs to identify these cases.
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
Backfilling data does not work for real-time tables. You can convert a real-time table to a hybrid table by adding an offline table that uses the same counterpart, and then backfilling the offline table to fill in values for the newly added column. For more information, see [hybrid tables](https://docs.pinot.apache.org/basics/components/table#hybrid-table).
{% endhint %}



