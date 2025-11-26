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
docker pull apachepinot/pinot:1.2.0
```

## Set up a cluster

Once you've downloaded the Pinot Docker image, it's time to set up a cluster. There are two ways to do this.

### Quick start

Pinot comes with quick start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick start command launches Pinot with a baseball dataset pre-loaded:

```
docker run \
    -p 2123:2123 \
    -p 9000:9000 \
    -p 8000:8000 \
    -p 7050:7050 \
    -p 6000:6000 \
    apachepinot/pinot:1.2.0 QuickStart \
    -type batch
```

For a list of all available quick start commands, see [Quick Start Examples](quick-start.md).

{% hint style="warning" %}
Below are the usages of different ports:

2123: Zookeeper Port

9000: Pinot Controller Port

8000: Pinot Broker Port

7050: Pinot Server Port

6000: Pinot Minion Port
{% endhint %}

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

#### Export Docker Image tags

Export the necessary docker image tags for Pinot, Zookeeper, and Kafka.

```
export PINOT_IMAGE=apachepinot/pinot:1.2.0
export ZK_IMAGE=zookeeper:3.9.2
export KAFKA_IMAGE= bitnami/kafka:3.6
```

#### Start Zookeeper

Start Zookeeper in daemon mode. This is a single node zookeeper setup. Zookeeper is the central metadata store for Pinot and should be set up with replication for production use. For more information, see [Running Replicated Zookeeper](https://zookeeper.apache.org/doc/r3.6.0/zookeeperStarted.html#sc\_RunningReplicatedZooKeeper).

```
docker run \
    --network=pinot-demo \
    --name pinot-zookeeper \
    --restart always \
    -p 2181:2181 \
    -d ${ZK_IMAGE}
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
    -d ${KAFKA_IMAGE}
```

Now all Pinot related components are started as an empty cluster.

Run the below command to check container status:

```
docker container ls -a
```

**Sample Console Output**

```
CONTAINER ID   IMAGE                     COMMAND                  CREATED              STATUS              PORTS                                                       NAMES
accc70bc7f07   bitnami/kafka:3.6         "/opt/bitnami/script…"   About a minute ago   Up About a minute   0.0.0.0:9092->9092/tcp                                      kafka
1b8b80395959   apachepinot/pinot:1.2.0   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8097/tcp, 8099/tcp, 9000/tcp, 0.0.0.0:8098->8098/tcp   pinot-server
134a67eec957   apachepinot/pinot:1.2.0   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8098/tcp, 9000/tcp, 0.0.0.0:8099->8099/tcp             pinot-broker
4fcc72cb7302   apachepinot/pinot:1.2.0   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8099/tcp, 0.0.0.0:9000->9000/tcp                       pinot-controller
144304524f6c   zookeeper:3.9.2           "/docker-entrypoint.…"   About a minute ago   Up About a minute   2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp        pinot-zookeeper
```

### Docker Compose

#### Export Docker Image tags

Optionally, export the necessary docker image tags for Pinot, Zookeeper, and Kafka.

```
export PINOT_IMAGE=apachepinot/pinot:1.2.0
export ZK_IMAGE=zookeeper:3.9.2
export KAFKA_IMAGE=bitnami/kafka:3.6
```

#### Create _docker-compose.yml_ file
Create a file called _docker-compose.yml_ that contains the following:

{% code title="docker-compose.yml" %}
```yaml
version: '3.7'

services:
  pinot-zookeeper:
    image: ${ZK_IMAGE:-zookeeper:3.9.2}
    container_name: "pinot-zookeeper"
    restart: unless-stopped
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    networks:
      - pinot-demo
    healthcheck:
      test: ["CMD", "zkServer.sh", "status"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s

  pinot-kafka:
    image: ${KAFKA_IMAGE:-bitnami/kafka:3.6}
    container_name: "kafka"
    restart: unless-stopped
    ports:
      - "9092:9092"
    environment:
      KAFKA_ZOOKEEPER_CONNECT: pinot-zookeeper:2181/kafka
      KAFKA_BROKER_ID: 0
      KAFKA_ADVERTISED_HOST_NAME: kafka
    depends_on:
      pinot-zookeeper:
        condition: service_healthy
    networks:
      - pinot-demo
    healthcheck:
      test: [ "CMD-SHELL", "kafka-broker-api-versions.sh -bootstrap-server kafka:9092" ]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s
    deploy:
      replicas: ${KAFKA_REPLICAS:-0}  # Default to 0, meaning Kafka won't start unless KAFKA_REPLICAS is set

  pinot-controller:
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.2.0}
    command: "StartController -zkAddress pinot-zookeeper:2181"
    container_name: "pinot-controller"
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms1G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
    depends_on:
      pinot-zookeeper:
        condition: service_healthy
    networks:
      - pinot-demo
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9000/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s

  pinot-broker:
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.2.0}
    command: "StartBroker -zkAddress pinot-zookeeper:2181"
    container_name: "pinot-broker"
    restart: unless-stopped
    ports:
      - "8099:8099"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log"
    depends_on:
      pinot-controller:
        condition: service_healthy
    networks:
      - pinot-demo
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8099/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s

  pinot-server:
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.2.0}
    command: "StartServer -zkAddress pinot-zookeeper:2181"
    container_name: "pinot-server"
    restart: unless-stopped
    ports:
      - "8098:8098"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
    depends_on:
      pinot-broker:
        condition: service_healthy
    networks:
      - pinot-demo
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8097/health/readiness || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s

networks:
  pinot-demo:
    name: pinot-demo
    driver: bridge
```
{% endcode %}

#### Launch the components
Run the following command to launch all the required components:

```
docker compose --project-name pinot-demo up
```

OR, optionally, run the following command to launch all the components, including kafka:
```
export KAFKA_REPLICAS=1
docker compose --project-name pinot-demo up
```
Run the below command to check the container status:

```
docker container ls -a
```

**Sample Console Output**

```
CONTAINER ID   IMAGE                     COMMAND                  CREATED          STATUS                        PORTS                                                       NAMES
f34a046ac69f   bitnami/kafka:3.6         "/opt/bitnami/script…"   9 minutes ago    Up About a minute (healthy)   0.0.0.0:9092->9092/tcp                                      kafka
f28021bd5b1d   apachepinot/pinot:1.2.0   "./bin/pinot-admin.s…"   18 minutes ago   Up About a minute (healthy)   8096-8097/tcp, 8099/tcp, 9000/tcp, 0.0.0.0:8098->8098/tcp   pinot-server
e938453054b0   apachepinot/pinot:1.2.0   "./bin/pinot-admin.s…"   18 minutes ago   Up About a minute (healthy)   8096-8098/tcp, 9000/tcp, 0.0.0.0:8099->8099/tcp             pinot-broker
e0d0c71303a8   apachepinot/pinot:1.2.0   "./bin/pinot-admin.s…"   18 minutes ago   Up About a minute (healthy)   8096-8099/tcp, 0.0.0.0:9000->9000/tcp                       pinot-controller
4be5f168f252   zookeeper:3.9.2           "/docker-entrypoint.…"   18 minutes ago   Up About a minute (healthy)   2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp        pinot-zookeeper
```

Once your cluster is up and running, see [Exploring Pinot](../components/exploring-pinot.md) to learn how to run queries against the data.

If you have [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) or [Docker Kubernetes](https://www.docker.com/products/kubernetes) installed, you can also try running the [Kubernetes quick start](kubernetes-quickstart.md).
