---
description: >-
  This guide shows you how to import data from files stored in Azure Data Lake
  Storage Gen2 (ADLS Gen2)
---

# Azure Data Lake Storage

Enable the Azure Data Lake Storage using the `pinot-adls` plugin. In the controller or server, add the config:

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-adls
```

{% hint style="info" %}
By default Pinot loads all the plugins, so you can just drop this plugin there. Also, if you specify `-Dplugins.include`, you need to put all the plugins you want to use, e.g. `pinot-json`, `pinot-avro` , `pinot-kafka-2.0...`
{% endhint %}

Azure Blob Storage provides the following options:

* `accountName`: Name of the Azure account under which the storage is created.
* `accessKey`: Access key required for the authentication.
* `fileSystemName`: Name of the file system to use, for example, the container name (similar to the bucket name in S3).
* `enableChecksum`: Enable MD5 checksum for verification. Default is `false`.

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.adl2.` where `node` is either `controller` or `server` depending on the config, like this:

```
pinot.controller.storage.factory.class.adl2.accountName=test-user
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
inputDirURI: 'adl2://path/to/input/directory/'
outputDirURI: 'adl2://path/to/output/directory/'
overwriteOutput: true
pinotFSSpecs:
    - scheme: adl2
      className: org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
      configs:
        accountName: 'my-account'
        accessKey: 'foo-bar-1234'
        fileSystemName: 'fs-name'
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

```
controller.data.dir=adl2://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.adl2=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
pinot.controller.storage.factory.adl2.accountName=my-account
pinot.controller.storage.factory.adl2.accessKey=foo-bar-1234
pinot.controller.storage.factory.adl2.fileSystemName=fs-name
pinot.controller.segment.fetcher.protocols=file,http,adl2
pinot.controller.segment.fetcher.adl2.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Server config

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.adl2=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
pinot.server.storage.factory.adl2.accountName=my-account
pinot.server.storage.factory.adl2.accessKey=foo-bar-1234
pinot.controller.storage.factory.adl2.fileSystemName=fs-name
pinot.server.segment.fetcher.protocols=file,http,adl2
pinot.server.segment.fetcher.adl2.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Minion config

```
storage.factory.class.adl2=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
storage.factory.adl2.accountName=my-account
storage.factory.adl2.fileSystemName=fs-name
storage.factory.adl2.accessKey=foo-bar-1234
segment.fetcher.protocols=file,http,adl2
segment.fetcher.adl2.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```
