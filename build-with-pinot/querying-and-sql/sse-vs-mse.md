---
description: Understand the differences between the single-stage (v1) and multi-stage (v2) query engines and when to use each.
---

# Query Engines (SSE vs MSE)

Pinot ships two query engines. The **single-stage engine (SSE, v1)** uses a scatter-gather model and is the default for simple analytic queries. The **multi-stage engine (MSE, v2)**, released in Pinot 1.0.0, adds distributed joins, window functions, and other multi-stage operators.

## Quick decision

| If your query needs… | Use | Why |
| --- | --- | --- |
| Basic filtering, projection, aggregation | SSE | Lowest overhead; simple scatter-gather model |
| JOINs | MSE | JOIN support requires the multi-stage engine |
| Window functions | MSE | Window functions require multi-stage execution |
| Colocated or partitioned joins | MSE | These are multi-stage patterns |
| Complex operator trees or advanced SQL | MSE | Built for distributed query planning |

## Single-stage engine (v1)

The single-stage engine uses a scatter-gather execution model. The broker receives a query, fans it out to the relevant servers, each server processes its local segments, and the broker merges the partial results.

![](../../.gitbook/assets/Multi-Stage-Pinot-Query-Engine-v1 (2).png)

*Single-stage query engine (v1)*

**Choose SSE when:**

- The query is a plain scatter-gather read over one or more tables
- You only need functions available in both engines
- You want the lowest conceptual and operational overhead

SSE is the default fit for the most common Pinot workloads: filter, project, group, and aggregate.

## Multi-stage engine (v2)

The multi-stage engine decouples the data exchange layer from the query engine layer. It breaks queries into multiple sub-plans ("stages") that run across different sets of servers.

![](../../.gitbook/assets/Multi-Stage-Query-Engine-2 (2).png)

*Multi-stage query execution model*

**Choose MSE when:**

- You need `JOIN`, window functions, or subqueries
- You need distributed query execution with intermediate stages
- You are running complex ANSI SQL

**When not to use MSE:**

- Large-scale, long-running queries that access entire datasets (MSE is pure in-memory)
- Complex joins touching many tables with non-trivial join conditions
- ETL-type workloads

### How queries are processed

Pinot breaks the query into stages connected in a tree structure:

1. **Leaf stages** — read from tables and send data to the next stage
2. **Intermediate stages** — process data (e.g., perform joins) and pass results along
3. **Root stage** — sends final results to the client

Each stage is assigned a parallelism level, and multiple servers execute that stage in parallel.

### Null handling

Since Pinot 1.1.0, the multi-stage engine supports null handling when column-based null storing is enabled. Before 1.1.0, all columns were treated as non-nullable.

## How to enable MSE

### Option 1: Query Console

In the Pinot Query Console, select the **Use Multi-Stage Engine** checkbox.

![](../../.gitbook/assets/pinot-query-console-multi-stage-enabled (2).png)

*Pinot Query Console with Use Multi Stage Engine enabled*

### Option 2: Query option

Add the query option at the top of your query:

```sql
SET useMultistageEngine=true;
SELECT * FROM baseballStats LIMIT 10;
```

### Option 3: REST API

Pass the option in the JSON payload:

```bash
curl -X POST http://localhost:9000/sql -d '
{
  "sql": "select * from baseballStats limit 10",
  "trace": false,
  "queryOptions": "useMultistageEngine=true"
}'
```

## Engine support in function docs

The function index uses an engine column to indicate availability:

- `Both` — safe in either engine
- `Multi-stage only` — requires MSE
- `Varies` — depends on the specific implementation

{% embed url="https://www.youtube.com/watch?v=wbo_vPVIBkA" fullWidth="false" %}
Apache Pinot 1.0 Multi-Stage Query Engine overview
{% endembed %}
