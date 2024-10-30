---
description: >-
  This page lists options for importing data into Apache Pinot™ with links to
  detailed instructions with examples.
---

# Import Data

There are multiple options for importing data into Apache Pinot™. The pages in this section provide step-by-step instructions for importing records into Pinot, supported by our [plugin architecture](../../developers/plugin-architecture/). The intent is to get you up and running with imported data as quickly as possible.

Pinot supports multiple file input formats without needing to change anything other than the file name. Each example imports a readsdsdy-made dataset so you can see how things work without needing to find or create your own dataset.

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

## Pinot file systems

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

## Pinot input formats

This guide shows you how to import data from various Pinot-supported input formats.

{% content-ref url="pinot-input-formats.md" %}
[pinot-input-formats.md](pinot-input-formats.md)
{% endcontent-ref %}

This guide shows you how to handle the complex type in the ingested data, such as map and array.

{% content-ref url="complex-type.md" %}
[complex-type.md](complex-type.md)
{% endcontent-ref %}

This guide shows you how to unnest JSON records that are grouped into an array at the root level.

{% content-ref url="unnest-json-array.md" %}
[unnest-json-array.md](unnest-json-array.md)
{% endcontent-ref %}

This guide shows you how to handle records with dynamic schemas, like JSON log events.

{% content-ref url="schema-conforming-transformer.md" %}
[schema-conforming-transformer.md](schema-conforming-transformer.md)
{% endcontent-ref %}

## Reloading and uploading existing Pinot segments

This guide shows you how to reload Pinot segments from your deep store.

{% content-ref url="segment-reload.md" %}
[segment-reload.md](segment-reload.md)
{% endcontent-ref %}

This guide shows you how to upload Pinot segments from an old, closed Pinot instance.

{% content-ref url="segment-upload.md" %}
[segment-upload.md](segment-upload.md)
{% endcontent-ref %}
