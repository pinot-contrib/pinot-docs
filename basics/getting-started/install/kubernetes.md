---
description: Deploy a Pinot cluster on Kubernetes using Helm.
---

# Kubernetes install

## Outcome

Deploy a production-ready Pinot cluster on Kubernetes with Helm charts.

{% hint style="warning" %}
**Helm 3 Migration:** Pinot Helm charts have been upgraded to Helm 3 (apiVersion v2). If you are upgrading from older Helm charts (v1), please note:
- **Minimum Helm version:** Helm 3.0+ is required
- **Dependency management:** Use `helm dependency build` (not `helm dependency update`)
- **Dependency file:** Charts now use `Chart.yaml` for dependency declarations (not `requirements.yaml`)
- **Lock file:** Uses `Chart.lock` (not `requirements.lock`)
- **Chart archives:** No longer checked into the repository; automatically fetched via `helm dependency build`
- **Chart versions:** No longer use the `-SNAPSHOT` suffix

For detailed upgrade instructions, see the [Upgrade Guide](#upgrading-from-helm-v1-charts) below.
{% endhint %}

{% hint style="info" %}
The examples in this guide are sample configurations for reference. For production deployments, customize settings as needed -- especially security features like TLS and authentication.
{% endhint %}

## Prerequisites

* A running Kubernetes cluster. Options include:
  * [Docker Desktop with Kubernetes enabled](https://docs.docker.com/docker-for-mac/kubernetes/)
  * [Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) -- start with sufficient resources: `minikube start --vm=true --cpus=4 --memory=8g --disk-size=50g`
  * A managed cloud cluster -- see [Managed Kubernetes](managed-kubernetes/) for AWS, GCP, and Azure setup guides
* **Helm 3** (apiVersion v2) -- Required for Pinot Helm charts. [Install Helm 3](https://helm.sh/docs/intro/install/)
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
helm dependency build
kubectl create ns pinot-quickstart
helm install -n pinot-quickstart pinot ./pinot
```

{% hint style="info" %}
**Helm 3 Migration (v2):** As of the recent migration to Helm 3 apiVersion v2, the Pinot charts now use `Chart.yaml` for dependency declarations (instead of `requirements.yaml`) and `Chart.lock` (instead of `requirements.lock`). The `helm dependency build` command fetches dependencies from the chart repository automatically.
{% endhint %}
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

## Upgrading from Helm v1 charts

If you are upgrading from older Pinot Helm charts (apiVersion v1), follow these steps:

### 1. Update Helm repository

```bash
helm repo update pinot
```

### 2. Back up your configuration

Save your current `values.yaml` in case you need to reference it:

```bash
helm get values pinot -n pinot-quickstart > values-backup.yaml
```

### 3. Uninstall old release (optional but recommended)

If upgrading from v1 charts, it's safest to uninstall and reinstall:

```bash
helm uninstall pinot -n pinot-quickstart
```

### 4. Reinstall with new Helm v2 charts

```bash
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot \
    --set server.replicaCount=2 \
    -f values-backup.yaml
```

### Key changes in Helm v2 charts

- **apiVersion:** Changed from `v1` to `v2`
- **Chart type:** Added explicit `type: application`
- **Dependencies:** Now declared in `Chart.yaml` instead of `requirements.yaml`
- **Lock file:** Changed from `requirements.lock` to `Chart.lock`
- **Dependency fetching:** Use `helm dependency build` instead of `helm dependency update`
- **Chart versions:** No longer include `-SNAPSHOT` suffix (uses standard SemVer)
- **Chart icons:** Now include official Apache Pinot icons

### If deploying from source

When deploying directly from the Git repository, always run `helm dependency build` before installing:

```bash
git clone https://github.com/apache/pinot.git
cd pinot/helm/pinot
helm dependency build  # Required for Helm 3 v2 charts
helm install pinot . -n pinot-quickstart
```
