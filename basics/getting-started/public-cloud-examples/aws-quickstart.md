---
description: >-
  This guide provides a quick start for running Pinot on Amazon Web Services
  (AWS).
---

# Running on AWS

This document provides the basic instruction to set up a Kubernetes Cluster on [Amazon Elastic Kubernetes Service (Amazon EKS)](https://aws.amazon.com/eks/)

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
QuickStart scripts are tested under kubectl client version v1.16.3 and server version v1.13.12
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
This QuickStart provides helm supports for helm v3.0.0 and v2.12.1. Please pick the script based on your helm version.
{% endhint %}

### **1.3 Install AWS CLI**

Follow this link ([https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html#install-tool-bundled](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html#install-tool-bundled)) to install _AWS CLI_.

_For Mac users_

```bash
curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-macos.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

### **1.4 Install Eksctl**

Follow this link ([https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl](https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html#installing-eksctl)) to install _AWS CLI_.

_For Mac users_

```bash
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl
```

## 2. (Optional) **Log in to your AWS account**

For first-time AWS users, register your account at [https://aws.amazon.com/](https://aws.amazon.com/).

Once created the account, you can go to [AWS Identity and Access Management (IAM)](https://console.aws.amazon.com/iam/home#/home) to create a user and create access keys under Security Credential tab.&#x20;

```bash
aws configure
```

{% hint style="info" %}
Environment variables **`AWS_ACCESS_KEY_ID`** and **`AWS_SECRET_ACCESS_KEY`** will override  AWS configuration stored in file **`~/.aws/credentials`**
{% endhint %}

## 3. (Optional) Create a Kubernetes cluster(EKS) in AWS&#x20;

The script below will create a **1** node cluster named **pinot-quickstart** in **us-west-2** with a **t3.xlarge** machine for demo purposes:

```bash
EKS_CLUSTER_NAME=pinot-quickstart
eksctl create cluster \
--name ${EKS_CLUSTER_NAME} \
--version 1.16 \
--region us-west-2 \
--nodegroup-name standard-workers \
--node-type t3.xlarge \
--nodes 1 \
--nodes-min 1 \
--nodes-max 1
```

Monitor the cluster status via this command:

```
EKS_CLUSTER_NAME=pinot-quickstart
aws eks describe-cluster --name ${EKS_CLUSTER_NAME} --region us-west-2
```

Once the cluster is in **ACTIVE** status, it's ready to be used.

## **4. Connect to an existing cluster**

Simply run below command to get the credential for the cluster **pinot-quickstart** that you just created or your existing cluster.

```
EKS_CLUSTER_NAME=pinot-quickstart
aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME}
```

To verify the connection, you can run:

```
kubectl get nodes
```

## 5. Pinot Quickstart

Please follow this [Kubernetes QuickStart](../kubernetes-quickstart.md) to deploy your Pinot Demo.

## 6. Delete a Kubernetes Cluster

```
EKS_CLUSTER_NAME=pinot-quickstart
aws eks delete-cluster --name ${EKS_CLUSTER_NAME}
```
