# Server

Servers **host the data segments** and **serve queries** off the data they host. There are two types of servers:

**Offline**\
****Offline servers are responsible for downloading segments from the segment store, to host and serve queries off. When a new segment is uploaded to the controller, the controller decides the servers (as many as replication) that will host the new segment and notifies them to download the segment from the segment store. On receiving this notification, the servers download the segment file and load the segment onto the server, to server queries off them.

![](../../.gitbook/assets/offlineserver-4.jpg)

**Real-time**\
****Real-time servers directly ingest from a real-time stream (such as Kafka, EventHubs). Periodically, they make segments of the in-memory ingested data, based on certain thresholds. This segment is then persisted onto the segment store.

![](../../.gitbook/assets/realtimeserver-1.jpg)

Pinot Servers are modeled as Helix Participants, hosting Pinot tables (referred to as _resources_ in Helix terminology). Segments of a table are modeled as Helix partitions (of a resource). Thus, a Pinot server hosts one or more helix partitions of one or more helix resources (_i.e._ one or more segments of one or more tables).

## Starting a Server

Make sure you've [setup Zookeeper](cluster.md#setup-a-pinot-cluster). If you're using docker, make sure to [pull the pinot docker image](cluster.md#setup-a-pinot-cluster).  To start a server&#x20;

```
Usage: StartServer
	-serverHost               <String>                      : Host name for controller. (required=false)
	-serverPort               <int>                         : Port number to start the server at. (required=false)
	-serverAdminPort          <int>                         : Port number to serve the server admin API at. (required=false)
	-dataDir                  <string>                      : Path to directory containing data. (required=false)
	-segmentDir               <string>                      : Path to directory containing segments. (required=false)
	-zkAddress                <http>                        : Http address of Zookeeper. (required=false)
	-clusterName              <String>                      : Pinot cluster name. (required=false)
	-configFileName           <Config File Name>            : Broker Starter Config file. (required=false)
	-help                                                   : Print this message. (required=false)
```



{% tabs %}
{% tab title="Docker Image" %}
```
docker run \
    --network=pinot-demo \
    --name pinot-server \
    -d ${PINOT_IMAGE} StartServer \
    -zkAddress pinot-zookeeper:2181
```
{% endtab %}

{% tab title="Launcher Scripts" %}
```
bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2181
```
{% endtab %}
{% endtabs %}

USAGE

```
Usage: StartServer
	-serverHost               <String>                      : Host name for controller. (required=false)
	-serverPort               <int>                         : Port number to start the server at. (required=false)
	-serverAdminPort          <int>                         : Port number to serve the server admin API at. (required=false)
	-dataDir                  <string>                      : Path to directory containing data. (required=false)
	-segmentDir               <string>                      : Path to directory containing segments. (required=false)
	-zkAddress                <http>                        : Http address of Zookeeper. (required=false)
	-clusterName              <String>                      : Pinot cluster name. (required=false)
	-configFileName           <Config File Name>            : Server Starter Config file. (required=false)
	-help                                                   : Print this message. (required=false)
```
