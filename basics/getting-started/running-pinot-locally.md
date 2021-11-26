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
For JDK 8 support use Pinot 0.7.1 or compile from source
{% endhint %}

### Build from source or download the distribution

{% tabs %}
{% tab title="Download the release" %}
Download the latest binary release from [Apache Pinot](https://pinot.apache.org/download/), or use this command

```bash
PINOT_VERSION=0.9.0 #set to the Pinot version you decide to use

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
cd pinot-distribution/target/apache-pinot-$PINOT_VERSION-bin/apache-pinot-$PINOT_VERSION-bin
```

{% hint style="info" %}
Add maven option `-Djdk.version=8` when building with JDK 8
{% endhint %}

{% hint style="info" %}
Note that Pinot scripts is located under **pinot-distribution/target** not **target** directory under root.
{% endhint %}
{% endtab %}
{% endtabs %}

## Setting up a Pinot cluster

Now that we've downloaded Pinot, it's time to set up a cluster. There are two ways to do this:

### Quick Start

Pinot comes with quick-start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick-start launches Pinot with a baseball dataset pre-loaded:

```
./bin/pinot-admin.sh QuickStart -type batch
```

For a list of all the available quick starts, see the [Quick Start Examples](quick-start.md).

### Manual Cluster

The quick start scripts launch Pinot with minimal resources. If you want to play with bigger datasets (more than a few MB), see the [Manual cluster setup](advanced-pinot-setup.md).
