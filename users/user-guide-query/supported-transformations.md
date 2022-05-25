---
description: >-
  This document contains the list of all the transformation functions supported
  by Pinot SQL.
---

# Transformation Functions

## Math Functions

| Function                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><a href="../../configuration-reference/functions/add.md"><strong>ADD(col1, col2, col3...)</strong></a><br>Sum of at least two values</p>       |
| <p><a href="../../configuration-reference/functions/sub.md"><strong>SUB(col1, col2)</strong></a><br>Difference between two values</p>             |
| <p><a href="../../configuration-reference/functions/mult.md"><strong>MULT(col1, col2, col3...)</strong></a><br>Product of at least two values</p> |
| <p><a href="../../configuration-reference/functions/div.md"><strong>DIV(col1, col2)</strong></a><br>Quotient of two values</p>                    |
| <p><a href="../../configuration-reference/functions/mod.md"><strong>MOD(col1, col2)</strong></a><br>Modulo of two values</p>                      |
| <p><a href="../../configuration-reference/functions/abs.md"><strong>ABS(col1)</strong></a><br>Absolute of a value</p>                             |
| <p><a href="../../configuration-reference/functions/ceil.md#signature"><strong>CEIL(col1)</strong></a><br>Rounded up to the nearest integer.</p>  |
| <p><a href="../../configuration-reference/functions/floor.md"><strong>FLOOR(col1)</strong></a><br>Rounded down to the nearest integer.</p>        |
| <p><a href="../../configuration-reference/functions/exp.md"><strong>EXP(col1)</strong></a><br>Euler’s number(e) raised to the power of col.</p>   |
| <p><a href="../../configuration-reference/functions/ln.md"><strong>LN(col1)</strong></a><br>Natural log of value i.e. ln(col1)</p>                |
| <p><a href="../../configuration-reference/functions/sqrt.md"><strong>SQRT(col1)</strong></a><br>Square root of a value</p>                        |

## String Functions

Multiple string functions are supported out of the box from release-0.5.0 .

| Function                                                                                                                                                                                                                                                                         |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
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
| <p><a href="../../configuration-reference/functions/regexpextract.md"><strong>regexpExtract(value, regexp)</strong></a><br>Extracts values that match the provided regular expression</p>                                                                                        |
| <p><a href="../../configuration-reference/functions/remove.md"><strong>remove(input, search)</strong></a><br>removes all instances of search from string</p>                                                                                                                     |
| <p><a href="../../configuration-reference/functions/url.md"><strong>urlEncoding(string)</strong></a><br>url-encode a string with UTF-8 format</p>                                                                                                                                |
| <p><a href="../../configuration-reference/functions/url.md"><strong>urlDecoding(string)</strong></a><br>decode a url to plaintext string</p>                                                                                                                                     |

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
| <p><a href="../../configuration-reference/functions/week.md"><strong>week(tsInMillis, timeZoneId)</strong></a><br>Returns the ISO week of the year from the given epoch millis and timezone id. The value ranges from 1 to 53. Alias <code>weekOfYear</code> is also supported.</p>              |
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

| Function                                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><a href="../../configuration-reference/functions/tojsonmapstr.md"><strong>TOJSONMAPSTR</strong>(map)<br>Convert map to JSON String</p>                                                                                                                                                                                                                                                                            |
| <p><a href="../../configuration-reference/functions/jsonformat.md"><strong>JSONFORMAT</strong>(object)</a><br>Convert object to JSON String</p>                                                                                                                                                                                                                                                                        |
| <p><a href="../../configuration-reference/functions/jsonpath.md"><strong>JSONPATH(jsonField, 'jsonPath')</strong></a><br>Extracts the object value from <code>jsonField</code> based on <code>'jsonPath'</code>, the result type is inferred based on JSON value. <strong>Cannot be used in query because data type is not specified.</strong></p> |
| <p><a href="../../configuration-reference/functions/jsonpathlong.md"><strong>JSONPATHLONG</strong>(jsonField, 'jsonPath', [defaultValue])</a><br>Extracts the <strong>Long</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.</p>                                                                                             |
| <p><a href="../../configuration-reference/functions/jsonpathdouble.md"><strong>JSONPATHDOUBLE</strong>(jsonField, 'jsonPath', [defaultValue])</a><br>Extracts the <strong>Double</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.</p>                                                                                         |
| <p><a href="../../configuration-reference/functions/jsonpathstring.md"><strong>JSONPATHSTRING(jsonField, 'jsonPath', [defaultValue])</strong></a><br>Extracts the <strong>String</strong> value from <code>jsonField</code> based on <code>'jsonPath'</code>, use optional <code>defaultValue</code>for null or parsing error.</p>                 |
| <p><a href="../../configuration-reference/functions/jsonpatharray.md"><strong>JSONPATHARRAY</strong>(jsonField, 'jsonPath')</a><br>Extracts an array from <code>jsonField</code> based on <code>'jsonPath'</code>, the result type is inferred based on JSON value. <strong>Cannot be used in query because data type is not specified.</strong></p>                                                                      |
| <p><a href="../../configuration-reference/functions/jsonpatharraydefaultempty.md"><strong>JSONPATHARRAYDEFAULTEMPTY</strong>(jsonField, 'jsonPath')</a><br>Extracts an array from <code>jsonField</code> based on <code>'jsonPath'</code>, the result type is inferred based on JSON value. Returns empty array for null or parsing error. <strong>Cannot be used in query because data type is not specified.</strong></p>           |


## Binary Functions

| Function                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><a href="../../configuration-reference/functions/sha.md"><strong>SHA(bytesCol)</strong></a><br>Return SHA-1 digest of binary column(<code>bytes</code> type) as hex string</p>         |
| <p><a href="../../configuration-reference/functions/sha256.md"><strong>SHA256(bytesCol)</strong></a><br>Return SHA-256 digest of binary column(<code>bytes</code> type) as hex string</p> |
| <p><a href="../../configuration-reference/functions/sha512.md"><strong>SHA512(bytesCol)</strong></a><br>Return SHA-512 digest of binary column(<code>bytes</code> type) as hex string</p> |
| <p><a href="../../configuration-reference/functions/md5.md"><strong>MD5(bytesCol)</strong></a><br>Return MD5 digest of binary column(<code>bytes</code> type) as hex string</p>           |

## Multi-value Column Functions

All of the functions mentioned till now only support single value columns. You can use the following functions to do operations on multi-value columns.

| Function                                                                                                                                                                                                                                                                                                                                                       |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <p><a href="../../configuration-reference/functions/arraylength.md"><strong>ARRAYLENGTH</strong></a><br>Returns the length of a multi-value</p>                                                                                                                                                                                                                |
| <p><strong>MAP_VALUE</strong><br>Select the value for a key from Map stored in Pinot.<br><code>MAP_VALUE(mapColumn, 'myKey', valueColumn)</code></p>                                                                                                                                                                                                           |
| <p><a href="../../configuration-reference/functions/valuein.md"><strong>VALUEIN</strong></a><br>The transform function will filter the value from the multi-valued column with the given constant values. The <code>VALUEIN</code> transform function is especially useful when the same multi-valued column is both filtering column and grouping column.</p> |

## Advanced Queries

### Geospatial Queries

Pinot supports Geospatial queries on columns containing text-based geographies. For more details on the queries and how to enable them, see [Geospatial](../../basics/indexing/geospatial-support.md).

### Text Queries

Pinot supports pattern matching on text-based columns. Only the columns mentioned as text columns in table config can be queried using this method. For more details on how to enable pattern matching, see [Text search support](../../basics/indexing/text-search-support.md).
