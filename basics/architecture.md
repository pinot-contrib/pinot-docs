---
description: >-
  Understand how the components of Apache Pinot™ work together to create a scalable OLAP database that can delivery low-latency, high-concurrecy queries at scale.
---

# Architecture

Learn the guiding principles behind the distributed architecture of Apache Pinot. Pinot is designed to handle large volumes of data with very low query latencies in the face of many concurrent queries, scaling query performance linearly with the number of nodes in a cluster.

{% hint style="info" %}
We recommend that you read [Basic Concepts](concepts.md) to better understand the terms used in this guide.
{% endhint %}

Apache Pinot™ is a distributed OLAP database designed to serve real-time, user-facing use cases. This imposes some unique and demanding requirements:

* Ultra low-latency queries (as low as 10ms P95)
* High query concurrency (as many as 100,000 queries per second)
* High data freshness (streaming data available for query immediately upon ingestion)
* Large data volume (up to petabytes)

This document describes the architectural choices the designers of Pinot have made to achieve these goals.

## Distributed design principles

To accommodate large data volumes with stringent latency and concurrency requirements, Pinot is designed as a distributed database. As a distributed system, it has these goals:

* **Highly available**: Pinot has no single point of failure. When operators choose data replication, the cluster can continue to serve queries when a node goes down.
* **Horizontally scalable**: Operators can scale a Pinot cluster by adding new nodes when the workload increases. There are even two node types to scale query volume, query complexity, and data size independently.
* **Immutable data**: Pinot treats all stored data as if it is immutable, which gives designers the ability to make simplifying assumptions elsewhere in the system. However, Pinot still supports upserts on streaming entity data and background purges of data to comply with data privacy regulations.
* **Dynamic configuration changes**: Operations like adding new tables, expanding a cluster, ingesting data, modifying an existing table, and adding indexes must not impact query availability or performance.

## Core components

As described in [Apache Pinot™ Concepts](concepts.md), Pinot has four node types:

* [Controller](components/cluster/controller.md)
* [Broker](components/cluster/broker.md)
* [Server](components/cluster/server.md)
* [Minion](components/cluster/minion.md)

![](<../.gitbook/assets/Pinot-architecture (1).svg>)

### Apache Helix and Zookeeper

Distributed systems do not maintain themselves, and in fact require sophisticated scheduling and resource management frameworks to function. Pinot uses [Apache Helix](http://helix.apache.org/) for this purpose. Helix exists as an independent project, but it was designed by the original creators of Pinot for Pinot's own cluster management purposes, so the architectures of the two systems are well-aligned. Helix takes the form of a process on the controller, plus embedded agents on the brokers and servers. It uses [Apache Zookeeper](https://zookeeper.apache.org/) as a fault-tolerant, strongly consistent, durable state store.

Helix maintains a picture of the intended state of the cluster, including the number of servers and brokers, the configuration and schema of all tables, connections to streaming ingest sources, currently executing batch ingestion jobs, the assignment of table segments to the servers in the cluster, and more. All of these configuration items are potentially mutable quantities, 

It's helpful to think of Helix as an event-driven discovery service with push and pull notifications that drives the state of a cluster to an ideal configuration. A finite-state machine maintains a contract of stateful operations that drives the health of the cluster towards its optimal configuration. Helix optimizes query load by updating routing configurations between nodes based on where data is stored in the cluster.




From a logical perspective, Helix as an event-driven discovery service that drives the state of a distributed system from its current state to an ideal configuration in its state store. In a cluster's quiescent state, the current state and the configured state are identical. Two things can alter this equilibrium:

* The configuration can change. This causes the ideal state of the cluster to become different from the actual state of the cluster.
* Cluster hardware resources can fail. This causes the actual state of the cluster to become different from the ideal state of the cluster.

Both scenarios require Helix to schedule new resources stand down existing resources to get the ideal and actual states to align again.

There are three physical node types in a Helix cluster:

* **Participant**: These nodes _do_ things, like store data or perform computation. Participants host _resources_, which are Helix's fundamental storage abstraction. Because Pinot servers store segment data, they are participants.
* **Spectator**: These nodes _see_ things, observing the evolving state of the _participants_ through an event push mechanism. Because Pinot brokers need to know which servers host which segments, they are spectators.
* **Controller**: This node observes and manages the state of participant nodes. The controller is responsible for coordinating all state transitions in the cluster and ensures that state constraints are satisfied while maintaining cluster stability. TODO: does it manage spectators?

In addition, Helix defines two logical components to express its storage abstraction:

* **Partition**. A unit of data storage that lives on at least one participant. Partitions may be replicated across multiple participants. A Pinot segment is a partition.
* **Resource**. A logical collection of partitions, providing a single view over a potentially large set of data stored across a distributed system. A Pinot table is a resource.

The Pinot architecture maps onto Helix components as follows:

|Pinot Component|Helix Component|
|----------|-----------|
|Segment|**Helix Partition**|
|Table|**Helix Resource**|
|Controller|Runs the Helix agent that drives the overall state of the cluster (also called the Helix Controller)|
|Server|**Helix Participant**|
|Broker|A **Helix Spectator** that observes the cluster for changes in the state of segments and servers. In order to support multi-tenancy, brokers are also modeled as **Helix Participants**. TODO: y tho?|
|Minion|**Helix Participant** that performs computation rather than store data|

Helix uses Zookeeper to maintain cluster state. The components of a Pinot cluster watch Zookeeper notifications and issue updates via their embedded Helix agents. Zookeeper stores the following information about the cluster:

|Resource|Stored Properties|
|--------|-----------------|
|Controller|<ul><li>Controller that is assigned as the current leader</li></ul>|
|Servers/Brokers|<ul><li>List of servers/brokers and their configuration</li><li>Health status</li></ul>|
|Tables|<ul><li>List of tables</li><li>Table configurations</li><li>Table schema information</li><li>List of segments within a table</li></ul>|
|Segment|<ul><li>Exact server location(s) of a segment (routing table)</li><li>State of each segment (online/offline/error/consuming)</li><li>Metadata about each segment</li></ul>|

Knowing the `ZNode` layout structure in Zookeeper for Helix agents in a cluster is useful for operations and/or troubleshooting cluster state and health.

![Pinot's Zookeeper Browser UI](../.gitbook/assets/Zookeeper\_UI.png)

### Controller

Pinot's [controller](components/cluster/controller.md) acts as the driver of the cluster's overall state and health. Because of its role as a Helix participant and spectator, which drives the state of other components, it's the first component that is typically started after Zookeeper.&#x20;

Starting a controller requires two parameters: Zookeeper address and cluster name. The controller will automatically create a cluster via Helix if it does not yet exist.

#### Fault tolerance

To configure fault tolerance, start multiple controllers (typically three) and one of them will act as a leader. If the leader crashes or dies, another leader is automatically elected. Leader election is achieved using Apache Helix. Having at-least one controller is required to perform any DDL equivalent operation on the cluster, such as adding a table or a segment.

The controller does not interfere with query execution. Query execution is not impacted even when all controllers nodes are offline. If all controller nodes are offline, the state of the cluster will stay as it was when the last leader went down. When a new leader comes online, a cluster resumes rebalancing activity and can accept new tables or segments.

#### Controller REST interface

The controller provides a REST interface to perform CRUD operations on all logical storage resources (servers, brokers, tables, and segments).

See [Pinot Data Explorer](components/exploring-pinot.md) for more information on the web-based admin tool.

### Broker

The [broker's](components/cluster/broker.md) responsibility is to route a given query to an appropriate [server](components/cluster/server.md) instance. A broker collects and merges the responses from all servers into a final result, then sends it back to the requesting client. The broker provides HTTP endpoints that accept SQL queries and returns the response in JSON format.

Brokers need three key things to start:

* Cluster name
* Zookeeper address
* Broker instance name

Initially, the broker registers as a **Helix Participant** and waits for notifications from other Helix agents. The broker handles these notifications for table creation, a new segment being loaded, or a server starting up or going down, in addition to any configuration changes.

**Service Discovery/Routing Table**

Regardless of the kind of notification, the key responsibility of a broker is to maintain the query routing table. The query routing table is simply a mapping between segments and the servers that a segment resides on. Typically, a segment resides on more than one server. The broker computes multiple routing tables depending on the configured routing strategy for a table. The default strategy is to balance the query load across all available servers.

{% hint style="info" %}
For special or generic cases that serve very high throughput queries, there are advanced routing strategies available such as ReplicaAware routing, partition-based routing, and minimal server selection routing.&#x20;
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

For every query, a cluster's broker performs the following:

* Fetches the routes that are computed for a query based on the routing strategy defined in a [table's](components/table/) configuration.
* Computes the list of segments to query from on each [server](components/cluster/server.md). To learn more about this, check out [routing](operators/tuning/routing.md).
* Scatter-gather: sends the requests to each server and gathers the responses.
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

Broker instances scale horizontally without an upper bound. In a majority of cases, only three brokers are required. If most query results that are returned to a client are less than 1 MB in size per query, you can run a broker and servers inside the same instance container. This lowers the overall footprint of a cluster deployment for use cases that don't need to guarantee a strict SLA on query performance in production.

### Server

[Servers](components/cluster/server.md) host [segments](components/table/segment/) and do most of the heavy lifting during query processing. Though the architecture shows that there are two kinds of servers, real-time and offline, a server doesn't really "know" if it's going to be a real-time server or an offline server. The server's responsibility depends on the [table](components/table/) assignment strategy.

{% hint style="info" %}
In theory, a server can host both real-time segments and offline segments. However, in practice, we use different types of machine SKUs for real-time servers and offline servers. The advantage of separating real-time servers and offline servers is to allow each to scale independently.
{% endhint %}

**Offline servers**

Offline servers typically host segments that are immutable. In this case, segments are created outside of a cluster and uploaded via a shell-based [curl](https://curl.haxx.se/) request. Based on the replication factor and the segment assignment strategy, the controller picks one or more servers to host the segment. Helix notifies the servers about the new segments. Servers fetch the segments from deep store and load them. At this point, the cluster's [broker](components/cluster/broker.md) detects that new segments are available and starts including them in query responses.

**Real-time servers**

Unlike offline servers, real-time [server](components/cluster/server.md) nodes ingest data from streaming sources, such as Kafka, and generate the indexed segments in-memory while flushing segments to disk periodically. In-memory segments are also known as consuming segments. Consuming segments get flushed periodically based on completion threshold (calculated with number of rows, time or segment size). At this point, they become completed segments. Completed segments are similar to offline servers' segments. Queries go over the in-memory (consuming) segments and the completed segments.

### Minion

[Minion](components/cluster/minion.md) is an optional component used for purging data from a Pinot cluster. For example, you might need to purge data for GDPR compliance in the UK.

## Data ingestion overview

Within Pinot, a logical [table](components/table/) is modeled as one of two types of physical tables: offline or real-time. Each table type follows a different state model.

Real-time and offline tables provide different configuration options for indexing. For real-time tables, you can also configure the connector properties for the stream data source, like Kafka. The two table types also allow users to use different containers for real-time and offline [server](components/cluster/server.md) nodes. For instance, offline servers might use virtual machines with larger storage capacity, whereas real-time servers might need higher system memory or more CPU cores.

The two types of tables also scale differently.

* Real-time tables have a smaller retention period and scale query performance based on the ingestion rate.
* Offline tables have larger retention and scale performance based on the size of stored data.

When ingesting data from the same source, you can have two tables that ingest the same data that are configured differently for real-time and offline queries. Even though the two tables have the same data, performance will scale differently for queries based on your requirements. In this scenario, real-time and offline tables must share the same [schema](../configuration-reference/schema.md).

You can configure real-time an offline tables differently depending on usage requirements. For example, you might choose to enable star-tree indexing for an offline table, while the real-time table with the same schema may not need it.

### Batch data flow

![](<../.gitbook/assets/OfflineServer (4).jpg>)

In batch mode, Pinot ingests data via an [ingestion job](data-import/batch-ingestion/), which works in the following way:

1. An ingestion job transforms a raw data source (such as a CSV file) into [segments](components/table/segment/).&#x20;
2. Once segments are generated for the imported data, the ingestion job stores them into the cluster's segment store (also known as deep store) and notifies the [controller](components/cluster/controller.md).&#x20;
3. The controller processes the notification, resulting in the Helix agent on the controller updating the ideal state configuration in Zookeeper.&#x20;
4. Helix then notifies the offline [server](components/cluster/server.md) that there are new segments available.&#x20;
5. In response to the notification from the controller, the offline server downloads the newly created segments directly from the cluster's segment store.&#x20;
6. The cluster's broker, which watches for state changes in Helix, detects the new segments and adds them to the list of segments to query (segment-to-server routing table).

### Real-time data flow

At table creation, a controller creates a new entry in Zookeeper for the consuming segment. Helix notices the new segment and notifies the real-time server, which starts consuming data from the streaming source. The broker, which watches for changes, detects the new segments and adds them to the list of segments to query (segment-to-server routing table).

![](../.gitbook/assets/real-time-flow.svg)

Whenever the segment is complete (full), the real-time server notifies the controller, which checks with all replicas and picks a winner to commit the segment to. The winner commits the segment and uploads it to the cluster's segment store, updating the state of the segment from "consuming" to "online". The controller then prepares a new segment in a "consuming" state.

## Query overview

Queries are received by brokers, which check the request against the segment-to-server routing table and scatter the request between real-time and offline servers.

![Pinot query overview](../.gitbook/assets/Pinot-Query-Overview.svg)

The two tables process the request by filtering and aggregating the queried data, which is then returned back to the broker. Finally, the broker gathers together all of the pieces of the query response and responds back to the client with the result.
