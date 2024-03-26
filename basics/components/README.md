---
description: >-
  Discover the core components of Apache Pinot, enabling efficient data
  processing and analytics. Unleash the power of Pinot's building blocks for
  high-performance data-driven applications.
---

# Components

Apache Pinot™ is a database designed to deliver highly concurrent, ultra-low-latency queries on large datasets through a set of common data model abstractions. Delivering on these goals requires several foundational architectural commitments, including:

* Storing data in columnar form to support high-performance scanning
* Sharding of data to scale both storage and computation
* A distributed architecture designed to scale capacity linearly
* A tabular data model read by SQL queries

## Components

Learn about the major components and logical abstractions used in Pinot.

![](../../.gitbook/assets/pinot-system-architecture.png)

#### Operator reference

{% content-ref url="cluster/" %}
[cluster](cluster/)
{% endcontent-ref %}

{% content-ref url="cluster/controller.md" %}
[controller.md](cluster/controller.md)
{% endcontent-ref %}

{% content-ref url="cluster/broker.md" %}
[broker.md](cluster/broker.md)
{% endcontent-ref %}

{% content-ref url="cluster/server.md" %}
[server.md](cluster/server.md)
{% endcontent-ref %}

{% content-ref url="cluster/minion.md" %}
[minion.md](cluster/minion.md)
{% endcontent-ref %}

{% content-ref url="cluster/tenant.md" %}
[tenant.md](cluster/tenant.md)
{% endcontent-ref %}

#### Developer reference

{% content-ref url="table/" %}
[table](table/)
{% endcontent-ref %}

{% content-ref url="table/schema.md" %}
[schema.md](table/schema.md)
{% endcontent-ref %}

{% content-ref url="table/segment/" %}
[segment](table/segment/)
{% endcontent-ref %}
