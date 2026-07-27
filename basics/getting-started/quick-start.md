---
description: >-
  This section describes quick start commands that launch all Pinot components
  in a single process.
---

# Quick Start Examples

Pinot ships with `QuickStart` commands that launch Pinot components in a single process and import pre-built datasets. These quick start examples are a good place if you're just getting started with Pinot. The examples begin with the [Batch Processing](quick-start.md#batch-processing) example, after the following notes:

*   **Prerequisites**

    You must have either [installed Pinot locally](install/local.md) or [have Docker installed if you want to use the Pinot Docker image](install/docker.md). The examples are available in each option and work the same. The decision of which to choose depends on your installation preference and how you generally like to work. If you don't know which to choose, using Docker will make your cleanup easier after you are done with the examples.
*   **Pinot versions in examples**

    The Docker-based examples on this page use `pinot:latest`, which instructs Docker to pull and use the most recent release of Apache Pinot. If you prefer to use a specific release instead, you can designate it by replacing `latest` with the release number, like this: `pinot:0.12.1`.

    The local install-based examples that are run using the launcher scripts will use the Apache Pinot version you installed.
*   **Stopping a running example**

    To stop a running example, enter `Ctrl+C` in the same terminal where you ran the `docker run` command to start the example.

{% hint style="warning" %}
**macOS Monterey Users**

By default the Airplay receiver server runs on port 7000, which is also the port used by the Pinot Server in the Quick Start. You may see the following error when running these examples:

```
Failed to start a Pinot [SERVER]
java.lang.RuntimeException: java.net.BindException: Address already in use
	at org.apache.pinot.core.transport.QueryServer.start(QueryServer.java:103) ~[pinot-all-0.9.0-jar-with-dependencies.jar:0.9.0-cf8b84e8b0d6ab62374048de586ce7da21132906]
	at org.apache.pinot.server.starter.ServerInstance.start(ServerInstance.java:158) ~[pinot-all-0.9.0-jar-with-dependencies.jar:0.9.0-cf8b84e8b0d6ab62374048de586ce7da21132906]
	at org.apache.helix.manager.zk.ParticipantManager.handleNewSession(ParticipantManager.java:110) ~[pinot-all-0.9.0-jar-with-dependencies.jar:0.9.0-cf8b84e8b0d6ab62374048de586ce7da2113
```

If you disable the Airplay receiver server and try again, you shouldn't see this error message anymore.
{% endhint %}

{% hint style="info" %}
**Use canonical quickstart types for new examples.** Use `BATCH` (or `OFFLINE`) for batch examples and `REALTIME` (or `STREAM`) for streaming examples. Each canonical quickstart initializes the samples that were previously started by separate feature-specific quickstarts and runs their sample queries.

The following legacy types remain available as deprecated aliases, but emit a warning and are not listed in the command help:

* Use `BATCH` instead of `MULTI_STAGE`, `JOIN`, `TIMESTAMP`, `BATCH_JSON_INDEX`, or `BATCH_COMPLEX_TYPE`.
* Use `REALTIME` instead of `UPSERT`, `PARTIAL_UPSERT`, `UPSERT_JSON_INDEX`, `REALTIME_JSON_INDEX`, or `REALTIME_COMPLEX_TYPE`.
{% endhint %}

## Command Options

All QuickStart commands support the following optional parameters in addition to `-type`:

| Option | Aliases | Description |
|--------|---------|-------------|
| `-type` | | The quickstart type to run (see sections below). |
| `-tmpDir` | `-quickstartDir`, `-dataDir` | Directory to store quickstart data. Use this to persist data across restarts so that tables and segments are reloaded from disk instead of being regenerated. |
| `-bootstrapTableDir` | | A list of directories, each containing a table schema, table config, and raw data. Use this with `-type EMPTY` or `-type GENERIC` to load your own tables into the quickstart cluster. |
| `-configFile` | `-configFilePath` | Path to a properties file that overrides default Pinot configuration values (controller, broker, server, etc.). |
| `-zkAddress` | `-zkUrl`, `-zkExternalAddress` | URL for an external ZooKeeper instance (e.g. `localhost:2181`) instead of using the default embedded instance. |
| `-kafkaBrokerList` | | Kafka broker list for streaming quickstarts (e.g. `localhost:9092`). Use this to connect to an external Kafka cluster instead of the embedded one. |

**Example: Persist data across restarts**

```bash
# First run: quickstart generates data in the specified directory
./bin/pinot-admin.sh QuickStart -type batch -dataDir /tmp/pinot-quick-start

# Subsequent runs: quickstart reloads existing data from disk
./bin/pinot-admin.sh QuickStart -type batch -dataDir /tmp/pinot-quick-start
```

**Example: Use an external ZooKeeper and custom config**

```bash
./bin/pinot-admin.sh QuickStart -type batch \
    -zkAddress localhost:2181 \
    -configFile /path/to/pinot-quickstart.conf
```

**Example: Load custom tables into an empty cluster**

```bash
./bin/pinot-admin.sh QuickStart -type EMPTY \
    -bootstrapTableDir /path/to/my-table-dir
```

## Batch Processing

This example demonstrates how to do batch processing with Pinot. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates the `baseballStats` table
* Launches a standalone data ingestion job that builds one segment for a given CSV data file for the `baseballStats` table and pushes the segment to the Pinot Controller.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## Batch JSON

This example demonstrates how to import and query JSON documents in Pinot. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates the `githubEvents` table
* Launches a standalone data ingestion job that builds one segment for a given JSON data file for the `githubEvents` table and pushes the segment to the Pinot Controller.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## Batch with complex data types

This example demonstrates how to do batch processing in Pinot where the the data items have complex fields that need to be unnested. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates the `githubEvents` table
* Launches a standalone data ingestion job that builds one segment for a given JSON data file for the `githubEvents` table and pushes the segment to the Pinot Controller.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## Streaming

This example demonstrates how to do stream processing with Pinot. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates `meetupRsvp` table
* Launches a `meetup` stream
* Publishes data to a Kafka topic `meetupRSVPEvents` that is subscribed to by Pinot.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type stream
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type stream
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type stream
```
{% endtab %}
{% endtabs %}

## Streaming JSON

This example demonstrates how to do stream processing with JSON documents in Pinot. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates `meetupRsvp` table
* Launches a `meetup` stream
* Publishes data to a Kafka topic `meetupRSVPEvents` that is subscribed to by Pinot
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type realtime
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type realtime
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type realtime
```
{% endtab %}
{% endtabs %}

## Streaming with minion cleanup

This example demonstrates how to do stream processing in Pinot with RealtimeToOfflineSegmentsTask and MergeRollupTask minion tasks continuously optimizing segments as data gets ingested. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, Pinot Minion, and Pinot Server.
* Creates `githubEvents` table
* Launches a GitHub events stream
* Publishes data to a Kafka topic `githubEvents` that is subscribed to by Pinot.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type realtime_minion
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type realtime_minion
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type realtime_minion
```
{% endtab %}
{% endtabs %}

## Streaming with complex data types

This example demonstrates how to do stream processing in Pinot where the stream contains items that have complex fields that need to be unnested. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, Pinot Minion, and Pinot Server.
* Creates `meetupRsvp` table
* Launches a `meetup` stream
* Publishes data to a Kafka topic `meetupRSVPEvents` that is subscribed to by Pinot.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type realtime
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type realtime
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type realtime
```
{% endtab %}
{% endtabs %}

## Upsert

This example demonstrates how to do [stream processing with upsert](../../build-with-pinot/ingestion/upsert-and-dedup/upsert.md) with Pinot. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates `meetupRsvp` table
* Launches a `meetup` stream
* Publishes data to a Kafka topic `meetupRSVPEvents` that is subscribed to by Pinot
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type realtime
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type realtime
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type realtime
```
{% endtab %}
{% endtabs %}

## Upsert JSON

This example demonstrates how to do [stream processing with upsert](../../build-with-pinot/ingestion/upsert-and-dedup/upsert.md) with JSON documents in Pinot. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates `meetupRsvp` table
* Launches a `meetup` stream
* Publishes data to a Kafka topic `meetupRSVPEvents` that is subscribed to by Pinot
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type realtime
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type realtime
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type realtime
```
{% endtab %}
{% endtabs %}

## Hybrid

This example demonstrates how to do hybrid stream and batch processing with Pinot. The command:

1. Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
2. Creates `airlineStats` table
3. Launches a standalone data ingestion job that builds segments under a given directory of Avro files for the `airlineStats` table and pushes the segments to the Pinot Controller.
4. Launches a stream of flights stats
5. Publishes data to a Kafka topic `airlineStatsEvents` that is subscribed to by Pinot.
6. Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type hybrid
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type hybrid
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type hybrid
```
{% endtab %}
{% endtabs %}

## Join

This example demonstrates how to do joins in Pinot using the [Lookup UDF](../../build-with-pinot/querying-and-sql/lookup-udf-join.md). The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server in the same container.
* Creates the `baseballStats` table
* Launches a data ingestion job that builds one segment for a given CSV data file for the `baseballStats` table and pushes the segment to the Pinot Controller.
* Creates the `dimBaseballTeams` table
* Launches a data ingestion job that builds one segment for a given CSV data file for the `dimBaseballStats` table and pushes the segment to the Pinot Controller.
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## Logical Table

This example demonstrates how to use logical tables in Pinot, which provide a unified query interface over multiple physical tables. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, Pinot Server, and Pinot Minion.
* Creates three physical tables (`ordersUS_OFFLINE`, `ordersEU_OFFLINE`, `ordersAPAC_OFFLINE`) representing regional order data
* Creates a logical table (`orders`) that provides a unified view over all regional tables
* Issues sample queries to both physical and logical tables

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type LOGICAL_TABLE
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type LOGICAL_TABLE
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type LOGICAL_TABLE
```
{% endtab %}
{% endtabs %}

For more details on logical tables, see [Logical Table](../../basics/components/table/logical-table.md).

## Empty

This example starts a bare Pinot cluster with no tables or data loaded. Use this when you want to set up your own tables and schemas from scratch. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* No tables or data are created

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type EMPTY
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type EMPTY
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type EMPTY
```
{% endtab %}
{% endtabs %}

## Multi-Stage Query Engine

This example demonstrates the [multi-stage query engine](../../build-with-pinot/querying-and-sql/multi-stage-query/README.md) with self-joins, dimension table joins, and vector distance queries. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates the `baseballStats` table and a fine food reviews table
* Launches data ingestion jobs to build segments and push them to the Pinot Controller.
* Issues sample multi-stage queries including joins and vector distance queries

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## Partial Upsert

This example demonstrates how to do [stream processing with partial upsert](../../build-with-pinot/ingestion/upsert-and-dedup/upsert.md) in Pinot, where individual fields can be updated independently while preserving other column values. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates a realtime table with partial upsert enabled
* Publishes data to a Kafka topic that is subscribed to by Pinot
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type realtime
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type realtime
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type realtime
```
{% endtab %}
{% endtabs %}

## Geospatial

This example demonstrates [geospatial indexing and query capabilities](../../build-with-pinot/indexing/geospatial-support.md) in Pinot. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates a table with geospatial indexes
* Launches a data ingestion job and pushes segments to the Pinot Controller.
* Issues sample geospatial queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type GEOSPATIAL
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type GEOSPATIAL
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type GEOSPATIAL
```
{% endtab %}
{% endtabs %}

## Null Handling

This example demonstrates [null value handling](../../build-with-pinot/querying-and-sql/null-value-support.md) features in Pinot. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates a table containing null values
* Launches a data ingestion job and pushes segments to the Pinot Controller.
* Issues sample queries demonstrating IS NULL, IS NOT NULL, and aggregate behavior with nulls

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type NULL_HANDLING
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type NULL_HANDLING
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type NULL_HANDLING
```
{% endtab %}
{% endtabs %}

## TPC-H

This example loads the 8 TPC-H benchmark tables (customer, lineitem, nation, orders, part, partsupp, region, supplier) for multi-stage query testing. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates all 8 TPC-H tables
* Launches data ingestion jobs to build segments for each table and pushes them to the Pinot Controller.
* Issues sample TPC-H benchmark queries using the multi-stage query engine

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type TPCH
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type TPCH
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type TPCH
```
{% endtab %}
{% endtabs %}

## Colocated Join

This example demonstrates [colocated join](../../build-with-pinot/querying-and-sql/multi-stage-query/join-strategies/colocated-join-strategy.md) operations using the multi-stage query engine with various partition configurations and parallelism hints. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates tables with matching partition configurations for colocated joins
* Launches data ingestion jobs and pushes segments to the Pinot Controller.
* Issues sample colocated join queries

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type COLOCATED_JOIN
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type COLOCATED_JOIN
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type COLOCATED_JOIN
```
{% endtab %}
{% endtabs %}

## Lookup Join

This example demonstrates the [lookup join strategy](../../build-with-pinot/querying-and-sql/multi-stage-query/join-strategies/lookup-join-strategy.md) using dimension tables with the multi-stage query engine. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates fact and dimension tables
* Launches data ingestion jobs and pushes segments to the Pinot Controller.
* Issues sample lookup join queries

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type LOOKUP_JOIN
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type LOOKUP_JOIN
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type LOOKUP_JOIN
```
{% endtab %}
{% endtabs %}

## Auth

This example demonstrates how to run Pinot with [basic authentication](../../operate-pinot/authentication/basic-auth-access-control.md) enabled. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server with basic auth configured.
* Creates tables and loads data with authentication enabled
* Issues sample authenticated queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type AUTH
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type AUTH
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type AUTH
```
{% endtab %}
{% endtabs %}

## Sorted Column

This example demonstrates sorted column indexing in Pinot with a generated dataset containing sorted columns. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates a table with sorted column configuration
* Generates a 100,000-row dataset and ingests it into Pinot
* Issues sample queries demonstrating sorted index performance

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type SORTED
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type SORTED
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type SORTED
```
{% endtab %}
{% endtabs %}

## Timestamp Index

This example demonstrates [timestamp index](../../build-with-pinot/indexing/timestamp-index.md) functionality, showing timestamp extraction at different granularities and dateTrunc bucketing. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates the `airlineStats` table with timestamp indexes
* Launches a data ingestion job and pushes segments to the Pinot Controller.
* Issues sample queries demonstrating timestamp extraction and bucketing

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## GitHub Events

This example sets up a streaming demo using GitHub events data. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates a `pullRequestMergedEvents` realtime table
* Publishes GitHub event data to a Kafka topic that is subscribed to by Pinot
* Issues sample analytical queries on the GitHub event data

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type GITHUB_EVENTS
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type GITHUB_EVENTS
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type GITHUB_EVENTS
```
{% endtab %}
{% endtabs %}

## Multi-Cluster

This example demonstrates cross-cluster querying via [logical tables](../../basics/components/table/logical-table.md) by initializing two independent Pinot clusters. The command:

* Starts two independent Pinot clusters, each with their own Zookeeper, Controller, Broker, and Server.
* Creates physical tables in each cluster
* Creates a logical table that spans both clusters
* Issues sample cross-cluster queries

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type MULTI_CLUSTER
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type MULTI_CLUSTER
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type MULTI_CLUSTER
```
{% endtab %}
{% endtabs %}

## Batch with Multi-Directory (Tiered Storage)

This example demonstrates multi-directory (tiered storage) support with hot and cold tiers. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server with tiered storage configured.
* Creates the `airlineStats` table with hot and cold storage tiers
* Launches a data ingestion job and pushes segments to the Pinot Controller.
* Issues sample queries that run across storage tiers

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type BATCH_MULTIDIR
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type BATCH_MULTIDIR
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type BATCH_MULTIDIR
```
{% endtab %}
{% endtabs %}

## Time Series

{% hint style="info" %}
For production use, you should ideally implement your own Time Series Language Plugin. The one included in the Pinot distribution is only for demonstration purposes.
{% endhint %}

This examples demonstrates Pinot's Time Series Engine, which supports running pluggable Time Series Query Languages via a Language Plugin architecture. The default Pinot binary includes a toy Time Series Query Language using the same name as Uber's language "m3ql". You can try the following query as an example:

```
fetch{table="meetupRsvp_REALTIME",filter="",ts_column="__metadata$recordTimestamp",ts_unit="MILLISECONDS",value="1"}
| sum{rsvp_count}
| transformNull{0}
| keepLastValue{}
```

![](../../.gitbook/assets/image.png)

**

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type time_series
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type time_series
```
{% endtab %}

{% tab title="Brew" %}
```
pinot-admin QuickStart -type time_series
```
{% endtab %}
{% endtabs %}
