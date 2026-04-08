# Kubernetes Production

This section covers everything you need to run Apache Pinot on Kubernetes in production, from initial Helm-based deployment through cloud-provider integration, Kafka connectivity, and security hardening.

## Purpose

After completing a quickstart or proof-of-concept, you need a production-grade Kubernetes deployment that is properly sized, secured, and integrated with your cloud provider's storage and streaming services. The guides in this section take you from a baseline Helm install to a hardened, observable cluster.

## When to use

Use these guides when you are:

* Deploying Pinot on Kubernetes for a staging or production workload.
* Migrating an existing Pinot cluster into Amazon EKS, Google GKE, or Azure AKS.
* Connecting Pinot to a managed Kafka service such as Amazon MSK.
* Hardening a Helm-based Pinot deployment for security and reliability.

## Key topics

### Helm-based deployment

The official Apache Pinot Helm chart deploys all Pinot components (controller, broker, server, minion, ZooKeeper) as Kubernetes StatefulSets. A production deployment requires attention to:

* **Container resources** -- Set `requests` and `limits` to the same values so pods receive Guaranteed QoS and are not evicted during traffic spikes.
* **JVM tuning** -- Controller and broker heap should match the container memory limit. Server heap should stay below 50% of container memory, leaving the rest for off-heap segment operations and page cache.
* **Deep storage** -- Replace the default local-disk deep store with S3, GCS, or ADLS for durability and multi-zone availability.
* **PodDisruptionBudgets** -- Enable PDBs on every component to prevent voluntary disruptions from draining too many pods at once.
* **Probes** -- Enable liveness and readiness probes (and startup probes on servers with large segment loads) so Kubernetes routes traffic only to healthy pods.

For a full walkthrough of resource sizing, JVM settings, deep storage configuration, and security controls, see:

* [Kubernetes Deployment](kubernetes/deployment-pinot-on-kubernetes.md)

### Helm chart reference

Every Helm value that controls replica counts, resource limits, persistence, service exposure, TLS, authentication, monitoring, and deep store configuration is documented in the chart reference. Use it as a lookup when customizing `values.yaml` for your environment.

* [Helm Chart Values Reference](kubernetes/helm-chart-reference.md)

### Cloud provider specifics

#### Amazon EKS

When running Pinot on EKS with a Kafka cluster inside the same VPC, pay attention to `advertised.listeners` configuration and Security Group rules. If Kafka consumers run outside EKS (Lambdas, EC2), the default advertised listeners will not resolve correctly.

* [Amazon EKS (Kafka)](kubernetes/non-eks-to-eks.md)

#### Connecting to Amazon MSK

Integrating Pinot real-time tables with Amazon Managed Streaming for Apache Kafka (MSK) requires VPC connectivity (or VPC peering), Security Group cross-references between EKS and MSK, and plaintext broker endpoints for the Pinot stream config.

* [Amazon MSK (Kafka)](kubernetes/how-to-connect-pinot-with-amazon-managed-streaming-for-apache-kafka-amazon-msk.md)

### Security hardening

The default Helm chart ships without authentication or TLS. Before exposing any Pinot service, apply the following controls:

1. **TLS** -- Terminate TLS at an Ingress or API gateway (simplest), or configure end-to-end TLS with Pinot keystores and truststores. For mTLS between Pinot components, enable 2-way TLS.
2. **Authentication** -- Enable HTTP Basic Auth with ACLs on the controller and broker. Choose file-based config or ZooKeeper-backed config with encrypted passwords.
3. **Secrets management** -- Store credentials in Kubernetes Secrets and inject them via environment variable templating. Never hardcode passwords in `values.yaml` or ConfigMaps.
4. **Network policies** -- Restrict ingress to controller and broker pods. Keep server and ZooKeeper as internal-only ClusterIP services.

The deployment guide includes a full hardening checklist:

* [Kubernetes Deployment -- Security](kubernetes/deployment-pinot-on-kubernetes.md#security)

## Prerequisites

* A running Kubernetes cluster (1.20+) with `kubectl` access.
* Helm 3.x installed.
* A block-storage StorageClass appropriate for your cloud provider (EBS `gp3`, GCE `pd-ssd`, Azure Disk).
* Deep storage bucket or container (S3, GCS, ADLS) created and accessible from the cluster.

## Validate

After deploying, confirm the cluster is healthy:

```bash
# All pods running
kubectl get pods -n pinot-quickstart

# Controller API responds
kubectl port-forward svc/pinot-controller 9000:9000 -n pinot-quickstart
curl http://localhost:9000/health

# Broker query endpoint responds
kubectl port-forward svc/pinot-broker 8099:8099 -n pinot-quickstart
curl http://localhost:8099/health
```
