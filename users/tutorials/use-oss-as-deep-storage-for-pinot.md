---
description: Configure AliCloud Object Storage Service (OSS) as Pinot deep storage
---

# Use OSS as Deep Storage for Pinot

OSS can be used as HDFS deep storage for Apache Pinot without implement OSS file system plugin. You should follow the steps below;\
\
**1.** Configure _**hdfs-site.xml**_ and _**core-site.xml**_ files. After that, put these configurations under any path, then set the value of `pinot.<node>.storage.factory.oss.hadoop.conf` config on the controller/server configs to this path.

For **hdfs-site.xml**; you do not have to give any configuration;

```
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
</configuration>
```

For **core-site.xml**; you have to give OSS access/secret and bucket configurations like below;

```
<?xml version="1.0"?>
<configuration>
    <property>
	      <name>fs.defaultFS</name>
	      <value>oss://your-bucket-name/</value>
	  </property>
    <property>
        <name>fs.oss.accessKeyId</name>
        <value>your-access-key-id</value>
    </property>
    <property>
        <name>fs.oss.accessKeySecret</name>
        <value>your-access-key-secret</value>
    </property>
    <property>
        <name>fs.oss.impl</name>
        <value>com.aliyun.emr.fs.oss.OssFileSystem</value>
    </property>
    <property>
        <name>fs.oss.endpoint</name>
        <value>your-oss-endpoint</value>
    </property>
</configuration>
```

**2.** In order to access OSS, find your HDFS jars related to OSS and put them under the `PINOT_DIR/lib`. You can use jars below but be careful about versions to avoid conflict.

* smartdata-aliyun-oss&#x20;
* smartdata-hadoop-common
* guava

**3.** Set OSS deep storage configs on **controller.conf** and **server.conf**;

**Controller config**

```
controller.data.dir=oss://your-bucket-name/path/to/segments
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.oss=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.controller.storage.factory.oss.hadoop.conf.path=path/to/conf/directory/
pinot.controller.segment.fetcher.protocols=file,http,oss
pinot.controller.segment.fetcher.oss.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

**Server config**

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.oss=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.server.storage.factory.oss.hadoop.conf.path=path/to/conf/directory/
pinot.server.segment.fetcher.protocols=file,http,oss
pinot.server.segment.fetcher.oss.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

**Example Job Spec**

Using the same HDFS deep storage configs and jars, you can read data from OSS, then create segments and push them to OSS again. An example standalone batch ingestion job can be like below;

```
executionFrameworkSpec:
  name: 'standalone'
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentMetadataPushJobRunner'
jobType: SegmentCreationAndMetadataPush
inputDirURI: 'oss://your-bucket-name/input'
includeFileNamePattern: 'glob:**/*.csv'
outputDirURI: 'oss://your-bucket-name/output'
overwriteOutput: true
pinotFSSpecs:
  - scheme: oss
    className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
    configs:
      hadoop.conf.path: '/path/to/hadoop/conf'
recordReaderSpec:
  dataFormat: 'csv'
  className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
  configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
  tableName: 'transcript'
pinotClusterSpecs:
  - controllerURI: '<http://localhost:9000>'

```
