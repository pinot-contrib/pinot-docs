---
description: >-
  Explore the fundamental concepts of Apache Pinot™ as a distributed OLAP database.
---

# Apache Pinot™ concepts

Apache Pinot™ is a database designed to deliver highly concurrent, ultra-low-latency queries on large datasets through a set of common data model abstractions. Delivering on these goals requires several foundational architectural commitments, including:

* Storing data in columnar form to support high-performance scanning
* Sharding of data to scale both storage and computation
* A distributed architecture designed to scale capacity linearly
* A tabular data model read by SQL queries

## Pinot storage model

Pinot stores data in [_tables_](https://docs.pinot.apache.org/pinot-components/table). Tables are physically represented on disk as a collection of [_segments_](https://docs.pinot.apache.org/pinot-components/segment). Client processes query tables with [SQL](https://docs.pinot.apache.org/user-guide/user-guide-query/pinot-query-language). Tables optionally belong to one or more logical [_tenants_](components/cluster/tenant.md). Tables and tenants reside in a Pinot [_cluster_](components/cluster/).

### Table

Pinot stores data in [_tables_](components/table/). A Pinot table is conceptually identical to a relational database table with rows and columns. Columns have the same name and data type, known as the table's [schema](components/table/schema.md).

Pinot schemas are defined in a JSON file. Because that schema definition is in its own file, multiple tables can share a single schema. Each table can have a unique name, indexing strategy, partitioning, data sources, and other metadata.

Pinot table types include:
-  **real-time:** Ingests data from a streaming source like Apache Kafka®
- **offline:** Loads data from a batch source
- **hybrid:** Loads data from both a batch source and a streaming source

### Segment

Pinot tables are stored in one or more independent shards called [segments](components/table/segment/). A small table may be contained by a single segment, but Pinot lets tables grow to an unlimited number of segments. There are different processes for creating segments (see [ingestion](/developers/advanced/data-ingestion)). Segments have time-based partitions of table data, and are stored on Pinot [servers](components/cluster/server) that scale horizontally as needed for both storage and computation.

### Tenant

Every table is associated with a [_tenant_](components/cluster/tenant.md), or a logical namespace that restricts where the cluster processes queries on the table. A Pinot tenant takes the form of a text tag in the logical tenant namespace. Physical cluster hardware resources (i.e., [brokers](components/cluster/broker.md) and [servers](components/cluster/server.md)) are also associated with a tenant tag in the common tenant namespace. Tables of a particular tenant tag will only be scheduled for storage and query processing on hardware resources that belong to the same tenant tag. This lets Pinot cluster operators assign specified workloads to certain hardware resources,  preventing data from separate workloads from being stored or processed on the same physical hardware.

By default, all tables, brokers, and servers belong to a tenant called _DefaultTenant_, but you can configure multiple tenants in a Pinot cluster.

### Cluster

A Pinot [_cluster_](components/cluster/) is a collection of the software processes and hardware resources required to ingest, store, and process data. For detail about Pinot cluster components, see [Physical architecture](#physical-architecture).


## Physical architecture

![](../.gitbook/assets/Pinot-Components.svg)

A Pinot cluster consists of the following processes, which are typically deployed on separate hardware resources in production. In development, they can fit comfortably into Docker containers on a typical laptop.

* **Controller**: Maintains cluster metadata and manages cluster resources.
* **Zookeeper**: Manages the Pinot cluster on behalf of the controller. Provides fault-tolerant, persistent storage of metadata, including table configurations, schemas, segment metadata, and cluster state.
* **Broker**: Accepts queries from client processes and forwards them to servers for processing.
* **Server**: Provides storage for segment files and compute for query processing.
* (Optional) **Minion**: Computes background tasks other than query processing, minimizing impact on query latency. Optimizes segments, and builds additional indexes to ensure performance (even if data is deleted). 

The simplest possible Pinot cluster consists of four components: a server, a broker, a controller, and a Zookeeper node. In production environments, these components typically run on separate server instances, and scale out as needed for data volume, load, availability, and latency. Pinot clusters in production range from fewer than ten total instances to more than 1,000.

Pinot uses [Apache Zookeeper](https://zookeeper.apache.org/) as a distributed metadata store and and [Apache Helix](http://helix.apache.org/) for cluster management.

Helix is a cluster management solution created by the authors of Pinot. Helix maintains a persistent, fault-tolerant map of the intended state of the Pinot cluster. It constantly monitors the cluster to ensure that the right hardware resources are allocated to implement the present configuration. When the configuration changes, Helix schedules or decommissions hardware resources to reflect the new configuration. When elements of the cluster change state catastrophically, Helix schedules hardware resources to keep the actual cluster consistent with the ideal represented in the metadata. From a physical perspective, Helix takes the form of a controller process plus agents running on servers and brokers.

### Controller

The Pinot [controller](components/cluster/controller.md) is responsible for orchestrating the resources of a Pinot cluster in the presence of constantly evolving metadata changes and occasional node failure. As an Apache Helix Controller, it schedules the hardware resources that comprise the cluster and orchestrates connections between certain external processes and cluster components (e.g., ingest of [real-time tables](data-import/pinot-stream-ingestion) and [offline tables](data-import/batch-ingestion)). It can be deployed as a single process on its own server or as a group of redundant servers in an active/passive configuration. 

The controller exposes a REST API endpoint for cluster-wide administrative operations as well as a web-based query console to execute interactive SQL queries and perform simple administrative tasks.

### Server

Pinot [servers](components/cluster/server.md) provide the primary storage for [segments](components/table/segment/) and perform the computation required to execute queries over them. A production Pinot cluster contains many servers. In general, the more servers, the more data the cluster can retain in tables, the lower latency it can deliver on queries, and the more concurrent queries it can process.

Servers are typically segregated into real-time and offline workloads, with "real-time" servers hosting only real-time tables, and "offline" servers hosting only offline tables. This is a ubiquitous operational convention, not a difference or an explicit configuration in the server process itself.

### Broker

Pinot [brokers](components/cluster/broker.md) take query requests from client processes, scatter them to applicable servers, gather the results, and return them to the client. The controller shares cluster metadata with the brokers that allows the brokers to create a plan for executing the query involving a minimal subset of servers with the source data and, when required, other servers to shuffle and consolidate results. 

A production Pinot cluster contains many brokers. In general, the more brokers, the more concurrent queries a cluster can process, and the lower latency it can deliver on queries.

### Minion

Pinot [minions](components/cluster/minion.md) are an optional cluster component that executes background tasks on table data apart from the normal query mechanism performed by brokers and servers. Minions are processes that run on independent hardware resources, and are responsible for exeucting _minion tasks_ as directed by the controller. Examples of minon tasks include converting batch data from a standard format like Avro or JSON into segment files to be loaded into an offline table, or rewriting existing segment files to purge records as required by data privacy laws like GDPR. Minion tasks can run once or be scheduled to run periodically.

The minion mechanism exists to isolate the computational burden of out-of-band data processing from the servers. A production Pinot cluster can function with zero minions, but in practice there are a few several minion instances to manage the typical minion task workload. 
