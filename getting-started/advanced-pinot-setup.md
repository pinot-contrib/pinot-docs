---
description: Setup Pinot by starting each component individually
---

# Advanced Pinot Setup

## Start Pinot components \(scripts or docker images\)

{% tabs %}
{% tab title="Using docker images" %}
## Start Pinot Components using docker 

### Pull docker image

You can try out pre-built Pinot all-in-one docker image.

```text
export PINOT_VERSION=0.10.0
export PINOT_IMAGE=apachepinot/pinot:${PINOT_VERSION}
docker pull ${PINOT_IMAGE}
```

\(Optional\) You can also follow the instructions [here](../misc/build-docker-images.md) to build your own images.

### 0. Create a Network

Create an isolated bridge network in docker

```text
docker network create -d bridge pinot-demo
```

### 1. Start Zookeeper

Start Zookeeper in daemon mode. This is a single node zookeeper setup. Zookeeper is the central metadata store for Pinot and should be set up with replication for production use. See [https://zookeeper.apache.org/doc/r3.6.0/zookeeperStarted.html\#sc\_RunningReplicatedZooKeeper](https://zookeeper.apache.org/doc/r3.6.0/zookeeperStarted.html#sc_RunningReplicatedZooKeeper) for more information.

```text
docker run \
    --network=pinot-demo \
    --name  pinot-zookeeper \
    --restart always \
    -p 2181:2181 \
    -d zookeeper:3.5.6
```

Start  [ZKUI](https://github.com/DeemOpen/zkui) to browse Zookeeper data at [http://localhost:9090](http://localhost:9090).

```text
docker run --rm -ti \
	--network pinot-demo --name=zkui \
	-p 9090:9090 \
	-e ZK_SERVER=pinot-zookeeper:2181 \
	-d qnib/plain-zkui:latest
```

Alternately, you can use [Zooinspector](https://github.com/zzhang5/zooinspector).

### 2. Start Pinot Controller

Start Pinot Controller in daemon and connect to Zookeeper.

```text
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-controller \
    -p 9000:9000 \
    -d ${PINOT_IMAGE} StartController \
    -zkAddress pinot-zookeeper:2181
```

### 3. Start Pinot Broker

Start Pinot Broker in daemon and connect to Zookeeper.

```text
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-broker \
    -d ${PINOT_IMAGE} StartBroker \
    -zkAddress pinot-zookeeper:2181
```

### 4. Start Pinot Server

Start Pinot Server in daemon and connect to Zookeeper.

```text
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-server \
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

You can run below command to check container status.

```text
docker container ls -a
```

**Sample Console Output**

```text
CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS                                                  NAMES
9ec20e4463fa        wurstmeister/kafka:latest   "start-kafka.sh"         43 minutes ago      Up 43 minutes                                                              kafka
0775f5d8d6bf        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-server
64c6392b2e04        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   44 minutes ago      Up 44 minutes       8096-8099/tcp, 9000/tcp                                pinot-broker
b6d0f2bd26a3        apachepinot/pinot:latest    "./bin/pinot-admin.s…"   45 minutes ago      Up 45 minutes       8096-8099/tcp, 0.0.0.0:9000->9000/tcp                  pinot-controller
570416fc530e        zookeeper:3.5.6             "/docker-entrypoint.…"   45 minutes ago      Up 45 minutes       2888/tcp, 3888/tcp, 0.0.0.0:2181->2181/tcp, 8080/tcp   pinot-zookeeper
```
{% endtab %}

{% tab title="Using launcher scripts" %}
{% hint style="info" %}
Prerequisites

Follow instruction in [Getting Pinot](./) to get Pinot
{% endhint %}

## Start Pinot components via launcher scripts

### 1. Start Zookeeper

```text
cd apache-pinot-${PINOT_VERSION}-bin
bin/pinot-admin.sh StartZookeeper \
  -zkPort 2191
```

You can use [Zooinspector](https://github.com/zzhang5/zooinspector) to browse the Zookeeper instance.

### 2. Start Pinot Controller

```text
bin/pinot-admin.sh StartController \
    -zkAddress localhost:2191 \
    -controllerPort 9000
```

### 3. Start Pinot Broker

```text
bin/pinot-admin.sh StartBroker \
    -zkAddress localhost:2191
```

### 4. Start Pinot Server

```text
bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2191
```

### 5. Start Kafka

```text
bin/pinot-admin.sh  StartKafka \ 
  -zkAddress=localhost:2191/kafka \
  -port 19092
```

Now all Pinot related components are started as an empty cluster.
{% endtab %}
{% endtabs %}

Now it's time to start adding data to the cluster. Check out some of the [Recipes](recipes/) or follow the [Batch upload sample data](pushing-your-data-to-pinot.md) and [Stream sample data](pushing-your-streaming-data-to-pinot.md) for instructions on loading your own data.

