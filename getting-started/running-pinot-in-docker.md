---
description: Pinot Quickstart in Docker
---

# Running Pinot in Docker

{% hint style="info" %}
**Prerequisites**

Install [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

You can also try [Kubernetes Quickstart](kubernetes-quickstart.md) if you already have a local [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) cluster installed or [docker kubernetes ](https://www.docker.com/products/kubernetes)setup.
{% endhint %}

Create an isolated bridge network in docker

```text
docker network create -d bridge pinot-demo
```

We'll be running a docker image `apachepinot/pinot:latest` to run a quick start, which does the following:

1. Sets up the Pinot cluster `QuickStartCluster`
2. Creates a sample table and loads sample data

There's 3 types of quick start

### Batch

This demo

1. Starts Pinot deployment by starting: 
   1. Apache Zookeeper
   2. Pinot Controller
   3. Pinot Broker
   4. Pinot Server
2. Creates a demo table:
   * baseballStats
3. Launches a standalone data ingestion job
   * build one Pinot segment for a given csv data file for table **baseballStats**
   * push built segment to Pinot controller
4. Issues sample queries to Pinot

```bash
docker run \
    --network=pinot-demo \
    --name pinot-quickstart \
    -p 9000:9000 \
    -d apachepinot/pinot:latest QuickStart \
    -type batch
```

Once docker container is running, you can view the logs by

```text
docker logs pinot-quickstart -f
```

That's it! We've spun up a Pinot cluster. 

It may take a while for all Pinot components to start and for the sample data to be loaded. Use the below command to check the container logs

```text
docker logs pinot-quickstart -f
```

Your cluster is ready once you saw the cluster setup completion messages and some sample queries shown up like below:

![Cluster Setup Completion Example ](../.gitbook/assets/image.png)

You can head over to  [Exploring Pinot](exploring-pinot.md) to check out the data in the `baseballStats` table.

### Streaming

This demo

1. Starts Pinot deployment by starting: 
   * Apache Kafka
   * Apache Zookeeper
   * Pinot Controller
   * Pinot Broker
   * Pinot Server
2. Creates a demo table:
   * meetupRsvp
3. Launches a **meetup** stream and publish data to a Kafka: **meetupRSVPEvents** to be subscribed by Pinot
4. Issues sample queries to Pinot

```bash
# stop previous container, if any, or use different network
docker run \
    --network=pinot-demo \
    --name pinot-quickstart \
    -p 9000:9000 \
    -d apachepinot/pinot:latest QuickStart \
    -type stream
```

Once the cluster is up, you can head over to  [Exploring Pinot](exploring-pinot.md) to check out the data in the `meetupRSVPEvents` table.

### Hybrid

This demo

1. Starts Pinot deployment by starting: 
   * Apache Kafka
   * Apache Zookeeper
   * Pinot Controller
   * Pinot Broker
   * Pinot Server
2. Creates a demo table:
   * airlineStats
3. Launches a standalone data ingestion job:
   * build Pinot segments under a given directory of Avro files for table **airlineStats**
   * push built segments to Pinot controller
4. Launches a ****stream of flights stats and publish data to a Kafka topic **airlineStatsEvents** to be subscribed by Pinot
5. Issues sample queries to Pinot 

```bash
# stop previous container, if any, or use different network
docker run \
    --network=pinot-demo \
    --name pinot-quickstart \
    -p 9000:9000 \
    -d apachepinot/pinot:latest QuickStart \
    -type hybrid
```

Once the cluster is up, you can head over to  [Exploring Pinot](exploring-pinot.md) to check out the data in the `airlineStats` table.

