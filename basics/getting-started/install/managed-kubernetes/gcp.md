---
description: Provision a managed Kubernetes cluster on Google GKE ready for Pinot.
---

# GCP (Google GKE)

## Outcome

Create a Google Kubernetes Engine cluster with the required tooling, ready to deploy Apache Pinot.

## Prerequisites

* A Google Cloud account and project
* The following CLI tools installed (see steps below)

## Steps

### 1. Install tooling

**kubectl**

```bash
brew install kubernetes-cli
```

Verify:

```bash
kubectl version
```

**Helm**

```bash
brew install kubernetes-helm
```

Verify:

```bash
helm version
```

**Google Cloud SDK**

Follow the [gcloud CLI installation guide](https://cloud.google.com/sdk/docs/install) or run:

```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2. Initialize Google Cloud

```bash
gcloud init
```

### 3. Create a GKE cluster

The following creates a 3-node cluster named `pinot-quickstart` in `us-west1-b` using `n1-standard-2` machines:

```bash
GCLOUD_PROJECT=[your gcloud project name]
GCLOUD_ZONE=us-west1-b
GCLOUD_CLUSTER=pinot-quickstart
GCLOUD_MACHINE_TYPE=n1-standard-2
GCLOUD_NUM_NODES=3
gcloud container clusters create ${GCLOUD_CLUSTER} \
  --num-nodes=${GCLOUD_NUM_NODES} \
  --machine-type=${GCLOUD_MACHINE_TYPE} \
  --zone=${GCLOUD_ZONE} \
  --project=${GCLOUD_PROJECT}
```

Monitor cluster status:

```bash
gcloud compute instances list
```

Wait until the cluster status is **RUNNING**.

### 4. Connect to the cluster

```bash
GCLOUD_PROJECT=[your gcloud project name]
GCLOUD_ZONE=us-west1-b
GCLOUD_CLUSTER=pinot-quickstart
gcloud container clusters get-credentials ${GCLOUD_CLUSTER} --zone ${GCLOUD_ZONE} --project ${GCLOUD_PROJECT}
```

## Verify

```bash
kubectl get nodes
```

You should see your worker nodes listed and in `Ready` status.

## Cleaning up

To delete the cluster when you are done:

```bash
GCLOUD_ZONE=us-west1-b
gcloud container clusters delete pinot-quickstart --zone=${GCLOUD_ZONE}
```

## Next step

Your cluster is ready. Continue to [Kubernetes install](../kubernetes.md) to deploy Pinot.
