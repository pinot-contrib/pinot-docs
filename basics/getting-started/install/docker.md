---
description: Start a Pinot cluster using Docker containers.
---

# Docker install

## Outcome

Start a multi-component Pinot cluster using Docker, suitable for local evaluation and CI environments.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) installed and running
* Recommended Docker resource settings:
  * CPUs: 8
  * Memory: 16 GB
  * Swap: 4 GB
  * Disk image size: 60 GB

## Steps

### 1. Set the image versions

```bash
export PINOT_VERSION=1.4.0
export PINOT_IMAGE=apachepinot/pinot:${PINOT_VERSION}
export ZK_IMAGE=zookeeper:3.9.2
export KAFKA_IMAGE=bitnami/kafka:3.6
```

See the [Version reference](../pinot-versions.md) page for the current stable release.

### 2. Pull the Pinot image

```bash
docker pull apachepinot/pinot:${PINOT_VERSION}
```

View all available tags on [Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).

### 3. Start the cluster

{% tabs %}
{% tab title="Docker Compose (recommended)" %}
Create a file called `docker-compose.yml` with the following content:

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

  pinot-controller:
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.4.0}
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
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.4.0}
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
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.4.0}
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

  pinot-minion:
    image: ${PINOT_IMAGE:-apachepinot/pinot:1.4.0}
    command: "StartMinion -zkAddress pinot-zookeeper:2181"
    restart: unless-stopped
    container_name: "pinot-minion"
    ports:
      - "6000:6000"
    depends_on:
      - pinot-broker
    networks:
      - pinot-demo

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
      test: ["CMD-SHELL", "kafka-broker-api-versions.sh -bootstrap-server kafka:9092"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s
    deploy:
      replicas: ${KAFKA_REPLICAS:-0}

networks:
  pinot-demo:
    name: pinot-demo
    driver: bridge
```
{% endcode %}

Launch the cluster:

```bash
docker compose --project-name pinot-demo up
```

To also start Kafka for real-time streaming:

```bash
export KAFKA_REPLICAS=1
docker compose --project-name pinot-demo up
```
{% endtab %}

{% tab title="Individual docker run commands" %}
**Create a network**

```bash
docker network create -d bridge pinot-demo
```

**Start ZooKeeper**

```bash
docker run \
    --network=pinot-demo \
    --name pinot-zookeeper \
    --restart always \
    -p 2181:2181 \
    -d ${ZK_IMAGE}
```

**Start Pinot Controller**

```bash
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-controller \
    -p 9000:9000 \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms1G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log" \
    -d ${PINOT_IMAGE} StartController \
    -zkAddress pinot-zookeeper:2181
```

**Start Pinot Broker**

```bash
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-broker \
    -p 8099:8099 \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log" \
    -d ${PINOT_IMAGE} StartBroker \
    -zkAddress pinot-zookeeper:2181
```

**Start Pinot Server**

```bash
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-server \
    -p 8098:8098 \
    -e JAVA_OPTS="-Dplugins.dir=/opt/pinot/plugins -Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log" \
    -d ${PINOT_IMAGE} StartServer \
    -zkAddress pinot-zookeeper:2181
```

**Start Pinot Minion (optional)**

```bash
docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-minion \
    -p 6000:6000 \
    -d ${PINOT_IMAGE} StartMinion \
    -zkAddress pinot-zookeeper:2181
```

**Start Kafka (optional)**

```bash
docker run --rm -ti \
    --network pinot-demo --name=kafka \
    -e KAFKA_ZOOKEEPER_CONNECT=pinot-zookeeper:2181/kafka \
    -e KAFKA_BROKER_ID=0 \
    -e KAFKA_ADVERTISED_HOST_NAME=kafka \
    -p 9092:9092 \
    -d ${KAFKA_IMAGE}
```
{% endtab %}
{% endtabs %}

## Verify

Check that all containers are running:

```bash
docker container ls -a
```

You should see containers for ZooKeeper, Controller, Broker, Server, and Minion all in a healthy state. Open the Pinot Query Console at [http://localhost:9000](http://localhost:9000) to confirm the cluster is ready.

## Next step

Your cluster is running. Continue to [First table and schema](../first-table-and-schema.md) to load data.
