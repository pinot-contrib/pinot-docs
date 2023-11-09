# Null Value Support

{% hint style="danger" %}
Multi-stage engine warning

Document below describes the null handling in the single-stage environment. At this time, **multi-stage environment does not support null handling**. Queries involving null in multi-stage environment may return unexpected results.
{% endhint %}

### Previous null support

Null handling support provided by Pinot by default is very basic. In fact by default Pinot does not store null values. Instead, they are transformed into a default value that can be specified in the [schema](../../configuration-reference/schema.md).

This means the predicate in the queries like below matches all the records always.

<pre class="language-sql"><code class="lang-sql"><strong>select count(*) from my_table where column IS NOT NULL
</strong></code></pre>

In order to filter out so called null value, user needs to write a query like:

```sql
select count(*) from my_table where column <> 'default_null_value'
```

This is a workaround, and it works well when the default null value is not used in your data set, e.g. use `-1` to indicate the value of `Age` is `null`.

However this could be error pruning when default null value is also a valid value in the dataset.

E.g. in order to calcaute the average age, instead of writing:

```sql
select avg(Age) from my_table
```

You need to write:

```sql
select avg(Age) from my_table WHERE Age <> -1
```

{% hint style="warning" %}
If null handling semantics are important in your use case, meanwhile you also are also looking for ultimate query latency, it is strongly recommended to follow the suggestions explained above.
{% endhint %}

### Advanced null handling support

Pinot provides an advanced null handling support that is closer to standard SQL null handling. This support is **not active** by default given it carries a notable performance impact even if query does not actually contain null values. The developer team is working on reducing this performance impact and it is planned to enable the advanced null handling support once its performance is good enough.

To turn `NULL` handling, users have to apply two changes (both are required):

1. Table config: Enable null handling at ingestion time by setting `nullHandlingEnabled` in [tableIndexConfig section](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1).
2. Query time: Enable null handling support at query time by setting `enableNullHandling` query option.

{% hint style="warning" %}
Remember that `nullHandlingEnabled` is the ingestion property while `enableNullHandling` is the query option
{% endhint %}

#### **Ingestion time**

In order to store the null values in the segment, users need to enable the `nullHandlingEnabled` in [tableIndexConfig section](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1) before ingesting the data.

During data ingestion (either real-time/offline) this property is checked. In case it is enabled, null values will be stored in the segment itself. Remember that data that was ingested when this property was disabled (the default value) does not store which values were null and therefore should be re-ingested.

This property affects all columns in the table. That means that a table in Pinot can define all or none columns as nullable.

{% hint style="info" %}
Column level null support is being actively developing right now
{% endhint %}

#### Query time

By default, Null usage in the predicate is enabled by default.

e.g.

<pre class="language-sql"><code class="lang-sql"><strong>select count(*) from my_table where column IS NOT NULL
</strong></code></pre>

For more usages like aggregation functions, users need to explicitly enable the support by setting the query option `enableNullHandling` to `true`.This option can be configured in different ways:

1. By adding `SET enableNullHandling=true` at the beginning of the query
2. If using JDBC, by setting the connection option `enableNullHandling=true` (either in the URL or as a property)

When this option is enabled, Pinot query engine will use a different execution path that needs to check null predicates. Sometimes this means that some indexes may not be usable, in which case the query is usually significantly more expensive. This is the main reason why null handling is not enabled by default. The developer team is working on optimizing these cases in order to provide a better user experience.

E.g. If the query includes a `IS NULL` or `IS NOT NULL` predicate as shown above, Pinot fetches the `NULL` value vector for the corresponding column within `FilterPlanNode` and retrieve the corresponding bitmap which represents all document IDs containing `NULL` values for that column. This bitmap is then used to create a `BitmapBasedFilterOperator` which does the actual filtering operation.

### Examples queries:

#### Select Query

![](https://lh7-us.googleusercontent.com/nXy6a9xdtVgM4aLpq2MX5NCZC\_IrGpK7bzYENcqpbUq2Of-KneuGL0z6Vvg\_U2RhkUrjsl8TsIuwm2GT90iFNaNFbaEd4Ga5oqWV5-8gvKEJ4P0V9mNTsmpt-TkOaAd35ayYR3uo07ijjS\_wm62SoDuf7Q=s2048)![](https://lh7-us.googleusercontent.com/Ba8gyIR9l8PytTCkIgcUlg6PrJazi6gFqKk5KfbrClVLS-lLySFwrMXZB073W3vb6wJoKvD9DvU7wf\_1Whj\_JPzfqfeKqcHyt7gxG-n71fYPaUucD1djRPkZTjYaWUr5sgDoHZSWNoosZZ-cv1D0doCb4Q=s2048)

Filter Query

![](https://lh7-us.googleusercontent.com/tW\_BWUTp8\_CvC-A0Ptd4rVXxfIY7QcgWD6IG2Tc3l7rUMvO1iYWZvSlh0mS-fEOK0aYBj1roD6\_4yuGDd2pdU6YTbGbcZMlsvS00drDh3WnNA3GRj\_DHlum55UtW23577QyoBJ80odjjMIbcOUyGBrOwoQ=s2048)![](https://lh7-us.googleusercontent.com/1V0fUS-Gvw18CBQrnlXXlRc9PPG3q-U\_87nRMjiiSJbB89fvpFJ7sSJA417XJtDO\_qOLVWrXZL\_UmzO0SypEZ1tIDIAw-gXVNCiVJj9lsGI5qnzT481Tg6XJrfd8M18x6Mk-UWyUExSRz1GSEuiJrLBEnw=s2048)

Aggregate Query

![](https://lh7-us.googleusercontent.com/-tCTwlmmcCWmkw\_9PUgEwczMEQIqAuG1oZXAcprxF\_lXEOU7tEh\_RLu0hL08Rbr5yccl-ncTfV0L3hPPy4eRMR-a7XTGLkv-Tl7ttnihYBc6AqvdocGExl8JpHeso5F\_dNq0EHlUaAtoVj9Bn3JJPKU2EQ=s2048)![](https://lh7-us.googleusercontent.com/cklgqy4Tdgubro6m2pnSSbih0QAhLMUDUGnb3SRCt7OswVOvjB\_7FNfn31kg23wUXuXNE5CbUZoHZYO6movrYFA6AOgukm\_nQiqXB\_eSvbpCUZYpGvbG8OjHHl-l8Nl7b\_vGnRMoPu9JAxzN3HE6pX2Cog=s2048)

Aggregate Filter Query

![](https://lh7-us.googleusercontent.com/dg408MRRnos1OU5dbc24YPeTwQafLqVmA7SCaZGzfN2ZTP7ghgjGzmQkz45gcSrUKl\_QUJwTadJJX5OR1gzauvsFPJKlq\_URCgQ8GUnKxjCQZkkVT9HhQGMTmU2-mjkdqQJarzDahWE4awPQyx0kJImHsg=s2048)![](https://lh7-us.googleusercontent.com/rLYW5d1iOE3-BtmoXsEPw5sa362aoI8cl4pnVXxp9KreScLoLYd6K6n0HqmlMOcCH5WdVxoPJXo9TNMIJ9xkTaxOQzhfmTBRmWXxeGOh1viH7nRx2OYiGKc51XdBVCG0dTJ700t4vqQ5oiaFwL5WmRhvzg=s2048)

Group By Query

![](https://lh7-us.googleusercontent.com/cAffjGlMh91qParql4VLO23-wKREfnfvihKNsJemO3Fh3GjQpb8q25XMKisATb6H\_Pd615XDkl6xT9sjqh45EXxv0kcs8oJxWtg\_ElyKJ86EDbunN36gkxqCDPFV3vkSlBQf7ibKZo2ndEqv3luG9VPxfQ=s2048)![](https://lh7-us.googleusercontent.com/aS5g\_lG\_vnjiqJ8z6sXEjPD95QW-YN4YVTeZxS2m\_ICzpESI9-7EotmGJvMNTgNyTGyVBk5XzOkd1ehrlKHFwQU0UHVzecU5TzSyYUFrDvaecPqclyO1ElPfinwGy-mCCI3yBS8J13xjbPvtQeRyJk-xpw=s2048)

Order By Query

![](https://lh7-us.googleusercontent.com/NlQwK1IxLuAlMHzqD9Kf-hXgcL9FNHPXIm1yP25VlReKRB1EmWs4aswp-H6FIp\_uO9Za86597F7UlENtDcSa3OkQm6-FbG3QcOj6U5CzTVJembd\_eS\_8Dx-fQ4CJfH2KMdJzRbCNJfFZZXKw89t4jlUYhQ=s2048)![](https://lh7-us.googleusercontent.com/e0E4JROmDeCO6e-EwCxPCo8AqNjlY6zF5Mk9tppx6KMWxr-CfHb6dL3yu1N0yM4LkqYu-ik0xtCVLiOgIGE9PwiN\_LUx1a3sqGrZGPvFO4Ul9HuedKvCXmwnSHYhzYt0AC-7asFYySwf2wEWyXJ5H--5mg=s2048)

Transform Query

![](https://lh7-us.googleusercontent.com/I\_By0UQTEWOY0Bs48QcGCP0cLn9OVQW9YdrSlJ3YtclYtaWgW76Gwko9Es351iKJMTcd2XzZEuUtY6pUIi7Zjf1\_dCBUUflVUV05xFuzHMVOMYLD3UF6U7xuZdAvhm5d0x3gRUwhJXI1Htrpq8zEmFFZug=s2048)![](https://lh7-us.googleusercontent.com/8v-QHctCuRsvLOtRfqMTlBt95dQvQprnLEIFykdMYsR\_YcdbVYgEzWiINeeJq5f5YzNo\_Lbar6AHR1mhW1pMLqvDm65eUJ3xjfgQKHQ1FdBAom2rPuCkSq4MMCX5xdUdU7wI4BP0\_0\_17bmqbmPDBPQ2PQ=s2048)





