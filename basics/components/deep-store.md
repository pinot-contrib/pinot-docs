---
description: >-
  Learn about the deep store that stores a compressed copy of segment files in
  Pinot.
---

# Deep Store

Pinot keeps a compressed copy of segment files in the deep store (or deep storage).

These compressed files can be stored on a local file system or on a variety of other file systems. For more details on supported file systems, see [File Systems](../data-import/pinot-file-system/README.md).

For hands on examples of how to configure the deep store, see the following tutorials:

*[Use OSS as Deep Storage for Pinot](../../users/tutoirals/use-oss-as-deep-storage-for-pinot.md)
*[Use S3 as Deep Storage for Pinot](../../users/tutoirals/use-s3-as-deep-store-for-pinot.md)