---
description: Provision a managed Kubernetes cluster on Amazon EKS ready for Pinot.
---

# AWS (Amazon EKS)

## Outcome

Create an Amazon EKS cluster with the required tooling, ready to deploy Apache Pinot.

## Prerequisites

* An AWS account
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

**AWS CLI**

Follow the [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) or run:

```bash
curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-macos.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**eksctl**

```bash
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl
```

### 2. Configure AWS credentials

```bash
aws configure
```

{% hint style="info" %}
Environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` override credentials stored in `~/.aws/credentials`.
{% endhint %}

### 3. Create an EKS cluster

The following creates a single-node cluster named `pinot-quickstart` in `us-west-2` using `t3.xlarge` instances:

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

For Kubernetes 1.23+, enable the EBS CSI driver to allow persistent volume provisioning:

```bash
eksctl utils associate-iam-oidc-provider --region=us-east-2 --cluster=pinot-quickstart --approve

eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster pinot-quickstart \
  --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --approve \
  --role-only \
  --role-name AmazonEKS_EBS_CSI_DriverRole

eksctl create addon --name aws-ebs-csi-driver --cluster pinot-quickstart \
  --service-account-role-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/AmazonEKS_EBS_CSI_DriverRole --force
```

Monitor cluster status:

```bash
EKS_CLUSTER_NAME=pinot-quickstart
aws eks describe-cluster --name ${EKS_CLUSTER_NAME} --region us-west-2
```

Wait until the cluster status is **ACTIVE**.

### 4. Connect to the cluster

```bash
EKS_CLUSTER_NAME=pinot-quickstart
aws eks update-kubeconfig --name ${EKS_CLUSTER_NAME}
```

## Verify

```bash
kubectl get nodes
```

You should see your worker nodes listed and in `Ready` status.

## Cleaning up

To delete the cluster when you are done:

```bash
EKS_CLUSTER_NAME=pinot-quickstart
aws eks delete-cluster --name ${EKS_CLUSTER_NAME}
```

## Next step

Your cluster is ready. Continue to [Kubernetes install](../kubernetes.md) to deploy Pinot.
