# Table

## Top-level fields

| Property             | Description                                                                                                                                                                                                                                                                                                                                                              |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **tableName**        | Specifies the name of the table. Should only contain alpha-numeric characters, hyphens (‘-‘), or underscores (‘_’). (Using a double-underscore (‘\__’) is not allowed and reserved for other features within Pinot)                                                                                                                                                      |
| **tableType**        | Defines the table type - `OFFLINE` for offline table, `REALTIME` for realtime table. A hybrid table is essentially 2 table configs one of each type, with the same table name.                                                                                                                                                                                           |
| **isDimTable**       | Boolean field to indicate whether the table is a [dimension table](../basics/data-import/batch-ingestion/dim-table.md).                                                                                                                                                                                                                                                  |
| **quota**            | This section defines properties related to quotas, such as storage quota and query quota. For more details scroll down to [quota](table.md#quota).                                                                                                                                                                                                                       |
| **task**             | This section defines the enabled minion tasks for the table. See [Minion](../basics/components/minion.md) for more details.                                                                                                                                                                                                                                              |
| **routing**          | This section defines the properties related to configuring how the broker selects the servers to route, and how segments can be pruned by the broker based on segment metadata. For more details, scroll down to [routing](table.md#routing).                                                                                                                            |
| **query**            | This section defines the properties related to query execution. For more details scroll down to [query](table.md#query).                                                                                                                                                                                                                                                 |
| **segmentsConfig**   | This section defines the properties related to the segments of the table, such as segment push frequency, type, retention, schema, time column etc. For more details scroll down to [segmentsConfig](table.md#segments-config).                                                                                                                                          |
| **tableIndexConfig** | This section defines the indexing related information for the Pinot table. For more details head over to [Table indexing config](table.md#table-index-config).                                                                                                                                                                                                           |
| **fieldConfigList**  | This section specifies the columns and the type of indices to be created on those columns. Currently, only [Text search](../basics/indexing/text-search-support.md) columns can be specified using this property. We will be migrating the rest of the indices to this field in future releases. See [Field config list](table.md#field-config-list) for sub-properties. |
| **tenants**          | Define the server and broker tenant used for this table. More details about tenant can be found in [Tenant](../basics/components/tenant.md).                                                                                                                                                                                                                             |
| **ingestionConfig**  | This section defines the configs needed for ingestion level transformations. More details in [Ingestion Level Transformations](../developers/advanced/ingestion-level-transformations.md) and [Ingestion Level Aggregations](../developers/advanced/ingestion-level-aggregations.md).                                                                                    |
| **upsertConfig**     | This section defines the configs related to the [upsert](../basics/data-import/upsert.md) feature.                                                                                                                                                                                                                                                                       |
| **dedupConfig**      | This section defines the configs related to the [dedup](../basics/data-import/dedup.md) feature.                                                                                                                                                                                                                                                                         |
| **tierConfigs**      | This section defines configs needed to setup tiered storage. More details in [Tiered Storage](../operators/operating-pinot/tiered-storage.md).                                                                                                                                                                                                                           |
| **metadata**         | This section is for keeping custom configs, which are expressed as key-value pairs.                                                                                                                                                                                                                                                                                      |

## Second level fields

The following properties can be nested inside the top-level configs.

### Quota

| Property            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| storage             | The maximum storage space the table is allowed to use, before replication. For example, in the above table, the storage is 140G and replication is 3. Therefore, the maximum storage the table is allowed to use is 140\*3=420G. The space used by the table is calculated by adding up the sizes of all segments from every server hosting this table. Once this limit is reached, offline segment push throws a `403` exception with message, `Quota check failed for segment: segment_0 of table: pinotTable`. |
| maxQueriesPerSecond | The maximum queries per second allowed to execute on this table. If query volume exceeds this, a `429` exception with message `Request 123 exceeds query quota for table:pinotTable, query:select count(*) from pinotTable` will be sent, and a BrokerMetric `QUERY_QUOTA_EXCEEDED` will be recorded. The application should build an exponential backoff and retry mechanism to react to this exception.                                                                                                         |

### Routing

| Property             | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| segmentPrunerTypes   | <p>The list of segment pruners to be enabled.</p><p>The segment pruner prunes the selected segments based on the query. Supported values currently are<br><code>partition</code> - prunes segments based on the partition metadata stored in zookeeper. By default, there is no pruner. For more details on how to configure this check out <a href="../operators/operating-pinot/tuning/routing.md#querying-all-segments">Querying All Segments</a><br><code>time</code> - prunes segments for queries filtering on <code>timeColumnName</code> that do not contain data in the query's time range</p> |
| instanceSelectorType | <p>The instance selector selects server instances to serve the query based on selected segments. Supported values are<br><code>balanced</code> - balances the number of segments served by each selected instance. Default.<br><code>replicaGroup</code> - instance selector for replica group routing strategy.<br>For more details on how to configure this check out <a href="../operators/operating-pinot/tuning/routing.md#querying-all-servers">Querying All Servers</a></p>                                                                                                                      |

### Query

| Property  | Description                   |
| --------- | ----------------------------- |
| timeoutMs | Query timeout in milliseconds |

### Segments Config

| Property                                                                                                                                                 | Description                                                                                                                                                                                                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| schemaName                                                                                                                                               | Name of the schema associated with the table                                                                                                                                                                                                                                                                                                                       |
| timeColumnName                                                                                                                                           | The name of the time column for this table. This must match with the time column name in the schema. This is mandatory for tables with push type `APPEND`, optional for `REFRESH.` timeColumnName along with timeColumnType is used to manage segment retention and time boundary for offline vs realtime.                                                         |
| replication                                                                                                                                              | Number of replicas for the tables. A replication value of 1 means segments won't be replicated across servers.                                                                                                                                                                                                                                                     |
| retentionTimeUnit                                                                                                                                        | Unit for the retention. e.g. HOURS, DAYS. This in combination with retentionTimeValue decides the duration for which to retain the segments e.g. `365 DAYS` in the example means that segments containing data older than 365 days will be deleted periodically. This is done by the `RetentionManager` Controller periodic task. By default, no retention is set. |
| retentionTimeValue                                                                                                                                       | A numeric value for the retention. This in combination with retentionTimeUnit decides the duration for which to retain the segments                                                                                                                                                                                                                                |
| <p>segmentPushType<br></p><p>(Deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -> BatchIngestionConfig -> segmentPushType )</p>           | <p>This can be either<br><code>APPEND</code> - new data segments pushed periodically, to append to the existing data eg. daily or hourly<br><code>REFRESH</code> - the entire data is replaced every time during a data push. Refresh tables have no retention.</p>                                                                                                |
| <p>segmentPushFrequency<br></p><p>(Deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -> BatchIngestionConfig -> segmentPushFrequency )</p> | <p>The cadence at which segments are pushed eg. <code>HOURLY</code>, <code>DAILY</code><br></p>                                                                                                                                                                                                                                                                    |

### Table Index Config

| Property                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------ |------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| invertedIndexColumns                       | The list of columns that inverted index should be created on. The name of columns should match the schema. e.g. in the table above, inverted index has been created on 3 columns `foo`, `bar`, `moo`                                                                                                                                                                                                                                                                                                                                                                                           |
| createInvertedIndexDuringSegmentGeneration | Boolean to indicate whether to create inverted indexes during the segment creation. By default, false i.e. inverted indexes are created when the segments are loaded on the server                                                                                                                                                                                                                                                                                                                                                                                                             |
| sortedColumn                               | The column which is sorted in the data and hence will have a sorted index. This does not need to be specified for the offline table, as the segment generation job will automatically detect the sorted column in the data and create a sorted index for it.                                                                                                                                                                                                                                                                                                                                   |
| bloomFilterColumns                         | The list of columns to apply bloom filter on. The names of the columns should match the schema. For more details about using bloom filters refer to [Bloom Filter](../basics/indexing/bloom-filter.md).                                                                                                                                                                                                                                                                                                                                                                                        |
| bloomFilterConfigs                         | The map from the column to the bloom filter config. The names of the columns should match the schema. For more details about using bloom filters refer to [Bloom Filter](../basics/indexing/bloom-filter.md).                                                                                                                                                                                                                                                                                                                                                                                  |
| rangeIndexColumns                          | The list of columns that range index should be created on. Typically used for numeric columns and mostly on metrics. e.g. `select count(*) from T where latency > 3000` will be faster if you enable range index for **latency**                                                                                                                                                                                                                                                                                                                                                               |
| starTreeIndexConfigs                       | The list of star-tree indexing configs for creating star-tree indexes. For more details on how to configure this, go to [Star-tree](https://apache-pinot.gitbook.io/apache-pinot-cookbook/indexing#index-generation-configuration)                                                                                                                                                                                                                                                                                                                                                             |
| enableDefaultStarTree                      | Boolean to indicate whether to create a default star-tree index for the segment. For more details about this, go to [Star-tree](https://docs.pinot.apache.org/basics/features/indexing#default-index-generation-configuration)                                                                                                                                                                                                                                                                                                                                                                 |
| enableDynamicStarTreeCreation              | Boolean to indicate whether to allow creating star-tree when server loads the segment. Star-tree creation could potentially consume a lot of system resources, so this config should be enabled when the servers have the free system resources to create the star-tree.                                                                                                                                                                                                                                                                                                                       |
| noDictionaryColumns                        | The set of columns that should not be dictionary encoded. The name of columns should match the schema. NoDictionary dimension columns are [Snappy](https://github.com/xerial/snappy-java/blob/master/README.md) compressed, while the metrics are not compressed.                                                                                                                                                                                                                                                                                                                              |
| onHeapDictionaryColumns                    | The list of columns for which the dictionary should be created on heap                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| varLengthDictionaryColumns                 | The list of columns for which the variable length dictionary needs to be enabled in offline segments. This is only valid for string and bytes columns and has no impact for columns of other data types.                                                                                                                                                                                                                                                                                                                                                                                       |
| segmentPartitionConfig                     | <p>The map from column to partition function, which indicates how the segment is partitioned.<br></p><p>Currently 4 types of partition functions are supported:</p><p><code>Murmur</code> - murmur2 hash function</p><p><code>Modulo</code> - modulo on integer values</p><p><code>HashCode</code> - java hashCode() function</p><p><code>ByteArray</code> - java hashCode() on deserialized byte array</p><p><br>Example:</p><p><code>{</code><br><code>"foo": {</code><br><code>"functionName": "Murmur",</code><br><code>"numPartitions": 32</code><br><code>}</code><br><code>}</code></p> |
| loadMode                                   | <p>Indicates how the segments will be loaded onto the server<br><code>heap</code> - load data directly into direct memory<br><code>mmap</code> - load data segments to off-heap memory</p>                                                                                                                                                                                                                                                                                                                                                                                                     |
| columnMinMaxValueGeneratorMode             | <p>Generate min max values for columns. Supported values are<br><code>NONE</code> - do not generate for any columns<br><code>ALL</code> - generate for all columns<br><code>TIME</code> - generate for only time column<br><code>NON_METRIC</code> - generate for time and dimension columns</p>                                                                                                                                                                                                                                                                                               |
| nullHandlingEnabled                        | Boolean to indicate whether to keep track of null values as part of the segment generation. This is required when using `IS NULL` or `IS NOT NULL` predicates in the query. Enabling this will lead to additional memory and storage usage per segment. By default, this is set to _false_.                                                                                                                                                                                                                                                                                                    |
| aggregateMetrics                           | (depreciated, use [Ingestion Aggregation](../developers/advanced/ingestion-level-aggregation.md)) (only applicable for stream) set to `true` to pre-aggregate the metrics                                                                                                                                                                                                                                                                                                                                                                                                                      |
| optimizeDictionaryForMetrics               | Set to `true` if you want to disable dictionaries for single valued metric columns. Only applicable to single-valued metric columns. If a column is specified Default `false`                                                                                                                                                                                                                                                                                                                                                                                                                  |
| noDictionarySizeRatioThreshold             | <p>If <code>optimizeDictionaryForMetrics</code> enabled, dictionary is not created for the metric columns for which <code>noDictionaryIndexSize/ indexWithDictionarySize</code> is less than the <code>noDictionarySizeRatioThreshold</code><br><code>Default: 0.85</code></p>                                                                                                                                                                                                                                                                                                                 |

### Field Config List

Specify the columns and the type of indices to be created on those columns. Currently, only [Text search](../basics/indexing/text-search-support.md) columns can be specified using this property. We will be migrating the rest of the indices to this field in future releases.

| Property     |                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name         | name of the column                                                                                                                                                                                                                                                                                                                                                              |
| encodingType | Should be one of `RAW` or `DICTIONARY`                                                                                                                                                                                                                                                                                                                                          |
| indexType    | index to create on this column. currently only `TEXT` is supported.                                                                                                                                                                                                                                                                                                             |
| properties   | <p>JSON of key-value pairs containing additional properties associated with the index. The following properties are supported currently -</p><ul><li><code>enableQueryCacheForTextIndex</code> - set to <code>true</code> to enable caching for text index in Lucene</li><li><code>rawIndexWriterVersion</code></li><li><code>deriveNumDocsPerChunkForRawIndex</code></li></ul> |

## Realtime Table Config

We will now discuss the sections that are only applicable to realtime tables.

### segmentsConfig

| Property                  | Description                                                                                                 |
| ------------------------- | ----------------------------------------------------------------------------------------------------------- |
| replicasPerPartition      | The number of replicas per partition for the stream                                                         |
| completionMode            | determines if segment should be downloaded from other server or built in memory. can be `DOWNLOAD` or empty |
| peerSegmentDownloadScheme | protocol to use to download segments from server. can be on of `http` or `https`                            |

### Indexing config

Below is the list of fields in `streamConfigs` section.

{% hint style="danger" %}
IndexingConfig -> streamConfig has been deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -> StreamIngestionConfig -> streamConfigMaps instead.
{% endhint %}

| Property                                                                                                                                                       | Description                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| streamType                                                                                                                                                     | only `kafka` is supported at the moment                                                                                                                                                                                                    |
| stream.\[streamType].consumer.type                                                                                                                             | should be one of `lowLevel` or `highLevel` . See [Stream ingestion](../basics/data-import/pinot-stream-ingestion/) for more details                                                                                                        |
| stream.\[streamType].topic.name                                                                                                                                | topic or equivalent datasource from which to consume data                                                                                                                                                                                  |
| stream\[streamType].consumer.prop.auto.offset.reset                                                                                                            | offset to start consuming data from. Should be one of `smallest` , `largest` or a timestamp in millis                                                                                                                                      |
| <p>(0.6.0 onwards) realtime.segment.flush.threshold.rows</p><p>(0.5.0 and prior) (deprecated) <del>realtime.segment.flush.threshold.size</del></p>             | The maximum number of rows to consume before persisting the consuming segment. Default is 5,000,000                                                                                                                                        |
| realtime.segment.flush.threshold.time                                                                                                                          | <p>Maximum elapsed time after which a consuming segment should be persisted.<br>The value can be set as a human readable string, such as <code>1d</code>, <code>4h30m</code><br>Default is 6 hours.</p>                                    |
| <p>(0.6.0 onwards) realtime.segment.flush.threshold.segment.size</p><p>(0.5.0 and prior) (deprecated)</p><p><del>realtime.segment.flush.desired.size</del></p> | Desired size of the completed segments. This value can be set as a human readable string such as `150M`, or `1.1G`, etc. This value is used when `realtime.segment.flush.threshold.rows` is set to 0. Default is `200M` i.e. 200 MegaBytes |
| realtime.segment.flush.autotune.initialRows                                                                                                                    | <p>Initial number of rows for learning.</p><p>This value is used only if <code>realtime.segment.flush.threshold.rows</code> is set o 0 and the consumer type is <code>LowLevel</code>.</p><p>Default is <code>100000 (ie 100K).</code></p> |



{% hint style="info" %}
When specifying `realtime.segment.flush.threshold.rows`, the actual number of rows per segment is computed using the following formula:\
``\
`realtime.segment.flush.threshold.rows / partitionsConsumedByServer`

\
This means that if we set `realtime.segment.flush.threshold.rows=1000` and each server consumes 10 partitions, the rows per segment will be:`1000/10 = 100`
{% endhint %}

All the configurations that are prefixed with the `streamType` are expected to be used by the underlying stream. So, you can set any of the configurations described in the [Kafka configuraton page](https://kafka.apache.org/documentation/#consumerconfigs) can be set using the prefix `stream.kafka` and Kafka should pay attention to it.

### Example

Here is a minimal example of what the `streamConfigs` section may look like:

0.6.0 onwards:

```
"streamConfigs" : {
  "realtime.segment.flush.threshold.rows": "0",
  "realtime.segment.flush.threshold.time": "24h",
  "realtime.segment.flush.threshold.segment.size": "150M",
  "streamType": "kafka",
  "stream.kafka.consumer.type": "LowLevel",
  "stream.kafka.topic.name": "ClickStream",
  "stream.kafka.consumer.prop.auto.offset.reset" : "largest"
}
```

0.5.0 and prior:

```
"streamConfigs" : {
  "realtime.segment.flush.threshold.size": "0",
  "realtime.segment.flush.threshold.time": "24h",
  "realtime.segment.flush.desired.size": "150M",
  "streamType": "kafka",
  "stream.kafka.consumer.type": "LowLevel",
  "stream.kafka.topic.name": "ClickStream",
  "stream.kafka.consumer.prop.auto.offset.reset" : "largest"
}
```

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

## Environment Variables Override

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

## Sample Configurations

### Offline Table

{% code title="pinot-table-offline.json" %}
```javascript
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
        "pk": {
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

### Realtime Table

Here's an example table config for a realtime table. **All the fields from the offline table config are valid for the realtime table**. Additionally, realtime tables use **some extra fields**.

{% code title="pinot-table-realtime.json" %}
```javascript
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
      "streamConfigs": {
        "realtime.segment.flush.threshold.rows": "0",
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
    },
    "tenants": {
      "broker": "myBrokerTenant",
      "server": "myServerTenant",
      "tagOverrideConfig": {}
    },
    "metadata": {
    }
}
```
{% endcode %}
