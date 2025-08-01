---
description: Introduces the new Multistage Engine Lite Mode
---

# Multistage Lite Mode

## Multistage Engine Lite Mode (Beta)

{% hint style="warning" %}
MSE Lite Mode is included in Pinot 1.4 and is currently in Beta.
{% endhint %}

Multistage Engine (MSE) Lite Mode is a new Query Mode that aims to enable safe access to the MSE for all Pinot users. One of the risks with running regular MSE queries is that users can easily write queries that scan a lot of records or run significantly expensive operations. Such queries can impact the reliability of a tenant and create friction in onboarding new use-cases. Lite Mode aims to address this problem. It is based on the observation that most of the users need access to advanced SQL features like Window Functions, Subqueries, etc., and aren't interested in scanning a lot of data or running fully Distributed Joins.

### Design

MSE Lite Mode has the following key characteristics:

* Users can still use all MSE query features like Window Functions, Subqueries, Joins, etc.
* But, the maximum number of rows returned by a Leaf Stage will be set to a user configurable value. The default value is `100,000`.
* Query execution follows a scatter-gather paradigm, similar to the Single-stage Engine. This is different from regular MSE that uses shuffles across Pinot Servers.
* Leaf stage(s) are run in the Servers, and all other operators are run using a single thread in the Broker.

Leaf Stage in a Multistage Engine query usually refers to Table Scan, an optional Project, an optional Filter and an optional Aggregate Plan Node.

At present, all joins in MSE Lite Mode are run in the Broker. This may change with the next release, since Colocated Joins can theoretically be run in the Servers.

### Enabling Lite Mode

To use Lite Mode, you can use the following query options.

```sql
SET useMultistageEngine=true;
SET usePhysicalOptimizer=true;  -- enables the new Physical MSE Query Optimizer
SET useLiteMode=true;           -- enables Lite Mode
```
