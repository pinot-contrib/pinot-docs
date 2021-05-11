---
description: FAQ for general questions around Pinot
---

# General

## How does Pinot use deep storage?

When data is pushed in to Pinot, it makes a backup copy of the data and stores it on the configured deep-storage \(S3/GCP/ADLS/NFS/etc\). This copy is stored as tar.gz Pinot segments. Note, that pinot servers keep a \(untarred\) copy of the segments on their local disk as well. This is done for performance reasons.





