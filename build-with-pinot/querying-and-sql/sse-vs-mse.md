---
description: Decide whether a Pinot query should use the single-stage engine or the multi-stage engine.
---

# SSE vs MSE

Use the single-stage engine when the query is straightforward and benefits from the lower overhead of scatter-gather execution. Use the multi-stage engine when the query needs distributed joins, window functions, or other multi-stage operators.

## Quick decision

| If your query needs... | Prefer | Why |
| --- | --- | --- |
| Basic filtering, projection, and standard aggregation | SSE | It is the simplest execution model and keeps query planning compact. |
| JOINs | MSE | Pinot documents JOIN support on the multi-stage engine. |
| Window functions | MSE | Window functions require the multi-stage engine. |
| Query-time partitioned or colocated joins | MSE | These are multi-stage patterns. |
| Complex operator trees or advanced SQL execution | MSE | The engine is built for distributed query planning and stage-level execution. |

## Choose SSE when

- The query is a plain scatter-gather read over one or more tables.
- You only need the function families that are already available in both engines.
- You want the lowest conceptual and operational overhead.

SSE is the default fit for the most common Pinot workloads: filter, project, group, and aggregate.

## Choose MSE when

- You need `JOIN`.
- You need window functions.
- You need distributed query execution with intermediate stages.
- You are following the multi-stage query syntax, explain plan, or stage stats workflow.

The multi-stage engine was released in Pinot 1.0.0. Since Pinot 1.1.0, it also supports null handling when column-based null storing is enabled.

## Engine cues in function docs

The function index uses an engine column to indicate whether a function is available in SSE, MSE, or both. Use that signal as the final check after you decide which engine the query shape needs.

- `Both` means the function is safe to consider in either engine.
- `Multi-stage only` means the function depends on the distributed execution model.
- `Varies` means the support depends on the implementation or the extension that provides the function.

## How to enable MSE

When you want to force the multi-stage engine, set the query option explicitly:

```sql
SET useMultistageEngine=true;
SELECT * FROM baseballStats LIMIT 10;
```

You can also enable it from the Query Console or via the REST-based query flow described in the multi-stage setup guide.

## Related docs

- [Single-stage query engine (v1)](../../reference/single-stage-engine.md)
- [Multi-stage query engine (v2)](../../reference/multi-stage-engine.md)
- [Use the multi-stage query engine (v2)](../../developers/advanced/v2-multi-stage-query-engine.md)
- [JOINs](../../users/user-guide-query/joins.md)

## What this page covered

- The practical rule for choosing between SSE and MSE.
- The Pinot features that require MSE.
- The version milestones and query option used to enable MSE.

## Next step

- Confirm the engine choice before you design the query, then open the join, window, or function page that matches the pattern.

## Related pages

- [Functions](../../functions/README.md)
- [Transformations](../../functions/transformations.md)
- [JOINs](../../users/user-guide-query/joins.md)
- [Multi-stage query engine (v2)](../../reference/multi-stage-engine.md)
