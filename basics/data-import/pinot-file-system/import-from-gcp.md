---
description: This guide shows you how to import data from GCP (Google Cloud Platform).
---

# Google Cloud Storage

You can enable the [Google Cloud Storage](https://cloud.google.com/products/storage/) using the plugin `pinot-gcs`. In the controller or server, add the config -

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-gcs
```

{% hint style="info" %}
By default Pinot loads all the plugins, so you can just drop this plugin there. Also, if you specify `-Dplugins.include`, you need to put all the plugins you want to use, e.g. `pinot-json`, `pinot-avro `, `pinot-kafka-2.0...`
{% endhint %}

GCP filesystems provides the following options -

* `projectId` - The name of the Google Cloud Platform project under which you have created your storage bucket.
* `gcpKey` - Location of the json file containing GCP keys. You can refer [Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) to download the keys.

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.gs.` where `node` is either `controller` or `server` depending on the config

e.g.

```
pinot.controller.storage.factory.class.gs.projectId=test-project
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
inputDirURI: 'gs://my-bucket/path/to/input/directory/'
outputDirURI: 'gs://my-bucket/path/to/output/directory/'
overwriteOutput: true
pinotFSSpecs:
    - scheme: gs
      className: org.apache.pinot.plugin.filesystem.GcsPinotFS
      configs:
        projectId: 'my-project'
        gcpKey: 'path-to-gcp json key file'
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
controller.data.dir=gs://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.gs=org.apache.pinot.plugin.filesystem.GcsPinotFS
pinot.controller.storage.factory.gs.projectId=my-project
pinot.controller.storage.factory.gs.gcpKey=path/to/gcp/key.json
pinot.controller.segment.fetcher.protocols=file,http,gs
pinot.controller.segment.fetcher.gs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Server config

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.gs=org.apache.pinot.plugin.filesystem.GcsPinotFS
pinot.server.storage.factory.gs.projectId=my-project
pinot.server.storage.factory.gs.gcpKey=path/to/gcp/key.json
pinot.server.segment.fetcher.protocols=file,http,gs
pinot.server.segment.fetcher.gs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Minion config

```
storage.factory.class.gs=org.apache.pinot.plugin.filesystem.GcsPinotFS
storage.factory.gs.projectId=my-project
storage.factory.gs.gcpKey=path/to/gcp/key.json
segment.fetcher.protocols=file,http,gs
segment.fetcher.gs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```
