---
description: >-
  This section describes quick start commands that launch all Pinot components
  in a single process.
---

# Quick Start Examples

Pinot ships with `QuickStart` commands that launch Pinot components in a single process and import pre-built datasets. These quick start examples are a good place if you're just getting started with Pinot. The examples begin with the [Batch Processing](quick-start.md#batch-processing) example, after the following notes.

{% hint style="info" %}
**Prerequisites**

You must have either [installed Pinot locally](running-pinot-locally.md) or [have Docker installed if you want to use the Pinot Docker image](running-pinot-in-docker.md).
{% endhint %}

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
**Stopping a running example**

To stop a running example, enter `Ctrl+C` in the same terminal where you ran the `docker run` command to start the example.
{% endhint %}

{% hint style="info" %}
**Pinot versions in examples**

The Docker-based examples on this page use `pinot:latest`, which instructs Docker to pull and use the most recent release of Apache Pinot. If you prefer to use a specific release instead, you can designate it by replacing `latest` with the release number, like this: `pinot:0.12.1`.

The local install-based examples that are run using the launcher scripts will use the Apache Pinot version you installed.
{% endhint %}

{% hint style="info" %}
**Running examples with Docker on Mac M1**

Add the `-arm64` suffix to the `run` commands, like this:

```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:latest-arm64 QuickStart \
    -type batch
```
{% endhint %}

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
    -type batch_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch_json_index
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
    -type batch_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch_json_index
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
    -type stream_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type stream_json_index
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
    -type stream_complex_type
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type stream_complex_type
```
{% endtab %}
{% endtabs %}

## Upsert

This example demonstrates how to do [stream processing with upsert](../data-import/upsert.md) with Pinot. The command:

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
    -type upsert
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type upsert
```
{% endtab %}
{% endtabs %}

## Upsert JSON

This example demonstrates how to do [stream processing with upsert](../data-import/upsert.md) with JSON documents in Pinot. The command:

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
    -type upsert_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type upsert_json_index
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
{% endtabs %}

## Join

This example demonstrates how to do joins in Pinot using the [Lookup UDF](../../users/user-guide-query/lookup-udf-join.md). The command:

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
    -type join
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type join
```
{% endtab %}
{% endtabs %}
