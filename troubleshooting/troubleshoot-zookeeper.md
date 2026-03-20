---
description: Troubleshoot issues with Zookeeper znodes.
---

# Troubleshoot issues with ZooKeeper znodes

Pinot stores cluster metadata, including schema definitions, table configuration, and segment assignment, in ZooKeeper. Internally, Zookeeper uses a hierarchical namespace, similar to a file system. The nodes in this hierarchy are called znodes and they can store data and have child nodes.

The default maximum size of znodes is 1MB, which is sufficient for most deployments. However, if you have 100s of thousands of segments, it's possible that this size limit is exceeded. If this happens, you will see an error message similar to the following:

```
java.io.ioexception: packet len 1250829 is out of range!
```

To address the size limit is exceeded error, do the following:

* Reduce the number of segments
* Adjust ZooKeeper znode size

## Reduce the number of segments

Reduce the number of segments to reduce the metadata stored in the `IDEALSTATE` and `EXTERNALVIEW` znodes, which are the two znodes most likely to exceed 1MB.

To do this for new segments, configure the [segment threshold](../basics/concepts/segment-threshold.md) to a higher value. For existing segments, run the [Minion merge rollup task](../operators/operating-pinot/minion-merge-rollup-task.md).

## Adjust Zookeeper znode size

Adjust the maximum size of znodes in ZooKeeper. To do this, configure the `jute.maxbuffer` Java system property, which defines the maximum znode size in bytes. To read more about this property, see the [ZooKeeper documentation](https://zookeeper.apache.org/doc/r3.6.2/zookeeperAdmin.html).

We recommend setting this value to 4MB.&#x20;

Set this parameter to all ZooKeeper node first then restart all the ZooKeeper nodes.

After this, we need to set the JVM Opt: `-Djute.maxbuffer=4000000` in all the pinot components, then restart all the Pinot components to allow Pinot interacts with ZooKeeper using larger jute buffer size.
