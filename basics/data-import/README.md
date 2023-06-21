---
description: >-
  This page lists options for importing data into Pinot with links to detailed instructions with examples.
---

# Import Data

There are multiple options for importing data into Pinot. The pages in this section provide step-by-step instructions for importing records into Pinot, supported by our [plugin architecture](../../developers/plugin-architecture/). The intent is to get you up and running with imported data as quickly as possible.

Pinot supports multiple file input formats without needing to change anything other than the file name. Each example imports a ready-made dataset so you can see how things work without needing to find or create your own dataset.

## Pinot Batch Ingestion

These guides show you how to import data from popular big data platforms.

{% content-ref url="batch-ingestion/spark.md" %}
[spark.md](batch-ingestion/spark.md)
{% endcontent-ref %}

{% content-ref url="batch-ingestion/hadoop.md" %}
[hadoop.md](batch-ingestion/hadoop.md)
{% endcontent-ref %}

## Pinot Stream Ingestion

This guide shows you how to import data using stream ingestion from Apache Kafka topics.

{% content-ref url="pinot-stream-ingestion/import-from-apache-kafka.md" %}
[import-from-apache-kafka.md](pinot-stream-ingestion/import-from-apache-kafka.md)
{% endcontent-ref %}

This guide shows you how to import data using stream ingestion with upsert.

{% content-ref url="upsert.md" %}
[upsert.md](upsert.md)
{% endcontent-ref %}

This guide shows you how to import data using stream ingestion with deduplication.

{% content-ref url="dedup.md" %}
[dedup.md](dedup.md)
{% endcontent-ref %}

This guide shows you how to import data using stream ingestion with CLP.

{% content-ref url="clp.md" %}
[clp.md](clp.md)
{% endcontent-ref %}

## Pinot File Systems

By default, Pinot does not come with a storage layer, so all the data sent won't be stored in case of system crash. In order to persistently store the generated segments, you will need to change controller and server configs to add a deep storage. See [File systems](pinot-file-system/) for all the info and related configs.

These guides show you how to import data and persist it in these file systems.

{% content-ref url="pinot-file-system/amazon-s3.md" %}
[amazon-s3.md](pinot-file-system/amazon-s3.md)
{% endcontent-ref %}

{% content-ref url="pinot-file-system/import-from-adls-azure.md" %}
[import-from-adls-azure.md](pinot-file-system/import-from-adls-azure.md)
{% endcontent-ref %}

{% content-ref url="pinot-file-system/import-from-gcp.md" %}
[import-from-gcp.md](pinot-file-system/import-from-gcp.md)
{% endcontent-ref %}

{% content-ref url="pinot-file-system/import-from-hdfs.md" %}
[import-from-hdfs.md](pinot-file-system/import-from-hdfs.md)
{% endcontent-ref %}

## Pinot Input Formats

This guide shows you how to import data from various Pinot-supported input formats.

{% content-ref url="pinot-input-formats.md" %}
[pinot-input-formats.md](pinot-input-formats.md)
{% endcontent-ref %}

This guide shows you how to handle the complex type in the ingested data, such as map and array.

{% content-ref url="complex-type.md" %}
[complex-type.md](complex-type.md)
{% endcontent-ref %}
