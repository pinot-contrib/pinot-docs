# Lookup join strategy

Lookup join is a special join strategy that can be applied when one of the tables is a [dimension table](../../../../manage-data/data-import/batch-ingestion/dim-table.md). In that case, Pinot can take advantage of the fact that dimension tables are guaranteed to be replicated in all the servers of a given tenant, so it can execute the join without shuffling data between servers.

{% hint style="info" %}
Lookup joins provide a similar performance to [Lookup UDF](../../lookup-udf-join.md) Join, the only kind of join that was supported in SSE. The lookup UDF should not be used in multi-stage queries
{% endhint %}

This technique was introduced in Pinot 1.3.0 and it is disabled by default. It can be enabled for specific queries by specifying the `joinOptions` hint in the SELECT clause. There are also some prerequisites/limitations in the current implementation:

* Right table must be configured as a dimension table.
* Primary key of the right table must be used as the join key. If the primary key is a compound key of multiple columns, all the columns must be used as the join key.

For example:

```sql
SELECT /*+ joinOptions(join_strategy='lookup') */
    A.col1, B.col2
FROM A
JOIN B -- this must be a dimension table
ON A.col2 = B.joinKey -- B.joinKey must be the primary key of B
```

