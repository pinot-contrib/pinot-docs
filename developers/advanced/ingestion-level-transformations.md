# Ingestion Transforms

Raw source data often needs to undergo some transformations before it is pushed to Pinot. Transformations include extracting records from nested objects, applying simple transform functions on certain columns, filtering out unwanted columns, etc and also more advanced operations like joining between datasets. Typically, a preprocessing job is needed to perform these operations. In streaming data sources, such transformations require users to write a samza job, and create another intermediate topic. Writing preprocessing jobs, especially for simple transformations, creates an additional step for user onboarding, can result in inconsistencies in the batch/stream data source, and increases the maintenance and operator overhead.

Here's some of the ingestion transformations that are supported by Pinot

## Filtering

Records can be filtered as they are being ingested. A filter function can be specified in the filterConfigs in the ingestionConfigs of the table config.

```text
tableConfig: {
    tableName: ...,
    tableType: ...,
    "ingestionConfig": {
        "filterConfig": {
            "filterFunction": “<expression>”
        }
    }
}
```

If the expression evaluates to true, the record will be filtered out. The expressions allowed here will be within the scope of the transform functions support that we have in Pinot today i.e. **Groovy expressions, or any inbuilt functions**.

### Examples

Consider table with a column `timestamp`.  
Filter out records which are older than timestamp 1589007600000

```text
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": “Groovy({timestamp < 1589007600000}, timestamp)”
    }
}
```

Consider a table with a string column `campaign` and a multi-value column double column `prices`.  
Filter out records where campaign = X or Y and sum of all elements in prices is less than 100

```text
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": “Groovy({(campaign == \"X\" || campaign == \"Y\") && prices.sum() < 100}, prices, campaign)”
    }
} 
```

## Column Transformation

Transform functions can be defined on columns in the ingestion config of the table config. For example:

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
      "transformFunction": "toEpochHours(timestamp)" // inbuilt function
    }]
  }
}
```
{% endcode %}

In this example, we're assuming that `prices` field is available in the source data, and `maxPrice` is expected in the Pinot schema. Similarly, `timestamp` is available in the source data, and `hoursSinceEpoch` is expected in the Pinot schema.

{% hint style="warning" %}
**Note**

Currently, the arguments must be from the source data. Other columns from Pinot schema can be used, as long as those columns have NOT been created through transformations themselves. In other words, chaining of transformations is not supported \(x = f\(y\) and z = f\(x\) not supported\)
{% endhint %}

Currently, we have support for 2 kinds of functions

1. Groovy functions
2. Inbuilt functions

### Groovy functions

Groovy functions can be defined using the syntax:

```javascript
Groovy({groovy script}, argument1, argument2...argumentN)
```

Here's some examples of commonly needed functions. Any valid Groovy expression can be used.

#### String concatenation

Concat `firstName` and `lasName` to get `fullName`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "fullName",
      "transformFunction": "Groovy({firstName+' '+lastName}, firstName, lastName)" 
    }
}
```

#### Find element in an array

Find max value in array `bids`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "maxBid",
      "transformFunction": "Groovy({bids.max{ it.toBigDecimal() }}, bids)" 
    }
}
```

#### Time transformation

Convert `timestamp` from `MILLISECONDS` to `HOURS`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "hoursSinceEpoch",
      "transformFunction": "Groovy({timestamp/(1000*60*60)}, timestamp)" 
    }
}
```

#### Column name change

Simply change name of the column from `user_id` to `userId`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "userId",
      "transformFunction": "Groovy({user_id}, user_id)" 
    }
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
    }
}
```

#### AVRO Map 

Store an AVRO Map in Pinot as two multi-value columns. Sort the keys, to maintain the mapping.  
1\) The keys of the map as `map_keys`  
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
    }
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
        <p>Usage:<code>&quot;toEpochSeconds(millis)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochMinutes</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch minutes</p>
        <p>Usage: <code>&quot;toEpochMinutes(millis)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochHours</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch hours</p>
        <p>Usage: <code>&quot;toEpochHours(millis)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">toEpochDays</td>
      <td style="text-align:left">
        <p>Converts epoch millis to epoch days</p>
        <p>Usage: <code>&quot;toEpochDays(millis)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

**toEpochXXXRounded**

Converts from epoch milliseconds to another granularity, rounding to the nearest rounding bucket. For example, `1588469352000` \(2020-05-01 42:29:12\) is `26474489` minutesSinceEpoch. ```toEpochMinutesRounded(1588469352000) = 26474480`` \(2020-05-01 42:20:00\)

| Function Name | Description |
| :--- | :--- |
| toEpochSecondsRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochSecondsRounded(millis, 30)"` |
| toEpochMinutesRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochMinutesRounded(millis, 10)"` |
| toEpochHoursRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochHoursRounded(millis, 6)"` |
| toEpochDaysRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochDaysRounded(millis, 7)"` |

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
        <p><code>&quot;fromEpochSeconds(secondsSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromEpochMinutes</td>
      <td style="text-align:left">
        <p>Converts from epoch minutes to milliseconds</p>
        <p><code>&quot;fromEpochMinutes(minutesSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromEpochHours</td>
      <td style="text-align:left">
        <p>Converts from epoch hours to milliseconds</p>
        <p><code>&quot;fromEpochHours(hoursSinceEpoch)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromEpochDays</td>
      <td style="text-align:left">
        <p>Converts from epoch days to milliseconds</p>
        <p><code>&quot;fromEpochDays(daysSinceEpoch)&quot;</code>
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
        <p><code>&quot;toDateTime(millis, &apos;yyyy-MM-dd&apos;)&quot;</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">fromDateTime</td>
      <td style="text-align:left">
        <p>Converts a formatted date time string to milliseconds, as per the provided
          pattern</p>
        <p><code>&quot;fromDateTime(dateTimeStr, &apos;EEE MMM dd HH:mm:ss ZZZ yyyy&apos;)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
**Note**

Letters that are not part of Simple Date Time legend \([https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)\) need to be escaped. For example:

`"transformFunction": "fromDateTime(dateTimeStr, 'yyyy-MM-dd''T''HH:mm:ss')"`
{% endhint %}

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
      <td style="text-align:left">json_format</td>
      <td style="text-align:left">
        <p>Converts a JSON/AVRO complex object to a string. This json map can then
          be queried using <a href="https://docs.pinot.apache.org/users/user-guide-query/pinot-query-language#transform-function-in-aggregation-and-grouping">jsonExtractScalar</a> function.</p>
        <p><code>&quot;json_format(jsonMapField)&quot;</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

## Flattening

There are 2 kinds of flattening

### One record into many

This is not natively supported as of yet. You can **write a custom Decoder/RecordReader if you want to use this**. Once the Decoder generates the multiple GenericRows from the provided input record, a List&lt;GenericRow&gt; should be set into the destination GenericRow, with the key `$MULTIPLE_RECORDS_KEY$`. The segment generation drivers will treat this as a special case and handle the multiple records case.

### Extract attributes from complex objects

_Feature TBD_

