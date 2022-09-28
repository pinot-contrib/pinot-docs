---
description: >-
  This quick start guide will help you bootstrap a Pinot standalone instance on
  your local machine.
---

# Running Pinot locally

In this guide, you'll learn how to download and install Apache Pinot as a standalone instance.

## Download Apache Pinot

First, let's download the Pinot distribution for this tutorial. You can either download a packaged release or build a distribution from the source code.

{% hint style="info" %}
**Prerequisites**

Install JDK11 or higher (JDK16 is not yet supported)\
For JDK 8 support use Pinot 0.7.1 or compile from the source code.
{% endhint %}

You can build from source or download the distribution:

{% tabs %}
{% tab title="Download the release" %}
Download the latest binary release from [Apache Pinot](https://pinot.apache.org/download/), or use this command

```bash
PINOT_VERSION=0.10.0 #set to the Pinot version you decide to use

wget https://downloads.apache.org/pinot/apache-pinot-$PINOT_VERSION/apache-pinot-$PINOT_VERSION-bin.tar.gz
```

Once you have the tar file,

```bash
# untar it
tar -zxvf apache-pinot-$PINOT_VERSION-bin.tar.gz

# navigate to directory containing the launcher scripts
cd apache-pinot-$PINOT_VERSION-bin
```
{% endtab %}

{% tab title="Build from source " %}
Follow these steps to checkout code from [Github](https://github.com/apache/pinot) and build Pinot locally

{% hint style="info" %}
**Prerequisites**

Install [Apache Maven](https://maven.apache.org/install.html) 3.6 or higher
{% endhint %}

```bash
# checkout pinot
git clone https://github.com/apache/pinot.git
cd pinot

# build pinot
mvn install package -DskipTests -Pbin-dist

# navigate to directory containing the setup scripts
cd build
```

{% hint style="info" %}
Add maven option `-Djdk.version=8` when building with JDK 8
{% endhint %}

{% hint style="info" %}
Note that Pinot scripts is located under **pinot-distribution/target** not **target** directory under root.
{% endhint %}
{% endtab %}
{% endtabs %}

### M1 Mac Support

Currently Apache Pinot doesn't provide official binaries for M1 Mac. You can however build from source using the steps provided above. In addition to the steps, you will need to add the following in your `~/.m2/settings.xml` prior to the build.

```xml
<settings>
  <activeProfiles>
    <activeProfile>
      apple-silicon
    </activeProfile>
  </activeProfiles>
  <profiles>
    <profile>
      <id>apple-silicon</id>
      <properties>
        <os.detected.classifier>osx-x86_64</os.detected.classifier>
      </properties>
    </profile>
  </profiles>
</settings>  
```

Also make sure to install rosetta

`softwareupdate --install-rosetta`

Note that some installations of the JDK do not contain the JNI bindings that are necessary to run all tests, if you see any `java.lang.UnsatisfiedLinkError` while running tests, you may need to change your JDK. If using Homebrew, you may install AdoptOpenJDK 11 using:
`brew install --cask adoptopenjdk11`

Now that we've downloaded Pinot, it's time to set up a cluster. There are two ways to do this:

## Quick Start

Pinot comes with quick-start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick-start launches Pinot with a baseball dataset pre-loaded:

```
./bin/pinot-admin.sh QuickStart -type batch
```

For a list of all the available quick starts, see the [Quick Start Examples](quick-start.md).

## Manual Cluster

If you want to play with bigger datasets (more than a few MB), you can launch all the components individually.

The video below is a step-by-step walk through for launching the individual components of Pinot and scaling them to multiple instances.

{% embed url="https://www.youtube.com/watch?v=cNnwMF0pOJ8" %}
Neha Pawar from the Apache Pinot team shows you how to setup a Pinot cluster
{% endembed %}

You can find the commands that are shown in this video in the [github.com/npawar/pinot-tutorial](https://github.com/npawar/pinot-tutorial) GitHub repository.

{% hint style="info" %}
The examples below assume that you are using Java 8.

If you are using Java 11+ users, remove the GC settings inside`JAVA_OPTS.` So, for example, instead of:

```bash
export JAVA_OPTS="-Xms4G -Xmx8G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
```

You'd have:

```bash
export JAVA_OPTS="-Xms4G -Xmx8G"
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
export JAVA_OPTS="-Xms4G -Xmx8G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
./bin/pinot-admin.sh StartController \
    -zkAddress localhost:2191 \
    -controllerPort 9000
```

### Start Pinot Broker

```
export JAVA_OPTS="-Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-broker.log"
./bin/pinot-admin.sh StartBroker \
    -zkAddress localhost:2191
```

### Start Pinot Server

```
export JAVA_OPTS="-Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
./bin/pinot-admin.sh StartServer \
    -zkAddress localhost:2191
```

### Start Kafka

```
./bin/pinot-admin.sh  StartKafka \ 
  -zkAddress=localhost:2191/kafka \
  -port 19092
```

Once your cluster is up and running, you can head over to [Exploring Pinot](../components/exploring-pinot.md) to learn how to run queries against the data.

## Start Pinot Component in Debug Mode with IntelliJ

Starting a pinot component of interest in IntelliJ using debug mode can be useful for development purposes. You can set break points and inspect variables. Take debugging server for example, one can start `zookeeper` , `controller`, and `broker` using the steps in [Manual Cluster](running-pinot-locally.md#manual-cluster). Then use the following configuration  put under `$PROJECT_DIR$\.run` ) to start server. This [commit](https://github.com/apache/pinot/commit/83fc63720cdf2a5470073d43183ae8710d0ecc51) is an example of how it can be used. Please replace the metrics-core version and cluster name as needed.

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
