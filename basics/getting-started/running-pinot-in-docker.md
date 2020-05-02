---
description: This quick start guide will show you how to run a Pinot cluster using Docker.
---

# Running Pinot in Docker

{% hint style="info" %}
**Prerequisites**

Install [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

You can also try [Kubernetes quick start](kubernetes-quickstart.md) if you already have a local [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) cluster installed or [Docker Kubernetes](https://www.docker.com/products/kubernetes) setup.
{% endhint %}

Create an isolated bridge network in docker

```text
docker network create -d bridge pinot-demo
```

We'll be using our docker image `apachepinot/pinot:latest` to run this quick start, which does the following:

* Sets up the Pinot cluster
* Creates a sample table and loads sample data

There are 3 types of quick start examples.

* Batch example
* Streaming example
* Hybrid example

## Batch example

In this example we demonstrate how to do batch processing with Pinot.

* Starts Pinot deployment by starting
  * Apache Zookeeper
  * Pinot Controller
  * Pinot Broker
  * Pinot Server
* Creates a demo table
  * `baseballStats`
* Launches a standalone data ingestion job
  * Builds one Pinot segment for a given CSV data file for table `baseballStats`
  * Pushes the built segment to the Pinot controller
* Issues sample queries to Pinot

```bash
docker run \
    --network=pinot-demo \
    --name pinot-quickstart \
    -p 9000:9000 \
    -d apachepinot/pinot:latest QuickStart \
    -type batch
```

Once the Docker container is running, you can view the logs by running the following command.

```text
docker logs pinot-quickstart -f
```

That's it! We've spun up a Pinot cluster. 

{% hint style="info" %}
It may take a while for all the Pinot components to start and for the sample data to be loaded. 

Use the below command to check the status in the container logs.
{% endhint %}

```text
docker logs pinot-quickstart -f
```

Your cluster is ready once you see the cluster setup completion messages and sample queries, as demonstrated below.

![Cluster Setup Completion Example ](../../.gitbook/assets/image%20%281%29.png)

You can head over to [Exploring Pinot](../../features/exploring-pinot.md) to check out the data in the `baseballStats` table.

## Streaming example

In this example we demonstrate how to do stream processing with Pinot.

* Starts Pinot deployment by starting
  * Apache Kafka
  * Apache Zookeeper
  * Pinot Controller
  * Pinot Broker
  * Pinot Server
* Creates a demo table
  * `meetupRsvp`
* Launches a `meetup` ****stream
* Publishes data to a Kafka topic `meetupRSVPEvents` to be subscribed to by Pinot
* Issues sample queries to Pinot

```bash
# stop previous container, if any, or use different network
docker run \
    --network=pinot-demo \
    --name pinot-quickstart \
    -p 9000:9000 \
    -d apachepinot/pinot:latest QuickStart \
    -type stream
```

Once the cluster is up, you can head over to  [Exploring Pinot](../../features/exploring-pinot.md) to check out the data in the `meetupRSVPEvents` table.

## Hybrid example

In this example we demonstrate how to do hybrid stream and batch processing with Pinot.

1. Starts Pinot deployment by starting
   * Apache Kafka
   * Apache Zookeeper
   * Pinot Controller
   * Pinot Broker
   * Pinot Server
2. Creates a demo table
   * `airlineStats`
3. Launches a standalone data ingestion job
   * Builds Pinot segments under a given directory of Avro files for table `airlineStats`
   * Pushes built segments to Pinot controller
4. Launches a ****stream of flights stats
5. Publishes data to a Kafka topic `airlineStatsEvents` to be subscribed to by Pinot
6. Issues sample queries to Pinot 

```bash
# stop previous container, if any, or use different network
docker run \
    --network=pinot-demo \
    --name pinot-quickstart \
    -p 9000:9000 \
    -d apachepinot/pinot:latest QuickStart \
    -type hybrid
```

Once the cluster is up, you can head over to  [Exploring Pinot](../../features/exploring-pinot.md) to check out the data in the `airlineStats` table.

