---
description: Pinot quickstart in Kubernetes
---

# Running in Kubernetes

Get started running Pinot in Kubernetes.

{% hint style="info" %}
<mark style="color:red;">Note:</mark> The examples in this guide are sample configurations to be used as reference. For production setup, you may want to customize it to your needs, especially enable those security features like TLS/Auth etc.
{% endhint %}

## Prerequisites

### Kubernetes

This guide assumes that you already have a running Kubernetes cluster.

If you haven't yet set up a Kubernetes cluster, see the links below for instructions:

* [Enable Kubernetes on Docker-Desktop](https://docs.docker.com/docker-for-mac/kubernetes/)
* [Install Minikube for local setup](https://kubernetes.io/docs/tasks/tools/install-minikube/)
  * Make sure to run with enough resources: `minikube start --vm=true --cpus=4 --memory=8g --disk-size=50g`
* [Set up a Kubernetes Cluster using Amazon Elastic Kubernetes Service (Amazon EKS)](../public-cloud-examples/aws-quickstart.md)
* [Set up a Kubernetes Cluster using Google Kubernetes Engine (GKE)](../public-cloud-examples/gcp-quickstart.md)
* [Set up a Kubernetes Cluster using Azure Kubernetes Service (AKS)](../public-cloud-examples/azure-quickstart.md)

### Pinot

Make sure that you've downloaded Apache Pinot. The scripts for the setup in this guide can be found in our[ open source project on GitHub](https://github.com/apache/pinot).

{% tabs %}
{% tab title="Git clone project source" %}
```bash
# checkout pinot
git clone https://github.com/apache/pinot.git
cd pinot/helm/pinot
```
{% endtab %}
{% endtabs %}

## Set up a Pinot cluster in Kubernetes

### Start Pinot with Helm

{% tabs %}
{% tab title="Run Helm with pre-installed package" %}
The Pinot repository has pre-packaged Helm charts for Pinot and Presto. The Helm repository index file is [here](https://github.com/apache/pinot/blob/master/helm/index.yaml).

```bash
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/helm
kubectl create ns pinot-quickstart
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot \
    --set server.replicaCount=2
```

**Note**: Specify **StorageClass** based on your cloud vendor. Don't mount a blob store (such as AzureFile, GoogleCloudStorage, or S3) as the data serving file system. Use only Amazon EBS/GCP Persistent Disk/Azure Disk-style disks.

* For AWS: "**gp2**"
* For GCP: "**pd-ssd**" or "**standard**"
* For Azure: "**AzureDisk**"
* For Docker-Desktop: "**hostpath**"
{% endtab %}

{% tab title="Run Helm script within Git repo" %}
**1.1.1 Update Helm dependency**

```bash
helm dependency update
```

**1.1.2 Start Pinot with Helm**

```bash
kubectl create ns pinot-quickstart
helm install -n pinot-quickstart pinot ./pinot
```
{% endtab %}
{% endtabs %}

### **Check Pinot deployment status**

```
kubectl get all -n pinot-quickstart
```

## Next steps

Once your cluster is running, load data into it:

{% content-ref url="stream-ingestion.md" %}
[stream-ingestion.md](stream-ingestion.md)
{% endcontent-ref %}

Connect query engines to your Pinot cluster:

{% content-ref url="query-engines.md" %}
[query-engines.md](query-engines.md)
{% endcontent-ref %}

## Delete a Pinot cluster in Kubernetes

To delete your Pinot cluster in Kubernetes, run the following command:

```bash
kubectl delete ns pinot-quickstart
```
