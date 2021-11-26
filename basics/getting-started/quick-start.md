---
description: >-
  This section describes quick start commands that launch all Pinot components
  in a single process.
---

# Quick Start

Pinot ships with multiple QuickStart command that can be used to launch Pinot components in a single process and import pre-built datasets.

## Batch

This example demonstrates how to do batch processing with Pinot. The command:

* Starts Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates the `baseballStats` table
* Launches a standalone data ingestion job that:
  * Builds one Pinot segment for a given CSV data file for table `baseballStats`
  * Pushes the built segment to the Pinot Controller
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    --name pinot-quickstart-batch \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type batch
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin QuickStart -type batch
```
{% endtab %}
{% endtabs %}

## Streaming

This example demonstrates how to do stream processing with Pinot. The command:

* Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
* Creates `meetupRsvp` table
* Launches a `meetup`** **stream
* Publishes data to a Kafka topic `meetupRSVPEvents` to be subscribed to by Pinot
* Issues sample queries to Pinot

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    --name pinot-quickstart-streaming \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type stream
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin QuickStart -type stream
```
{% endtab %}
{% endtabs %}

## Hybrid

This example demonstrates how to do hybrid stream and batch processing with Pinot. The command:

1. Starts Apache Kafka, Apache Zookeeper, Pinot Controller, Pinot Broker, and Pinot Server.
2. Creates `airlineStats` table
3. Launches a standalone data ingestion job that:
   * Builds Pinot segments under a given directory of Avro files for table `airlineStats`
   * Pushes built segments to Pinot controller
4. Launches a** **stream of flights stats
5. Publishes data to a Kafka topic `airlineStatsEvents` to be subscribed to by Pinot
6. Issues sample queries to Pinot&#x20;

{% tabs %}
{% tab title="Docker" %}
```
docker run \
    --name pinot-quickstart-hybrid \
    -p 9000:9000 \
    apachepinot/pinot:latest QuickStart \
    -type hybrid
```
{% endtab %}

{% tab title="Launcher scripts" %}
```
./bin/pinot-admin QuickStart -type hybrid
```
{% endtab %}
{% endtabs %}
