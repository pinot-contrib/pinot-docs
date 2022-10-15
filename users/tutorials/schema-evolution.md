# Schema Evolution

So far, you've seen how to [create a new schema](https://docs.pinot.apache.org/basics/components/schema#creating-a-schema) for a Pinot table. In this tutorial, we'll see how to evolve the schema (e.g. add a new column to the schema). This guide assumes you have a Pinot cluster up and running (eg: as mentioned in [https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally)). We will also assume there's an existing table `baseballStats` created as part of the [batch quick start](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally#batch).

{% hint style="info" %}
Pinot only allows adding new columns to the schema. In order to drop a column, change the column name or data type, a new table has to be created.
{% endhint %}

## **Key takeaways**

1. For a newly added column to become queryable in Pinot, you would need to reload all segments using reload segments API.
2. As far as values for this newly added column are concerned, all existing records in the table will get defaultNullValue configured for this column.
3. If you have a scenario to backfill actual values, re-ingestion would be needed.
4. If newly added column is a derived column, the values will be auto-derived from the dependent columns.

### **A few gotchas around segment reload operation**

1. Reloading of each segment is expected to happen gracefully without impacting in-flight queries; a segment becomes eligible for reload only after reaching the reference count of 0; (i.e: when the segment is not serving any in-flight queries).
2. Assuming that you have segment replicas in place (recommendation is to have at least 3), all new queries entering the system during the segment reload operation are routed to healthy segment replicas. If you don’t have enough replicas in place, it could result in empty results

## &#x20;Add Column Guide

### Get the existing schema

Let's begin by first fetching the existing schema. We can do this using the controller API:

```
$ curl localhost:9000/schemas/baseballStats > baseballStats.schema
```

### Add a new column

Let's add a new column at the end of the schema, something like this (by editing `baseballStats.schema`

```
{
  "schemaName" : "baseballStats",
  "dimensionFieldSpecs" : [ {
  
    ...
    
    }, {
    "name" : "myNewColumn",
    "dataType" : "INT",
    "defaultNullValue": 1
  } ]
}
```

In this example, we're adding a new column called `yearsOfExperience` with a default value of 1.

### Update the schema

You can now update the schema using the following command

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

Please note: this will not be reflected immediately. You can use the following command to reload the table segments for this column to show up. This can be done as follows:

```
$ curl -X POST localhost:9000/segments/baseballStats/reload

{"baseballStats_OFFLINE":{"reloadJobId":"98ad3705-58f3-47d0-a02d-d66dc66a9567","reloadJobMetaZKStorageStatus":"SUCCESS","numMessagesSent":"3"}}
```

This will trigger a reload operation on each of the servers hosting the table's segments. The API response has a reloadJobId which can be used to monitor the status of the reload operation using the segment reload status API

{% hint style="warning" %}
The reloadJobId and the segmentReloadStatus API below is only available starting 0.11.0 or from [this](https://github.com/apache/pinot/commit/3d2b6f3429957e47c3de1764b9f87743a0770ce5) commit.
{% endhint %}

```
$ curl -X GET localhost:9000/segments/segmentReloadStatus/98ad3705-58f3-47d0-a02d-d66dc66a9567

{
  "estimatedTimeRemainingInMinutes": 0,
  "timeElapsedInMinutes": 0.17655,
  "totalServersQueried": 3,
  "successCount": 12,
  "totalSegmentCount": 12,
  "totalServerCallsFailed": 0,
  "metadata": {
    "jobId": "98ad3705-58f3-47d0-a02d-d66dc66a9567",
    "messageCount": "3",
    "submissionTimeMs": "1661753088066",
    "jobType": "RELOAD_ALL_SEGMENTS",
    "tableName": "baseballStats_OFFLINE"
  }
}
```

After the reload, now you can query the new column as shown below:

```
$ bin/pinot-admin.sh PostQuery \
  -queryType sql \
  -brokerPort 8000 \
  -query "select playerID, yearsOfExperience from baseballStats limit 10" 2>/dev/null
Executing command: PostQuery -brokerHost 192.168.86.234 -brokerPort 8000 -queryType sql -query select playerID, yearsOfExperience from baseballStats limit 10
Result: {"resultTable":{"dataSchema":{"columnNames":["playerID","yearsOfExperience"],"columnDataTypes":["STRING","INT"]},"rows":[["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aaronha01",1],["aaronha01",1],["aaronha01",1]]},"exceptions":[],"numServersQueried":1,"numServersResponded":1,"numSegmentsQueried":1,"numSegmentsProcessed":1,"numSegmentsMatched":1,"numConsumingSegmentsQueried":0,"numDocsScanned":10,"numEntriesScannedInFilter":0,"numEntriesScannedPostFilter":20,"numGroupsLimitReached":false,"totalDocs":97889,"timeUsedMs":3,"segmentStatistics":[],"traceInfo":{},"minConsumingFreshnessTimeMs":0}
```

{% hint style="info" %}
**Real-Time Pinot table:** In case of real-time tables, make sure the "_pinot.server.instance.reload.consumingSegment_" config is set to true inside [Server config](https://docs.pinot.apache.org/configuration-reference/server). Without this, the current consuming segment(s) will not reflect the default null value for newly added columns.

Note that the real values for the newly added columns won't be reflected within the current consuming segment(s). The next consuming segment(s) will start consuming the real values.
{% endhint %}

### Derived Column

New columns can be added with [ingestion transforms](../../developers/advanced/ingestion-level-transformations.md). If all the source columns for the new column exist in the schema, the transformed values will be generated for the new column instead of filling default values. Note that derived column as well as corresponding data type needs to be first defined in the schema before making changes in table config for ingestion transform.

### Backfilling the Data

As you can observe, the current query returns the `defaultNullValue` for the newly added column. In order to populate this column with real values, you will need to re-run the batch ingestion job for the past dates.

{% hint style="info" %}
**Real-Time Pinot table:** Backfilling data does not work for real-time tables. If you only have a real-time table, you can convert it to a hybrid table, by adding an offline counterpart that uses the same schema. Then you can backfill the offline table and fill in values for the newly added column. More on [hybrid tables here](https://docs.pinot.apache.org/basics/components/table#hybrid-table).
{% endhint %}
