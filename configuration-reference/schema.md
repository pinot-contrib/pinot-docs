# Schema

Schema is used to define the names, data types, and other information for the columns of a Pinot table.

The Pinot schema is composed of:

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Release Version</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**schemaName**</td>
      <td>-</td>
      <td>required</td>
      <td>Name of the schema. This must be the same as the table name without the REALTIME or OFFLINE suffix. Therefore, the offline and the real-time table of a hybrid table should use the same schema.</td>
    </tr>
    <tr>
      <td>**enableColumnBasedNullHandling**</td>
      <td>1.1.0</td>
      <td>false</td>
      <td>When set to `true`, enables column-based null handling. The default value `false` means to use table-based null handling. See [Null value support](../developers/advanced/null-value-support.md) for more information about this.</td>
    </tr>
    <tr>
      <td>**dimensionFieldSpec**</td>
      <td>-</td>
      <td>\[]</td>
      <td>A dimensionFieldSpec is defined for each dimension column. For more details, see [DimensionFieldSpec](schema.md#dimensionfieldspec).</td>
    </tr>
    <tr>
      <td>**metricFieldSpec**</td>
      <td>-</td>
      <td>\[]</td>
      <td>A metricFieldSpec is defined for each metric column. For more details, see [MetricFieldSpec](schema.md#metricfieldspec).</td>
    </tr>
    <tr>
      <td>**dateTimeFieldSpec**</td>
      <td>-</td>
      <td>\[]</td>
      <td>A dateTimeFieldSpec is defined for the time columns. There can be multiple time columns. For more details, see [DateTimeFieldSpec](schema.md#datetimefieldspec).</td>
    </tr>
    <tr>
      <td>**complexFieldSpec**</td>
      <td>-</td>
      <td>\[]</td>
      <td><p>A complexFieldSpec is defined for complex data types Map.  For more details, see <a data-mention href="schema.md#complexfieldspec">#complexfieldspec</a><br></p></td>
    </tr>
  </tbody>
</table>

{% code title="flights-schema.json" %}
```javascript
{
  "schemaName": "flights",
  "enableColumnBasedNullHandling": false,
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

The above json configuration is the example of Pinot schema derived from the flight data. As seen in the example, the schema is composed of 4 parts: `schemaName`, `dimensionFieldSpec`, `metricFieldSpec`, and `dateTimeFieldSpec`. Below is a detailed description of each type of field spec.

```json
flights-schema-map.json
{
  "schemaName": "flights",
  "enableColumnBasedNullHandling": false,
  "dimensionFieldSpecs": [
    {
      "name": "flightNumber",
      "dataType": "LONG"
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
  ],
  "complexFieldSpecs": [
    {
      "name": "tags",
      "dataType": "MAP",
      "fieldType": "COMPLEX",
      "notNull": false,
      "childFieldSpecs": {
        "key": {
          "name": "key",
          "dataType": "STRING",
          "fieldType": "DIMENSION",
          "notNull": false
        },
        "value": {
          "name": "value",
          "dataType": "STRING",
          "fieldType": "DIMENSION",
          "notNull": false
        }
      }
    }
  ]
}
```

The above JSON configuration is an example of a Pinot schema derived from flight data. As seen in the example, the schema is composed of 5 parts: schemaName, dimensionFieldSpecs, metricFieldSpecs, dateTimeFieldSpecs, and complexFieldSpecs.&#x20;

### Data Types

Data types determine the operations that can be performed on a column. Pinot supports the following data types:

<table>
  <thead>
    <tr>
      <th>Data Type</th>
      <th>Default Dimension Value</th>
      <th>Default Metric Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>[Integer.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE)</td>
      <td>0</td>
    </tr>
    <tr>
      <td>LONG</td>
      <td>[Long.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE)</td>
      <td>0</td>
    </tr>
    <tr>
      <td>FLOAT</td>
      <td>[Float.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY)</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>DOUBLE</td>
      <td>[Double.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY)</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>BIG\_DECIMAL</td>
      <td>Not supported</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>BOOLEAN</td>
      <td>0 (false)</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>TIMESTAMP</td>
      <td>0 (1970-01-01 00:00:00 UTC)</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>STRING</td>
      <td>"null"</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>JSON</td>
      <td>"null"</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>BYTES</td>
      <td>byte array of length 0</td>
      <td>byte array of length 0</td>
    </tr>
  </tbody>
</table>

{% hint style="warning" %}
The lowest granularity TIMESTAMP type supports is milliseconds epoch, nanoseconds is not supported.
{% endhint %}

{% hint style="info" %}
All the data types are comparable, and the ordering of the values must be consistent with equals (i.e. `v1.compareTo(v2) == 0` always has the same value as `v1.equals(v2)`). Also any value should equal to itself. In order to achieve so, the following conversions are applied:

For `FLOAT`and `DOUBLE`:

* Negative zero (`-0.0`) is converted to `0.0`&#x20;
* `NaN` is converted to `null` (default value)

For `BIG_DECIMAL`:

* Trailing zeros are stripped off (can be turned off)
{% endhint %}

Read the following sections for details on how data types are used in various parts of a schema.

### DimensionFieldSpec

A dimensionFieldSpec is defined for each dimension column. Here's a list of the fields in the dimensionFieldSpec:

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>name</td>
      <td>Name of the dimension column.</td>
    </tr>
    <tr>
      <td>dataType</td>
      <td>Data type of the dimension column. Can be INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING, BYTES,JSON.</td>
    </tr>
    <tr>
      <td>defaultNullValue</td>
      <td>Represents null values in the data, since Pinot doesn't support storing null column values natively (as part of its on-disk storage format). If not specified, an internal default null value is used as listed here.</td>
    </tr>
    <tr>
      <td>singleValueField</td>
      <td>Boolean indicating if this is a single-valued or a multi-valued column. Multi-valued column is modeled as a list, where the order of the values are preserved and duplicate values are allowed. Individual rows don’t necessarily have the same number of values. Typical use case for this would be a column such as `skillSet` for a person (one row in the table) that can have multiple values such as `Real Estate, Mortgages`. The default null value for a multi-valued column is a single `defaultNullValue`, e.g. `[Integer.MIN_VALUE]`.</td>
    </tr>
  </tbody>
</table>

#### Internal default null values for dimension

<table>
  <thead>
    <tr>
      <th>Data Type</th>
      <th>Internal Default Null Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>​[Integer.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE)​</td>
    </tr>
    <tr>
      <td>LONG</td>
      <td>​[Long.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE)​</td>
    </tr>
    <tr>
      <td>FLOAT</td>
      <td>​[Float.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY)​</td>
    </tr>
    <tr>
      <td>DOUBLE</td>
      <td>​[Double.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY)​</td>
    </tr>
    <tr>
      <td>BOOLEAN</td>
      <td>0 (`false`)</td>
    </tr>
    <tr>
      <td>TIMESTAMP</td>
      <td>0 (`1970-01-01 00:00:00 UTC`)</td>
    </tr>
    <tr>
      <td>STRING</td>
      <td>"null"</td>
    </tr>
    <tr>
      <td>BYTES</td>
      <td>byte array of length 0</td>
    </tr>
    <tr>
      <td>JSON</td>
      <td>"null"</td>
    </tr>
  </tbody>
</table>

### MetricFieldSpec

A metricFieldSpec is defined for each metric column. Here's a list of fields in the metricFieldSpec

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>name</td>
      <td>Name of the metric column</td>
    </tr>
    <tr>
      <td>dataType</td>
      <td>Data type of the column. Can be INT, LONG, FLOAT, DOUBLE, BIG\_DECIMAL, BYTES (for specialized representations such as HLL, TDigest, etc, where the column stores byte serialized version of the value)</td>
    </tr>
    <tr>
      <td>defaultNullValue</td>
      <td>Represents null values in the data. If not specified, an internal default null value is used, as listed here.</td>
    </tr>
  </tbody>
</table>

#### Internal default null values for metric

<table>
  <thead>
    <tr>
      <th>Data Type</th>
      <th>Internal Default Null Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>INT</td>
      <td>0</td>
    </tr>
    <tr>
      <td>LONG</td>
      <td>0</td>
    </tr>
    <tr>
      <td>FLOAT</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>DOUBLE</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>BIG\_DECIMAL</td>
      <td>0.0</td>
    </tr>
    <tr>
      <td>BYTES</td>
      <td>byte array of length 0</td>
    </tr>
  </tbody>
</table>

### ComplexFieldSpec

A complexFieldSpec is defined for complex data types Map. The following fields can be configured in the complex field spec -

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Name</td>
      <td>Name of the complex column</td>
    </tr>
    <tr>
      <td>dataType</td>
      <td>Data type of the complex column.Currently supports MAP</td>
    </tr>
    <tr>
      <td>fieldType</td>
      <td>Should be set to COMPLEX</td>
    </tr>
    <tr>
      <td>notNull</td>
      <td>Boolean indicating if this column can contain null values</td>
    </tr>
    <tr>
      <td>childFieldSpecs</td>
      <td>Specification for the key and value fields of the Map. See the details below</td>
    </tr>
  </tbody>
</table>

### childFieldSpecs

The \`childFieldSpecs\` property defines the structure of the key and value fields within the Map. It contains two sub-specifications: \`key\` and \`value\`.&#x20;

### key childFieldSpec

The key of a Map in Pinot is always a String. The key childFieldSpec has the following properties:

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Name</td>
      <td>Should be set to key.</td>
    </tr>
    <tr>
      <td>dataType</td>
      <td>Should be set to String</td>
    </tr>
    <tr>
      <td>fieldType</td>
      <td>Should be set to Dimension</td>
    </tr>
    <tr>
      <td>notNull</td>
      <td>Boolean indicating if the key can be null (typically set to false)</td>
    </tr>
  </tbody>
</table>

### value childFieldSpec

The value childFieldSpec defines the type of values stored in the Map. It has the following properties:

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Name</td>
      <td>Should be set to "value"</td>
    </tr>
    <tr>
      <td>dataType</td>
      <td>Data type of the value ("STRING", "INT", "LONG", "FLOAT", "DOUBLE")</td>
    </tr>
    <tr>
      <td>fieldType</td>
      <td>Should be set to "DIMENSION" for non-numeric types</td>
    </tr>
    <tr>
      <td>notNull</td>
      <td>Boolean indicating if the value can be null</td>
    </tr>
  </tbody>
</table>

### DateTimeFieldSpec

A dateTimeFieldSpec is used to define time columns of the table. The following fields can be configured in the date time field spec -

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>name</td>
      <td>Name of the date time column</td>
    </tr>
    <tr>
      <td>dataType</td>
      <td><p>Data type of the date time column. Can be <code>STRING</code>, <code>INT</code>, <code>LONG</code>, or <code>TIMESTAMP.</code><br><br><strong><code>Note:</code></strong>Internally <code>TIMESTAMP</code> is stored as <code>LONG</code> (milliseconds since epoch). To use the<code>TIMESTAMP format, ensure your</code> source data is either in<code>LONG</code> values or <code>STRING</code> values of JDBC timestamp format (<code>2021-01-01 01:01:01.123</code>).</p></td>
    </tr>
    <tr>
      <td>format</td>
      <td>The format in which the datetime is present in the column. Refer to [Date time formats](schema.md#new-datetime-formats) for supported formats.</td>
    </tr>
    <tr>
      <td>granularity</td>
      <td><p>The granularity in which the column is bucketed. The syntax of granularity is<br><code>bucket size:bucket unit</code><br>For example, the format can be milliseconds <code>1:MILLISECONDS:EPOCH</code>, but bucketed to 15 minutes i.e. we only have one value for every 15 minute interval, in which case granularity can be specified as <code>15:MINUTES</code>. <strong>Currently it is just for documentation purpose, and Pinot won't automatically round the time value to the specified granularity.</strong></p></td>
    </tr>
    <tr>
      <td>defaultNullValue</td>
      <td><p>Represents null values in the data. If not specified, an internal default null value is used. If date time is in String format, the default value will be <code>null</code> or if timestamp then it is epoch 0 (i.e. <code>1970-01-01 00:00:00</code>).</p><p><strong>For the main time column of the table (time column specified in the <code>segmentsConfig</code></strong></p><p><strong>in the table config), the main time column value must be in the range of <code>1971-01-01 UTC</code> to <code>2071-01-01 UTC</code> for segment management purpose (e.g. retention, time boundary). If the specified default null value is not within this range, segment creation time is used.</strong></p></td>
    </tr>
  </tbody>
</table>

#### New DateTime Formats

In the pinot master (0.12.0-SNAPSHOT), We have simplified date time formats for the users. The formats now follow the pattern - `timeFormat|pattern/timeUnit|`\[`timeZone/timeSize]` . The fields present in `[]` are completely optional. timeFormat can be one of `EPOCH` , `SIMPLE_DATE_FORMAT` or `TIMESTAMP` .

* `TIMESTAMP` - This represents timestamp in milliseconds. It is equivalent to specifying `EPOCH|MILLISECONDS|1`\
  Examples -
  * `TIMESTAMP`
* `EPOCH` - This represents time in `timeUnit` since `00:00:00 UTC on 1 January 1970`, where `timeUnit` is one of [TimeUnit](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeUnit.html) enum values, e.g. `HOURS` , `MINUTES` etc. You can also specify the `timeSize` parameter. This size is multiplied to the value present in the time column to get an actual timestamp. e.g. if timesize is 5 and value in time column is 4996308 minutes. The value that will be converted to epoch timestamp will be 4996308 \* 5 \* 60 \* 1000 = 1498892400000 milliseconds. In simplest terms, `EPOCH|SECONDS|5` denotes the count of intervals of length 5 seconds from epoch 0 to now.\
  \
  Examples -
  * `EPOCH` - Defaults to MILLISECONDS (only in `master` branch)
  * `EPOCH|SECONDS`
  * `EPOCH|SECONDS|5`
* `SIMPLE_DATE_FORMAT` - This represents time in the string format. The pattern should be specified using the Joda's [DateTimeFormat](https://www.joda.org/joda-time/key_format.html) representation. In the master branch build, if no pattern is specified, we use [ISO 8601 DateTimeFormat](https://www.iso.org/iso-8601-date-and-time-format.html) to parse the date times. Optionals are supported with ISO format so users can specify date time string in `yyyy` or `yyyy-MM` or `yyyy-MM-dd` and so on\
  \
  You can also specify optional `timeZone` parameter which is the ID for a TimeZone, either an abbreviation such as `PST`, a full name such as `America/Los_Angeles`, or a custom ID such as `GMT-8:00`.\
  Examples -
  * `SIMPLE_DATE_FORMAT` (only in `master` branch)
  * `SIMPLE_DATE_FORMAT|yyyy-MM-dd HH:mm:ss`
  * `SIMPLE_DATE_FORMAT|yyyy-MM-dd|IST`

{% hint style="warning" %}
Only datetime timeformats in lexicographical order are support in Pinot. so `yyyy-MM-dd` ,`MM-dd` and `yyyy-dd` are valid while `MM-dd-yyyy` is not.\
The order is decided as year > month > day > hour > minutes > second.
{% endhint %}

#### Old date time formats

These date-time formats are still supported in Pinot for backward compatibility. However, new users should prefer to use the formats mentioned in the previous sections.

You will need to provide the format of the date along with the data type in the schema. The format is described using the following syntax: `timeSize:timeUnit:timeFormat:pattern` .

* **time size** - the size of the time unit. This size is multiplied to the value present in the time column to get an actual timestamp. e.g. if timesize is 5 and value in time column is 4996308 minutes. The value that will be converted to epoch timestamp will be 4996308 \* 5 \* 60 \* 1000 = 1498892400000 milliseconds.\
  If your date is not in `EPOCH` format, this value is not used and can be set to 1 or any other integer.
* **time unit** - one of [TimeUnit](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeUnit.html) enum values. e.g. `HOURS` , `MINUTES` etc. If your date is not in `EPOCH` format, this value is not used and can be set to `MILLISECONDS` or any other unit.
* **timeFormat** - can be either `EPOCH` or `SIMPLE_DATE_FORMAT`. If it is `SIMPLE_DATE_FORMAT`, the pattern string is also specified.
* **pattern** - This is optional and is only specified when the date is in `SIMPLE_DATE_FORMAT` . The pattern should be specified using Joda's [DateTimeFormat](https://www.joda.org/joda-time/key_format.html) representation. e.g. 2020-08-21 can be represented as `yyyy-MM-dd`.

Here are some sample date-time formats you can use in the schema:

* `1:MILLISECONDS:EPOCH` - used when timestamp is in the epoch milliseconds and stored in `LONG` format
* `1:HOURS:EPOCH` - used when timestamp is in the epoch hours and stored in `LONG` or `INT` format
* `1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd` - when the date is in `STRING` format and has the pattern year-month-date. e.g. 2020-08-21
* `1:HOURS:SIMPLE_DATE_FORMAT:EEE MMM dd HH:mm:ss ZZZ yyyy` - when date is in `STRING` format. e.g. Mon Aug 24 12:36:50 America/Los\_Angeles 2019

### Built-in virtual columns

There are several built-in virtual columns inside the schema the can be used for debugging purposes:

<table>
  <thead>
    <tr>
      <th>Column Name</th>
      <th>Column Type</th>
      <th>Data Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$hostName</td>
      <td>Dimension</td>
      <td>STRING</td>
      <td>Name of the server hosting the data</td>
    </tr>
    <tr>
      <td>$segmentName</td>
      <td>Dimension</td>
      <td>STRING</td>
      <td>Name of the segment containing the record</td>
    </tr>
    <tr>
      <td>$docId</td>
      <td>Dimension</td>
      <td>INT</td>
      <td>Document id of the record within the segment</td>
    </tr>
  </tbody>
</table>

These virtual columns can be used in queries in a similar way to regular columns.

### Advanced fields

Apart from these, there's some advanced fields. These are common to all field specs.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>maxLength</td>
      <td><p>Max length of this column.<br>Applicable for dataType: <code>STRING</code>, <code>JSON</code> and <code>BYTES</code></p></td>
    </tr>
    <tr>
      <td>maxLengthExceedStrategy</td>
      <td><p>Takes in 4 values: <code>TRIM_LENGTH</code>, <code>SUBSTITUTE_DEFAULT_VALUE</code>, <code>NO_ACTION</code>, <code>ERROR</code>.<br>Default is <code>TRIM_LENGTH</code> for <code>STRING</code>; <code>NO_ACTION</code> for <code>JSON</code> and <code>BYTES</code>.<br><code>TRIM_LENGTH</code>: Only <code>maxLength</code> characters are ingested for this field in incoming record.<br><code>SUBSTITUTE_DEFAULT_VALUE</code>: If the length of value in incoming record exceeds <code>maxLength</code>, substitute it with default value specified for the field.<br><code>NO_ACTION</code>: Ingest the record as is.<br><code>ERROR</code>: Throws an error if length of incoming record exceeds <code>maxLength</code>.</p></td>
    </tr>
    <tr>
      <td>allowTrailingZeros</td>
      <td>Whether to allow trailing zeros for `BIG_DECIMAL` column. By default `false`, where trailing zeros are stripped off.</td>
    </tr>
    <tr>
      <td>virtualColumnProvider</td>
      <td>Column value provider</td>
    </tr>
  </tbody>
</table>

