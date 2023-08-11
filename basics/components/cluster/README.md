---
description: >-
  Learn to build and manage Apache Pinot clusters, uncovering key components for
  efficient data processing and optimized analysis.
---

# Cluster

A cluster is a set of nodes comprising of servers, brokers, controllers and minions.

![Pinot cluster components](../../../.gitbook/assets/components.jpg)

Pinot uses [Apache Helix](http://helix.apache.org) for cluster management. Helix is a cluster management framework that manages replicated, partitioned resources in a distributed system. Helix uses Zookeeper to store cluster state and metadata.

## Cluster configuration

For details of cluster configuration settings, see [Cluster configuration reference](https://docs.pinot.apache.org/configuration-reference/cluster).

## Cluster components

Helix divides nodes into logical components based on their responsibilities:

### Participant

Participants are the nodes that host distributed, partitioned resources

Pinot servers are modeled as participants. For details about server nodes, see [Server](server.md).

### Spectator

Spectators are the nodes that observe the current state of each participant and use that information to access the resources. Spectators are notified of state changes in the cluster (state of a participant, or that of a partition in a participant).

Pinot brokers are modeled as spectators. For details about broker nodes, see [Broker](broker.md).

### Controller

The node that observes and controls the Participant nodes. It is responsible for coordinating all transitions in the cluster and ensuring that state constraints are satisfied while maintaining cluster stability.

Pinot controllers are modeled as controllers. For details about controller nodes, see [Controller](controller.md).

## Logical view

Another way to visualize the cluster is a logical view, where:

* A cluster contains [tenants](tenant.md)
* Tenants contain [tables](../table/)
* Tables contain [segments](../table/segment/)

![](../../../.gitbook/assets/ClusterLogical.jpg)

## Set up a Pinot cluster

Typically, there is only one cluster per environment/data center. There is no need to create multiple Pinot clusters because Pinot supports [tenants](tenant.md).&#x20;

To set up a cluster, see one of the following guides:

* [Running Pinot in Docker](../../getting-started/running-pinot-in-docker.md)
* [Running Pinot locally](../../getting-started/running-pinot-locally.md)
