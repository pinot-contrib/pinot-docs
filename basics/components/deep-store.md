---
description: >-
  Learn about the deep store that stores a compressed copy of segment files in
  Pinot.
---

# Deep Store

The deep store (or deep storage) is the permanent store for [segment](segment.md) files.

It is used for backup and restore operations. 
New [server](server.md) nodes in a cluster will pull down a copy of segment files from the deep store.
If the local segment files on a server gets damaged in some way (or accidentally deleted), a new copy will be pulled down from the deep store on server restart.

The deep store stores a compressed version of the segment files and it typically won't include any indexes.
These compressed files can be stored on a local file system or on a variety of other file systems. 
For more details on supported file systems, see [File Systems](../data-import/pinot-file-system/).

For hands-on examples of how to configure the deep store, see the following tutorials:

* [Use OSS as Deep Storage for Pinot](../../users/tutorials/use-oss-as-deep-storage-for-pinot.md)&#x20;
* [Use S3 as Deep Storage for Pinot](../../users/tutorials/use-s3-as-deep-store-for-pinot.md)
