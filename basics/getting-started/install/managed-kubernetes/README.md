---
description: Set up a Kubernetes cluster on your cloud provider.
---

# Managed Kubernetes

## Outcome

Provision a managed Kubernetes cluster on AWS, GCP, or Azure that is ready for a Pinot deployment.

## Overview

These guides walk you through creating a managed Kubernetes cluster on your cloud provider. Once the cluster is running, you will use the [Kubernetes install](../kubernetes.md) page to deploy Pinot onto it.

## Cloud providers

<table>
  <thead>
    <tr>
      <th>Provider</th>
      <th>Service</th>
      <th>Guide</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Amazon Web Services</td>
      <td>Amazon EKS</td>
      <td>[AWS setup](aws.md)</td>
    </tr>
    <tr>
      <td>Google Cloud Platform</td>
      <td>Google GKE</td>
      <td>[GCP setup](gcp.md)</td>
    </tr>
    <tr>
      <td>Microsoft Azure</td>
      <td>Azure AKS</td>
      <td>[Azure setup](azure.md)</td>
    </tr>
  </tbody>
</table>

## Next step

Once your cluster is ready, follow the [Kubernetes install guide](../kubernetes.md) to deploy Pinot.
