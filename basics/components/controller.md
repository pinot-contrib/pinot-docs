---
description: >-
  Discover the controller component of Apache Pinot, enabling efficient data and
  query management.
---

# Controller

The Pinot controller is responsible for the following:

* Maintaining **global metadata** (e.g., configs and schemas) of the system with the help of Zookeeper which is used as the persistent metadata store.
* Hosting the **Helix Controller** and managing other Pinot components (brokers, servers, minions)&#x20;
* Maintaining the **mapping of which servers are responsible for which segments**. This mapping is used by the servers to download the portion of the segments that they are responsible for. This mapping is also used by the broker to decide which servers to route the queries to.
* Serving **admin endpoints** for viewing, creating, updating, and deleting configs, which are used to manage and operate the cluster.
* Serving endpoints for **segment uploads**, which are used in offline data pushes. They are responsible for initializing **real-time consumption** and coordination of persisting real-time segments into the segment store periodically.
* Undertaking other **management activities** such as managing retention of segments, validations.

For redundancy, there can be multiple instances of Pinot controllers. Pinot expects that all controllers are configured with the same back-end storage system so that they have a common view of the segments (_e.g._ NFS). Pinot can use other storage systems such as HDFS or [ADLS](https://azure.microsoft.com/en-us/services/storage/data-lake-storage/).

## Controller periodic tasks

The controller runs several periodic tasks in the background, to perform activities such as management and validation. Each periodic task has its own configs to define the run frequency and default frequency. Each task runs at its own schedule or can also be triggered manually if needed. The task runs on the lead controller for each table.

Here's a list of all the periodic tasks

### BrokerResourceValidationManager

This task rebuilds the BrokerResource if the instance set has changed.

| Config                                                      | Default Value |
| ----------------------------------------------------------- | ------------- |
| controller.broker.resource.validation.frequencyPeriod       | 1h            |
| controller.broker.resource.validation.initialDelayInSeconds | between 2m-5m |

### StaleInstancesCleanupTask

This task periodically cleans up stale Pinot broker/server/minion instances.

| Config                                                                     | Default Value |
| -------------------------------------------------------------------------- | ------------- |
| controller.stale.instances.cleanup.task.frequencyPeriod                    | 1h            |
| controller.stale.instances.cleanup.task.initialDelaySeconds                | between 2m-5m |
| controller.stale.instances.cleanup.task.minOfflineTimeBeforeDeletionPeriod | 1h            |

### OfflineSegmentIntervalChecker

This task manages the segment ValidationMetrics (missingSegmentCount, offlineSegmentDelayHours, lastPushTimeDelayHours, TotalDocumentCount, NonConsumingPartitionCount, SegmentCount), to ensure that all offline segments are contiguous (no missing segments) and that the offline push delay isn't too high.

| Config                                                         | Default Value |
| -------------------------------------------------------------- | ------------- |
| controller.offline.segment.interval.checker.frequencyPeriod    | 24h           |
| controller.statuschecker.waitForPushTimePeriod                 | 10m           |
| controller.offlineSegmentIntervalChecker.initialDelayInSeconds | between 2m-5m |

### PinotTaskManager

TBD

### RealtimeSegmentValidationManager

This task validates the ideal state and segment zk metadata of real-time tables by doing the following:&#x20;

* fixing any partitions which have stopped consuming
* starting consumption from new partitions
* uploading segments to deep store if segment download url is missing

This task ensures that the consumption of the real-time tables gets fixed and keeps going when met with erroneous conditions.

{% hint style="danger" %}
This task does not fix consumption stalled due to

* CONSUMING segment being deleted
* Kafka OOR exceptions
{% endhint %}

| Config                                                       | Default Value |
| ------------------------------------------------------------ | ------------- |
| controller.realtime.segment.validation.frequencyPeriod       | 1h            |
| controller.realtime.segment.validation.initialDelayInSeconds | between 2m-5m |

### RetentionManager

This task manages retention of segments for all tables. During the run, it looks at the `retentionTimeUnit` and `retentionTimeValue` inside the `segmentsConfig` of every table, and deletes segments which are older than the retention. The deleted segments are moved to a DeletedSegments folder colocated with the dataDir on segment store, and permanently deleted from that folder in a configurable number of days.

| Config                                            | Default Value |
| ------------------------------------------------- | ------------- |
| controller.retention.frequencyPeriod              | 6h            |
| controller.retentionManager.initialDelayInSeconds | between 2m-5m |
| controller.deleted.segments.retentionInDays       | 7d            |

### SegmentRelocator

This task is applicable only if you have tierConfig or tagOverrideConfig. It runs rebalance in the background to

1. relocate COMPLETED segments to tag overrides
2. relocate ONLINE segments to tiers if tier configs are set&#x20;

At most one replica is allowed to be unavailable during rebalance.

| Config                                            | Default Value |
| ------------------------------------------------- | ------------- |
| controller.segment.relocator.frequencyPeriod      | 1h            |
| controller.segmentRelocator.initialDelayInSeconds | between 2m-5m |

### SegmentStatusChecker

This task manages segment status metrics such as realtimeTableCount, offlineTableCount, disableTableCount, numberOfReplicas, percentOfReplicas, percentOfSegments, idealStateZnodeSize, idealStateZnodeByteSize, segmentCount, segmentsInErrorState, tableCompressedSize.

| Config                                         | Default Value |
| ---------------------------------------------- | ------------- |
| controller.statuschecker.frequencyPeriod       | 5m            |
| controller.statusChecker.initialDelayInSeconds | between 2m-5m |

### TaskMetricsEmitter

TBD

## Running the periodic task manually

Use the `GET /periodictask/names` API to fetch the names of all the Periodic Tasks running on your Pinot cluster.

```
curl -X GET "http://localhost:9000/periodictask/names" -H "accept: application/json"

[
  "RetentionManager",
  "OfflineSegmentIntervalChecker",
  "RealtimeSegmentValidationManager",
  "BrokerResourceValidationManager",
  "SegmentStatusChecker",
  "SegmentRelocator",
  "StaleInstancesCleanupTask",
  "TaskMetricsEmitter"
]
```

To manually run a named Periodic task, use the `GET /periodictask/run` API

```
curl -X GET "http://localhost:9000/periodictask/run?taskname=SegmentStatusChecker&tableName=jsontypetable&type=OFFLINE" -H "accept: application/json"

{
  "Log Request Id": "api-09630c07",
  "Controllers notified": true
}
```

The `Log Request Id` (`api-09630c07`) can be used to search through pinot-controller log file to see log entries related to execution of the Periodic task that was manually run.

If `tableName` (and its type `OFFLINE` or `REALTIME`) is not provided, the task will run against all tables.



## Starting a controller

Make sure you've [set up Zookeeper](cluster.md#setup-a-pinot-cluster). If you're using Docker, make sure to [pull the Pinot Docker image](cluster.md#setup-a-pinot-cluster). To start a controller:

{% tabs %}
{% tab title="Docker Image" %}
```
docker run \
    --network=pinot-demo \
    --name pinot-controller \
    -p 9000:9000 \
    -d ${PINOT_IMAGE} StartController \
    -zkAddress pinot-zookeeper:2181
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```
bin/pinot-admin.sh StartController \
  -zkAddress localhost:2181 \
  -clusterName PinotCluster \
  -controllerPort 9000
```
{% endtab %}
{% endtabs %}
