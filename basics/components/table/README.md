---
description: >-
  Explore the table component in Apache Pinot, a fundamental building block for
  organizing and managing data in Pinot clusters, enabling effective data
  processing and analysis.
---

# Table

A **table** is a logical abstraction that represents a collection of related data. It is composed of columns and rows (known as documents in Pinot). The columns, data types, and other metadata related to the table are defined using a [schema](../../../configuration-reference/schema.md).

Pinot breaks a table into multiple [segments](segment/) and stores these segments in a deep-store such as Hadoop Distributed File System (HDFS) as well as Pinot servers.

In the Pinot cluster, a table is modeled as a [Helix resource](https://helix.apache.org/Concepts.html) and each segment of a table is modeled as a [Helix Partition](https://helix.apache.org/Concepts.html).

{% hint style="info" %}
Table naming in Pinot follows typical naming conventions, such as starting names with a letter, not ending with an underscore, and using only alphanumeric characters.
{% endhint %}

Pinot supports the following types of tables:

| Type          | Description                                                                                                                   |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **Offline**   | Offline tables ingest pre-built Pinot segments from external data stores and are generally used for batch ingestion.          |
| **Real-time** | Real-time tables ingest data from streams (such as Kafka) and build segments from the consumed data.                          |
| **Hybrid**    | Hybrid Pinot tables have both real-time as well as offline tables under the hood. By default, all tables in Pinot are hybrid. |

{% hint style="info" %}
The user querying the database does not need to know the type of the table. They only need to specify the table name in the query.

e.g. regardless of whether we have an offline table `myTable_OFFLINE`, a real-time table `myTable_REALTIME`, or a hybrid table containing both of these, the query will be:

```sql
select count(*)
from myTable
```
{% endhint %}

[Table configuration](../../../configuration-reference/table.md) is used to define the table properties, such as name, type, indexing, routing, and retention. It is written in JSON format and is stored in Zookeeper, along with the table schema.

Use the following properties to make your tables faster or leaner:

* Segment
* Indexing
* Tenants

## Segments

A table is comprised of small chunks of data known as segments. Learn more about how Pinot creates and manages segments [here](https://docs.pinot.apache.org/basics/components/segment).

For offline tables, segments are built outside of Pinot and uploaded using a distributed executor such as Spark or Hadoop. For details, see [Batch Ingestion](../../data-import/batch-ingestion/).

For real-time tables, segments are built in a specific interval inside Pinot. You can tune the following for the real-time segments.

### Flush

The Pinot real-time consumer ingests the data, creates the segment, and then flushes the in-memory segment to disk. Pinot allows you to configure when to flush the segment in the following ways:

* **Number of consumed rows**: After consuming the specified number of rows from the stream, Pinot will persist the segment to disk.
* **Number of desired rows per segment**[:](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/\~/diff/\~/changes/1650/basics/concepts) Pinot learns and then estimates the number of rows that need to be consumed. The learning phase starts by setting the number of rows to 100,000 (this value can be changed) and adjusts it to reach the appropriate segment size. Because Pinot corrects the estimate as it goes along, the segment size might go significantly over the correct size during the learning phase. You should set this value to optimize the performance of queries.
* **Max time duration to wait**: Pinot consumers wait for the configured time duration after which segments are persisted to the disk.

**Replicas**\
A segment can have multiple replicas to provide higher availability. You can configure the number of replicas for a table segment [using the CLI](https://docs.pinot.apache.org/operators/cli#change-num-replicas).

**Completion Mode**\
By default, if the in-memory segment in the [non-winner server](../cluster/server.md) is equivalent to the committed segment, then the non-winner server builds and replaces the segment. If the available segment is not equivalent to the committed segment, the server just downloads the committed segment from the controller.

However, in certain scenarios, the segment build can get very memory-intensive. In these cases, you might want to enforce the non-committer servers to just download the segment from the controller instead of building it again. You can do this by setting `completionMode: "DOWNLOAD"` in the table configuration.

For details, see [Completion Config](../../../operators/operating-pinot/tuning/realtime.md#controlling-segment-build-vs-segment-download-on-realtime-servers).

**Download Scheme**

A Pinot server might fail to download segments from the deep store, such as HDFS, after its completion. However, you can configure servers to download these segments from peer servers instead of the deep store. Currently, only HTTP and HTTPS download schemes are supported. More methods, such as gRPC/Thrift, are planned be added in the future.

For more details about peer segment download during real-time ingestion, refer to this design doc on [bypass deep store for segment completion.](https://cwiki.apache.org/confluence/display/PINOT/By-passing+deep-store+requirement+for+Realtime+segment+completion#BypassingdeepstorerequirementforRealtimesegmentcompletion-Configchange)

## Indexing

You can create multiple indices on a table to increase the performance of the queries. The following types of indices are supported:

* [Forward Index](../../indexing/forward-index.md)
  * Dictionary-encoded forward index with bit compression
  * Raw value forward index
  * Sorted forward index with run-length encoding
* [Inverted Index](../../indexing/inverted-index.md)
  * Bitmap inverted index
  * Sorted inverted index
* [Star-tree Index](../../indexing/star-tree-index.md)
* [Range Index](../../indexing/range-index.md)
* [Text Index](../../indexing/text-search-support.md)
* [Geospatial](../../indexing/geospatial-support.md)

For more details on each indexing mechanism and corresponding configurations, see [Indexing](../../indexing/).

Set up [Bloomfilters](../indexing/bloom-filter.md) on columns to make queries faster. You can also keep segments in off-heap instead of on-heap memory for faster queries.

### Pre-aggregation

Aggregate the real-time stream data as it is consumed to reduce segment sizes. We add the metric column values of all rows that have the same values for all dimension and time columns and create a single row in the segment. This feature is only available on `REALTIME` tables.

The only supported aggregation is `SUM`. The columns to pre-aggregate need to satisfy the following requirements:

* All metrics should be listed in `noDictionaryColumns`.
* No multi-value dimensions
* All dimension columns are treated to have a dictionary, even if they appear as `noDictionaryColumns` in the config.

The following table config snippet shows an example of enabling pre-aggregation during real-time ingestion:

{% code title="pinot-table-realtime.json" %}
```javascript
    "tableIndexConfig": { 
      "noDictionaryColumns": ["metric1", "metric2"],
      "aggregateMetrics": true,
      ...
    }
```
{% endcode %}

## Tenants

Each table is associated with a tenant. A segment resides on the server, which has the same tenant as itself. For details, see [Tenant](../cluster/tenant.md).

Optionally, override if a table should move to a server with different tenant based on segment status. The example below adds a `tagOverrideConfig` under the `tenants` section for real-time tables to override tags for consuming and completed segments.&#x20;

```javascript
  "broker": "brokerTenantName",
  "server": "serverTenantName",
  "tagOverrideConfig" : {
    "realtimeConsuming" : "serverTenantName_REALTIME"
    "realtimeCompleted" : "serverTenantName_OFFLINE"
  }
}
```

In the above example, the consuming segments will still be assigned to `serverTenantName_REALTIME` hosts, but once they are completed, the segments will be moved to `serverTeantnName_OFFLINE`.&#x20;

You can specify the full name of _any_ tag in this section. For example, you could decide that completed segments for this table should be in Pinot servers tagged as `allTables_COMPLETED`). To learn more about, see the [Moving Completed Segments](../../../operators/operating-pinot/tuning/realtime.md#moving-completed-segments-to-different-hosts) section.

## Hybrid table

A hybrid table is a table composed of two tables, one offline and one real-time, that share the same name. In a hybrid table, offline segments can be pushed periodically. The retention on the offline table can be set to a high value because segments are coming in on a periodic basis, whereas the retention on the real-time part can be small.

Once an offline segment is pushed to cover a recent time period, the brokers automatically switch to using the offline table for segments for that time period and use the real-time table only for data not available in the offline table.

To learn how time boundaries work for hybrid tables, see [Broker](https://docs.pinot.apache.org/basics/components/broker).

A typical use case for hybrid tables is pushing deduplicated, cleaned-up data into an offline table every day while consuming real-time data as it arrives. Data can remain in offline tables for as long as a few years, while the real-time data would be cleaned every few days.

## Examples

Create a table config for your data, or see [`examples`](https://github.com/apache/pinot/tree/master/pinot-tools/src/main/resources/examples) for all possible batch/streaming tables.

**Prerequisites**

* [Set up the cluster](../cluster/#setup-a-pinot-cluster)
* [Create broker and server tenants](../cluster/tenant.md#creating-a-tenant)

## Offline table creation

{% tabs %}
{% tab title="Docker" %}
```bash
docker run \
    --network=pinot-demo \
    --name pinot-batch-table-creation \
    ${PINOT_IMAGE} AddTable \
    -schemaFile examples/batch/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
```

**Sample console output**

```bash
Executing command: AddTable -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -schemaFile examples/batch/airlineStats/airlineStats_schema.json -controllerHost pinot-controller -controllerPort 9000 -exec
Sending request: http://pinot-controller:9000/schemas to controller: a413b0013806, version: Unknown
{"status":"Table airlineStats_OFFLINE succesfully added"}
```
{% endtab %}

{% tab title="Using launcher scripts" %}
```bash
bin/pinot-admin.sh AddTable \
    -schemaFile examples/batch/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json \
    -exec
```
{% endtab %}

{% tab title="curl" %}
```bash
# add schema
curl -F schemaName=@airlineStats_schema.json  localhost:9000/schemas

# add table
curl -i -X POST -H 'Content-Type: application/json' \
    -d @airlineStats_offline_table_config.json localhost:9000/tables
```
{% endtab %}
{% endtabs %}

Check out the table config in the [Rest API](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig) to make sure it was successfully uploaded.

## Streaming table creation

{% tabs %}
{% tab title="Docker" %}
**Start Kafka**

```
docker run \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -d wurstmeister/kafka:latest
```

**Create a Kafka topic**

```
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic flights-realtime
```

**Create a streaming table**

```
docker run \
    --network=pinot-demo \
    --name pinot-streaming-table-creation \
    ${PINOT_IMAGE} AddTable \
    -schemaFile examples/stream/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/docker/table-configs/airlineStats_realtime_table_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
```

**Sample output**

```
Executing command: AddTable -tableConfigFile examples/docker/table-configs/airlineStats_realtime_table_config.json -schemaFile examples/stream/airlineStats/airlineStats_schema.json -controllerHost pinot-controller -controllerPort 9000 -exec
Sending request: http://pinot-controller:9000/schemas to controller: 8fbe601012f3, version: Unknown
{"status":"Table airlineStats_REALTIME succesfully added"}
```
{% endtab %}

{% tab title="Using launcher scripts" %}
**Start Kafka-Zookeeper**

```
bin/pinot-admin.sh StartZookeeper -zkPort 2191
```

**Start Kafka**

```
bin/pinot-admin.sh  StartKafka -zkAddress=localhost:2191/kafka -port 19092
```

**Create stream table**

```
bin/pinot-admin.sh AddTable \
    -schemaFile examples/stream/airlineStats/airlineStats_schema.json \
    -tableConfigFile examples/stream/airlineStats/airlineStats_realtime_table_config.json \
    -exec
```
{% endtab %}
{% endtabs %}

Check out the table config in the [Rest API](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig) to make sure it was successfully uploaded.

## Hybrid table creation

To create a hybrid table, you have to create the offline and real-time tables individually. You don't need to create a separate hybrid table.

```javascript
"OFFLINE": {
    "tableName": "pinotTable", 
    "tableType": "OFFLINE", 
    "segmentsConfig": {
      ... 
    }, 
    "tableIndexConfig": { 
      ... 
    },  
    "tenants": {
      "broker": "myBrokerTenant", 
      "server": "myServerTenant"
    },
    "metadata": {
      ...
    }
  },
  "REALTIME": { 
    "tableName": "pinotTable", 
    "tableType": "REALTIME", 
    "segmentsConfig": {
      ...
    }, 
    "tableIndexConfig": { 
      ... 
      "streamConfigs": {
        ...
      },  
    },  
    "tenants": {
      "broker": "myBrokerTenant", 
      "server": "myServerTenant"
    },
    "metadata": {
    ...
    }
  }
}
```
