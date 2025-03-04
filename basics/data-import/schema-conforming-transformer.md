---
description: Storing records with dynamic schemas in a table with a fixed schema.
---

# Ingest and text index records with dynamic schemas

Some domains (e.g., logging) generate records where each record can have a different set of keys, whereas Pinot tables have a relatively static schema. For records with varying keys, it's impractical to store each field in its own table column. However, most (if not all) fields may be important, so fields should not be dropped unnecessarily.

Additionally, searching patterns on such table could also be complex and change frequently. Exact match, range query, prefix/suffix match, wildcard search and aggregation functions could be used on any old or newly created keys or values.


## SchemaConformingTransformer

The [SchemaConformingTransformer](https://github.com/apache/pinot/blob/master/pinot-segment-local/src/main/java/org/apache/pinot/segment/local/recordtransformer/SchemaConformingTransformer.java) is a [RecordTransformer](https://github.com/apache/pinot/blob/master/pinot-segment-local/src/main/java/org/apache/pinot/segment/local/recordtransformer/RecordTransformer.java) that can transform records with dynamic schemas such that they can be ingested in a table with a static schema. The transformer takes record fields that don't exist in the schema and stores them in a type of catchall field. Moreover, it builds a `__mergedTextIndex` field and takes advantage of Lucene to fulfill text search.

For example, consider this record:

```json
{
  "arrayField":[0, 1, 2, 3],
  "stringField":"a",
  "intField_noIndex":9,
  "string_noIndex":"z",
  "message": "a",
  "mapField":{
    "arrayField":[0, 1, 2, 3],
    "stringField":"a",
    "intField_noIndex":9,
    "string_noIndex":"z"
  },
  "mapField_noIndex":{
    "arrayField":[0, 1, 2, 3],
    "stringField":"a",
  },
  "nestedFields":{
    "arrayField":[0, 1, 2, 3],
    "stringField":"a",
    "intField_noIndex":9,
    "string_noIndex":"z",
    "mapField":{
      "arrayField":[0, 1, 2, 3],
      "stringField":"a",
      "intField_noIndex":9,
      "string_noIndex":"z"
    }
  }
}
```

Let's say the table's schema contains the following fields:
* arrayField
* mapField
* nestedFields
* nestedFields.stringField
* json_data
* json_data_no_idx
* __mergedTextIndex

Without this transformer, `stringField` field and fields ends with `_noIdx` would be dropped. `mapField` and `nestedFields` fields' storage needs to rely on the global setup in complexTransformers without granular customizations. However, with this transformer, the record would be transformed into the following:

```json
{
  "arrayField":[0, 1, 2, 3],
  "nestedFields.stringField":"a",
  "json_data":{
    "stringField":"a",
    "mapField":{
      "arrayField":[0, 1, 2, 3],
      "stringField":"a",
      "stringField":"aA_123"
    },
    "nestedFields":{
      "arrayField":[0, 1, 2, 3],
      "mapField":{
        "arrayField":[0, 1, 2, 3],
        "stringField":"a"
      }
    }
  },
  "json_data_no_idx":{
    "intField_noIndex":9,
    "string_noIndex":"z",
    "mapField":{
      "intField_noIndex":9,
      "string_noIndex":"z"
    },
    "mapField_noIndex":{
      "arrayField":[0, 1, 2, 3],
      "stringField":"a",
    },
    "nestedFields":{
      "intField_noIndex":9,
      "string_noIndex":"z",
      "mapField":{
        "intField_noIndex":9,
        "string_noIndex":"z"
      }
    }
  },
  "__mergedTextIndex": [
    // To be explained in following sections
  ]
}
```

Notice that there are 3 reserved (and configurable) fields `json_data`, `json_data_no_idx` and `__mergedTextIndex`. And the transformer does the following:
* Flattens nested fields all the way to the leaf node and:
  * Conducts special treatments if necessary according to the config
  * If the key path matches the schema, put the data into the dedicated field
  * Otherwise, put them into `json_data` or `json_data_no_idx` depending on its key suffix
* For keys in dedicated columns or json_data, puts them into `__mergedTextIndex` in the form of "Begin Anchor + value + Separator + key + End Anchor" to power the text matches.
* Additional functionalities by configurations
  * Drop fields `fieldPathsToDrop`
  * Preserve the subtree without flattening `fieldPathsToPreserveInput` and `fieldPathsToPreserveInputWithIndex`
  * Skip storaging the fields but still indexing it (`message` in the example) `fieldPathsToSkipStorage`
  * Skip indexing the fields `unindexableFieldSuffix`
  * Optimize case insensitive search `optimizeCaseInsensitiveSearch`
  * Map input key path to a schema name with customizations `columnNameToJsonKeyPathMap`
  * Support anonymous dot, {'a.b': 'c'} vs {'a': {'b': 'c}} `useAnonymousDotInFieldNames`
  * Truncate value by length `mergedTextIndexDocumentMaxLength`
  * Double ingestion to support schema evolution `fieldsToDoubleIngest`

## Table Configurations

### SchemaConformingTransformer Configuration

To use the transformer, add the `schemaConformingTransformerConfig` option in the `ingestionConfig` section of your table configuration, as shown in the following example.

For example:

```json
"schemaConformingTransformerConfig": {
  "enableIndexableExtras": true,
  "indexableExtrasField": "json_data",
  "enableUnindexableExtras": true,
  "unindexableExtrasField": "json_data_no_idx",
  "unindexableFieldSuffix": "_noindex",
  "fieldPathsToDrop": [],
  "fieldPathsToSkipStorage": [
    "message"
  ],
  "columnNameToJsonKeyPathMap": {},
  "mergedTextIndexField": "__mergedTextIndex",
  "useAnonymousDotInFieldNames": true,
  "optimizeCaseInsensitiveSearch": false,
  "reverseTextIndexKeyValueOrder": true,
  "mergedTextIndexDocumentMaxLength": 32766,
  "mergedTextIndexBinaryDocumentDetectionMinLength": 512,
  "mergedTextIndexPathToExclude": [
    "_timestampMillisNegative",
    "__mergedTextIndex",
    "_timestampMillis"
  ],
  "fieldsToDoubleIngest": [],
  "jsonKeyValueSeparator": "\u001e",
  "mergedTextIndexBeginOfDocAnchor": "\u0002",
  "mergedTextIndexEndOfDocAnchor": "\u0003",
  "fieldPathsToPreserveInput": [],
  "fieldPathsToPreserveInputWithIndex": []
}
```

Available configuration options are listed in [SchemaConformingTransformerConfig](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/config/table/ingestion/SchemaConformingTransformerConfig.java).

### Configuration of reserved fields

Other index config of 3 reserved columns could be set like:

```json
"fieldConfigList": [
  {
    "name": "json_data",
    "encodingType": "RAW",
    "indexTypes": [],
    "compressionCodec": "LZ4",
    "indexes": null,
    "properties": {
      "rawIndexWriterVersion": "4"
    },
    "tierOverwrites": null
  },
  {
    "name": "json_data_no_idx",
    "encodingType": "RAW",
    "indexTypes": [],
    "compressionCodec": "ZSTANDARD",
    "indexes": null,
    "properties": {
      "rawIndexWriterVersion": "4"
    },
    "tierOverwrites": null
  },
  {
    "name": "__mergedTextIndex",
    "encodingType": "RAW",
    "indexType": "TEXT",
    "indexTypes": [
      "TEXT"
    ],
    "compressionCodec": "LZ4",
    "indexes": null,
    "properties": {
      "enableQueryCacheForTextIndex": "false",
      "luceneAnalyzerClass": <analyzerClass>,
      "luceneAnalyzerClassArgTypes": <>,
      "luceneAnalyzerClassArgs": <>,
      "luceneMaxBufferSizeMB": "50",
      "luceneQueryParserClass": <parserClass>,
      "luceneUseCompoundFile": "true",
      "noRawDataForTextIndex": "true",
      "rawIndexWriterVersion": "4"
    },
    "tierOverwrites": null
  }
]

"jsonIndexConfigs": {
  "json_data": {
    "disabled": false,
    "maxLevels": 3,
    "excludeArray": true,
    "disableCrossArrayUnnest": true,
    "maxValueLength": 1000,
    "skipInvalidJson": true
  }
}
```
Specifically, customizable json index could be set according to [json index indexPaths](../indexing/json-index.md/#enable-and-configure-a-json-index).

## Power the text search

### Schema Design

With the help of `SchemaConformingTransformer`, all data could be kept even without specifying special dedicated columns in table schema. However, to optimize the storage and various query patterns, dedicated columns should be created based on the usage:
* Fields with frequent exact match query, e.g. region, log_level, runtime_env
* Fields with range query, e.g. timestamp
* High frequency fields from messages
  * Reduce json index size
  * Optimize group by queries

### Text Search

After putting each key/value pairs into the `__mergedTextIndex` field, there will neeed to be `luceneAnalyzerClass` to tokenize the document and `luceneQueryParserClass` to query by tokens.
Some example common searching patterns and their queries are:
* Exact key/value match
  TEXT_MATCH(__mergedTextIndex, '\"valuer:key\"')
* Wildcard value search in a key
  TEXT_MATCH(__mergedTextIndex, '/.* value .*:key/')
* Key exists check
  TEXT_MATCH(__mergedTextIndex, '/.*:key/')
* Global value exact match
  TEXT_MATCH(__mergedTextIndex, '/\"value\"/')
* Global value wildcard match
  TEXT_MATCH(__mergedTextIndex, '/.* value .*/')

The `luceneAnalyzerClass` and `luceneQueryParserClass` usually need to have similar delimiter set. It also needs to consider the values below.
```
"jsonKeyValueSeparator": "\u001e",
"mergedTextIndexBeginOfDocAnchor": "\u0002",
"mergedTextIndexEndOfDocAnchor": "\u0003",
```
With given example, each key/value pair would be stored as "\u0002value\u001ekey\u0003". The prefix and suffix match on key or value need to be adjusted accordingly in the `luceneQueryParserClass`.
