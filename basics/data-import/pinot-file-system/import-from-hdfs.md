---
description: This guide shows you how to import data from HDFS.
---

# HDFS

You can enable the [Hadoop DFS](https://hadoop.apache.org/) using the plugin `pinot-hdfs`. In the controller or server, add the config -

```text
pinot.controller.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.controller.segment.fetcher.protocols=file,http,hdfs
pinot.controller.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

Azure Blob Storage provides the following options -

* `hadoop.conf.path` : Absolute path of the directory containing hadoop XML configuration files such as hdfs-site.xml .
* `hadoop.write.checksum` : create checksum while pushing an object. Default is `false`

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.hdfs.` where `node` is either `controller` or `server` depending on the config

e.g.

```text
pinot.controller.storage.factory.class.hdfs.hadoop.conf.path=path/to/hdfs.xml
```

