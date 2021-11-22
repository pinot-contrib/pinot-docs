# Controller

The Pinot Controller is responsible for the following:

* Maintaining **global metadata** (e.g. configs and schemas) of the system with the help of Zookeeper which is used as the persistent metadata store.
* Hosting the **Helix Controller **and managing other Pinot components (brokers, servers, minions)&#x20;
* Maintaining the **mapping of which servers are responsible for which segments**. This mapping is used by the servers to download the portion of the segments that they are responsible for. This mapping is also used by the broker to decide which servers to route the queries to.
* Serving **admin endpoints** for viewing, creating, updating, and deleting configs, which are used to manage and operate the cluster.
* Serving endpoints for **segment uploads**, which are used in offline data pushes. They are responsible for initializing **real-time consumption **and coordination of persisting real-time segments into the segment store periodically.
* Undertaking other **management activities** such as managing retention of segments, validations.

For redundancy, there can be multiple instances of Pinot controllers. Pinot expects that all controllers are configured with the same back-end storage system so that they have a common view of the segments (_e.g._ NFS). Pinot can use other storage systems such as HDFS or [ADLS](https://azure.microsoft.com/en-us/services/storage/data-lake-storage/).

## Starting a Controller

Make sure you've [setup Zookeeper](cluster.md#setup-a-pinot-cluster). If you're using docker, make sure to [pull the pinot docker image](cluster.md#setup-a-pinot-cluster).  To start a controller&#x20;

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
