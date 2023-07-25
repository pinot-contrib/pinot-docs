---
description: Set up HTTP basic auth and ACLs for access to controller and broker
---

# Authentication, Authorization, and ACLs

Apache Pinot 0.8.0+ comes out of the box with support for HTTP Basic Auth. While disabled by default for easier setup, authentication and authorization can be added to any environment simply via configuration. ACLs can be set on both API and table levels. This upgrade can be performed with zero downtime in any environment that provides replication.

For external access, Pinot exposes two primary APIs via the following components:

* **pinot-controller** handles cluster management and configuration
* **pinot-broker** handles incoming SQL queries

Both components can be protected via auth and even be configured independently. This makes it is possible to separate accounts for administrative functions such as table creation from accounts that are read the contents of tables in production.

Additionally, all other Pinot components such as **pinot-server** and **pinot-minion** can be configured to authenticate themselves to pinot-controller via the same mechanism. This can be done independently of (and in addition to) using 2-way TLS/SSL to ensure intra-cluster authentication on the lower networking layer.

## Quickstart

If you'd rather dive directly into the action with an all-in-one running example, we provide an **AuthQuickstart** runnable with Apache Pinot. This sample app is preconfigured with the settings below but only intended as a dev-friendly, local, single-node  deployment.

{% content-ref url="basic-auth-access-control.md" %}
[basic-auth-access-control.md](basic-auth-access-control.md)
{% endcontent-ref %}

{% content-ref url="zk-basic-auth-access-control.md" %}
[zk-basic-auth-access-control.md](zk-basic-auth-access-control.md)
{% endcontent-ref %}



##
