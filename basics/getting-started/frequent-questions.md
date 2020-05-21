---
description: >-
  This page has a collection of frequently asked questions with answers from the
  community.
---

# Frequent questions

{% hint style="info" %}
This is a list of frequent questions most often asked in our troubleshooting channel on Slack. Please feel free to contribute your questions and answers here and make a pull request.
{% endhint %}

### Do replica groups work for real-time? <a id="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3"></a>

Yes, replica groups work for realtime. There's 2 parts to enabling replica groups:

1. Replica groups segment assignment
2. Replica group query routing

**Replica group segment assignment**

Replica group segment assignment is achieved in realtime, if number of servers is a multiple of number of replicas. The partitions get uniformly sprayed across the servers, creating replica groups.  
  
For example, consider we have 6 partitions, 2 replicas, and 4 servers.

|  | r1 | r2 |
| :--- | :--- | :--- |
| p1 | S0 | S1 |
| p2 | S2 | S3 |
| p3 | S0 | S1 |
| p4 | S2 | S3 |
| p5 | S0 | S1 |
| p6 | S2 | S3 |

As you can see, the set \(S0, S2\) contains r1 of every partition, and \(s1, S3\) contains r2 of every partition. The query will only be routed to one of the sets, and not span every server.  
If you are are adding/removing servers from an existing table setup, you have to run [rebalance](frequent-questions.md#how-to-run-a-rebalance-on-a-table) for segment assignment changes to take effect.

**Replica group query routing**

Once replica group segment assignment is in effect, the query routing can take advantage of it. For replica group based query routing, set the following in the table config's [routing](https://docs.pinot.apache.org/basics/components/table#routing) section, and then restart brokers

```text
{
    "tableName": "pinotTable", 
    "tableType": "REALTIME",
    "routing": {
        "instanceSelectorType": "replicaGroup"
    }
    ..
}
```

### How to set inverted indexes?

Inverted indexes are set in the tableConfig's tableIndexConfig -&gt; invertedIndexColumns list. Here's the documentation for tableIndexConfig: [https://docs.pinot.apache.org/basics/components/table\#tableindexconfig-1](https://docs.pinot.apache.org/basics/components/table#tableindexconfig-1) along with a sample table that has set inverted indexes on some columns.

Applying inverted indexes to a table config will generate inverted index to all new segments. In order to apply the inverted indexes to all existing segments, follow steps in [How to apply inverted index to existing setup?](frequent-questions.md#how-to-apply-inverted-index-to-existing-setup)

### How to apply inverted index to existing setup?

1. Add the columns you wish to index to the tableIndexConfig-&gt; invertedIndexColumns list. This sample table config show inverted indexes set: [https://docs.pinot.apache.org/basics/components/table\#offline-table-config ](https://docs.pinot.apache.org/basics/components/table#offline-table-config)To update the table config use the Pinot Swagger API: [http://localhost:9000/help\#!/Table/updateTableConfig](http://localhost:9000/help#!/Table/updateTableConfig)
2. Invoke the reload API: [http://localhost:9000/help\#!/Segment/reloadAllSegments](http://localhost:9000/help#!/Segment/reloadAllSegments)

Right now, there’s no easy way to confirm that reload succeeded. One way it to check out the index\_map file inside the segment metadata, you should see inverted index entries for the new columns. An API for this is coming soon: [https://github.com/apache/incubator-pinot/issues/5390](https://github.com/apache/incubator-pinot/issues/5390)

### How to apply star tree index?

### How do I flatten my JSON Kafka stream?

We have `toJsonStr(key)` function which can store a top level json field as a STRING in Pinot.

Then you can use `jsonExtractScalar(JSON_STRING_FIELD, JSON_PATH, OUTPUT_FORMAT)` function during query time to fetch the desired field from the json string. For example

```text
Select jsonExtractScalar(myJsonMapStr,'$.k1','STRING') 
    from myTable  
    where jsonExtractScalar(myJsonMapStr,'$.k1','STRING') = 'value-k1-0'"
```

```text
Select sum(jsonExtractScalar(complexMapStr,'$.k4.met','INT')) 
    from myTable 
    group by jsonExtractScalar(complexMapStr,'$.k1','STRING')
```

{% hint style="warning" %}
**NOTE**  
This works well if some of your fields are nested json, but most of your fields are top level json keys. If all of your fields are within a nested JSON key, you will have to store the entire payload as 1 column, which is not ideal.  
  
Support for flattening during ingestion is on the roadmap: [https://github.com/apache/incubator-pinot/issues/5264](https://github.com/apache/incubator-pinot/issues/5264)
{% endhint %}

### Can I change a column name in my table, without losing data?

### How to change number of replicas of a table?

You can change the number of replicas by updating the table config's [segmentsConfig](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1) section. Make sure you have at least as many servers as the replication.

For OFFLINE table, update [replication](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1)

```text
{ 
    "tableName": "pinotTable", 
    "tableType": "OFFLINE", 
    "segmentsConfig": {
      "replication": "3", 
      ... 
    }
    ..
```

For REALTIME table update [replicasPerPartition](https://docs.pinot.apache.org/basics/components/table#segmentsconfig)

```text
{ 
    "tableName": "pinotTable", 
    "tableType": "REALTIME", 
    "segmentsConfig": {
      "replicasPerPartition": "3", 
      ... 
    }
    ..
```

After changing the replication, run a [table rebalance](frequent-questions.md#how-to-run-a-rebalance-on-a-table). 

### How to run a rebalance on a table?

A rebalance is run to reassign all the segments of a table to the available servers. This is typically done when capacity changes are done i.e. adding more servers or removing servers from a table.

**Offline**

Use the rebalance API from the Swagger APIs on the controller [http://localhost:9000/help\#!/Table/rebalance](%20http://localhost:9000/help#!/Table/rebalance), with tableType OFFLINE

**Realtime**

Use the rebalance API from the Swagger APIs on the controller [http://localhost:9000/help\#!/Table/rebalance](%20http://localhost:9000/help#!/Table/rebalance), with tableType REALTIME**.**   
A realtime table has 2 components, the consuming segments and the completed segments. By default, only the completed segments will get rebalanced. The consuming segments will pick the right assignment once they complete. But you can enforce the consuming segments to also be included in the rebalance, by setting the param `includeConsuming` to true. Note that rebalancing the consuming segments would mean the consuming segment will drop the consumed data so far, and restart consumption from the last offset, which may lead to a short duration of data staleness.

You can check the status of the rebalance by

1. Checking the controller logs
2. Running rebalance again after a while, you should receive status `"status": "NO_OP"`
3. Checking the External View of the table, to see the changes in capacity/replicas have taken effect.

## Querying

### What are all the fields in the Pinot query's JSON response?

Here's the page explaining the Pinot response format: [https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format](https://docs.pinot.apache.org/users/api/querying-pinot-using-standard-sql/response-format)

### SQL Query fails with "Encountered 'timestamp' was expecting one of..."

"timestamp" is a reserved keyword in SQL. Escape timestamp with double quotes. 

```text
select "timestamp" from myTable
```

Other commonly encountered reserved keywords are date, time, table.

### Filtering on STRING column WHERE column = "foo" does not work?

For filtering on STRING columns, use single quotes

```text
SELECT COUNT(*) from myTable WHERE column = 'foo'
```

### ORDER BY using an alias doesn't work?

The fields in the `ORDER BY` clause must be one of the group by clauses or aggregations, _**BEFORE**_ applying the alias. Therefore, this will not work

```text
SELECT count(colA) as aliasA, colA from tableA GROUP BY colA ORDER BY aliasA
```

Instead, this will work

```text
SELECT count(colA) as sumA, colA from tableA GROUP BY colA ORDER BY count(colA)
```

