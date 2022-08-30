---
description: FAQ for general questions around Pinot
---

# General

## How does Pinot use deep storage?

When data is pushed in to Pinot, it makes a backup copy of the data and stores it on the configured deep-storage (S3/GCP/ADLS/NFS/etc). This copy is stored as tar.gz Pinot segments. Note, that pinot servers keep a (untarred) copy of the segments on their local disk as well. This is done for performance reasons.

## How does Pinot use Zookeeper?

Pinot uses Apache Helix for cluster management, which in turn is built on top of Zookeeper. Helix uses Zookeeper to store the cluster state, including Ideal State, External View, Participants, etc. Besides that, Pinot uses Zookeeper to store other information such as Table configs, schema, Segment Metadata, etc.

## Why am I getting "Could not find or load class" error when running Quickstart using 0.8.0 release?

Please check the JDK version you are using. The release 0.8.0 binary is on JDK 11. You may be getting this error if you are using JDK8. In that case, please consider using JDK11, or you will need to download the [source code](https://downloads.apache.org/pinot/apache-pinot-0.8.0/apache-pinot-0.8.0-src.tar.gz) for the release and [build](https://github.com/apache/pinot/pull/6424) it locally.

