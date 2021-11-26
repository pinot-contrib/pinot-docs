---
description: This guide will show you to run a Pinot Cluster using Docker.
---

# Running Pinot in Docker

{% hint style="info" %}
**Prerequisites**

In this guide we will learn about running Pinot in Docker.

This guide assumes that you have installed [Docker](https://hub.docker.com/editions/community/docker-ce-desktop-mac) and have configured it with enough memory. 

A sample config is shown below:

![](<../../.gitbook/assets/image (4).png>)
{% endhint %}

The latest Pinot Docker image is published at `apachepinot/pinot:latest` and you can see a list [all published tags on Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).
You can pull the Docker image onto your machine by running the following command:

```bash
docker pull apachepinot/pinot:latest
```

## Setting up a Pinot cluster

Now that we've downloaded the Pinot Docker image, it's time to set up a cluster. 
There are two ways to do this:

### Quick Start

Pinot comes with quick-start commands that launch instances of Pinot components in the same process and import pre-built datasets.

For example, the following quick-start launches Pinot with a baseball dataset pre-loaded:

```
docker run \
    -p 9000:9000 \
    apachepinot/pinot:0.9.0 QuickStart \
    -type batch
```

For a list of all the available quick starts, see the [Quick Start Examples](quick-start.md).

### Manual Cluster

The quick start scripts launch Pinot with minimal resources. 
If you want to play with bigger datasets (more than a few MB), see the [Manual cluster setup](advanced-pinot-setup.md).

{% hint style="info" %}
If you have [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) or [Docker Kubernetes](https://www.docker.com/products/kubernetes) installed, you could also try running the [Kubernetes quick start](kubernetes-quickstart.md).
{% endhint %}


Once your cluster is up and running, you can head over to  [Exploring Pinot](../components/exploring-pinot.md) to learn how to run queries against the data.
