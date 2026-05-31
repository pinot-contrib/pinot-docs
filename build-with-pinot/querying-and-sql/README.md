---
description: Learn how to query Apache Pinot, choose the right query engine, and find SQL and function guidance quickly.
---

# Querying & SQL

Use this section to decide how to query Pinot, how much SQL support you need, which query engine to use, and where to look for execution controls such as quotas, cancellation, and cursors. Narrative guidance lives here. Dense syntax and endpoint detail is linked where needed.

## Start here

{% content-ref url="querying-pinot.md" %}
[querying-pinot.md](querying-pinot.md)
{% endcontent-ref %}

{% content-ref url="sql-syntax.md" %}
[sql-syntax.md](sql-syntax.md)
{% endcontent-ref %}

{% content-ref url="sql-ddl.md" %}
[sql-ddl.md](sql-ddl.md)
{% endcontent-ref %}

{% content-ref url="materialized-views.md" %}
[materialized-views.md](materialized-views.md)
{% endcontent-ref %}

{% content-ref url="../../functions/README.md" %}
[Functions](../../functions/README.md)
{% endcontent-ref %}

{% content-ref url="sse-vs-mse.md" %}
[sse-vs-mse.md](sse-vs-mse.md)
{% endcontent-ref %}

{% content-ref url="query-execution-controls/README.md" %}
[query-execution-controls/README.md](query-execution-controls/README.md)
{% endcontent-ref %}

## Deep dives

For explain plans, joins, optimizer behavior, and operator details, continue into the multi-stage query docs and engine-specific material linked from [SSE vs MSE](sse-vs-mse.md) and [SQL syntax](sql-syntax.md).

## What this page covered

This page mapped the main query workflows in Pinot: learning the query path, understanding SQL behavior, finding functions, choosing between SSE and MSE, using controller-managed SQL DDL for tables and materialized views, and tuning execution controls.

## Next step

Read [Querying Pinot](querying-pinot.md) if you want the end-to-end query flow, or [SSE vs MSE](sse-vs-mse.md) if you are deciding which engine to use.

## Related pages

- [Build with Pinot](../README.md)
- [Materialized Views](materialized-views.md)
- [Functions](../../functions/README.md)
- [Reference](../../reference/README.md)
