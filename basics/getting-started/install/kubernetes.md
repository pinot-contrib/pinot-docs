---
description: Deploy a Pinot cluster on Kubernetes using Helm.
---

# Kubernetes install

## Outcome

Deploy a production-ready Pinot cluster on Kubernetes with Helm charts.

{% hint style="info" %}
The examples in this guide are sample configurations for reference. For production deployments, customize settings as needed -- especially security features like TLS and authentication.
{% endhint %}

## Prerequisites

* A running Kubernetes cluster. Options include:
  * [Docker Desktop with Kubernetes enabled](https://docs.docker.com/docker-for-mac/kubernetes/)
  * [Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) -- start with sufficient resources: `minikube start --vm=true --cpus=4 --memory=8g --disk-size=50g`
  * A managed cloud cluster -- see [Managed Kubernetes](managed-kubernetes/) for AWS, GCP, and Azure setup guides
* [Helm 3](https://helm.sh/docs/intro/install/)
* [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

## Steps

### 1. Add the Pinot Helm repository

```bash
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/helm
```

### 2. Create a namespace

```bash
kubectl create ns pinot-quickstart
```

### 3. Install Pinot

{% tabs %}
{% tab title="Helm with pre-packaged chart" %}
```bash
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot \
    --set server.replicaCount=2
```

{% hint style="info" %}
**StorageClass:** Specify the StorageClass for your cloud vendor. Use block storage only -- do not mount blob stores (S3, GCS, AzureFile) as the data-serving file system.

* AWS: `gp2`
* GCP: `pd-ssd` or `standard`
* Azure: `AzureDisk`
* Docker Desktop: `hostpath`
{% endhint %}
{% endtab %}

{% tab title="Helm from Git repo" %}
```bash
git clone https://github.com/apache/pinot.git
cd pinot/helm/pinot
helm dependency update
kubectl create ns pinot-quickstart
helm install -n pinot-quickstart pinot ./pinot
```
{% endtab %}
{% endtabs %}

## Verify

Check the deployment status:

```bash
kubectl get all -n pinot-quickstart
```

All pods should reach `Running` status. You can port-forward the Controller to access the UI:

```bash
kubectl port-forward service/pinot-controller 9000:9000 -n pinot-quickstart
```

Then open [http://localhost:9000](http://localhost:9000).

## Loading data

For stream ingestion on Kubernetes, see the [Kubernetes stream ingestion guide](../kubernetes/stream-ingestion.md). For batch data loading and table creation, continue with the onboarding path below.

## Deleting the cluster

To remove Pinot from your cluster:

```bash
kubectl delete ns pinot-quickstart
```

## Next step

Your cluster is running. Continue to [First table and schema](../first-table-and-schema.md) to load data.
