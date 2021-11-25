---
description: This quick start guide will show you how to set up a Pinot cluster manually.
---

# Manual cluster setup

## Start Pinot components (scripts or Docker images)

A manual cluster setup consists of the following components -\
1\. Zookeeper\
2\. Controller\
3\. Broker\
4\. Server\
5\. Kafka

We will run each of these components in separate containers

{% tabs %}
{% tab title="Docker" %}
## Start Pinot Components using Docker

### **Prerequisites**

{% hint style="info" %}
If running locally, please ensure your docker cluster has enough resources, below is a sample config.
{% endhint %}

![Sample docker resources](<../../.gitbook/assets/image (4) (1).png>)

### Pull docker image

You can try out the pre-built Pinot all-in-one docker image.

```
export PINOT_VERSION=0.9.0
export PINOT_IMAGE=apachepinot/pinot:${PINOT_VERSION}
docker pull ${PINOT_IMAGE}
```

(Optional) You can also follow the instructions [here](../../operators/tutorials/build-docker-images.md) to build your own images.

### 0. Create a Network

Create an isolated bridge network in docker

```
docker network create -d bridge pinot-demo
```

### 1. Start Zookeeper

Start Zookeeper in daemon mode. This is a single node zookeeper setup. Zookeeper is the central metadata store for Pinot and should be set up with replication for production use. For more information, see [Running Replicated Zookeeper](https://zookeeper.apache.org/doc/r3.6.0/zookeeperStarted.html#sc\_RunningReplicatedZooKeeper).&#x20;

```
docker run \
    --network=pinot-demo \
    --name  pinot-zookeeper \
    --restart always \
    -p 2181:2181 \
    -d zookeeper:3.5.6
```

### 2. Start Pinot Controller

Start Pinot Controller in daemon and connect to Zookeeper.

{% hint style="info" %}
The command below expects a 4GB memory container. Please tune`-Xms` and`-Xmx` if your machine doesn't have enough resources.
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

### 3. Start Pinot Broker

Start Pinot Broker in daemon and connect to Zookeeper.

{% hint style="info" %}
The command below expects a 4GB memory container. Please tune`-Xms` and`-Xmx` if your machine doesn't have enough resources.
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

### 4. Start Pinot Server

Start Pinot Server in daemon and connect to Zookeeper.

{% hint style="info" %}
The command below expects a 16GB memory container. Please tune`-Xms` and`-Xmx` if your machine doesn't have enough resources.
{% endhint %}

```
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-server \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log" \
    -d ${PINOT_IMAGE} StartServer \
    -zkAddress pinot-zookeeper:2181
```

### **5. Start Kafka**

Optionally, you can also start Kafka for setting up realtime streams. This brings up the Kafka broker on port 9092.

```
docker run --rm -ti \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -d wurstmeister/kafka:latest
```

Now all Pinot related components are started as an empty cluster.

You can run the below command to check container status.

```
docker container ls -a
```

**Sample Console Output**

```
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS                                                  NAMES
9ec20e4463fa        wurstmeister/kafka:latest   "start-kafka.sh"         43 minutes ago      Up 43 minutes                                                              kafka
0775f5d8d6bf        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-server
64c6392b2e04        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-broker
b6d0f2bd26a3        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   45 minutes ago      Up 45 minutes       8096-8099/tcp, 0.0.0.0:9000->9000/tcp                  pinot-quickstart
570416fc530e        zookeeper:3.5.6             "/docker-entrypoint.…"   45 minutes ago      Up 45 minutes       2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   pinot-zookeeper
```
{% endtab %}

{% tab title="Docker Compose" %}
## Start Pinot Components using Docker Compose

### **Prerequisites**

{% hint style="info" %}
If running locally, please ensure your docker cluster has enough resources, below is a sample config.
{% endhint %}

![Sample docker resources](<../../.gitbook/assets/image (4) (1).png>)

Create a file called _docker-compose.yml_ that contains the following:

{% code title="docker-compose.yml" %}
```yaml
version: '3.7'
services:
  zookeeper:
    image: zookeeper:3.5.6
    hostname: zookeeper
    container_name: manual-zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
  pinot-controller:
    image: apachepinot/pinot:0.9.0
    command: "StartController -zkAddress manual-zookeeper:2181"
    container_name: "manual-pinot-controller"
    restart: unless-stopped
    ports:
      - "9000:9000"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms1G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
    depends_on:
      - zookeeper
  pinot-broker:
    image: apachepinot/pinot:0.9.0
    command: "StartBroker -zkAddress manual-zookeeper:2181"
    restart: unless-stopped
    container_name: "manual-pinot-broker"
    ports:
      - "8099:8099"
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log"
    depends_on:
      - pinot-controller
  pinot-server:
    image: apachepinot/pinot:0.9.0
    command: "StartServer -zkAddress manual-zookeeper:2181"
    restart: unless-stopped
    container_name: "manual-pinot-server" 
    environment:
      JAVA_OPTS: "-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
    depends_on:
      - pinot-broker
  
```
{% endcode %}

Run `docker-compose up` to launch all the components.&#x20;

You can run the below command to check container status.

```
docker container ls 
```

**Sample Console Output**

```
CONTAINER ID   IMAGE                     COMMAND                  CREATED              STATUS              PORTS                                                                     NAMES
ba5cb0868350   apachepinot/pinot:0.9.0   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8099/tcp, 9000/tcp                                                   manual-pinot-server
698f160852f9   apachepinot/pinot:0.9.0   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8098/tcp, 9000/tcp, 0.0.0.0:8099->8099/tcp, :::8099->8099/tcp        manual-pinot-broker
b1ba8cf60d69   apachepinot/pinot:0.9.0   "./bin/pinot-admin.s…"   About a minute ago   Up About a minute   8096-8099/tcp, 0.0.0.0:9000->9000/tcp, :::9000->9000/tcp                  manual-pinot-controller
54e7e114cd53   zookeeper:3.5.6           "/docker-entrypoint.…"   About a minute ago   Up About a minute   2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, :::2181->2181/tcp, 8080/tcp   manual-zookeeper
```
{% endtab %}

{% tab title="Using launcher scripts" %}
{% hint style="info" %}
Prerequisites

Download pinot by following the instructions in [Getting Pinot](./).
{% endhint %}

## Start Pinot components via launcher scripts

### 1. Start Zookeeper

```
cd apache-pinot-${PINOT_VERSION}-bin
bin/pinot-admin.sh StartZookeeper \
  -zkPort 2191
```

You can use [Zooinspector](https://github.com/zzhang5/zooinspector) to browse the Zookeeper instance.

### 2. Start Pinot Controller

{% hint style="info" %}
The examples below are for Java 8 users.

For Java 11+ users, remove the GC settings inside`JAVA_OPTS.` So it looks like: `export JAVA_OPTS="-Xms4G -Xmx8G"`
{% endhint %}

```
export JAVA_OPTS="-Xms4G -Xmx8G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
bin/pinot-admin.sh StartController \
    -zkAddress localhost:2191 \
    -controllerPort 9000
```

### 3. Start Pinot Broker

```
export JAVA_OPTS="-Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log"
bin/pinot-admin.sh StartBroker \
    -zkAddress localhost:2191
```

### 4. Start Pinot Server

```
export JAVA_OPTS="-Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2191
```

### 5. Start Kafka

```
bin/pinot-admin.sh  StartKafka \ 
  -zkAddress=localhost:2191/kafka \
  -port 19092
```

Now all Pinot related components are started as an empty cluster.
{% endtab %}
{% endtabs %}

Now it's time to start adding data to the cluster. Check out some of the [Recipes](../recipes/) or follow the [Batch upload sample data](pushing-your-data-to-pinot.md) and [Stream sample data](pushing-your-streaming-data-to-pinot.md) for instructions on loading your own data.
