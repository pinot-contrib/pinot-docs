# Access Control

Access control can be set up at various points in Pinot, such as controller endpoints and broker query endpoints. By default we will use [AllowAllAccessFactory](https://github.com/apache/pinot/blob/master/pinot-controller/src/main/java/org/apache/pinot/controller/api/access/AllowAllAccessFactory.java) and hence not be enforcing any access controls. You can add access control by implementing the [AccessControlFactory](https://github.com/apache/pinot/blob/master/pinot-controller/src/main/java/org/apache/pinot/controller/api/access/AccessControlFactory.java) interface.

The access control factory can be configured in the controller configs by setting the fully qualified class name of the AccessControlFactory in the property `controller.admin.access.control.factory.class`

The access control factory can be configured in the broker configs by setting the fully qualified class name of the AccessControlFactory in the property `pinot.broker.access.control.class`. Any other properties required for initializing the factory can be set in the broker configs as properties with the prefix `pinot.broker.access.control`.

## Row-Level Security (RLS)

{% hint style="info" %}
Row-Level Security is available starting in Apache Pinot 1.4.0.
{% endhint %}

Row-Level Security (RLS) enables fine-grained access control at the row level, so that different users or service accounts see only the rows they are authorized to view. This is particularly useful in multi-tenant environments where a single table contains data belonging to multiple organizations, departments, or users.

With RLS enabled, the broker automatically rewrites each incoming query to inject additional WHERE-clause predicates based on the authenticated principal. The rewriting is transparent to the caller -- the original SQL is submitted as usual, and the broker appends the configured filters before execution.

### How RLS works

1. A user submits a SQL query to the broker.
2. The broker authenticates the request and resolves the user principal.
3. The broker calls `getRowColFilters()` on the configured `AccessControl` implementation to retrieve any RLS filters associated with the principal and the target table.
4. If RLS filters exist, the `RlsFiltersRewriter` injects them into the query's WHERE clause using AND logic.
5. The rewritten query is executed by the single-stage or multi-stage query engine.

If no RLS filters are configured for a given principal and table, the query is executed without modification.

### Configuring RLS with Basic Auth

RLS filters are configured as part of the broker's Basic Auth principal definition. Each filter is a SQL predicate expression tied to a specific table.

```properties
# Define principals
pinot.broker.access.control.principals=admin,alice,bob

# Admin has full access, no RLS filters
pinot.broker.access.control.principals.admin.password=verysecret

# Alice can only access the sales_table and user_table
pinot.broker.access.control.principals.alice.password=alice123
pinot.broker.access.control.principals.alice.tables=sales_table,user_table
pinot.broker.access.control.principals.alice.sales_table.rls=department='marketing'
pinot.broker.access.control.principals.alice.user_table.rls=user_id='alice'

# Bob can access sales_table but only for a different department
pinot.broker.access.control.principals.bob.password=bob456
pinot.broker.access.control.principals.bob.tables=sales_table
pinot.broker.access.control.principals.bob.sales_table.rls=department='engineering'
```

The configuration key format is:

```
pinot.broker.access.control.principals.<user>.<tableName>.rls=<filter_predicate>
```

The value is parsed as a comma-separated list of filter predicates for that table. Pinot trims each predicate and combines them with `AND`.

### Query rewriting example

Given the configuration above, when Alice runs:

```sql
SELECT * FROM sales_table WHERE region = 'US'
```

The broker rewrites the query to:

```sql
SELECT * FROM sales_table WHERE region = 'US' AND department = 'marketing'
```

The additional filter is combined with the original WHERE clause using AND. If multiple RLS filters are configured for the same table, they are all combined using AND logic.

### Cross-table functions are rejected under row filters

RLS filters are applied only to the WHERE clause of the queried table, so functions that read rows from somewhere other than the FROM clause bypass them. To prevent a principal with row filters from reading or enumerating hidden rows through such a function, the single-stage broker rejects a query that calls any of the following functions when row filters apply to the queried table:

* `lookup()`
* `IN_SUBQUERY`
* `IN_PARTITIONED_SUBQUERY`

The query is rejected with `403 Permission denied` before any filters are added and before anything reaches a server, with a message of the form:

```
Cross-table functions are not allowed on table <table> when row-level security filters apply
```

Principals without row filters are unaffected and can continue to use these functions.

{% hint style="info" %}
This applies to the single-stage query engine. The multi-stage query engine applies row filters per table on the server and does not resolve `lookup()` or `IN_PARTITIONED_SUBQUERY`, so these functions are not available there under RLS.
{% endhint %}

### Custom access control implementations

If you use a custom `AccessControlFactory`, you can support RLS by implementing the `getRowColFilters()` method on your `AccessControl` class. This method receives the `RequesterIdentity` and table name, and returns a `TableRowColAccessResult` containing the RLS filter predicates to apply.

### Performance considerations

RLS filters are applied as additional WHERE-clause predicates. For best performance:

* Ensure that columns referenced in RLS filters have appropriate indexes (inverted index, range index, or sorted index) to avoid full table scans. The server evaluates the RLS filter first, per segment, so that user expressions never run on hidden rows; without an index on the RLS columns this materializes a bitmap over the whole segment.
* Keep filter predicates simple. Complex expressions or functions in RLS filters add overhead to every query for that principal.
* Test the rewritten queries using the query explain plan to verify that indexes are being utilized.

The time spent materializing the RLS bitmap is tracked by the `RLS_FILTER_TIME_MS` server timer and reported as `rlsFilterTimeMs` in the server query log.

### Debugging RLS

When RLS filters are applied to a query, the broker response includes a `rlsFiltersApplied` field set to `true`. This field appears in the standard broker query response JSON alongside other metadata fields like `numDocsScanned` and `timeUsedMs`. When no RLS filters are in effect, the field is set to `false`.

You can use this field to verify that RLS policies are being applied as expected. For more details on the broker response format, see [Query Response Format](../reference/api-reference/query-response-format.md).

### Response statistics under RLS

To avoid revealing the layout of the full table to a principal who can only see a subset of its rows, a query with row-level security omits the table-layout statistics from its response. The following fields are reported as `0`:

* `totalDocs`
* `numSegmentsQueried`, `numSegmentsProcessed`, `numSegmentsMatched`
* `numConsumingSegmentsQueried`, `numConsumingSegmentsProcessed`, `numConsumingSegmentsMatched`
* `numSegmentsPrunedByBroker`, `numSegmentsPrunedByServer`, `numSegmentsPrunedInvalid`, `numSegmentsPrunedByLimit`, `numSegmentsPrunedByValue`

{% hint style="warning" %}
Dashboards or tooling that read these fields for principals subject to RLS should expect them to be `0`. The server query log still records the real values.
{% endhint %}

If the broker cannot apply a configured RLS filter (for example, the filter predicate fails to parse), the query now fails with a `QUERY_VALIDATION` error instead of running without the filter. The error message does not include the policy text.

A query with row-level security does not use the single-stage broker's materialized-view rewrite.

### Performance considerations
