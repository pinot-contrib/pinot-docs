---
description: Learn about the distributed systems architecture of Pinot
---

# Architecture

{% hint style="info" %}
It's recommended that you read [Basic Concepts](concepts.md) to better understand the terms used in this guide.
{% endhint %}

This guide will walk you through the guiding principles behind the design of Pinot. Here you will learn the distributed systems architecture that allows Pinot to scale linearly based on the number of nodes in a cluster.

## Guiding Design Principles

Pinot was designed by engineers at LinkedIn and Uber to scale query performance based on the number of nodes in a cluster. As you add more nodes, query performance will always improve based on the expected query volume per second quota. To achieve horizontal scalability to an unbounded number of nodes and data storage, without performance degradation, the following guiding design principles were established.

* **Highly available**: Pinot is built to serve low latency analytical queries for customer facing applications. By design, there is no single point of failure in Pinot. The system continues to serve queries when a node goes down.
* **Horizontally scalable**: Ability to scale by adding new nodes as a workload changes.
* **Latency vs Storage:**  Pinot is built to provide low latency even at high-throughput. Features such as segment assignment strategy, routing strategy, star-tree indexing were developed to achieve this. 
* **Immutable data**: Pinot assumes that all data stored is immutable. For GDPR compliance, we provide an add-on solution for purging data while maintaining performance guarantees.
* **Dynamic configuration changes**: Operations such as adding new tables, expanding a cluster, ingesting data, modifying indexing config, and re-balancing must be performed without impacting query availability or performance.

## Core Components

As described in the [concepts](concepts.md), Pinot has multiple distributed system components:[ Controller](components/controller.md), [Broker](components/broker.md), [Server](components/server.md), and [Minion](components/minion.md). 

Pinot uses [Apache Helix](http://helix.apache.org/) for cluster management. Helix is embedded as an agent within the different components and uses [Apache Zookeeper](https://zookeeper.apache.org/) for coordination and maintaining the overall cluster state and health.

![](../.gitbook/assets/pinot-architecture-1.svg)

### Apache Helix and Zookeeper

All Pinot Servers and Brokers are managed by Apache Helix. Apache Helix is a generic cluster management framework to manage partitions and replicas in a distributed system. It's helpful to think of Helix as an event-driven discovery service with push and pull notifications that drives the state of a cluster to an ideal configuration. A finite-state machine maintains a contract of stateful operations that drives the health of the cluster towards its optimal configuration. Query load is optimized as Helix updates routing configurations between nodes based on where data is stored in the cluster.

Helix divides nodes into three logical components based on their responsibilities:

1. **Participant**: These are the nodes in the cluster that actually host the distributed storage resources.
2. **Spectator**: These nodes observe the current state of each _**participant**_ and routes requests accordingly. Routers, for example, need to know the instance on which a partition is hosted and its state in order to route the request to the appropriate endpoint. Routing is continually being changed to optimize cluster performance as storage primitives are added and changed.
3. **Controller**: The [controller](components/controller.md) observes and manages the state of _**participant**_ nodes. The controller is responsible for coordinating all state transitions in the cluster and ensures that state constraints are satisfied while maintaining cluster stability.

Helix uses Zookeeper to maintain cluster state. Each component in a Pinot cluster takes a Zookeeper address as a startup parameter. The various components that are distributed in a Pinot cluster will watch Zookeeper notifications and issue updates via its embedded Helix-defined agent.

| Component  | Helix Mapping |
| :--- | :--- |
| Segment | Modeled as a **Helix Partition.** Each [segment](components/segment.md) can have multiple copies referred to as **Replicas**. |
| Table | Modeled as a **Helix Resource.** Multiple segments are grouped into a [table](components/table.md). All segments belonging to a Pinot Table have the same schema. |
| Controller | Embeds the Helix agent that drives the overall state of the cluster. |
| Server | [Server](components/server.md) is modeled as a **Helix Participant** and hosts [segments](components/segment.md). |
| Broker | Broker is modeled as a **Helix Spectator** that observes the cluster for changes in the state of segments and servers. In order to support multi-tenancy, brokers are also modeled as **Helix Participants**. |
| Minion | Pinot Minion is modeled as a **Helix Participant**. |

Helix agents use Zookeeper to store and update configurations, as well as for distributed coordination. Zookeeper stores the following information about the cluster:

<table>
  <thead>
    <tr>
      <th style="text-align:left">Resource</th>
      <th style="text-align:left">Stored Properties</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">Controller</td>
      <td style="text-align:left">
        <ul>
          <li>The controller that is assigned as the current leader</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">Servers/Brokers</td>
      <td style="text-align:left">
        <ul>
          <li>A list of servers/brokers and their configuration</li>
          <li>Health status</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">Tables</td>
      <td style="text-align:left">
        <ul>
          <li>List of tables</li>
          <li>Table configurations</li>
          <li>Table schema information</li>
          <li>List of segments within a table</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">Segment</td>
      <td style="text-align:left">
        <ul>
          <li>Exact server location(s) of a segment (routing table)</li>
          <li>State of each segment (online/offline/error/consuming)</li>
          <li>Meta data about each segment</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>Knowing the _ZNode_ layout structure in Zookeeper for Helix agents in a cluster is useful for operations and/or troubleshooting cluster state and health.

![](../.gitbook/assets/znode-layout%20%281%29.svg)

### Controller

Pinot's controller acts as the driver of the cluster's overall state and health. Because of its role as a Helix participant and spectator, which drives the state of other components, it is the first component that is typically started after Zookeeper. Two parameters are required for starting a controller:  Zookeeper URI and cluster name. The controller will automatically create a cluster via Helix if it does not yet exist. 

#### Fault tolerance

To achieve fault tolerance, one can start multiple controllers \(typically 3\) and one of them will act as a leader. If the leader crashes or dies, another leader is automatically elected. Leader election is achieved using Apache Helix. Having at-least one controller is required to perform any DDL equivalent operation on the cluster, such as adding a table or a segment. The controller does not interfere with query execution. Query execution is not impacted even when all controllers nodes are offline. If all controller nodes are offline, the state of the cluster will stay as it was when the last leader went down. When a new leader comes online, a cluster resumes rebalancing activity and can accept new tables or segments.

#### Controller Rest Interface

Controller provides a REST interface to perform CRUD operations on all logical storage resources \(Servers, Brokers, Tables, Segments\). See [Pinot Data Explorer](getting-started/exploring-pinot.md) for more information on the web-based admin tool.

### Broker

The responsibility of the [broker](components/broker.md) is to route a given query to an appropriate [server](components/server.md) instance. A broker will collect and merge the responses from all servers into a final result and send it back to the requesting client. The broker provides HTTP endpoints that accept SQL queries and returns the response in JSON format. 

Brokers need three key things to start.

* Cluster name
* Zookeeper address
* Broker instance name

At the start, a broker registers as a **Helix Participant** and awaits notifications from other Helix agents. These notifications will be handled for table creation, a new segment being loaded, or a server starting up/or going down, in addition to any configuration changes.

**Service Discovery/Routing Table**

Irrespective of the kind of notification, the key responsibility of a broker is to maintain the query routing table. The query routing table is simply a mapping between segments and the servers that a segment resides on. Typically, a segment resides on more than one server. The broker computes multiple routing tables depending on the configured routing strategy for a table. The default strategy is to balance the query load across all available servers. 

{% hint style="info" %}
There are advanced routing strategies available such as ReplicaAware routing,  partition-based routing, and minimal server selection routing. These strategies are meant for special or generic cases that are meant to serve very high throughput queries. 
{% endhint %}

```javascript
//This is an example ZNode config for EXTERNAL VIEW in Helix
{
  "id" : "baseballStats_OFFLINE",
  "simpleFields" : {
    ...
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

For every query**,** a cluster's broker performs the following:

* Fetches the routes that are computed for a query based on the routing strategy defined in a [table's](components/table.md) configuration.
* Computes the list of segments to query from on each [server](components/server.md).
* _Scatter-Gather:_ sends the requests to each server and gathers the responses.
* _Merge:_ merges the query results returned from each server.
* Sends the query result to the client. 

```javascript
// Query: select count(*) from baseballStats limit 10

// RESPONSE
// ========
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
  
Broker instances scale horizontally without an upper bound. In a majority of cases, only three brokers are required. If most query results that are returned to a client are &lt;1MB in size per query, one can run a broker and servers inside the same instance container. This lowers the overall footprint of a cluster deployment for use cases that do not need to guarantee a strict SLA on query performance in production.

### Server

Servers host segments and does most of the heavy lifting during query processing. Though the architecture shows that there are two kinds of servers, real-time and offline, a server does not really know if its going to be a real-time server or an offline server. The responsibility of a server depends on the [table](components/table.md) assignment strategy. 

{% hint style="info" %}
In theory, a server can host both real-time segments and offline segments. However, in practice, we use different types of machine SKU's for real-time servers and offline servers. The advantage of separating real-time servers and offline servers is to allow each to scale independently.
{% endhint %}

**Offline servers**

Offline servers typically host segments that are immutable. In this case, segments are created outside of a cluster and uploaded via a shell-based [curl](https://curl.haxx.se/) request. Based on the replication factor and the segment assignment strategy, the controller picks one or more servers to host the segment. Servers are notified via Helix about the new segments. Servers fetch the segments from deep store and loads them before being ready to serve query requests. At this point, the cluster's [broker](components/broker.md) detects that new segments are available and starts including them in query responses.

**Real-time servers**

Real-time servers are different from the offline servers. Real-time [server](components/server.md) nodes ingest data from streaming sources, such as Kafka, and generate the indexed segments in-memory \(flushing segments to disk periodically\). In memory segments are also known as consuming segments. These consuming segments get flushed periodically based on completion threshold \(based on number of rows, time or segment size\). At this point, they are known as completed segments. Completed segments are similar to the offline server's segments. Queries go over the in-flight \(consuming\) segments and the completed segments.

### Minion

[Minion](components/minion.md) is an optional component and is not required to get started with Pinot. Minion is used for purging data from a Pinot cluster \(for reasons such as GDPR compliance in the UK\).

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

 

