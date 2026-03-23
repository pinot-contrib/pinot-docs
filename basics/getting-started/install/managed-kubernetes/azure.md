---
description: Provision a managed Kubernetes cluster on Azure AKS ready for Pinot.
---

# Azure (Azure AKS)

## Outcome

Create an Azure Kubernetes Service cluster with the required tooling, ready to deploy Apache Pinot.

## Prerequisites

* An Azure account
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

**Azure CLI**

Follow the [Azure CLI installation guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) or run:

```bash
brew update && brew install azure-cli
```

### 2. Log in to Azure

```bash
az login
```

### 3. Create a resource group

```bash
AKS_RESOURCE_GROUP=pinot-demo
AKS_RESOURCE_GROUP_LOCATION=eastus
az group create --name ${AKS_RESOURCE_GROUP} \
                --location ${AKS_RESOURCE_GROUP_LOCATION}
```

### 4. Create an AKS cluster

The following creates a 3-node cluster named `pinot-quickstart`:

```bash
AKS_RESOURCE_GROUP=pinot-demo
AKS_CLUSTER_NAME=pinot-quickstart
az aks create --resource-group ${AKS_RESOURCE_GROUP} \
              --name ${AKS_CLUSTER_NAME} \
              --node-count 3
```

### 5. Connect to the cluster

```bash
AKS_RESOURCE_GROUP=pinot-demo
AKS_CLUSTER_NAME=pinot-quickstart
az aks get-credentials --resource-group ${AKS_RESOURCE_GROUP} \
                       --name ${AKS_CLUSTER_NAME}
```

## Verify

```bash
kubectl get nodes
```

You should see your worker nodes listed and in `Ready` status.

## Cleaning up

To delete the cluster when you are done:

```bash
AKS_RESOURCE_GROUP=pinot-demo
AKS_CLUSTER_NAME=pinot-quickstart
az aks delete --resource-group ${AKS_RESOURCE_GROUP} \
              --name ${AKS_CLUSTER_NAME}
```

## Next step

Your cluster is ready. Continue to [Kubernetes install](../kubernetes.md) to deploy Pinot.
