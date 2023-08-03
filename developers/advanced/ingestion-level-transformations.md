# Ingestion Transformations

Raw source data often needs to undergo some transformations before it is pushed to Pinot.

Transformations include extracting records from nested objects, applying simple transform functions on certain columns, filtering out unwanted columns, as well as more advanced operations like joining between datasets.

A preprocessing job is usually needed to perform these operations. In streaming data sources you might write a Samza job and create an intermediate topic to store the transformed data.

For simple transformations, this can result in inconsistencies in the batch/stream data source and increase maintenance and operator overhead.

To make things easier, Pinot supports transformations that can be applied via the [table config](../../configuration-reference/table.md).

## Transformation Functions

Pinot supports the following functions:

1. Groovy functions
2. Inbuilt functions

{% hint style="warning" %}
A transformation function cannot mix Groovy and built-in functions - you can only use one type of function at a time.
{% endhint %}

### Groovy functions

Groovy functions can be defined using the syntax:

```javascript
Groovy({groovy script}, argument1, argument2...argumentN)
```

Any valid Groovy expression can be used.

:warning: **Enabling Groovy**

Allowing execuatable Groovy in ingestion transformation can be a security vulnerability. If you would like to enable Groovy for ingestion, you can set the following controller config.

`controller.disable.ingestion.groovy=false`

If not set, Groovy for ingestion transformation is disabled by default.

### Inbuilt Pinot functions

All the functions defined in [this directory](https://github.com/apache/pinot/tree/02cb2d4970c71a2ea5b4c140a860fbf220e11bd3/pinot-common/src/main/java/org/apache/pinot/common/function/scalar) annotated with `@ScalarFunction` (e.g. [toEpochSeconds](https://github.com/apache/pinot/blob/02cb2d4970c71a2ea5b4c140a860fbf220e11bd3/pinot-common/src/main/java/org/apache/pinot/common/function/scalar/DateTimeFunctions.java#L78)) are supported ingestion transformation functions.

Below are some commonly used built-in Pinot functions for ingestion transformations.

#### DateTime functions

These functions enable time transformations.

**toEpochXXX**

Converts from epoch milliseconds to a higher granularity.

| Function name  | Description                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------ |
| toEpochSeconds | <p>Converts epoch millis to epoch seconds.</p><p>Usage:<code>"toEpochSeconds(millis)"</code></p> |
| toEpochMinutes | <p>Converts epoch millis to epoch minutes</p><p>Usage: <code>"toEpochMinutes(millis)"</code></p> |
| toEpochHours   | <p>Converts epoch millis to epoch hours</p><p>Usage: <code>"toEpochHours(millis)"</code></p>     |
| toEpochDays    | <p>Converts epoch millis to epoch days</p><p>Usage: <code>"toEpochDays(millis)"</code></p>       |

**toEpochXXXRounded**

Converts from epoch milliseconds to another granularity, rounding to the nearest rounding bucket. For example, `1588469352000` (2020-05-01 42:29:12) is `26474489` minutesSinceEpoch. `` `toEpochMinutesRounded(1588469352000) = 26474480 `` (2020-05-01 42:20:00)

| Function Name         | Description                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| toEpochSecondsRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochSecondsRounded(millis, 30)"` |
| toEpochMinutesRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochMinutesRounded(millis, 10)"` |
| toEpochHoursRounded   | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochHoursRounded(millis, 6)"`    |
| toEpochDaysRounded    | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochDaysRounded(millis, 7)"`     |

**fromEpochXXX**

Converts from an epoch granularity to milliseconds.

| Function Name    | Description                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| fromEpochSeconds | <p>Converts from epoch seconds to milliseconds</p><p><code>"fromEpochSeconds(secondsSinceEpoch)"</code></p> |
| fromEpochMinutes | <p>Converts from epoch minutes to milliseconds</p><p><code>"fromEpochMinutes(minutesSinceEpoch)"</code></p> |
| fromEpochHours   | <p>Converts from epoch hours to milliseconds</p><p><code>"fromEpochHours(hoursSinceEpoch)"</code></p>       |
| fromEpochDays    | <p>Converts from epoch days to milliseconds</p><p><code>"fromEpochDays(daysSinceEpoch)"</code></p>          |

**Simple date format**

Converts simple date format strings to milliseconds and vice-a-versa, as per the provided pattern string.

| Function name                                                           | Description                                                                                                                                                              |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [ToDateTime](../../configuration-reference/functions/todatetime.md)     | <p>Converts from milliseconds to a formatted date time string, as per the provided pattern</p><p><code>"toDateTime(millis, 'yyyy-MM-dd')"</code></p>                     |
| [FromDateTime](../../configuration-reference/functions/fromdatetime.md) | <p>Converts a formatted date time string to milliseconds, as per the provided pattern</p><p><code>"fromDateTime(dateTimeStr, 'EEE MMM dd HH:mm:ss ZZZ yyyy')"</code></p> |

{% hint style="info" %}
**Note**

Letters that are not part of Simple Date Time legend ([https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)) need to be escaped. For example:

`"transformFunction": "fromDateTime(dateTimeStr, 'yyyy-MM-dd''T''HH:mm:ss')"`
{% endhint %}

#### JSON functions

| Function name | Description                                                                                                                                                                                                                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| json\_format  | <p>Converts a JSON/AVRO complex object to a string. This json map can then be queried using <a href="https://docs.pinot.apache.org/users/user-guide-query/pinot-query-language#transform-function-in-aggregation-and-grouping">jsonExtractScalar</a> function.</p><p><code>"json_format(jsonMapField)"</code></p> |

## Types of transformation

### Filtering

Records can be filtered as they are being ingested. A filter function can be specified in the filterConfigs in the ingestionConfigs of the table config.

```javascript
"tableConfig": {
    "tableName": ...,
    "tableType": ...,
    "ingestionConfig": {
        "filterConfig": {
            "filterFunction": "<expression>"
        }
    }
}
```

If the expression evaluates to true, the record will be filtered out. The expressions can use any of the transform functions described in the previous section.

Consider a table that has a column `timestamp`. If you want to filter out records that are older than timestamp 1589007600000, you could apply the following function:

```javascript
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": "Groovy({timestamp < 1589007600000}, timestamp)"
    }
}
```

Consider a table that has a string column `campaign` and a multi-value column double column `prices`. If you want to filter out records where campaign = 'X' or 'Y' and sum of all elements in prices is less than 100, you could apply the following function:

```javascript
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": "Groovy({(campaign == \"X\" || campaign == \"Y\") && prices.sum() < 100}, prices, campaign)"
    }
}
```

Filter config also supports SQL-like expression of built-in [scalar functions](../../users/user-guide-query/scalar-functions.md#scalar-functions) for filtering records (starting v 0.11.0+). Example:

```javascript
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": "strcmp(campaign, 'X') = 0 OR strcmp(campaign, 'Y') = 0 OR timestamp < 1589007600000"
    }
}
```

### Column Transformation

Transform functions can be defined on columns in the ingestion config of the table config.

```javascript
{ "tableConfig": {
    "tableName": ...,
    "tableType": ...,
    "ingestionConfig": {
        "transformConfigs": [{
          "columnName": "fieldName",
          "transformFunction": "<expression>"
        }]
    },
    ...
}
```

For example, imagine that our source data contains the `prices` and `timestamp` fields. We want to extract the maximum price and store that in the `maxPrices` field and convert the timestamp into the number of hours since the epoch and store it in the `hoursSinceEpoch` field. You can do this by applying the following transformation:

{% code title="pinot-table-offline.json" %}
```javascript
{
"tableName": "myTable",
...
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "maxPrice",
      "transformFunction": "Groovy({prices.max()}, prices)" // groovy function
    },
    {
      "columnName": "hoursSinceEpoch",
      "transformFunction": "toEpochHours(timestamp)" // built-in function
    }]
  }
}
```
{% endcode %}

Below are some examples of commonly used functions.

#### String concatenation

Concat `firstName` and `lastName` to get `fullName`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "fullName",
      "transformFunction": "Groovy({firstName+' '+lastName}, firstName, lastName)"
    }]
}
```

#### Find an element in an array

Find max value in array `bids`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "maxBid",
      "transformFunction": "Groovy({bids.max{ it.toBigDecimal() }}, bids)"
    }]
}
```

#### Time transformation

Convert `timestamp` from `MILLISECONDS` to `HOURS`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "hoursSinceEpoch",
      "transformFunction": "Groovy({timestamp/(1000*60*60)}, timestamp)"
    }]
}
```

#### Column name change

Change name of the column from `user_id` to `userId`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "userId",
      "transformFunction": "Groovy({user_id}, user_id)"
    }]
}
```

#### Extract value from a column containing space

Pinot doesn't support columns that have spaces, so if a source data column has a space, we'll need to store that value in a column with a supported name. To extract the value from `first Name` into the column `firstName`, run the following:

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "firstName",
      "transformFunction": "\"first Name \""
    }]
}
```

#### Ternary operation

If `eventType` is `IMPRESSION` set `impression` to `1`. Similar for `CLICK`.

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "impressions",
      "transformFunction": "Groovy({eventType == 'IMPRESSION' ? 1: 0}, eventType)"
    },
    {
      "columnName": "clicks",
      "transformFunction": "Groovy({eventType == 'CLICK' ? 1: 0}, eventType)"
    }]
}
```

#### AVRO Map

Store an AVRO Map in Pinot as two multi-value columns. Sort the keys, to maintain the mapping.\
1\) The keys of the map as `map_keys`\
2\) The values of the map as `map_values`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "map2_keys",
      "transformFunction": "Groovy({map2.sort()*.key}, map2)"
    },
    {
      "columnName": "map2_values",
      "transformFunction": "Groovy({map2.sort()*.value}, map2)"
    }]
}
```

#### Chaining transformations

Transformations can be chained. This means that you can use a field created by a transformation in another transformation function.

For example, we might have the following JSON document in the `data` field of our source data:

```json
{
  "userId": "12345678__foo__othertext"
}
```

We can apply one transformation to extract the `userId` and then another one to pull out the numerical part of the identifier:

```javascript
"ingestionConfig": {
    "transformConfigs": [
      {
        "columnName": "userOid",
        "transformFunction": "jsonPathString(data, '$.userId')"
      },
      {
        "columnName": "userId",
        "transformFunction": "Groovy({Long.valueOf(userOid.substring(0, 8))}, userOid)"
      }
   ]
}
```

### Flattening

There are 2 kinds of flattening:

#### One record into many

This is not natively supported as of yet. You can **write a custom Decoder/RecordReader if you want to use this**. Once the Decoder generates the multiple GenericRows from the provided input record, a List\<GenericRow> should be set into the destination GenericRow, with the key `$MULTIPLE_RECORDS_KEY$`. The segment generation drivers will treat this as a special case and handle the multiple records case.

#### Extract attributes from complex objects

_Feature TBD_
