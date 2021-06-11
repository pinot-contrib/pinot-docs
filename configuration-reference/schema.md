# Schema

Schema is used to define the names, data types, and other information for the columns of a Pinot table. 

The Pinot schema is composed of:

| Field | Description |
| :--- | :--- |
| **schemaName** | Defines the name of the schema. This is usually the same as the table name. The offline and the realtime table of a hybrid table should use the same schema. |
| **dimensionFieldSpecs** | A dimensionFieldSpec is defined for each dimension column. For more details, scroll down to [DimensionFieldSpec](schema.md#dimensionfieldspecs). |
| **metricFieldSpecs** | A metricFieldSpec is defined for each metric column. For more details, scroll down to [MetricFieldSpec](schema.md#metricfieldspecs). |
| **dateTimeFieldSpec** | A dateTimeFieldSpec is defined for the time columns. There can be multiple time columns. For more details, scroll down to [DateTimeFieldSpec](schema.md#datetimefieldspec). |

Below is a detailed description of each type of field spec.

### DimensionFieldSpec

A dimensionFieldSpec is defined for each dimension column. Here's a list of the fields in the dimensionFieldSpec:

| Property | Description |
| :--- | :--- |
| name | Name of the dimension column. |
| dataType | Data type of the dimension column. Can be INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING, BYTES. |
| defaultNullValue | Represents null values in the data, since Pinot doesn't support storing null column values natively \(as part of its on-disk storage format\). If not specified, an internal default null value is used as listed here. |
| singleValueField | Boolean indicating if this is a single value or a multi value column. In the example above, the dimension `tags` is multi-valued. This means that it can have multiple values for a particular row, say `tag1, tag2, tag3`. For a multi-valued column, individual rows don’t necessarily need to have the same number of values. Typical use case for this would be a column such as `skillSet` for a person \(one row in the table\) that can have multiple values such as `Real Estate, Mortgages`. The default null value for a multi-valued column is a single `defaultNullValue`, e.g. `[Integer.MIN_VALUE]`. |

#### Internal default null values for dimension

| Data Type | Internal Default Null Value |
| :--- | :--- |
| INT | ​[Integer.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE)​ |
| LONG | ​[Long.MIN\_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE)​ |
| FLOAT | ​[Float.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY)​ |
| DOUBLE | ​[Double.NEGATIVE\_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY)​ |
| BOOLEAN | 0 \(`false`\) |
| TIMESTAMP | 0 \(`1970-01-01 00:00:00 UTC`\) |
| STRING | "null" |
| BYTES | byte array of length 0 |

### MetricFieldSpec

A metricFieldSpec is defined for each metric column. Here's a list of fields in the metricFieldSpec

| Property | Description |
| :--- | :--- |
| name | Name of the metric column |
| dataType | Data type of the column. Can be INT, LONG, FLOAT, DOUBLE, BYTES \(for specialized representations such as HLL, TDigest, etc, where the column stores byte serialized version of the value\) |
| defaultNullValue | Represents null values in the data. If not specified, an internal default null value is used, as listed here. |

#### Internal default null values for metric

| Data Type | Internal Default Null Value |
| :--- | :--- |
| INT | 0 |
| LONG | 0 |
| FLOAT | 0.0 |
| DOUBLE | 0.0 |
| BYTES | byte array of length 0 |

### DateTimeFieldSpec

A dateTimeFieldSpec is used to define time columns of the table. Here's a list of the fields in a dateTimeFieldSpec

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
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

### Advanced fields

Apart from these, there's some advanced fields. These are common to all field specs. 

| Property | Description |
| :--- | :--- |
| maxLength | Max length of this column |
| virtualColumnProvider | Column value provider |



