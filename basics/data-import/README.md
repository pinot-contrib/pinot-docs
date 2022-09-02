---
description: >-
  This section is an overview of the various options for importing data into
  Pinot.
---

# Import Data

There are multiple options for importing data into Pinot. These guides are ready-made examples that show you step-by-step instructions for importing records into Pinot, supported by our [plugin architecture](../../developers/plugin-architecture/).

These guides are meant to get you up and running with imported data as quick as possible. Pinot supports multiple file input formats without needing to change anything other than the file name. Each example imports a ready-made dataset so you can see how things work without needing to bring your own dataset.

## Pinot Batch Ingestion

{% content-ref url="batch-ingestion/spark.md" %}
[spark.md](batch-ingestion/spark.md)
{% endcontent-ref %}

{% content-ref url="batch-ingestion/hadoop.md" %}
[hadoop.md](batch-ingestion/hadoop.md)
{% endcontent-ref %}

## Pinot Stream Ingestion

This guide will show you how to import data using stream ingestion from Apache Kafka topics.

{% content-ref url="pinot-stream-ingestion/import-from-apache-kafka.md" %}
[import-from-apache-kafka.md](pinot-stream-ingestion/import-from-apache-kafka.md)
{% endcontent-ref %}

This guide will show you how to import data using stream ingestion with upsert.

{% content-ref url="upsert.md" %}
[upsert.md](upsert.md)
{% endcontent-ref %}

This guide will show you how to import data using stream ingestion with deduplication.

{% content-ref url="dedup.md" %}
[dedup.md](dedup.md)
{% endcontent-ref %}

## Pinot File Systems

By default, Pinot does not come with a storage layer, so all the data sent, won't be stored in case of system crash. In order to persistently store the generated segments, you will need to change controller and server configs to add a deep storage. Checkout [File systems](pinot-file-system/) for all the info and related configs.

These guides will show you how to import data as well as persist it in the file systems.

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

These guides will show you how to import data from a Pinot supported input format.

{% content-ref url="pinot-input-formats.md" %}
[pinot-input-formats.md](pinot-input-formats.md)
{% endcontent-ref %}

This guide will show you how to handle the complex type in the ingested data, such as map and array.

{% content-ref url="complex-type.md" %}
[complex-type.md](complex-type.md)
{% endcontent-ref %}
