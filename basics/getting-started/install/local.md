---
description: Start a Pinot cluster on your local machine.
---

# Local install

## Outcome

Start a multi-component Pinot cluster directly on your machine without containers.

## Prerequisites

* JDK 21 or later (required for building and running Pinot services)
* Apache Maven 3.6+ (only if building from source)

{% hint style="info" %}
**Note:** The SPI and Java/JDBC client modules (`pinot-spi`, `pinot-java-client`, `pinot-jdbc-client`) remain compatible with Java 11 for external JVM consumers.
{% endhint %}

## Steps

### 1. Download or build Apache Pinot

{% tabs %}
{% tab title="Download release" %}
```bash
export PINOT_VERSION=1.4.0

wget https://downloads.apache.org/pinot/apache-pinot-${PINOT_VERSION}/apache-pinot-${PINOT_VERSION}-bin.tar.gz
```

See the [Version reference](../pinot-versions.md) page for the current stable release.

Extract and enter the directory:

```bash
tar -zxvf apache-pinot-${PINOT_VERSION}-bin.tar.gz
cd apache-pinot-${PINOT_VERSION}-bin
```
{% endtab %}

{% tab title="Build from source" %}
{% hint style="info" %}
**Prerequisite:** Install [Apache Maven](https://maven.apache.org/install.html) 3.6 or higher.
{% endhint %}

```bash
git clone https://github.com/apache/pinot.git
cd pinot
mvn install package -DskipTests -Pbin-dist
cd build
```
{% endtab %}

{% tab title="Homebrew" %}
```bash
brew install pinot
```
{% endtab %}
{% endtabs %}

### 2. Start ZooKeeper

```bash
./bin/pinot-admin.sh StartZookeeper \
  -zkPort 2181
```

### 3. Start Pinot Controller

```bash
export JAVA_OPTS="-Xms4G -Xmx8G"
./bin/pinot-admin.sh StartController \
    -zkAddress localhost:2181 \
    -controllerPort 9000
```

### 4. Start Pinot Broker

```bash
export JAVA_OPTS="-Xms4G -Xmx4G"
./bin/pinot-admin.sh StartBroker \
    -zkAddress localhost:2181
```

### 5. Start Pinot Server

```bash
export JAVA_OPTS="-Xms4G -Xmx16G"
./bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2181
```

### 6. Start Pinot Minion (optional)

```bash
export JAVA_OPTS="-Xms4G -Xmx4G"
./bin/pinot-admin.sh StartMinion \
    -zkAddress localhost:2181
```

### 7. Start Kafka (optional)

Only needed if you plan to ingest real-time streaming data.

```bash
./bin/pinot-admin.sh StartKafka \
  -zkAddress=localhost:2181/kafka \
  -port 19092
```

## Verify

Check that the Controller is healthy:

```bash
curl localhost:9000/health
```

The response should return `OK`. You can also open the Pinot Query Console at [http://localhost:9000](http://localhost:9000).

## Next step

Your cluster is running. Continue to [First table and schema](../first-table-and-schema.md) to load data.
