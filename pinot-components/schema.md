# Schema

Schema  is used to define the names, data types and other information for the columns of a Pinot table. 

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
        <p></p>
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
      <td style="text-align:left"><b>Time</b>
      </td>
      <td style="text-align:left">
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
</table>## Schema format

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
  "timeFieldSpec": {
    "incomingGranularitySpec": {
      "name": "millisSinceEpoch",
      "dataType": "LONG",
      "timeFormat" : "EPOCH",
      "timeType": "MILLISECONDS"
    },
     "outgoingGranularitySpec": {
      "name": "fiveMinutesEpoch",
      "dataType": "INT",
      "timeFormat" : "EPOCH",
      "timeType": "MINUTES",
      "timeSize": "5"
    }
  }
}
```
{% endcode %}

The Pinot schema is composed of

| schema fields | description |
| :--- | :--- |
| **schemaName** | Defines the name of the schema. This is usually the same as the table name. The offline and the realtime table of a hybrid table should use the same schema. |
| **dimensionFieldSpecs** | A dimensionFieldSpec is defined for each dimension column. For more details, scroll down to [dimensionFieldSpec](schema.md#dimensionfieldspecs) |
| **metricFieldSpecs** | A metricFieldSpec is defined for each metric column. For more details, scroll down to [metricFieldSpec](schema.md#metricfieldspecs) |
| **timeFieldSpec** | A timeFieldSpec is defined for the time column. There can only be one time column. For more details, scroll down to [timeFieldSpec](schema.md#timefieldspec) |

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
        that can have multiple values such as <code>Real Estate, Mortgages</code>
      </td>
    </tr>
  </tbody>
</table>#### Internal default null values for dimension

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
| defaultNullValue | Represents null values in the data. If not specified, an internal default null value is used, as listed here. |

#### Internal default null values for metric

| Data Type | Internal Default Null Value |
| :--- | :--- |
| INT | 0 |
| LONG | 0 |
| FLOAT | 0.0 |
| DOUBLE | 0.0 |
| STRING | "null" |
| BYTES | byte array of length 0 |

### timeFieldSpec

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

Apart from these, there's some advanced fields. These are common to all field specs. You shouldn't typically need to use them:

| field name | description |
| :--- | :--- |
| maxLength | Max length of this column |
| transformFunction | \[WIP\] Transform function to generate this column. Can be based on other columns |
| virtualColumnProvider | Column value provider |

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
```
curl -F schemaName=@transcript-schema.json  localhost:9000/schemas
```
{% endtab %}
{% endtabs %}

Check out the schema in the [Rest API ](http://localhost:9000/help#!/Schema/getSchema)to make sure it was successfully uploaded

