---
description: This page describes how to rebalance a table
---

# Rebalance

Rebalance operation is used to recompute assignment of brokers or servers in the cluster. This is not a single command, but more of a series of steps that need to be taken.

In case of servers, rebalance operation is used to balance the distribution of the segments amongst the servers being used by a Pinot table. This is typically done after capacity changes, or config changes such as replication or segment assignment strategies.

In case of brokers, rebalance operation is used to recalculate the broker assignment to the tables. This is typically done after capacity changes (scale up/down brokers).

In few cases such as when a server is tagged or untagged to a tenant i.e. server is added or removed from a tenant we need to rebalance all the tables that belong to that tenant.

{% content-ref url="rebalance-servers.md" %}
[rebalance-servers.md](rebalance-servers.md)
{% endcontent-ref %}

{% content-ref url="rebalance-brokers.md" %}
[rebalance-brokers.md](rebalance-brokers.md)
{% endcontent-ref %}

{% content-ref url="rebalance-tenant.md" %}
[rebalance-tenant.md](rebalance-tenant.md)
{% endcontent-ref %}



##
