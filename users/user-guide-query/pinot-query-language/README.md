---
description: Learn how to query Pinot using PQL
---

# Pinot Query Language \(PQL\)

## PQL

PQL is a derivative of SQL that supports selection, projection, aggregation, and grouping aggregation. 

## PQL Limitations

PQL is only a derivative of SQL, and it does not support Joins nor Subqueries. In order to support them, we suggest to rely on PrestoDB [https://prestodb.io/](https://prestodb.io/), although Subqueries are not completely supported by PrestoDB at the moment of writing.

## PQL Examples

The Pinot Query Language \(PQL\) is very similar to standard SQL:

```sql
SELECT COUNT(*) FROM myTable
```

### Aggregation

```sql
SELECT COUNT(*), MAX(foo), SUM(bar) FROM myTable
```

### Grouping on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM myTable
  GROUP BY bar, baz LIMIT 50
```

### Ordering on Aggregation

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM myTable
  GROUP BY bar, baz 
  ORDER BY bar, MAX(foo) DESC LIMIT 50
```

### Filtering

```sql
SELECT COUNT(*) FROM myTable
  WHERE foo = 'foo'
  AND bar BETWEEN 1 AND 20
  OR (baz < 42 AND quux IN ('hello', 'goodbye') AND quuux NOT IN (42, 69))
```

### Selection \(Projection\)

```sql
SELECT * FROM myTable
  WHERE quux < 5
  LIMIT 50
```

### Ordering on Selection

```sql
SELECT foo, bar FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 100
```

### Pagination on Selection

Note: results might not be consistent if column ordered by has same value in multiple rows.

```sql
SELECT foo, bar FROM myTable
  WHERE baz > 20
  ORDER BY bar DESC
  LIMIT 50, 100
```

### Wild-card match \(in WHERE clause only\)

To count rows where the column `airlineName` starts with `U`

```sql
SELECT count(*) FROM SomeTable
  WHERE regexp_like(airlineName, '^U.*')
  GROUP BY airlineName TOP 10
```

### UDF

As of now, functions have to be implemented within Pinot. Injecting functions is not allowed yet. The example below demonstrate the use of UDFs. More examples in [Transform Function in Aggregation Grouping](https://apache-pinot.gitbook.io/apache-pinot-cookbook/pinot-user-guide/pinot-query-language#transform-function-in-aggregation-and-grouping)

```sql
SELECT count(*) FROM myTable
  GROUP BY timeConvert(timeColumnName, 'SECONDS', 'DAYS')
```

### BYTES column

Pinot supports queries on BYTES column using HEX string. The query response also uses hex string to represent bytes value.

E.g. the query below fetches all the rows for a given UID.

```sql
SELECT * FROM myTable
  WHERE UID = "c8b3bce0b378fc5ce8067fc271a34892"
```

## PQL Specification

### SELECT

The select statement is as follows

```sql
SELECT <outputColumn> (, outputColumn, outputColumn,...)
  FROM <tableName>
  (WHERE ... | GROUP BY ... | ORDER BY ... | TOP ... | LIMIT ...)
```

`outputColumn` can be `*` to project all columns, columns \(`foo`, `bar`, `baz`\) or aggregation functions like \(`MIN(foo)`, `MAX(bar)`, `AVG(baz)`\).



### Filter Functions on Single Value/Multi-value 

* `EQUALS`
* `IN`
* `NOT IN`
* `GT`
* `LT`
* `BETWEEN`
* `REGEXP_LIKE`

For Multi-Valued columns, EQUALS is similar to CONTAINS. 

### Supported aggregations on single-value columns

* `COUNT`
* `MIN`
* `MAX`
* `SUM`
* `AVG`
* `MINMAXRANGE`
* `DISTINCT`
* `DISTINCTCOUNT`
* `DISTINCTCOUNTHLL`
* `DISTINCTCOUNTRAWHLL`: Returns HLL response serialized as string. The serialized HLL can be converted back into an HLL \(see pinot-core/\*\*/HllUtil.java as an example\) and then aggregated with other HLLs. A common use case may be to merge HLL responses from different Pinot tables, or to allow aggregation after client-side batching.
* `FASTHLL` \(**WARN**: will be deprecated soon. `FASTHLL` stores serialized HyperLogLog in String format, which performs worse than `DISTINCTCOUNTHLL`, which supports serialized HyperLogLog in BYTES \(byte array\) format\)
* `PERCENTILE[0-100]`: e.g. `PERCENTILE5`, `PERCENTILE50`, `PERCENTILE99`, etc.
* `PERCENTILEEST[0-100]`: e.g. `PERCENTILEEST5`, `PERCENTILEEST50`, `PERCENTILEEST99`, etc.

### Supported aggregations on multi-value columns

* `COUNTMV`
* `MINMV`
* `MAXMV`
* `SUMMV`
* `AVGMV`
* `MINMAXRANGEMV`
* `DISTINCTCOUNTMV`
* `DISTINCTCOUNTHLLMV`
* `DISTINCTCOUNTRAWHLLMV`: Returns HLL response serialized as string. The serialized HLL can be converted back into an HLL \(see pinot-core/\*\*/HllUtil.java as an example\) and then aggregated with other HLLs. A common use case may be to merge HLL responses from different Pinot tables, or to allow aggregation after client-side batching.
* `FASTHLLMV` \(**WARN**: will be deprecated soon. It does not make lots of sense to configure serialized HyperLogLog column as a dimension\)
* `PERCENTILE[0-100]MV`: e.g. `PERCENTILE5MV`, `PERCENTILE50MV`, `PERCENTILE99MV`, etc.
* `PERCENTILEEST[0-100]MV`: e.g. `PERCENTILEEST5MV`, `PERCENTILEEST50MV`, `PERCENTILEEST99MV`, etc.

### WHERE

Supported predicates are comparisons with a constant using the standard SQL operators \(`=`, `<`, `<=`, `>`, `>=`, `<>`, ‘!=’\) , range comparisons using `BETWEEN` \(`foo BETWEEN 42 AND 69`\), set membership \(`foo IN (1, 2, 4, 8)`\) and exclusion \(`foo NOT IN (1, 2, 4, 8)`\). For `BETWEEN`, the range is inclusive.

Comparison with a regular expression is supported using the regexp\_like function, as in `WHERE regexp_like(columnName, 'regular expression')`

### GROUP BY

The `GROUP BY` clause groups aggregation results by a list of columns, or transform functions on columns \(see below\)

### ORDER BY

The `ORDER BY` clause orders selection results or group by results by a list of columns. PQL supports ordering `DESC` or `ASC`.

### TOP

The `TOP n` clause causes the ‘n’ largest group results to be returned. If not specified, the top 10 groups are returned.

### LIMIT

The `LIMIT n` clause causes the selection results to contain at most ‘n’ results. The `LIMIT a, b` clause paginate the selection results from the ‘a’ th results and return at most ‘b’ results.

### Transform Function in Aggregation and Grouping

In aggregation and grouping, each column can be transformed from one or multiple columns. For example, the following query will calculate the maximum value of column `foo` divided by column `bar` grouping on the column `time` converted from time unit `MILLISECONDS` to `SECONDS`:

```sql
SELECT MAX(DIV(foo, bar) FROM myTable
  GROUP BY TIMECONVERT(time, 'MILLISECONDS', 'SECONDS')
```

#### Supported transform functions

<table>
  <thead>
    <tr>
      <th style="text-align:left"></th>
      <th style="text-align:left"></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">ADD</td>
      <td style="text-align:left">Sum of at least two values</td>
    </tr>
    <tr>
      <td style="text-align:left">SUB</td>
      <td style="text-align:left">Difference between two values</td>
    </tr>
    <tr>
      <td style="text-align:left">MULT</td>
      <td style="text-align:left">Product of at least two values</td>
    </tr>
    <tr>
      <td style="text-align:left">DIV</td>
      <td style="text-align:left">Quotient of two values</td>
    </tr>
    <tr>
      <td style="text-align:left">TIMECONVERT</td>
      <td style="text-align:left">
        <p>Takes 3 arguments, converts the value into another time unit.</p>
        <p><em><br /></em><b>Examples</b><em> <br /></em><code>TIMECONVERT(time, &apos;MILLISECONDS&apos;, &apos;SECONDS&apos;)</code> -
          This expression converts the value of column <code>time</code> (taken to
          be in milliseconds) to the nearest seconds (<em>i.e.</em> the nearest seconds
          that is lower than the value of <code>date</code> column)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">DATETIMECONVERT</td>
      <td style="text-align:left">
        <p>Takes 4 arguments, converts the value into another date time format, and
          buckets time based on the given time granularity.</p>
        <p><code>DATETIMECONVERT(columnName, inputFormat, outputFormat, outputGranularity)</code>where,
          <br
          /><code>columnName</code> - column name to convert
          <br /><code>inputFormat</code> - format of the column columnName
          <br /><code>outputFormat</code> - format of the result desired after conversion <code>outputGranularity</code> -
          the granularity in which to bucket the result</p>
        <p></p>
        <p>Format is expressed as <code>&lt;time size&gt;:&lt;time unit&gt;:&lt;time format&gt;:&lt;pattern&gt;</code>
          <br
          />where,</p>
        <p><code>time size</code> - size of the time unit eg: 1, 10</p>
        <p><code>time unit</code> - HOURS, DAYS etc</p>
        <p><code>time format</code> - EPOCH or SIMPLE_DATE_FORMAT</p>
        <p><code>pattern</code> - <b> </b>this is defined in case of SIMPLE_DATE_FORMAT.
          eg: yyyyMMdd. A specific timezone can be passed using tz(timezone).</p>
        <p><code>timezone</code> - can be expressed as long form tz(Asia/Kolkata),
          or short form tz(IST) or in terms of GMT tz(GMT+0530). Default is UTC.
          It is recommended to use long form timezone, as short forms are ambiguous
          with daylight savings (eg: PDT works during daylight savings, PST otherwise)</p>
        <p></p>
        <p>Granularity is expressed as <code>&lt;time size&gt;:&lt;time unit&gt;</code>
        </p>
        <p></p>
        <p><b>Examples</b>
        </p>
        <p>1) To convert column &quot;Date&quot; from hoursSinceEpoch to daysSinceEpoch
          and bucket it to 1 day granularity
          <br /><code>dateTimeConvert(Date, &apos;1:HOURS:EPOCH&apos;, &apos;1:DAYS:EPOCH&apos;, &apos;1:DAYS&apos;)</code>
        </p>
        <p>2) To simply bucket millis &quot;Date&quot; to 15 minutes granularity
          <br
          /><code>dateTimeConvert(Date, &apos;1:MILLISECONDS:EPOCH&apos;, &apos;1:MILLISECONDS:EPOCH&apos;, &apos;15:MINUTES&apos;)</code>
        </p>
        <p>3) To convert column &quot;Date&quot; from hoursSinceEpoch to format yyyyMdd
          and bucket it to 1 days granularity
          <br /><code>dateTimeConvert(Date, &apos;1:HOURS:EPOCH&apos;, &apos;1:DAYS:SIMPLE_DATE_FORMAT:yyyyMMdd&apos;, &apos;1:DAYS&apos;)</code>
        </p>
        <p>4) To convert column &quot;Date&quot; from format yyyy/MM/dd to weeksSinceEpoch
          and bucket it to 1 weeks granularity
          <br /><code>dateTimeConvert(Date, &apos;1:DAYS:SIMPLE_DATE_FORMAT:yyyy/MM/dd&apos;, &apos;1:WEEKS:EPOCH&apos;, &apos;1:WEEKS&apos;)</code>
        </p>
        <p>5) To convert column &quot;Date&quot; from millis to format yyyyMdd in
          timezone PST
          <br /><code>dateTimeConvert(Date, &apos;1:MILLISECONDS:EPOCH&apos;, &apos;1:DAYS:SIMPLE_DATE_FORMAT:yyyyMMdd tz(America/Los_Angeles)&apos;, &apos;1:DAYS&apos;)</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">DATETRUNC</td>
      <td style="text-align:left">
        <p>(Presto) SQL compatible date truncation, equivalent to the Presto function
          <a
          href="https://mode.com/blog/date-trunc-sql-timestamp-function-count-on">date_trunc</a>. Takes at least 3 and upto 5 arguments, converts the value
            into a specified output granularity seconds since UTC epoch that is bucketed
            on a unit in a specified timezone.
            <br />
            <br /><b>Examples</b>
            <br /><code>DATETRUNC(&apos;week&apos;, time_in_seconds, &apos;SECONDS&apos;)</code> This
            expression converts the column <code>time_in_seconds</code>, which is a
            long containing seconds since UTC epoch truncated at <code>WEEK</code> (where
            a Week starts at Monday UTC midnight). The output is a long seconds since
            UTC epoch.
            <br />
        </p>
        <p><code>DATETRUNC(&apos;quarter&apos;, DIV(time_milliseconds/1000), &apos;SECONDS&apos;, &apos;America/Los_Angeles&apos;, &apos;HOURS&apos;)</code> This
          expression converts the expression <code>time_in_milliseconds/1000</code> (which
          is thus in seconds) into hours that are truncated at <code>QUARTER</code> at
          the Los Angeles time zone (where a Quarter begins on 1/1, 4/1, 7/1, 10/1
          in Los Angeles timezone). The output is expressed as hours since UTC epoch
          (note that the output is not Los Angeles timezone)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">VALUEIN</td>
      <td style="text-align:left">Takes at least 2 arguments, where the first argument is a multi-valued
        column, and the following arguments are constant values. The transform
        function will filter the value from the multi-valued column with the given
        constant values. The <code>VALUEIN</code> transform function is especially
        useful when the same multi-valued column is both filtering column and grouping
        column.
        <br />
        <br /><b>Examples</b>
        <br /><code>VALUEIN(mvColumn, 3, 5, 15)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">JSONEXTRACTSCALAR</td>
      <td style="text-align:left">
        <p><b><code>JSONEXTRACTSCALAR(jsonField, &apos;jsonPath&apos;, &apos;resultsType&apos;)</code></b>evaluates
          the <code>jsonPath</code> on <code>jsonField</code> (a string containing JSON)
          and returns the result as a type <code>resultsType</code>
        </p>
        <p><code>jsonFieldName</code> is a String field with Json document.</p>
        <p><code>jsonPath</code> is a <a href="https://goessner.net/articles/JsonPath/">JsonPath expression</a> to
          read from JSON document</p>
        <p><code>results_type</code> refers to the results data type, could be <code>INT</code>, <code>LONG</code>, <code>FLOAT</code>, <code>DOUBLE</code>, <code>STRING</code>, <code>INT_ARRAY</code>, <code>LONG_ARRAY</code>, <code>FLOAT_ARRAY</code>, <code>DOUBLE_ARRAY</code>, <code>STRING_ARRAY</code>.</p>
        <p><b>Examples</b>
        </p>
        <p><code>JSONEXTRACTSCALAR(profile_json_str, &apos;$.name&apos;, &apos;STRING&apos;) -&gt; &quot;bob&quot;</code>
        </p>
        <p><code>JSONEXTRACTSCALAR(profile_json_str, &apos;$.age&apos;, &apos;INT&apos;) -&gt; 37</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">JSONEXTRACTKEY</td>
      <td style="text-align:left">
        <p><b><code>JSONEXTRACTKEY(jsonField, &apos;jsonPath&apos;)</code></b> extracts
          all field names based on <code>jsonPath</code> as a <code>STRING_ARRAY.</code>
        </p>
        <p><code>jsonFieldName</code> is a String field with Json document.</p>
        <p><code>jsonPath</code> is a <a href="https://goessner.net/articles/JsonPath/">JsonPath expression</a> to
          read from JSON document</p>
        <p><b>Examples</b>
        </p>
        <p><code>JSONEXTRACTSCALAR(profile_json_str, &apos;$.*&apos;) -&gt; [&quot;name&quot;, &quot;age&quot;, &quot;phone&quot;...]</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>## Differences with SQL

{% hint style="info" %}
These differences only apply to the PQL endpoint. They do not hold true for the standard-SQL endpoint, which is the recommended endpoint. More information about the two types of endpoints in [Querying Pinot](../../api/querying-pinot-using-standard-sql/#rest-api-on-the-broker)
{% endhint %}

* `TOP` works like `LIMIT` for truncation in group by queries
* No need to select the columns to group with. The following two queries are both supported in PQL, where the non-aggregation columns are ignored.

```sql
SELECT MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM mytable
  GROUP BY bar, baz
  TOP 50

SELECT bar, baz, MIN(foo), MAX(foo), SUM(foo), AVG(foo) FROM mytable
  GROUP BY bar, baz
  TOP 50
```

* The results will always order by the aggregated value \(descending\). The results for query

```sql
SELECT MIN(foo), MAX(foo) FROM myTable
  GROUP BY bar
  TOP 50
```

will be the same as the combining results from the following queries

```sql
SELECT MIN(foo) FROM myTable
  GROUP BY bar
  TOP 50
SELECT MAX(foo) FROM myTable
  GROUP BY bar
  TOP 50
```

where we don’t put the results for the same group together.

* No support for ORDER BY in aggregation group by. However, ORDER BY support was added recently and is available in the standard-SQL endpoint. It can be used in the PQL endpoint by passing `queryOptions` into the payload as follows

```javascript
{
  "pql" : "SELECT SUM(foo), SUM(bar) from myTable GROUP BY moo ORDER BY SUM(bar) ASC, moo DESC TOP 10",
  "queryOptions" : "groupByMode=sql;responseFormat=sql"
}
```

where,

* `groupByMode=sql` - standard sql way of execution group by, hence accepting order by
* `responseFormat=sql` - standard sql way of displaying results, in a tabular manner

