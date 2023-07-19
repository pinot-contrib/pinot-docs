---
description: >-
  This page has a collection of frequently asked questions of a general nature with answers from the
  community.
---

# General

{% hint style="info" %}
This is a list of questions frequently asked in our troubleshooting channel on Slack. To contribute additional questions and answers, [make a pull request](https://docs.pinot.apache.org/contributing/contributing).
{% endhint %}

## How does Apache Pinot use deep storage?

When data is pushed to Apache Pinot, Pinot makes a backup copy of the data and stores it on the configured deep-storage (S3/GCP/ADLS/NFS/etc). This copy is stored as tar.gz Pinot segments. Note, that Pinot servers keep a (untarred) copy of the segments on their local disk as well. This is done for performance reasons.

## How does Pinot use Zookeeper?

Pinot uses Apache Helix for cluster management, which in turn is built on top of Zookeeper. Helix uses Zookeeper to store the cluster state, including Ideal State, External View, Participants, and so on. Pinot also uses Zookeeper to store information such as Table configurations, schemas, Segment Metadata, and so on.

## Why am I getting "Could not find or load class" error when running Quickstart using 0.8.0 release?

Please check the JDK version you are using.  You may be getting this error if you are using an older version than the current Pinot binary release was built on. If so, you have two options: switch to the same JDK release as Pinot was built with or download the [source code](https://downloads.apache.org/pinot/apache-pinot-0.8.0/apache-pinot-0.8.0-src.tar.gz) for the Pinot release and [build](https://github.com/apache/pinot/pull/6424) it locally.
