# Null Value Support

{% hint style="danger" %}
Multi-stage engine warning

Document above describes the null handling in the single-stage environment. At this time, **multi-stage environment does not support null handling**. Queries involving null in multi-stage environment may return unexpected results.
{% endhint %}

### Basic null handling support

Null handling support provided by Pinot by default is very basic. In fact by default Pinot does not store null values. Instead, they are transformed into a default value that can be specified in the [schema](../../configuration-reference/schema.md).

This means that queries like:

```sql
select count(*) from my_table where column IS NOT NULL
```

Are translated to:

```sql
select count(*) from my_table where column = <default value>
```

This is a workaround that is error prone since oftentimes it's difficult to distinguish valid values from the default null values.

{% hint style="warning" %}
If null handling semantics are important in your use case, it is strongly recommended to apply changes explained above.
{% endhint %}

### Advanced null handling support

Pinot provides an advanced null handling support that is closer to standard SQL null handling. This support is **not active** by default given it carries a notable performance impact even if query does not actually contain null values. The developer team is working on reducing this performance impact and it is planned to enable the advanced null handling support once its performance is good enough.

To turn `NULL` handling, users have to apply two changes (both are required):

1. Enable null handling at ingestion time by setting `nullHandlingEnabled` in [tableIndexConfig section](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1).
2. Enable null handling support at query time by setting `enableNullHandling` query option.

{% hint style="warning" %}
Remember that `nullHandlingEnabled` is the ingestion property while `enableNullHandling` is the query option
{% endhint %}

#### **Ingestion time**

In order to store the null values in the segment, users need to enable the `nullHandlingEnabled` in [tableIndexConfig section](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1) before ingesting the data.

During data ingestion (either real-time/offline) this property is checked. In case it is enabled, null values will be stored in the segment itself. Remember that data that was ingested when this property was disabled (the default value) does not store which values were null and therefore should be re-ingested.

This property affects all columns in the table. That means that a table in Pinot can define all or none columns as nullable.

#### Query time

In order to enable null handling at query execution time the option `enableNullHandling` must be enabled. This option can be configured in different ways:

1. By adding `SET enableNullHandling` at the beginning of the query
2. By adding `OPTION(enableNullHandling=true)` at the end of the query.
3. If using JDBC, by setting the connection option `enableNullHandling=true` (either in the URL or as a property)

When this option is enabled, Pinot query engine will use a different execution path that needs to check null predicates. Sometimes this means that some indexes may not be usable, in which case the query is usually significantly more expensive. This is the main reason why null handling is not enabled by default. The developer team is working on optimizing these cases in order to provide a better user experience.
