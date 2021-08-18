# Table

### Top-level fields

| Property | Description |
| :--- | :--- |
| **tableName** | Specifies the name of the table. Should only contain alpha-numeric characters, hyphens \(‘-‘\), or underscores \(‘_’\).  \(Using a double-underscore \(‘\__’\) is not allowed and reserved for other features within Pinot\) |
| **tableType** | Defines the table type - `OFFLINE` for offline table,  `REALTIME` for realtime table.  A hybrid table is essentially 2 table configs one of each type, with the same table name. |
| **isDimTable** | Boolean field to indicate whether the table is a [dimension table](../basics/data-import/batch-ingestion/dim-table.md). |
| **quota** | This section defines properties related to quotas, such as storage quota and query quota. For more details scroll down to [quota](table.md#quota). |
| **task** | This section defines the enabled minion tasks for the table. See [Minion](../basics/components/minion.md) for more details. |
| **routing** | This section defines the properties related to configuring how the broker selects the servers to route, and how segments can be pruned by the broker based on segment metadata. For more details, scroll down to [routing](table.md#routing). |
| **query** | This section defines the properties related to query execution. For more details scroll down to [query](table.md#query). |
| **segmentsConfig** | This section defines the properties related to the segments of the table, such as segment push frequency, type, retention, schema, time column etc. For more details scroll down to [segmentsConfig](table.md#segments-config). |
| **tableIndexConfig** | This section defines the indexing related information for the Pinot table. For more details head over to [Table indexing config](table.md#table-index-config). |
| **fieldConfigList** | This section specifies the columns and the type of indices to be created on those columns. Currently, only [Text search](../basics/indexing/text-search-support.md) columns can be specified using this property. We will be migrating the rest of the indices to this field in future releases. See [Field config list](table.md#field-config-list) for sub-properties. |
| **tenants** | Define the server and broker tenant used for this table. More details about tenant can be found in [Tenant](../basics/components/tenant.md). |
| **ingestionConfig** | This section defines the configs needed for ingestion level transformations. More details in[ Ingestion Level Transformations](../developers/advanced/ingestion-level-transformations.md). |
| **upsertConfig** | This section defines the configs related to the [upsert](../basics/data-import/upsert.md) feature. |
| **tierConfigs** | This section defines configs needed to setup tiered storage. More details in [Tiered Storage](../operators/operating-pinot/tiered-storage.md). |
| **metadata** | This section is for keeping custom configs, which are expressed as key-value pairs. |

### Second level fields

The following properties can be nested inside the top-level configs.

#### Quota

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">storage</td>
      <td style="text-align:left">The maximum storage space the table is allowed to use, before replication.
        For example, in the above table, the storage is 140G and replication is
        3. Therefore, the maximum storage the table is allowed to use is 140*3=420G.
        The space used by the table is calculated by adding up the sizes of all
        segments from every server hosting this table. Once this limit is reached,
        offline segment push throws a <code>403</code> exception with message, <code>Quota check failed for segment: segment_0 of table: pinotTable</code>.</td>
    </tr>
    <tr>
      <td style="text-align:left">maxQueriesPerSecond</td>
      <td style="text-align:left">The maximum queries per second allowed to execute on this table. If query
        volume exceeds this, a <code>429</code> exception with message <code>Request 123 exceeds query quota for table:pinotTable, query:select count(*) from pinotTable</code>
        will be sent, and a BrokerMetric <code>QUERY_QUOTA_EXCEEDED</code> will
        be recorded. The application should build an exponential backoff and retry
        mechanism to react to this exception.
      </td>
    </tr>
  </tbody>
</table>

#### Routing

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">segmentPrunerTypes</td>
      <td style="text-align:left">
        <p>The list of segment pruners to be enabled.</p>
        <p>The segment pruner prunes the selected segments based on the query. Supported
          values currently are
          <br /> <code>partition</code> - prunes segments based on the partition metadata
          stored in zookeeper. By default, there is no pruner. For more details on
          how to configure this check out <a href="../operators/operating-pinot/tuning/routing.md#querying-all-segments">Querying All Segments</a>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">instanceSelectorType</td>
      <td style="text-align:left">The instance selector selects server instances to serve the query based
        on selected segments. Supported values are
        <br /><code>balanced</code> - balances the number of segments served by each
        selected instance. Default.
        <br /><code>replicaGroup</code> - instance selector for replica group routing
        strategy.
        <br />For more details on how to configure this check out <a href="../operators/operating-pinot/tuning/routing.md#querying-all-servers">Querying All Servers</a>
      </td>
    </tr>
  </tbody>
</table>

#### Query

| Property | Description |
| :--- | :--- |
| timeoutMs | Query timeout in milliseconds |

#### Segments Config

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">schemaName</td>
      <td style="text-align:left">Name of the schema associated with the table</td>
    </tr>
    <tr>
      <td style="text-align:left">timeColumnName</td>
      <td style="text-align:left">The name of the time column for this table. This must match with the time
        column name in the schema. This is mandatory for tables with push type <code>APPEND</code>,
        optional for <code>REFRESH. </code>timeColumnName along with timeColumnType
        is used to manage segment retention and time boundary for offline vs realtime.</td>
    </tr>
    <tr>
      <td style="text-align:left">allowNullTimeValue</td>
      <td style="text-align:left">Boolean to indicate whether null value in time column is allowed.
        By default, false i.e. data source needs to make sure the value is not null in time column.
        When this flag is enabled, a default value based on machine time will be filled in if time column is null.</td>
    </tr>
    <tr>
      <td style="text-align:left">replication</td>
      <td style="text-align:left">Number of replicas</td>
    </tr>
    <tr>
      <td style="text-align:left">retentionTimeUnit</td>
      <td style="text-align:left">Unit for the retention. e.g. HOURS, DAYS. This in combination with retentionTimeValue
        decides the duration for which to retain the segments e.g. <code>365 DAYS</code> in
        the example means that segments containing data older than 365 days will
        be deleted periodically. This is done by the <code>RetentionManager</code> Controller
        periodic task. By default, no retention is set.</td>
    </tr>
    <tr>
      <td style="text-align:left">retentionTimeValue</td>
      <td style="text-align:left">A numeric value for the retention. This in combination with retentionTimeUnit
        decides the duration for which to retain the segments</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>segmentPushType
          <br />
        </p>
        <p>(Deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -&gt;
          BatchIngestionConfig -&gt; segmentPushType )</p>
      </td>
      <td style="text-align:left">This can be either
        <br /><code>APPEND</code> - new data segments pushed periodically, to append
        to the existing data eg. daily or hourly
        <br /><code>REFRESH</code> - the entire data is replaced every time during a
        data push. Refresh tables have no retention.</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>segmentPushFrequency
          <br />
        </p>
        <p>(Deprecated starting 0.7.0 or commit 9eaea9. Use IngestionConfig -&gt;
          BatchIngestionConfig -&gt; segmentPushFrequency )</p>
      </td>
      <td style="text-align:left">The cadence at which segments are pushed eg. <code>HOURLY</code>, <code>DAILY</code>
        <br
        />
      </td>
    </tr>
  </tbody>
</table>

#### Table Index Config

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">invertedIndexColumns</td>
      <td style="text-align:left">The list of columns that inverted index should be created on. The name
        of columns should match the schema. e.g. in the table above, inverted index
        has been created on 3 columns <code>foo</code>, <code>bar</code>, <code>moo</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">createInvertedIndexDuringSegmentGeneration</td>
      <td style="text-align:left">Boolean to indicate whether to create inverted indexes during the segment
        creation. By default, false i.e. inverted indexes are created when the
        segments are loaded on the server</td>
    </tr>
    <tr>
      <td style="text-align:left">sortedColumn</td>
      <td style="text-align:left">The column which is sorted in the data and hence will have a sorted index.
        This does not need to be specified for the offline table, as the segment
        generation job will automatically detect the sorted column in the data
        and create a sorted index for it.</td>
    </tr>
    <tr>
      <td style="text-align:left">bloomFilterColumns</td>
      <td style="text-align:left">The list of columns to apply bloom filter on. The names of the columns
        should match the schema. For more details about using bloom filters refer
        to <a href="../basics/indexing/bloom-filter.md">Bloom Filter</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">bloomFilterConfigs</td>
      <td style="text-align:left">The map from the column to the bloom filter config. The names of the columns
        should match the schema. For more details about using bloom filters refer
        to <a href="../basics/indexing/bloom-filter.md">Bloom Filter</a>.</td>
    </tr>
    <tr>
      <td style="text-align:left">rangeIndexColumns</td>
      <td style="text-align:left">The list of columns that range index should be created on. Typically used
        for numeric columns and mostly on metrics. e.g. <code>select count(*) from T where latency &gt; 3000</code> will
        be faster if you enable range index for <b>latency</b>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">starTreeIndexConfigs</td>
      <td style="text-align:left">The list of star-tree indexing configs for creating star-tree indexes.
        For more details on how to configure this, go to <a href="https://apache-pinot.gitbook.io/apache-pinot-cookbook/indexing#index-generation-configuration">Star-tree</a>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">enableDefaultStarTree</td>
      <td style="text-align:left">Boolean to indicate whether to create a default star-tree index for the
        segment. For more details about this, go to <a href="https://docs.pinot.apache.org/basics/features/indexing#default-index-generation-configuration">Star-tree</a>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">enableDynamicStarTreeCreation</td>
      <td style="text-align:left">Boolean to indicate whether to allow creating star-tree when server loads
        the segment. Star-tree creation could potentially consume a lot of system
        resources, so this config should be enabled when the servers have the free
        system resources to create the star-tree.</td>
    </tr>
    <tr>
      <td style="text-align:left">noDictionaryColumns</td>
      <td style="text-align:left">The set of columns that should not be dictionary encoded. The name of
        columns should match the schema. NoDictionary dimension columns are <a href="https://github.com/xerial/snappy-java/blob/master/README.md">Snappy</a> compressed,
        while the metrics are not compressed.</td>
    </tr>
    <tr>
      <td style="text-align:left">onHeapDictionaryColumns</td>
      <td style="text-align:left">The list of columns for which the dictionary should be created on heap</td>
    </tr>
    <tr>
      <td style="text-align:left">varLengthDictionaryColumns</td>
      <td style="text-align:left">The list of columns for which the variable length dictionary needs to
        be enabled in offline segments. This is only valid for string and bytes
        columns and has no impact for columns of other data types.</td>
    </tr>
    <tr>
      <td style="text-align:left">segmentPartitionConfig</td>
      <td style="text-align:left">
        <p>The map from column to partition function, which indicates how the segment
          is partitioned.
          <br />
        </p>
        <p>Currently 4 types of partition functions are supported:</p>
        <p><code>Murmur</code> - murmur2 hash function</p>
        <p><code>Modulo</code> - modulo on integer values</p>
        <p><code>HashCode</code> - java hashCode() function</p>
        <p><code>ByteArray</code> - java hashCode() on deserialized byte array</p>
        <p>
          <br />Example:</p>
        <p><code>{<br />  &quot;foo&quot;: {<br />    &quot;functionName&quot;: &quot;Murmur&quot;,<br />    &quot;numPartitions&quot;: 32<br />  }<br />}</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">loadMode</td>
      <td style="text-align:left">Indicates how the segments will be loaded onto the server
        <br /><code>heap</code> - load data directly into direct memory
        <br /><code>mmap</code> - load data segments to off-heap memory</td>
    </tr>
    <tr>
      <td style="text-align:left">columnMinMaxValueGeneratorMode</td>
      <td style="text-align:left">Generate min max values for columns. Supported values are
        <br /><code>NONE</code> - do not generate for any columns
        <br /><code>ALL</code> - generate for all columns
        <br /><code>TIME</code> - generate for only time column
        <br /><code>NON_METRIC</code> - generate for time and dimension columns</td>
    </tr>
    <tr>
      <td style="text-align:left">nullHandlingEnabled</td>
      <td style="text-align:left">Boolean to indicate whether to keep track of null values as part of the
        segment generation. This is required when using <code>IS NULL</code> or <code>IS NOT NULL</code> predicates
        in the query. Enabling this will lead to additional memory and storage
        usage per segment. By default, this is set to <em>false</em>.</td>
    </tr>
    <tr>
      <td style="text-align:left">aggregateMetrics</td>
      <td style="text-align:left">(only applicable for stream) set to <code>true</code> to pre-aggregate the
        metrics</td>
    </tr>
  </tbody>
</table>

#### Field Config List

Specify the columns and the type of indices to be created on those columns. Currently, only [Text search](../basics/indexing/text-search-support.md) columns can be specified using this property. We will be migrating the rest of the indices to this field in future releases.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">name</td>
      <td style="text-align:left">name of the column</td>
    </tr>
    <tr>
      <td style="text-align:left">encodingType</td>
      <td style="text-align:left">Should be one of <code>RAW</code> or <code>DICTIONARY</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">indexType</td>
      <td style="text-align:left">index to create on this column. currently only <code>TEXT</code> is supported.</td>
    </tr>
    <tr>
      <td style="text-align:left">properties</td>
      <td style="text-align:left">
        <p>JSON of key-value pairs containing additional properties associated with
          the index. The following properties are supported currently -</p>
        <ul>
          <li><code>enableQueryCacheForTextIndex</code> - set to <code>true</code> to enable
            caching for text index in Lucene</li>
          <li><code>rawIndexWriterVersion</code>
          </li>
          <li><code>deriveNumDocsPerChunkForRawIndex </code>
          </li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### Realtime Table Config

We will now discuss the sections that are only applicable to realtime tables.

#### segmentsConfig

| Property | Description |
| :--- | :--- |
| replicasPerPartition | The number of replicas per partition for the stream |
| completionMode | determines if segment should be downloaded from other server or built in memory. can be `DOWNLOAD` or empty |
| peerSegmentDownloadScheme | protocol to use to download segments from server. can be on of `http` or `https`  |

#### Indexing config

Below is the list of fields in `streamConfigs` section.

{% hint style="danger" %}
IndexingConfig -&gt; streamConfig has been deprecated starting 0.7.0 or commit 9eaea9.
Use IngestionConfig -&gt; StreamIngestionConfig -&gt; streamConfigMaps instead.
{% endhint %}

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">streamType</td>
      <td style="text-align:left">only <code>kafka</code> is supported at the moment</td>
    </tr>
    <tr>
      <td style="text-align:left">stream.[streamType].consumer.type</td>
      <td style="text-align:left">should be one of <code>lowLevel</code> or <code>highLevel</code> . See <a href="../basics/data-import/pinot-stream-ingestion/">Stream ingestion</a> for
        more details</td>
    </tr>
    <tr>
      <td style="text-align:left">stream.[streamType].topic.name</td>
      <td style="text-align:left">topic or equivalent datasource from which to consume data</td>
    </tr>
    <tr>
      <td style="text-align:left">stream[streamType].consumer.prop.auto.offset.reset</td>
      <td style="text-align:left">offset to start consuming data from. Should be one of <code>smallest</code> , <code>largest</code> or
        a timestamp in millis</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>(0.6.0 onwards) realtime.segment.flush.threshold.rows</p>
        <p>(0.5.0 and prior) (deprecated) <del>realtime.segment.flush.threshold.size</del>
        </p>
      </td>
      <td style="text-align:left">Maximum number of rows to consume before persisting the consuming segment.
        Default is 5000000</td>
    </tr>
    <tr>
      <td style="text-align:left">realtime.segment.flush.threshold.time</td>
      <td style="text-align:left">Maximum elapsed time after which a consuming segment should be persisted.
        <br
        />The value can be set as a human readable string, such as <code>1d</code>, <code>4h30m</code>
        <br
        />Default is 6 hours.</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>(0.6.0 onwards) realtime.segment.flush.threshold.segment.size</p>
        <p>(0.5.0 and prior) (deprecated)</p>
        <p><del>realtime.segment.flush.desired.size</del>
        </p>
      </td>
      <td style="text-align:left">Desired size of the completed segments. This value can be set as a human
        readable string such as <code>150M</code>, or <code>1.1G</code>, etc. This
        value is used when <code>realtime.segment.flush.threshold.size</code> is
        set to 0. Default is <code>200M</code> i.e. 200 MegaBytes</td>
    </tr>
    <tr>
      <td style="text-align:left">realtime.segment.flush.autotune.initialRows</td>
      <td style="text-align:left">
        <p>Initial number of rows for learning.</p>
        <p>This value is used only if <code>realtime.segment.flush.threshold.size</code> is
          set o 0 and the consumer type is <code>LowLevel</code>.</p>
        <p>Default is <code>100K</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

All the configurations that are prefixed with the `streamType` are expected to be used by the underlying stream. So, you can set any of the configurations described in the [Kafka configuraton page](https://kafka.apache.org/documentation/#consumerconfigs) can be set using the prefix `stream.kafka` and Kafka should pay attention to it.

#### Example

Here is a minimal example of what the `streamConfigs` section may look like:

0.6.0 onwards:

```text
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

```text
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

### Tenants

| Property | Description |
| :--- | :--- |
| broker | Broker tenant in which the segment should reside |
| server | Server tenant in which the segment should reside |
| tagOverrideConfig | Override the tenant for segment if it fulfills certain conditions. Currently, only support override on `realtimeConsuming` or `realtimeCompleted` |

#### Example

```javascript
  "broker": "brokerTenantName",
  "server": "serverTenantName",
  "tagOverrideConfig" : {
    "realtimeConsuming" : "serverTenantName_REALTIME"
    "realtimeCompleted" : "serverTenantName_OFFLINE"
  }
}
```

### Environment Variables Override

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

### Sample Configurations

#### Offline Table

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



#### Realtime Table

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
      "aggregateMetrics": true,
      "nullHandlingEnabled": false,
      "streamConfigs": {
        "realtime.segment.flush.threshold.size": "0",
        "realtime.segment.flush.threshold.time": "24h",
        "realtime.segment.flush.desired.size": "150M",
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

