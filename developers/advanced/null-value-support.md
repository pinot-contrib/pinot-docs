# Null value support

{% hint style="danger" %}
**Multi-stage engine warning**

This document describes null handling for the [single-stage query engine](../../reference/single-stage-engine.md). At this time, the [**multi-stage query engine**](../../reference/multi-stage-engine.md) **(v2) does not support null handling**. Queries involving null values in a multi-stage environment may return unexpected results.
{% endhint %}

## Basic null support

By default, null handling is disabled (`nullHandlingEnabled=false`) in the Table index configuration ([tableIndexConfig](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1)). When null support is disabled, `IS NOT NULL` evaluates to `true,` and `IS NULL` evaluates to `false`. For example, the predicate in the query below matches all records.

<pre class="language-sql"><code class="lang-sql"><strong>select count(*) from my_table where column IS NOT NULL
</strong></code></pre>

### Enable basic null support

To enable basic null support (`IS NULL` and `IS NOT NULL`) and generate the null index, in the Table index configuration ([tableIndexConfig](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1)), set **`nullHandlingEnabled=true`**.

When null support is enabled, `IS NOT NULL` and `IS NULL` evaluate to `true` or `false` according to whether a null is detected.

{% hint style="info" %}
**Important**

You MUST `SET enableNullHandling=true;` before you query. Just having `"nullHandlingEnabled: true,"` set in your table config does not automatically provide `enableNullHandling=true` when you execute a query. Basic null handling only supports `IS NOT NULL` and `IS NULL` predicates. Advanced null handling adds SQL compatiblilty.
{% endhint %}

### Example workarounds to handle null values

If you're not able to generate the null index for your use case, you may filter for null values using a default value specified in your schema or a specific value included in your query.

{% hint style="info" %}
The following example queries work when the null value is not used in a dataset. Errors may occur if the specified null value is a valid value in the dataset.
{% endhint %}

#### Filter for default null value(s) specified  in your schema

1. Specify a _default null value_ (`defaultNullValue`) in your [schema](https://docs.pinot.apache.org/basics/components/table/schema) for dimension fields, (`dimensionFieldSpecs`), metric fields (`metricFieldSpecs)`, and date time fields (`dateTimeFieldSpecs`).
2. To filter out the specified _default null value_, for example, you could write a query like the following:

```sql
    select count(*) from my_table where column <> 'default_null_value'
```

#### Filter for a specific value in your query

Filter for a specific value in your query that will not be included in the dataset. For example, to calculate the average age, use `-1` to indicate the value of `Age` is `null`.

* Rewrite the following query:

```sql
    select avg(Age) from my_table
```

* To cover null values as follows:

```sql
    select avg(Age) from my_table WHERE Age <> -1
```

## Advanced null handling support

**Under development to improve performance for advanced null handling.**&#x20;

Pinot provides advanced null handling support similar to standard SQL null handling. Because this feature carries a notable performance impact (even queries without null values), this feature **is not enabled** by default. For optimal query latency, we recommend [enabling basic null support](null-value-support.md#to-enable-basic-null-support).

### Enable advanced null handling

To enable `NULL` handling, do the following:

1. `To enable` null handling during ingestion, in [tableIndexConfig](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1), set**`nullHandlingEnabled=true`**.
2. To enable null handling for queries, set the**`enableNullHandling`** [query option](https://docs.pinot.apache.org/users/user-guide-query/query-options).

{% hint style="info" %}
**Important**

You MUST `SET enableNullHandling=true;` before you query. Just having `"nullHandlingEnabled: true,"` set in your table config does not automatically provide `enableNullHandling=true` when you execute a query. Basic null handling only supports `IS NOT NULL` and `IS NULL` predicates. Advanced null handling adds SQL compatiblilty.
{% endhint %}

#### **Ingestion time**

To store the null values in a segment, you must enable the `nullHandlingEnabled` in [tableIndexConfig section](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1) before ingesting the data.

During real-time or offline ingestion, Pinot checks to see if null handling is enabled, and stores null values in the segment itself. Data ingested when null handling is disabled does not store null values, and should be ingested again.

The `nullHandlingEnabled` configuration affects all columns in a Pinot table.

{% hint style="info" %}
Column-level null support is under development.
{% endhint %}

#### Query time

By default, null usage in the predicate is disabled.&#x20;

For handling nulls in aggregation functions, explicitly enable the null support by setting the query option `enableNullHandling` to `true`. Configure this option in one of the following ways:

1. `Set enableNullHandling=true` at the beginning of the query.
2. If using JDBC, set the connection option `enableNullHandling=true` (either in the URL or as a property).

When this option is enabled, the Pinot query engine uses a different execution path that checks null predicates. Therefore, some indexes may not be usable, and the query is significantly more expensive. This is the main reason why null handling is not enabled by default.&#x20;

If the query includes a `IS NULL` or `IS NOT NULL` predicate, Pinot fetches the `NULL` value vector for the corresponding column within `FilterPlanNode` and retrieves the corresponding bitmap that represents all document IDs containing `NULL` values for that column. This bitmap is then used to create a `BitmapBasedFilterOperator` to do the filtering operation.

### Examples queries

#### Select Query

![](https://lh7-us.googleusercontent.com/nXy6a9xdtVgM4aLpq2MX5NCZC\_IrGpK7bzYENcqpbUq2Of-KneuGL0z6Vvg\_U2RhkUrjsl8TsIuwm2GT90iFNaNFbaEd4Ga5oqWV5-8gvKEJ4P0V9mNTsmpt-TkOaAd35ayYR3uo07ijjS\_wm62SoDuf7Q=s2048)![](https://lh7-us.googleusercontent.com/Ba8gyIR9l8PytTCkIgcUlg6PrJazi6gFqKk5KfbrClVLS-lLySFwrMXZB073W3vb6wJoKvD9DvU7wf\_1Whj\_JPzfqfeKqcHyt7gxG-n71fYPaUucD1djRPkZTjYaWUr5sgDoHZSWNoosZZ-cv1D0doCb4Q=s2048)

#### Filter Query

![](https://lh7-us.googleusercontent.com/tW\_BWUTp8\_CvC-A0Ptd4rVXxfIY7QcgWD6IG2Tc3l7rUMvO1iYWZvSlh0mS-fEOK0aYBj1roD6\_4yuGDd2pdU6YTbGbcZMlsvS00drDh3WnNA3GRj\_DHlum55UtW23577QyoBJ80odjjMIbcOUyGBrOwoQ=s2048)![](https://lh7-us.googleusercontent.com/1V0fUS-Gvw18CBQrnlXXlRc9PPG3q-U\_87nRMjiiSJbB89fvpFJ7sSJA417XJtDO\_qOLVWrXZL\_UmzO0SypEZ1tIDIAw-gXVNCiVJj9lsGI5qnzT481Tg6XJrfd8M18x6Mk-UWyUExSRz1GSEuiJrLBEnw=s2048)

#### Aggregate Query

![](https://lh7-us.googleusercontent.com/-tCTwlmmcCWmkw\_9PUgEwczMEQIqAuG1oZXAcprxF\_lXEOU7tEh\_RLu0hL08Rbr5yccl-ncTfV0L3hPPy4eRMR-a7XTGLkv-Tl7ttnihYBc6AqvdocGExl8JpHeso5F\_dNq0EHlUaAtoVj9Bn3JJPKU2EQ=s2048)![](https://lh7-us.googleusercontent.com/cklgqy4Tdgubro6m2pnSSbih0QAhLMUDUGnb3SRCt7OswVOvjB\_7FNfn31kg23wUXuXNE5CbUZoHZYO6movrYFA6AOgukm\_nQiqXB\_eSvbpCUZYpGvbG8OjHHl-l8Nl7b\_vGnRMoPu9JAxzN3HE6pX2Cog=s2048)

#### Aggregate Filter Query

![](https://lh7-us.googleusercontent.com/dg408MRRnos1OU5dbc24YPeTwQafLqVmA7SCaZGzfN2ZTP7ghgjGzmQkz45gcSrUKl\_QUJwTadJJX5OR1gzauvsFPJKlq\_URCgQ8GUnKxjCQZkkVT9HhQGMTmU2-mjkdqQJarzDahWE4awPQyx0kJImHsg=s2048)![](https://lh7-us.googleusercontent.com/rLYW5d1iOE3-BtmoXsEPw5sa362aoI8cl4pnVXxp9KreScLoLYd6K6n0HqmlMOcCH5WdVxoPJXo9TNMIJ9xkTaxOQzhfmTBRmWXxeGOh1viH7nRx2OYiGKc51XdBVCG0dTJ700t4vqQ5oiaFwL5WmRhvzg=s2048)

#### Group By Query

![](https://lh7-us.googleusercontent.com/cAffjGlMh91qParql4VLO23-wKREfnfvihKNsJemO3Fh3GjQpb8q25XMKisATb6H\_Pd615XDkl6xT9sjqh45EXxv0kcs8oJxWtg\_ElyKJ86EDbunN36gkxqCDPFV3vkSlBQf7ibKZo2ndEqv3luG9VPxfQ=s2048)![](https://lh7-us.googleusercontent.com/aS5g\_lG\_vnjiqJ8z6sXEjPD95QW-YN4YVTeZxS2m\_ICzpESI9-7EotmGJvMNTgNyTGyVBk5XzOkd1ehrlKHFwQU0UHVzecU5TzSyYUFrDvaecPqclyO1ElPfinwGy-mCCI3yBS8J13xjbPvtQeRyJk-xpw=s2048)

#### Order By Query

![](https://lh7-us.googleusercontent.com/NlQwK1IxLuAlMHzqD9Kf-hXgcL9FNHPXIm1yP25VlReKRB1EmWs4aswp-H6FIp\_uO9Za86597F7UlENtDcSa3OkQm6-FbG3QcOj6U5CzTVJembd\_eS\_8Dx-fQ4CJfH2KMdJzRbCNJfFZZXKw89t4jlUYhQ=s2048)![](https://lh7-us.googleusercontent.com/e0E4JROmDeCO6e-EwCxPCo8AqNjlY6zF5Mk9tppx6KMWxr-CfHb6dL3yu1N0yM4LkqYu-ik0xtCVLiOgIGE9PwiN\_LUx1a3sqGrZGPvFO4Ul9HuedKvCXmwnSHYhzYt0AC-7asFYySwf2wEWyXJ5H--5mg=s2048)

#### Transform Query

![](https://lh7-us.googleusercontent.com/I\_By0UQTEWOY0Bs48QcGCP0cLn9OVQW9YdrSlJ3YtclYtaWgW76Gwko9Es351iKJMTcd2XzZEuUtY6pUIi7Zjf1\_dCBUUflVUV05xFuzHMVOMYLD3UF6U7xuZdAvhm5d0x3gRUwhJXI1Htrpq8zEmFFZug=s2048)![](https://lh7-us.googleusercontent.com/8v-QHctCuRsvLOtRfqMTlBt95dQvQprnLEIFykdMYsR\_YcdbVYgEzWiINeeJq5f5YzNo\_Lbar6AHR1mhW1pMLqvDm65eUJ3xjfgQKHQ1FdBAom2rPuCkSq4MMCX5xdUdU7wI4BP0\_0\_17bmqbmPDBPQ2PQ=s2048)





