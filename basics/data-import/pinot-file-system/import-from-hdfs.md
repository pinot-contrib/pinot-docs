---
description: This guide shows you how to import data from HDFS.
---

# HDFS

You can enable the [Hadoop DFS](https://hadoop.apache.org/) using the plugin `pinot-hdfs`. In the controller or server, add the config -

```text
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-hdfs
```

Azure Blob Storage provides the following options -

* `hadoop.conf.path` : Absolute path of the directory containing hadoop XML configuration files such as **hdfs-site.xml, core-site.xml** .
* `hadoop.write.checksum` : create checksum while pushing an object. Default is `false`

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.hdfs.` where `node` is either `controller` or `server` depending on the config

e.g.

```text
pinot.controller.storage.factory.class.hdfs.hadoop.conf.path=path/to/hdfs.xml
```

### Examples

#### Job spec

```yaml
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: 'hdfs:///path/to/input/directory/'
outputDirURI: 'hdfs:///path/to/output/directory/'
overwriteOutput: true
pinotFSSpecs:
    - scheme: hdfs
      className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
      configs:
        hadoop.conf.path: 'path/to/conf/directory/' 
recordReaderSpec:
    dataFormat: 'csv'
    className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
    configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
    tableName: 'students'
pinotClusterSpecs:
    - controllerURI: 'http://localhost:9000'
```

#### Controller config

```text
pinot.controller.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.controller.storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory/
pinot.controller.segment.fetcher.protocols=file,http,hdfs
pinot.controller.segment.fetcher.adl.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Server config

```text
pinot.server.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.server.storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory/
pinot.server.segment.fetcher.protocols=file,http,hdfs
pinot.server.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### 



