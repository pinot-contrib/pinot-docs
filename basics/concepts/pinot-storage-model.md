# Pinot storage model

Apache Pinot™ uses a variety of terms which can refer to either abstractions that model the storage of data or infrastructure components that drive the functionality of the system, including:

* [Tables](pinot-storage-model.md#table) to store data
* [Segments](pinot-storage-model.md#segment) to partition data
* [Tenants](pinot-storage-model.md#tenant) to isolate data
* [Clusters](pinot-storage-model.md#cluster) to manage data

Pinot has a distributed systems architecture that scales horizontally. Pinot expects the size of a table to grow infinitely over time. To achieve this, all data needs to be distributed across multiple nodes. Pinot achieves this by breaking data into smaller chunks known as [segments](https://docs.pinot.apache.org/pinot-components/segment) (similar to shards/partitions in HA relational databases). Segments can also be seen as time-based partitions.

## Table

Similar to traditional databases, Pinot has the concept of a [table](https://docs.pinot.apache.org/pinot-components/table)—a logical abstraction to refer to a collection of related data. As is the case with relational database management systems (RDBMS), a table is a construct that consists of columns and rows (documents) that are queried using SQL. A table is associated with a [schema](https://docs.pinot.apache.org/pinot-components/schema), which defines the columns in a table as well as their data types.

As opposed to RDBMS schemas, multiple tables can be created in Pinot (real-time or batch) that inherit a single schema definition. Tables are independently configured for concerns such as indexing strategies, partitioning, tenants, data sources, and replication.

Pinot stores data in [tables](../components/table/). A Pinot table is conceptually identical to a relational database table with rows and columns. Columns have the same name and data type, known as the table's [schema](../components/table/schema.md).

Pinot schemas are defined in a JSON file. Because that schema definition is in its own file, multiple tables can share a single schema. Each table can have a unique name, indexing strategy, partitioning, data sources, and other metadata.

Pinot table types include:

* **real-time:** Ingests data from a streaming source like Apache Kafka®
* **offline:** Loads data from a batch source
* **hybrid:** Loads data from both a batch source and a streaming source

## Segment

Pinot tables are stored in one or more independent shards called [segments](../components/table/segment/). A small table may be contained by a single segment, but Pinot lets tables grow to an unlimited number of segments. There are different processes for creating segments (see [ingestion](../../developers/advanced/data-ingestion.md)). Segments have time-based partitions of table data, and are stored on Pinot [servers](../components/cluster/server.md) that scale horizontally as needed for both storage and computation.

## Tenant

To support multi-tenancy, Pinot has first class support for tenants. A table is associated with a [tenant](https://docs.pinot.apache.org/pinot-components/tenant). This allows all tables belonging to a particular logical namespace to be grouped under a single tenant name and isolated from other tenants. This isolation between tenants provides different namespaces for applications and teams to prevent sharing tables or schemas. Development teams building applications do not have to operate an independent deployment of Pinot. An organization can operate a single cluster and scale it out as new tenants increase the overall volume of queries. Developers can manage their own schemas and tables without being impacted by any other tenant on a cluster.

Every table is associated with a [_tenant_](../components/cluster/tenant.md), or a logical namespace that restricts where the cluster processes queries on the table. A Pinot tenant takes the form of a text tag in the logical tenant namespace. Physical cluster hardware resources (i.e., [brokers](../components/cluster/broker.md) and [servers](../components/cluster/server.md)) are also associated with a tenant tag in the common tenant namespace. Tables of a particular tenant tag will only be scheduled for storage and query processing on hardware resources that belong to the same tenant tag. This lets Pinot cluster operators assign specified workloads to certain hardware resources, preventing data from separate workloads from being stored or processed on the same physical hardware.

By default, all tables, brokers, and servers belong to a tenant called _DefaultTenant_, but you can configure multiple tenants in a Pinot cluster.

## Cluster

A Pinot [_cluster_](../components/cluster/) is a collection of the software processes and hardware resources required to ingest, store, and process data. For detail about Pinot cluster components, see [Physical architecture](pinot-storage-model.md#physical-architecture).

## Physical architecture

<figure><img src="../../.gitbook/assets/image (2).png" alt=""><figcaption></figcaption></figure>

A Pinot cluster consists of the following processes, which are typically deployed on separate hardware resources in production. In development, they can fit comfortably into Docker containers on a typical laptop.

* **Controller**: Maintains cluster metadata and manages cluster resources.
* **Zookeeper**: Manages the Pinot cluster on behalf of the controller. Provides fault-tolerant, persistent storage of metadata, including table configurations, schemas, segment metadata, and cluster state.
* **Broker**: Accepts queries from client processes and forwards them to servers for processing.
* **Server**: Provides storage for segment files and compute for query processing.
* (Optional) **Minion**: Computes background tasks other than query processing, minimizing impact on query latency. Optimizes segments, and builds additional indexes to ensure performance (even if data is deleted).

The simplest possible Pinot cluster consists of four components: a server, a broker, a controller, and a Zookeeper node. In production environments, these components typically run on separate server instances, and scale out as needed for data volume, load, availability, and latency. Pinot clusters in production range from fewer than ten total instances to more than 1,000.

Pinot uses [Apache Zookeeper](https://zookeeper.apache.org/) as a distributed metadata store and and [Apache Helix](http://helix.apache.org/) for cluster management.

Helix is a cluster management solution created by the authors of Pinot. Helix maintains a persistent, fault-tolerant map of the intended state of the Pinot cluster. It constantly monitors the cluster to ensure that the right hardware resources are allocated to implement the present configuration. When the configuration changes, Helix schedules or decommissions hardware resources to reflect the new configuration. When elements of the cluster change state catastrophically, Helix schedules hardware resources to keep the actual cluster consistent with the ideal represented in the metadata. From a physical perspective, Helix takes the form of a controller process plus agents running on servers and brokers.

## Controller

A[ controller](https://docs.pinot.apache.org/pinot-components/controller) is the core orchestrator that drives the consistency and routing in a Pinot cluster. Controllers are horizontally scaled as an independent component (container) and has visibility of the state of all other components in a cluster. The controller reacts and responds to state changes in the system and schedules the allocation of resources for tables, segments, or nodes. As mentioned earlier, Helix is embedded within the controller as an agent that is a participant responsible for observing and driving state changes that are subscribed to by other components.

The Pinot [controller](../components/cluster/controller.md) schedules and re-schedules resources in a Pinot cluster when metadata changes or a node fails. As an Apache Helix Controller, it schedules the resources that comprise the cluster and orchestrates connections between certain external processes and cluster components (e.g., ingest of [real-time tables](../data-import/pinot-stream-ingestion/) and [offline tables](../data-import/batch-ingestion/)). It can be deployed as a single process on its own server or as a group of redundant servers in an active/passive configuration.

The controller exposes a [REST API endpoint](../../users/api/controller-api-reference/) for cluster-wide administrative operations as well as a web-based query console to execute interactive SQL queries and perform simple administrative tasks.

## Server

[Servers](https://docs.pinot.apache.org/pinot-components/server) host segments (shards) that are scheduled and allocated across multiple nodes and routed on an assignment to a tenant (there is a single tenant by default). Servers are independent containers that scale horizontally and are notified by Helix through state changes driven by the controller. A server can either be a real-time server or an offline server.

A real-time and offline server have very different resource usage requirements, where real-time servers are continually consuming new messages from external systems (such as Kafka topics) that are ingested and allocated on segments of a tenant. Because of this, resource isolation can be used to prioritize high-throughput real-time data streams that are ingested and then made available for query through a broker.

## Broker

Pinot [brokers](../components/cluster/broker.md) take query requests from client processes, scatter them to applicable servers, gather the results, and return them to the client. The controller shares cluster metadata with the brokers that allows the brokers to create a plan for executing the query involving a minimal subset of servers with the source data and, when required, other servers to shuffle and consolidate results.

A production Pinot cluster contains many brokers. In general, the more brokers, the more concurrent queries a cluster can process, and the lower latency it can deliver on queries.

## Pinot minion

Pinot minion is an optional component that can be used to run background tasks such as "purge" for GDPR (General Data Protection Regulation). As Pinot is an immutable aggregate store, records containing sensitive private data need to be purged on a request-by-request basis. Minion provides a solution for this purpose that complies with GDPR while optimizing Pinot segments and building additional indices that guarantees performance in the presence of the possibility of data deletion. One can also write a custom task that runs on a periodic basis. While it's possible to perform these tasks on the Pinot servers directly, having a separate process (Minion) lessens the overall degradation of query latency as segments are impacted by mutable writes.

A Pinot [minion](../components/cluster/minion.md) is an optional cluster component that executes background tasks on table data apart from the query processes performed by brokers and servers. Minions run on independent hardware resources, and are responsible for executing _minion tasks_ as directed by the controller. Examples of minon tasks include converting batch data from a standard format like Avro or JSON into segment files to be loaded into an offline table, and rewriting existing segment files to purge records as required by data privacy laws like GDPR. Minion tasks can run once or be scheduled to run periodically.

Minions isolate the computational burden of out-of-band data processing from the servers. Although a Pinot cluster can function with or without minions, they are typically present to support routine tasks like batch data ingest.

\
\
