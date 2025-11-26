---
description: >-
  This quick start guide will help you bootstrap a Pinot standalone instance on
  your local machine.
---

# Running Pinot locally

In this guide, you'll learn how to download and install Apache Pinot as a standalone instance.

* [Download Apache Pinot](running-pinot-locally.md#download-apache-pinot)
* [Set up a cluster](running-pinot-locally.md#set-up-a-cluster)
* [Start a Pinot component in debug mode with IntelliJ](running-pinot-locally.md#start-a-pinot-component-in-debug-mode-with-intellij)

## Download Apache Pinot

First, download the Pinot distribution for this tutorial. You can either download a packaged release or build a distribution from the source code.

### Prerequisites

* Install with JDK 11 or 21. JDK 17 should work, but it is not officially supported.
* For JDK 8 support, Pinot 0.12.1 is the last version compilable from the source code.
* Pinot 1.0+ doesn't support JDK 8 anymore, build with JDK 11+

Note that some installations of the JDK do not contain the JNI bindings necessary to run all tests. If you see an error like `java.lang.UnsatisfiedLinkError` while running tests, you might need to change your JDK.

Download the distribution or build from source by selecting one of the following tabs:

{% tabs %}
{% tab title="Download the release" %}
Download the latest binary release from [Apache Pinot](https://pinot.apache.org/download), or use this command:

```bash
PINOT_VERSION=1.1.0 #set to the Pinot version you decide to use

wget https://downloads.apache.org/pinot/apache-pinot-$PINOT_VERSION/apache-pinot-$PINOT_VERSION-bin.tar.gz
```

Extract the TAR file:

```
tar -zxvf apache-pinot-$PINOT_VERSION-bin.tar.gz
```

Navigate to the directory containing the launcher scripts:

```
cd apache-pinot-$PINOT_VERSION-bin
```

You can also find older versions of Apache Pinot at [https://archive.apache.org/dist/pinot/](https://archive.apache.org/dist/pinot/apache-pinot-0.11.0/). For example, to download Pinot 0.10.0, run the following command:

```
OLDER_VERSION="0.10.0"
wget https://archive.apache.org/dist/pinot/apache-pinot-$OLDER_VERSION/apache-pinot-$OLDER_VERSION-bin.tar.gz
```
{% endtab %}

{% tab title="Build from source " %}
Follow these steps to checkout code from [Github](https://github.com/apache/pinot) and build Pinot locally

{% hint style="info" %}
**Prerequisites**

Install [Apache Maven](https://maven.apache.org/install.html) 3.6 or higher
{% endhint %}

Check out Pinot:

```bash
git clone https://github.com/apache/pinot.git
cd pinot
```

Build Pinot:

{% hint style="info" %}
If you're building with JDK 8, add Maven option `-Djdk.version=8.`
{% endhint %}

```bash
mvn install package -DskipTests -Pbin-dist
```

Navigate to the directory containing the setup scripts. Note that Pinot scripts are located under `pinot-distribution/target`**,** not the `target` directory under `root`.

```bash
cd build
```
{% endtab %}

{% tab title="Homebrew" %}
Pinot can also be installed on Mac OS using the Brew package manager. For instructions on installing Brew, see the [Brew documentation](https://brew.sh/).

```bash
brew install pinot
```
{% endtab %}
{% endtabs %}

## Set up a cluster

Now that we've downloaded Pinot, it's time to set up a cluster. There are two ways to do this: through quick start or through setting up a cluster manually.

### Quick start

Pinot comes with quick start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick start command launches Pinot with a baseball dataset pre-loaded:

```
./bin/pinot-admin.sh QuickStart -type batch
```

For a list of all the available quick start commands, see the [Quick Start Examples](quick-start.md).

### Manual cluster

If you want to play with bigger datasets (more than a few megabytes), you can launch each component individually.

The video below is a step-by-step walk through for launching the individual components of Pinot and scaling them to multiple instances.

{% embed url="https://www.youtube.com/watch?v=cNnwMF0pOJ8" %}
Neha Pawar from the Apache Pinot team shows you how to set up a Pinot cluster
{% endembed %}

You can find the commands that are shown in this video in the [this Github repository](https://github.com/npawar/pinot-tutorial).

{% hint style="info" %}
The examples below assume that you are using Java 11+.

If you are using Java 8, add the following settings inside`JAVA_OPTS`. So, for example, instead of this:

```bash
export JAVA_OPTS="-Xms4G -Xmx8G"
```

Use the following:

```bash
export JAVA_OPTS="-Xms4G -Xmx8G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
```
{% endhint %}

### Start Zookeeper

```
./bin/pinot-admin.sh StartZookeeper \
  -zkPort 2191
```

You can use [Zooinspector](https://github.com/zzhang5/zooinspector) to browse the Zookeeper instance.

### Start Pinot Controller

```
export JAVA_OPTS="-Xms4G -Xmx8G"
./bin/pinot-admin.sh StartController \
    -zkAddress localhost:2191 \
    -controllerPort 9000
```

### Start Pinot Broker

```
export JAVA_OPTS="-Xms4G -Xmx4G"
./bin/pinot-admin.sh StartBroker \
    -zkAddress localhost:2191
```

### Start Pinot Server

```
export JAVA_OPTS="-Xms4G -Xmx16G"
./bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2191
```

### Start Pinot Minion

```
export JAVA_OPTS="-Xms4G -Xmx4G"
./bin/pinot-admin.sh StartMinion \
    -zkAddress localhost:2191
```



### Start Kafka

```
./bin/pinot-admin.sh  StartKafka \ 
  -zkAddress=localhost:2191/kafka \
  -port 19092
```

Once your cluster is up and running, you can head over to [Exploring Pinot](../components/exploring-pinot.md) to learn how to run queries against the data.

## Setup cluster with config files

Users could start and customize the cluster by modifying the config files and start the components with config files:

```shell
./bin/pinot-admin.sh StartController -config conf/pinot-controller.conf
./bin/pinot-admin.sh StartBroker -config conf/pinot-broker.conf
./bin/pinot-admin.sh StartServer -config conf/pinot-server.conf
./bin/pinot-admin.sh StartMinion -config conf/pinot-minion.conf
```

## Start a Pinot component in debug mode with IntelliJ

Set break points and inspect variables by starting a Pinot component with debug mode in IntelliJ.

The following example demonstrates server debugging:

1. First, start`zookeeper` , `controller`, and `broker` using the [steps described above](running-pinot-locally.md#manual-cluster).
2. Then, use the following configuration under `$PROJECT_DIR$\.run` ) to start the server, replacing the `metrics-core` version and cluster name as needed.\
   This [commit](https://github.com/apache/pinot/commit/83fc63720cdf2a5470073d43183ae8710d0ecc51) is an example of how to use it.

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="HelixServerStarter" type="Application" factoryName="Application" nameIsGenerated="true">
    <classpathModifications>
      <entry path="$PROJECT_DIR$/pinot-plugins/pinot-metrics/pinot-yammer/target/classes" />
      <entry path="$MAVEN_REPOSITORY$/com/yammer/metrics/metrics-core/2.2.0/metrics-core-2.2.0.jar" />
    </classpathModifications>
    <option name="MAIN_CLASS_NAME" value="org.apache.pinot.server.starter.helix.HelixServerStarter" />
    <module name="pinot-server" />
    <extension name="coverage">
      <pattern>
        <option name="PATTERN" value="org.apache.pinot.server.starter.helix.*" />
        <option name="ENABLED" value="true" />
      </pattern>
    </extension>
    <method v="2">
      <option name="Make" enabled="true" />
    </method>
  </configuration>
</component>
```
