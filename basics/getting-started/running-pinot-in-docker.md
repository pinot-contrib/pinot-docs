---
description: This guide will show you to run a Pinot Cluster using Docker.
---

# Running Pinot in Docker

In this guide we will learn about running Pinot in Docker.

This guide assumes that you have installed [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac) and have configured it with enough memory. A sample config is shown below:

![Sample Docker resources](<../../.gitbook/assets/image (4) (2).png>)

The latest Pinot Docker image is published at `apachepinot/pinot:latest` and you can see a list of [all published tags on Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).

You can pull the Docker image onto your machine by running the following command:

```bash
docker pull apachepinot/pinot:latest
```

Or if you want to use a specific version:

```bash
docker pull apachepinot/pinot:0.9.3
```

Now that we've downloaded the Pinot Docker image, it's time to set up a cluster. There are two ways to do this:

## Quick Start

Pinot comes with quick-start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick-start launches Pinot with a baseball dataset pre-loaded:

```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:0.9.3 QuickStart \
    -type batch
```

For a list of all the available quick starts, see the [Quick Start Examples](quick-start.md).

## Manual Cluster

The quick start scripts launch Pinot with minimal resources. If you want to play with bigger datasets (more than a few MB), you can launch each of the Pinot components individually.

### Docker

#### Create a Network

Create an isolated bridge network in docker

```
docker network create -d bridge pinot-demo
```

#### Start Zookeeper

Start Zookeeper in daemon mode. This is a single node zookeeper setup. Zookeeper is the central metadata store for Pinot and should be set up with replication for production use. For more information, see [Running Replicated Zookeeper](https://zookeeper.apache.org/doc/r3.6.0/zookeeperStarted.html#sc\_RunningReplicatedZooKeeper).

```
docker run \
    --network=pinot-demo \
    --name pinot-zookeeper \
    --restart always \
    -p 2181:2181 \
    -d zookeeper:3.5.6
```

#### Start Pinot Controller

Start Pinot Controller in daemon and connect to Zookeeper.

{% hint style="info" %}
The command below expects a 4GB memory container. Tune`-Xms` and`-Xmx` if your machine doesn't have enough resources.
{% endhint %}

```
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-controller \
    -p 9000:9000 \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms1G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log" \
    -d ${PINOT_IMAGE} StartController \
    -zkAddress pinot-zookeeper:2181
```

#### Start Pinot Broker

Start Pinot Broker in daemon and connect to Zookeeper.

{% hint style="info" %}
The command below expects a 4GB memory container. Tune`-Xms` and`-Xmx` if your machine doesn't have enough resources.
{% endhint %}

```
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-broker \
    -p 8099:8099 \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log" \
    -d ${PINOT_IMAGE} StartBroker \
    -zkAddress pinot-zookeeper:2181
```

#### Start Pinot Server

Start Pinot Server in daemon and connect to Zookeeper.

{% hint style="info" %}
The command below expects a 16GB memory container. Tune`-Xms` and`-Xmx` if your machine doesn't have enough resources.
{% endhint %}

```
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-server \
    -p 8098:8098 \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log" \
    -d ${PINOT_IMAGE} StartServer \
    -zkAddress pinot-zookeeper:2181
```

#### Start Kafka

Optionally, you can also start Kafka for setting up realtime streams. This brings up the Kafka broker on port 9092.

```
docker run --rm -ti \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -p 9092:9092 \
    -d bitnami/kafka:latest
```

Now all Pinot related components are started as an empty cluster.

You can run the below command to check container status.

```
docker container ls -a
```

**Sample Console Output**

```
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS                                                  NAMES
9ec20e4463fa        bitnami/kafka:latest        "start-kafka.sh"         43 minutes ago      Up 43 minutes                                                              kafka
0775f5d8d6bf        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-server
64c6392b2e04        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-broker
b6d0f2bd26a3        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   45 minutes ago      Up 45 minutes       8096-8099/tcp, 0.0.0.0:9000->9000/tcp                  pinot-quickstart
570416fc530e        zookeeper:3.5.6             "/docker-entrypoint.…"   45 minutes ago      Up 45 minutes       2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   pinot-zookeeper
```

### Docker Compose

Create a file called _docker-compose.yml_ that contains the following:

{% code title="docker-compose.yml" %}
```yaml
version: '3.7'
services:
  pinot-zookeeper:
    image: zookeeper:3.5.6
    container_name: pinot-zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
  pinot-controller:
    image: apachepinot/pinot:0.9.3
    command: "StartController -zkAddress pinot-zookeeper:2181"
    container_name: pinot-controller
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms1G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
    depends_on:
      - pinot-zookeeper
  pinot-broker:
    image: apachepinot/pinot:0.9.3
    command: "StartBroker -zkAddress pinot-zookeeper:2181"
    restart: unless-stopped
    container_name: "pinot-broker"
    ports:
      - "8099:8099"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log"
    depends_on:
      - pinot-controller
  pinot-server:
    image: apachepinot/pinot:0.9.3
    command: "StartServer -zkAddress pinot-zookeeper:2181"
    restart: unless-stopped
    container_name: "pinot-server"
    ports:
      - "8098:8098"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
    depends_on:
      - pinot-broker
```
{% endcode %}

Run the following command to launch all the components:

```
docker-compose --project-name pinot-demo up
```

You can run the below command to check container status.

```
docker container ls 
```

**Sample Console Output**

```
CONTAINER ID   IMAGE                     COMMAND                  CREATED              STATUS              PORTS                                                                     NAMES
ba5cb0868350   apachepinot/pinot:0.9.3   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8099/tcp, 9000/tcp                                                   pinot-server
698f160852f9   apachepinot/pinot:0.9.3   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8098/tcp, 9000/tcp, 0.0.0.0:8099->8099/tcp, :::8099->8099/tcp        pinot-broker
b1ba8cf60d69   apachepinot/pinot:0.9.3   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8099/tcp, 0.0.0.0:9000->9000/tcp, :::9000->9000/tcp                  pinot-controller
54e7e114cd53   zookeeper:3.5.6           "/docker-entrypoint.…"   About a minute ago   Up About a minute   2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, :::2181->2181/tcp, 8080/tcp   pinot-zookeeper
```

Once your cluster is up and running, you can head over to [Exploring Pinot](../components/exploring-pinot.md) to learn how to run queries against the data.

{% hint style="info" %}
If you have [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) or [Docker Kubernetes](https://www.docker.com/products/kubernetes) installed, you could also try running the [Kubernetes quick start](kubernetes-quickstart.md).
{% endhint %}

<mark style="color:red;">Note:</mark> These are sample configs to be used as reference. For production setup, you may want to customize it to your needs.
