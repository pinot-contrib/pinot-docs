---
description: >-
  Explore the Schema component in Apache Pinot, vital for defining the structure
  and data types of Pinot tables, enabling efficient data processing and
  analysis.
---

# Schema

Each table in Pinot is associated with a schema. A schema defines what fields are present in the table along with the data types.

The schema is stored in Zookeeper along with the table configuration.

{% hint style="info" %}
Schema naming in Pinot follows typical database table naming conventions, such as starting names with a letter, not ending with an underscore, and using only alphanumeric characters
{% endhint %}

### Categories

A schema also defines what category a column belongs to. Columns in a Pinot table can be categorized into three categories:

| Category      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Dimension** | <p>Dimension columns are typically used in slice and dice operations for answering business queries. Some operations for which dimension columns are used:</p><ul><li><code>GROUP BY</code> - group by one or more dimension columns along with aggregations on one or more metric columns</li><li>Filter clauses such as <code>WHERE</code></li></ul>                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Metric**    | <p>These columns represent the quantitative data of the table. Such columns are used for aggregation. In data warehouse terminology, these can also be referred to as fact or measure columns.</p><p>Some operation for which metric columns are used:</p><ul><li>Aggregation - <code>SUM</code>, <code>MIN</code>, <code>MAX</code>, <code>COUNT</code>, <code>AVG</code> etc</li><li>Filter clause such as <code>WHERE</code></li></ul>                                                                                                                                                                                                                                                                                                                          |
| **DateTime**  | <p>This column represents time columns in the data. There can be multiple time columns in a table, but only one of them can be treated as primary. The primary time column is the one that is present in the <a href="../../../configuration-reference/table.md#segments-config">segment config</a>.<br>The primary time column is used by Pinot to maintain the time boundary between offline and real-time data in a hybrid table and for retention management. A primary time column is mandatory if the table's push type is <code>APPEND</code> and optional if the push type is <code>REFRESH</code> .</p><p>Common operations that can be done on time column:</p><ul><li><code>GROUP BY</code></li><li>Filter clauses such as <code>WHERE</code></li></ul> |

Pinot does not enforce strict rules on which of these categories columns belong to, rather the categories can be thought of as hints to Pinot to do internal optimizations.

For example, metrics may be stored without a dictionary and can have a different default null value.

The categories are also relevant when doing segment merge and rollups. Pinot uses the dimension and time fields to identify records against which to apply merge/rollups.

Metrics aggregation is another example where Pinot uses dimensions and time are used as the key, and automatically aggregates values for the metric columns.

For configuration details, see [Schema configuration reference](https://docs.pinot.apache.org/configuration-reference/schema).&#x20;

### Date and time fields

Since Pinot doesn't have a dedicated `DATETIME` datatype support, you need to input time in either STRING, LONG, or INT format. However, Pinot needs to convert the date into an understandable format such as epoch timestamp to do operations. You can refer to [DateTime field spec configs](../../../configuration-reference/schema.md#datetimefieldspec) for more details on supported formats.

### Creating a schema

First, Make sure your [cluster is up](../cluster/#setup-a-pinot-cluster) and running.

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

Check out the schema in the [Rest API](http://localhost:9000/help#!/Schema/getSchema) to make sure it was successfully uploaded
