# Schema

Each table in Pinot is associated with a Schema. A schema defines what fields are present in the table along with the data types.

The schema is stored in the Zookeeper, along with the table configuration.

### Categories

A schema also defines what category a column belongs to. Columns in a Pinot table can be categorized into three categories:

| Category      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Dimension** | <p>Dimension columns are typically used in slice and dice operations for answering business queries. Some operations for which dimension columns are used:</p><ul><li><code>GROUP BY</code> - group by one or more dimension columns along with aggregations on one or more metric columns</li><li>Filter clauses such as <code>WHERE</code></li></ul>                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Metric**    | <p>These columns represent the quantitative data of the table. Such columns are used for aggregation. In data warehouse terminology, these can also be referred to as fact or measure columns.</p><p>Some operation for which metric columns are used:</p><ul><li>Aggregation - <code>SUM</code>, <code>MIN</code>, <code>MAX</code>, <code>COUNT</code>, <code>AVG</code> etc</li><li>Filter clause such as <code>WHERE</code></li></ul>                                                                                                                                                                                                                                                                                                                       |
| **DateTime**  | <p>This column represents time columns in the data. There can be multiple time columns in a table, but only one of them can be treated as primary. The primary time column is the one that is present in the <a href="../../configuration-reference/table.md#segments-config">segment config</a>.<br>The primary time column is used by Pinot to maintain the time boundary between offline and real-time data in a hybrid table and for retention management. A primary time column is mandatory if the table's push type is <code>APPEND</code> and optional if the push type is <code>REFRESH</code> .</p><p>Common operations that can be done on time column:</p><ul><li><code>GROUP BY</code></li><li>Filter clauses such as <code>WHERE</code></li></ul> |

Pinot does not enforce strict rules on which of these categories columns belong to, rather the categories can be thought of as hints to Pinot to do internal optimizations.

For example, metrics may be stored without a dictionary and can have a different default null value.

The categories are also relevant when doing segment merge and rollups. Pinot uses the dimension and time fields to identify records against which to apply merge/rollups.

Metrics aggregation is another example where Pinot uses dimensions and time are used as the key, and automatically aggregates values for the metric columns.

### Data Types

Data types determine the operations that can be performed on a column. Pinot supports the following data types:

| Data Type    | Default Dimension Value                                                                                         | Default Metric Value   |
| ------------ | --------------------------------------------------------------------------------------------------------------- | ---------------------- |
| INT          | [Integer.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN\_VALUE)               | 0                      |
| LONG         | [Long.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN\_VALUE)                     | 0                      |
| FLOAT        | [Float.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE\_INFINITY)   | 0.0                    |
| DOUBLE       | [Double.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE\_INFINITY) | 0.0                    |
| BIG\_DECIMAL | Not supported                                                                                                   | 0.0                    |
| BOOLEAN      | 0 (false)                                                                                                       | N/A                    |
| TIMESTAMP    | 0 (1970-01-01 00:00:00 UTC)                                                                                     | N/A                    |
| STRING       | "null"                                                                                                          | N/A                    |
| JSON         | "null"                                                                                                          | N/A                    |
| BYTES        | byte array of length 0                                                                                          | byte array of length 0 |

{% hint style="warning" %}
`BOOLEAN`, `TIMESTAMP`, `JSON` are added after release `0.7.1`. In release `0.7.1` and older releases, `BOOLEAN` is equivalent to `STRING.` `BIG_DECIMAL` is added after release `0.10.0`.
{% endhint %}

Pinot also supports columns that contain lists or arrays of items, but there isn't an explicit data type to represent these lists or arrays. Instead, you can indicate that a dimension column accepts multiple values. For more information, see [DimensionFieldSpec](https://docs.pinot.apache.org/configuration-reference/schema#dimensionfieldspec) in the Schema configuration reference.

### Date Time Fields

Since Pinot doesn't have a dedicated `DATETIME` datatype support, you need to input time in either STRING, LONG, or INT format. However, Pinot needs to convert the date into an understandable format such as epoch timestamp to do operations.

To achieve this conversion, you will need to provide the format of the date along with the data type in the schema. The format is described using the following syntax: `timeSize:timeUnit:timeFormat:pattern` .

* **time size** - the size of the time unit. This size is multiplied to the value present in the time column to get an actual timestamp. e.g. if timesize is 5 and value in time column is 4996308 minutes. The value that will be converted to epoch timestamp will be 4996308 \* 5 \* 60 \* 1000 = 1498892400000 milliseconds.\
  If your date is not in `EPOCH` format, this value is not used and can be set to 1 or any other integer.\\
* **time unit** - one of [TimeUnit](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeUnit.html) enum values. e.g. `HOURS` , `MINUTES` etc. If your date is not in `EPOCH` format, this value is not used and can be set to `MILLISECONDS` or any other unit.\\
* **timeFormat** - can be either `EPOCH` or `SIMPLE_DATE_FORMAT`. If it is `SIMPLE_DATE_FORMAT`, the pattern string is also specified. \\
* **pattern** - This is optional and is only specified when the date is in `SIMPLE_DATE_FORMAT` . The pattern should be specified using the java [SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html) representation. e.g. 2020-08-21 can be represented as `yyyy-MM-dd`.\\

Here are some sample date-time formats you can use in the schema:

* `1:MILLISECONDS:EPOCH` - used when timestamp is in the epoch milliseconds and stored in `LONG` format
* `1:HOURS:EPOCH` - used when timestamp is in the epoch hours and stored in `LONG` or `INT` format
* `1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd` - when the date is in `STRING` format and has the pattern year-month-date. e.g. 2020-08-21
* `1:HOURS:SIMPLE_DATE_FORMAT:EEE MMM dd HH:mm:ss ZZZ yyyy` - when date is in `STRING` format. e.g. Mon Aug 24 12:36:50 America/Los\_Angeles 2019

#### New DateTime Formats

From Pinot release 0.11.0, We have simplified date time formats for the users. The formats now follow the pattern  - `timeFormat|pattern/timeUnit|`\[`timeZone/timeSize]` . The fields present in `[]` are completely optional.  timeFormat can be one of `EPOCH` , `SIMPLE_DATE_FORMAT` or `TIMESTAMP` .&#x20;

* `TIMESTAMP` - This represents timestamp in milliseconds. It is equivalent to specifying `EPOCH:MILLISECONDS:1`&#x20;
* `EPOCH` - This represents time in `timeUnit` since `00:00:00 UTC on 1 January 1970.`  You can also specify the timeSize parameter.This size is multiplied to the value present in the time column to get an actual timestamp. e.g. if timesize is 5 and value in time column is 4996308 minutes. The value that will be converted to epoch timestamp will be 4996308 \* 5 \* 60 \* 1000 = 1498892400000 milliseconds.\
  Examples -&#x20;
  * `EPOCH|SECONDS`
  * `EPOCH|SECONDS|10`
* `SIMPLE_DATE_FORMAT` - This represents time in the string format. The pattern should be specified using the java [SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html) representation. If no pattern is specified, we use [ISO 8601 DateTimeFormat](https://www.iso.org/iso-8601-date-and-time-format.html) to parse the date times. Optionals are supported with ISO format so users can specify date time string in `yyyy` or `yyyy-MM` or `yyyy-MM-dd` and so on\
  \
  You can also specify optional `timeZone` parameter which is the ID for a TimeZone, either an abbreviation such as `PST`, a full name such as `America/Los_Angeles`, or a custom ID such as `GMT-8:00`. \
  Examples -&#x20;
  * `SIMPLE_DATE_FORMAT`
  * `SIMPLE_DATE_FORMAT|yyyy-MM-dd HH:mm:ss`&#x20;
  * `SIMPLE_DATE_FORMAT|yyyy-MM-dd|IST`

### Built-in Virtual Columns

There are several built-in virtual columns inside the schema the can be used for debugging purposes:

| Column Name  | Column Type | Data Type | Description                                  |
| ------------ | ----------- | --------- | -------------------------------------------- |
| $hostName    | Dimension   | STRING    | Name of the server hosting the data          |
| $segmentName | Dimension   | STRING    | Name of the segment containing the record    |
| $docId       | Dimension   | INT       | Document id of the record within the segment |

These virtual columns can be used in queries in a similar way to regular columns.

### Creating a Schema

First, Make sure your [cluster is up](cluster.md#setup-a-pinot-cluster) and running.

Let's create a schema and put it in a JSON file. For this example, we have created a schema for flight data.

{% hint style="info" %}
For more details on constructing a schema file, see the [Schema configuration reference](https://docs.pinot.apache.org/configuration-reference/schema).
{% endhint %}

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
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "15:MINUTES"
    },
    {
      "name": "hoursSinceEpoch",
      "dataType": "INT",
      "format": "1:HOURS:EPOCH",
      "granularity": "1:HOURS"
    },
    {
      "name": "dateString",
      "dataType": "STRING",
      "format": "1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd",
      "granularity": "1:DAYS"
    }
  ]
}
```
{% endcode %}

Then, we can upload the sample schema provided above using either a Bash command or REST API call.

{% tabs %}
{% tab title="pinot-admin.sh" %}
```bash
bin/pinot-admin.sh AddSchema -schemaFile flights-schema.json -exec

OR

bin/pinot-admin.sh AddTable -schemaFile flights-schema.json -tableFile flights-table.json -exec
```
{% endtab %}

{% tab title="curl" %}
```
curl -F schemaName=@transcript-schema.json  localhost:9000/schemas
```
{% endtab %}
{% endtabs %}

Check out the schema in the [Rest API](http://localhost:9000/help#!/Schema/getSchema)to make sure it was successfully uploaded
