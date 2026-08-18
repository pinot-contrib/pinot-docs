# Lookup join strategy

Lookup join is a special join strategy that can be applied when one of the tables is a [dimension table](../../../../build-with-pinot/ingestion/batch-ingestion/dim-table.md). In that case, Pinot can take advantage of the fact that dimension tables are guaranteed to be replicated in all the servers of a given tenant, so it can execute the join without shuffling data between servers.

{% hint style="info" %}
Lookup joins provide a similar performance to [Lookup UDF](../../lookup-udf-join.md) Join, the only kind of join that was supported in SSE. The lookup UDF should not be used in multi-stage queries
{% endhint %}

This technique was introduced in Pinot 1.3.0 and it is disabled by default. It can be enabled for specific queries by specifying the `joinOptions` hint in the SELECT clause. There are also some prerequisites/limitations in the current implementation:

* Right table must be configured as a dimension table.
* Every primary-key column of the right table must receive exactly one lookup value. The value can come from an equi-join key or an equality to a literal in the `ON` or `WHERE` condition.
* The order of predicates does not need to match the order of `primaryKeyColumns`; Pinot builds the lookup key in schema order.
* A join key on a non-primary-key dimension column, duplicate keys for one primary-key column, or a missing primary-key component causes the query to fail instead of silently returning empty or incorrect results. Remove the lookup hint to use a regular join for those conditions.

For example:

```sql
SELECT /*+ joinOptions(join_strategy='lookup') */
    A.col1, B.col2
FROM A
JOIN B -- this must be a dimension table
ON A.col2 = B.joinKey -- B.joinKey must be the primary key of B
```

For a compound key such as `primaryKeyColumns: ["currency", "rate_start_date"]`, a literal can supply one key component:

```sql
SELECT /*+ joinOptions(join_strategy='lookup') */
    f.amount, r.rate
FROM fact_sales f
JOIN dim_rates r
  ON r.rate_start_date = f.rate_start_date
 AND r.currency = 'gbp'
```

The predicate order can be reversed without changing the lookup. A literal on a `BYTES` primary-key column is not supported. `SEMI` and `ANTI` lookup joins do not support non-equi conditions because their output does not include right-table columns needed to evaluate those filters.


## Physical Optimizer Support

As of Pinot 1.6.0, lookup joins are now supported by the V2 physical optimizer. Previously, attempting to use lookup join with the physical optimizer would fail with "Right input must be leaf operator" because the optimizer would insert a BROADCAST_EXCHANGE on the dimension table, splitting it into a separate fragment incompatible with LookupJoinOperator.

When using lookup joins with the V2 physical optimizer:
* The dimension table remains as a `LeafOperator` in the same fragment as the join
* The EXPLAIN plan will show a `LOOKUP_LOCAL_EXCHANGE` pseudo-exchange on the dimension table side
* This pseudo-exchange does not cause data to be split into a separate fragment; it is purely for plan representation

**Current limitations:**
* Lookup joins in MSE lite mode are not yet supported
* Auto-detection of lookup joins based on dimension table + primary key join conditions is not yet implemented
