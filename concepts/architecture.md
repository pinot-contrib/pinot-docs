---
description: Architecture diagram
---

# Architecture

![Pinot Architecture](../.gitbook/assets/pinot-architecture-1.svg)

This page assumes that the reader has read the Pinot [Concepts](concepts.md) 

Guiding design principles behind Pinot project

* **Highly available**: Pinot is built to  serve low latency analytical queries for customer facing  applications. By design, there is no single point of failure in Pinot i.e. the system continues to serve queries when a node goes down.
* **Horizontally scalable**: Ability to scale by adding new nodes as workload changes.
* **Latency vs Storage:**  Pinot is built to provide low latency even at high throughput. Lot of features such as segment assignment strategy, routing strategy, star-tree index were developed to achieve this. 
* **Immutable data**: Pinot assumes the data is immutable. There is an ongoing effort to support mutation.
* **Dynamic configuration changes**:  Operations such as adding new table, expanding cluster, ingesting data, modifying indexing config, rebalancing etc must be performed without impacting the end-users.

## Core Components

As described in the concepts, Pinot has multiple components - Controller, Broker, Server, Minion. Pinot uses Apache Helix for cluster management. Helix is embedded within the Pinot components and uses Zookeeper for coordination and maintaining the cluster state. 

### Apache Helix and Zookeeper

All Pinot Servers and Brokers are managed by Apache Helix. Apache Helix is a generic cluster management framework to manage partitions and replicas in a distributed system. See helix.apache.org for additional information.

Helix divides nodes into 3 logical components based on their responsibilities:

1. **Participant**: The nodes that actually host the distributed resources.
2. **Spectator**: The nodes that simply observe the current state of each Participant and routes requests accordingly. Routers, for example, need to know the instance on which a partition is hosted and its state in order to route the request to the appropriate endpoint.
3. **Controller**: The node that observes and controls the Participant nodes. It is responsible for coordinating all transitions in the cluster and ensuring that state constraints are satisfied while maintaining cluster stability.

Pinot leverages [Apache Helix](http://helix.apache.org) for cluster management. Apache Helix internally uses Zookeeper to maintain state. Zookeeper is a critical for Pinot and most of the other components rely on zookeeper. In fact, all components take zookeeper address as a startup parameter. Pinot  components interact with Zookeeper via Helix APIs.

Understanding Apache Helix [concepts](https://helix.apache.org/Concepts.html) and [Architecture](https://helix.apache.org/Architecture.html) will help in understanding and operating Pinot. Pinot Terminology and its mapping to Helix Concepts

| Pinot  | Helix Mapping |
| :--- | :--- |
| Segment | Modeled as a **Helix Partition.** Each Pinot Segment can have multiple copies referred to as **Replicas**. |
| Table | Modeled as **Helix Resource.** Multiple Pinot segment are grouped into a logical entity referred to as Pinot Table. All segments belonging to a Pinot Table have the same schema. |
| Controller | Pinot controller embeds Helix Controller. |
| Server | Pinot Server is modeled as a **Helix Participant** and hosts the Pinot segments |
| Broker | Pinot Broker is modeled as a **Helix Spectator** that observes the cluster for changes in the state of segments and Pinot Server. In order to support Multi tenancy in Pinot Brokers, Pinot Brokers are also modeled as Helix Participants. |
| Minion | Pinot Minion is modeled as a Participant |

Pinot via Helix uses Zookeeper to maintain cluster state, configuration and distributed coordination.  Zookeeper stores the following information about the cluster

* Controller
  * Current leader controller.
* Servers/Brokers 
  * List of servers/brokers and their configuration
  * Status \(Live/Dead\)
* Tables 
  * List of tables
  * Table configuration
  * Table Schema information
  * List of segments within a table 
* Segment
  * Exact location\(s\) of segment - segment to server mapping
  * Status of each segment \(online/offline/error/consuming\)
  * Metadata about each segment

Understanding the ZNode layout structure in Helix will help in understanding and operating the Pinot Cluster. 

![](../.gitbook/assets/znode-layout%20%281%29.svg)

### Controller

Controller acts as the central brain of the pinot system. It's typically the first component that is started after Zookeeper. The only two parameters  needed for a controller to start is Zookeeper and a cluster name. Controller automatically creates the cluster in Helix if it does not exist. 

#### Fault tolerance

To achieve fault tolerance, one can start multiple controllers \(typically 3\) and one of them will act as a leader. If the leader crashes or dies, another leader is automatically elected. Leader election is achieved using Apache Helix. Having at-least one controller is required to perform any DDL equivalent operation on the Pinot Cluster such as - Add new Table, Add Segment etc. Controller does not interfere in the query path - queries are not impacted if all controllers are down.

#### Controller Rest Interface

Controller provides a rest interface to perform CRUD operations on all entities - Servers, Brokers, Tables, Segments, etc. See  [Pinot Data Explorer](../getting-started/exploring-pinot.md)  for more information on admin interface.

### Broker

The responsibility of Broker is to route a given query to appropriate Pinot Server instances, collect and merge the responses into final result and send it back to the client. Broker provides the http endpoints that accepts sql queries and returns the response in JSON format. Brokers need 3 key things to start - cluster-name, zookeeper address and broker instance name. At the start, brokers registers as a Helix Participant and awaits notifications from Helix. These notifications can be new table creation, a new segment being loaded, or a server starting up/or going down, any configuration changes, etc. 

**Service Discovery/Routing Table**

Irrespective of the kind of notification, the key responsibility of a broker is to maintain the query routing table. Query routing table is simply a mapping from segment to servers it resides on. In Helix terminology, routing table is nothing but the contents of ExternalView. For example, the snippet below indicates the segment - baseballStats\_OFFLINE\_0 exists on Server\_10.1.10.82\_7000. Typically, a segment resides on more than 1 server. Broker computes multiple routing table depending on the routing strategies. This strategy can be configured in table config. The default strategy is to balance the query load across all the servers. There are advanced options available such as ReplicaAware routing,  partition based routing, minimal server selection routing which come in handy for serving high throughput queries. 

```text
//EXTERNAL VIEW In Helix
{
  "id" : "baseballStats_OFFLINE",
  "simpleFields" : {
    .....
  },
  "mapFields" : {
    "baseballStats_OFFLINE_0" : {
      "Server_10.1.10.82_7000" : "ONLINE"
    }
  },
  ...
}
```

**Query processing**  
For every query the broker performs the following -

* Fetches the routing table which is computed based on the routing strategy defined in tableconfig
* Compute the list of segments to query from each server
* Scatter-Gather : send the requests to each server and gather the responses
* Merge: Merge all the results from servers 
* Send the result back to the client. 

```text
Query: select count(*) from baseballStats limit 10

RESPONSE
========
{
    "resultTable": {
        "dataSchema": {
            "columnDataTypes": ["LONG"],
            "columnNames": ["count(*)"]
        },
        "rows": [
            [97889]
        ]
    },
    "exceptions": [],
    "numServersQueried": 1,
    "numServersResponded": 1,
    "numSegmentsQueried": 1,
    "numSegmentsProcessed": 1,
    "numSegmentsMatched": 1,
    "numConsumingSegmentsQueried": 0,
    "numDocsScanned": 97889,
    "numEntriesScannedInFilter": 0,
    "numEntriesScannedPostFilter": 0,
    "numGroupsLimitReached": false,
    "totalDocs": 97889,
    "timeUsedMs": 5,
    "segmentStatistics": [],
    "traceInfo": {},
    "minConsumingFreshnessTimeMs": 0
}
```

**Fault tolerance**  
  
Brokers scale horizontally and one can add as many brokers as needed. Typically, 3 brokers are sufficient. If the data size is small, one can run the broker and server as part of the same process.

### Server

Servers host the pinot segments and are does most of heavy lifting during  query processing. Though the architecture shows that there are two kinds of servers - realtime and offline, a pinot server does not really know if its going to be a realtime server or offline server. The responsibility of a server depends on the table assignment strategy. 

`In theory, a server can host both realtime segments and offline segments. However in practice, we use different types of machine sku's for realtime servers and offline servers. The advantage of separating realtime servers and offline servers is to allow them to scale independently.` 

**Offline servers**

Offline servers typically host segments that are immutable. The segments are created outside the pinot cluster and uploaded via a curl call. Based on the replication factor and the segment assignment strategy, the controller picks one or more servers to host the segment. Servers are notified via Helix about the new segments. Servers fetch the segments from deep store, loads them and is ready to serve. At this point, the brokers detect that new segments are loaded and starts including these segments in the query request.

**Realtime servers**

Real-time servers are different from the offline servers. Real-time nodes ingests data  from streaming sources such as Kafka and generate the index segments in memory and flush them to disk periodically. In memory segments are also known as consuming segments. These consuming segments gets flushed periodically based on completion threshold \(based on number of rows, time or segment size\). At this point, they are known as completed segments. Completed segments are similar to the offline segments. Queries go over the inflight \(consuming\) segments and the completed segments.

### Minion

Minion is an optional component and is not required to get started with Pinot. Minion allows performing background tasks such as merging segments, roll up, GDPR tasks to purge records and many more. Most of the tasks involve downloading the segment, modifying it and uploading it back to Pinot. These operations can be resource intensive and running these tasks on pinot servers will impact query latency. Minion allows one to run these tasks on separate nodes without impacting the query performance.



## Data Ingestion Overview

### Table 

Creation of a table in Pinot is as simple as running couple of rest api calls. Within Pinot a logical table is modeled as two physical tables - offline and realtime.  The main reason for this is that they follow different state model.

The realtime and offline tables can potentially have different configurations - indexing, stream config. This also allows users to use  different machine types for realtime and offline nodes. For instance, offline servers might use machines with larger capacity where realtime servers might need higher memory and high compute servers. They also scale differently. Realtime has a smaller retention period and scales based on the ingestion rate where as offline data has larger retention and  scale based on data size.

Few things to keep in mind 

1. There are two types of tables - realtime and offline. For example, myTable\_REALTIME represent the realtime table and myTable\_OFFLINE represents the offline table. 
2. Realtime table and offline table must have the same schema.
3. The configuration can be different for real-time and offline. For e.g. one might chose to have star-tree for offline tables but realtime might chose not to.

State Model

### Batch data flow 

![](../.gitbook/assets/offlineserver-4.jpg)

In _Batch mode_, Data is ingested into _Pinot_ via _Ingestion Job_. _Ingestion Job_ transforms the _raw data_ into _segments_. Once _segments_ are generated, the _Ingestion Job_ stores them into the _Segment store_ \(a.k.a. Deep store\) and notifies the _Controller_, which updates _Helix Idealstate_ in the _Zookeeper_. _Helix_ notifies the _Offline server_ of the new _segments_. The _Offline server_ downloads and loads the newly created _segments_ from the _Segment store_. The _Broker_, which watches for changes, detects the new _segments_ and adds them to the list of _segments_ to query.

### Realtime data flow 

![](../.gitbook/assets/real-time-flow.svg)

At table creation, the _Controller_ creates a new entry in _Zookeeper_ for the consuming segment. _Helix_ notices the new segment and notifies the _Realtime server_, which start consuming data from the streaming source. The _Broker_, which watches for changes, detects the new segments and adds them to the list of segments to query.

Whenever the segment is complete \(i.e. full\), the _Realtime server_ notifies the _Controller_, which checks with all replicas and picks a winner to commit the segment. The winner commits the segment and uploads it to the _Segment store_, updating the state of the segment from "consuming" to "online". Then the _Controller_ prepares a new segment in "consuming" state.



## Query Overview

![Pinot Query Overview](../.gitbook/assets/pinot-query-overview.svg)



Queries are received by Brokers, which check the request against the routing table, scatter the request between realtime and offline server. These two process the request, by filtering and aggregating the data, which is sent to the Broker. Finally, the Broker gathers together all the pieces of responses and responds back to the client.

All the servers \(Broker, realtime and offline\) are coordinated by an Apache Helix instance.

 

