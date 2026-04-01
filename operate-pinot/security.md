# Security

This section covers how to secure an Apache Pinot cluster -- authentication, authorization, access control lists (ACLs), TLS/mTLS encryption, and secrets management.

## Why security matters

By default, Pinot ships with all security disabled (`AllowAllAccessFactory`) so you can get started quickly. Before promoting any cluster beyond development, you should enable at least authentication and transport encryption.

## Security layers

Pinot security is organized into three independent layers that can be adopted incrementally:

<table>
  <thead>
    <tr>
      <th>Layer</th>
      <th>What it protects</th>
      <th>Key mechanism</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Authentication**</td>
      <td>Verifies the identity of users and services</td>
      <td>HTTP Basic Auth (static config or ZooKeeper-managed)</td>
    </tr>
    <tr>
      <td>**Authorization / ACLs**</td>
      <td>Controls what each principal can do</td>
      <td>Per-table and per-operation permissions, Row-Level Security (RLS)</td>
    </tr>
    <tr>
      <td>**Transport encryption (TLS)**</td>
      <td>Protects data in transit between clients, brokers, servers, and controllers</td>
      <td>1-way or 2-way (mutual) TLS</td>
    </tr>
  </tbody>
</table>

## Authentication models

Pinot provides two built-in authentication backends. Both use HTTP Basic Auth, but they differ in how user credentials are stored and managed.

### Static Basic Auth (`BasicAuthAccessControlFactory`)

Credentials and permissions are declared in each component's properties file. Changes require a config update and rolling restart. Best for small clusters with stable user lists.

### ZooKeeper-managed Basic Auth (`ZkBasicAuthAccessControlFactory`)

Credentials are stored in ZooKeeper with bcrypt encryption. Users can be created and modified through the Pinot controller UI with hot deployment -- no restart required. Best for environments that need dynamic user management.

Both backends support:

- Separate user definitions for the controller and broker
- Table-level and operation-level (CREATE, READ, UPDATE, DELETE) ACLs
- Service tokens for inter-component authentication (server, minion, controller)

## Authorization and Row-Level Security

Beyond table-level ACLs, Pinot 1.4.0+ supports **Row-Level Security (RLS)**. RLS injects additional WHERE-clause predicates per principal, so different users see only the rows they are authorized to view. This is configured per-user, per-table, and works transparently -- the broker rewrites queries before execution.

For custom authorization logic, implement the `AccessControlFactory` interface and configure it via `controller.admin.access.control.factory.class` (controller) or `pinot.broker.access.control.class` (broker).

## TLS / mTLS

Pinot supports TLS for both client-to-cluster and intra-cluster connections. A zero-downtime migration path lets you add TLS to a running cluster in phases:

1. Add a secondary HTTPS listener alongside the existing HTTP listener
2. Switch inter-component egress to prefer HTTPS
3. Disable the HTTP listener

Two-way TLS (mutual TLS / mTLS) adds client certificate verification, ensuring that only trusted components and clients can connect.

## Secrets management

Credentials stored in plain-text config files are a risk in production. Pinot supports **Dynamic Environment Configuration** so you can inject secrets from environment variables or external stores (for example, Kubernetes Secrets, HashiCorp Vault) rather than hardcoding them in property files. See the [Dynamic Environment Configuration](../configuration-reference/dynamic-environment.md) reference for details.

## Prerequisites

Before enabling security, ensure:

- All Pinot components (controller, broker, server, minion) are at version 0.8.0+ for Basic Auth, or 0.10.0+ for ZK-managed auth
- For TLS: JKS or PKCS12 keystores and truststores have been generated for each component
- For production: a secrets management solution is in place for credential injection

## Child pages

<table>
  <thead>
    <tr>
      <th>Page</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Access Control](../operators/operating-pinot/access-control.md)</td>
      <td>ACL framework, custom `AccessControlFactory`, and Row-Level Security (RLS)</td>
    </tr>
    <tr>
      <td>[Authentication overview](../tutorials/operations/authentication/README.md)</td>
      <td>Introduction to Pinot's HTTP Basic Auth and links to setup guides</td>
    </tr>
    <tr>
      <td>[Basic Auth Access Control](../tutorials/operations/authentication/basic-auth-access-control.md)</td>
      <td>Step-by-step setup of static Basic Auth for controller, broker, server, and minion</td>
    </tr>
    <tr>
      <td>[ZK Basic Auth Access Control](../tutorials/operations/authentication/zkbasicauthaccesscontrol.md)</td>
      <td>ZooKeeper-managed Basic Auth with hot deployment and bcrypt encryption</td>
    </tr>
    <tr>
      <td>[Configuring TLS/SSL](../tutorials/operations/configuring-tls-ssl.md)</td>
      <td>Listener configuration, zero-downtime TLS migration, and 2-way TLS setup</td>
    </tr>
  </tbody>
</table>

## Next step

Once your cluster is secured, set up observability to detect issues early. Continue to [Monitoring](monitoring.md).
