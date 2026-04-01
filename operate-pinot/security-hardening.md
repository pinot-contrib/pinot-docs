---
description: Operator-facing guide to hardening an Apache Pinot cluster for production
---

# Security Hardening Guide

This guide is an operator-facing companion to the individual security pages (authentication, access control, TLS). It ties those features together into a single hardening checklist and explains the decisions you need to make when moving a Pinot cluster from "works on my laptop" to production.

## Threat model at a glance

A Pinot cluster has several network boundaries worth thinking about:

| Boundary | Who talks here | Risk if unsecured |
|---|---|---|
| **Client → Broker** | BI tools, application code, ad-hoc analysts | Unauthorized query access, data exfiltration |
| **Client → Controller** | Operators, CI/CD, Pinot CLI | Unauthorized admin actions (table creation, schema changes, segment uploads) |
| **Controller ↔ Broker ↔ Server ↔ Minion** | Internal Pinot components | Spoofed components, unencrypted data in transit |
| **Controller / Server → Deep Store** | Segment reads and writes (S3, GCS, HDFS, etc.) | Segment data exposure |
| **Controller → ZooKeeper** | Cluster metadata, helix state | Metadata tampering, credential leakage |
| **Broker → Kafka / Pulsar / Kinesis** | Stream consumption | Unauthenticated stream reads, data in transit exposure |

A hardened cluster adds authentication, authorization, and encryption at each of these boundaries.

## Which endpoints should be public?

In most deployments, only the **broker query endpoint** needs to be reachable from application networks. Everything else should be internal.

| Component | Default Port | Expose Externally? | Notes |
|---|---|---|---|
| Broker (query API) | 8099 | Yes (via load balancer) | The only endpoint that application code and BI tools need. Lock down with auth and TLS. |
| Controller (admin API + UI) | 9000 | Usually no | Restrict to operator VPN or bastion. If exposed, require authentication and TLS. |
| Server (data) | 8098 | No | Only brokers and controllers need to reach servers. |
| Minion | 9514 | No | Only the controller needs to reach minions. |
| ZooKeeper | 2181 | No | Internal only. Consider ZK auth (see below). |

**Recommendation:** Place brokers behind an external load balancer with TLS termination or passthrough. Place all other components on an internal network or use Kubernetes NetworkPolicies to restrict cross-namespace traffic.

## Step-by-step hardening

### 1. Enable authentication

Pinot ships with `AllowAllAccessFactory` by default -- no auth at all. Start by enabling one of the two built-in Basic Auth backends.

**Choosing an auth backend:**

| | Static Basic Auth | ZK-managed Basic Auth |
|---|---|---|
| **Config location** | Properties files on each component | ZooKeeper (bcrypt-encrypted) |
| **User changes** | Require config change + rolling restart | Hot deployment via controller UI |
| **Best for** | Small clusters, GitOps-managed config | Larger teams, dynamic user management |
| **Setup guide** | [Basic Auth Access Control](authentication/basic-auth-access-control.md) | [ZK Basic Auth Access Control](authentication/zkbasicauthaccesscontrol.md) |

**Alternatively**, if your organization uses an external identity provider, implement the `AccessControlFactory` interface to integrate with LDAP, OAuth 2.0, or your own token service. See [Access Control](../operators/operating-pinot/access-control.md) for the extension point.

Whichever method you choose, make sure to:

- Define a service token for controller-to-broker, controller-to-server, and controller-to-minion communication.
- Configure both the controller and broker with matching principal definitions.
- Protect ingestion jobs (Spark, Hadoop, Flink) with an appropriate service token.

### 2. Set up authorization and ACLs

Authentication alone proves identity; authorization decides what each identity can do.

- **Table-level ACLs**: Assign `CREATE`, `READ`, `UPDATE`, `DELETE` permissions per principal per table. If `*.principals.<user>.tables` is not configured, all tables are accessible to that user — configure an explicit allowlist (or `excludeTables`) to restrict access. Note that broker-level ACLs are always READ-only since all broker requests are queries.
- **Row-Level Security (RLS)** (Pinot 1.4.0+): Inject per-user WHERE-clause filters at the broker so different principals see different row subsets. Useful for multi-tenant workloads where one table serves many customers.

Configure ACLs in the same properties that define your principals:

```properties
# Example: "analyst" can only READ orders_table
pinot.broker.access.control.principals.analyst.tables=orders_table
pinot.broker.access.control.principals.analyst.permissions=READ

# Example: RLS filter — analyst sees only their own region
pinot.broker.access.control.principals.analyst.rls.orders_table=region='us-west'
```

For full details see [Access Control](../operators/operating-pinot/access-control.md).

### 3. Enable TLS for client-facing connections

At a minimum, encrypt traffic between clients and the broker/controller.

Setting keystore/truststore paths alone is not enough — you must also enable HTTPS listeners via the `*.access.protocols` properties. The example below shows a minimal broker and controller configuration with HTTPS enabled:

```properties
# Broker TLS — listener + certificates
pinot.broker.client.access.protocols=https
pinot.broker.client.access.protocols.https.port=8443
pinot.broker.tls.keystore.path=/opt/pinot/tls/broker-keystore.jks
pinot.broker.tls.keystore.password=broker-keystore-password
pinot.broker.tls.truststore.path=/opt/pinot/tls/truststore.jks
pinot.broker.tls.truststore.password=broker-truststore-password

# Controller TLS — listener + certificates
controller.access.protocols=https
controller.access.protocols.https.port=9443
controller.tls.keystore.path=/opt/pinot/tls/controller-keystore.jks
controller.tls.keystore.password=controller-keystore-password
controller.tls.truststore.path=/opt/pinot/tls/truststore.jks
controller.tls.truststore.password=controller-truststore-password
```

{% hint style="warning" %}
The passwords above are placeholders. Never commit real passwords to config files. Use [Dynamic Environment Configuration](../reference/configuration-reference/dynamic-environment.md) to inject secrets at runtime (see step 6 below).
{% endhint %}

{% hint style="info" %}
To keep HTTP available during a rolling migration, set `*.access.protocols=http,https` and configure both ports. See [Configuring TLS/SSL](configuring-tls-ssl.md) for the full three-phase zero-downtime migration process.
{% endhint %}

### 4. Enable mTLS for intra-cluster communication

Mutual TLS (two-way TLS) ensures that brokers only talk to genuine servers and controllers only accept connections from trusted components.

```properties
# Enable client certificate verification on the controller
controller.tls.client.auth.enabled=true

# Enable client certificate verification on the broker
pinot.broker.tls.client.auth.enabled=true

# Enable client certificate verification on the server
pinot.server.tls.client.auth.enabled=true

# Enable client certificate verification on the minion
pinot.minion.tls.client.auth.enabled=true
```

Each component presents its own certificate and validates the peer's certificate against the shared truststore. This prevents an attacker who gains network access from impersonating a Pinot component.

See the **2-way TLS** section in [Configuring TLS/SSL](configuring-tls-ssl.md) for a complete configuration example.

### 5. Secure ZooKeeper communication

ZooKeeper stores cluster metadata, helix state, and (if using `ZkBasicAuthAccessControlFactory`) user credentials. You should:

- **Network-isolate ZooKeeper**: Run it on an internal network with no external access.
- **Enable ZooKeeper authentication**: Configure SASL/Kerberos or digest-based auth so only authenticated Pinot components can read/write ZK znodes.
- **Enable ZooKeeper TLS** (ZooKeeper 3.5+): Encrypt the ZK client connections. Configure ZooKeeper servers with a TLS-enabled `secureClientPort` and JVM keystore/truststore options; point Pinot's ZooKeeper connection strings at that `secureClientPort`; and start Pinot components with `-Dzookeeper.client.secure=true`, `-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty`, and the appropriate `-Dzookeeper.ssl.*` JVM properties plus matching keystore/truststore options. See the ZooKeeper TLS section in [ZooKeeper configuration reference](../reference/configuration-reference/zookeeper.md) for a complete example.

### 6. Manage secrets properly

Hardcoding passwords in property files is the most common security mistake in Pinot deployments. Use **Dynamic Environment Configuration** to inject secrets at runtime:

```properties
# In the properties file, reference environment variables
dynamic.env.config=controller.admin.access.control.principals.admin.password,pinot.broker.tls.keystore.password

controller.admin.access.control.principals.admin.password=ADMIN_PASSWORD_ENV
pinot.broker.tls.keystore.password=BROKER_KS_PASSWORD_ENV
```

At startup, Pinot replaces each value with the contents of the named environment variable.

**Kubernetes deployments** should source these environment variables from Kubernetes Secrets:

```yaml
env:
  - name: ADMIN_PASSWORD_ENV
    valueFrom:
      secretKeyRef:
        name: pinot-secrets
        key: admin-password
  - name: BROKER_KS_PASSWORD_ENV
    valueFrom:
      secretKeyRef:
        name: pinot-tls
        key: keystore-password
```

For more advanced rotation workflows, mount secrets from **HashiCorp Vault**, **AWS Secrets Manager**, or **GCP Secret Manager** using a sidecar or init container and point the environment variables at the injected values.

See [Dynamic Environment Reference](../reference/configuration-reference/dynamic-environment.md) for the full syntax.

### 7. Secure stream connections

If you consume from Kafka, Pulsar, or Kinesis, the stream connection also needs authentication and encryption:

- **Kafka**: Configure `security.protocol=SASL_SSL` or `SSL` in the stream config section of your table config. Provide the keystore/truststore paths and credentials.
- **Pulsar**: Use `authPlugin` and `authParams` in the stream config.
- **Kinesis**: Use IAM roles (preferred) or access key / secret key pairs via environment variables.

These credentials appear in table configs, so store them using Dynamic Environment Configuration to avoid plain-text secrets in ZooKeeper.

### 8. Secure deep store access

Segments stored in S3, GCS, HDFS, or Azure Blob Storage should be protected:

- **S3**: Use IAM roles for service accounts (IRSA on EKS) rather than static access keys. Restrict the S3 bucket policy to the Pinot service account.
- **GCS**: Use Workload Identity on GKE. Restrict the bucket IAM policy.
- **HDFS**: Use Kerberos authentication and restrict directory permissions.
- **Azure Blob**: Use Managed Identity or service principal credentials injected via environment variables.

Avoid placing cloud credentials directly in Pinot property files.

## Production hardening checklist

Use this checklist to verify your cluster is production-ready:

- [ ] **Authentication enabled** on both controller and broker
- [ ] **Service tokens configured** for inter-component auth (controller → broker, controller → server, controller → minion, broker → server)
- [ ] **Table-level ACLs** restricting each principal to only the tables they need
- [ ] **Row-Level Security** configured for multi-tenant tables (Pinot 1.4.0+)
- [ ] **TLS enabled** on all client-facing endpoints (broker, controller)
- [ ] **mTLS enabled** for intra-cluster traffic (controller ↔ broker ↔ server ↔ minion)
- [ ] **ZooKeeper** network-isolated and authenticated
- [ ] **No plain-text passwords** in property files — all secrets injected via Dynamic Environment Configuration
- [ ] **Kubernetes Secrets** (or Vault / cloud secret managers) used for credential storage
- [ ] **Stream connections** (Kafka, Pulsar, Kinesis) use TLS + authentication
- [ ] **Deep store** access uses IAM roles or Workload Identity, not static keys
- [ ] **Controller UI** restricted to operator network (VPN, bastion, or NetworkPolicy)
- [ ] **Unused ports** firewalled or blocked by NetworkPolicy
- [ ] **Monitoring** configured to alert on auth failures and certificate expiry

## Common mistakes

| Mistake | Why it matters | Fix |
|---|---|---|
| Leaving `AllowAllAccessFactory` in production | Every request is authorized, even unauthenticated ones | Enable Basic Auth or a custom `AccessControlFactory` |
| Enabling auth on the broker but not the controller | Attackers bypass the broker and hit controller admin APIs directly | Enable auth on both components |
| Storing passwords in `pinot-controller.conf` committed to Git | Credentials leak into version control | Use Dynamic Environment Configuration with Kubernetes Secrets |
| Enabling TLS on client-facing ports but not intra-cluster | Internal traffic is readable to anyone with network access | Enable mTLS for all inter-component links |
| Using self-signed certificates without a private CA | No revocation path; can't distinguish legitimate from rogue certs | Set up an internal CA (or use cert-manager on Kubernetes) |
| Granting admin permissions to service tokens | A compromised minion or ingestion job has full cluster access | Create least-privilege service accounts with only the permissions each component needs |
| Forgetting to secure ZooKeeper | ZK stores ACL definitions and cluster state — full cluster compromise | Network-isolate ZK and enable SASL or digest auth |

## Network architecture example

A typical production deployment looks like this:

```
                    ┌──────────────────────────────────┐
                    │        External Network           │
                    │   (BI tools, app servers, users)  │
                    └───────────────┬──────────────────┘
                                    │ HTTPS (TLS)
                              ┌─────▼─────┐
                              │    LB /    │
                              │  Ingress   │
                              └─────┬──────┘
                                    │ HTTPS
            ┌───────────────────────┼──────────────────────┐
            │                 Internal Network              │
            │                                               │
            │  ┌──────────┐   mTLS   ┌──────────┐         │
            │  │ Broker(s)│◄────────►│Server(s) │         │
            │  └────┬─────┘          └──────────┘         │
            │       │ mTLS                                  │
            │  ┌────▼──────┐  mTLS   ┌──────────┐         │
            │  │Controller │◄───────►│ Minion(s)│         │
            │  └────┬──────┘         └──────────┘         │
            │       │                                       │
            │  ┌────▼──────┐                               │
            │  │ ZooKeeper │  (SASL / network-isolated)    │
            │  └───────────┘                               │
            └───────────────────────────────────────────────┘
```

- External clients connect only to brokers through a load balancer.
- Controller UI / admin API access is restricted to operators (VPN or bastion).
- All internal links use mTLS.
- ZooKeeper is fully internal with authentication enabled.

## Related pages

| Page | Description |
|---|---|
| [Security overview](security.md) | High-level summary of Pinot's security layers |
| [Basic Auth Access Control](authentication/basic-auth-access-control.md) | Static Basic Auth setup |
| [ZK Basic Auth Access Control](authentication/zkbasicauthaccesscontrol.md) | ZooKeeper-managed Basic Auth setup |
| [Access Control](../operators/operating-pinot/access-control.md) | ACL framework and Row-Level Security |
| [Configuring TLS/SSL](configuring-tls-ssl.md) | Listener specs, zero-downtime TLS migration, mTLS |
| [Dynamic Environment Reference](../reference/configuration-reference/dynamic-environment.md) | Secret injection via environment variables |
