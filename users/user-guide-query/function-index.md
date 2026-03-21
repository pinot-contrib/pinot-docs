# Function Index

This page provides a comprehensive A-Z reference of the most commonly used functions in Apache Pinot, organized by category. Each category section links to its detailed documentation page with full syntax, parameters, and examples.

Functions are available in the **Single-Stage Engine (SSE)**, the **Multi-Stage Engine (MSE)**, or **both**. Window functions require the multi-stage engine.

---

## Aggregation Functions

For full details, see [Aggregation Functions](supported-aggregations.md).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `COUNT` | `COUNT(*)` or `COUNT(col)` | LONG | Counts the number of rows | Both |
| `MIN` | `MIN(col)` | DOUBLE | Returns the minimum value | Both |
| `MAX` | `MAX(col)` | DOUBLE | Returns the maximum value | Both |
| `SUM` | `SUM(col)` | DOUBLE | Returns the sum of values | Both |
| `AVG` | `AVG(col)` | DOUBLE | Returns the average of values | Both |
| `MODE` | `MODE(col)` | DOUBLE | Returns the most frequent value | Both |
| `MINMAXRANGE` | `MINMAXRANGE(col)` | DOUBLE | Returns the range (max - min) | Both |
| `DISTINCTCOUNT` | `DISTINCTCOUNT(col)` | INT | Returns the exact distinct count | Both |
| `DISTINCTCOUNTHLL` | `DISTINCTCOUNTHLL(col [, log2m])` | LONG | Approximate distinct count using HyperLogLog | Both |
| `DISTINCTCOUNTHLLPLUS` | `DISTINCTCOUNTHLLPLUS(col [, p])` | LONG | Approximate distinct count using HyperLogLog++ | Both |
| `DISTINCTCOUNTBITMAP` | `DISTINCTCOUNTBITMAP(col)` | INT | Distinct count using bitmap | Both |
| `DISTINCTCOUNTTHETASKETCH` | `DISTINCTCOUNTTHETASKETCH(col [, predicates...])` | LONG | Distinct count using Theta Sketch | Both |
| `DISTINCTCOUNTCPCSKETCH` | `DISTINCTCOUNTCPCSKETCH(col [, lgK])` | LONG | Distinct count using CPC Sketch | Both |
| `DISTINCTCOUNTULL` | `DISTINCTCOUNTULL(col [, p])` | LONG | Distinct count using UltraLogLog | Both |
| `DISTINCTSUM` | `DISTINCTSUM(col)` | DOUBLE | Sum of distinct values | Both |
| `DISTINCTAVG` | `DISTINCTAVG(col)` | DOUBLE | Average of distinct values | Both |
| `SEGMENTPARTITIONEDDISTINCTCOUNT` | `SEGMENTPARTITIONEDDISTINCTCOUNT(col)` | LONG | Optimized distinct count for partitioned columns | Both |
| `PERCENTILE` | `PERCENTILE(col, pct)` | DOUBLE | Exact percentile value | Both |
| `PERCENTILEEST` | `PERCENTILEEST(col, pct)` | LONG | Estimated percentile using Quantile Digest | Both |
| `PERCENTILETDIGEST` | `PERCENTILETDIGEST(col, pct)` | DOUBLE | Estimated percentile using T-Digest | Both |
| `PERCENTILEKLL` | `PERCENTILEKLL(col, pct)` | DOUBLE | Estimated percentile using KLL Sketch | Both |
| `HISTOGRAM` | `HISTOGRAM(col, binEdges...)` | DOUBLE[] | Computes histogram over bin edges | Both |
| `COVARPOP` | `COVARPOP(col1, col2)` | DOUBLE | Population covariance | Both |
| `COVARSAMP` | `COVARSAMP(col1, col2)` | DOUBLE | Sample covariance | Both |
| `VARPOP` | `VARPOP(col)` | DOUBLE | Population variance | Both |
| `VARSAMP` | `VARSAMP(col)` | DOUBLE | Sample variance | Both |
| `STDDEVPOP` | `STDDEVPOP(col)` | DOUBLE | Population standard deviation | Both |
| `STDDEVSAMP` | `STDDEVSAMP(col)` | DOUBLE | Sample standard deviation | Both |
| `SKEWNESS` | `SKEWNESS(col)` | DOUBLE | Skewness of values | Both |
| `KURTOSIS` | `KURTOSIS(col)` | DOUBLE | Kurtosis of values | Both |
| `FIRSTWITHTIME` | `FIRSTWITHTIME(dataCol, timeCol, 'type')` | varies | Value associated with the earliest timestamp | Both |
| `LASTWITHTIME` | `LASTWITHTIME(dataCol, timeCol, 'type')` | varies | Value associated with the latest timestamp | Both |
| `ANYVALUE` | `ANYVALUE(col)` | varies | Returns any arbitrary value from the group | Both |
| `BOOLAND` | `BOOLAND(col)` | BOOLEAN | Logical AND across all values | Both |
| `BOOLOR` | `BOOLOR(col)` | BOOLEAN | Logical OR across all values | Both |
| `EXPRMIN` | `EXPRMIN(measureCol, exprCol1, ...)` | varies | Columns at the row with minimum measure | Both |
| `EXPRMAX` | `EXPRMAX(measureCol, exprCol1, ...)` | varies | Columns at the row with maximum measure | Both |
| `FREQUENTSTRINGSSKETCH` | `FREQUENTSTRINGSSKETCH(col, maxMapSize)` | STRING | Frequent items sketch for strings | Both |
| `FREQUENTLONGSSKETCH` | `FREQUENTLONGSSKETCH(col, maxMapSize)` | STRING | Frequent items sketch for longs | Both |
| `FUNNELCOUNT` | `FUNNELCOUNT(stepCol, corCol, settings, step1, step2, ...)` | LONG[] | Funnel step counts | Both |
| `FUNNELMAXSTEP` | `FUNNELMAXSTEP(stepCol, corCol, settings, step1, step2, ...)` | INT | Maximum funnel step reached | Both |
| `FUNNELCOMPLETECOUNT` | `FUNNELCOMPLETECOUNT(stepCol, corCol, settings, step1, step2, ...)` | INT | Count of completed funnels | Both |
| `FUNNELSTEPDURATIONSTATS` | `FUNNELSTEPDURATIONSTATS(stepCol, corCol, tsCol, settings, step1, step2, ...)` | STRING | Step duration statistics | Both |
| `DISTINCTSUM` | `DISTINCTSUM(col)` | DOUBLE | Sum of distinct values | Both |
| `DISTINCTAVG` | `DISTINCTAVG(col)` | DOUBLE | Average of distinct values | Both |
| `SUMPRECISION` | `SUMPRECISION(col [, precision])` | STRING | High-precision sum using BigDecimal | Both |
| `ARRAYAGG` | `ARRAYAGG(col, 'type' [, distinct])` | ARRAY | Aggregates values into an array | Both |
| `LISTAGG` | `LISTAGG(col [, delimiter])` | STRING | Aggregates values into delimited string | Both |
| `SUMARRAYLONG` | `SUMARRAYLONG(arrCol)` | LONG[] | Element-wise sum of long arrays | Both |
| `SUMARRAYDOUBLE` | `SUMARRAYDOUBLE(arrCol)` | DOUBLE[] | Element-wise sum of double arrays | Both |

---

## String Functions

For full details, see [String Functions](../../functions/string/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `UPPER` | `UPPER(str)` | STRING | Converts string to uppercase | Both |
| `LOWER` | `LOWER(str)` | STRING | Converts string to lowercase | Both |
| `INITCAP` | `INITCAP(str)` | STRING | Capitalizes first letter of each word | Both |
| `REVERSE` | `REVERSE(str)` | STRING | Reverses the string | Both |
| `SUBSTR` | `SUBSTR(str, start [, end])` | STRING | Extracts substring by start/end position | Both |
| `SUBSTRING` | `SUBSTRING(str, start [, length])` | STRING | Extracts substring by start position and length | Both |
| `LEFT` | `LEFT(str, length)` | STRING | Returns leftmost N characters | Both |
| `RIGHT` | `RIGHT(str, length)` | STRING | Returns rightmost N characters | Both |
| `CONCAT` | `CONCAT(str1, str2)` | STRING | Concatenates two strings | Both |
| `TRIM` | `TRIM(str)` | STRING | Removes leading and trailing whitespace | Both |
| `LTRIM` | `LTRIM(str)` | STRING | Removes leading whitespace | Both |
| `RTRIM` | `RTRIM(str)` | STRING | Removes trailing whitespace | Both |
| `LPAD` | `LPAD(str, size, pad)` | STRING | Left-pads string to specified size | Both |
| `RPAD` | `RPAD(str, size, pad)` | STRING | Right-pads string to specified size | Both |
| `LENGTH` | `LENGTH(str)` | INT | Returns the length of the string | Both |
| `STRPOS` | `STRPOS(str, find [, instance])` | INT | Returns position of substring | Both |
| `STRRPOS` | `STRRPOS(str, find [, instance])` | INT | Returns last position of substring | Both |
| `STARTSWITH` | `STARTSWITH(str, prefix)` | BOOLEAN | Checks if string starts with prefix | Both |
| `ENDSWITH` | `ENDSWITH(str, suffix)` | BOOLEAN | Checks if string ends with suffix | Both |
| `CONTAINS` | `CONTAINS(str, substring)` | BOOLEAN | Checks if string contains substring | Both |
| `REPLACE` | `REPLACE(str, target, replacement)` | STRING | Replaces occurrences of target | Both |
| `REMOVE` | `REMOVE(str, search)` | STRING | Removes all occurrences of search string | Both |
| `SPLIT` | `SPLIT(str, delimiter [, limit])` | STRING[] | Splits string by delimiter | Both |
| `SPLITPART` | `SPLITPART(str, delimiter, index)` | STRING | Returns Nth part after splitting | Both |
| `REPEAT` | `REPEAT(str, times)` | STRING | Repeats string N times | Both |
| `REGEXP_EXTRACT` | `REGEXP_EXTRACT(str, pattern [, group])` | STRING | Extracts regex match from string | Both |
| `CHR` | `CHR(codepoint)` | STRING | Returns character for Unicode code point | Both |
| `CODEPOINT` | `CODEPOINT(str)` | INT | Returns Unicode code point of first character | Both |
| `NORMALIZE` | `NORMALIZE(str [, form])` | STRING | Normalizes Unicode string | Both |
| `STRCMP` | `STRCMP(str1, str2)` | INT | Compares two strings lexicographically | Both |
| `HAMMINGDISTANCE` | `HAMMINGDISTANCE(str1, str2)` | INT | Hamming distance between two strings | Both |
| `LEVENSTEINDISTANCE` | `LEVENSTEINDISTANCE(str1, str2)` | INT | Levenshtein edit distance | Both |

---

## Math Functions

For full details, see [Math Functions](../../functions/math/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `ABS` | `ABS(val)` | DOUBLE | Absolute value | Both |
| `CEIL` / `CEILING` | `CEIL(val)` | DOUBLE | Rounds up to nearest integer | Both |
| `FLOOR` | `FLOOR(val)` | DOUBLE | Rounds down to nearest integer | Both |
| `EXP` | `EXP(val)` | DOUBLE | Euler's number raised to the power | Both |
| `LN` / `LOG` | `LN(val)` | DOUBLE | Natural logarithm | Both |
| `LOG2` | `LOG2(val)` | DOUBLE | Base-2 logarithm | Both |
| `LOG10` | `LOG10(val)` | DOUBLE | Base-10 logarithm | Both |
| `SQRT` | `SQRT(val)` | DOUBLE | Square root | Both |
| `SIGN` | `SIGN(val)` | DOUBLE | Sign of a number (-1, 0, 1) | Both |
| `POW` / `POWER` | `POW(base, exp)` | DOUBLE | Raises base to exponent | Both |
| `MOD` | `MOD(a, b)` | DOUBLE | Modulo operation | Both |
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
| `NOW` | `NOW()` | LONG | Current timestamp in milliseconds | Both |
| `AGO` | `AGO('period')` | LONG | Timestamp for a period in the past | Both |
| `TODATETIME` | `TODATETIME(millis, pattern [, tz])` | STRING | Converts epoch millis to formatted string | Both |
| `FROMDATETIME` | `FROMDATETIME(str, pattern [, tz])` | LONG | Parses datetime string to epoch millis | Both |
| `TOEPOCHSECONDS` | `TOEPOCHSECONDS(millis)` | LONG | Converts millis to epoch seconds | Both |
| `TOEPOCHMINUTES` | `TOEPOCHMINUTES(millis)` | LONG | Converts millis to epoch minutes | Both |
| `TOEPOCHHOURS` | `TOEPOCHHOURS(millis)` | LONG | Converts millis to epoch hours | Both |
| `TOEPOCHDAYS` | `TOEPOCHDAYS(millis)` | LONG | Converts millis to epoch days | Both |
| `FROMEPOCHSECONDS` | `FROMEPOCHSECONDS(seconds)` | LONG | Converts epoch seconds to millis | Both |
| `FROMEPOCHMINUTES` | `FROMEPOCHMINUTES(minutes)` | LONG | Converts epoch minutes to millis | Both |
| `FROMEPOCHHOURS` | `FROMEPOCHHOURS(hours)` | LONG | Converts epoch hours to millis | Both |
| `FROMEPOCHDAYS` | `FROMEPOCHDAYS(days)` | LONG | Converts epoch days to millis | Both |
| `TOEPOCHSECONDSROUNDED` | `TOEPOCHSECONDSROUNDED(millis, roundTo)` | LONG | Converts millis to rounded epoch seconds | Both |
| `TOEPOCHMINUTESROUNDED` | `TOEPOCHMINUTESROUNDED(millis, roundTo)` | LONG | Converts millis to rounded epoch minutes | Both |
| `TOEPOCHHOURSROUNDED` | `TOEPOCHHOURSROUNDED(millis, roundTo)` | LONG | Converts millis to rounded epoch hours | Both |
| `TOEPOCHSECONDSBUCKET` | `TOEPOCHSECONDSBUCKET(millis, bucket)` | LONG | Buckets millis into epoch second intervals | Both |
| `FROMEPOCHSECONDSBUCKET` | `FROMEPOCHSECONDSBUCKET(seconds, bucket)` | LONG | Converts bucketed epoch seconds to millis | Both |
| `DATETRUNC` | `DATETRUNC(unit, timeVal [, inputUnit [, tz [, outputUnit]]])` | LONG | Truncates timestamp to specified granularity | Both |
| `DATEBIN` | `DATEBIN(binWidth, sourceTs, originTs)` | TIMESTAMP | Bins a timestamp into intervals | Both |
| `TIMESTAMPADD` / `DATEADD` | `TIMESTAMPADD(unit, interval, ts)` | LONG | Adds interval to timestamp | Both |
| `TIMESTAMPDIFF` / `DATEDIFF` | `TIMESTAMPDIFF(unit, ts1, ts2)` | LONG | Difference between two timestamps | Both |
| `EXTRACT` | `EXTRACT(field FROM ts)` | INT | Extracts date/time field from timestamp | Both |
| `YEAR` | `YEAR(millis [, tz])` | INT | Extracts year | Both |
| `QUARTER` | `QUARTER(millis [, tz])` | INT | Extracts quarter (1-4) | Both |
| `MONTH` | `MONTH(millis [, tz])` | INT | Extracts month (1-12) | Both |
| `WEEK` | `WEEK(millis [, tz])` | INT | Extracts ISO week of year | Both |
| `DAYOFYEAR` | `DAYOFYEAR(millis [, tz])` | INT | Extracts day of year (1-366) | Both |
| `DAYOFMONTH` / `DAY` | `DAYOFMONTH(millis [, tz])` | INT | Extracts day of month (1-31) | Both |
| `DAYOFWEEK` / `DOW` | `DAYOFWEEK(millis [, tz])` | INT | Extracts day of week (1-7) | Both |
| `HOUR` | `HOUR(millis [, tz])` | INT | Extracts hour (0-23) | Both |
| `MINUTE` | `MINUTE(millis [, tz])` | INT | Extracts minute (0-59) | Both |
| `SECOND` | `SECOND(millis [, tz])` | INT | Extracts second (0-59) | Both |
| `MILLISECOND` | `MILLISECOND(millis [, tz])` | INT | Extracts millisecond (0-999) | Both |
| `YEAROFWEEK` | `YEAROFWEEK(millis [, tz])` | INT | Extracts ISO year-of-week | Both |
| `TIMEZONEHOUR` | `TIMEZONEHOUR(tzId [, millis])` | INT | UTC offset hours for timezone | Both |
| `TIMEZONEMINUTE` | `TIMEZONEMINUTE(tzId [, millis])` | INT | UTC offset minutes for timezone | Both |
| `TOTIMESTAMP` | `TOTIMESTAMP(millis)` | TIMESTAMP | Converts millis to SQL Timestamp | Both |
| `FROMTIMESTAMP` | `FROMTIMESTAMP(ts)` | LONG | Converts SQL Timestamp to millis | Both |
| `DATETIMECONVERT` | `DATETIMECONVERT(col, inFormat, outFormat, granularity)` | STRING/LONG | Converts datetime between formats | Both |

---

## JSON Functions

For full details, see [JSON Functions](../../functions/json/).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `JSONPATH` | `JSONPATH(obj, path)` | OBJECT | Evaluates JSONPath expression | Both |
| `JSONPATHSTRING` | `JSONPATHSTRING(obj, path [, default])` | STRING | Extracts string via JSONPath | Both |
| `JSONPATHLONG` | `JSONPATHLONG(obj, path [, default])` | LONG | Extracts long via JSONPath | Both |
| `JSONPATHDOUBLE` | `JSONPATHDOUBLE(obj, path [, default])` | DOUBLE | Extracts double via JSONPath | Both |
| `JSONPATHARRAY` | `JSONPATHARRAY(obj, path)` | OBJECT[] | Extracts array via JSONPath | Both |
| `JSONPATHARRAYDEFAULTEMPTY` | `JSONPATHARRAYDEFAULTEMPTY(obj, path)` | OBJECT[] | Extracts array, returns empty if null | Both |
| `JSONPATHEXISTS` | `JSONPATHEXISTS(obj, path)` | BOOLEAN | Checks if JSONPath exists | Both |
| `JSONEXTRACTKEY` | `JSONEXTRACTKEY(obj, path)` | STRING[] | Extracts keys at JSONPath | Both |
| `JSONEXTRACTSCALAR` | `JSONEXTRACTSCALAR(json, path, type [, default])` | varies | Extracts scalar value from JSON | Both |
| `JSONFORMAT` | `JSONFORMAT(obj)` | STRING | Serializes object to JSON string | Both |
| `TOJSONMAPSTR` | `TOJSONMAPSTR(map)` | STRING | Converts map to JSON string | Both |
| `JSONSTRINGTOARRAY` | `JSONSTRINGTOARRAY(jsonStr)` | LIST | Parses JSON string to array | Both |
| `JSONSTRINGTOMAP` | `JSONSTRINGTOMAP(jsonStr)` | MAP | Parses JSON string to map | Both |
| `ISJSON` | `ISJSON(str)` | BOOLEAN | Checks if string is valid JSON | Both |

---

## Array Functions

For full details, see [Array Functions](../../functions/array).

| Function | Signature | Return Type | Description | Engine |
|---|---|---|---|---|
| `ARRAY_AGG` | `ARRAY_AGG(col, 'type' [, distinct])` | ARRAY | Aggregates values into an array | Both |
| `LISTAGG` | `LISTAGG(col [, delimiter [, distinct]])` | STRING | Aggregates values into a delimited string | Both |
| `ARRAYLENGTH` | `ARRAYLENGTH(arr)` | INT | Returns the length of an array | Both |
| `ARRAYCONTAINSINT` | `ARRAYCONTAINSINT(arr, val)` | BOOLEAN | Checks if integer array contains value | Both |
| `ARRAYCONTAINSSTRING` | `ARRAYCONTAINSSTRING(arr, val)` | BOOLEAN | Checks if string array contains value | Both |
| `ARRAYCONCATINT` | `ARRAYCONCATINT(arr1, arr2)` | INT[] | Concatenates two integer arrays | Both |
| `ARRAYCONCATSTRING` | `ARRAYCONCATSTRING(arr1, arr2)` | STRING[] | Concatenates two string arrays | Both |
| `ARRAYDISTINCTINT` | `ARRAYDISTINCTINT(arr)` | INT[] | Removes duplicates from integer array | Both |
| `ARRAYDISTINCTSTRING` | `ARRAYDISTINCTSTRING(arr)` | STRING[] | Removes duplicates from string array | Both |
| `ARRAYINDEXOFINT` | `ARRAYINDEXOFINT(arr, val)` | INT | Index of value in integer array | Both |
| `ARRAYINDEXOFSTRING` | `ARRAYINDEXOFSTRING(arr, val)` | INT | Index of value in string array | Both |
| `ARRAYREMOVEINT` | `ARRAYREMOVEINT(arr, val)` | INT[] | Removes first occurrence from integer array | Both |
| `ARRAYREMOVESTRING` | `ARRAYREMOVESTRING(arr, val)` | STRING[] | Removes first occurrence from string array | Both |
| `ARRAYREVERSEINT` | `ARRAYREVERSEINT(arr)` | INT[] | Reverses integer array | Both |
| `ARRAYREVERSESTRING` | `ARRAYREVERSESTRING(arr)` | STRING[] | Reverses string array | Both |
| `ARRAYSLICEINT` | `ARRAYSLICEINT(arr, start, end)` | INT[] | Extracts subarray from integer array | Both |
| `ARRAYSLICESTRING` | `ARRAYSLICESTRING(arr, start, end)` | STRING[] | Extracts subarray from string array | Both |
| `ARRAYSORTINT` | `ARRAYSORTINT(arr)` | INT[] | Sorts integer array ascending | Both |
| `ARRAYSORTSTRING` | `ARRAYSORTSTRING(arr)` | STRING[] | Sorts string array ascending | Both |
| `ARRAYUNIONINT` | `ARRAYUNIONINT(arr1, arr2)` | INT[] | Union of two integer arrays (unique) | Both |
| `ARRAYUNIONSTRING` | `ARRAYUNIONSTRING(arr1, arr2)` | STRING[] | Union of two string arrays (unique) | Both |
| `ARRAYSOVERLAP` | `ARRAYSOVERLAP(arr1, arr2)` | BOOLEAN | True if arrays share any element | Both |
| `ARRAYSUMINT` | `ARRAYSUMINT(arr)` | INT | Sum of integer array elements | Both |
| `ARRAYSUMLONG` | `ARRAYSUMLONG(arr)` | LONG | Sum of long array elements | Both |
| `ARRAYTOSTRING` | `ARRAYTOSTRING(arr, delimiter [, null])` | STRING | Joins array elements into string | Both |
| `SUMARRAYLONG` | `SUMARRAYLONG(arrCol)` | LONG | Aggregate: sums all elements across rows | Both |
| `SUMARRAYDOUBLE` | `SUMARRAYDOUBLE(arrCol)` | DOUBLE | Aggregate: sums all elements across rows | Both |

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
| `STPOINT` | `STPOINT(lng, lat)` | BYTES | Creates a geometry point | Both |
| `STPOLYGON` | `STPOLYGON(wkt)` | BYTES | Creates a polygon from WKT | Both |
| `STDISTANCE` | `STDISTANCE(geo1, geo2)` | DOUBLE | Distance between two geometries | Both |
| `STCONTAINS` | `STCONTAINS(geo1, geo2)` | BOOLEAN | Tests if first geometry contains second | Both |
| `STGEOMFROMTEXT` | `STGEOMFROMTEXT(wkt)` | BYTES | Creates geometry from WKT | Both |
| `STGEOMFROMWKB` | `STGEOMFROMWKB(wkb)` | BYTES | Creates geometry from WKB | Both |
| `STGEOMFROMGEOJSON` | `STGEOMFROMGEOJSON(json)` | BYTES | Creates geometry from GeoJSON | Both |
| `STGEOGFROMTEXT` | `STGEOGFROMTEXT(wkt)` | BYTES | Creates geography from WKT | Both |
| `STGEOGFROMWKB` | `STGEOGFROMWKB(wkb)` | BYTES | Creates geography from WKB | Both |
| `STGEOGFROMGEOJSON` | `STGEOGFROMGEOJSON(json)` | BYTES | Creates geography from GeoJSON | Both |
| `STASTEXT` | `STASTEXT(geo)` | STRING | Converts geometry to WKT | Both |
| `STASBINARY` | `STASBINARY(geo)` | BYTES | Converts geometry to WKB | Both |
| `STASGEOJSON` | `STASGEOJSON(geo)` | STRING | Converts geometry to GeoJSON | Both |
| `STGEOMETRYTYPE` | `STGEOMETRYTYPE(geo)` | STRING | Returns geometry type | Both |
| `TOSPHERICALGEOGRAPHY` | `TOSPHERICALGEOGRAPHY(geo)` | BYTES | Converts geometry to spherical geography | Both |
| `IDSET` | `IDSET(col [, params])` | BYTES | Serialized IdSet for use with IN_ID_SET filter | Both |
| `STUNION` | `STUNION(geoCol)` | BYTES | Aggregation: union of geometries | Both |

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
| `ISSUBNETOF` | `ISSUBNETOF(prefix, addr)` | BOOLEAN | Checks if IP address is in subnet | Both |
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
Window functions require the [multi-stage query engine (v2)](../../configuration-reference/cluster.md).
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
| `SUM` | `SUM(col) OVER (...)` | DOUBLE | Running/windowed sum | MSE |
| `AVG` | `AVG(col) OVER (...)` | DOUBLE | Running/windowed average | MSE |
| `MIN` | `MIN(col) OVER (...)` | DOUBLE | Running/windowed minimum | MSE |
| `MAX` | `MAX(col) OVER (...)` | DOUBLE | Running/windowed maximum | MSE |
| `COUNT` | `COUNT(col) OVER (...)` | LONG | Running/windowed count | MSE |
| `BOOL_AND` | `BOOL_AND(col) OVER (...)` | BOOLEAN | Windowed boolean AND | MSE |
| `BOOL_OR` | `BOOL_OR(col) OVER (...)` | BOOLEAN | Windowed boolean OR | MSE |
