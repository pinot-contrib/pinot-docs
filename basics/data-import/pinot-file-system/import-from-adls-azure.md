---
description: >-
  This guide shows you how to import data from files stored in Azure Data Lake
  Storage (ADLS)
---

# Azure Data Lake Storage

You can enable the Azure Data Lake Storage using the plugin `pinot-adls`. In the controller or server, add the config -

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-adls
```

{% hint style="info" %}
By default Pinot loads all the plugins, so you can just drop this plugin there. Also, if you specify `-Dplugins.include`, you need to put all the plugins you want to use, e.g. `pinot-json`, `pinot-avro `, `pinot-kafka-2.0...`
{% endhint %}

Azure Blob Storage provides the following options -

* `accountName` : Name of the azure account under which the storage is created
* `accessKey` : access key required for the authentication
* `fileSystemName` - name of the filesystem to use i.e. container name (container name is similar to bucket name in S3)
* `enableChecksum` - enable MD5 checksum for verification. Default is `false`.

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.abfss.` where `node` is either `controller` or `server` depending on the config

e.g.

```
pinot.controller.storage.factory.class.adl.accountName=test-user
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
inputDirURI: 'adl://path/to/input/directory/'
outputDirURI: 'adl://path/to/output/directory/'
overwriteOutput: true
pinotFSSpecs:
    - scheme: adl
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
controller.data.dir=adl://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.adl=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
pinot.controller.storage.factory.adl.accountName=my-account
pinot.controller.storage.factory.adl.accessKey=foo-bar-1234
pinot.controller.storage.factory.adl.fileSystemName=fs-name
pinot.controller.segment.fetcher.protocols=file,http,adl
pinot.controller.segment.fetcher.adl.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Server config

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.adl=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
pinot.server.storage.factory.adl.accountName=my-account
pinot.server.storage.factory.adl.accessKey=foo-bar-1234
pinot.controller.storage.factory.adl.fileSystemName=fs-name
pinot.server.segment.fetcher.protocols=file,http,adl
pinot.server.segment.fetcher.adl.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Minion config

```
storage.factory.class.adl=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
storage.factory.adl.accountName=my-account
storage.factory.adl.fileSystemName=fs-name
storage.factory.adl.accessKey=foo-bar-1234
segment.fetcher.protocols=file,http,adl
segment.fetcher.adl.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

