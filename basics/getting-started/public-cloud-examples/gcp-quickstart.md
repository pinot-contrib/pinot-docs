---
description: >-
  This quickstart guide helps you get started running Pinot on Google Cloud Platform (GCP).
---

# Running on GCP

In this quickstart guide, you will set up a Kubernetes Cluster on [Google Kubernetes Engine(GKE)](https://cloud.google.com/kubernetes-engine)

## 1. Tooling Installation

### **1.1 Install Kubectl**

Follow this link ([https://kubernetes.io/docs/tasks/tools/install-kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)) to install kubectl.

_For Mac users_

```bash
brew install kubernetes-cli
```

Check kubectl version after installation.

```
kubectl version
```

{% hint style="info" %}
Quickstart scripts are tested under kubectl client version v1.16.3 and server version v1.13.12
{% endhint %}

### **1.2 Install Helm**

Follow this link ([https://helm.sh/docs/using\_helm/#installing-helm](https://helm.sh/docs/using\_helm/#installing-helm)) to install helm.

_For Mac users_

```bash
brew install kubernetes-helm
```

Check helm version after installation.

```
helm version
```

{% hint style="info" %}
This quickstart provides helm supports for helm v3.0.0 and v2.12.1. Choose the script based on your helm version.
{% endhint %}

### **1.3 Install Google Cloud SDK**

To install Google Cloud SDK, see [Install the gcloud CLI](https://cloud.google.com/sdk/docs/install)

#### _1.3.1 For Mac users_

* _Install Google Cloud SDK_

```bash
curl https://sdk.cloud.google.com | bash
```

Restart your shell

```
exec -l $SHELL
```

## **2. (Optional) Initialize Google Cloud Environment**

```
gcloud init
```

## 3. (Optional) Create a Kubernetes cluster(GKE) in Google Cloud

This script will create a 3 node cluster named **pinot-quickstart** in **us-west1-b** with **n1-standard-2** machines for demo purposes.

Modify the parameters in the following example command with your gcloud details:

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

Use the following command do monitor cluster status:

```
gcloud compute instances list
```

Once the cluster is in **RUNNING** status, it's ready to be used.

## **4. Connect to an existing cluster**

Run the following command to get the credential for the cluster **pinot-quickstart** that you just created:

```
GCLOUD_PROJECT=[your gcloud project name]
GCLOUD_ZONE=us-west1-b
GCLOUD_CLUSTER=pinot-quickstart
gcloud container clusters get-credentials ${GCLOUD_CLUSTER} --zone ${GCLOUD_ZONE} --project ${GCLOUD_PROJECT}
```

To verify the connection, run the following:

```
kubectl get nodes
```

## 5. Pinot quickstart

Follow this [Kubernetes quickstart](../kubernetes-quickstart.md) to deploy your Pinot demo.

## 6. Delete a Kubernetes Cluster

```
GCLOUD_ZONE=us-west1-b
gcloud container clusters delete pinot-quickstart --zone=${GCLOUD_ZONE}
```
