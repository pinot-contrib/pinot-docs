# Schema Evolution

So far, you've seen how to [create a new schema](https://docs.pinot.apache.org/basics/components/schema#creating-a-schema) for a Pinot table. In this tutorial, we'll see how to evolve the schema \(e.g. add a new column to the schema\). This guide assumes you have a Pinot cluster up and running \(eg: as mentioned in [https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally)\). We will also assume there's an existing table `baseballStats` created as part of the [batch quick start](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally#batch).

{% hint style="info" %}
Pinot only allows adding new columns to the schema. In order to drop a column, change the column name or data type, a new table has to be created.
{% endhint %}

### Get the existing schema

Let's begin by first fetching the existing schema. We can do this using the controller API:

```
$ curl localhost:9000/schemas/baseballStats > baseballStats.schema
```

### Add a new column

Let's add a new column at the end of the schema, something like this \(by editing `baseballStats.schema`

```text
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
```text
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

```text
$ curl -X POST localhost:9000/segments/baseballStats/reload
```

After the reload, now you can query the new column as shown below:

```text
$ bin/pinot-admin.sh PostQuery \
  -queryType sql \
  -brokerPort 8000 \
  -query "select playerID, yearsOfExperience from baseballStats limit 10" 2>/dev/null
Executing command: PostQuery -brokerHost 192.168.86.234 -brokerPort 8000 -queryType sql -query select playerID, yearsOfExperience from baseballStats limit 10
Result: {"resultTable":{"dataSchema":{"columnNames":["playerID","yearsOfExperience"],"columnDataTypes":["STRING","INT"]},"rows":[["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aardsda01",1],["aaronha01",1],["aaronha01",1],["aaronha01",1]]},"exceptions":[],"numServersQueried":1,"numServersResponded":1,"numSegmentsQueried":1,"numSegmentsProcessed":1,"numSegmentsMatched":1,"numConsumingSegmentsQueried":0,"numDocsScanned":10,"numEntriesScannedInFilter":0,"numEntriesScannedPostFilter":20,"numGroupsLimitReached":false,"totalDocs":97889,"timeUsedMs":3,"segmentStatistics":[],"traceInfo":{},"minConsumingFreshnessTimeMs":0}
```

{% hint style="info" %}
**Real-Time Pinot table:** In case of real-time tables, make sure the "_pinot.server.instance.reload.consumingSegment_" config is set to true inside [Server config](https://docs.pinot.apache.org/configuration-reference/server). Without this, the current consuming segment\(s\) will not reflect the default null value for newly added columns.
{% endhint %}

### Backfilling the Data

As you can observe, the current query returns the `defaultNullValue` for the newly added column. In order to populate this column with real values, you will need to re-run the batch ingestion job for the past dates.

{% hint style="info" %}
**Real-Time Pinot table:** Backfilling data does not work for real-time tables. If you only have a real-time table, you can convert it to a hybrid table, by adding an offline counterpart that uses the same schema. Then you can backfill the offline table and fill in values for the newly added column. More on [hybrid tables here](https://docs.pinot.apache.org/basics/components/table#hybrid-table).
{% endhint %}

