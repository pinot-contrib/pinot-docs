---
description: Storing records with dynamic schemas in a table with a fixed schema.
---

# Ingest records with dynamic schemas

Some domains (e.g., logging) generate records where each record can have a different set of keys, whereas Pinot tables have a relatively static schema. Since these records have varying keys, it is impractical to store each field in its own table column. At the same time, most (if not all) fields may be important to the user, so we should not drop any field unnecessarily.

The [SchemaConformingTransformer](https://github.com/apache/pinot/blob/master/pinot-segment-local/src/main/java/org/apache/pinot/segment/local/recordtransformer/SchemaConformingTransformer.java) is a [RecordTransformer](https://github.com/apache/pinot/blob/master/pinot-segment-local/src/main/java/org/apache/pinot/segment/local/recordtransformer/RecordTransformer.java) that can transform records with dynamic schemas such that they can be ingested in a table with a static schema. The transformer primarily takes record-fields that don't exist in the schema and stores them in a type of catchall field.

For example, consider this record:

```json
{
  "timestamp": 1687786535928,
  "hostname": "host1",
  "HOSTNAME": "host1",
  "level": "INFO",
  "message": "Started processing job1",
  "tags": {
    "platform": "data",
    "service": "serializer",
    "params": {
      "queueLength": 5,
      "timeout": 299,
      "userData_noIndex": {
        "nth": 99
      }
    }
  }
}
```

Let's say the table's schema contains the following fields:
* timestamp
* hostname
* level
* message
* tags.platform
* tags.service
* indexableExtras
* unindexableExtras

Without this transformer, the `HOSTNAME` field and the entire `tags` field would be dropped when storing the record in the table. However, with this transformer, the record would be transformed into the following:

```json
{
  "timestamp": 1687786535928,
  "hostname": "host1",
  "level": "INFO",
  "message": "Started processing job1",
  "tags.platform": "data",
  "tags.service": "serializer",
  "indexableExtras": {
    "tags": {
      "params": {
        "queueLength": 5,
        "timeout": 299
      }
    }
  },
  "unindexableExtras": {
    "tags": {
      "userData_noIndex": {
        "nth": 99
      }
    }
  }
}
```

Notice that the transformer does the following:
* Flattens nested fields which exist in the schema, like `tags.platform`
* Drops some fields like `HOSTNAME`, where `HOSTNAME` must be listed as a field in the config option `fieldPathsToDrop`
* Moves fields which don't exist in the schema and have the suffix `_noIndex` into the `unindexableExtras` field (the field name is configurable)
* Moves any remaining fields which don't exist in the schema into the `indexableExtras` field (the field name is configurable)

The `unindexableExtras` field allows the transformer to separate fields which don't need indexing (because they are only retrieved, not searched) from those that do.

## SchemaConformingTransformer Configuration

To use the transformer, add the `schemaConformingTransformerConfig` option in the `ingestionConfig` section of your table configuration, as shown in the following example.

For example:

```json
{
  "ingestionConfig": {
    "schemaConformingTransformerConfig": {
      "indexableExtrasField": "extras",
      "unindexableExtrasField": "extrasNoIndex",
      "unindexableFieldSuffix": "_no_index",
      "fieldPathsToDrop": [
        "HOSTNAME"
      ]
    }
  }
}
```

Available configuration options are listed in [SchemaConformingTransformerConfig](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/config/table/ingestion/SchemaConformingTransformerConfig.java).
