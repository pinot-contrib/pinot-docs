---
description: This guide shows you how to import data from HDFS.
---

# Hadoop DFS

Enable the [Hadoop distributed file system (HDFS)](https://hadoop.apache.org/) using the `pinot-hdfs` plugin. In the controller or server, add the config:

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-hdfs
```

{% hint style="info" %}
By default Pinot loads all the plugins, so you can just drop this plugin there. Also, if you specify `-Dplugins.include`, you need to put all the plugins you want to use, e.g. `pinot-json`, `pinot-avro` , `pinot-kafka-2.0...`
{% endhint %}

HDFS implementation provides the following options:

* `hadoop.conf.path`: Absolute path of the directory containing Hadoop XML configuration files, such as **hdfs-site.xml, core-site.xml** .
* `hadoop.write.checksum`: Create checksum while pushing an object. Default is `false`
* `hadoop.kerberos.principle`
* `hadoop.kerberos.keytab`

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.hdfs.` where `node` is either `controller` or `server` depending on the config

The `kerberos` configs should be used only if your Hadoop installation is secured with Kerberos. Refer to the [Hadoop in secure mode documentation](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SecureMode.html) for information on how to secure Hadoop using Kerberos.

You must provide proper Hadoop dependencies jars from your Hadoop installation to your Pinot startup scripts.

```
export HADOOP_HOME=/local/hadoop/
export HADOOP_VERSION=2.7.1
export HADOOP_GUAVA_VERSION=11.0.2
export HADOOP_GSON_VERSION=2.2.4
export CLASSPATH_PREFIX="${HADOOP_HOME}/share/hadoop/hdfs/hadoop-hdfs-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-annotations-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-auth-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/hadoop-common-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/guava-${HADOOP_GUAVA_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/gson-${HADOOP_GSON_VERSION}.jar"
```

## Push HDFS segment to Pinot Controller

To push HDFS segment files to Pinot controller, send the HDFS path of your newly created segment files to the Pinot Controller. The controller will download the files.

This curl example requests tells the controller to download segment files to the proper table:

```
curl -X POST -H "UPLOAD_TYPE:URI" -H "DOWNLOAD_URI:hdfs://nameservice1/hadoop/path/to/segment/file.
```

## Examples

### Job spec

Standalone Job:

```yaml
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: 'hdfs:///path/to/input/directory/'
outputDirURI: 'hdfs:///path/to/output/directory/'
includeFileNamePath: 'glob:**/*.csv'
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

Hadoop Job:

```yaml
executionFrameworkSpec:
    name: 'hadoop'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentUriPushJobRunner'
    extraConfigs:
      stagingDir: 'hdfs:///path/to/staging/directory/'
jobType: SegmentCreationAndTarPush
inputDirURI: 'hdfs:///path/to/input/directory/'
outputDirURI: 'hdfs:///path/to/output/directory/'
includeFileNamePath: 'glob:**/*.csv'
overwriteOutput: true
pinotFSSpecs:
    - scheme: hdfs
      className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
      configs:
        hadoop.conf.path: '/etc/hadoop/conf/' 
recordReaderSpec:
    dataFormat: 'csv'
    className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
    configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
    tableName: 'students'
pinotClusterSpecs:
    - controllerURI: 'http://localhost:9000'
```

### Controller config

```
controller.data.dir=hdfs://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.controller.storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory/
pinot.controller.segment.fetcher.protocols=file,http,hdfs
pinot.controller.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
```

### Server config

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.server.storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory/
pinot.server.segment.fetcher.protocols=file,http,hdfs
pinot.server.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
pinot.server.segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
pinot.server.segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
```

### Minion config

```
storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory
segment.fetcher.protocols=file,http,hdfs
segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
```
