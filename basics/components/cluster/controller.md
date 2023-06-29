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

## Running the periodic task manually

The controller runs several periodic tasks in the background, to perform activities such as management and validation. Each periodic task has [its own configuration](https://docs.pinot.apache.org/configuration-reference/controller#periodic-tasks-configuration) to define the run frequency and default frequency. Each task runs at its own schedule or can also be triggered manually if needed. The task runs on the lead controller for each table.&#x20;

For period task configuration details, see [Controller configuration reference](https://docs.pinot.apache.org/configuration-reference/controller#periodic-tasks-configuration).&#x20;

Use the `GET /periodictask/names` API to fetch the names of all the periodic tasks running on your Pinot cluster.

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

To manually run a named periodic task, use the `GET /periodictask/run` API:

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

Make sure you've [set up Zookeeper](./#setup-a-pinot-cluster). If you're using Docker, make sure to [pull the Pinot Docker image](./#setup-a-pinot-cluster). To start a controller:

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
