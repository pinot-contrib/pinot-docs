# Schema

Schema is used to define the names, data types, and other information for the columns of a Pinot table.

The Pinot schema is composed of:

| Field                  | Description                                                                                                                                                                 |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **schemaName**         | Defines the name of the schema. This is usually the same as the table name. The offline and the real-time table of a hybrid table should use the same schema.                |
| **dimensionFieldSpec** | A dimensionFieldSpec is defined for each dimension column. For more details, scroll down to [DimensionFieldSpec](schema.md#dimensionfieldspec).                             |
| **metricFieldSpec**    | A metricFieldSpec is defined for each metric column. For more details, scroll down to [MetricFieldSpec](schema.md#metricfieldspec).                                         |
| **dateTimeFieldSpec**  | A dateTimeFieldSpec is defined for the time columns. There can be multiple time columns. For more details, scroll down to [DateTimeFieldSpec](schema.md#datetimefieldspec). |

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
      "format": "EPOCH",
      "granularity": "15:MINUTES"
    },
    {
      "name": "hoursSinceEpoch",
      "dataType": "INT",
      "format": "EPOCH|HOURS",
      "granularity": "1:HOURS"
    },
    {
      "name": "dateString",
      "dataType": "STRING",
      "format": "SIMPLE_DATE_FORMAT|yyyy-MM-dd",
      "granularity": "1:DAYS"
    }
  ]
}
```
{% endcode %}

The above json configuration is the example of Pinot schema derived from the flight data. As seen in the example, the schema is composed of 4 parts: `schemaName`, `dimensionFieldSpec`, `metricFieldSpec`, and  `dateTimeFieldSpec`. Below is a detailed description of each type of field spec.&#x20;

### DimensionFieldSpec

A dimensionFieldSpec is defined for each dimension column. Here's a list of the fields in the dimensionFieldSpec:

| Property         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name             | Name of the dimension column.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| dataType         | Data type of the dimension column. Can be INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING, BYTES,JSON.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| defaultNullValue | Represents null values in the data, since Pinot doesn't support storing null column values natively (as part of its on-disk storage format). If not specified, an internal default null value is used as listed here.                                                                                                                                                                                                                                                                                                                             |
| singleValueField | Boolean indicating if this is a single-valued or a multi-valued column. Multi-valued column is modeled as a list, where the order of the values are preserved and duplicate values are allowed. Individual rows don’t necessarily have the same number of values. Typical use case for this would be a column such as `skillSet` for a person (one row in the table) that can have multiple values such as `Real Estate, Mortgages`. The default null value for a multi-valued column is a single `defaultNullValue`, e.g. `[Integer.MIN_VALUE]`. |

#### Internal default null values for dimension

| Data Type | Internal Default Null Value                                                                                       |
| --------- | ----------------------------------------------------------------------------------------------------------------- |
| INT       | ​[Integer.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN\_VALUE)​               |
| LONG      | ​[Long.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN\_VALUE)​                     |
| FLOAT     | ​[Float.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE\_INFINITY)​   |
| DOUBLE    | ​[Double.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE\_INFINITY)​ |
| BOOLEAN   | 0 (`false`)                                                                                                       |
| TIMESTAMP | 0 (`1970-01-01 00:00:00 UTC`)                                                                                     |
| STRING    | "null"                                                                                                            |
| BYTES     | byte array of length 0                                                                                            |
| JSON      | "null"                                                                                                            |

### MetricFieldSpec

A metricFieldSpec is defined for each metric column. Here's a list of fields in the metricFieldSpec

| Property         | Description                                                                                                                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name             | Name of the metric column                                                                                                                                                                               |
| dataType         | Data type of the column. Can be INT, LONG, FLOAT, DOUBLE, BIG\_DECIMAL, BYTES (for specialized representations such as HLL, TDigest, etc, where the column stores byte serialized version of the value) |
| defaultNullValue | Represents null values in the data. If not specified, an internal default null value is used, as listed here.                                                                                           |

#### Internal default null values for metric

| Data Type    | Internal Default Null Value |
| ------------ | --------------------------- |
| INT          | 0                           |
| LONG         | 0                           |
| FLOAT        | 0.0                         |
| DOUBLE       | 0.0                         |
| BIG\_DECIMAL | 0.0                         |
| BYTES        | byte array of length 0      |

### DateTimeFieldSpec

A dateTimeFieldSpec is used to define time columns of the table. The following fields can be configured in the date time field spec -

| Property         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name             | Name of the date time column                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| dataType         | Data type of the date time column. Can be STRING, INT, LONG or TIMESTAMP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| format           | <p>The format in which the datetime is present in the column. Refer to <a href="schema.md#new-datetime-formats">Date time formats</a> for supported formats.</p><p></p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| granularity      | <p>The granularity in which the column is bucketed. The syntax of granularity is<br><code>bucket size:bucket unit</code><br>For example, the format can be milliseconds <code>1:MILLISECONDS:EPOCH</code>, but bucketed to 15 minutes i.e. we only have one value for every 15 minute interval, in which case granularity can be specified as <code>15:MINUTES</code>. <strong>Currently it is just for documentation purpose, and Pinot won't automatically round the time value to the specified granularity.</strong></p>                                                                                                                                                                                           |
| defaultNullValue | <p>Represents null values in the data. If not specified, an internal default null value is used. If date time is in String format, the default value will be <code>null</code>  or if timestamp then it is epoch 0 (i.e. <code>1970-01-01 00:00:00</code>).</p><p></p><p><strong>For the main time column of the table (time column specified in the <code>segmentsConfig</code></strong></p><p> <strong>in the table config), the main time column value must be in the range of <code>1971-01-01 UTC</code> to <code>2071-01-01 UTC</code> for segment management purpose (e.g. retention, time boundary). If the specified default null value is not within this range, segment creation time is used.</strong></p> |

#### New DateTime Formats

In the pinot master (0.12.0-SNAPSHOT), We have simplified date time formats for the users. The formats now follow the pattern  - `timeFormat|pattern/timeUnit|`\[`timeZone/timeSize]` . The fields present in `[]` are completely optional.  timeFormat can be one of `EPOCH` , `SIMPLE_DATE_FORMAT` or `TIMESTAMP` .&#x20;

* `TIMESTAMP` - This represents timestamp in milliseconds. It is equivalent to specifying `EPOCH:MILLISECONDS:1` \
  Examples -
  * `TIMESTAMP`
* `EPOCH` - This represents time in `timeUnit` since `00:00:00 UTC on 1 January 1970`, where `timeUnit` is one of [TimeUnit](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeUnit.html) enum values, e.g. `HOURS` , `MINUTES` etc. You can also specify the `timeSize` parameter. This size is multiplied to the value present in the time column to get an actual timestamp. e.g. if timesize is 5 and value in time column is 4996308 minutes. The value that will be converted to epoch timestamp will be 4996308 \* 5 \* 60 \* 1000 = 1498892400000 milliseconds. In simplest terms, `EPOCH|SECONDS|5` denotes the count of intervals of length 5 seconds from epoch 0 to now.\
  \
  Examples -&#x20;
  * `EPOCH` - Defaults to MILLISECONDS (only in `master` branch)
  * `EPOCH|SECONDS`
  * `EPOCH|SECONDS|5`
* `SIMPLE_DATE_FORMAT` - This represents time in the string format. The pattern should be specified using the Joda's [DateTimeFormat](https://www.joda.org/joda-time/key\_format.html) representation. In the master branch build, if no pattern is specified, we use [ISO 8601 DateTimeFormat](https://www.iso.org/iso-8601-date-and-time-format.html) to parse the date times. Optionals are supported with ISO format so users can specify date time string in `yyyy` or `yyyy-MM` or `yyyy-MM-dd` and so on \
  \
  You can also specify optional `timeZone` parameter which is the ID for a TimeZone, either an abbreviation such as `PST`, a full name such as `America/Los_Angeles`, or a custom ID such as `GMT-8:00`. \
  Examples -&#x20;
  * `SIMPLE_DATE_FORMAT`  (only in `master` branch)
  * `SIMPLE_DATE_FORMAT|yyyy-MM-dd HH:mm:ss`&#x20;
  * `SIMPLE_DATE_FORMAT|yyyy-MM-dd|IST`

{% hint style="warning" %}
Only datetime timeformats in lexicographical order are support in Pinot. so `yyyy-MM-dd` ,`MM-dd`  and `yyyy-dd` are valid while `MM-dd-yyyy` is not. \
The order is decided as year > month > day > hour > minutes > second.
{% endhint %}

#### Old date time formats

These date-time formats are still supported in Pinot for backward compatibility. However, new users should prefer to use the formats mentioned in the previous sections.

You will need to provide the format of the date along with the data type in the schema. The format is described using the following syntax: `timeSize:timeUnit:timeFormat:pattern` .

* **time size** - the size of the time unit. This size is multiplied to the value present in the time column to get an actual timestamp. e.g. if timesize is 5 and value in time column is 4996308 minutes. The value that will be converted to epoch timestamp will be 4996308 \* 5 \* 60 \* 1000 = 1498892400000 milliseconds.\
  If your date is not in `EPOCH` format, this value is not used and can be set to 1 or any other integer.
* **time unit** - one of [TimeUnit](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeUnit.html) enum values. e.g. `HOURS` , `MINUTES` etc. If your date is not in `EPOCH` format, this value is not used and can be set to `MILLISECONDS` or any other unit.
* **timeFormat** - can be either `EPOCH` or `SIMPLE_DATE_FORMAT`. If it is `SIMPLE_DATE_FORMAT`, the pattern string is also specified.
* **pattern** - This is optional and is only specified when the date is in `SIMPLE_DATE_FORMAT` . The pattern should be specified using Joda's [DateTimeFormat](https://www.joda.org/joda-time/key\_format.html) representation. e.g. 2020-08-21 can be represented as `yyyy-MM-dd`.

Here are some sample date-time formats you can use in the schema:

* `1:MILLISECONDS:EPOCH` - used when timestamp is in the epoch milliseconds and stored in `LONG` format
* `1:HOURS:EPOCH` - used when timestamp is in the epoch hours and stored in `LONG` or `INT` format
* `1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd` - when the date is in `STRING` format and has the pattern year-month-date. e.g. 2020-08-21
* `1:HOURS:SIMPLE_DATE_FORMAT:EEE MMM dd HH:mm:ss ZZZ yyyy` - when date is in `STRING` format. e.g. Mon Aug 24 12:36:50 America/Los\_Angeles 2019

### Built-in virtual columns

There are several built-in virtual columns inside the schema the can be used for debugging purposes:

| Column Name  | Column Type | Data Type | Description                                  |
| ------------ | ----------- | --------- | -------------------------------------------- |
| $hostName    | Dimension   | STRING    | Name of the server hosting the data          |
| $segmentName | Dimension   | STRING    | Name of the segment containing the record    |
| $docId       | Dimension   | INT       | Document id of the record within the segment |

These virtual columns can be used in queries in a similar way to regular columns.

### Advanced fields

Apart from these, there's some advanced fields. These are common to all field specs.

| Property              | Description               |
| --------------------- | ------------------------- |
| maxLength             | Max length of this column |
| virtualColumnProvider | Column value provider     |
