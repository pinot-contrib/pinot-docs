---
description: Troubleshoot issues with Zookeeper znodes.
---

# Troubleshoot issues with Zookeeper

Pinot stores cluster metadata, including schema definitions, table configuration, and segment assignment, in ZooKeeper.
Internally, Zookeeper uses a hierarchical namespace, similar to a file system.
The nodes in this hierarchy are called znodes and they can store data and have child nodes.

The default maximum size of znodes is 1MB, which is sufficient for most deployments.
However, if you have 100s of thousands of segments, it's possible that this size limit is exceeded.
If this happens, you will see an error message similar to the following:

```text
java.io.ioexception: packet len 1250829 is out of range!
```

To address the size limit is exceeded error, do the following:
- Reduce the number of segments
- Adjust ZooKeeper znode size

## Reduce the number of segments

The first way is to reduce the number of segments, which will reduce the amount of metadata that's stored in the `IDEALSTATE` and `EXTERNALVIEW` znodes, which are the two znodes most likely to exceed 1MB.

For new segments this is done by configuring the [segment threshold](segment-threshold.md) to a higher value.
For existing segments, we'll need to run the [Minion merge rollup task](../recipes/merge-segments-realtime.md).

## Adjust Zookeeper znode size

Adjust the maximum size of znodes in ZooKeeper.
To do this, configure the `jute.maxbuffer` Java system property, which defines the maximum znode size in bytes.
To read more about this property, see the [ZooKeeper documentation](https://zookeeper.apache.org/doc/r3.6.2/zookeeperAdmin.html).

We recommend setting this value to 4MB. Set this parameter to the same value on the ZooKeeper node and clients that are interacting with ZooKeeper (all Pinot components).