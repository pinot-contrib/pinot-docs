# Function Index

This page provides a comprehensive A-Z reference of the most commonly used functions in Apache Pinot, organized by category. Each category section links to its detailed documentation page with full syntax, parameters, and examples.

Functions are available in the **Single-Stage Engine (SSE)**, the **Multi-Stage Engine (MSE)**, or **both**. Window functions require the multi-stage engine.

---

## Aggregation Functions

For full details, see [Aggregation Functions](../../functions/aggregation/README.md).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`COUNT`](../../functions/aggregation/count.md) | `COUNT(*)` or `COUNT(col)` | LONG | Counts the number of rows | Both |
| [`MIN`](../../functions/aggregation/min.md) | `MIN(col)` | DOUBLE | Returns the minimum value | Both |
| [`MAX`](../../functions/aggregation/max.md) | `MAX(col)` | DOUBLE | Returns the maximum value | Both |
| [`SUM`](../../functions/aggregation/sum.md) | `SUM(col)` | DOUBLE | Returns the sum of values | Both |
| [`AVG`](../../functions/aggregation/avg.md) | `AVG(col)` | DOUBLE | Returns the average of values | Both |
| [`MODE`](../../functions/aggregation/mode.md) | `MODE(col)` | DOUBLE | Returns the most frequent value | Both |
| [`MINMAXRANGE`](../../functions/aggregation/minmaxrange.md) | `MINMAXRANGE(col)` | DOUBLE | Returns the range (max - min) | Both |
| [`DISTINCTCOUNT`](../../functions/aggregation/distinctcount.md) | `DISTINCTCOUNT(col)` | INT | Returns the exact distinct count | Both |
| [`DISTINCTCOUNTHLL`](../../functions/aggregation/distinctcounthll.md) | `DISTINCTCOUNTHLL(col [, log2m])` | LONG | Approximate distinct count using HyperLogLog | Both |
| [`DISTINCTCOUNTHLLPLUS`](../../functions/sketch/distinctcounthllplus.md) | `DISTINCTCOUNTHLLPLUS(col [, p])` | LONG | Approximate distinct count using HyperLogLog++ | Both |
| [`DISTINCTCOUNTSMARTHLLPLUS`](../../functions/sketch/distinctcounthllplus.md#distinctcountsmarthllplus) | `DISTINCTCOUNTSMARTHLLPLUS(col [, params])` | LONG | Exact-then-approximate distinct count that switches to HLL++ after a threshold | Both |
| [`DISTINCTCOUNTBITMAP`](../../functions/aggregation/distinctcountbitmap.md) | `DISTINCTCOUNTBITMAP(col)` | INT | Distinct count using bitmap | Both |
| [`DISTINCTCOUNTTHETASKETCH`](../../functions/aggregation/distinctcountthetasketch.md) | `DISTINCTCOUNTTHETASKETCH(col [, predicates...])` | LONG | Distinct count using Theta Sketch | Both |
| [`DISTINCTCOUNTCPCSKETCH`](../../functions/sketch/distinctcountcpcsketch.md) | `DISTINCTCOUNTCPCSKETCH(col [, lgK])` | LONG | Distinct count using CPC Sketch | Both |
| [`DISTINCTCOUNTULL`](../../functions/sketch/distinctcountull.md) | `DISTINCTCOUNTULL(col [, p])` | LONG | Distinct count using UltraLogLog | Both |
| [`DISTINCTSUM`](../../functions/aggregation/distinctsum.md) | `DISTINCTSUM(col)` | DOUBLE | Sum of distinct values | Both |
| [`DISTINCTAVG`](../../functions/aggregation/distinctavg.md) | `DISTINCTAVG(col)` | DOUBLE | Average of distinct values | Both |
| [`SEGMENTPARTITIONEDDISTINCTCOUNT`](../../functions/aggregation/segmentpartitioneddistinctcount.md) | `SEGMENTPARTITIONEDDISTINCTCOUNT(col)` | LONG | Optimized distinct count for partitioned columns | Both |
| [`PERCENTILE`](../../functions/aggregation/percentile.md) | `PERCENTILE(col, pct)` | DOUBLE | Exact percentile value | Both |
| [`PERCENTILEEST`](../../functions/aggregation/percentileest.md) | `PERCENTILEEST(col, pct)` | LONG | Estimated percentile using Quantile Digest | Both |
| [`PERCENTILETDIGEST`](../../functions/aggregation/percentiletdigest.md) | `PERCENTILETDIGEST(col, pct)` | DOUBLE | Estimated percentile using T-Digest | Both |
| [`PERCENTILEKLL`](../../functions/aggregation/percentilekll.md) | `PERCENTILEKLL(col, pct)` | DOUBLE | Estimated percentile using KLL Sketch | Both |
| [`HISTOGRAM`](../../functions/aggregation/histogram.md) | `HISTOGRAM(col, binEdges...)` | DOUBLE[] | Computes histogram over bin edges | Both |
| [`COVARPOP`](../../functions/statistical/covar_pop.md) | `COVARPOP(col1, col2)` | DOUBLE | Population covariance | Both |
| [`COVARSAMP`](../../functions/statistical/covar_samp.md) | `COVARSAMP(col1, col2)` | DOUBLE | Sample covariance | Both |
| [`VARPOP`](../../functions/statistical/varpop.md) | `VARPOP(col)` | DOUBLE | Population variance | Both |
| [`VARSAMP`](../../functions/statistical/varsamp.md) | `VARSAMP(col)` | DOUBLE | Sample variance | Both |
| [`STDDEVPOP`](../../functions/statistical/stddevpop.md) | `STDDEVPOP(col)` | DOUBLE | Population standard deviation | Both |
| [`STDDEVSAMP`](../../functions/statistical/stddevsamp.md) | `STDDEVSAMP(col)` | DOUBLE | Sample standard deviation | Both |
| [`SKEWNESS`](../../functions/aggregation/skewness.md) | `SKEWNESS(col)` | DOUBLE | Skewness of values | Both |
| [`KURTOSIS`](../../functions/aggregation/kurtosis.md) | `KURTOSIS(col)` | DOUBLE | Kurtosis of values | Both |
| [`FIRSTWITHTIME`](../../functions/aggregation/firstwithtime.md) | `FIRSTWITHTIME(dataCol, timeCol, 'type')` | varies | Value associated with the earliest timestamp | Both |
| [`LASTWITHTIME`](../../functions/aggregation/lastwithtime.md) | `LASTWITHTIME(dataCol, timeCol, 'type')` | varies | Value associated with the latest timestamp | Both |
| [`ANYVALUE`](../../functions/aggregation/anyvalue.md) | `ANYVALUE(col)` | varies | Returns any arbitrary value from the group | Both |
| [`BOOLAND`](../../functions/aggregation/booland.md) | `BOOLAND(col)` | BOOLEAN | Logical AND across all values | Both |
| [`BOOLOR`](../../functions/aggregation/boolor.md) | `BOOLOR(col)` | BOOLEAN | Logical OR across all values | Both |
| [`EXPRMIN`](../../functions/aggregation/exprmin.md) | `EXPRMIN(measureCol, exprCol1, ...)` | varies | Columns at the row with minimum measure | Both |
| [`EXPRMAX`](../../functions/aggregation/exprmax.md) | `EXPRMAX(measureCol, exprCol1, ...)` | varies | Columns at the row with maximum measure | Both |
| [`FREQUENTSTRINGSSKETCH`](../../functions/sketch/frequentstringssketch.md) | `FREQUENTSTRINGSSKETCH(col, maxMapSize)` | STRING | Frequent items sketch for strings | Both |
| [`FREQUENTLONGSSKETCH`](../../functions/sketch/frequentlongssketch.md) | `FREQUENTLONGSSKETCH(col, maxMapSize)` | STRING | Frequent items sketch for longs | Both |
| [`FUNNELCOUNT`](../../functions/funnel/funnelcount.md) | `FUNNELCOUNT(stepCol, corCol, settings, step1, step2, ...)` | LONG[] | Funnel step counts | Both |
| [`FUNNELMAXSTEP`](../../functions/funnel/funnelmaxstep.md) | `FUNNELMAXSTEP(stepCol, corCol, settings, step1, step2, ...)` | INT | Maximum funnel step reached | Both |
| [`FUNNELCOMPLETECOUNT`](../../functions/funnel/funnelcompletecount.md) | `FUNNELCOMPLETECOUNT(stepCol, corCol, settings, step1, step2, ...)` | INT | Count of completed funnels | Both |
| [`FUNNELSTEPDURATIONSTATS`](../../functions/aggregation/funnelstepdurationstats.md) | `FUNNELSTEPDURATIONSTATS(stepCol, corCol, tsCol, settings, step1, step2, ...)` | STRING | Step duration statistics | Both |
| [`DISTINCTSUM`](../../functions/aggregation/distinctsum.md) | `DISTINCTSUM(col)` | DOUBLE | Sum of distinct values | Both |
| [`DISTINCTAVG`](../../functions/aggregation/distinctavg.md) | `DISTINCTAVG(col)` | DOUBLE | Average of distinct values | Both |
| [`SUMPRECISION`](../../functions/aggregation/sumprecision.md) | `SUMPRECISION(col [, precision])` | STRING | High-precision sum using BigDecimal | Both |
| [`ARRAYAGG`](../../functions/aggregation/arrayagg.md) | `ARRAYAGG(col, 'type' [, distinct])` | ARRAY | Aggregates values into an array | Both |
| [`LISTAGG`](../../functions/aggregation/listagg.md) | `LISTAGG(col [, delimiter])` | STRING | Aggregates values into delimited string | Both |
| [`SUMARRAYLONG`](../../functions/aggregation/sumarraylong.md) | `SUMARRAYLONG(arrCol)` | LONG[] | Element-wise sum of long arrays | Both |
| [`SUMARRAYDOUBLE`](../../functions/aggregation/sumarraydouble.md) | `SUMARRAYDOUBLE(arrCol)` | DOUBLE[] | Element-wise sum of double arrays | Both |

---

## String Functions

For full details, see [String Functions](../../functions/string/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`UPPER`](../../functions/string/upper.md) | `UPPER(str)` | STRING | Converts string to uppercase | Both |
| [`LOWER`](../../functions/string/lower.md) | `LOWER(str)` | STRING | Converts string to lowercase | Both |
| [`INITCAP`](../../functions/string/initcap.md) | `INITCAP(str)` | STRING | Capitalizes first letter of each word | Both |
| [`REVERSE`](../../functions/string/reverse.md) | `REVERSE(str)` | STRING | Reverses the string | Both |
| [`SUBSTR`](../../functions/string/substr.md) | `SUBSTR(str, start [, end])` | STRING | Extracts substring by start/end position | Both |
| `SUBSTRING` | `SUBSTRING(str, start [, length])` | STRING | Extracts substring by start position and length | Both |
| `LEFT` | `LEFT(str, length)` | STRING | Returns leftmost N characters | Both |
| `RIGHT` | `RIGHT(str, length)` | STRING | Returns rightmost N characters | Both |
| [`CONCAT`](../../functions/string/concat.md) | `CONCAT(str1, str2)` | STRING | Concatenates two strings | Both |
| [`TRIM`](../../functions/string/trim.md) | `TRIM(str)` | STRING | Removes leading and trailing whitespace | Both |
| [`LTRIM`](../../functions/string/ltrim.md) | `LTRIM(str)` | STRING | Removes leading whitespace | Both |
| [`RTRIM`](../../functions/string/rtrim.md) | `RTRIM(str)` | STRING | Removes trailing whitespace | Both |
| [`LPAD`](../../functions/string/lpad.md) | `LPAD(str, size, pad)` | STRING | Left-pads string to specified size | Both |
| [`RPAD`](../../functions/string/rpad.md) | `RPAD(str, size, pad)` | STRING | Right-pads string to specified size | Both |
| [`LENGTH`](../../functions/string/length.md) | `LENGTH(str)` | INT | Returns the length of the string | Both |
| [`STRPOS`](../../functions/string/strpos.md) | `STRPOS(str, find [, instance])` | INT | Returns position of substring | Both |
| `STRRPOS` | `STRRPOS(str, find [, instance])` | INT | Returns last position of substring | Both |
| [`STARTSWITH`](../../functions/string/startswith.md) | `STARTSWITH(str, prefix)` | BOOLEAN | Checks if string starts with prefix | Both |
| `ENDSWITH` | `ENDSWITH(str, suffix)` | BOOLEAN | Checks if string ends with suffix | Both |
| `CONTAINS` | `CONTAINS(str, substring)` | BOOLEAN | Checks if string contains substring | Both |
| [`REPLACE`](../../functions/string/replace.md) | `REPLACE(str, target, replacement)` | STRING | Replaces occurrences of target | Both |
| [`REMOVE`](../../functions/string/remove.md) | `REMOVE(str, search)` | STRING | Removes all occurrences of search string | Both |
| `SPLIT` | `SPLIT(str, delimiter [, limit])` | STRING[] | Splits string by delimiter | Both |
| [`SPLITPART`](../../functions/string/splitpart.md) | `SPLITPART(str, delimiter, index)` or `SPLITPART(str, delimiter, limit, index)` | STRING | Returns the selected element after splitting; negative indices count from the end | Both |
| `REPEAT` | `REPEAT(str, times)` | STRING | Repeats string N times | Both |
| [`REGEXP_EXTRACT`](../../functions/string/regexpextract.md) | `REGEXP_EXTRACT(str, pattern [, group])` | STRING | Extracts regex match from string | Both |
| [`CHR`](../../functions/string/chr.md) | `CHR(codepoint)` | STRING | Returns character for Unicode code point | Both |
| [`CODEPOINT`](../../functions/string/codepoint.md) | `CODEPOINT(str)` | INT | Returns Unicode code point of first character | Both |
| `NORMALIZE` | `NORMALIZE(str [, form])` | STRING | Normalizes Unicode string | Both |
| `STRCMP` | `STRCMP(str1, str2)` | INT | Compares two strings lexicographically | Both |
| `HAMMINGDISTANCE` | `HAMMINGDISTANCE(str1, str2)` | INT | Hamming distance between two strings | Both |
| [`LEVENSTEINDISTANCE`](../../functions/string/levenshtein_distance.md) | `LEVENSTEINDISTANCE(str1, str2)` | INT | Levenshtein edit distance | Both |

---

## Math Functions

For full details, see [Math Functions](../../functions/math/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`ABS`](../../functions/math/abs.md) | `ABS(val)` | DOUBLE | Absolute value | Both |
| `CEIL` / `CEILING` | `CEIL(val)` | DOUBLE | Rounds up to nearest integer | Both |
| [`FLOOR`](../../functions/math/floor.md) | `FLOOR(val)` | DOUBLE | Rounds down to nearest integer | Both |
| [`EXP`](../../functions/math/exp.md) | `EXP(val)` | DOUBLE | Euler's number raised to the power | Both |
| `LN` / `LOG` | `LN(val)` | DOUBLE | Natural logarithm | Both |
| `LOG2` | `LOG2(val)` | DOUBLE | Base-2 logarithm | Both |
| `LOG10` | `LOG10(val)` | DOUBLE | Base-10 logarithm | Both |
| [`SQRT`](../../functions/math/sqrt.md) | `SQRT(val)` | DOUBLE | Square root | Both |
| `SIGN` | `SIGN(val)` | DOUBLE | Sign of a number (-1, 0, 1) | Both |
| `POW` / `POWER` | `POW(base, exp)` | DOUBLE | Raises base to exponent | Both |
| [`MOD`](../../functions/math/mod.md) | `MOD(a, b)` | DOUBLE | Modulo operation | Both |
| `ROUNDDECIMAL` | `ROUNDDECIMAL(val [, scale])` | DOUBLE | Rounds to specified decimal places | Both |
| `TRUNCATE` | `TRUNCATE(val [, scale])` | DOUBLE | Truncates to specified decimal places | Both |
| `DIV` / `DIVIDE` | `DIV(a, b [, default])` | DOUBLE | Division with optional default for divide-by-zero | Both |
| `INTDIV` | `INTDIV(a, b)` | LONG | Integer division | Both |
| `LEAST` | `LEAST(a, b)` | DOUBLE | Returns the smaller of two values | Both |
| `GREATEST` | `GREATEST(a, b)` | DOUBLE | Returns the larger of two values | Both |
| `GCD` | `GCD(a, b)` | LONG | Greatest common divisor | Both |
| `LCM` | `LCM(a, b)` | LONG | Least common multiple | Both |
| `HYPOT` | `HYPOT(a, b)` | DOUBLE | Hypotenuse (sqrt(a^2 + b^2)) | Both |
| `NEGATE` | `NEGATE(val)` | DOUBLE | Negates the value | Both |
| `RAND` | `RAND([seed])` | DOUBLE | Random number between 0 and 1 | Both |
| `SIN` | `SIN(val)` | DOUBLE | Sine | Both |
| `COS` | `COS(val)` | DOUBLE | Cosine | Both |
| `TAN` | `TAN(val)` | DOUBLE | Tangent | Both |
| `COT` | `COT(val)` | DOUBLE | Cotangent | Both |
| `ASIN` | `ASIN(val)` | DOUBLE | Inverse sine | Both |
| `ACOS` | `ACOS(val)` | DOUBLE | Inverse cosine | Both |
| `ATAN` | `ATAN(val)` | DOUBLE | Inverse tangent | Both |
| `ATAN2` | `ATAN2(y, x)` | DOUBLE | Two-argument inverse tangent | Both |
| `DEGREES` | `DEGREES(radians)` | DOUBLE | Converts radians to degrees | Both |
| `RADIANS` | `RADIANS(degrees)` | DOUBLE | Converts degrees to radians | Both |

---

## DateTime Functions

For full details, see [DateTime Functions](../../functions/datetime/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`NOW`](../../functions/datetime/now.md) | `NOW()` | LONG | Current timestamp in milliseconds | Both |
| [`AGO`](../../functions/datetime/ago.md) | `AGO('period')` | LONG | Timestamp for a period in the past | Both |
| [`TODATETIME`](../../functions/datetime/todatetime.md) | `TODATETIME(millis, pattern [, tz])` | STRING | Converts epoch millis to formatted string | Both |
| [`FROMDATETIME`](../../functions/datetime/fromdatetime.md) | `FROMDATETIME(str, pattern [, tz])` | LONG | Parses datetime string to epoch millis | Both |
| [`TOEPOCHSECONDS`](../../functions/datetime/toepoch.md) | `TOEPOCHSECONDS(millis)` | LONG | Converts millis to epoch seconds | Both |
| [`TOEPOCHMINUTES`](../../functions/datetime/toepoch.md) | `TOEPOCHMINUTES(millis)` | LONG | Converts millis to epoch minutes | Both |
| [`TOEPOCHHOURS`](../../functions/datetime/toepoch.md) | `TOEPOCHHOURS(millis)` | LONG | Converts millis to epoch hours | Both |
| [`TOEPOCHDAYS`](../../functions/datetime/toepoch.md) | `TOEPOCHDAYS(millis)` | LONG | Converts millis to epoch days | Both |
| [`FROMEPOCHSECONDS`](../../functions/datetime/fromepoch.md) | `FROMEPOCHSECONDS(seconds)` | LONG | Converts epoch seconds to millis | Both |
| [`FROMEPOCHMINUTES`](../../functions/datetime/fromepoch.md) | `FROMEPOCHMINUTES(minutes)` | LONG | Converts epoch minutes to millis | Both |
| [`FROMEPOCHHOURS`](../../functions/datetime/fromepoch.md) | `FROMEPOCHHOURS(hours)` | LONG | Converts epoch hours to millis | Both |
| [`FROMEPOCHDAYS`](../../functions/datetime/fromepoch.md) | `FROMEPOCHDAYS(days)` | LONG | Converts epoch days to millis | Both |
| [`TOEPOCHSECONDSROUNDED`](../../functions/datetime/toepochrounded.md) | `TOEPOCHSECONDSROUNDED(millis, roundTo)` | LONG | Converts millis to rounded epoch seconds | Both |
| [`TOEPOCHMINUTESROUNDED`](../../functions/datetime/toepochrounded.md) | `TOEPOCHMINUTESROUNDED(millis, roundTo)` | LONG | Converts millis to rounded epoch minutes | Both |
| [`TOEPOCHHOURSROUNDED`](../../functions/datetime/toepochrounded.md) | `TOEPOCHHOURSROUNDED(millis, roundTo)` | LONG | Converts millis to rounded epoch hours | Both |
| [`TOEPOCHSECONDSBUCKET`](../../functions/datetime/toepochbucket.md) | `TOEPOCHSECONDSBUCKET(millis, bucket)` | LONG | Buckets millis into epoch second intervals | Both |
| [`FROMEPOCHSECONDSBUCKET`](../../functions/datetime/fromepochbucket.md) | `FROMEPOCHSECONDSBUCKET(seconds, bucket)` | LONG | Converts bucketed epoch seconds to millis | Both |
| [`DATETRUNC`](../../functions/datetime/datetrunc.md) | `DATETRUNC(unit, timeVal [, inputUnit [, tz [, outputUnit]]])` | LONG | Truncates timestamp to specified granularity | Both |
| `DATEBIN` | `DATEBIN(binWidth, sourceTs, originTs)` | TIMESTAMP | Bins a timestamp into intervals | Both |
| `TIMESTAMPADD` / `DATEADD` | `TIMESTAMPADD(unit, interval, ts)` | LONG | Adds interval to timestamp | Both |
| `TIMESTAMPDIFF` / `DATEDIFF` | `TIMESTAMPDIFF(unit, ts1, ts2)` | LONG | Difference between two timestamps | Both |
| [`EXTRACT`](../../functions/datetime/extract.md) | `EXTRACT(field FROM ts)` | INT | Extracts date/time field from timestamp | Both |
| [`YEAR`](../../functions/datetime/year.md) | `YEAR(millis [, tz])` | INT | Extracts year | Both |
| [`QUARTER`](../../functions/datetime/quarter.md) | `QUARTER(millis [, tz])` | INT | Extracts quarter (1-4) | Both |
| [`MONTH`](../../functions/datetime/month.md) | `MONTH(millis [, tz])` | INT | Extracts month (1-12) | Both |
| [`WEEK`](../../functions/datetime/week.md) | `WEEK(millis [, tz])` | INT | Extracts ISO week of year | Both |
| [`DAYOFYEAR`](../../functions/datetime/dayofyear.md) | `DAYOFYEAR(millis [, tz])` | INT | Extracts day of year (1-366) | Both |
| `DAYOFMONTH` / `DAY` | `DAYOFMONTH(millis [, tz])` | INT | Extracts day of month (1-31) | Both |
| [`DAYOFWEEK`](../../functions/datetime/dayofweek.md) / `DOW` | `DAYOFWEEK(millis [, tz])` | INT | Extracts day of week (1-7) | Both |
| [`HOUR`](../../functions/datetime/hour.md) | `HOUR(millis [, tz])` | INT | Extracts hour (0-23) | Both |
| [`MINUTE`](../../functions/datetime/minute.md) | `MINUTE(millis [, tz])` | INT | Extracts minute (0-59) | Both |
| [`SECOND`](../../functions/datetime/second.md) | `SECOND(millis [, tz])` | INT | Extracts second (0-59) | Both |
| [`MILLISECOND`](../../functions/datetime/millisecond.md) | `MILLISECOND(millis [, tz])` | INT | Extracts millisecond (0-999) | Both |
| [`YEAROFWEEK`](../../functions/datetime/yearofweek.md) | `YEAROFWEEK(millis [, tz])` | INT | Extracts ISO year-of-week | Both |
| [`TIMEZONEHOUR`](../../functions/datetime/timezonehour.md) | `TIMEZONEHOUR(tzId [, millis])` | INT | UTC offset hours for timezone | Both |
| [`TIMEZONEMINUTE`](../../functions/datetime/timezoneminute.md) | `TIMEZONEMINUTE(tzId [, millis])` | INT | UTC offset minutes for timezone | Both |
| `TOTIMESTAMP` | `TOTIMESTAMP(millis)` | TIMESTAMP | Converts millis to SQL Timestamp | Both |
| `FROMTIMESTAMP` | `FROMTIMESTAMP(ts)` | LONG | Converts SQL Timestamp to millis | Both |
| [`DATETIMECONVERT`](../../functions/datetime/datetimeconvert.md) | `DATETIMECONVERT(col, inFormat, outFormat, granularity)` | STRING/LONG | Converts datetime between formats | Both |

---

## JSON Functions

For full details, see [JSON Functions](../../functions/json/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`JSONPATH`](../../functions/json/jsonpath.md) | `JSONPATH(obj, path)` | OBJECT | Evaluates JSONPath expression | Both |
| [`JSONPATHSTRING`](../../functions/json/jsonpathstring.md) | `JSONPATHSTRING(obj, path [, default])` | STRING | Extracts string via JSONPath | Both |
| [`JSONPATHLONG`](../../functions/json/jsonpathlong.md) | `JSONPATHLONG(obj, path [, default])` | LONG | Extracts long via JSONPath | Both |
| [`JSONPATHDOUBLE`](../../functions/json/jsonpathdouble.md) | `JSONPATHDOUBLE(obj, path [, default])` | DOUBLE | Extracts double via JSONPath | Both |
| [`JSONPATHARRAY`](../../functions/json/jsonpatharray.md) | `JSONPATHARRAY(obj, path)` | OBJECT[] | Extracts array via JSONPath | Both |
| [`JSONPATHARRAYDEFAULTEMPTY`](../../functions/json/jsonpatharraydefaultempty.md) | `JSONPATHARRAYDEFAULTEMPTY(obj, path)` | OBJECT[] | Extracts array, returns empty if null | Both |
| [`JSONPATHEXISTS`](../../functions/json/jsonpathexists.md) | `JSONPATHEXISTS(obj, path)` | BOOLEAN | Checks if JSONPath exists | Both |
| [`JSONKEYVALUEARRAYTOMAP`](../../functions/json/jsonkeyvaluearraytomap.md) | `JSONKEYVALUEARRAYTOMAP(arr [, keyColumnName, valueColumnName])` | MAP | Converts key/value-object array to map | Both |
| [`JSONEXTRACTKEY`](../../functions/json/jsonextractkey.md) | `JSONEXTRACTKEY(obj, path)` | STRING[] | Extracts keys at JSONPath | Both |
| [`JSONEXTRACTSCALAR`](../../functions/json/jsonextractscalar.md) | `JSONEXTRACTSCALAR(json, path, type [, default])` | varies | Extracts scalar value from JSON | Both |
| [`JSONFORMAT`](../../functions/json/jsonformat.md) | `JSONFORMAT(obj)` | STRING | Serializes object to JSON string | Both |
| [`TOJSONMAPSTR`](../../functions/json/tojsonmapstr.md) | `TOJSONMAPSTR(map)` | STRING | Converts map to JSON string | Both |
| `JSONSTRINGTOARRAY` | `JSONSTRINGTOARRAY(jsonStr)` | LIST | Parses JSON string to array | Both |
| `JSONSTRINGTOMAP` | `JSONSTRINGTOMAP(jsonStr)` | MAP | Parses JSON string to map | Both |
| `ISJSON` | `ISJSON(str)` | BOOLEAN | Checks if string is valid JSON | Both |

---

## Array Functions

For full details, see [Array Functions](../../functions/array).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `ARRAY_AGG` | `ARRAY_AGG(col, 'type' [, distinct])` | ARRAY | Aggregates values into an array | Both |
| [`LISTAGG`](../../functions/aggregation/listagg.md) | `LISTAGG(col [, delimiter [, distinct]])` | STRING | Aggregates values into a delimited string | Both |
| [`ARRAYLENGTH`](../../functions/array/arraylength.md) | `ARRAYLENGTH(arr)` | INT | Returns the length of an array | Both |
| [`ARRAYCONTAINSINT`](../../functions/array/arraycontainsint.md) | `ARRAYCONTAINSINT(arr, val)` | BOOLEAN | Checks if integer array contains value | Both |
| [`ARRAYCONTAINSSTRING`](../../functions/array/arraycontainsstring.md) | `ARRAYCONTAINSSTRING(arr, val)` | BOOLEAN | Checks if string array contains value | Both |
| [`ARRAYCONCATINT`](../../functions/array/arrayconcatint.md) | `ARRAYCONCATINT(arr1, arr2)` | INT[] | Concatenates two integer arrays | Both |
| [`ARRAYCONCATSTRING`](../../functions/array/arrayconcatstring.md) | `ARRAYCONCATSTRING(arr1, arr2)` | STRING[] | Concatenates two string arrays | Both |
| [`ARRAYDISTINCTINT`](../../functions/array/arraydistinctint.md) | `ARRAYDISTINCTINT(arr)` | INT[] | Removes duplicates from integer array | Both |
| [`ARRAYDISTINCTSTRING`](../../functions/array/arraydistinctstring.md) | `ARRAYDISTINCTSTRING(arr)` | STRING[] | Removes duplicates from string array | Both |
| [`ARRAYINDEXOFINT`](../../functions/array/arrayindexofint.md) | `ARRAYINDEXOFINT(arr, val)` | INT | Index of value in integer array | Both |
| [`ARRAYINDEXOFSTRING`](../../functions/array/arrayindexofstring.md) | `ARRAYINDEXOFSTRING(arr, val)` | INT | Index of value in string array | Both |
| [`ARRAYPUSHBACKINT`](../../functions/array/arraypushback.md) | `ARRAYPUSHBACKINT(arr, val)` | INT[] | Appends an integer to the end of an array | Both |
| [`ARRAYPUSHBACKLONG`](../../functions/array/arraypushback.md) | `ARRAYPUSHBACKLONG(arr, val)` | LONG[] | Appends a long to the end of an array | Both |
| [`ARRAYPUSHBACKFLOAT`](../../functions/array/arraypushback.md) | `ARRAYPUSHBACKFLOAT(arr, val)` | FLOAT[] | Appends a float to the end of an array | Both |
| [`ARRAYPUSHBACKDOUBLE`](../../functions/array/arraypushback.md) | `ARRAYPUSHBACKDOUBLE(arr, val)` | DOUBLE[] | Appends a double to the end of an array | Both |
| [`ARRAYPUSHBACKSTRING`](../../functions/array/arraypushback.md) | `ARRAYPUSHBACKSTRING(arr, val)` | STRING[] | Appends a string to the end of an array | Both |
| [`ARRAYPUSHFRONTINT`](../../functions/array/arraypushfront.md) | `ARRAYPUSHFRONTINT(arr, val)` | INT[] | Prepends an integer to the beginning of an array | Both |
| [`ARRAYPUSHFRONTLONG`](../../functions/array/arraypushfront.md) | `ARRAYPUSHFRONTLONG(arr, val)` | LONG[] | Prepends a long to the beginning of an array | Both |
| [`ARRAYPUSHFRONTFLOAT`](../../functions/array/arraypushfront.md) | `ARRAYPUSHFRONTFLOAT(arr, val)` | FLOAT[] | Prepends a float to the beginning of an array | Both |
| [`ARRAYPUSHFRONTDOUBLE`](../../functions/array/arraypushfront.md) | `ARRAYPUSHFRONTDOUBLE(arr, val)` | DOUBLE[] | Prepends a double to the beginning of an array | Both |
| [`ARRAYPUSHFRONTSTRING`](../../functions/array/arraypushfront.md) | `ARRAYPUSHFRONTSTRING(arr, val)` | STRING[] | Prepends a string to the beginning of an array | Both |
| [`ARRAYREMOVEINT`](../../functions/array/arrayremoveint.md) | `ARRAYREMOVEINT(arr, val)` | INT[] | Removes first occurrence from integer array | Both |
| [`ARRAYREMOVESTRING`](../../functions/array/arrayremovestring.md) | `ARRAYREMOVESTRING(arr, val)` | STRING[] | Removes first occurrence from string array | Both |
| [`ARRAYREVERSEINT`](../../functions/array/arrayreverseint.md) | `ARRAYREVERSEINT(arr)` | INT[] | Reverses integer array | Both |
| [`ARRAYREVERSESTRING`](../../functions/array/arrayreversestring.md) | `ARRAYREVERSESTRING(arr)` | STRING[] | Reverses string array | Both |
| [`ARRAYSLICEINT`](../../functions/array/arraysliceint.md) | `ARRAYSLICEINT(arr, start, end)` | INT[] | Extracts subarray from integer array | Both |
| [`ARRAYSLICESTRING`](../../functions/array/arrayslicestring.md) | `ARRAYSLICESTRING(arr, start, end)` | STRING[] | Extracts subarray from string array | Both |
| [`ARRAYSORTINT`](../../functions/array/arraysortint.md) | `ARRAYSORTINT(arr)` | INT[] | Sorts integer array ascending | Both |
| [`ARRAYSORTSTRING`](../../functions/array/arraysortstring.md) | `ARRAYSORTSTRING(arr)` | STRING[] | Sorts string array ascending | Both |
| [`ARRAYUNIONINT`](../../functions/array/arrayunionint.md) | `ARRAYUNIONINT(arr1, arr2)` | INT[] | Union of two integer arrays (unique) | Both |
| [`ARRAYUNIONSTRING`](../../functions/array/arrayunionstring.md) | `ARRAYUNIONSTRING(arr1, arr2)` | STRING[] | Union of two string arrays (unique) | Both |
| [`ARRAYS_OVERLAP`](../../functions/array/arraysoverlap.md) | `ARRAYS_OVERLAP(arr1, arr2)` | BOOLEAN | True if same-type arrays share any element | Both |
| `ARRAYSUMINT` | `ARRAYSUMINT(arr)` | INT | Sum of integer array elements | Both |
| `ARRAYSUMLONG` | `ARRAYSUMLONG(arr)` | LONG | Sum of long array elements | Both |
| [`ARRAYTOSTRING`](../../functions/array/arraytostring.md) | `ARRAYTOSTRING(arr, delimiter [, null])` | STRING | Joins string array elements into one string | Both |
| [`SUMARRAYLONG`](../../functions/aggregation/sumarraylong.md) | `SUMARRAYLONG(arrCol)` | LONG | Aggregate: sums all elements across rows | Both |
| [`SUMARRAYDOUBLE`](../../functions/aggregation/sumarraydouble.md) | `SUMARRAYDOUBLE(arrCol)` | DOUBLE | Aggregate: sums all elements across rows | Both |

---

## Hash Functions

For full details, see [Hash Functions](../../functions/hash).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `SHA` | `SHA(bytes)` | STRING | SHA-1 hash | Both |
| `SHA224` | `SHA224(bytes)` | STRING | SHA-224 hash | Both |
| `SHA256` | `SHA256(bytes)` | STRING | SHA-256 hash | Both |
| `SHA512` | `SHA512(bytes)` | STRING | SHA-512 hash | Both |
| `MD2` | `MD2(bytes)` | STRING | MD2 hash | Both |
| `MD5` | `MD5(bytes)` | STRING | MD5 hash | Both |
| `MURMURHASH2` | `MURMURHASH2(bytes)` | INT | 32-bit MurmurHash2 | Both |
| `MURMURHASH2UTF8` | `MURMURHASH2UTF8(str)` | INT | 32-bit MurmurHash2 for strings | Both |
| `MURMURHASH3BIT32` | `MURMURHASH3BIT32(bytes, seed)` | INT | 32-bit MurmurHash3 | Both |
| `MURMURHASH3BIT64` | `MURMURHASH3BIT64(bytes, seed)` | LONG | 64-bit MurmurHash3 | Both |
| `MURMURHASH3BIT128` | `MURMURHASH3BIT128(bytes, seed)` | BYTES | 128-bit MurmurHash3 | Both |
| `CRC32` | `CRC32(bytes)` | INT | 32-bit CRC checksum | Both |
| `CRC32C` | `CRC32C(bytes)` | INT | 32-bit CRC32C (Castagnoli) | Both |
| `ADLER32` | `ADLER32(bytes)` | INT | 32-bit Adler checksum | Both |

---

## URL Functions

For full details, see [URL Functions](../../functions/url).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `URLPROTOCOL` | `URLPROTOCOL(url)` | STRING | Extracts protocol/scheme | Both |
| `URLDOMAIN` | `URLDOMAIN(url)` | STRING | Extracts domain | Both |
| `URLDOMAINWITHOUTWWW` | `URLDOMAINWITHOUTWWW(url)` | STRING | Extracts domain without www prefix | Both |
| `URLTOPLEVELDOMAIN` | `URLTOPLEVELDOMAIN(url)` | STRING | Extracts top-level domain | Both |
| `URLPORT` | `URLPORT(url)` | INT | Extracts port number | Both |
| `URLPATH` | `URLPATH(url)` | STRING | Extracts path component | Both |
| `URLQUERYSTRING` | `URLQUERYSTRING(url)` | STRING | Extracts query string | Both |
| `URLFRAGMENT` | `URLFRAGMENT(url)` | STRING | Extracts fragment identifier | Both |
| `EXTRACTURLPARAMETER` | `EXTRACTURLPARAMETER(url, name)` | STRING | Extracts specific query parameter | Both |
| `EXTRACTURLPARAMETERS` | `EXTRACTURLPARAMETERS(url)` | STRING[] | Extracts all query parameters | Both |
| `URLENCODE` | `URLENCODE(url)` | STRING | URL-encodes a string | Both |
| `URLDECODE` | `URLDECODE(url)` | STRING | Decodes URL-encoded string | Both |
| `CUTWWW` | `CUTWWW(url)` | STRING | Removes www prefix from URL | Both |
| `CUTQUERYSTRING` | `CUTQUERYSTRING(url)` | STRING | Removes query string from URL | Both |
| `CUTFRAGMENT` | `CUTFRAGMENT(url)` | STRING | Removes fragment from URL | Both |
| `CUTURLPARAMETER` | `CUTURLPARAMETER(url, name)` | STRING | Removes specific query parameter | Both |

---

## Binary Functions

For full details, see [Binary Functions](../../functions/binary/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `TOUTF8` | `TOUTF8(str)` | BYTES | Converts string to UTF-8 bytes | Both |
| `FROMUTF8` | `FROMUTF8(bytes)` | STRING | Converts UTF-8 bytes to string | Both |
| `TOASCII` | `TOASCII(str)` | BYTES | Converts string to ASCII bytes | Both |
| `FROMASCII` | `FROMASCII(bytes)` | STRING | Converts ASCII bytes to string | Both |
| `TOBASE64` | `TOBASE64(bytes)` | STRING | Encodes bytes as Base64 string | Both |
| `FROMBASE64` | `FROMBASE64(str)` | BYTES | Decodes Base64 string to bytes | Both |
| `BASE64ENCODE` | `BASE64ENCODE(bytes)` | BYTES | Base64 encodes byte array | Both |
| `BASE64DECODE` | `BASE64DECODE(bytes)` | BYTES | Base64 decodes byte array | Both |
| `HEXTOBYTES` | `HEXTOBYTES(hex)` | BYTES | Converts hex string to bytes | Both |
| `BYTESTOHEX` | `BYTESTOHEX(bytes)` | STRING | Converts bytes to hex string | Both |

---

## Geospatial Functions

For full details, see [GeoSpatial Functions](../../functions/geospatial/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`STPOINT`](../../functions/geospatial/stpoint.md) | `STPOINT(lng, lat)` | BYTES | Creates a geometry point | Both |
| [`STPOLYGON`](../../functions/geospatial/stpolygon.md) | `STPOLYGON(wkt)` | BYTES | Creates a polygon from WKT | Both |
| [`STDISTANCE`](../../functions/geospatial/stdistance.md) | `STDISTANCE(geo1, geo2)` | DOUBLE | Distance between two geometries | Both |
| [`STCONTAINS`](../../functions/geospatial/stcontains.md) | `STCONTAINS(geo1, geo2)` | BOOLEAN | Tests if first geometry contains second | Both |
| [`STGEOMFROMTEXT`](../../functions/geospatial/stgeomfromtext.md) | `STGEOMFROMTEXT(wkt)` | BYTES | Creates geometry from WKT | Both |
| [`STGEOMFROMWKB`](../../functions/geospatial/stgeomfromwkb.md) | `STGEOMFROMWKB(wkb)` | BYTES | Creates geometry from WKB | Both |
| [`STGEOMFROMGEOJSON`](../../functions/geospatial/st_geomfromgeojson.md) | `STGEOMFROMGEOJSON(json)` | BYTES | Creates geometry from GeoJSON | Both |
| [`STGEOGFROMTEXT`](../../functions/geospatial/stgeogfromtext.md) | `STGEOGFROMTEXT(wkt)` | BYTES | Creates geography from WKT | Both |
| [`STGEOGFROMWKB`](../../functions/geospatial/stgeogfromwkb.md) | `STGEOGFROMWKB(wkb)` | BYTES | Creates geography from WKB | Both |
| [`STGEOGFROMGEOJSON`](../../functions/geospatial/st_geogfromgeojson.md) | `STGEOGFROMGEOJSON(json)` | BYTES | Creates geography from GeoJSON | Both |
| [`STASTEXT`](../../functions/geospatial/stastext.md) | `STASTEXT(geo)` | STRING | Converts geometry to WKT | Both |
| [`STASBINARY`](../../functions/geospatial/stasbinary.md) | `STASBINARY(geo)` | BYTES | Converts geometry to WKB | Both |
| [`STASGEOJSON`](../../functions/geospatial/st_asgeojson.md) | `STASGEOJSON(geo)` | STRING | Converts geometry to GeoJSON | Both |
| [`STGEOMETRYTYPE`](../../functions/geospatial/stgeometrytype.md) | `STGEOMETRYTYPE(geo)` | STRING | Returns geometry type | Both |
| [`TOSPHERICALGEOGRAPHY`](../../functions/geospatial/tosphericalgeography.md) | `TOSPHERICALGEOGRAPHY(geo)` | BYTES | Converts geometry to spherical geography | Both |
| [`GridDistance`](../../functions/geospatial/griddistance.md) | `gridDistance(h3Index1, h3Index2)` | LONG | H3 grid distance between two cells | Both |
| [`GridDisk`](../../functions/geospatial/griddisk.md) | `gridDisk(h3Index, k)` | LONG[] | H3 cells within `k` grid steps of a center cell | Both |
| [`IDSET`](../../functions/aggregation/idset.md) | `IDSET(col [, params])` | BYTES | Serialized IdSet for use with IN_ID_SET filter | Both |
| [`STUNION`](../../functions/geospatial/stunion.md) | `STUNION(geoCol)` | BYTES | Aggregation: union of geometries | Both |

---

## Vector / Similarity Functions

For full details, see [Vector Functions](../../functions/vector/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `COSINEDISTANCE` | `COSINEDISTANCE(arr1, arr2)` | DOUBLE | Cosine distance between two vectors | Both |
| `INNERPRODUCT` | `INNERPRODUCT(arr1, arr2)` | DOUBLE | Inner (dot) product of two vectors | Both |
| `L1DISTANCE` | `L1DISTANCE(arr1, arr2)` | DOUBLE | Manhattan distance between two vectors | Both |
| `L2DISTANCE` | `L2DISTANCE(arr1, arr2)` | DOUBLE | Euclidean distance between two vectors | Both |
| `VECTORDIMS` | `VECTORDIMS(arr)` | INT | Number of dimensions in a vector | Both |
| `VECTORNORM` | `VECTORNORM(arr)` | DOUBLE | L2 norm (magnitude) of a vector | Both |

---

## IP Address Functions

For full details, see [IP Address Functions](../../functions/ip-address/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| [`ISSUBNETOF`](../../functions/misc/issubnetof.md) | `ISSUBNETOF(prefix, addr)` | BOOLEAN | Checks if IP address is in subnet | Both |
| `IPPREFIX` | `IPPREFIX(addr, prefixLen)` | STRING | Returns CIDR prefix for IP address | Both |
| `IPSUBNETMIN` | `IPSUBNETMIN(prefix)` | STRING | Returns lowest IP in subnet | Both |
| `IPSUBNETMAX` | `IPSUBNETMAX(prefix)` | STRING | Returns highest IP in subnet | Both |

---

## Null Handling Functions

For full details, see [Null Handling Functions](../../functions/null-handling/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `IS NULL` | `col IS NULL` | BOOLEAN | True if value is null | Both |
| `IS NOT NULL` | `col IS NOT NULL` | BOOLEAN | True if value is not null | Both |
| `COALESCE` | `COALESCE(val1, val2, ...)` | varies | Returns first non-null value | Both |
| `NULLIF` | `NULLIF(val1, val2)` | varies | Returns null if values are equal | Both |
| `IS DISTINCT FROM` | `a IS DISTINCT FROM b` | BOOLEAN | Null-safe inequality comparison | Both |
| `IS NOT DISTINCT FROM` | `a IS NOT DISTINCT FROM b` | BOOLEAN | Null-safe equality comparison | Both |
| `CASE WHEN` | `CASE WHEN cond THEN val ... END` | varies | Conditional expression | Both |

---

## Type Conversion Functions

For full details, see [Type Conversion Functions](../../functions/type-conversion/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `CAST` | `CAST(val AS type)` | varies | Converts value to specified type | Both |
| `BIGDECIMALTOBYTES` | `BIGDECIMALTOBYTES(decimal)` | BYTES | Converts BigDecimal to bytes | Both |
| `BYTESTOBIGDECIMAL` | `BYTESTOBIGDECIMAL(bytes)` | BIGDECIMAL | Converts bytes to BigDecimal | Both |
| `HEXDECIMALTOLONG` | `HEXDECIMALTOLONG(hex)` | LONG | Converts hex string to long | Both |
| `LONGTOHEXDECIMAL` | `LONGTOHEXDECIMAL(val)` | STRING | Converts long to hex string | Both |
| `TOUUIDBYTES` | `TOUUIDBYTES(uuid)` | BYTES | Converts UUID string to bytes | Both |
| `FROMUUIDBYTES` | `FROMUUIDBYTES(bytes)` | STRING | Converts bytes to UUID string | Both |

---

## Window Functions

For full details, see [Window Functions](../../functions/window).

{% hint style="info" %}
Window functions require the [multi-stage engine (MSE)](../../reference/configuration-reference/cluster.md).
{% endhint %}

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `ROW_NUMBER` | `ROW_NUMBER() OVER (...)` | LONG | Sequential row number within partition | MSE |
| `RANK` | `RANK() OVER (...)` | LONG | Rank with gaps for ties | MSE |
| `DENSE_RANK` | `DENSE_RANK() OVER (...)` | LONG | Rank without gaps for ties | MSE |
| `LAG` | `LAG(col [, offset [, default]]) OVER (...)` | varies | Value from a preceding row | MSE |
| `LEAD` | `LEAD(col [, offset [, default]]) OVER (...)` | varies | Value from a following row | MSE |
| `FIRST_VALUE` | `FIRST_VALUE(col) OVER (...)` | varies | First value in the window frame | MSE |
| `LAST_VALUE` | `LAST_VALUE(col) OVER (...)` | varies | Last value in the window frame | MSE |
| [`SUM`](../../functions/aggregation/sum.md) | `SUM(col) OVER (...)` | DOUBLE | Running/windowed sum | MSE |
| [`AVG`](../../functions/aggregation/avg.md) | `AVG(col) OVER (...)` | DOUBLE | Running/windowed average | MSE |
| [`MIN`](../../functions/aggregation/min.md) | `MIN(col) OVER (...)` | DOUBLE | Running/windowed minimum | MSE |
| [`MAX`](../../functions/aggregation/max.md) | `MAX(col) OVER (...)` | DOUBLE | Running/windowed maximum | MSE |
| [`COUNT`](../../functions/aggregation/count.md) | `COUNT(col) OVER (...)` | LONG | Running/windowed count | MSE |
| `BOOL_AND` | `BOOL_AND(col) OVER (...)` | BOOLEAN | Windowed boolean AND | MSE |
| `BOOL_OR` | `BOOL_OR(col) OVER (...)` | BOOLEAN | Windowed boolean OR | MSE |
