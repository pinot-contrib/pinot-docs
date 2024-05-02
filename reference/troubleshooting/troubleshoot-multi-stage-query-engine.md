---
description: Troubleshoot issues with the multi-stage query engine (v2).
---

# Troubleshoot issues with the multi-stage query engine (v2)

Learn how to [troubleshoot errors](troubleshoot-multi-stage-query-engine.md#troubleshoot-errors) when using the multi-stage query engine (v2), and see [multi-stage query engine limitations](troubleshoot-multi-stage-query-engine.md#limitations-of-the-multi-stage-query-engine).&#x20;

Find instructions on [how to enable the multi-stage query engine](v2-multi-stage-query-engine.md), or see a high-level overview of [how the multi-stage query engine works](../../reference/multi-stage-engine.md).

## Limitations of the multi-stage query engine&#x20;

We are continuously improving the multi-stage query engine. A few limitations to call out:

### Support for multi-value columns is limited

Support for multi-value columns is limited to projections, and predicates must use the `arrayToMv` function. For example, to successfully run the following query:

{% code overflow="wrap" %}
```sql
-- example 1: used in GROUP-BY
SELECT count(*), RandomAirports FROM airlineStats 
GROUP BY RandomAirports

-- example 2: used in PREDICATE
SELECT * FROM airlineStats WHERE RandomAirports IN ('SFO', 'JFK')

-- example 3: used in ORDER-BY
SELECT count(*), RandomAirports FROM airlineStats 
GROUP BY RandomAirports
ORDER BY RandomAirports DESC
```
{% endcode %}

You must include `arrayToMv` in the query as follows:

{% code overflow="wrap" %}
```sql
-- example 1: used in GROUP-BY
SELECT count(*), arrayToMv(RandomAirports) FROM airlineStats 
GROUP BY arrayToMv(RandomAirports)

-- example 2: used in PREDICATE
SELECT * FROM airlineStats WHERE arrayToMv(RandomAirports) IN ('SFO', 'JFK')

-- example 3: used in ORDER-BY
SELECT count(*), arrayToMV(RandomAirports) FROM airlineStats 
GROUP BY arrayToMV(RandomAirports)
ORDER BY arrayToMV(RandomAirports) DESC
```
{% endcode %}

### Schema and other prefixes are not supported

Schema and other prefixes are not supported in queries. For example, the following queries are _**not**_ supported:

```
SELECT* from default.myTable;
SELECT * from schemaName.myTable;
```

&#x20;Queries _**without prefixes are supported**_:&#x20;

```
SELECT * from myTable;
```

### Modifying query behavior based on the cluster config is not supported

Modifying query behavior based on the cluster configuration is not supported. 
`distinctcounthll`, `distinctcounthllmv`, `distinctcountrawhll`, and \```distinctcountrawhllmv` use`` a different 
default value of `log2mParam` in the multi-stage engine. 
In multi-stage, this value can no longer be configured. 
Therefore, the following query may produce different results in single-stage and multi-stage engine:

```sql
select distinctcounthll(col) from myTable
```

To ensure multi-stage returns the same result, specify the `log2mParam` value in your query:

```sql
select distinctcounthll(col, 8) from myTable
```

### Ambiguous reference to a projected column in statement clauses

If a column is repeated more than once in SELECT statement, that column requires disambiguate aliasing. For example, in the following query, the reference to `colA` is ambiguous whether it's to the first or second projected `colA`:

```sql
SELECT colA, colA, COUNT(*)
FROM myTable GROUP BY colA ORDER BY colA
```

The solution is to rewrite the query either use aliasing:

```sql
SELECT colA AS tmpA, colA as tmpB, COUNT(*) 
FROM myTable GROUP BY tmpA, tmpB ORDER BY tmpA
```

Or use index-based referencing:

```sql
SELECT colA, colA, COUNT(*) 
FROM myTable GROUP BY 1, 2 ORDER BY 1
```

### Tightened restriction on function naming

Pinot single-stage query engine automatically removes the underscore `_ character from function names. So co_u_n_t()`is equivalent to `count().`

In multi-stage, function naming restrictions were tightened, so the underscore(`_)` character is only allowed to separate word boundaries in a function name. Also camel case is supported in function names. For example, the following function names are allowed:

```markup
is_distinct_from(...)
isDistinctFrom(...)
```

### Tightened restriction on function signature and type matching

Pinot single-stage query engine automatically do implicit type casts in many of the situations, for example when running  the following:&#x20;

```
timestampCol >= longCol
```

it will automatically convert both values to long datatypes before comparison. 
This behavior however could cause issues and thus it is not so widely applied in the multi-stage engine where a 
stricter datatype conformance is enforced. the example above should be explicitly written as:

```
CAST(timestampCol AS BITINT) >= longCol 
```

### Default names for projections with function calls

Default names for projections with function calls are different between single and multi-stage.

* For example, in multi-stage, the following query:

```sql
  SELECT count(*) from mytable 
```

&#x20;      Returns the following result:

```
    "columnNames": [
        "EXPR$0"
      ],
```

* In single-stage, the following function:

```sql
  SELECT count(*) from mytable
```

&#x20;       Returns the following result:

```
      "columnNames": [
        "count(*)"
      ],
```

### Table names and column names are case sensitive

In multi-stage, table and column names and are case sensitive. In single-stage they were not. 
For example, the following two queries are not equivalent in multi-stage engine:

`select * from myTable`

`select * from mytable`

{% hint style="info" %}
**Note:** Function names are not case sensitive in neither single nor multi-stage.
{% endhint %}

### Arbitrary number of arguments isn't supported

An arbitrary number of arguments is no longer supported in multi-stage. 
For example, in single-stage, the following query worked:

<pre><code><a data-footnote-ref href="#user-content-fn-1">select add(1,2,3,4,5) from table</a>
</code></pre>

In multi-stage, this query must be rewritten as follows:

```
select add(1, add(2,add(3, add(4,5)))) from table
```

{% hint style="info" %}
**Note:** Remember that `select 1 + 2 + 3 + 4 + 5 from table` is still valid in multi-stage
{% endhint %}


### NULL function support

Null handling is not supported when tables use table based null storing. 
You have to use column base null storing instead.
See [null handling support](null-value-support.md)

### Custom transform function support

In multi-stage:

* The `histogram` function is not supported.
* The `timeConvert` function is not supported, see `dateTimeConvert` for more details.
* The `dateTimeConvertWindowHop` function is not supported.
* Array & Map-related functions are not supported.

### Custom aggregate function support

* aggregate function that requires literal input (such as `percentile`, `firstWithTime`) might result in a non-compilable query plan.

### Different type names

The multi-stage engine uses different type names than the single-stage engine.
Although the classical names must still be used in schemas and some SQL expressions, the new names must be used in
CAST expressions.

The following table shows the differences in type names:

| Single-stage engine | Multi-stage engine |
|---------------------|--------------------|
| NULL                | NULL               |
| BOOLEAN             | BOOLEAN            |
| INT                 | INT                |
| LONG                | BIGINT             |
| BIG_DECIMAL         | DECIMAL            |
| FLOAT               | FLOAT/REAL         |
| DOUBLE              | DOUBLE             |
| INTERVAL            | INTERVAL           |
| TIMESTAMP           | TIMESTAMP          |
| STRING              | VARCHAR            |
| BYTES               | VARBINARY          |
| -                   | ARRAY              |
| JSON                | -                  |

### Varbinary literals

VARBINARY literals in multi-stage engine must be prefixed with `X` or `x`. For example, the following query:

```sql
SELECT col1, col2 FROM myTable where bytesCol = X'4a220e6096b25eadb88358cb44068a3248254675'
```

In single-stage engine the same query would be:

```sql
-- not supported in multi-stage
SELECT col1, col2 FROM myTable where bytesCol = '4a220e6096b25eadb88358cb44068a3248254675'
```

## Troubleshoot errors

Troubleshoot semantic/runtime errors and timeout errors.

### Semantic/runtime errors

* Try downloading the latest docker image or building from the latest master commit.
  * We continuously push bug fixes for the multi-stage engine so bugs you encountered might have already been fixed in the latest master build.
* Try rewriting your query.
  * Some functions previously supported in the single-stage query engine (v1) may have a new way to express in the multi-stage engine (v2). Check and see if you are using any non-standard SQL functions or semantics.

### Timeout errors

* Try reducing the size of the table(s) used.&#x20;
  * Add higher selectivity filters to the tables.
* Try executing part of the subquery or a simplified version of the query first.
  * This helps to determine the selectivity and scale of the query being executed.
* Try adding more servers.
  * The new multi-stage engine runs distributed across the entire cluster, so adding more servers to partitioned queries such as GROUP BY aggregates, and equality JOINs help speed up the query runtime.



###

[^1]: 
