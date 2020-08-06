---
description: This guide shows you how to import data from GCP (Google Cloud Platform).
---

# Google Cloud Storage

You can enable the [Google Cloud Storage](https://cloud.google.com/products/storage/) using the plugin `pinot-gcs`. In the controller or server, add the config -

```text
pinot.controller.storage.factory.class.gs=org.apache.pinot.plugin.filesystem.GcsPinotFS
pinot.controller.segment.fetcher.protocols=file,http,gs
pinot.controller.segment.fetcher.gs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

GCP filesystems provides the following options -

* `projectId` - The name of the Google Cloud Platform project under which you have created your storage bucket.
* `gcpKey` - Location of the json file containing GCP keys. You can refer [Creating and managing service account keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) to download the keys.

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.gs.` where `node` is either `controller` or `server` depending on the config

e.g.

```text
pinot.controller.storage.factory.class.gs.projectId=test-project
```



