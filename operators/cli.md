# Command-Line Interface \(CLI\)

Pinot provides a rich CLI to perform almost every operation on the cluster. You can execute all the commands using the `pinot-admin.sh`  . The script is located in the `bin/` directory of the [Pinot binary distribution](https://pinot.apache.org/download/) or `/opt/pinot/bin` in docker container.

The following commands are supported by the admin script.

### Add Schema

Upload the schema configuration to controller. If their is already a schema with same name, it will be updated.

```text
pinot-admin.sh AddSchema -schemaFile /path/to/schema.json -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| schemaFile | path to [schema JSON](../configuration-reference/schema.md) file mentioned in table configuration. |
| controllerHost | controllerHost on which to send the upload requests |
| controllerPort | controllerPort on which to send the upload requests |
| exec | If not specified, a dry run will be done but configs won't actually be uploaded.  |

### Add Table

Upload the table configuration to controller.

```text
pinot-admin.sh AddTable -tableConfigFile /path/to/table.json -schemaFile /path/to/schema.json -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| tableConfigFile | path to JSON file containing [Table configuration](../configuration-reference/table.md). |
| schemaFile | path to [schema JSON](../configuration-reference/schema.md) file mentioned in table configuration. |
| controllerHost | controllerHost on which to send the upload requests |
| controllerPort | controllerPort on which to send the upload requests |
| exec | If not specified, a dry run will be done but configs won't actually be uploaded.  |

### Add Tenant

Add a new tenant to the server

```text
pinot-admin.sh AddTenant -name myTenant -role SERVER -instanceCount 10 -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| controllerHost | controllerHost on which to send the upload requests |
| controllerPort | controllerPort on which to send the upload requests |
| name | name of the tenant |
| role | where the tenant should reside. can be `BROKER` or `SERVER` |
| instanceCount | total number of instances to assign to this tenant |
| offlineInstanceCount | \(only applicable for `SERVER`\) total number of instances which can host offline tables belonging to this tenant |
| realTimeInstanceCount | \(only applicable for `SERVER`\)total number of instances which can host realtime tables belonging to this tenant |
| exec | If not specified, a dry run will be done but configs won't actually be uploaded.  |

### Check Offline Segment Intervals

Lists all the segments which have invalid time interval. Only `OFFLINE` segments are supported.

```text
pinot-admin.sh CheckOfflineSegmentIntervals -zkAddress localhost:2181 -clusterName PinotCluster -tableNames myTable
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tableName | Comma separated list of tables to check for invalid segment intervals. By default all tables are checked. |

### Change Num Replicas

This command changes the replicas of the table. The number of replicas are set from the latest available table config.

```text
pinot-admin.sh ChangeNumReplicas -tableNames myTable -clusterName PinotCluster -zkAddress localhost:2181 -exec
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tableNames | name of the table on which to perform operation |
| exec | If not specified, a dry run will be done but configs won't actually be uploaded.  |

### Change Table State

Enable, Disable or Drop the table available in database.

```text
pinot-admin.sh ChangeTableState -

s myTable -state disable -controllerHost localhost -controllerPort 9000 -exec
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| controllerHost | controllerHost on which to send the upload requests |
| controllerPort | controllerPort on which to send the upload requests |
| tableNames | name of the table to modify  |
| state | can be one of `enable` , `disable` or `drop`  |

### Create Segment

Create segment files from the input file in local filesystem. 

```text
pinot-admin.sh CreateSegment -dataDir /path/to/data/dir -format CSV -outDir /path/to/output/dir -overwrite -tableConfigFile /path/to/table.json -schemaConfigFile /path/to/schema.json
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| dataDir | Directory containing input files |
| format | Input data formats. See [Input formats](../basics/data-import/pinot-input-formats.md) for all the supported formats |
| outDir | Local output directory to publish the segments |
| overwrite | Set to `true` to overwrite segments of already present in the directory |
| tableConfigFile | Path to [Table Config](../configuration-reference/table.md) |
| schemaFile | Path to [Schema Config](../configuration-reference/schema.md) |
| readerConfigFile | properties file containing the config related to the reader. See [Input formats](../basics/data-import/pinot-input-formats.md) |
| retry | Number of retry attempts in case of failure |
| postCreationVerification | Set  `true` to verify the segment files post creation.  |
| numThreads | Number of threads to use to execute the segment creation job |

### Convert Pinot Segment

Convert the segment file from Pinot specific format to other data formats. Currently only `CSV`, `AVRO` and `JSON` are supported.

```text
pinot-admin.sh ConvertPinotSegment -dataDir /path/to/data/dir -outputDir /path/to/output/dir -outputFormat CSV -overwrite -csvDelimiter , 
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| dataDir | directory containing the segment files. Only local filePaths are supported |
| outputDir | directory to put the converted segment files in. |
| outputFormat | format to output the files in. Can be one of `CSV`, `AVRO` or `JSON` |
| overwrite | set it to overwrite the files if already present in output directory |
| csvDelimiter | delimiter to use for CSV files. only applicable to `CSV` |
| csvListDelimiter | delimiter to use for list/array in CSV files. only applicable to `CSV` |
| csvWithHeader | set to print CSV header in output file. Default is `false`. |

### Delete Cluster

Delete the cluster namespace from zookeeper.

```text
pinot-admin.sh DeleteCluster -clusterName PinotCluster -zkAddress localhost:2181
```

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| clusterName | name of the cluster to delete |
| zkAddress | Comma seperated host:port list of zookeeper from which to delete the cluster namespace |

### Launch Data Ingestion Job

Run job to consume batch or streaming data and push it to Pinot.

```text
pinot-admin.sh LaunchDataIngestionJob -jobSpecFile /path/to/job_spec.json -propertyFile /path/to/job.properties -values dt=2020-08-10 hour=15
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| jobSpecFile | Path to[ job spec file.](../configuration-reference/job-specification.md) Only local file paths are supported |
| propertyFile | Path to properties file. This file can contain properties related to ingestion job or template paramaters |
| values | list of string containing the values to replace template parameters with  |

### Merge Segments

Merge multiple segment files into a single file. The content of the files is concatenated although the support for Rollup merge is in WIP.

```text
pinot-admin.sh MergeSegments -inputPaths /path/to/dir1 /path/to/dir2 -outputPath /path/to/output/dir -tarOutputSegment -tableConfigFilePaths /path/to/table.json -schemaFilePath /path/to/schema.json
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| inputPaths | input segment files or directories that contains input segments to be merged" |
| ouptutPath | directory in which merged segment file should be put. This should be different from working directory. |
| tableConfigFilePaths | path to table config for which segments are to be merged |
| schemaFilePath | path to schema of the table for which segment should be merged |
| tarOutputSegment | set it to output the compressed .tar.gz segment file |
| mergeType | can be one of `CONCATENATE` or `ROLLUP.` Currently on CONCATENATE is supported |
| workingDirectory | Path for working directory. This directory gets cleaned up after the job. Default is `/tmp` directory |

### Move Replica Group

Command to migrate a subset of replica group from current servers to the provided destination servers. This command is intended to be run multiple times to migrate all the replicas of a table to the destination servers \(if intended\).

```text
pinot-admin.sh MoveReplicaGroup -zkHost localhost:2181 -cluster PinotCluster -srcHosts host1,host2 -destHostsFile /path/to/destination/file -tableName myTable -exec
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| srcHosts | path of the file with all the source hosts or comma seperated list of hostnames |
| destHostsFile | path of the file with all the destination hosts |
| tableNames | name of the table for which replica group is to be moved. Supports only `OFFLINE` tables currently |
| maxSegmentsToMove | maximum number of segments to move. default is `Integer.MAX_VALUE` |
| zkHost | zookeeper host:port string |
| cluster | name of the cluster inside zookeeper .  |
| exec  | set to execute the command. If unset, only a dry run will be done |

### Operate Cluster Config

Modify[ cluster level configs](../configuration-reference/cluster.md) for pinot.  These are the configs which are applicable to all nodes in the cluster.

```text
pinot-admin.sh OperateClusterConfig -controllerHost localhost -controllerPort 9000 -operation ADD -config pinot.broker.enable.query.limit.override=1
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| operation | Type of operation to perform.  Can be one of `GET, ADD, UPDATE or DELETE`  |
| config | The config on which operation should be performed. In case of ADD or UPDATE, the config value is provided after `=`  |
| controllerHost | The host on which to send the request |
| controllerPort | The port on which to send the requests |

### Post Query

Execute a SQL query on the cluster.

```text
pinot-admin.sh PostQuery -brokerHost localhost -brokerPort 8000 -queryType sql -query "SELECT * FROM myTable"
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| brokerHost | broker host to execute the query on |
| brokerPort | broker port to execute the query on |
| queryType | can be one of `sql` or `pql`\(deprecated\). |
| query | SQL query to execute |

### Rebalance Table

Rebalance a table i.e. reassign instances and segments for a table in the cluster. 

For segment reassignment, the following modes are offered:

* `With-downtime rebalance`: the IdealState is replaced with the target segment assignment in one go and there are no guarantees around replica availability. This mode returns immediately without waiting for ExternalView to reach the target segment assignment. Disabled tables will always be rebalanced with downtime.
* `No-downtime rebalance`: care is taken to ensure that the configured number of replicas of any segment are available \(ONLINE or CONSUMING\) at all times. This mode returns after ExternalView reaching the target segment assignment.   In the edge case scenarios mentioned later, if `best-efforts` is disabled, **rebalancer will fail the rebalance because the no-downtime contract cannot be achieved**, and table might end up in a middle stage. User needs to check the rebalance result, solve the issue, and run the rebalance again if necessary.   If `best-efforts` is enabled, rebalancer will log a warning and continue the rebalance, but the no-downtime contract will not be guaranteed.  Downtime can occur in the following edge case scenarios - 
  * Segment falls into ERROR state in ExternalView -&gt; with best-efforts, count ERROR state as good state. 
  * ExternalView has not converged within the maximum wait time -&gt; with best-efforts, continue to the next stage

{% hint style="danger" %}
**If the controller that handles the rebalance goes down/restarted, the rebalance isn't automatically resumed by other controllers**
{% endhint %}

```text
pinot-admin.sh RebalanceTable -zkAddress localhost:2181 -clusterName PinotCluster -tableName myTable -reassignInstances -includeConsuming -downtime  
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tableNames | name of the table on which to perform operation |
| reassignInstances | set to reassign instances before reassigning segments \(`false` by default\) |
| includeConsuming | set to reassign `CONSUMING` segments for real-time table \(`false` by default\) |
| bootstrap | set to rebalance table in bootstrap mode \(regardless of minimum segment movement, reassign all segments in a round-robin fashion as if adding new segments to an empty table, `false` by default\) |
| downtime | Set to allow downtime for the rebalance \(`false` by default\) |
| minAvailableReplicas | minimum number of replicas to keep alive during rebalance, or maximum number of replicas allowed to be unavailable if value is negative \(default is 1\), Only applicable if downtime is set to `false` |
| bestEfforts | set to use best-efforts to rebalance i.e. not fail the rebalance when the no-downtime contract cannot be achieved, `false` by default |

### Start Broker

Start a broker instance on host

```text
pinot-admin.sh StartBroker -zkAddress localhost:2181 -clusterName PinotCluster -configFileName /path/to/broker.conf
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| brokerHost | hostname of the instance on which to run the broker |
| brokerPort | port on which the broker should listen. Default 8099. |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| configFileName | path to properties file containing controller configs. See [Broker](../configuration-reference/broker.md) for complete configuration |

### Start Controller

Start a controller instance on host

```text
pinot-admin.sh StartController -controllerMode helix_only -dataDir /path/to/data/dir -zkAddress localhost:2181 -clusterName PinotCluster -configFileName /path/to/controller.conf
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| controllerMode | Should be one of `dual`, `pinot_only` or `helix_only`. Default is `dual` |
| controllerHost | hostname of the instance on which to run the controller |
| controllerPort | port on which the controller should listen. Default 9000. |
| dataDir | path to directory to store data. Default is `java.io.tmpDir` +  `PinotController` |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| configFileName | path to properties file containing controller configs. See [Controller](../configuration-reference/controller.md) for complete configuration |

### Start Server

Start a server instance on host

```text
pinot-admin.sh StartServer -dataDir /path/to/data/dir -zkAddress localhost:2181 -clusterName PinotCluster -configFileName /path/to/server.conf
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| serverHost | hostname of the instance on which to run the broker |
| serverPort | port on which the broker should listen. Default 8099. |
| serverAdminPort | port on which admin API should be available. Default it 8097 |
| dataDir | directory in which to store the data |
| segmentDir | directory in which to download the .tar segment files temporarily |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| configFileName | path to properties file containing controller configs. See [Server](../configuration-reference/server.md) for complete configuration |

### Start Service Manager

Start multiple Pinot process with all the default configuration using single command.

```text
pinot-admin.sh StartBroker -zkAddress localhost:2181 -clusterName PinotCluster -bootstrapServices CONTROLLER BROKER -bootstrapConfigPaths /path/to/controller.conf /path/to/broker.conf 
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| port | set to -1 to disable, 0 to run service manager on any available port |
| bootstrapConfigPaths | list of Pinot config file paths. Each config file requires an extra config: `pinot.service.role` to indicate which service to start. The service role can be one of `CONTROLLER`, `BROKER` or `SERVER` |
| bootstrapServices | list of service roles to start with default configurations. For these roles, the default configuration will be taken even if bootstrapConfig is provided. |

### Show Cluster Info

Show all the available clusters namespaces along with metadata

```text
pinot-admin.sh ShowClusterInfo -clusterName PinotCluster -zkAddress localhost:2181
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tables |  |
| tags |  |

### Stop Process

Stop all the processes of the specified types running on the host.

```text
pinot-admin.sh StopProcess -controller -broker -server
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| controller | Stop all the controller processes |
| broker | Stop all the broker processes |
| server | Stop all the server processes |
| zookeeper | Stop all the zookeeper process. The process should have been started by pinot admin script otherwise it won't be killed. |
| kafka | Stop all the kafka process. The process should have been started by pinot admin script otherwise it won't be killed. |

### Upload Segments

Compress and upload segment files to server.

```text
pinot-admin.sh UploadSegment -controllerHost localhost -controllerPort 9000 -segmentDir /path/to/local/dir -tableName myTable
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| controllerHost | hostname or ip of the controller |
| controllerPort | port of the controller |
| segmentDir | local directory containing segment files |
| tableNames | name of the table to push the segments in |

### Validate Config

Validate the table configs and schema present in Zookeeper. 

```text
pinot-admin.sh ValidateConfig -clusterName PinotCluster -zkAddress localhost:2181 -tableConfig -tableNames mytable myTable2 -schema -schemaNames myschema myschema2
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tableConfig | if set, table configs are validated |
| tableNames | space seperated list of table names. By default, all tables are validated |
| schema | if set, schemas are validated |
| schemaNames | space seperated list of schema names. By default, all schemas are validated |

### Validate Segment

Compares Helix [Ideal state and External view](https://helix.apache.org/Concepts.html) for specified table prefixes. 

```text
pinot-admin.sh ValidateSegment -tablePrefix myTable -clusterName PinotCluster -zkAddress localhost:2181
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tablePrefix | prefix of the table names for which the validation should be done |

### Verify Cluster State

Verify if all the tables in the cluster have same Ideal State and External View.

```text
pinot-admin.sh VerifyClusterState -zkAddress localhost:2181 -clusterName PinotCluster -tableNames myTable -timeoutSec 10
```

#### Supported Options

All the options should be prefixed with `-` \(hyphen\) 

| Option | Description |
| :--- | :--- |
| zkAddress | comma seperated host:port string of zookeeper to connect |
| clusterName | name of the cluster to connect to. It can be thought of as a namespace inside zookeeper. |
| tableNames | name of the table for which the validation should be done.  By default, all tables are verified. |
| timeoutSec | timeout in seconds for the request to check the cluster state. |

 

