---
description: This guide will show you to run a Pinot cluster using Docker.
---

# Running Pinot in Docker

Get started setting up a Pinot cluster with Docker using the guide below.

**Prerequisites:**

* Install [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac)
* Configure Docker memory with the following minimum resources:
  * CPUs: 8
  * Memory: 16.00 GB
  * Swap: 4 GB
  * Disk Image size: 60 GB

The latest Pinot Docker image is published at `apachepinot/pinot:latest`. View a list of [all published tags on Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).

Pull the latest Docker image onto your machine by running the following command:

```bash
docker pull apachepinot/pinot:latest
```

To pull a specific version, modify the command like below:

```bash
docker pull apachepinot/pinot:0.12.0
```

## Set up a cluster

Once you've downloaded the Pinot Docker image, it's time to set up a cluster. There are two ways to do this.

### Quick start

Pinot comes with quick start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick start command launches Pinot with a baseball dataset pre-loaded:

```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:0.12.0 QuickStart \
    -type batch
```

For a list of all available quick start commands, see [Quick Start Examples](quick-start.md).

### Manual cluster

The quick start scripts launch Pinot with minimal resources. If you want to play with bigger datasets (more than a few MB), you can launch each of the Pinot components individually.

{% hint style="info" %}
Note that these are sample configurations to be used as references. You will likely want to customize them to meet your needs for production use.
{% endhint %}

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

Optionally, you can also start Kafka for setting up real-time streams. This brings up the Kafka broker on port 9092.

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

Run the below command to check container status:

```
docker container ls -a
```

**Sample Console Output**

```
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS                                                  NAMES
9ec20e4463fa        bitnami/kafka:latest        "start-kafka.sh"         43 minutes ago      Up 43 minutes                                                              kafka
0775f5d8d6bf        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-server
64c6392b2e04        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-broker
b6d0f2bd26a3        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   45 minutes ago      Up 45 minutes       8096-8099/tcp, 0.0.0.0:9000->9000/tcp                  pinot-controller
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
    image: apachepinot/pinot:0.12.0
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
    image: apachepinot/pinot:0.12.0
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
    image: apachepinot/pinot:0.12.0
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

Run the below command to check the container status:

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

Once your cluster is up and running, see [Exploring Pinot](../components/exploring-pinot.md) to learn how to run queries against the data.

If you have [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) or [Docker Kubernetes](https://www.docker.com/products/kubernetes) installed, you can also try running the [Kubernetes quick start](kubernetes-quickstart.md).
