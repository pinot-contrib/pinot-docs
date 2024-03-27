# Null value support

{% hint style="danger" %}
**Multi-stage engine warning**

This document begins with null handling for the [single-stage query engine](../../reference/single-stage-engine.md). For the [multi-stage query engine](../../reference/multi-stage-engine.md) (v2), see the [Enable basic null support for the multi-stage query engine](#enable-basic-null-support-for-the-multi) section.
{% endhint %}

Null handling is defined in two different parts: at ingestion and at query time.
* [Basic null handling support](#basic-null-handling-support) means that you have enabled null handling at ingestion.
* [Advanced null support](#advanced-null-handling-support) means that you have also enabled null handling at query time.

## Basic null handling support

By default, null handling is disabled (`nullHandlingEnabled=false`) in the Table index configuration ([tableIndexConfig](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1)). When null support is disabled, `IS NOT NULL` evaluates to `true,` and `IS NULL` evaluates to `false`. For example, the predicate in the query below matches all records.

For example, the predicate in the query below matches all records.
<pre class="language-sql"><code class="lang-sql"><strong>select count(*) from my_table where column IS NOT NULL
</strong></code></pre>

### Enable basic null support for the single-stage query engine

The following table summarizes the behavior of null handling support in Pinot:

|                          | disabled (default) | basic (enabled at ingestion time) | advanced (enabled at query time) |
|--------------------------|--------------------|-----------------------------------|----------------------------------|
| IS NULL                  | always false       | depends on data                   | depends on data                  |
| IS NOT NULL              | always true        | depends on data                   | depends on data                  |
| Transformation functions | use default value  | use default value                 | null aware                       |
| Null aware aggregations  | use default value  | use default value                 | null aware                       |

## Default behavior

Pinot always stores column values in a [forward index](../../basics/indexing/forward-index.md).
Forward index never stores null values but have to store a value for each row.
Therefore independent of the null handling configuration, Pinot always stores a default value for nulls rows in the forward index.
The default value used in a column can be specified in the [schema](../../configuration-reference/schema.md) 
configuration by setting the `defaultNullValue` field spec. The `defaultNullValue` depends on the type of data.

{% hint style="info" %}
Remember that in the JSON used as table configuration, `defaultNullValue` must always be a String.
If the column type is not String, Pinot will convert that value to the column type automatically.
{% endhint %}

### Enable basic null support for the multi-stage query engine

To enable basic null support (`IS NULL` and `IS NOT NULL`) and generate the null index, in the Table index configuration ([tableIndexConfig](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1)), set `enableColumnBasedNullHandling=true`.

*If you are converting from null support for the single-stage query engine*, you can simplify your model by removing `nullHandlingEnabled` at the same time you set `enableColumnBasedNullHandling`. Also, when converting:
- No reingestion is needed.
- If the columns are changed from nullable to not nullable and there is a value that was previously null, the default value will be used instead.

Optional: Add `notNull: true` on the columns you want to consider not nullable.

When null support is enabled, `IS NOT NULL` and `IS NULL` evaluate to `true` or `false` according to whether a null is detected.

{% hint style="info" %}
**Important**

You MUST `SET enableColumnBasedNullHandling=true;` before you query. Just having `"nullHandlingEnabled: true,"` set in your table config does not automatically provide `enableColumnBasedNullHandling=true` when you execute a query. Basic null handling supports `IS NOT NULL` and `IS NULL` predicates. Advanced null handling adds SQL compatibility.
{% endhint %}


### Example workarounds to handle null values

To support null handling, Pinot must store null values in segments. The forward index stores the default value for null rows whether null storing is enabled or _not_.
When null storing is enabled, Pinot creates a new index called the _null index_ or _null vector index_.
This index stores the document IDs of the rows that have null values for the column.

{% hint style="danger" %}
Although null storing can be enabled after data has been ingested, data ingested before this mode is enabled
will not store the null index and therefore it will be treated as not null.
{% endhint %}

Null support is configured per table. You can configure one table to store nulls, and configure another table to not store nulls.
There are two ways to define null storing support in Pinot:

1. [Column based null handling](#column-based-null-handling), where each column in a table is configured as nullable or not nullable. 
We recommend enabling null storing support by column. This is the only way to support null handling in the 
[multi-stage query engine](../../reference/multi-stage-engine.md).
2. [Table based null handling](#table-based-null-handling), where all columns in the table are considered nullable.
This is how null values were handled before Pinot 1.1.0 and now deprecated.

### Column based null storing

We recommend configuring column based null storing, which lets you specify null handling per column and supports null handling in the multi-stage query engine.

To enable column based null handling:
1. Set [enableColumnBasedNullHandling](../../configuration-reference/schema.md#Schema) to `true` in the schema configuration before ingesting data.
2. Then specify which columns are not nullable using the `notNull` field spec, which defaults to false.

```json
{
  "schemaName": "my_table",
  "enableColumnBasedNullHandling": true,
  "dimensionFieldSpecs": [
    {
      "name": "notNullColumn",
      "dataType": "STRING",
      "notNull": true
    },
    {
      "name": "explicitNullableColumn",
      "dataType": "STRING",
      "notNull": false
    },
    {
      "name": "implicitNullableColumn",
      "dataType": "STRING"
    }
  ]
}
```

### Table based null storing

This is the only way to enable null storing in Pinot before 1.1.0, but it is deprecated since then.
Table based null storing is more expensive in terms of disk space and query performance than column based null storing.
Also, it is not possible to support null handling in multi-stage query engine using table based null storing.

To enable table based null storing, enable the `nullHandlingEnabled` configuration in
[tableIndexConfig.nullHandlingEnabled](../../configuration-reference/table#table-index-config) before ingesting data.
All columns in the table are now nullable.

{% hint style="warning" %}
Remember `nullHandlingEnabled` table configuration enables table based null handling
while `enableNullHandling` is the query option that enables advanced null handling at query time.
See [advanced null handling support](#advanced-null-handling-support) for more information.
{% endhint %}

As an example:

```json
{
  "tableIndexConfig": {
    "nullHandlingEnabled": true
  }
}
```

## Null handling at query time

To enable basic null handling by at query time, enable Pinot to [store nulls at ingestion time](#store-nulls-at-ingestion-time).
Advanced null handling support can be optionally enabled.

{% hint style="warn" %}
The multi-stage query engine requires column based null storing. Tables with table based null storing are considered not nullable.
{% endhint %}

### Basic null support

The basic null support is automatically enabled when null values are stored on a segment
(see [storing nulls at ingestion time](#store-nulls-at-ingestion-time)).

In this mode, Pinot is able to handle simple predicates like `IS NULL` or `IS NOT NULL`.
Other transformation functions (like `CASE`, `COALESCE`, `+`, etc.) and aggregations functions (like `COUNT`, `SUM`, 
`AVG`, etc.) will use the default value specified in the schema for null values.

For example, in the following table:

| rowId | col1 |
|-------|------|
| 0     | null |
| 1     | 1    |
| 2     | 2    |
| 3     | 2    |
| 4     | null |

If the default value for `col1` is `1`, the following query:

```sql
select $docId as rowId, col1 from my_table where col1 IS NULL
```

Will return the following result:

| rowId | col1 |
|-------|------|
| 1     | 1    |
| 2     | 2    |
| 3     | 2    |

While
```sql
select $docId as rowId, col1 + 1 as result from my_table
```

While return the following:

| rowId | col1 |
|-------|------|
| 0     | 2    |
| 1     | 2    |
| 2     | 3    |
| 3     | 3    |
| 4     | 2    |

And queries like
```sql
select $docId as rowId, col1 from my_table where col1 = 1
```

Will return

| rowId | col1 |
|-------|------|
| 0     | null |
| 1     | 1    |
| 4     | null |

Also
```sql
select count(col1)  as count, mode(col1) as mode from my_table
```

| count | mode |
|-------|------|
| 5     | 1    |

Given that neither `count` or `mode` function will ignore `null` values as expected but read instead the default value
(in this case `1`) stored in the forward index.

## Advanced null handling support

Advanced null handling has two requirements:
1. Segments must store null values (see [storing nulls at ingestion time](#store-nulls-at-ingestion-time)).
2. The query must enable null handling by setting the `enableNullHandling` [query option](query-options.md#enable-null-handling) to `true`.

The later can be done in one of the following ways:
- Set `enableNullHandling=true` at the beginning of the query.
- If using JDBC, set the connection option `enableNullHandling=true` (either in the URL or as a property).

{% hint style="warn" %}
Even they have similar names, the `nullHandlingEnabled` table configuration and the `enableNullHandling` query option are different.
Remember `nullHandlingEnabled` table configuration modifies how segments are stored and `enableNullHandling` query option modifies how queries are executed.
{% endhint %}

When the `enableNullHandling` option is set to `true`, the Pinot query engine uses a different execution path that interprets nulls in a standard SQL way.
This means that `IS NULL` and `IS NOT NULL` predicates will evaluate to `true` or `false` according to whether a null 
is detected (like in basic null support mode) but also aggregation functions like `COUNT`, `SUM`, `AVG`, `MODE`, etc. 
will deal with null values as expected (usually ignoring null values).

In this mode, some indexes may not be usable, and queries may be significantly more expensive.
Performance degradation impacts all the columns in the table, including columns in the query that do not contain null values.
This degradation happens even when table uses column base null storing.

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

## Appendix: Workarounds to handle null values without storing nulls

If you're not able to generate the null index for your use case, you may filter for null values using a default value
specified in your schema or a specific value included in your query.

{% hint style="info" %}
The following example queries work when the null value is not used in a dataset.
Unexpected values may be returned if the specified null value is a valid value in the dataset.
{% endhint %}

#### Filter for default null value(s) specified  in your schema

1. Specify a _default null value_ (`defaultNullValue`) in your [schema](https://docs.pinot.apache.org/basics/components/table/schema) for dimension fields, (`dimensionFieldSpecs`), metric fields (`metricFieldSpecs)`, and date time fields (`dateTimeFieldSpecs`).
2. Ingest the data.
3. To filter out the specified _default null value_, for example, you could write a query like the following:

```sql
    select count(*) from my_table where column <> 'default_null_value'
```

#### Filter for a specific value in your query

Filter for a specific value in your query that will not be included in the dataset.
For example, to calculate the average age, use `-1` to indicate the value of `Age` is `null`.

* Rewrite the following query:

```sql
    select avg(Age) from my_table
```

* To cover null values as follows:

```sql
    select avg(Age) from my_table WHERE Age <> -1
```


