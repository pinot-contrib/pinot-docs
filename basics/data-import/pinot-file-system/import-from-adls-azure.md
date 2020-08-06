---
description: >-
  This guide shows you how to import data from files stored in Azure Data Lake
  Storage (ADLS)
---

# Azure Data Lake Storage

You can enable the Azure Data Lake Storage using the plugin `pinot-adls`. In the controller or server, add the config -

```text
pinot.controller.storage.factory.class.abfss=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
pinot.controller.segment.fetcher.protocols=file,http,abfss
pinot.controller.segment.fetcher.abfss.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

Azure Blob Storage provides the following options -

* `accountName` : Name of the azure account under which the storage is created
* `accessKey` : access key required for the authentication
* `fileSystemName` - name of the filesystem to use
* `enableChecksum` - enable MD5 checksum for verification. Default is `false`.

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.abfss.` where `node` is either `controller` or `server` depending on the config

e.g.

```text
pinot.controller.storage.factory.class.abfss.accountName=test-user
```

#### 



