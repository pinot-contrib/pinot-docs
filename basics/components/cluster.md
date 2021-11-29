# Cluster

Cluster is a set of nodes comprising of servers, brokers, controllers and minions.

![Pinot cluster components](../../.gitbook/assets/components.jpg)

Pinot uses [Apache Helix](http://helix.apache.org) for cluster management. Helix is a cluster management framework that manages replicated, partitioned resources in a distributed system. Helix uses Zookeeper to store cluster state and metadata.

### Cluster components

Helix divides nodes into logical components based on their responsibilities:

#### Participant

The nodes that host distributed, partitioned resources

_**Pinot Servers**_ are modeled as Participants. For more details about server nodes, see [Server](server.md).

#### Spectator

The nodes that observe the current state of each Participant and use that information to access the resources. Spectators are notified of state changes in the cluster (state of a participant, or that of a partition in a participant).

_**Pinot Brokers**_ are modeled as Spectators. For more details about broker nodes, see [Broker](broker.md).

#### Controller

The node that observes and controls the Participant nodes. It is responsible for coordinating all transitions in the cluster and ensuring that state constraints are satisfied while maintaining cluster stability_._

_**Pinot Controllers**_ are modeled as Controllers. For more details about controller nodes, see [Controller](controller.md).

### Logical view

Another way to visualize the cluster is a logical view, wherein a cluster contains [tenants](tenant.md), tenants contain [tables](table.md), and tables contain [segments](segment.md).

![](../../.gitbook/assets/clusterlogical.jpg)

## Setup a Pinot Cluster

Typically, there is only one cluster per environment/data center. There is no need to create multiple Pinot clusters since Pinot supports the concept of [tenants](tenant.md). At LinkedIn, the largest Pinot cluster consists of 1000+ nodes.

To set up a cluster, see one of the following guides:

* [Running Pinot in Docker](../getting-started/running-pinot-in-docker.md)
* [Running Pinot locally](../getting-started/running-pinot-locally.md)
