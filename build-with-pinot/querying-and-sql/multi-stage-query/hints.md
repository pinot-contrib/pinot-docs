# Hints

Multi-stage query engine behavior can be customized with hints. Hints are provided as a comment, for example `/* hintType(hint1='value1',hint2='value2') */`.

Apache Pinot supports the following hints:

* `aggOptions`, explained in [aggregate operator](operator-types/aggregate.md#hints).
* `windowOptions`, explained in [window operator](operator-types/window.md#hints).
* `joinOptions`, explained in [join operator](operator-types/hash_join.md#hints).
* `setOpOptions`, explained in [union](operator-types/union.md#hints), [intersect](operator-types/intersect.md#hints), and [minus](operator-types/minus.md#hints).

## setOpOptions

Use `setOpOptions` to control the exchange Pinot inserts below `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT` / `MINUS`.

### is_colocated_by_set_op_keys

Type: Boolean

Default: planner chosen

When the option is unset, the V1 planner auto-detects whether each set-op input is already partitioned compatibly and can use a direct exchange. You can override that decision explicitly:

* `'true'` forces a pre-partitioned direct exchange on every input.
* `'false'` forces a shuffled hash exchange on every input.

This hint is only honored by the V1 planner. The V2 physical optimizer ignores it and determines set-op colocation on its own.

Pinot accepts the hint in two places:

* Inline on the first branch:

```sql
SELECT /*+ setOpOptions(is_colocated_by_set_op_keys='true') */ col FROM a
UNION ALL
SELECT col FROM b
```

* On an outer `SELECT` that wraps the set operation:

```sql
SELECT /*+ setOpOptions(is_colocated_by_set_op_keys='true') */ *
FROM (
  SELECT col FROM a
  INTERSECT
  SELECT col FROM b
)
```

{% hint style="warning" %}
Only force `'true'` when every input is partitioned compatibly on one or more projected columns, so equal full output rows land on the same worker. If that is not true, `INTERSECT`, `EXCEPT`, and plain `UNION` can return wrong results. `UNION ALL` is always safe because it only concatenates rows.
{% endhint %}

Use the outer-wrap form for plain `UNION`, which Pinot rewrites before the exchange rule resolves the inline hint. Prefer the outer-wrap form for nested `INTERSECT` or `EXCEPT` queries too when you want the hint to apply at every set-op level.
