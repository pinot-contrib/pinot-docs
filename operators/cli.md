# Command-Line Interface (CLI)

Pinot provides a rich CLI to perform almost every operation on the cluster. You can execute all the commands using the `pinot-admin.sh`. The script is located in the `bin/` directory of the [Pinot binary distribution](https://pinot.apache.org/download) or `/opt/pinot/bin` in docker container.

The following commands are supported by the admin script.

### Add Schema

Upload the schema configuration to controller. If their is already a schema with same name, it will be updated.

```
pinot-admin.sh AddSchema -schemaFile /path/to/schema.json -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>schemaFile</td>
      <td>path to [schema JSON](../configuration-reference/schema.md) file mentioned in table configuration.</td>
    </tr>
    <tr>
      <td>controllerHost</td>
      <td>controllerHost on which to send the upload requests</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>controllerPort on which to send the upload requests</td>
    </tr>
    <tr>
      <td>exec</td>
      <td>If not specified, a dry run will be done but configs won't actually be uploaded.</td>
    </tr>
  </tbody>
</table>

### Add Table

Upload the table configuration to controller.

```
pinot-admin.sh AddTable -tableConfigFile /path/to/table.json -schemaFile /path/to/schema.json -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>tableConfigFile</td>
      <td>path to JSON file containing [Table configuration](../configuration-reference/table.md).</td>
    </tr>
    <tr>
      <td>schemaFile</td>
      <td>path to [schema JSON](../configuration-reference/schema.md) file mentioned in table configuration.</td>
    </tr>
    <tr>
      <td>controllerHost</td>
      <td>controllerHost on which to send the upload requests</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>controllerPort on which to send the upload requests</td>
    </tr>
    <tr>
      <td>exec</td>
      <td>If not specified, a dry run will be done but configs won't actually be uploaded.</td>
    </tr>
  </tbody>
</table>

### Add Tenant

Add a new tenant to the server

```
pinot-admin.sh AddTenant -name myTenant -role SERVER -instanceCount 10 -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controllerHost</td>
      <td>controllerHost on which to send the upload requests</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>controllerPort on which to send the upload requests</td>
    </tr>
    <tr>
      <td>name</td>
      <td>name of the tenant</td>
    </tr>
    <tr>
      <td>role</td>
      <td>where the tenant should reside. can be `BROKER` or `SERVER`</td>
    </tr>
    <tr>
      <td>instanceCount</td>
      <td>total number of instances to assign to this tenant</td>
    </tr>
    <tr>
      <td>offlineInstanceCount</td>
      <td>(only applicable for `SERVER`) total number of instances which can host offline tables belonging to this tenant</td>
    </tr>
    <tr>
      <td>realTimeInstanceCount</td>
      <td>(only applicable for `SERVER`)total number of instances which can host real-time tables belonging to this tenant</td>
    </tr>
    <tr>
      <td>exec</td>
      <td>If not specified, a dry run will be done but configs won't actually be uploaded.</td>
    </tr>
  </tbody>
</table>

### Check Offline Segment Intervals

Lists all the segments which have invalid time interval. Only `OFFLINE` segments are supported.

```
pinot-admin.sh CheckOfflineSegmentIntervals -zkAddress localhost:2181 -clusterName PinotCluster -tableName myTable
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of Zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>Comma separated list of tables to check for invalid segment intervals. By default all tables are checked.</td>
    </tr>
  </tbody>
</table>

### Change Num Replicas

This command changes the replicas of the table. The number of replicas are set from the latest available table config.

```
pinot-admin.sh ChangeNumReplicas -tableName myTable -clusterName PinotCluster -zkAddress localhost:2181 -exec
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>name of the table on which to perform operation</td>
    </tr>
    <tr>
      <td>exec</td>
      <td>If not specified, a dry run will be done but configs won't actually be uploaded.</td>
    </tr>
  </tbody>
</table>

### Change Table State

Enable, Disable or Drop the table available in database.

```
pinot-admin.sh ChangeTableState -tableName myTable -state disable -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controllerHost</td>
      <td>controllerHost on which to send the upload requests</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>controllerPort on which to send the upload requests</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>name of the table to modify</td>
    </tr>
    <tr>
      <td>state</td>
      <td>can be one of `enable` , `disable` or `drop`</td>
    </tr>
  </tbody>
</table>

### Create Segment

Create segment files from the input file in local filesystem.

```
pinot-admin.sh CreateSegment -dataDir /path/to/data/dir -format CSV -outDir /path/to/output/dir -overwrite -tableConfigFile /path/to/table.json -schemaConfigFile /path/to/schema.json
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dataDir</td>
      <td>Directory containing input files</td>
    </tr>
    <tr>
      <td>format</td>
      <td>Input data formats. See [Input formats](../manage-data/data-import/pinot-input-formats.md) for all the supported formats</td>
    </tr>
    <tr>
      <td>outDir</td>
      <td>Local output directory to publish the segments</td>
    </tr>
    <tr>
      <td>overwrite</td>
      <td>Set to `true` to overwrite segments of already present in the directory</td>
    </tr>
    <tr>
      <td>tableConfigFile</td>
      <td>Path to [Table Config](../configuration-reference/table.md)</td>
    </tr>
    <tr>
      <td>schemaFile</td>
      <td>Path to [Schema Config](../configuration-reference/schema.md)</td>
    </tr>
    <tr>
      <td>readerConfigFile</td>
      <td>properties file containing the config related to the reader. See [Input formats](../manage-data/data-import/pinot-input-formats.md)</td>
    </tr>
    <tr>
      <td>retry</td>
      <td>Number of retry attempts in case of failure</td>
    </tr>
    <tr>
      <td>postCreationVerification</td>
      <td>Set `true` to verify the segment files post creation.</td>
    </tr>
    <tr>
      <td>numThreads</td>
      <td>Number of threads to use to execute the segment creation job</td>
    </tr>
  </tbody>
</table>

### Convert Pinot Segment

Convert the segment file from Pinot specific format to other data formats. Currently `CSV`, `AVRO`, `JSON`, and `PARQUET` are supported.

```
pinot-admin.sh ConvertPinotSegment -dataDir /path/to/data/dir -outputDir /path/to/output/dir -outputFormat CSV -overwrite -csvDelimiter ,
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>dataDir</td>
      <td>directory containing the segment files. Only local filePaths are supported</td>
    </tr>
    <tr>
      <td>outputDir</td>
      <td>directory to put the converted segment files in.</td>
    </tr>
    <tr>
      <td>outputFormat</td>
      <td>format to output the files in. Can be one of `CSV`, `AVRO`, `JSON`, or `PARQUET`</td>
    </tr>
    <tr>
      <td>overwrite</td>
      <td>set it to overwrite the files if already present in output directory</td>
    </tr>
    <tr>
      <td>csvDelimiter</td>
      <td>delimiter to use for CSV files. only applicable to `CSV`</td>
    </tr>
    <tr>
      <td>csvListDelimiter</td>
      <td>delimiter to use for list/array in CSV files. only applicable to `CSV`</td>
    </tr>
    <tr>
      <td>csvWithHeader</td>
      <td>set to print CSV header in output file. Default is `false`.</td>
    </tr>
  </tbody>
</table>

##### Parquet Format Notes

When converting to `PARQUET` format, the following features are supported:

* Multi-value columns (Object[]) are automatically converted to lists
* Binary data (byte[]) is wrapped in ByteBuffer for Parquet compatibility
* GZIP compression is applied by default for reduced file size
* Example usage: `pinot-admin.sh ConvertPinotSegment -dataDir /path/to/segments -outputDir /path/to/output -outputFormat PARQUET`

### Delete Cluster

Delete the cluster namespace from zookeeper.

```
pinot-admin.sh DeleteCluster -clusterName PinotCluster -zkAddress localhost:2181
```

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to delete</td>
    </tr>
    <tr>
      <td>zkAddress</td>
      <td>Comma separated host:port list of zookeeper from which to delete the cluster namespace</td>
    </tr>
  </tbody>
</table>

### Launch Data Ingestion Job

Run job to consume batch or streaming data and push it to Pinot.

```
pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /path/to/job_spec.json -propertyFile /path/to/job.properties -values dt=2020-08-10 hour=15
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>jobSpecFile</td>
      <td>Path to[ job spec file.](../configuration-reference/job-specification.md) Only local file paths are supported</td>
    </tr>
    <tr>
      <td>propertyFile</td>
      <td>Path to properties file. This file can contain properties related to ingestion job or template paramaters</td>
    </tr>
    <tr>
      <td>values</td>
      <td>list of string containing the values to replace template parameters with</td>
    </tr>
  </tbody>
</table>

### Merge/Rollup Segments

Perform operations similar to the [Minion Merge Rollup Task](operating-pinot/minion-merge-rollup-task.md), where multiple segments can be merged based on the provided spec.

{% hint style="warning" %}
This command is mostly for debugging purpose. Use Minion Merge Rollup Task for production.
{% endhint %}

```
pinot-admin.sh SegmentProcessorFramework -segmentProcessorFrameworkSpec /path/to/framework_spec.json
```

#### Fields within the spec file

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>inputSegmentsDir</td>
      <td>directory that contains all the input segment files or directories to be merged</td>
    </tr>
    <tr>
      <td>outputSegmentsDir</td>
      <td>directory in which merged segment file should be put</td>
    </tr>
    <tr>
      <td>tableConfigFile</td>
      <td>path to table config for which segments are to be merged</td>
    </tr>
    <tr>
      <td>schemaFile</td>
      <td>path to schema of the table for which segment should be merged</td>
    </tr>
    <tr>
      <td>timeHandlerConfig</td>
      <td>configs related to time handling, including `type`, `startTimeMs`, `endTimeMs`, `roundBucketMs`, `partitionBucketMs`</td>
    </tr>
    <tr>
      <td>partitionerConfigs</td>
      <td>list of partition related configs, including `partitionerType`, `numPartitions`, `columnName`, `transformFunction`, `columnPartitionConfig`</td>
    </tr>
    <tr>
      <td>mergeType</td>
      <td>`CONCAT`, `ROLLUP`, `DEDUP`</td>
    </tr>
    <tr>
      <td>aggregationTypes</td>
      <td>map from metric column to aggregation function type for the `ROLLUP` merge type</td>
    </tr>
    <tr>
      <td>segmentConfig</td>
      <td>configs related to the generated segments, including `maxNumRecordsPerSegment`, `segmentNamePrefix`</td>
    </tr>
  </tbody>
</table>

### Move Replica Group

Command to migrate a subset of replica group from current servers to the provided destination servers. This command is intended to be run multiple times to migrate all the replicas of a table to the destination servers (if intended).

```
pinot-admin.sh MoveReplicaGroup -zkHost localhost:2181 -cluster PinotCluster -srcHosts host1,host2 -destHostsFile /path/to/destination/file -tableName myTable -exec
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>srcHosts</td>
      <td>path of the file with all the source hosts or comma-separated list of hostnames</td>
    </tr>
    <tr>
      <td>destHostsFile</td>
      <td>path of the file with all the destination hosts</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>name of the table for which replica group is to be moved. Supports only `OFFLINE` tables currently</td>
    </tr>
    <tr>
      <td>maxSegmentsToMove</td>
      <td>maximum number of segments to move. default is `Integer.MAX_VALUE`</td>
    </tr>
    <tr>
      <td>zkHost</td>
      <td>zookeeper host:port string</td>
    </tr>
    <tr>
      <td>cluster</td>
      <td>name of the cluster inside zookeeper .</td>
    </tr>
    <tr>
      <td>exec</td>
      <td>set to execute the command. If unset, only a dry run will be done</td>
    </tr>
  </tbody>
</table>

### Operate Cluster Config

Modify[ cluster level configs](../configuration-reference/cluster.md) for pinot. These are the configs which are applicable to all nodes in the cluster.

```
pinot-admin.sh OperateClusterConfig -controllerHost localhost -controllerPort 9000 -operation ADD -config pinot.broker.enable.query.limit.override=1
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>operation</td>
      <td><p>Type of operation to perform.<br>Can be one of <code>GET, ADD, UPDATE or DELETE</code></p></td>
    </tr>
    <tr>
      <td>config</td>
      <td>The config on which operation should be performed. In case of ADD or UPDATE, the config value is provided after `=`</td>
    </tr>
    <tr>
      <td>controllerHost</td>
      <td>The host on which to send the request</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>The port on which to send the requests</td>
    </tr>
  </tbody>
</table>

### Post Query

Execute a SQL query on the cluster.

```
pinot-admin.sh PostQuery -brokerHost localhost -brokerPort 8000 -query "SELECT * FROM myTable"
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>brokerHost</td>
      <td>broker host to execute the query on</td>
    </tr>
    <tr>
      <td>brokerPort</td>
      <td>broker port to execute the query on</td>
    </tr>
    <tr>
      <td>query</td>
      <td>SQL query to execute</td>
    </tr>
  </tbody>
</table>

### Rebalance Table

Rebalance a table i.e. reassign instances and segments for a table in the cluster.

For segment reassignment, the following modes are offered:

* `With-downtime rebalance`: the IdealState is replaced with the target segment assignment in one go and there are no guarantees around replica availability. This mode returns immediately without waiting for ExternalView to reach the target segment assignment. Disabled tables will always be rebalanced with downtime.
* `No-downtime rebalance`: care is taken to ensure that the configured number of replicas of any segment are available (ONLINE or CONSUMING) at all times. This mode returns after ExternalView reaching the target segment assignment.\
  \
  In the edge case scenarios mentioned later, if `best-efforts` is disabled, **rebalancer will fail the rebalance because the no-downtime contract cannot be achieved**, and table might end up in a middle stage. User needs to check the rebalance result, solve the issue, and run the rebalance again if necessary.\
  \
  If `best-efforts` is enabled, rebalancer will log a warning and continue the rebalance, but the no-downtime contract will not be guaranteed.\
  \
  Downtime can occur in the following edge case scenarios -
  * Segment falls into ERROR state in ExternalView -> with best-efforts, count ERROR state as good state.
  * ExternalView has not converged within the maximum wait time -> with best-efforts, continue to the next stage

{% hint style="danger" %}
**If the controller that handles the rebalance goes down/restarted, the rebalance isn't automatically resumed by other controllers**
{% endhint %}

```
pinot-admin.sh RebalanceTable -zkAddress localhost:2181 -clusterName PinotCluster -tableName myTable -reassignInstances -includeConsuming -downtime  
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>name of the table on which to perform operation</td>
    </tr>
    <tr>
      <td>reassignInstances</td>
      <td>set to reassign instances before reassigning segments (`false` by default)</td>
    </tr>
    <tr>
      <td>includeConsuming</td>
      <td>set to reassign `CONSUMING` segments for real-time table (`false` by default)</td>
    </tr>
    <tr>
      <td>bootstrap</td>
      <td>set to rebalance table in bootstrap mode (regardless of minimum segment movement, reassign all segments in a round-robin fashion as if adding new segments to an empty table, `false` by default)</td>
    </tr>
    <tr>
      <td>downtime</td>
      <td>Set to allow downtime for the rebalance (`false` by default)</td>
    </tr>
    <tr>
      <td>minAvailableReplicas</td>
      <td>minimum number of replicas to keep alive during rebalance, or maximum number of replicas allowed to be unavailable if value is negative (default is 1), Only applicable if downtime is set to `false`</td>
    </tr>
    <tr>
      <td>bestEfforts</td>
      <td>set to use best-efforts to rebalance i.e. not fail the rebalance when the no-downtime contract cannot be achieved, `false` by default</td>
    </tr>
  </tbody>
</table>

### Start Broker

Start a broker instance on host

```
pinot-admin.sh StartBroker -zkAddress localhost:2181 -clusterName PinotCluster -configFileName /path/to/broker.conf
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>brokerHost</td>
      <td>hostname of the instance on which to run the broker</td>
    </tr>
    <tr>
      <td>brokerPort</td>
      <td>port on which the broker should listen. Default 8099.</td>
    </tr>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of Zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>configFileName</td>
      <td>path to properties file containing controller configs. See [Broker](../configuration-reference/broker.md) for complete configuration</td>
    </tr>
  </tbody>
</table>

### Start Controller

Start a controller instance on host

```
pinot-admin.sh StartController -controllerMode helix_only -dataDir /path/to/data/dir -zkAddress localhost:2181 -clusterName PinotCluster -configFileName /path/to/controller.conf
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controllerMode</td>
      <td>Should be one of `dual`, `pinot_only` or `helix_only`. Default is `dual`</td>
    </tr>
    <tr>
      <td>controllerHost</td>
      <td>hostname of the instance on which to run the controller</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>port on which the controller should listen. Default 9000.</td>
    </tr>
    <tr>
      <td>dataDir</td>
      <td>path to directory to store data. Default is `java.io.tmpDir` + `PinotController`</td>
    </tr>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of Zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>configFileName</td>
      <td>path to properties file containing controller configs. See [Controller](../configuration-reference/controller.md) for complete configuration</td>
    </tr>
  </tbody>
</table>

### Start Server

Start a server instance on host

```
pinot-admin.sh StartServer -dataDir /path/to/data/dir -zkAddress localhost:2181 -clusterName PinotCluster -configFileName /path/to/server.conf
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>serverHost</td>
      <td>hostname of the instance on which to run the broker</td>
    </tr>
    <tr>
      <td>serverPort</td>
      <td>port on which the broker should listen. Default 8099.</td>
    </tr>
    <tr>
      <td>serverAdminPort</td>
      <td>port on which admin API should be available. Default it 8097</td>
    </tr>
    <tr>
      <td>dataDir</td>
      <td>directory in which to store the data</td>
    </tr>
    <tr>
      <td>segmentDir</td>
      <td>directory in which to download the .tar segment files temporarily</td>
    </tr>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>configFileName</td>
      <td>path to properties file containing controller configs. See [Server](../configuration-reference/server.md) for complete configuration</td>
    </tr>
  </tbody>
</table>

### Start Service Manager

Start multiple Pinot processes with all the default configurations using a single command.

```
pinot-admin.sh StartServiceManager -zkAddress localhost:2181 -clusterName PinotCluster -bootstrapServices CONTROLLER BROKER -bootstrapConfigPaths /path/to/controller.conf /path/to/broker.conf 
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>port</td>
      <td>set to -1 to disable, 0 to run service manager on any available port</td>
    </tr>
    <tr>
      <td>bootstrapConfigPaths</td>
      <td>list of Pinot config file paths. Each config file requires an extra config: `pinot.service.role` to indicate which service to start. The service role can be one of `CONTROLLER`, `BROKER` or `SERVER`</td>
    </tr>
    <tr>
      <td>bootstrapServices</td>
      <td>list of service roles to start with default configurations. For these roles, the default configuration will be taken even if bootstrapConfig is provided.</td>
    </tr>
  </tbody>
</table>

### Show Cluster Info

Show all the available clusters namespaces along with metadata

```
pinot-admin.sh ShowClusterInfo -clusterName PinotCluster -zkAddress localhost:2181
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tables</td>
      <td></td>
    </tr>
    <tr>
      <td>tags</td>
      <td></td>
    </tr>
  </tbody>
</table>

### Stop Process

Stop all the processes of the specified types running on the host.

```
pinot-admin.sh StopProcess -controller -broker -server
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller</td>
      <td>Stop all the controller processes</td>
    </tr>
    <tr>
      <td>broker</td>
      <td>Stop all the broker processes</td>
    </tr>
    <tr>
      <td>server</td>
      <td>Stop all the server processes</td>
    </tr>
    <tr>
      <td>zookeeper</td>
      <td>Stop all the zookeeper process. The process should have been started by pinot admin script otherwise it won't be killed.</td>
    </tr>
    <tr>
      <td>kafka</td>
      <td>Stop all the kafka process. The process should have been started by pinot admin script otherwise it won't be killed.</td>
    </tr>
  </tbody>
</table>

### Upload Segments

Compress and upload segment files to server.

```
pinot-admin.sh UploadSegment -controllerHost localhost -controllerPort 9000 -segmentDir /path/to/local/dir -tableName myTable
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controllerHost</td>
      <td>hostname or ip of the controller</td>
    </tr>
    <tr>
      <td>controllerPort</td>
      <td>port of the controller</td>
    </tr>
    <tr>
      <td>segmentDir</td>
      <td>local directory containing segment files</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>name of the table to push the segments in</td>
    </tr>
  </tbody>
</table>

### Validate Config

Validate the table configs and schema present in Zookeeper.

```
pinot-admin.sh ValidateConfig -clusterName PinotCluster -zkAddress localhost:2181 -tableConfig -tableName mytable myTable2 -schema -schemaNames myschema myschema2
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of Zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tableConfig</td>
      <td>if set, table configs are validated</td>
    </tr>
    <tr>
      <td>tableNames</td>
      <td>space seperated list of table names. By default, all tables are validated</td>
    </tr>
    <tr>
      <td>schema</td>
      <td>if set, schemas are validated</td>
    </tr>
    <tr>
      <td>schemaNames</td>
      <td>space seperated list of schema names. By default, all schemas are validated</td>
    </tr>
  </tbody>
</table>

### Validate Segment

Compares Helix [Ideal state and External view](https://helix.apache.org/Concepts.html) for specified table prefixes.

```
pinot-admin.sh ValidateSegment -tablePrefix myTable -clusterName PinotCluster -zkAddress localhost:2181
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of Zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tablePrefix</td>
      <td>prefix of the table names for which the validation should be done</td>
    </tr>
  </tbody>
</table>

### Verify Cluster State

Verify if all the tables in the cluster have same Ideal State and External View.

```
pinot-admin.sh VerifyClusterState -zkAddress localhost:2181 -clusterName PinotCluster -tableName myTable -timeoutSec 10
```

#### Supported Options

All the options should be prefixed with `-` (hyphen)

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>zkAddress</td>
      <td>comma-separated host:port string of Zookeeper to connect</td>
    </tr>
    <tr>
      <td>clusterName</td>
      <td>name of the cluster to connect to. It can be thought of as a namespace inside zookeeper.</td>
    </tr>
    <tr>
      <td>tableName</td>
      <td>name of the table for which the validation should be done. By default, all tables are verified.</td>
    </tr>
    <tr>
      <td>timeoutSec</td>
      <td>timeout in seconds for the request to check the cluster state.</td>
    </tr>
  </tbody>
</table>
