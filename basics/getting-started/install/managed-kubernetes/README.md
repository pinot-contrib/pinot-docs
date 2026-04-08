---
description: Set up a Kubernetes cluster on your cloud provider.
---

# Managed Kubernetes

## Outcome

Provision a managed Kubernetes cluster on AWS, GCP, or Azure that is ready for a Pinot deployment.

## Overview

These guides walk you through creating a managed Kubernetes cluster on your cloud provider. Once the cluster is running, you will use the [Kubernetes install](../kubernetes.md) page to deploy Pinot onto it.

## Cloud providers

| Provider | Service | Guide |
|---|---|---|
| Amazon Web Services | Amazon EKS | [AWS setup](aws.md) |
| Google Cloud Platform | Google GKE | [GCP setup](gcp.md) |
| Microsoft Azure | Azure AKS | [Azure setup](azure.md) |

## Next step

Once your cluster is ready, follow the [Kubernetes install guide](../kubernetes.md) to deploy Pinot.
