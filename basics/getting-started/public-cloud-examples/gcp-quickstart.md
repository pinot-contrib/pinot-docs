---
description: >-
  This starter provides a quick start for running Pinot on Google Cloud Platform
  (GCP)
---

# Running on GCP

This document provides the basic instruction to set up a Kubernetes Cluster on [Google Kubernetes Engine\(GKE\)](https://cloud.google.com/kubernetes-engine)

## 1. Tooling Installation

### **1.1 Install Kubectl**

Please follow this link \([https://kubernetes.io/docs/tasks/tools/install-kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)\) to install kubectl.

_For Mac User_

```bash
brew install kubernetes-cli
```

Please check kubectl version after installation.

```text
kubectl version
```

{% hint style="info" %}
QuickStart scripts are tested under kubectl client version v1.16.3 and server version v1.13.12
{% endhint %}

### **1.2 Install Helm**

Please follow this link \([https://helm.sh/docs/using\_helm/\#installing-helm](https://helm.sh/docs/using_helm/#installing-helm)\) to install helm.

_For Mac User_

```bash
brew install kubernetes-helm
```

Please check helm version after installation.

```text
helm version
```

{% hint style="info" %}
This QuickStart provides helm supports for helm v3.0.0 and v2.12.1. Please pick the script based on your helm version.
{% endhint %}

### **1.3 Install Google Cloud SDK**

\_\_

Please follow this link \([https://cloud.google.com/sdk/install](https://cloud.google.com/sdk/install)\) to install Google Cloud SDK.

#### _1.3.1 For Mac User_

* _Install Google Cloud SDK_

```bash
curl https://sdk.cloud.google.com | bash
```

* Restart your shell

```text
exec -l $SHELL
```

## **2. \(Optional\) Initialize Google Cloud Environment**

```text
gcloud init
```

## 3. \(Optional\) Create a Kubernetes cluster\(GKE\) in Google Cloud

Below script will create a 3 nodes cluster named **pinot-quickstart** in **us-west1-b** with **n1-standard-2** machines for demo purposes.

Please modify the parameters in the example command below:

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

You can monitor cluster status by command:

```text
gcloud compute instances list
```

Once the cluster is in **RUNNING** status, it's ready to be used.

## **4. Connect to an existing cluster**

Simply run below command to get the credential for the cluster **pinot-quickstart** that you just created or your existing cluster.

```text
GCLOUD_PROJECT=[your gcloud project name]
GCLOUD_ZONE=us-west1-b
GCLOUD_CLUSTER=pinot-quickstart
gcloud container clusters get-credentials ${GCLOUD_CLUSTER} --zone ${GCLOUD_ZONE} --project ${GCLOUD_PROJECT}
```

To verify the connection, you can run:

```text
kubectl get nodes
```

## 5. Pinot Quickstart

Please follow this [Kubernetes QuickStart](../kubernetes-quickstart.md) to deploy your Pinot Demo.

## 6. Delete a Kubernetes Cluster

```text
GCLOUD_ZONE=us-west1-b
gcloud container clusters delete pinot-quickstart --zone=${GCLOUD_ZONE}
```

