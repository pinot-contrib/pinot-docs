---
description: >-
  This section is an overview of the various options for importing data into
  Pinot.
---

# Import Data

There are multiple options for importing data into Pinot. These guides are ready-made examples that show you step-by-step instructions for importing records into Pinot, supported by our [plugin architecture](../../developers/plugin-architecture/).

These guides are meant to get you up and running with imported data as quick as possible. Pinot supports multiple file input formats without needing to change anything other than the file name. Each example imports a ready-made dataset so you can see how things work without needing to bring your own dataset.

## Pinot Batch Ingestion

{% page-ref page="batch-ingestion/spark.md" %}

{% page-ref page="batch-ingestion/hadoop.md" %}

## Pinot Stream Ingestion

This guide will show you how to import data using stream ingestion from Apache Kafka topics.

{% page-ref page="pinot-stream-ingestion/import-from-apache-kafka.md" %}

This guide will show you how to import data using stream ingestion with upsert.

{% page-ref page="upsert.md" %}

This guide will show you how to import data using stream ingestion with deduplication.

{% page-ref page="dedup.md" %}

## Pinot File Systems

By default, Pinot does not come with a storage layer, so all the data sent, won't be stored in case of system crash. In order to persistently store the generated segments, you will need to change controller and server configs to add a deep storage. Checkout [File systems](pinot-file-system/) for all the info and related configs.

These guides will show you how to import data as well as persist it in the file systems.

{% page-ref page="pinot-file-system/amazon-s3.md" %}

{% page-ref page="pinot-file-system/import-from-adls-azure.md" %}

{% page-ref page="pinot-file-system/import-from-gcp.md" %}

{% page-ref page="pinot-file-system/import-from-hdfs.md" %}

## Pinot Input Formats

These guides will show you how to import data from a Pinot supported input format.

{% page-ref page="pinot-input-formats.md" %}

This guide will show you how to handle the complex type in the ingested data, such as map and array.

{% page-ref page="complex-type.md" %}

