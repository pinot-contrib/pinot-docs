---
description: This starter guide provides a quick start for running Pinot on Microsoft Azure
---

# Running on Azure

This document provides the basic instruction to set up a Kubernetes Cluster on [Azure Kubernetes Service (AKS)](https://azure.microsoft.com/en-us/services/kubernetes-service/)

## 1. Tooling Installation

### **1.1 Install Kubectl**

Follow this link ([https://kubernetes.io/docs/tasks/tools/install-kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl)) to install kubectl.

_For Mac users_

```bash
brew install kubernetes-cli
```

Please check kubectl version after installation.

```
kubectl version
```

{% hint style="info" %}
QuickStart scripts are tested under kubectl client version v1.16.3 and server version v1.13.12
{% endhint %}

### **1.2 Install Helm**

Follow this link ([https://helm.sh/docs/using\_helm/#installing-helm](https://helm.sh/docs/using\_helm/#installing-helm)) to install helm.

_For Mac users_

```bash
brew install kubernetes-helm
```

Please check helm version after installation.

```
helm version
```

{% hint style="info" %}
This QuickStart provides helm supports for helm v3.0.0 and v2.12.1. Please pick the script based on your helm version.
{% endhint %}

### **1.3 Install** Azure CLI

Follow this link ([https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)) to install _Azure CLI_.

_For Mac users_

```bash
brew update && brew install azure-cli
```

## 2. (Optional) **Log in to your Azure account**

The below script will open default browser to sign-in to your Azure Account.

```bash
az login
```

## 3. (Optional) Create a Resource Group

The below script will create a resource group in location **eastus**.

```
AKS_RESOURCE_GROUP=pinot-demo
AKS_RESOURCE_GROUP_LOCATION=eastus
az group create --name ${AKS_RESOURCE_GROUP} \
                --location ${AKS_RESOURCE_GROUP_LOCATION}
```

## 4. (Optional) Create a Kubernetes cluster(AKS) in Azure&#x20;

The below script will create a **3** nodes cluster named **pinot-quickstart** for demo purposes.

Modify the parameters in the example command below:

```bash
AKS_RESOURCE_GROUP=pinot-demo
AKS_CLUSTER_NAME=pinot-quickstart
az aks create --resource-group ${AKS_RESOURCE_GROUP} \
              --name ${AKS_CLUSTER_NAME} \
              --node-count 3
```

Once the command succeeds, it's ready to be used.

## **5. Connect to an existing cluster**

Run the below command to get the credential for the cluster **pinot-quickstart** that you just created or your existing cluster.&#x20;

```
AKS_RESOURCE_GROUP=pinot-demo
AKS_CLUSTER_NAME=pinot-quickstart
az aks get-credentials --resource-group ${AKS_RESOURCE_GROUP} \
                       --name ${AKS_CLUSTER_NAME}
```

To verify the connection, you can run:

```
kubectl get nodes
```

## 6. Pinot Quickstart

Follow this [Kubernetes QuickStart](../kubernetes-quickstart.md) to deploy your Pinot Demo.

## 7. Delete a Kubernetes Cluster

```
AKS_RESOURCE_GROUP=pinot-demo
AKS_CLUSTER_NAME=pinot-quickstart
az aks delete --resource-group ${AKS_RESOURCE_GROUP} \
              --name ${AKS_CLUSTER_NAME}
```
