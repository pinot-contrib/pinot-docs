---
description: The tables below shows the properties available to set at the table level.
---

# Table

## Top-level fields

| Property             | Description                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tableName            | Specifies the name of the table. Should only contain alpha-numeric characters, hyphens (‘-‘), or underscores (‘\__’). (Two notes: While the hyphen is allowed in table names, it is also a reserved character in SQL, so if you use it you must remember to double quote the table name in your queries. Using a double-underscore (‘\_\__’) is not allowed as it is reserved for other features within Pinot.) |
| tableType            | Defines the table type: `OFFLINE` for offline tables or `REALTIME` for real-time tables. A hybrid table is essentially two table configurations: one of each type, with the same table name.                                                                                                                                                                                                                    |
| isDimTable           | Boolean field to indicate whether the table is a [dimension table](../basics/data-import/batch-ingestion/dim-table.md).                                                                                                                                                                                                                                                                                         |
| quota                | Defines properties related to quotas, such as storage quota and query quota. For details, see the [Quota](table.md#quota) table below.                                                                                                                                                                                                                                                                          |
| task                 | Defines the enabled minion tasks for the table. See [Minion](../basics/components/cluster/minion.md) for more details.                                                                                                                                                                                                                                                                                          |
| routing              | Defines the properties that determine how the broker selects the servers to route, and how segments can be pruned by the broker based on segment metadata. For details, see the [Routing](table.md#routing) table below.                                                                                                                                                                                        |
| query                | Defines the properties related to query execution. For details, see the [Query](table.md#query) table below.                                                                                                                                                                                                                                                                                                    |
| segmentsConfig       | Defines the properties related to the segments of the table, such as segment push frequency, type, retention, schema, time column etc. For details, see the [segmentsConfig](table.md#segments-config) table below.                                                                                                                                                                                             |
| tableIndexConfig     | Defines the indexing related information for the Pinot table. For details, see [Table indexing config](table.md#table-index-config) below.                                                                                                                                                                                                                                                                      |
| fieldConfigList      | Specifies the columns and the type of indices to be created on those columns. See [Field config list](table.md#field-config-list) for sub-properties.                                                                                                                                                                                                                                                           |
| tenants              | Defines the server and broker tenant used for this table. For details, see [Tenant](../basics/components/cluster/tenant.md) below.                                                                                                                                                                                                                                                                              |
| ingestionConfig      | Defines the configurations needed for ingestion level transformations. For details, see [Ingestion Level Transformations](../developers/advanced/ingestion-level-transformations.md) and [Ingestion Level Aggregations](../developers/advanced/ingestion-level-aggregations.md).                                                                                                                                |
| upsertConfig         | Set upset configurations. For details, see [Stream ingestion with upsert](../basics/data-import/upsert.md).                                                                                                                                                                                                                                                                                                     |
| dedupConfig          | Set deduplication configurations. For details, see [Stream ingestion with Dedup](../basics/data-import/dedup.md).                                                                                                                                                                                                                                                                                               |
| dimensionTableConfig | Set `disablePreload` to `true` to save memory if the table is a [dimension table](../basics/data-import/batch-ingestion/dim-table.md).                                                                                                                                                                                                                                                                          |
| tierConfigs          | Defines configurations for tiered storage. For details, see [Tiered Storage](../operators/operating-pinot/separating-data-storage-by-age/moving-segments-across-tenants.md).                                                                                                                                                                                                                                    |
| metadata             | Contains other metadata of the table. There is a string to string map field "_customConfigs"_ under it which is expressed as key-value pairs to hold the custom configurations.                                                                                                                                                                                                                                 |

## Second-level fields

The following properties can be nested inside the top-level configurations.

### Quota

| Property            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| storage             | <p>The maximum storage space the table is allowed to use before replication.</p><p>For example, in the above table, the storage is 140G and replication is 3, so the maximum storage the table is allowed to use is 140G x 3 = 420G. The space the table uses is calculated by adding up the sizes of all segments from every server hosting this table. Once this limit is reached, offline segment push throws a <code>403</code> exception with message, <code>Quota check failed for segment: segment_0 of table: pinotTable</code>.</p> |
| maxQueriesPerSecond | The maximum queries per second allowed to execute on this table. If query volume exceeds this, a `429` exception with message `Request 123 exceeds query quota for table:pinotTable, query:select count(*) from pinotTable` will be sent, and a BrokerMetric `QUERY_QUOTA_EXCEEDED` will be recorded. The application should build an exponential backoff and retry mechanism to react to this exception.                                                                                                                                    |

### Routing

Find details on configuring routing [here](https://docs.pinot.apache.org/operators/operating-pinot/tuning/routing).

| Property             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| segmentPrunerTypes   | <p>The list of segment pruners to be enabled.</p><p>The segment pruner prunes the selected segments based on the query.</p><p>Supported values:</p><ul><li><code>partition</code>: Prunes segments based on the partition metadata stored in zookeeper. By default, there is no pruner.</li><li><code>time</code>: Prune segments for queries filtering on <code>timeColumnName</code> that do not contain data in the query's time range.</li></ul> |
| instanceSelectorType | <p>The server instances to serve the query based on selected segments. Supported values:</p><ul><li><code>balanced</code>: Balances the number of segments served by each selected instance. Default.</li><li><code>replicaGroup</code>: Instance selector for replica group routing strategy.</li></ul>                                                                                                                                             |

### Query

| Property               | Description                                                                                                                                                                                                                                                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| timeoutMs              | Query timeout in milliseconds                                                                                                                                                                                                                                                                                                            |
| disableGroovy          | Whether to disable groovy in query. This overrides the broker instance level config (`pinot.broker.disable.query.groovy`) if configured.                                                                                                                                                                                                 |
| useApproximateFunction | Whether to automatically use approximate function for expensive aggregates, such as `DISTINCT_COUNT` and `PERCENTILE`. This overrides the broker instance level config (`pinot.broker.use.approximate.function`) if configured.                                                                                                          |
| expressionOverrideMap  | A map that configures the expressions to override in the query. This can be useful when users cannot control the queries sent to Pinot (e.g. queries auto-generated by some other tools), but want to override the expressions within the query (e.g. override a transform function to a derived column). Example: `{"myFunc(a)": "b"}`. |

### Segments config

| Property                                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| schemaName                                                                                                                                               | Name of the schema associated with the table                                                                                                                                                                                                                                                                                                                                                                            |
| timeColumnName                                                                                                                                           | The name of the time column for this table. This must match with the time column name in the schema. This is mandatory for tables with push type `APPEND`, optional for `REFRESH.` timeColumnName along with timeColumnType is used to manage segment retention and time boundary for offline vs real-time.                                                                                                             |
| replication                                                                                                                                              | Number of replicas for the tables. A replication value of 1 means segments won't be replicated across servers.                                                                                                                                                                                                                                                                                                          |
| retentionTimeUnit                                                                                                                                        | <p>Unit for the retention, such as <code>HOURS</code> or <code>DAYS</code>. This, in combination with retentionTimeValue decides the duration for which to retain the segments.</p><p>For example, <code>365 DAYS</code> means that segments containing data older than 365 days will be deleted periodically by the <code>RetentionManager</code> Controller periodic task. By default, there is no set retention.</p> |
| retentionTimeValue                                                                                                                                       | A numeric value for the retention. This, in combination with `retentionTimeUnit`, determines the duration for which to retain the segments                                                                                                                                                                                                                                                                              |
| <p>segmentPushType<br></p><p>(Deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -> BatchIngestionConfig -> segmentPushType )</p>           | <p>Can be either:</p><ul><li><code>APPEND</code>: New data segments pushed periodically, to append to the existing data eg. daily or hourly</li><li><code>REFRESH</code>: Entire data is replaced every time during a data push. Refresh tables have no retention.</li></ul>                                                                                                                                            |
| <p>segmentPushFrequency<br></p><p>(Deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -> BatchIngestionConfig -> segmentPushFrequency )</p> | <p>The cadence at which segments are pushed, such as <code>HOURLY</code> or <code>DAILY</code><br></p>                                                                                                                                                                                                                                                                                                                  |

### Table index config

This section is used to specify some general index configuration and multi-column indexes like [Star-tree](https://apache-pinot.gitbook.io/apache-pinot-cookbook/indexing#index-generation-configuration).

{% hint style="info" %}

Before Pinot version 0.13, the configuration described above was also used to configure certain single-column indexes.
While this approach is still supported, it is highly recommended to specify these indexes in the 
[Field Config List](#Field Config List) section instead. 
The documentation page for each index type provides guidance on how to utilize this section to create that specific 
index type. 
This updated method offers more flexibility and aligns with best practices for configuring single-column indexes in Pinot.

{% endhint %}


| Property                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------------------ |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| createInvertedIndexDuringSegmentGeneration | Boolean to indicate whether to create inverted indexes when segments are created. By default, false, which means indexes are created when the segments are loaded on the server. Learn more about this setting in [advanced Pinot setup](../developers/advanced/advanced-pinot-setup.md#add-an-inverted-index-to-your-table-automatically).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| sortedColumn                               | The column which is sorted in the data and hence will have a sorted index. This does not need to be specified for the offline table, as the segment generation job will automatically detect the sorted column in the data and create a sorted index for it.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| starTreeIndexConfigs                       | The list of StarTree indexing configs for creating StarTree indexes. For details on how to configure this, see [StarTree Index](https://docs.pinot.apache.org/basics/indexing/star-tree-index).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| enableDefaultStarTree                      | Boolean to indicate whether to create a default StarTree index for the segment. For details, see [StarTree Index](http://localhost:5000/s/bJukE0xQiyVCG6qOd7iZ/users/api/querying-pinot-using-standard-sql).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| enableDynamicStarTreeCreation              | Boolean to indicate whether to allow creating StarTree when server loads the segment. StarTree creation could potentially consume a lot of system resources, so this config should be enabled when the servers have the free system resources to create the StarTree.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| segmentPartitionConfig                     | <p>Use <code>segmentPartitionConfig.columnPartitionMap</code> along with <a href="table.md#routing"><code>routing.segementPrunerTypes</code></a> to enable partitioning. For each column, configure the following options:</p><ul><li><p><code>functionName</code>: Specify one of the supported functions:</p><ul><li><code>Murmur:</code>MurmurHash 2</li><li><code>Modulo</code>: Modulo on integer values</li><li><code>HashCode</code>: Java <code>hashCode()</code></li><li><code>ByteArray</code>: Java <code>hashCode()</code> on deserialized byte array</li></ul></li></ul><ul><li><code>numPartitions</code>: Number of partitions you want per segment. Controls how data is divided within each segment.</li></ul><p>Example:<br><code>{</code></p><p><code>"columnPartitionMap": {</code><br><code>"column_memberID": {</code><br><code>"functionName": "Murmur",</code><br><code>"numPartitions": 32</code><br><code>}</code><br><code>}</code></p> |
| loadMode                                   | <p>Indicates how the segments will be loaded onto the server:<br><code>heap</code> - load data directly into direct memory<br><code>mmap</code> - load data segments to off-heap memory</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| columnMinMaxValueGeneratorMode             | <p>Generate min max values for columns. Supported values:<br><code>NONE</code> - do not generate for any columns<br><code>ALL</code> - generate for all columns<br><code>TIME</code> - generate for only time column<br><code>NON_METRIC</code> - generate for time and dimension columns</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| nullHandlingEnabled                        | Boolean to indicate whether to keep track of null values as part of the segment generation. This is required when using `IS NULL` or `IS NOT NULL` predicates in the query. Enabling this will lead to additional memory and storage usage per segment. By default, this is set to _false_.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| aggregateMetrics                           | (deprecated, use [Ingestion Aggregation](https://github.com/pinot-contrib/pinot-docs/blob/master/developers/advanced/ingestion-level-aggregation.md)) (only applicable for stream) set to `true` to pre-aggregate the metrics                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| optimizeDictionary                         | Set to `true` if you want to disable dictionaries for single valued metric columns. Only applicable to single-valued columns. Applies other modifications to dictionary indexes. Read [their documentation page](../basics/indexing/dictionary-index.md) to get more info. Defaults to `false`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| optimizeDictionaryForMetrics               | Set to `true` if you want to disable dictionaries for single valued metric columns. Only applicable to single-valued metric columns. Defaults to `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| noDictionarySizeRatioThreshold             | <p>If <code>optimizeDictionaryForMetrics</code> enabled, dictionary is not created for the metric columns for which <code>noDictionaryIndexSize/ indexWithDictionarySize</code> is less than the <code>noDictionarySizeRatioThreshold</code><br><code>Default: 0.85</code></p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| segmentNameGeneratorType                   | <p>Type of segmentNameGenerator, default is <code>SimpleSegmentNameGenerator.</code></p><p>See more on <a data-mention href="job-specification.md#segment-name-generator-spec">#segment-name-generator-spec</a></p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

### Field Config List

Specify the columns and the type of indices to be created on those columns.

| Property          |                                                                                                                                                    |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name              | Name of the column                                                                                                                                 |
| encodingType      | Should be one of `RAW` or `DICTIONARY`                                                                                                             |
| indexes           | An object whose keys identify indexes. Values are interpreted as the configuration for each index. See each index section to learn more about them |
| timestampConfig   | An object that defines the granularities used in [timestamp](../basics/indexing/timestamp-index.md) indexes                                        |
| properties        | <p>JSON of key-value pairs containing additional properties associated with the index.                                                             |

#### Deprecated configuration options
There are several deprecated configuration options in Pinot that are still supported but recommended for migration to 
newer ways of configuration. 
Here's a summary of these options:

##### `indexTypes`
- Description: An older way to define indexes enabled for a column.
- Supported Index Types: [Text](../basics/indexing/text-search-support.md), [FST](../basics/indexing/native-text-index.md), [Timestamp](../basics/indexing/timestamp-index.md), [H3 (also known as geospatial)](../basics/indexing/geospatial-support.md).
- Note: Some index types required additional `properties` for configuration.

##### `indexType`
- Description: Similar to `indexTypes`, but only supports a single index type as a string.
- Note: If both `indexTypes` and `indexType` are present, the latter is ignored.

##### `compressionCodec`
- Description: An older way to specify compression for indexes.
- Recommendation: It's now recommended to specify compression in the [forward index config](../basics/indexing/forward-index.md).

##### Deprecated `properties`
- Description: Before Pinot 0.13, certain indexes were configured using properties within this section.
- Migration: Since Pinot 0.13, each index can be configured in a type-safe manner within its dedicated section in the `indexes` object. 
  The documentation for each index type lists the properties that were previously used.
- Notable Properties:
  - Text Index Properties: `enableQueryCacheForTextIndex` (used to enable/disable the cache, with values specified as 
  strings, e.g., "true" or "false").
  - Forward Index Properties: `rawIndexWriterVersion`, `deriveNumDocsPerChunkForRawIndex`, `forwardIndexDisabled`.

It's strongly recommended to migrate from these deprecated options to the new, more structured configuration methods 
introduced in Pinot 0.13 for better maintainability and compatibility.

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

| Property                  | Description                                                                                                 |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| replicasPerPartition      | The number of replicas per partition for the stream                                                         |
| completionMode            | determines if segment should be downloaded from other server or built in memory. can be `DOWNLOAD` or empty |
| peerSegmentDownloadScheme | protocol to use to download segments from server. can be on of `http` or `https`                            |

### Indexing config

The `streamConfigs` section has been deprecated as of release 0.7.0. See [`streamConfigMaps`](https://docs.pinot.apache.org/basics/data-import/pinot-stream-ingestion#create-ingestion-configuration) instead.

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
      "schemaName": "pinotTable",
      "timeColumnName": "daysSinceEpoch",
      "timeType": "DAYS",
      "allowNullTimeValue": false,
      "replication": "3",
      "retentionTimeUnit": "DAYS",
      "retentionTimeValue": "365",
      "segmentPushFrequency": "DAILY",
      "segmentPushType": "APPEND"
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
      "loadMode": "MMAP",
      "columnMinMaxValueGeneratorMode": null,
      "nullHandlingEnabled": false
    },
    "tenants": {
      "broker": "myBrokerTenant",
      "server": "myServerTenant"
    },
    "ingestionConfig": {
      "filterConfig": {
        "filterFunction": "Groovy({foo == \"VALUE1\"}, foo)"
      },
      "transformConfigs": [{
        "columnName": "bar",
        "transformFunction": "lower(moo)"
      },
      {
        "columnName": "hoursSinceEpoch",
        "transformFunction": "toEpochHours(millis)"
      }]
    }
    "metadata": {
      "customConfigs": {
        "key": "value",
        "key": "value"
      }
    }
  }
}
```
{% endcode %}

### Real-time table

Here's an example table config for a real-time table. **All the fields from the offline table config are valid for the real-time table**. Additionally, real-time tables use **some extra fields**.

{% code title="pinot-table-realtime.json" %}
```json
"REALTIME": {
    "tableName": "pinotTable",
    "tableType": "REALTIME",
    "segmentsConfig": {
      "schemaName": "pinotTable",
      "timeColumnName": "daysSinceEpoch",
      "timeType": "DAYS",
      "allowNullTimeValue": true,
      "replicasPerPartition": "3",
      "retentionTimeUnit": "DAYS",
      "retentionTimeValue": "5",
      "segmentPushType": "APPEND",
      "completionConfig": {
        "completionMode": "DOWNLOAD"
      }
    },
    "tableIndexConfig": {
      "invertedIndexColumns": ["foo", "bar", "moo"],
      "sortedColumn": ["column1"],
      "noDictionaryColumns": ["metric1", "metric2"],
      "loadMode": "MMAP",
      "nullHandlingEnabled": false,
    },
    "ingestionConfig:" {
      "streamIngestionConfig": {
       "streamConfigMaps":[
        { "realtime.segment.flush.threshold.rows": "0",
        "realtime.segment.flush.threshold.time": "24h",
        "realtime.segment.flush.threshold.segment.size": "150M",
        "stream.kafka.broker.list": "XXXX",
        "stream.kafka.consumer.factory.class.name": "XXXX",
        "stream.kafka.consumer.prop.auto.offset.reset": "largest",
        "stream.kafka.consumer.type": "XXXX",
        "stream.kafka.decoder.class.name": "XXXX",
        "stream.kafka.decoder.prop.schema.registry.rest.url": "XXXX",
        "stream.kafka.decoder.prop.schema.registry.schema.name": "XXXX",
        "stream.kafka.hlc.zk.connect.string": "XXXX",
        "stream.kafka.topic.name": "XXXX",
        "stream.kafka.zk.broker.url": "XXXX",
        "streamType": "kafka"
      }
    ]
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
