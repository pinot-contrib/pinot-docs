---
description: >-
  Learn about the various components of Pinot and terminologies used to describe
  data stored in Pinot
---

# Concepts

Pinot is designed to deliver low latency queries on large datasets. In order to achieve this performance, Pinot stores data in a columnar format and adds additional indices to perform fast filtering, aggregation and group by.

Raw data is broken into small data shards and each shard is converted into a unit known as a [segment](https://docs.pinot.apache.org/pinot-components/segment). One or more segments together form a [table](https://docs.pinot.apache.org/pinot-components/table), which is the logical container for querying Pinot using [SQL/PQL](https://docs.pinot.apache.org/user-guide/user-guide-query/pinot-query-language).

## Pinot Storage Model

Pinot uses a variety of terms which can refer to either abstractions that model the storage of data or infrastructure components that drive the functionality of the system. 

![Pinot Storage Model Abstraction](../.gitbook/assets/pinot_entities.jpg)

### **Table**

Similar to traditional databases, Pinot has the concept of a [**table**](components/table.md)—a logical abstraction to refer to a collection of related data. As is the case with RDBMS, a table is a construct that consists of columns and rows \(documents\) that are queried using SQL. A table is associated with a [schema](components/schema.md) which defines the columns in a table as well as their data types. 

As opposed to RDBMS schemas, multiple tables can be created in Pinot \(real-time or batch\) that inherit a single schema definition. Tables are independently configured for concerns such as indexing strategies, partitioning, tenants, data sources, and/or replication.

### **Segment**

Pinot has a distributed systems architecture that scales horizontally. Pinot expects the size of a table to grow infinitely over time. In order to achieve this, all data needs to be distributed across multiple nodes. Pinot achieves this by breaking data into smaller chunks known as [**segments**](components/segment.md) ****\(this is similar to shards/partitions in HA relational databases\). Segments can also be seen as time-based partitions. 

### **Tenant**

In order to support multi-tenancy, Pinot has first class support for tenants. A table is associated with a [tenant.](components/tenant.md) This allows all tables belonging to a particular logical namespace to be grouped under a single tenant name and isolated from other tenants. This isolation between tenants provides different namespaces for applications and teams to prevent sharing tables or schemas. Development teams building applications will never have to operate an independent deployment of Pinot. An organization can operate a single cluster and scale it out as new tenants increase the overall volume of queries. Developers can manage their own schemas and tables without being impacted by any other tenant on a cluster. 

By default, all tables belong to a default tenant named "default". The concept of tenants is very important, as it satisfies the architectural principle of a "database per service/application" without having to operate many independent data stores. Further, tenants will schedule resources so that segments \(shards\) are able to restrict a table's data to reside only on a specified set of nodes. Similar to the kind of isolation that is ubiquitously used in Linux containers, compute resources in Pinot can be scheduled to prevent resource contention between tenants.

### **Cluster**

Logically, a [cluster ](components/cluster.md)is simply a group of tenants. As with the classical definition of a cluster, it is also a grouping of a set of compute nodes. Typically, there is only one cluster per environment/data center. There is no needed to create multiple clusters since Pinot supports the concept of tenants. At LinkedIn, the largest Pinot cluster consists of 1000+ nodes distributed across a data center. The number of nodes in a cluster can be added in a way that will linearly increase performance and availability of queries. The number of nodes and the compute resources per node will reliably predict the QPS for a Pinot cluster, and as such, capacity planning can be easily achieved using SLAs that assert performance expectations for end-user applications. 

{% hint style="info" %}
Auto-scaling is also achievable, however, a set amount of nodes is recommended to keep QPS consistent when query loads vary in sudden unpredictable end-user usage scenarios.
{% endhint %}

## Pinot Components

![](../.gitbook/assets/pinot-components.svg)

A Pinot cluster is comprised of multiple distributed system components. These components are useful to understand for operators that are monitoring system usage or are debugging an issue with a cluster deployment.

* Controller
* Server
* Broker
* Minion \(optional\)

The benefits of scale that make Pinot linearly scalable for an unbounded number of nodes is made possible through its integration with [Apache Zookeeper](https://zookeeper.apache.org/) and [Apache Helix](http://helix.apache.org/). 

{% hint style="info" %}
Helix is a cluster management solution that was designed and created by the authors of Pinot at LinkedIn. Helix drives the state of a Pinot cluster from a transient state to an ideal state, acting as the fault-tolerant distributed state store that guarantees consistency. Helix is embedded as agents that operate within a controller, broker, and server, and does not exist as an independent and horizontally scaled component.
{% endhint %}

### Pinot Controller

A [controller](components/controller.md) is the core orchestrator that drives the consistency and routing in a Pinot cluster. Controllers are horizontally scaled as an independent component \(container\) and has visibility of the state of all other components in a cluster. The controller reacts and responds to state changes in the system and schedules the allocation of resources for tables, segments, or nodes. As mentioned earlier, Helix is embedded within the controller as an agent that is a participant responsible for observing and driving state changes that are subscribed to by other components. 

In addition to cluster management, resource allocation, and scheduling, the controller is also the HTTP gateway for REST API administration of a Pinot deployment. A web-based query console is also provided for operators to quickly and easily run SQL/PQL queries.

### Pinot Broker

A [broker](components/broker.md) receives queries from a client and routes their execution to one or more Pinot servers before returning a consolidated response.

### Pinot Server

[Servers](components/server.md) host segments \(shards\) that are scheduled and allocated across multiple nodes and routed on an assignment to a tenant \(there is a single tenant by default\). Servers are independent containers that scale horizontally and are notified by Helix through state changes driven by the controller. A server can either be a real-time server or an offline server. 

A real-time and offline server have very different resource usage requirements, where real-time servers are continually consuming new messages from external systems \(such as Kafka topics\) that are ingested and allocated on segments of a tenant. Because of this, resource isolation can be used to prioritize high-throughput real-time data streams that are ingested and then made available for query through a broker.

### Pinot Minion

Pinot [minion](components/minion.md) is an optional component that can be used to run background tasks such as "purge" for GDPR \(General Data Protection Regulation\). As Pinot is an immutable aggregate store, records containing sensitive private data need to be purged on a request-by-request basis. Minion provides a solution for this purpose that complies with GDPR while optimizing Pinot segments and building additional indices that guarantees performance in the presence of the possibility of data deletion. One can also write a custom task that runs on a periodic basis. While it's possible to perform these tasks on the Pinot servers directly, having a separate process \(Minion\) lessens the overall degradation of query latency as segments are impacted by mutable writes.

