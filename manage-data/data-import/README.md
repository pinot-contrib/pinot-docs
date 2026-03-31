---
description: >-
  This page lists options for importing data into Apache Pinot™ with links to
  detailed instructions with examples.
---

# Import Data

There are multiple options for importing data into Apache Pinot™. The pages in this section provide step-by-step instructions for importing records into Pinot, supported by our [plugin architecture](../../developers/plugin-architecture/). The intent is to get you up and running with imported data as quickly as possible.

Pinot supports multiple file input formats without needing to change anything other than the file name. Each example imports a ready-made dataset so you can see how things work without needing to find or create your own dataset.

## Pinot Batch Ingestion

These guides show you how to import data from popular big data platforms.

{% content-ref url="../../build-with-pinot/ingestion/batch-ingestion/spark.md" %}
[spark.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/batch-ingestion/spark.md)
{% endcontent-ref %}

{% content-ref url="../../build-with-pinot/ingestion/batch-ingestion/hadoop.md" %}
[hadoop.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/batch-ingestion/hadoop.md)
{% endcontent-ref %}

## Pinot Stream Ingestion

This guide shows you how to import data using stream ingestion from Apache Kafka topics.

{% content-ref url="../../build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md" %}
[import-from-apache-kafka.md](../../build-with-pinot/ingestion/stream-ingestion/import-from-apache-kafka.md)
{% endcontent-ref %}

This guide shows you how to import data using stream ingestion with upsert.

{% content-ref url="../../build-with-pinot/ingestion/upsert-and-dedup/upsert.md" %}
[upsert.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/upsert-and-dedup/upsert.md)
{% endcontent-ref %}

This guide shows you how to import data using stream ingestion with deduplication.

{% content-ref url="../../build-with-pinot/ingestion/upsert-and-dedup/dedup.md" %}
[dedup.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/upsert-and-dedup/dedup.md)
{% endcontent-ref %}

This guide shows you how to import data using stream ingestion with CLP.

{% content-ref url="../../build-with-pinot/ingestion/stream-ingestion/clp.md" %}
[clp.md](../../build-with-pinot/ingestion/stream-ingestion/clp.md)
{% endcontent-ref %}

## Pinot file systems

By default, Pinot does not come with a storage layer, so all the data sent won't be stored in case of system crash. In order to persistently store the generated segments, you will need to change controller and server configs to add a deep storage. See [File systems](pinot-file-system/) for all the info and related configs.

These guides show you how to import data and persist it in these file systems.

{% content-ref url="../../build-with-pinot/ingestion/file-systems/amazon-s3.md" %}
[amazon-s3.md](../../build-with-pinot/ingestion/file-systems/amazon-s3.md)
{% endcontent-ref %}

{% content-ref url="../../build-with-pinot/ingestion/file-systems/import-from-adls-azure.md" %}
[import-from-adls-azure.md](../../build-with-pinot/ingestion/file-systems/import-from-adls-azure.md)
{% endcontent-ref %}

{% content-ref url="../../build-with-pinot/ingestion/file-systems/import-from-gcp.md" %}
[import-from-gcp.md](../../build-with-pinot/ingestion/file-systems/import-from-gcp.md)
{% endcontent-ref %}

{% content-ref url="../../build-with-pinot/ingestion/file-systems/import-from-hdfs.md" %}
[import-from-hdfs.md](../../build-with-pinot/ingestion/file-systems/import-from-hdfs.md)
{% endcontent-ref %}

## Pinot input formats

This guide shows you how to import data from various Pinot-supported input formats.

{% content-ref url="../../build-with-pinot/ingestion/pinot-input-formats.md" %}
[../../build-with-pinot/ingestion/pinot-input-formats.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/pinot-input-formats.md)
{% endcontent-ref %}

This guide shows you how to handle the complex type in the ingested data, such as map and array.

{% content-ref url="complex-type/" %}
[complex-type](complex-type/)
{% endcontent-ref %}

This guide shows additional examples on how to work with complex types.

{% content-ref url="../../build-with-pinot/ingestion/complex-type/complex-type-examples.md" %}
[complex-type-examples.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/complex-type/complex-type-examples.md)
{% endcontent-ref %}

This guide shows you how to handle records with dynamic schemas, like JSON log events.

{% content-ref url="../../build-with-pinot/ingestion/schema-conforming-transformer.md" %}
[../../build-with-pinot/ingestion/schema-conforming-transformer.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/schema-conforming-transformer.md)
{% endcontent-ref %}

## Reloading and uploading existing Pinot segments

This guide shows you how to reload Pinot segments from your deep store.

{% content-ref url="../../operate-pinot/segment-reload.md" %}
[segment-reload.md](../../operate-pinot/segment-reload.md)
{% endcontent-ref %}

This guide shows you how to upload Pinot segments from an old, closed Pinot instance.

{% content-ref url="../../build-with-pinot/ingestion/segment-upload.md" %}
[../../build-with-pinot/ingestion/segment-upload.md](../../build-with-pinot/ingestion/../../build-with-pinot/ingestion/segment-upload.md)
{% endcontent-ref %}
