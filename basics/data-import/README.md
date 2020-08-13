---
description: >-
  This section is an overview of the various options for importing data into
  Pinot.
---

# Data import

There are multiple options for importing data into Pinot. These guides are ready-made examples that show you step-by-step instructions for importing records into Pinot, supported by our [plugin architecture](../../plugins/plugin-architecture.md). These guides are meant to get you up and running with imported data as quick as possible. Pinot supports multiple file input formats without needing to change anything other than the file name. Each example imports a ready-made dataset so you can see how things work without needing to bring your own dataset.

## Pinot File Systems

These guides will show you how to import data from a supported file system.

{% page-ref page="pinot-file-system/import-from-adls-azure.md" %}

{% page-ref page="pinot-file-system/import-from-gcp.md" %}

{% page-ref page="pinot-file-system/import-from-hdfs.md" %}

## Pinot Input Formats

These guides will show you how to import data from a Pinot supported input format.

{% page-ref page="pinot-input-formats/import-from-csv.md" %}

{% page-ref page="pinot-input-formats/import-from-json.md" %}

{% page-ref page="pinot-input-formats/import-from-avro.md" %}

{% page-ref page="pinot-input-formats/import-from-parquet.md" %}

{% page-ref page="pinot-input-formats/import-from-thrift.md" %}

## Pinot Stream Ingestion

This guide will show you how to import data using stream ingestion from Apache Kafka topics.

{% page-ref page="pinot-stream-ingestion/import-from-apache-kafka.md" %}

