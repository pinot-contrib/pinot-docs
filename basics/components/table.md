# Table

A **table** is a logical abstraction that represents a collection of related data. It is composed of columns and rows (known as documents in Pinot). The columns, data types and other metadata related to the table is defined using a [schema](../../configuration-reference/schema.md).

Pinot breaks a table into multiple [segments](segment.md) and stores these segments in a deep-store such as HDFS as well as Pinot servers.

In the Pinot cluster, a table is modeled as a [Helix resource](https://helix.apache.org/Concepts.html) and each segment of a table is modeled as a [Helix Partition](https://helix.apache.org/Concepts.html).

The following types of table can be created in pinot -

| Type         | Description                                                                                                                            |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Offline**  | Offline tables ingest pre-built pinot-segments from external data stores. This is generally used for batch ingestion.                  |
| **Realtime** | Realtime tables ingest data from streams (such as Kafka) and build segments from the consumed data.                                    |
| **Hybrid**   | A hybrid Pinot table has both realtime as well as offline tables under the hood. By default, all tables in Pinot are Hybrid in nature. |

{% hint style="info" %}
The user querying the database does not need to know the type of the table. They only need to specify the table name in the query.

e.g. regardless of whether we have an offline table `myTable_OFFLINE`, a real-time table `myTable_REALTIME`, or a hybrid table containing both of these, the query will be:

```sql
select count(*)
from myTable
```
{% endhint %}

[Table Configuration](../../configuration-reference/table.md) is used to define the table properties, such as name, type, indexing, routing, retention etc. It is written in JSON format and is stored in Zookeeper, along with the table schema.

You can use the following properties to make your tables faster or leaner:

* Segment
* Indexing
* Tenants

## Segments

A table in pinot is comprised of small chunks of data. These chunks are known as Segments. To learn more about how Pinot creates and manages segments see [the official documentation](segment.md)

For offline tables, Segments are built outside of pinot and uploaded using a distributed executor such as Spark or Hadoop. For more details, see [Batch Ingestion](../data-import/batch-ingestion/).

For real-time tables, segments are built in a specific interval inside Pinot. You can tune the following for the real-time segments:

### Flush

The Pinot real-time consumer ingests the data, creates the segment, and then flushes the in-memory segment to disk. Pinot allows you to configure when to flush the segment in the following ways:

* **Number of consumed rows** - After consuming X no. of rows from the stream, Pinot will persist the segment to disk
* **Number of desired rows per segment** - Pinot learns and then estimates the number of rows that need to be consumed so that the persisted segment is approximately the size. The learning phase starts by setting the number of rows to 100,000 (this value can be changed) and adjusts it to reach the desired segment size. The segment size may go significantly over the desired size during the learning phase. Pinot corrects the estimation as it goes along, so it is not guaranteed that the resulting completed segments are of the exact size as configured. You should set this value to optimize the performance of queries
* **Max time duration to wait** Pinot consumers wait for the configured time duration after which segments are persisted to the disk.

**Replicas**\
A segment can have multiple replicas to provide higher availability. You can configure the number of replicas for a table segment using

**Completion Mode**\
By default, if the in-memory segment in the [non-winner server](server.md) is equivalent to the committed segment, then the non-winner server builds and replaces the segment. If the available segment is not equivalent to the committed segment, the server simply downloads the committed segment from the controller.

However, in certain scenarios, the segment build can get very memory intensive. It might be desirable to enforce the non-committer servers to just download the segment from the controller, instead of building it again. You can do this by setting `completionMode: "DOWNLOAD"` in the table configuration

For more details on why this is needed, see [Completion Config](../../operators/operating-pinot/tuning/realtime.md#controlling-segment-build-vs-segment-download-on-realtime-servers)

**Download Scheme**

It can happen that a pinot server fails to download segments from the deep store such as HDFS after its completion. However, you can configure servers to download these segments from peer servers instead of the deep store. Currently, only HTTP and HTTPS download schemes are supported. More methods such as gRPC/Thrift can be added in the future.

For more details about peer segment download during real-time ingestion, please refer to this design doc on [bypass deep store for segment completion.](https://cwiki.apache.org/confluence/display/PINOT/By-passing+deep-store+requirement+for+Realtime+segment+completion#BypassingdeepstorerequirementforRealtimesegmentcompletion-Configchange)

## Indexing

You can create multiple indices on a table to increase the performance of the queries. The following types of indices are supported:

* [Forward Index](../indexing/forward-index.md)
  * Dictionary-encoded forward index with bit compression
  * Raw value forward index
  * Sorted forward index with run-length encoding
* [Inverted Index](../indexing/inverted-index.md)
  * Bitmap inverted index
  * Sorted inverted index
* [Star-tree Index](../indexing/star-tree-index.md)
* [Range Index](../indexing/range-index.md)
* [Text Index](../indexing/text-search-support.md)
* [Geospatial](../indexing/geospatial-support.md)

For more details on each indexing mechanism and corresponding configurations, see [Indexing](../indexing/).

You can also set up [Bloomfilters](../../operators/operating-pinot/tuning/routing.md#bloom-filter-for-dictionary) on columns to make queries faster. Further, you can also keep segments in off-heap instead of on-heap memory for faster queries.

### Pre-aggregation

You can aggregate the real-time stream data as it is consumed to reduce segment sizes. We sum the metric column values of all rows that have the same dimensions and create a single row in the segment. This feature is only available on `REALTIME` tables.

The only supported aggregation is `SUM`. The columns on which pre-aggregation is to be done need to satisfy the following requirements:

* All metrics should be listed in `noDictionaryColumns` .
* There should not be any multi-value dimensions.
* All dimension columns are treated to have a dictionary, even if they appear as `noDictionaryColumns` in the config.

The following table config snippet shows an example of enabling pre-aggregation during real-time ingestion.

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

Each table is associated with a tenant. A segment resides on the server, which has the same tenant as itself. For more details on how tenants work, see [Tenant](tenant.md).

You can also override if a table should move to a server with different tenant based on segment status.

A `tagOverrideConfig` can be added under the `tenants` section for realtime tables, to override tags for consuming and completed segments. For example:

```javascript
  "broker": "brokerTenantName",
  "server": "serverTenantName",
  "tagOverrideConfig" : {
    "realtimeConsuming" : "serverTenantName_REALTIME"
    "realtimeCompleted" : "serverTenantName_OFFLINE"
  }
}
```

In the above example, the consuming segments will still be assigned to `serverTenantName_REALTIME` hosts, but once they are completed, the segments will be moved to `serverTeantnName_OFFLINE`. It is possible to specify the full name of _any_ tag in this section (so, for example, you could decide that completed segments for this table should be in pinot servers tagged as `allTables_COMPLETED`). To learn more about this config, see the [Moving Completed Segments](../../operators/operating-pinot/tuning/realtime.md#moving-completed-segments-to-different-hosts) section.

## Hybrid Table

A hybrid table is a table composed of 2 tables, one offline and one real-time that share the same name. In such a table, offline segments may be pushed periodically. The retention on the offline table can be set to a high value since segments are coming in on a periodic basis, whereas the retention on the real-time part can be small.\
Once an offline segment is pushed to cover a recent time period, the brokers automatically switch to using the offline table for segments for that time period and use the real-time table only for data not available in the offline table.

**To understand how time boundary works in the case of a hybrid table see -** [**https://docs.pinot.apache.org/basics/components/broker**](https://docs.pinot.apache.org/basics/components/broker)

A typical scenario is pushing a deduped cleaned up data into an offline table every day while consuming real-time data as and when it arrives. The data can be kept in offline tables for even a few years while the real-time data would be cleaned every few days.

## Examples

Create a table config for your data, or see [`examples`](https://github.com/apache/pinot/tree/master/pinot-tools/src/main/resources/examples) for all possible batch/streaming tables.

**Prerequisites**

1. [Setup the cluster](cluster.md#setup-a-pinot-cluster)
2. [Create broker and server tenants](tenant.md#creating-a-tenant)

## Offline Table Creation

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

**Sample Console Output**

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

## Streaming Table Creation

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

**Create a Kafka Topic**

```
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic flights-realtime
```

**Create a Streaming table**

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

## Hybrid Table creation

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

{% hint style="warning" %}
Note that creating a hybrid table has to be done in 2 separate steps of creating an offline and realtime table individually.
{% endhint %}
