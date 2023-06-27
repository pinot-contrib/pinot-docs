---
description: >-
  This section contains a collection of short guides to show you how to import
  data from a Pinot-supported file system.
---

# File Systems

FileSystem is an abstraction provided by Pinot to access data stored in distributed file systems (DFS).

Pinot uses distributed file systems for:

* Batch Ingestion Job - To read the input data (CSV, Avro, Thrift, etc.) and to write generated segments to DFS.
* Controller - When a segment is uploaded to the controller, the controller saves it in the configured DFS.
* Server - When a server(s) is notified of a new segment, the server copies the segment from remote DFS to their local node using the DFS abstraction.

## Supported File Systems

Pinot lets you choose a distributed file system provider. The following file systems are supported by Pinot:

* [Amazon S3](amazon-s3.md)
* [Google Cloud Storage](import-from-gcp.md)
* [HDFS](import-from-hdfs.md)
* [Azure Data Lake Storage](import-from-adls-azure.md)

## Enabling a File System

To use a distributed file system, you need to enable plugins. To do that, specify the plugin directory and include the required plugins:

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-plugin-to-include-1,pinot-plugin-to-include-2
```

You can change the filesystem in the `controller` and `server` config as shown here, where `scheme` refers to the prefix used in the URI of the filesystem, such as in the URI `s3://bucket/path/to/file`, where the scheme is `s3`.

```
#CONTROLLER

pinot.controller.storage.factory.class.[scheme]=className of the pinot file system
pinot.controller.segment.fetcher.protocols=file,http,[scheme]
pinot.controller.segment.fetcher.[scheme].class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

```
#SERVER

pinot.server.storage.factory.class.[scheme]=className of the pinot file system
pinot.server.segment.fetcher.protocols=file,http,[scheme]
pinot.server.segment.fetcher.[scheme].class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

You can also change the file system during ingestion. In the ingestion job spec, specify the file system with the following config:

```
pinotFSSpecs
  - scheme: file
    className: org.apache.pinot.spi.filesystem.LocalPinotFS
```
