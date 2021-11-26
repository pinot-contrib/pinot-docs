---
description: >-
  This section describes quick start commands that launch all Pinot components
  in a single process.
---

# Quick Start

Pinot ships with QuickStart commands that launch Pinot components in a single process and import pre-built datasets.
These QuickStarts are a good place if you're just getting started with Pinot.

## Batch

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
    apachepinot/pinot:0.9.0 QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch
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
    apachepinot/pinot:0.9.0 QuickStart \
    -type stream
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type stream
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
6. Issues sample queries to Pinot&#x20;

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:0.9.0 QuickStart \
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
    apachepinot/pinot:0.9.0 QuickStart \
    -type join
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type join
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
    apachepinot/pinot:0.9.0 QuickStart \
    -type upsert
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type upsert
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
    apachepinot/pinot:0.9.0 QuickStart \
    -type batch_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type batch_json_index
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
    apachepinot/pinot:0.9.0 QuickStart \
    -type stream_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type stream_json_index
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
    apachepinot/pinot:0.9.0 QuickStart \
    -type upsert_json_index
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type upsert_json_index
```
{% endtab %}
{% endtabs %}

## Streaming with minion cleanup

This example demonstrates how to do stream processing with Pinot with RealtimeToOfflineSegmentsTask and MergeRollupTask minion tasks continuously optimizing segments as data gets ingested.
The command:

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
    apachepinot/pinot:0.9.0 QuickStart \
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

This example demonstrates how to do stream processing with Pinot where the stream contains items that have complex fields that need to be unnested. 
The command:

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
    apachepinot/pinot:0.9.0 QuickStart \
    -type stream_complex_type
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin.sh QuickStart -type stream_complex_type
```
{% endtab %}
{% endtabs %}