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
pinot.broker.access.control.principals.alice.rls.sales_table=department='marketing'
pinot.broker.access.control.principals.alice.rls.user_table=user_id='alice'

# Bob can access sales_table but only for a different department
pinot.broker.access.control.principals.bob.password=bob456
pinot.broker.access.control.principals.bob.tables=sales_table
pinot.broker.access.control.principals.bob.rls.sales_table=department='engineering'
```

The configuration key format is:

```
pinot.broker.access.control.principals.<user>.rls.<tableName>=<filter_predicate>
```

Where `<filter_predicate>` is any valid SQL predicate expression such as `department='marketing'` or `region IN ('US', 'EU')`.

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

### Custom access control implementations

If you use a custom `AccessControlFactory`, you can support RLS by implementing the `getRowColFilters()` method on your `AccessControl` class. This method receives the `RequesterIdentity` and table name, and returns a `TableRowColAuthResult` containing the RLS filter predicates to apply.

### Performance considerations

RLS filters are applied as additional WHERE-clause predicates. For best performance:

* Ensure that columns referenced in RLS filters have appropriate indexes (inverted index, range index, or sorted index) to avoid full table scans.
* Keep filter predicates simple. Complex expressions or functions in RLS filters add overhead to every query for that principal.
* Test the rewritten queries using the query explain plan to verify that indexes are being utilized.

### Debugging RLS

When RLS filters are applied to a query, the broker response includes a `rlsFiltersApplied` field set to `true`. This field appears in the standard broker query response JSON alongside other metadata fields like `numDocsScanned` and `timeUsedMs`. When no RLS filters are in effect, the field is set to `false`.

You can use this field to verify that RLS policies are being applied as expected. For more details on the broker response format, see [Query Response Format](../../reference/api-reference/query-response-format.md).
