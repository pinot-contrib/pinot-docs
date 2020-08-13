# Schema

Schema is used to define the names, data types and other information for the columns of a Pinot table.

## Types of columns

Columns in a Pinot table can be broadly categorized into three categories

<table>
  <thead>
    <tr>
      <th style="text-align:left">Column Category</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><b>Dimension</b>
      </td>
      <td style="text-align:left">
        <p>Dimension columns are typically used in slice and dice operations for
          answering business queries. Frequent operations done on dimension columns:</p>
        <ul>
          <li>GROUP BY - group by one or more dimension columns along with aggregations
            on one or more metric columns</li>
          <li>Filter processing</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>Metric</b>
      </td>
      <td style="text-align:left">
        <p>These columns represent quantitative data of the table. Such columns are
          frequently used in aggregation operations. In data warehouse terminology,
          these are also referred to as fact or measure columns.</p>
        <p>Frequent operations done on metric columns:</p>
        <ul>
          <li>Aggregation - SUM, MIN, MAX, COUNT, AVG etc</li>
          <li>Filter processing</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DateTime</b>
      </td>
      <td style="text-align:left">
        <p>This column represents time columns in the data. There can be multiple
          time columns in a table, but only one of them is the primary time column.
          Primary time column is the one that is set in the <a href="https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1">segmentConfig</a>.
          This primary time column is used by Pinot, for maintaining the time boundary
          between offline and realtime data in a hybrid table and for retention management.
          A primary time column is mandatory if the table&apos;s push type is <code>APPEND</code> and
          optional if the push type is <code>REFRESH</code> .</p>
        <p>Common operations done on time column:</p>
        <ul>
          <li>GROUP BY</li>
          <li>Filter processing</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><del><b>Time</b></del>
      </td>
      <td style="text-align:left">
        <p><b>This has been deprecated.</b> Use DateTime column type for time columns.</p>
        <p>This column represents a timestamp. There can be at most one time column
          in a table. Common operations done on time column:</p>
        <ul>
          <li>GROUP BY</li>
          <li>Filter processing</li>
        </ul>
        <p>The time column is also used internally by Pinot, for maintaining the
          time boundary between offline and realtime data in a hybrid table and for
          retention management. A time column is mandatory if the table&apos;s push
          type is <code>APPEND</code> and optional if the push type is <code>REFRESH</code> .</p>
      </td>
    </tr>
  </tbody>
</table>

## Schema format

A Pinot schema is written in JSON format. Here's an example which shows all the fields of a schema

{% code title="flights-schema.json" %}
```javascript
{
  "schemaName": "flights",
  "dimensionFieldSpecs": [
    {
      "name": "flightNumber",
      "dataType": "LONG"
    },
    {
      "name": "tags",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": "null"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "price",
      "dataType": "DOUBLE",
      "defaultNullValue": 0
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "millisSinceEpoch",
      "dataType": "LONG",
      "format": "1:MILLSECONDS:EPOCH",
      "granularity": "15:MINUTES"
    },
    {
      "name": "hoursSinceEpoch",
      "dataType": "INT",
      "format": "1:HOURS:EPOCH",
      "granularity": "1:HOURS"
    },
    {
      "name": "date",
      "dataType": "STRING",
      "format": "1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd",
      "granularity": "1:DAYS"
    }
  ]
}
```
{% endcode %}

The Pinot schema is composed of

| schema fields | description |
| :--- | :--- |
| **schemaName** | Defines the name of the schema. This is usually the same as the table name. The offline and the realtime table of a hybrid table should use the same schema. |
| **dimensionFieldSpecs** | A dimensionFieldSpec is defined for each dimension column. For more details, scroll down to [dimensionFieldSpec](schema.md#dimensionfieldspecs) |
| **metricFieldSpecs** | A metricFieldSpec is defined for each metric column. For more details, scroll down to [metricFieldSpec](schema.md#metricfieldspecs) |
| **dateTimeFieldSpec** | A dateTimeFieldSpec is defined for the time columns. There can be multiple time columns. For more details, scroll down to dateTimeFieldSpec. |
| ~~**timeFieldSpec**~~ | **Deprecated. Use dateTimeFieldSpec instead.** A timeFieldSpec is defined for the time column. There can only be one time column. For more details, scroll down to [timeFieldSpec](schema.md#timefieldspec) |

Below is a detailed description of each type of field spec.

### dimensionFieldSpecs

A dimensionFieldSpec is defined for each dimension column. Here's a list of the fields in the dimensionFieldSpec

<table>
  <thead>
    <tr>
      <th style="text-align:left">field</th>
      <th style="text-align:left">description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">name</td>
      <td style="text-align:left">Name of the dimension column</td>
    </tr>
    <tr>
      <td style="text-align:left">dataType</td>
      <td style="text-align:left">
        <p>Data type of the dimension column. Can be STRING, BOOLEAN, INT, LONG,
          DOUBLE, FLOAT, BYTES</p>
        <p>&lt;b&gt;&lt;/b&gt;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">defaultNullValue</td>
      <td style="text-align:left">Represents null values in the data, since Pinot doesn&apos;t support storing
        null column values natively (as part of its on-disk storage format). If
        not specified, an internal default null value is used as listed here</td>
    </tr>
    <tr>
      <td style="text-align:left">singleValueField</td>
      <td style="text-align:left">Boolean indicating if this is a single value or a multi value column.
        In the example above, the dimension <code>tags</code> is multi-valued. This
        means that it can have multiple values for a particular row, say <code>tag1, tag2, tag3</code>.
        For a multi-valued column, individual rows don&#x2019;t necessarily need
        to have the same number of values. Typical use case for this would be a
        column such as <code>skillSet</code> for a person (one row in the table)
        that can have multiple values such as <code>Real Estate, Mortgages.</code>
      </td>
    </tr>
  </tbody>
</table>

#### Internal default null values for dimension

| Data Type | Internal Default Null Value |
| :--- | :--- |
| INT | ​[Integer.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE)​ |
| LONG | ​[LONG.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE)​ |
| FLOAT | ​[Float.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY)​ |
| DOUBLE | ​[DOUBLE.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY)​ |
| STRING | "null" |
| BYTES | byte array of length 0 |

### metricFieldSpecs

A metricFieldSpec is defined for each metric column. Here's a list of fields in the metricFieldSpec

| field | description |
| :--- | :--- |
| name | Name of the metric column |
| dataType | Data type of the column. Can be INT, LONG, DOUBLE, FLOAT, BYTES \(for specialized representations such as HLL, TDigest, etc, where the column stores byte serialized version of the value\) |
| defaultNullValue | Represents null values in the data. If not specified, an internal default null value is used, as listed here. The values are the same as those used for dimensionFieldSpec. |

#### Internal default null values for metric

| Data Type | Internal Default Null Value |
| :--- | :--- |
| INT | 0 |
| LONG | 0 |
| FLOAT | 0.0 |
| DOUBLE | 0.0 |
| STRING | "null" |
| BYTES | byte array of length 0 |

### dateTimeFieldSpec

A dateTimeFieldSpec is used to define time columns of the table. Here's a list of the fields in a dateTimeFieldSpec

<table>
  <thead>
    <tr>
      <th style="text-align:left">field</th>
      <th style="text-align:left">description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">name</td>
      <td style="text-align:left">Name of the date time column</td>
    </tr>
    <tr>
      <td style="text-align:left">dataType</td>
      <td style="text-align:left">Data type of the date time column. Can be STRING, INT, LONG</td>
    </tr>
    <tr>
      <td style="text-align:left">format</td>
      <td style="text-align:left">
        <p>The format of the time column. The syntax of the format is <code>timeSize:timeUnit:timeFormat</code>
        </p>
        <p>timeFormat can be either EPOCH or SIMPLE_DATE_FORMAT. If it is SIMPLE_DATE_FORMAT,
          the pattern string is also specified. For example:</p>
        <p>1:MILLISECONDS:EPOCH - epoch millis</p>
        <p>1:HOURS:EPOCH - epoch hours</p>
        <p>1:DAYS:SIMPLE_DATE_FORMAT:yyyyMMdd - date specified like <code>20191018</code>
        </p>
        <p>1:HOURS:SIMPLE_DATE_FORMAT:EEE MMM dd HH:mm:ss ZZZ yyyy - date specified
          like <code>Mon Aug 24 12:36:50 America/Los_Angeles 2019</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">granularity</td>
      <td style="text-align:left">The granularity in which the column is bucketed. The syntax of granularity
        is
        <br /><code>bucket size:bucket unit</code>
        <br />For example, the format can be milliseconds <code>1:MILLISECONDS:EPOCH</code>,
        but bucketed to 15 minutes i.e. we only have one value for every 15 minute
        interval, in which case granularity can be specified as <code>15:MINUTES</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">defaultNullValue</td>
      <td style="text-align:left">Represents null values in the data. If not specified, an internal default
        null value is used, as listed here. The values are the same as those used
        for dimensionFieldSpec.</td>
    </tr>
  </tbody>
</table>

### ~~timeFieldSpec~~

This has been deprecated. Older schemas containing timeFieldSpec will be supported. But for new schemas, use DateTimeFieldSpec instead.

A timeFieldSpec is defined for the time column. A timeFieldSpec is composed of an incomingGranularitySpec and an outgoingGranularitySpec. **IncomingGranularitySpec** in combination with **outgoingGranularitySpec** can be used to transform the time column from incoming format to the outgoing format. If both of them are specified, the segment creation process will convert the time column from the incoming format to the outgoing format. If no time column transformation is required, you can specify just the **incomingGranularitySpec**.

| timeFieldSpec fields | Description |
| :--- | :--- |
| incomingGranularitySpec | Details of the time column in the incoming data |
| outgoingGranularitySpec | Details of the format to which the time column should be converted for using in Pinot |

The incoming and outgoing granularitySpec are defined as:

| field | description |
| :--- | :--- |
| name | Name of the time column. If incomingGranularitySpec, this is the name of the time column in the incoming data. If outgoingGranularitySpec, this is the name of the column you wish to transform it to and see in Pinot |
| dataType | Data type of the time column. Can be INT, LONG or STRING |
| timeType | Indicates the time unit. Can be one of DAYS, SECONDS, HOURS, MILLISECONDS, MICROSECONDS and NANOSECONDS |
| timeUnitSize | Indicates the bucket length. By default 1. E.g. in the sample above outgoing time is in fiveMinutesSinceEpoch i.e. rounded to 5 minutes buckets |
| timeFormat | EPOCH \(millisSinceEpoch, hoursSinceEpoch etc\) or SIMPLE\_DATE\_FORMAT \(yyyyMMdd, yyyyMMdd:hhssmm etc\) |

### Advanced fields

Apart from these, there's some advanced fields. These are common to all field specs.

| field name | description |
| :--- | :--- |
| maxLength | Max length of this column |
| transformFunction | Transform function to generate this column. See section [below](schema.md#ingestion-transform-functions). |
| virtualColumnProvider | Column value provider |

## Ingestion Transform Functions

Transform functions can be defined on columns in the schema. For example:

```javascript
"metricFieldSpecs": [
    {
      "name": "maxPrice",
      "dataType": "DOUBLE",
      "transformFunction": "Groovy({prices.max()}, prices)" // groovy function
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "hoursSinceEpoch",
      "dataType": "INT",
      "format": "1:HOURS:EPOCH",
      "granularity": "1:HOURS",
      "transformFunction": "toEpochHours(timestamp)" // inbuilt function
    }
```

Currently, we have support for 2 kinds of functions

1. Groovy functions
2. Inbuilt functions

{% hint style="warning" %}
**Note**

Currently, the arguments must be from the source data. They cannot be columns from the Pinot schema which have been created through transformations.
{% endhint %}

### Groovy functions

Groovy functions can be defined using the syntax:

```javascript
Groovy({groovy script}, argument1, argument2...argumentN)
```

Here's some examples of commonly needed functions. Any valid Groovy expression can be used.

#### String concatenation

Concat `firstName` and `lasName` to get `fullName`

```javascript
{
      "name": "fullName",
      "dataType": "STRING",
      "transformFunction": "Groovy({firstName+' '+lastName}, firstName, lastName)"
}
```

#### Find element in an array

Find max value in array `bids`

```javascript
{
      "name": "maxBid",
      "dataType": "INT",
      "transformFunction": "Groovy({bids.max{ it.toBigDecimal() }}, bids)"
}
```

#### Time transformation

Convert `timestamp` from `MILLISECONDS` to `HOURS`

```javascript
"dateTimeFieldSpecs": [{
    "name": "hoursSinceEpoch",
    "dataType": "LONG",
    "format" : "1:HOURS:EPOCH",
    "granularity": "1:HOURS"
    "transformFunction": "Groovy({timestamp/(1000*60*60)}, timestamp)"
  }]
```

#### Column name change

Simply change name of the column from `user_id` to `userId`

```javascript
{
      "name": "userId",
      "dataType": "LONG",
      "transformFunction": "Groovy({user_id}, user_id)"
}
```

#### Ternary operation

If `eventType` is `IMPRESSION` set `impression` to `1`. Similar for `CLICK`.

```javascript
{
    "name": "impressions",
    "dataType": "LONG",
    "transformFunction": "Groovy({eventType == 'IMPRESSION' ? 1: 0}, eventType)"
},
{
    "name": "clicks",
    "dataType": "LONG",
    "transformFunction": "Groovy({eventType == 'CLICK' ? 1: 0}, eventType)"
}
```

#### AVRO Map

Store an AVRO Map in Pinot as two multi-value columns. Sort the keys, to maintain the mapping.  
1\) The keys of the map as `map_keys`  
2\) The values of the map as `map_values`

```javascript
{
      "name": "map2_keys",
      "dataType": "STRING",
      "singleValueField": false,
      "transformFunction": "Groovy({map2.sort()*.key}, map2)"
},
{
      "name": "map2_values",
      "dataType": "INT",
      "singleValueField": false,
      "transformFunction": "Groovy({map2.sort()*.value}, map2)"
}
```

### Inbuilt Pinot functions

We have several inbuilt functions that can be used directly in as ingestion transform functions

#### DateTime functions

These are functions which enable commonly needed time transformations.

**toEpochXXX**

Converts from epoch milliseconds to a higher granularity.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function name</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">toEpochSeconds</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch seconds.</p>
        <p>Usage: <code>&quot;transformFunction&quot;: &quot;toEpochSeconds(millis)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochMinutes</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch minutes</p>
        <p>Usage: <code>&quot;transformFunction&quot;: &quot;toEpochMinutes(millis)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochHours</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch hours</p>
        <p>Usage: <code>&quot;transformFunction&quot;: &quot;toEpochHours(millis)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochDays</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch days</p>
        <p>Usage: <code>&quot;transformFunction&quot;: &quot;toEpochDays(millis)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

**toEpochXXXRounded**

Converts from epoch milliseconds to another granularity, rounding to the nearest rounding bucket. For example, `1588469352000` \(2020-05-01 42:29:12\) is `26474489` minutesSinceEpoch. ```toEpochMinutesRounded(1588469352000) = 26474480`` \(2020-05-01 42:20:00\)

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function Name</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">toEpochSecondsRounded</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch seconds, rounding to nearest rounding bucket</p>
        <p><code>&quot;transformFunction&quot;: &quot;toEpochSecondsRounded(millis, 30)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochMinutesRounded</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch seconds, rounding to nearest rounding bucket</p>
        <p><code>&quot;transformFunction&quot;: &quot;toEpochMinutesRounded(millis, 10)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochHoursRounded</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch seconds, rounding to nearest rounding bucket</p>
        <p><code>&quot;transformFunction&quot;: &quot;toEpochHoursRounded(millis, 6)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochDaysRounded</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch seconds, rounding to nearest rounding bucket</p>
        <p><code>&quot;transformFunction&quot;: &quot;toEpochDaysRounded(millis, 7)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

**fromEpochXXX**

Converts from an epoch granularity to milliseconds.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function Name</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">fromEpochSeconds</td>
      <td style="text-align:left">
        <p>Converts from epoch seconds to milliseconds</p>
        <p><code>&quot;transformFunction&quot;: &quot;fromEpochSeconds(secondsSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromEpochMinutes</td>
      <td style="text-align:left">
        <p>Converts from epoch minutes to milliseconds</p>
        <p><code>&quot;transformFunction&quot;: &quot;fromEpochMinutes(minutesSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromEpochHours</td>
      <td style="text-align:left">
        <p>Converts from epoch hours to milliseconds</p>
        <p><code>&quot;transformFunction&quot;: &quot;fromEpochHours(hoursSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromEpochDays</td>
      <td style="text-align:left">
        <p>Converts from epoch days to milliseconds</p>
        <p><code>&quot;transformFunction&quot;: &quot;fromEpochDays(daysSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

**Simple date format**

Converts simple date format strings to milliseconds and vice-a-versa, as per the provided pattern string.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function name</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">toDateTime</td>
      <td style="text-align:left">
        <p>Converts from milliseconds to a formatted date time string, as per the
          provided pattern</p>
        <p><code>&quot;transformFunction&quot;: &quot;toDateTime(millis, &apos;yyyy-MM-dd&apos;)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromDateTime</td>
      <td style="text-align:left">
        <p>Converts a formatted date time string to milliseconds, as per the provided
          pattern</p>
        <p><code>&quot;transformFunction&quot;: &quot;fromDateTime(dateTimeStr, &apos;EEE MMM dd HH:mm:ss ZZZ yyyy&apos;)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

#### Json functions

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function name</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">toJsonMapStr</td>
      <td style="text-align:left">
        <p>Converts a JSON/Avro map to a string. This json map can then be queried
          using <a href="https://docs.pinot.apache.org/users/user-guide-query/pinot-query-language#transform-function-in-aggregation-and-grouping">jsonExtractScalar</a> function.</p>
        <p><code>&quot;transformFunction&quot;: &quot;toJsonMapStr(jsonMapField)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

## Creating a Schema

Create a schema for your data, or see [`examples`](https://github.com/apache/incubator-pinot/tree/master/pinot-tools/src/main/resources/examples) for examples. Make sure you've [setup the cluster](cluster.md#setup-a-pinot-cluster)

Note: schema can also be created as part of table creation, refer to [Creating a table](table.md#creating-a-table).

{% tabs %}
{% tab title="pinot-admin.sh" %}
```bash
bin/pinot-admin.sh AddSchema -schemaFile transcript-schema.json -exec
```
{% endtab %}

{% tab title="curl" %}
```text
curl -F schemaName=@transcript-schema.json  localhost:9000/schemas
```
{% endtab %}
{% endtabs %}

Check out the schema in the [Rest API ](http://localhost:9000/help#!/Schema/getSchema)to make sure it was successfully uploaded

