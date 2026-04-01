---
description: Understand the differences between the single-stage engine (SSE) and multi-stage engine (MSE) and when to use each.
---

# Query Engines (SSE vs MSE)

Pinot ships two supported query engines. The **single-stage engine (SSE)** uses a scatter-gather model and is the default for simple analytic queries. The **multi-stage engine (MSE)** supports distributed joins, window functions, subqueries, and other advanced SQL operations.

SSE is the default because it has lower overhead for the most common Pinot workloads; that default does not imply that MSE is experimental. MSE is Pinot's supported engine for queries that require relational operators beyond simple scatter-gather execution.

> **History:** MSE was introduced as the "v2 query engine" in Pinot 1.0.0. You may still see references to "v1" and "v2" in configuration properties such as `useMultistageEngine`.

## Quick decision

| If your query needs… | Use | Why |
| --- | --- | --- |
| Basic filtering, projection, aggregation | SSE | Lowest overhead; simple scatter-gather model |
| JOINs | MSE | JOIN support requires the multi-stage engine |
| Window functions | MSE | Window functions require multi-stage execution |
| Colocated or partitioned joins | MSE | These are multi-stage patterns |
| Complex operator trees or advanced SQL | MSE | Built for distributed query planning |

## Single-stage engine (SSE)

The single-stage engine uses a scatter-gather execution model. The broker receives a query, fans it out to the relevant servers, each server processes its local segments, and the broker merges the partial results.

![](<../../.gitbook/assets/Multi-Stage-Pinot-Query-Engine-v1 (2).png>)

*Single-stage query engine (SSE)*

**Choose SSE when:**

- The query is a plain scatter-gather read over one or more tables
- You only need functions available in both engines
- You want the lowest conceptual and operational overhead

SSE is the default fit for the most common Pinot workloads: filter, project, group, and aggregate.

## Multi-stage engine (MSE)

The multi-stage engine decouples the data exchange layer from the query engine layer. It breaks queries into multiple sub-plans ("stages") that run across different sets of servers.

![](<../../.gitbook/assets/Multi-Stage-Query-Engine-2 (2).png>)

*Multi-stage query execution model*

**Choose MSE when:**

- You need `JOIN`, window functions, or subqueries
- You need distributed query execution with intermediate stages
- You are running complex ANSI SQL

**Workloads better served by SSE or external query engines:**

- Large-scale, long-running queries that scan entire datasets — MSE executes in-memory without spill-to-disk, so very large intermediate result sets can exceed available memory
- Heavy ETL-style joins across many tables — consider an external engine such as Trino or Spark for batch-oriented workloads
- Simple scatter-gather queries (filter, aggregate, top-K) — SSE handles these with lower overhead

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

![](<../../.gitbook/assets/pinot-query-console-multi-stage-enabled (2).png>)

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

## Running MSE in production

For operational guidance on resource planning, guardrails, and known limitations when running MSE in production, see [Run the Multi-Stage Engine in Production](../../operate-pinot/production-guides/run-multi-stage-engine-in-production.md).

{% embed url="https://www.youtube.com/watch?v=wbo_vPVIBkA" fullWidth="false" %}
Apache Pinot 1.0 Multi-Stage Query Engine overview
{% endembed %}
