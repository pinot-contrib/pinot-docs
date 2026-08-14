---
description: The tables below shows the properties available to set at the table level.
---

# Table

## Top-level fields

| Property             | Description                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tableName            | Specifies the name of the table. Should only contain alpha-numeric characters, hyphens (‘-‘), or underscores (‘\__’). (Two notes: While the hyphen is allowed in table names, it is also a reserved character in SQL, so if you use it you must remember to double quote the table name in your queries. Using a double-underscore (‘\_\__’) is not allowed as it is reserved for other features within Pinot.) |
| tableType            | Defines the table type: `OFFLINE` for offline tables or `REALTIME` for real-time tables. A hybrid table is essentially two table configurations: one of each type, with the same table name.                                                                                                                                                                                                                    |
| isDimTable           | Boolean field to indicate whether the table is a [dimension table](../../build-with-pinot/ingestion/batch-ingestion/dim-table.md).                                                                                                                                                                                                                                                                                    |
| description          | Optional human-readable description of the table. Pinot supports Markdown in this field.                                                                                                                                                                                                                                                                                                                           |
| tags                 | Optional list of tags for categorizing and filtering the table.                                                                                                                                                                                                                                                                                                                                                      |
| quota                | Defines properties related to quotas, such as storage quota and query quota. For details, see the [Quota](table.md#quota) table below.                                                                                                                                                                                                                                                                          |
| task                 | Defines the enabled minion tasks for the table. See [Minion](../../basics/components/cluster/minion.md) for more details.                                                                                                                                                                                                                                                                                          |
| routing              | Defines the properties that determine how the broker selects the servers to route, and how segments can be pruned by the broker based on segment metadata. For details, see the [Routing](table.md#routing) table below.                                                                                                                                                                                        |
| query                | Defines the properties related to query execution. For details, see the [Query](table.md#query) table below.                                                                                                                                                                                                                                                                                                    |
| tableSamplers        | Defines named table samplers that can be selected per query with the [`sampler`](../../build-with-pinot/querying-and-sql/query-execution-controls/query-options.md#supported-query-options) query option. See [Table samplers](table.md#table-samplers) below.                                                                                                                                                  |
| segmentsConfig       | Defines the properties related to the segments of the table, such as segment push frequency, type, retention, schema, time column etc. For details, see the [segmentsConfig](table.md#segments-config) table below.                                                                                                                                                                                             |
| tableIndexConfig     | Defines the indexing related information for the Pinot table. For details, see [Table indexing config](table.md#table-index-config) below.                                                                                                                                                                                                                                                                      |
| fieldConfigList      | Specifies the columns and the type of indices to be created on those columns. See [Field config list](table.md#field-config-list) for sub-properties.                                                                                                                                                                                                                                                           |
| tenants              | Defines the server and broker tenant used for this table. For details, see [Tenant](../../basics/components/cluster/tenant.md) below.                                                                                                                                                                                                                                                                              |
| ingestionConfig      | Defines the properties related to ingesting data. See the [ingestionConfig](ingestion.md#ingestionconfig) section for details.                                                                                                                                                                                                                                                                                  |
| upsertConfig         | Set upset configurations. For details, see [Stream ingestion with upsert](../../build-with-pinot/ingestion/upsert-and-dedup/upsert.md).                                                                                                                                                                                                                                                                               |
| dedupConfig          | Set deduplication configurations. For details, see [Stream ingestion with Dedup](../../build-with-pinot/ingestion/upsert-and-dedup/dedup.md).                                                                                                                                                                                                                                                                         |
| dimensionTableConfig | Set `disablePreload` to `true` to save memory if the table is a [dimension table](../../build-with-pinot/ingestion/batch-ingestion/dim-table.md).                                                                                                                                                                                                                                                                     |
| tierConfigs          | Defines configurations for tiered storage. For details, see [Tiered Storage](../../operate-pinot/separating-data-storage-by-age/moving-segments-across-tenants.md).                                                                                                                                                                                                                                    |
| metadata             | Contains other metadata of the table. There is a string to string map field "_customConfigs"_ under it which is expressed as key-value pairs to hold the custom configurations.                                                                                                                                                                                                                                 |

## Second-level fields

The following properties can be nested inside the top-level configurations.

### Quota

| Property | Format | Description |
| --- | --- | --- |
| storage | case-insensitive human-readable Data Size Double + (K, M, G, T, P) Double + (KB, MB, GB, TB, PB) | The maximum storage space the table is allowed to use before replication. For example, in the above table, the storage is 140G and replication is 3, so the maximum storage the table is allowed to use is 140G x 3 = 420G. The space the table uses is calculated by adding up the sizes of all segments from every server hosting this table. Once this limit is reached, offline segment push throws a `403` exception with message, `Quota check failed for segment: segment_0 of table: pinotTable`. For real-time tables, Pinot also pauses consumption with reason code `STORAGE_QUOTA_EXCEEDED` when periodic validation sees the table over quota, and resumes segment creation once the table is back within quota. examples: `storage: 100MB` `storage: 140.0G` `storage: 1t` |
| maxQueriesPerSecond | Double | The maximum queries per second allowed to execute on this table. The value must be a positive, finite number; zero, negative values, `NaN`, and positive or negative infinity are rejected. Omit the property to leave the table query quota unlimited. If query volume exceeds the configured quota, a `429` exception with message `Request 123 exceeds query quota for table:pinotTable, query:select count(*) from pinotTable` will be sent, and a BrokerMetric `QUERY_QUOTA_EXCEEDED` will be recorded. The application should build an exponential backoff and retry mechanism to react to this exception. Examples: `maxQueriesPerSecond: 10.0` `maxQueriesPerSecond: 100` |
|  |  |  |
|  |  |  |

Find more details on query quotas [here](../../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md)

### Routing

Find details on configuring routing [here](../../operate-pinot/tuning/routing.md).

| Property             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| segmentPrunerTypes | The list of segment pruners to be enabled. The segment pruner prunes the selected segments based on the query. Supported values: - `partition`: Prunes segments based on the partition metadata stored in zookeeper. By default, there is no pruner. - `time`: Prune segments for queries filtering on `timeColumnName` that do not contain data in the query's time range. |
| instanceSelectorType | The server instances to serve the query based on selected segments. Supported values: - `balanced`: Balances the number of segments served by each selected instance. Default. - `replicaGroup`: Instance selector for replica group routing strategy. |

### Query

| Property                   | Description                                                                                                                                                                                                                                                                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| timeoutMs                  | Query timeout in milliseconds                                                                                                                                                                                                                                                                                                            |
| disableGroovy              | Whether to disable groovy in query. This overrides the broker instance level config (`pinot.broker.disable.query.groovy`) if configured.                                                                                                                                                                                                 |
| useApproximateFunction     | Whether to automatically use approximate function for expensive aggregates, such as `DISTINCT_COUNT OR DISTINCT_COUNT_MV` will be converted to `DISTINCT_COUNT_SMARTHLL` and `PERCENTILE` to `PERCENTILE_SMART_TDIGEST` .This overrides the broker instance level config (`pinot.broker.use.approximate.function`) if configured.        |
| expressionOverrideMap      | A map that configures the expressions to override in the query. This can be useful when users cannot control the queries sent to Pinot (e.g. queries auto-generated by some other tools), but want to override the expressions within the query (e.g. override a transform function to a derived column). Example: `{"myFunc(a)": "b"}`. |
| maxQueryResponseSizeBytes  | Long value config indicating the maximum serialized response size across all servers for a query. This value is // equally divided across all servers processing the query.                                                                                                                                                              |
| maxServerResponseSizeBytes | Long value config indicating the maximum length of the serialized response per server for a query.                                                                                                                                                                                                                                       |
| maxEntriesScannedInFilter  | Optional per-table override for the maximum cumulative `numEntriesScannedInFilter` server-side scan cost. When set, this overrides the cluster scan-based killing threshold for this table.                                                                                                                                               |
| maxDocsScanned             | Optional per-table override for the maximum cumulative `numDocsScanned` server-side scan cost. When set, this overrides the cluster scan-based killing threshold for this table.                                                                                                                                                        |
| maxEntriesScannedPostFilter | Optional per-table override for the maximum cumulative `numEntriesScannedPostFilter` server-side scan cost. When set, this overrides the cluster scan-based killing threshold for this table.                                                                                                                                           |
| scanKillingMode            | Optional per-table override for server-side scan-based killing mode. Valid values are `disabled`, `logOnly`, and `enforce` (case-insensitive). If unset, Pinot uses the cluster-level mode. Invalid values are rejected when the table config is submitted.                                                                            |

### Table samplers

| Property | Description |
| --- | --- |
| name | Sampler name used from the query option, for example `SET sampler='small'`. Names must be unique within the table config. |
| type | Sampler implementation to use. This can be a built-in sampler type, a fully qualified class name, or an alias registered through broker annotation scanning. |
| properties | Sampler-specific string map. Supported keys depend on the sampler type. |

Example:

```json
"tableSamplers": [
  {
    "name": "small",
    "type": "firstN",
    "properties": {
      "numSegments": "1"
    }
  }
]
```

The built-in `firstN` sampler sorts segment names lexicographically and keeps the first `numSegments` entries. `numSegments` must be a positive integer.

### Segments config

| Property           | Description                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| schemaName | **Deprecated**: schema name should always match the table name (without the type suffix, e.g. `myTable`), and this field should not be configured. Name of the schema associated with the table |
| timeColumnName     | The name of the time column for this table. This must match with the time column name in the schema. This is mandatory for tables with push type `APPEND`, optional for `REFRESH.` timeColumnName along with timeColumnType is used to manage segment retention and time boundary for offline vs real-time.                                                                                                             |
| replication        | Number of replicas for the tables. A replication value of 1 means segments won't be replicated across servers.                                                                                                                                                                                                                                                                                                          |
| retentionTimeUnit | Unit for the retention, such as `HOURS` or `DAYS`. This, in combination with retentionTimeValue decides the duration for which to retain the segments. For example, `365 DAYS` means that segments containing data older than 365 days will be deleted periodically by the `RetentionManager` Controller periodic task. By default, there is no set retention. |
| retentionTimeValue | A numeric value for the retention. This, in combination with `retentionTimeUnit`, determines the duration for which to retain the segments                                                                                                                                                                                                                                                                              |

### Table index config

This section is used to specify some general index configuration and multi-column indexes like [Star-tree](../../build-with-pinot/indexing/star-tree-index.md#index-generation-configuration).

{% hint style="info" %}
Before Pinot version 0.13, the configuration described above was also used to configure certain single-column indexes. While this approach is still supported, it is highly recommended to specify these indexes in the \[Field Config List]\(#Field Config List) section instead. The documentation page for each index type provides guidance on how to utilize this section to create that specific index type. This updated method offers more flexibility and aligns with best practices for configuring single-column indexes in Pinot.
{% endhint %}

| Property                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| createInvertedIndexDuringSegmentGeneration | **DEPRECATED (Apache Pinot PR #17951):** This flag is no longer honored. Inverted indexes are always created during segment generation. Previously, this Boolean indicated whether to create inverted indexes when segments are created (by default, false). This setting is ignored and will be removed in a future version.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| sortedColumn                               | The column which is sorted in the data and hence will have a sorted index. This does not need to be specified for the offline table, as the segment generation job will automatically detect the sorted column in the data and create a sorted index for it.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| multiColumnTextIndexConfig                 | The multi-column / per-segment text index configuration. For details on how to configure this, see [Text search support](../../build-with-pinot/indexing/text-search-support.md#enable-a-per-segment-text-index) .                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| starTreeIndexConfigs                       | The list of StarTree indexing configs for creating StarTree indexes. For details on how to configure this, see [StarTree Index](../../build-with-pinot/indexing/star-tree-index.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| enableDefaultStarTree                      | Boolean to indicate whether to create a default StarTree index for the segment. For details, see[ ](../../build-with-pinot/indexing/star-tree-index.md)[Star-Tree index](../../build-with-pinot/indexing/star-tree-index.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| enableDynamicStarTreeCreation              | Boolean to indicate whether to allow creating StarTree when server loads the segment. StarTree creation could potentially consume a lot of system resources, so this config should be enabled when the servers have the free system resources to create the StarTree.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| segmentPartitionConfig | Configure per-column partition functions for broker-side partition pruning. Use `segmentPartitionConfig.columnPartitionMap` together with [`routing.segmentPrunerTypes`](table.md#routing). See [Segment partition config](#segment-partition-config). |
| tierOverwrites | Optional JSON object keyed by tier name. Pinot merges the matching object onto `tableIndexConfig` when loading that tier. For realtime tables, `tierOverwrites.consuming` is special: it only changes the mutable consuming-segment view, while completed segments still use the base table config. If `tierConfigs` declares a real storage tier named `consuming`, Pinot treats that as ordinary tiered storage instead of the mutable consuming-segment override. |
| loadMode | Indicates how the segments will be loaded onto the server: `heap` - load data directly into direct memory `mmap` - load data segments to off-heap memory |
| columnMinMaxValueGeneratorMode | Generate min max values for columns. Supported values: `NONE` - do not generate for any columns `ALL` - generate for all columns `TIME` - generate for only time column `NON_METRIC` - generate for time and dimension columns |
| nullHandlingEnabled                        | (deprecated, use `enableColumnBasedNullHandling` in [schema](schema.md)) For more information, see the [null handling section](../../build-with-pinot/querying-and-sql/null-value-support.md).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| skipSegmentPreprocess                      | Boolean to skip the segment preprocessing step during server startup and segment reload. When set to `true`, the server will not check or update default columns, single-column indexes (inverted, JSON, etc.), star-tree indexes, multi-column text indexes, or column min/max values when loading segments. This can significantly reduce server startup time and segment reload time for tables with a large number of segments where the table configuration and schema are stable. Default: `false`. **Use with caution**: enabling this means any new indexes or schema changes that require segment preprocessing will not be applied until this flag is set back to `false` and segments are reloaded. Only recommended for production tables with stable schemas and index configurations where faster restarts are more important than automatic index updates. |
| aggregateMetrics                           | (deprecated, use [Ingestion Aggregation](../../build-with-pinot/ingestion/ingestion-level-aggregations.md)) (only applicable for stream) set to `true` to pre-aggregate the metrics                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| optimizeDictionary                         | Set to `true` if you want to disable dictionaries for single valued metric columns. Only applicable to single-valued columns. Applies other modifications to dictionary indexes. Read [their documentation page](../../build-with-pinot/indexing/dictionary-index.md) to get more info. Defaults to `false`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| optimizeDictionaryForMetrics               | Set to `true` if you want to disable dictionaries for single valued metric columns. Only applicable to single-valued metric columns. Defaults to `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| optimizeDictionaryType                     | When `true`, Pinot automatically chooses fixed-width dictionaries for `STRING`, `BYTES`, and `BIG_DECIMAL` columns when all values in a segment have the same length, and falls back to variable-width dictionaries otherwise. This does not disable dictionaries; it only changes how Pinot stores dictionary values for those variable-width column types. Defaults to `false`. |
| noDictionarySizeRatioThreshold | If `optimizeDictionaryForMetrics` enabled, dictionary is not created for the metric columns for which `noDictionaryIndexSize/ indexWithDictionarySize` is less than the `noDictionarySizeRatioThreshold` `Default: 0.85` |
| noDictionaryCardinalityRatioThreshold   | If `optimizeDictionary` is enabled, columns whose `cardinality / totalDocs` ratio is below this threshold will still have a dictionary created (because low-cardinality columns benefit from dictionary encoding). A value around `0.1` (10%) is a reasonable starting point. Default: not set (disabled).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| columnMajorSegmentBuilderEnabled       | Boolean to enable column-major segment building, which can improve segment generation performance. Default: `true`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| segmentNameGeneratorType | Type of segmentNameGenerator, default is `SimpleSegmentNameGenerator.` See more on [#segment-name-generator-spec](job-specification.md#segment-name-generator-spec) |

#### Segment partition config

Use `tableIndexConfig.segmentPartitionConfig.columnPartitionMap` together with `routing.segmentPrunerTypes: ["partition"]` when you want Pinot brokers to prune segments based on a partitioned column.

{% hint style="warning" %}
For an upsert- or dedup-enabled table, Pinot rejects table configuration updates that add, remove, or modify `segmentPartitionConfig`. Changing the partition configuration can send records with the same primary key to different partitions or servers, which can produce duplicates or incorrect query results. Plan the partition function and partition count before creating the table.

The table update API can bypass this backward-compatibility check with `force=true`, but doing so does not preserve the upsert or dedup routing invariant. Use a new table and migrate the data when the partition configuration must change.
{% endhint %}

Each entry under `columnPartitionMap` configures one column:

| Property | Description |
| --- | --- |
| `functionName` | Partition function name. Matching is case-insensitive. Built-ins are `Modulo`, `Murmur`, `Murmur3`, `FNV`, `HashCode`, `ByteArray`, and `BoundedColumnValue`. `Murmur2` is an alias for `Murmur`. |
| `numPartitions` | Total number of partitions for the column. |
| `functionConfig` | Optional string map with function-specific settings. |

Built-in partition functions use the following defaults:

| Function | Aliases | Default `partitionIdNormalizer` | Function-specific config |
| --- | --- | --- | --- |
| `Modulo` | none | `POSITIVE_MODULO` | none |
| `Murmur` | `Murmur2` | `MASK` | `useRawBytes` |
| `Murmur3` | none | `MASK` | `seed`, `variant` (`x86_32`, `x64_32`), `useRawBytes` |
| `FNV` | none | `MASK` | `variant` (`fnv1_32`, `fnv1a_32`, `fnv1_64`, `fnv1a_64`), `useRawBytes` |
| `HashCode` | none | `PRE_MODULO_ABS` | none |
| `ByteArray` | none | `PRE_MODULO_ABS` | none |
| `BoundedColumnValue` | none | `NO_OP` | `columnValues`, `columnValuesDelimiter` |

`partitionIdNormalizer` is the shared config key for every built-in function except `BoundedColumnValue`. Supported values are `POSITIVE_MODULO`, `ABS`, `MASK`, `PRE_MODULO_ABS`, and `NO_OP`. Use this when Pinot needs to match the partition-id math used by your producer or upstream partitioner. `NO_OP` is only appropriate when the function already returns values in `[0, numPartitions)`.

`BoundedColumnValue` maps configured values to fixed partition ids and sends all unmatched values to partition `0`. Set `numPartitions` to the number of configured values plus one.

Example:

```json
{
  "tableIndexConfig": {
    "segmentPartitionConfig": {
      "columnPartitionMap": {
        "memberId": {
          "functionName": "FNV",
          "numPartitions": 16,
          "functionConfig": {
            "variant": "fnv1a_32",
            "partitionIdNormalizer": "ABS"
          }
        },
        "subject": {
          "functionName": "BoundedColumnValue",
          "numPartitions": 4,
          "functionConfig": {
            "columnValues": "Maths|English|Chemistry",
            "columnValuesDelimiter": "|"
          }
        }
      }
    }
  }
}
```

{% hint style="info" %}
Pinot no longer uses a closed `PartitionFunctionFactory` enum. Custom partition functions are discovered at startup when they are public, concrete `PartitionFunction` implementations under `org.apache.pinot.*` with a public `(int numPartitions, Map<String, String> functionConfig)` constructor. Override `getNames()` only when you need aliases beyond the default `[getName()]`.
{% endhint %}

### Field Config List

Specify the columns and the type of indices to be created on those columns.

| Property        |                                                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| name            | Name of the column                                                                                                                                 |
| encodingType    | Should be one of `RAW` or `DICTIONARY`                                                                                                             |
| indexes         | An object whose keys identify indexes. Values are interpreted as the configuration for each index. See each index section to learn more about them |
| tierOverwrites  | Optional JSON object keyed by tier name. Pinot merges the matching object onto the field config for that tier. For realtime tables, `tierOverwrites.consuming` can change encoding or field-level indexes only while the segment is mutable and consuming. |
| timestampConfig | An object that defines the granularities used in [timestamp](../../build-with-pinot/indexing/timestamp-index.md) indexes                                        |
| properties      | JSON of key-value pairs containing additional properties associated with the index.                                                                |

When `encodingType` is `RAW`, the forward index stores raw values. The column can still have a dictionary if another field-level index requires dictionary IDs or dictionary values. For config updates, make that dictionary explicit in `indexes.dictionary` and keep the column out of legacy `tableIndexConfig.noDictionaryColumns` and `tableIndexConfig.noDictionaryConfig`; those legacy settings still disable the dictionary and can cause validation to reject dictionary-backed secondary indexes such as inverted, FST, or IFST.

Example RAW forward index with a standalone dictionary:

```json
{
  "fieldConfigList": [
    {
      "name": "myColumn",
      "encodingType": "RAW",
      "indexes": {
        "dictionary": {},
        "inverted": {}
      }
    }
  ]
}
```

#### OPEN_STRUCT index

Use the `open_struct` field-level index on a single-value `OPEN_STRUCT` column when you want Pinot to keep a semi-structured object in one column but materialize frequently used keys as standard Pinot columns.

Pinot stores `OPEN_STRUCT` data in two tiers:

* Dense keys become materialized child columns named `<column>$<key>`.
* Remaining keys are written into one sparse JSON column named `<column>$__sparse__`.

The `open_struct` config object supports the following properties:

| Property | Description |
| --- | --- |
| `denseKeys` | Optional explicit set of keys that Pinot always materializes as dense child columns, regardless of fill rate. |
| `denseKeyMinFillRate` | Minimum fraction of documents that must contain a key before Pinot materializes it automatically. Default: `0.5`. |
| `maxDenseKeys` | Maximum number of dense keys to materialize. `-1` means unlimited, `0` disables dense keys entirely, and positive values keep only the highest-fill-rate qualifying keys as dense. |
| `sparseJsonIndex` | Whether to build a JSON index over the shared sparse column. Default: `false`. When enabled, compatible string-key equality and `IN` filters can use the JSON index; other sparse-key operations use the virtual scan path. |
| `defaultValueFieldConfig` | Optional fallback `FieldConfig` applied to dense keys that do not appear in `valueFieldConfigs`. |
| `valueFieldConfigs` | Optional list of per-key `FieldConfig` entries. Each entry's `name` must match an `OPEN_STRUCT` key name. |

Per-key `FieldConfig.indexes` inside `defaultValueFieldConfig` or `valueFieldConfigs` may use only the vetted subset: `dictionary`, `forward`, `inverted`, `range`, and `bloom`. Forward indexes are always written for materialized child columns. When neither `defaultValueFieldConfig` nor `valueFieldConfigs` configures a dense key, Pinot uses dictionary encoding plus an inverted index for that key by default.

Example:

```json
{
  "fieldConfigList": [
    {
      "name": "attributes",
      "indexes": {
        "open_struct": {
          "denseKeys": ["customerId", "country"],
          "denseKeyMinFillRate": 0.5,
          "maxDenseKeys": 32,
          "sparseJsonIndex": true,
          "valueFieldConfigs": [
            {
              "name": "customerId",
              "indexes": {
                "inverted": {}
              }
            },
            {
              "name": "country",
              "indexes": {
                "bloom": {}
              }
            }
          ]
        }
      }
    }
  ]
}
```

For realtime tables, you can also give mutable consuming segments a different index layout without changing the
persisted segment format. Pinot applies the `consuming` override first, validates the effective config through the
normal table-config path, and then uses that effective view only while the segment is still consuming:

```json
{
  "tableIndexConfig": {
    "noDictionaryColumns": ["profiledString"],
    "tierOverwrites": {
      "consuming": {
        "noDictionaryColumns": []
      }
    }
  },
  "fieldConfigList": [
    {
      "name": "profiledString",
      "encodingType": "RAW",
      "tierOverwrites": {
        "consuming": {
          "encodingType": "DICTIONARY",
          "indexes": {
            "inverted": {
              "disabled": false
            }
          }
        }
      }
    }
  ]
}
```

Use this pattern when you want mutable consuming segments to expose extra indexes, such as a dictionary-backed
inverted index, while completed realtime segments keep the base layout. Keep row-shape settings in the base config, and
do not define a real `tierConfigs` entry named `consuming` unless you intend normal storage-tier behavior instead of
the mutable consuming-segment override.

#### Deprecated configuration options

There are several deprecated configuration options in Pinot that are still supported but recommended for migration to newer ways of configuration. Here's a summary of these options:

**`indexTypes`**

* Description: An older way to define indexes enabled for a column.
* Supported Index Types: [Text](../../build-with-pinot/indexing/text-search-support.md), [FST](../../build-with-pinot/indexing/native-text-index.md), [Timestamp](../../build-with-pinot/indexing/timestamp-index.md), [H3 (also known as geospatial)](../../build-with-pinot/indexing/geospatial-support.md).
* Note: Some index types required additional `properties` for configuration.

**`indexType`**

* Description: Similar to `indexTypes`, but only supports a single index type as a string.
* Note: If both `indexTypes` and `indexType` are present, the latter is ignored.

**`compressionCodec`**

* Description: An older way to specify compression for indexes.
* Recommendation: It's now recommended to specify compression in the [forward index config](../../build-with-pinot/indexing/forward-index.md).

**Deprecated `properties`**

* Description: Before Pinot 0.13, certain indexes were configured using properties within this section.
* Migration: Since Pinot 0.13, each index can be configured in a type-safe manner within its dedicated section in the `indexes` object. The documentation for each index type lists the properties that were previously used.
* Notable Properties:
  * Text Index Properties: `enableQueryCacheForTextIndex` (used to enable/disable the cache, with values specified as strings, e.g., "true" or "false").
  * Forward Index Properties: `rawIndexWriterVersion`, `deriveNumDocsPerChunkForRawIndex`, `forwardIndexDisabled`.

It's strongly recommended to migrate from these deprecated options to the new, more structured configuration methods introduced in Pinot 0.13 for better maintainability and compatibility.

{% hint style="danger" %}
**Warning:**

If removing the `forwardIndexDisabled` property above to regenerate the forward index for multi-value (MV) columns note that the following invariants cannot be maintained after regenerating the forward index for a forward index disabled column:

* Ordering guarantees of the MV values within a row
* If entries within an MV row are duplicated, the duplicates will be lost. Regenerate the segments via your offline jobs and re-push / refresh the data to get back the original MV data with duplicates.

We will work on removing the second invariant in the future.
{% endhint %}

## Real-time table config

The sections below apply to real-time tables only.

### segmentsConfig

| Property                                           | Description                                                                                                 |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| replicasPerPartition (Deprecated, use replication) | The number of replicas per partition for the stream                                                         |
| completionMode                                     | determines if segment should be downloaded from other server or built in memory. can be `DOWNLOAD` or empty |
| peerSegmentDownloadScheme                          | protocol to use to download segments from server. can be on of `http` or `https`                            |

### Indexing config

The `streamConfigs` section has been deprecated as of release 0.7.0. See [`streamConfigMaps`](../../build-with-pinot/ingestion/stream-ingestion/README.md#create-table-configuration-with-ingestion-configuration) instead.

## Tenants

| Property          | Description                                                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| broker            | Broker tenant in which the segment should reside                                                                                                  |
| server            | Server tenant in which the segment should reside                                                                                                  |
| tagOverrideConfig | Override the tenant for segment if it fulfills certain conditions. Currently, only support override on `realtimeConsuming` or `realtimeCompleted` |

### Example

```javascript
  "broker": "brokerTenantName",
  "server": "serverTenantName",
  "tagOverrideConfig" : {
    "realtimeConsuming" : "serverTenantName_REALTIME"
    "realtimeCompleted" : "serverTenantName_OFFLINE"
  }
}
```

## Environment variables override

Pinot allows users to define environment variables in the format of `${ENV_NAME}` or `${ENV_NAME:DEFAULT_VALUE}`as field values in table config.

Pinot instance will override it during runtime.

When you create or update a table, the controller now validates these placeholders against its own runtime environment before persisting the table config. If a placeholder without a default value cannot be resolved there, Pinot rejects the write instead of saving a config that would later fail on read paths such as realtime segment commit.

{% hint style="warning" %}
Brackets are required when defining the environment variable.`"$ENV_NAME"`is not supported.
{% endhint %}

{% hint style="warning" %}
Environment variables used without default value in table config have to be available to all Pinot components - **Controller**, **Broker**, **Server**, and **Minion**. Otherwise, querying/consumption will be affected depending on the service to which these variables are not available.
{% endhint %}

Below is an example of setting AWS credential as part of table config using environment variable.

**Example:**

```javascript
{
...
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "DAILY",
      "batchConfigMaps": [
        {
          "inputDirURI": "s3://<my-bucket>/baseballStats/rawdata",
          "includeFileNamePattern": "glob:**/*.csv",
          "excludeFileNamePattern": "glob:**/*.tmp",
          "inputFormat": "csv",
          "outputDirURI": "s3://<my-bucket>/baseballStats/segments",
          "input.fs.className": "org.apache.pinot.plugin.filesystem.S3PinotFS",
          "input.fs.prop.region": "us-west-2",
          "input.fs.prop.accessKey": "${AWS_ACCESS_KEY}",
          "input.fs.prop.secretKey": "${AWS_SECRET_KEY}",
          "push.mode": "tar"
        }
      ],
      "segmentNameSpec": {},
      "pushSpec": {}
    }
  },
...
}
```

## Sample configurations

### Offline table

{% code title="pinot-table-offline.json" %}
```json
{% hint style="warning" %}
The examples below use some legacy configuration patterns for familiarity. In new table configs, prefer using `fieldConfigList` with the `indexes` object for single-column indexes instead of `invertedIndexColumns`, `rangeIndexColumns`, `bloomFilterColumns`, etc. in `tableIndexConfig`. The `timeType` field in `segmentsConfig` is also deprecated — define the time format in the schema's `dateTimeFieldSpec` instead.
{% endhint %}

"OFFLINE": {
  "tableName": "pinotTable",
  "tableType": "OFFLINE",
  "quota": {
    "maxQueriesPerSecond": 300,
    "storage": "140G"
  },
  "routing": {
    "segmentPrunerTypes": ["partition"],
    "instanceSelectorType": "replicaGroup"
  },
  "segmentsConfig": {
    "timeColumnName": "daysSinceEpoch",
    "timeType": "DAYS",
    "replication": "3",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "365"
  },
  "tableIndexConfig": {
    "invertedIndexColumns": ["foo", "bar", "moo"],
    "createInvertedIndexDuringSegmentGeneration": false,
    "sortedColumn": ["pk"],
    "bloomFilterColumns": [],
    "starTreeIndexConfigs": [],
    "noDictionaryColumns": [],
    "rangeIndexColumns": [],
    "onHeapDictionaryColumns": [],
    "varLengthDictionaryColumns": [],
    "segmentPartitionConfig": {
      "columnPartitionMap": {
        "column_foo": {
          "functionName": "Murmur",
          "numPartitions": 32
        }
      }
    },
    "loadMode": "MMAP",
    "columnMinMaxValueGeneratorMode": null,
    "nullHandlingEnabled": false
  },
  "ingestionConfig": {
    "batchIngestionConfig": {
      "segmentIngestionType": "APPEND",
      "segmentIngestionFrequency": "DAILY"
    },
    "filterConfig": {
      "filterFunction": "Groovy({foo == \"VALUE1\"}, foo)"
    },
    "transformConfigs": [
    {
      "columnName": "bar",
      "transformFunction": "lower(moo)"
    },
    {
      "columnName": "hoursSinceEpoch",
      "transformFunction": "toEpochHours(millis)"
    }]
  },
  "tenants": {
    "broker": "myBrokerTenant",
    "server": "myServerTenant"
  },
  "metadata": {
    "customConfigs": {
      "key": "value",
      "key": "value"
    }
  }
}
```
{% endcode %}

### Real-time table

Here's an example table config for a real-time table. **All the fields from the offline table config are valid for the real-time table**. Additionally, real-time tables use **some extra fields**.

{% hint style="info" %}
Flush keys such as `realtime.segment.flush.threshold.rows`, `realtime.segment.flush.threshold.time`, and `realtime.segment.flush.threshold.segment.size` live under `ingestionConfig.streamIngestionConfig.streamConfigMaps`. The first threshold that is met flushes the consuming segment; desired size is used when table-level rows is **not positive** (explicit `0` or unset) and size-based autotune is selected. Full precedence and tuning guidance: [Realtime segment flush threshold precedence](../../operate-pinot/tuning/realtime.md#realtime-segment-flush-threshold-precedence) and [Ingestion stream configs](ingestion.md#streamconfigmaps).
{% endhint %}

{% code title="pinot-table-realtime.json" %}
```json
"REALTIME": {
  "tableName": "pinotTable",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "daysSinceEpoch",
    "timeType": "DAYS",
    "replication": "3",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "5",
    "completionConfig": {
      "completionMode": "DOWNLOAD"
    }
  },
  "tableIndexConfig": {
    "invertedIndexColumns": ["foo", "bar", "moo"],
    "sortedColumn": ["column1"],
    "noDictionaryColumns": ["metric1", "metric2"],
    "loadMode": "MMAP",
    "nullHandlingEnabled": false
  },
  "ingestionConfig:" {
    "streamIngestionConfig": {
      "streamConfigMaps": [
      {
        "realtime.segment.flush.threshold.rows": "0",
        "realtime.segment.flush.threshold.time": "24h",
        "realtime.segment.flush.threshold.segment.size": "150M",
        "stream.kafka.broker.list": "XXXX",
        "stream.kafka.consumer.factory.class.name": "XXXX",
        "stream.kafka.consumer.prop.auto.offset.reset": "largest",
        "stream.kafka.decoder.class.name": "XXXX",
        "stream.kafka.decoder.prop.schema.registry.rest.url": "XXXX",
        "stream.kafka.decoder.prop.schema.registry.schema.name": "XXXX",
        "stream.kafka.topic.name": "XXXX",
        "streamType": "kafka"
      }]
    }
  },
  "tenants":{
    "broker": "myBrokerTenant",
    "server": "myServerTenant",
    "tagOverrideConfig": {}
  },
  "metadata": {}
}
```
{% endcode %}
