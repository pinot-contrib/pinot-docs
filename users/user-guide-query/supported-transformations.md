---
description: >-
  This document contains the list of all the transformation functions supported
  by Pinot SQL.
---

# Transformation Functions

## Math Functions

| Function                                                                               | 
| -------------------------------------------------------------------------------------- | 
| ****[**ADD(col1, col2, col3...)**](../../configuration-reference/functions/add.md)****<br/>Sum of at least two values | 
| ****[**SUB(col1, col2)**](../../configuration-reference/functions/sub.md)****<br />Difference between two values          | 
| [**MULT(col1, col2, col3...)**](../../configuration-reference/functions/mult.md)<br />Product of at least two values                                                          | 
| ****[**DIV(col1, col2)**](../../configuration-reference/functions/div.md)****<br /> Quotient of two values         | 
| ****[**MOD(col1, col2)**](../../configuration-reference/functions/mod.md)****<br/>Modulo of two values          | 
| ****[**ABS(col1)**](../../configuration-reference/functions/abs.md)****<br />Absolute of a value                | 
| ****[**CEIL(col1)**](../../configuration-reference/functions/ceil.md#signature)****<br />Rounded up to the nearest integer.    | 
| ****[**FLOOR(col1)**](../../configuration-reference/functions/floor.md)****<br />Rounded down to the nearest integer.           | 
| ****[**EXP(col1)**](../../configuration-reference/functions/exp.md)**** <br /> Euler’s number(e) raised to the power of col.             | 
| ****[**LN(col1)**](../../configuration-reference/functions/ln.md)****    <br />Natural log of value i.e. ln(col1)              | 
| [**SQRT(col1)**](../../configuration-reference/functions/sqrt.md) <br/> Square root of a value                                                                         | 

## String Functions

Multiple string functions are supported out of the box from release-0.5.0 .

| Function                                                                                                                                                                                                                                                                         |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><a href="../../configuration-reference/functions/upper.md"><strong>UPPER</strong></a>(col)<br>convert string to upper case</p>                                                                                                                                                |
| <p><a href="../../configuration-reference/functions/lower.md"><strong>LOWER</strong></a>(col)<br>convert string to lower case</p>                                                                                                                                                |
| <p><a href="../../configuration-reference/functions/reverse.md"><strong>REVERSE</strong></a>(col)<br>reverse the string</p>                                                                                                                                                      |
| <p><a href="../../configuration-reference/functions/substr.md"><strong>SUBSTR</strong></a>(col, startIndex, endIndex)<br>Gets substring of the input string from start to endIndex. Index begins at 0. Set endIndex to -1 to calculate till end of the string</p>                |
| <p><a href="../../configuration-reference/functions/concat.md"><strong>CONCAT(col1, col2, seperator)</strong></a><br>Concatenate two input strings using the seperator</p>                                                                                                       |
| <p><a href="../../configuration-reference/functions/trim.md"><strong>TRIM(col)</strong></a><br>trim spaces from both side of the string</p>                                                                                                                                      |
| <p><a href="../../configuration-reference/functions/ltrim.md"><strong>LTRIM(col)</strong></a><br>trim spaces from left side of the string</p>                                                                                                                                    |
| <p><a href="../../configuration-reference/functions/rtrim.md"><strong>RTRIM(col)</strong></a><br>trim spaces from right side of the string</p>                                                                                                                                   |
| <p><a href="../../configuration-reference/functions/length.md"><strong>LENGTH(col)</strong></a><br>calculate length of the string</p>                                                                                                                                            |
| <p><a href="../../configuration-reference/functions/strpos.md"><strong>STRPOS(col, find, N)</strong></a><br>Find Nth instance of <code>find</code> string in input. Returns 0 if input string is empty. Returns -1 if the Nth instance is not found or input string is null.</p> |
| <p><a href="../../configuration-reference/functions/startswith.md"><strong>STARTSWITH(col, prefix)</strong></a><br>returns <code>true</code> if columns starts with prefix string.</p>                                                                                           |
| <p><a href="../../configuration-reference/functions/replace.md"><strong>REPLACE(col, find, substitute)</strong></a><br>replace all instances of <code>find</code> with <code>replace</code> in input</p>                                                                         |
| <p><a href="../../configuration-reference/functions/rpad.md"><strong>RPAD(col, size, pad)</strong></a><br>string padded from the right side with <code>pad</code> to reach final <code>size</code></p>                                                                           |
| <p><a href="../../configuration-reference/functions/lpad.md"><strong>LPAD(col, size, pad)</strong></a><br>string padded from the left side with <code>pad</code> to reach final <code>size</code></p>                                                                            |
| <p><a href="../../configuration-reference/functions/codepoint.md"><strong>CODEPOINT(col)</strong></a><br>the Unicode codepoint of the first character of the string</p>                                                                                                          |
| <p><a href="../../configuration-reference/functions/chr.md"><strong>CHR(codepoint)</strong></a><br>the character corresponding to the Unicode codepoint</p>                                                                                                                      |

## DateTime Functions

Date time functions allow you to perform transformations on columns that contain timestamps or dates.

| Function                                                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| <p><a href="../../configuration-reference/functions/timeconvert.md"><strong>TIMECONVERT(col, fromUnit, toUnit)</strong></a><br>Converts the value into another time unit. the column should be an epoch timestamp.</p>                                                                           |
| <p><a href="../../configuration-reference/functions/datetimeconvert.md"><strong>DATETIMECONVERT(columnName, inputFormat, outputFormat, outputGranularity)</strong></a><br>Converts the value into another date time format, and buckets time based on the given time granularity.</p>            |
| <p><a href="../../configuration-reference/functions/datetrunc.md"><strong>DATETRUNC</strong></a><br>Converts the value into a specified output granularity seconds since UTC epoch that is bucketed on a unit in a specified timezone.</p>                                                       |
| <p><a href="../../configuration-reference/functions/toEpoch.md"><strong>ToEpoch&#x3C;TIME_UNIT>(timeInMillis)</strong></a><br>Convert epoch milliseconds to epoch &#x3C;Time Unit>.</p>                                                                                                          |
| <p><a href="../../configuration-reference/functions/toEpochRounded.md"><strong>ToEpoch&#x3C;TIME_UNIT>Rounded(timeInMillis, bucketSize)</strong></a><br>Convert epoch milliseconds to epoch &#x3C;Time Unit>, round to nearest rounding bucket(Bucket size is defined in &#x3C;Time Unit>).</p>  |
| <p><a href="../../configuration-reference/functions/toEpochBucket.md"><strong>ToEpoch&#x3C;TIME_UNIT>Bucket(timeInMillis, bucketSize)</strong></a><br>Convert epoch milliseconds to epoch &#x3C;Time Unit>, and divided by bucket size(Bucket size is defined in &#x3C;Time Unit>).</p>          |
| <p><a href="../../configuration-reference/functions/fromEpoch.md"><strong>FromEpoch&#x3C;TIME_UNIT></strong><br></a>Convert epoch &#x3C;Time Unit> to epoch milliseconds.<a href="../../configuration-reference/functions/fromEpoch.md"><strong>(timeIn&#x3C;Time_UNIT>)</strong></a></p>        |
| <p><a href="../../configuration-reference/functions/fromEpochBucket.md"><strong>FromEpoch&#x3C;TIME_UNIT>Bucket(timeIn&#x3C;Time_UNIT>, bucketSizeIn&#x3C;Time_UNIT>)</strong></a><br>Convert epoch &#x3C;Bucket Size>&#x3C;Time Unit> to epoch milliseconds.</p>                                |
| <p><a href="../../configuration-reference/functions/todatetime.md"><strong>ToDateTime(timeInMillis, pattern[, timezoneId])</strong></a><br>Convert epoch millis value to DateTime string represented by pattern.</p>                                                                             |
| <p><a href="../../configuration-reference/functions/fromdatetime.md"><strong>FromDateTime(dateTimeString, pattern)</strong></a><br>Convert DateTime string represented by pattern to epoch millis.</p>                                                                                           |
| <p><a href="../../configuration-reference/functions/round.md"><strong>round(timeValue, bucketSize)</strong></a><br>Round the given time value to nearest bucket start value.</p>                                                                                                                 |
| <p><a href="../../configuration-reference/functions/now.md"><strong>now()</strong></a><br>Return current time as epoch millis</p>                                                                                                                                                                |
| <p><a href="../../configuration-reference/functions/timezoneHour.md"><strong>timezoneHour(timeZoneId)</strong></a><br>Returns the hour of the time zone offset.</p>                                                                                                                              |
| <p><a href="../../configuration-reference/functions/timezoneMinute.md"><strong>timezoneMinute(timeZoneId)</strong></a><br>Returns the minute of the time zone offset.</p>                                                                                                                        |
| <p><a href="../../configuration-reference/functions/year.md"><strong>year(tsInMillis)</strong></a><br>Returns the year from the given epoch millis in UTC timezone.</p>                                                                                                                          |
| <p><a href="../../configuration-reference/functions/year.md"><strong>year(tsInMillis, timeZoneId)</strong></a><br>Returns the year from the given epoch millis and timezone id.</p>                                                                                                              |
| <p><a href="../../configuration-reference/functions/yearOfWeek.md"><strong>yearOfWeek(tsInMillis)</strong></a><br>Returns the year of the ISO week from the given epoch millis in UTC timezone. Alias <code>yow</code>is also supported.</p>                                                     |
| <p><a href="../../configuration-reference/functions/yearOfWeek.md"><strong>yearOfWeek(tsInMillis, timeZoneId)</strong></a><br>Returns the year of the ISO week from the given epoch millis and timezone id. Alias <code>yow</code>is also supported.</p>                                         |
| <p><a href="../../configuration-reference/functions/quarter.md"><strong>quarter(tsInMillis)</strong></a><br>Returns the quarter of the year from the given epoch millis in UTC timezone. The value ranges from 1 to 4.</p>                                                                       |
| <p><a href="../../configuration-reference/functions/quarter.md"><strong>quarter(tsInMillis, timeZoneId)</strong></a><br>Returns the quarter of the year from the given epoch millis and timezone id. The value ranges from 1 to 4.</p>                                                           |
| <p><a href="../../configuration-reference/functions/month.md"><strong>month(tsInMillis)</strong></a><br>Returns the month of the year from the given epoch millis in UTC timezone. The value ranges from 1 to 12.</p>                                                                            |
| <p><a href="../../configuration-reference/functions/month.md"><strong>month(tsInMillis, timeZoneId)</strong></a><br>Returns the month of the year from the given epoch millis and timezone id. The value ranges from 1 to 12.</p>                                                                |
| <p><a href="../../configuration-reference/functions/week.md"><strong>week(tsInMillis)</strong></a><br>Returns the ISO week of the year from the given epoch millis in UTC timezone. The value ranges from 1 to 53. Alias <code>weekOfYear</code> is also supported.</p>                          |
| <p><a href="../../configuration-reference/functions/week.md"><strong>week(tsInMillis, timeZoneId)</strong></a><br>Returns the ISO week of the year from the given epoch millis and timezone id. The value ranges from 1 to 5</p>                                                                 |
| <p><a href="../../configuration-reference/functions/dayofyear.md"><strong>dayOfYear(tsInMillis)</strong></a><br>Returns the day of the year from the given epoch millis in UTC timezone. The value ranges from 1 to 366. Alias <code>doy</code> is also supported.</p>                           |
| <p><a href="../../configuration-reference/functions/dayofyear.md"><strong>dayOfYear(tsInMillis, timeZoneId)</strong></a><br>Returns the day of the year from the given epoch millis and timezone id. The value ranges from 1 to 366. Alias <code>doy</code> is also supported.</p>               |
| <p><a href="../../configuration-reference/functions/day.md"><strong>day(tsInMillis)</strong></a><br>Returns the day of the month from the given epoch millis in UTC timezone. The value ranges from 1 to 31. Alias <code>dayOfMonth</code> is also supported.</p>                                |
| <p><a href="../../configuration-reference/functions/day.md"><strong>day(tsInMillis, timeZoneId)</strong></a><br>Returns the day of the month from the given epoch millis and timezone id. The value ranges from 1 to 31. Alias <code>dayOfMonth</code> is also supported.</p>                    |
| <p><a href="../../configuration-reference/functions/dayofweek.md"><strong>dayOfWeek(tsInMillis)</strong></a><br>Returns the day of the week from the given epoch millis in UTC timezone. The value ranges from 1(Monday) to 7(Sunday). Alias <code>dow</code> is also supported.</p>             |
| <p><a href="../../configuration-reference/functions/dayofweek.md"><strong>dayOfWeek(tsInMillis, timeZoneId)</strong></a><br>Returns the day of the week from the given epoch millis and timezone id. The value ranges from 1(Monday) to 7(Sunday). Alias <code>dow</code> is also supported.</p> |
| <p><a href="../../configuration-reference/functions/hour.md"><strong>hour(tsInMillis)</strong></a><br>Returns the hour of the day from the given epoch millis in UTC timezone. The value ranges from 0 to 23.</p>                                                                                |
| <p><a href="../../configuration-reference/functions/hour.md"><strong>hour(tsInMillis, timeZoneId)</strong></a><br>Returns the hour of the day from the given epoch millis and timezone id. The value ranges from 0 to 23.</p>                                                                    |
| <p><a href="../../configuration-reference/functions/minute.md"><strong>minute(tsInMillis)</strong></a><br>Returns the minute of the hour from the given epoch millis in UTC timezone. The value ranges from 0 to 59.</p>                                                                         |
| <p><a href="../../configuration-reference/functions/minute.md"><strong>minute(tsInMillis, timeZoneId)</strong></a><br>Returns the minute of the hour from the given epoch millis and timezone id. The value ranges from 0 to 59.</p>                                                             |
| <p><a href="../../configuration-reference/functions/second.md"><strong>second(tsInMillis)</strong></a><br>Returns the second of the minute from the given epoch millis in UTC timezone. The value ranges from 0 to 59.</p>                                                                       |
| <p><a href="../../configuration-reference/functions/second.md"><strong>second(tsInMillis, timeZoneId)</strong></a><br>Returns the second of the minute from the given epoch millis and timezone id. The value ranges from 0 to 59.</p>                                                           |
| <p><a href="../../configuration-reference/functions/millisecond.md"><strong>millisecond(tsInMillis)</strong></a><br>Returns the millisecond of the second from the given epoch millis in UTC timezone. The value ranges from 0 to 999.</p>                                                       |
| <p><a href="../../configuration-reference/functions/millisecond.md"><strong>millisecond(tsInMillis, timeZoneId)</strong></a><br>Returns the millisecond of the second from the given epoch millis and timezone id. The value ranges from 0 to 999.</p>                                           |

## JSON Functions

### **Transform Functions**

These functions can only be used in Pinot SQL queries.

| Function                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><a href="../../configuration-reference/functions/jsonextractscalar.md"><strong>JSONEXTRACTSCALAR(jsonField, 'jsonPath', 'resultsType', [defaultValue])</strong></a><br>Evaluates the <code>'jsonPath'</code> on <code>jsonField</code>, returns the result as the type <code>'resultsType'</code>, use optional <code>defaultValue</code>for null or parsing error.</p> |
| <p><a href="../../configuration-reference/functions/jsonextractkey.md"><strong>JSONEXTRACTKEY</strong></a><a href="../../configuration-reference/functions/jsonextractkey.md"><strong>(</strong>jsonField, 'jsonPath'<strong>)</strong></a><br>Extracts all matched JSON field keys based on <code>'jsonPath'</code> into a <code>STRING_ARRAY.</code></p>                 |

### **Scalar Functions**

These functions can be used for column transformation in table ingestion configs.

| Function                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><strong>TOJSONMAPSTR</strong>(map)<br>Convert map to JSON String</p>                                                                                                                                                                                                                                                                  |
| <p><strong>JSONFORMAT</strong>(object)<br>Convert object to JSON String</p>                                                                                                                                                                                                                                                              |
| <p><strong>JSONPATH</strong>(jsonField, 'jsonPath')<br>Extracts the object value from <code>jsonField</code> based on <code>'jsonPath'</code>, the result type is inferred based on JSON value. <strong>Cannot be used in query because data type is not specified.</strong></p>                                                         |
| <p><strong>JSONPATHLONG</strong>(jsonField, 'jsonPath', [defaultValue])<br>Extracts the <strong>Long</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.</p>                                                                                   |
| <p><strong>JSONPATHDOUBLE</strong>(jsonField, 'jsonPath', [defaultValue])<br>Extracts the <strong>Double</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.</p>                                                                               |
| <p><strong>JSONPATHSTRING</strong>(jsonField, 'jsonPath', [defaultValue])<br>Extracts the <strong>String</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.</p>                                                                               |
| <p><strong>JSONPATHARRAY</strong>(jsonField, 'jsonPath')<br>Extracts an array from <code>jsonField</code> based on <code>'jsonPath'</code>, the result type is inferred based on JSON value. <strong>Cannot be used in query because data type is not specified.</strong></p>                                                            |
| <p><strong>JSONPATHARRAYDEFAULTEMPTY</strong>(jsonField, 'jsonPath')<br>Extracts an array from <code>jsonField</code> based on <code>'jsonPath'</code>, the result type is inferred based on JSON value. Returns empty array for null or parsing error. <strong>Cannot be used in query because data type is not specified.</strong></p> |

**Usage**

|                  |                                                                                                                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`Arguments`**  | **Description**                                                                                                                                                                                                                                   |
| `jsonField`      | An **Identifier**/**Expression** contains JSON documents.                                                                                                                                                                                         |
| `'jsonPath'`     | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.                                                                                                                                            |
| `'results_type'` | <p>One of the Pinot supported data types:<strong><code>INT, LONG, FLOAT, DOUBLE, BOOLEAN, TIMESTAMP, STRING,</code></strong></p><p><strong><code>INT_ARRAY, LONG_ARRAY, FLOAT_ARRAY, DOUBLE_ARRAY, STRING_ARRAY</code></strong><code>.</code></p> |

{% hint style="warning" %}
**`'jsonPath'`**` and`` `` `**`'results_type'`are literals.** Pinot uses single quotes to distinguish them from **identifiers**.

e.g.

* `JSONEXTRACTSCALAR(profile_json_str, '$.name', 'STRING')` is v**alid**.
* `JSONEXTRACTSCALAR(profile_json_str, "$.name", "STRING")` is i**nvalid**.
{% endhint %}

**Examples**

The examples below are based on these 3 sample profile JSON documents:

```
{
  "name" : "Bob",
  "age" : 37,
  "gender": "male",
  "location": "San Francisco"
},{
  "name" : "Alice",
  "age" : 25,
  "gender": "female",
  "location": "New York"
},{
  "name" : "Mia",
  "age" : 18,
  "gender": "female",
  "location": "Chicago"
}
```

Query 1: Extract string values from the field 'name'

```
SELECT
    JSONEXTRACTSCALAR(profile_json_str, '$.name', 'STRING')
FROM
    myTable
```

Results are

```
["Bob", "Alice", "Mia"]
```

Query 2: Extract integer values from the field 'age'

```
SELECT
    JSONEXTRACTSCALAR(profile_json_str, '$.age', 'INT')
FROM
    myTable
```

Results are

```
[37, 25, 18]
```

Query 3: Extract Bob's age from the JSON profile.

```
SELECT
    JSONEXTRACTSCALAR(myMapStr,'$.age','INT')
FROM
    myTable
WHERE
    JSONEXTRACTSCALAR(myMapStr,'$.name','STRING') = 'Bob'
```

Results are

```
[37]
```

Query 4: Extract all field keys of JSON profile.

```
SELECT
    JSONEXTRACTKEY(myMapStr,'$.*')
FROM
    myTable
```

Results are

```
["name", "age", "gender", "location"]
```

Another **example** of extracting JSON fields from below JSON record:

```
{
        "name": "Pete",
        "age": 24,
        "subjects": [{
                        "name": "maths",
                        "homework_grades": [80, 85, 90, 95, 100],
                        "grade": "A",
                        "score": 90
                },
                {
                        "name": "english",
                        "homework_grades": [60, 65, 70, 85, 90],
                        "grade": "B",
                        "score": 70
                }
        ]
}
```

Extract JSON fields:

| Expression                                                        | Value                  |
| ----------------------------------------------------------------- | ---------------------- |
| `JSONPATH(myJsonRecord, '$.name')`                                | `"Pete"`               |
| `JSONPATH(myJsonRecord, '$.age')`                                 | `24`                   |
| `JSONPATHSTRING(myJsonRecord, '$.age')`                           | `"24"`                 |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].name')`               | `["maths", "english"]` |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].score')`              | `[90, 70]`             |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].homework_grades[1]')` | `[85, 65]`             |

## Binary Functions

| Function             | Description                                                        | Example           |
| -------------------- | ------------------------------------------------------------------ | ----------------- |
| **SHA(bytesCol)**    | Return SHA-1 digest of binary column(`bytes` type) as hex string   | `SHA(rawData)`    |
| **SHA256(bytesCol)** | Return SHA-256 digest of binary column(`bytes` type) as hex string | `SHA256(rawData)` |
| **SHA512(bytesCol)** | Return SHA-512 digest of binary column(`bytes` type) as hex string | `SHA512(rawData)` |
| **MD5(bytesCol)**    | Return MD5 digest of binary column(`bytes` type) as hex string     | `MD5(rawData)`    |

## Multi-value Column Functions

All of the functions mentioned till now only support single value columns. You can use the following functions to do operations on multi-value columns.

| Function        | Description                                                                                                                                                                                                                                                                                                                                                                     | Example                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **ARRAYLENGTH** | Returns the length of a multi-value column                                                                                                                                                                                                                                                                                                                                      |                                              |
| **MAP\_VALUE**  | Select the value for a key from Map stored in Pinot.                                                                                                                                                                                                                                                                                                                            | `MAP_VALUE(mapColumn, 'myKey', valueColumn)` |
| [**VALUEIN**](../../configuration-reference/functions/valuein.md)     | Takes at least 2 arguments, where the first argument is a multi-valued column, and the following arguments are constant values. The transform function will filter the value from the multi-valued column with the given constant values. The `VALUEIN` transform function is especially useful when the same multi-valued column is both filtering column and grouping column. | `VALUEIN(mvColumn, 3, 5, 15)`                |

## Advanced Queries

### Geospatial Queries

Pinot supports Geospatial queries on columns containing text-based geographies. For more details on the queries and how to enable them, see [Geospatial](../../basics/indexing/geospatial-support.md).

### Text Queries

Pinot supports pattern matching on text-based columns. Only the columns mentioned as text columns in table config can be queried using this method. For more details on how to enable pattern matching, see [Text search support](../../basics/indexing/text-search-support.md).
