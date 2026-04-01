# Function Index

This page provides a comprehensive A-Z reference of the most commonly used functions in Apache Pinot, organized by category. Each category section links to its detailed documentation page with full syntax, parameters, and examples.

Functions are available in the **Single-Stage Engine (SSE)**, the **Multi-Stage Engine (MSE)**, or **both**. Window functions require the multi-stage engine.

---

## Aggregation Functions

For full details, see [Aggregation Functions](../../functions/aggregation/README.md).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`COUNT`](../../functions/aggregation/count.md)</td>
      <td>`COUNT(*)` or `COUNT(col)`</td>
      <td>LONG</td>
      <td>Counts the number of rows</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MIN`](../../functions/aggregation/min.md)</td>
      <td>`MIN(col)`</td>
      <td>DOUBLE</td>
      <td>Returns the minimum value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MAX`](../../functions/aggregation/max.md)</td>
      <td>`MAX(col)`</td>
      <td>DOUBLE</td>
      <td>Returns the maximum value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUM`](../../functions/aggregation/sum.md)</td>
      <td>`SUM(col)`</td>
      <td>DOUBLE</td>
      <td>Returns the sum of values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`AVG`](../../functions/aggregation/avg.md)</td>
      <td>`AVG(col)`</td>
      <td>DOUBLE</td>
      <td>Returns the average of values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MODE`](../../functions/aggregation/mode.md)</td>
      <td>`MODE(col)`</td>
      <td>DOUBLE</td>
      <td>Returns the most frequent value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MINMAXRANGE`](../../functions/aggregation/minmaxrange.md)</td>
      <td>`MINMAXRANGE(col)`</td>
      <td>DOUBLE</td>
      <td>Returns the range (max - min)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNT`](../../functions/aggregation/distinctcount.md)</td>
      <td>`DISTINCTCOUNT(col)`</td>
      <td>INT</td>
      <td>Returns the exact distinct count</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNTHLL`](../../functions/aggregation/distinctcounthll.md)</td>
      <td>`DISTINCTCOUNTHLL(col [, log2m])`</td>
      <td>LONG</td>
      <td>Approximate distinct count using HyperLogLog</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNTHLLPLUS`](../../functions/sketch/distinctcounthllplus.md)</td>
      <td>`DISTINCTCOUNTHLLPLUS(col [, p])`</td>
      <td>LONG</td>
      <td>Approximate distinct count using HyperLogLog++</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNTBITMAP`](../../functions/aggregation/distinctcountbitmap.md)</td>
      <td>`DISTINCTCOUNTBITMAP(col)`</td>
      <td>INT</td>
      <td>Distinct count using bitmap</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNTTHETASKETCH`](../../functions/aggregation/distinctcountthetasketch.md)</td>
      <td>`DISTINCTCOUNTTHETASKETCH(col [, predicates...])`</td>
      <td>LONG</td>
      <td>Distinct count using Theta Sketch</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNTCPCSKETCH`](../../functions/sketch/distinctcountcpcsketch.md)</td>
      <td>`DISTINCTCOUNTCPCSKETCH(col [, lgK])`</td>
      <td>LONG</td>
      <td>Distinct count using CPC Sketch</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTCOUNTULL`](../../functions/sketch/distinctcountull.md)</td>
      <td>`DISTINCTCOUNTULL(col [, p])`</td>
      <td>LONG</td>
      <td>Distinct count using UltraLogLog</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTSUM`](../../functions/aggregation/distinctsum.md)</td>
      <td>`DISTINCTSUM(col)`</td>
      <td>DOUBLE</td>
      <td>Sum of distinct values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTAVG`](../../functions/aggregation/distinctavg.md)</td>
      <td>`DISTINCTAVG(col)`</td>
      <td>DOUBLE</td>
      <td>Average of distinct values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SEGMENTPARTITIONEDDISTINCTCOUNT`](../../functions/aggregation/segmentpartitioneddistinctcount.md)</td>
      <td>`SEGMENTPARTITIONEDDISTINCTCOUNT(col)`</td>
      <td>LONG</td>
      <td>Optimized distinct count for partitioned columns</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`PERCENTILE`](../../functions/aggregation/percentile.md)</td>
      <td>`PERCENTILE(col, pct)`</td>
      <td>DOUBLE</td>
      <td>Exact percentile value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`PERCENTILEEST`](../../functions/aggregation/percentileest.md)</td>
      <td>`PERCENTILEEST(col, pct)`</td>
      <td>LONG</td>
      <td>Estimated percentile using Quantile Digest</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`PERCENTILETDIGEST`](../../functions/aggregation/percentiletdigest.md)</td>
      <td>`PERCENTILETDIGEST(col, pct)`</td>
      <td>DOUBLE</td>
      <td>Estimated percentile using T-Digest</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`PERCENTILEKLL`](../../functions/aggregation/percentilekll.md)</td>
      <td>`PERCENTILEKLL(col, pct)`</td>
      <td>DOUBLE</td>
      <td>Estimated percentile using KLL Sketch</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`HISTOGRAM`](../../functions/aggregation/histogram.md)</td>
      <td>`HISTOGRAM(col, binEdges...)`</td>
      <td>DOUBLE[]</td>
      <td>Computes histogram over bin edges</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`COVARPOP`](../../functions/statistical/covar_pop.md)</td>
      <td>`COVARPOP(col1, col2)`</td>
      <td>DOUBLE</td>
      <td>Population covariance</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`COVARSAMP`](../../functions/statistical/covar_samp.md)</td>
      <td>`COVARSAMP(col1, col2)`</td>
      <td>DOUBLE</td>
      <td>Sample covariance</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`VARPOP`](../../functions/statistical/varpop.md)</td>
      <td>`VARPOP(col)`</td>
      <td>DOUBLE</td>
      <td>Population variance</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`VARSAMP`](../../functions/statistical/varsamp.md)</td>
      <td>`VARSAMP(col)`</td>
      <td>DOUBLE</td>
      <td>Sample variance</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STDDEVPOP`](../../functions/statistical/stddevpop.md)</td>
      <td>`STDDEVPOP(col)`</td>
      <td>DOUBLE</td>
      <td>Population standard deviation</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STDDEVSAMP`](../../functions/statistical/stddevsamp.md)</td>
      <td>`STDDEVSAMP(col)`</td>
      <td>DOUBLE</td>
      <td>Sample standard deviation</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SKEWNESS`](../../functions/aggregation/skewness.md)</td>
      <td>`SKEWNESS(col)`</td>
      <td>DOUBLE</td>
      <td>Skewness of values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`KURTOSIS`](../../functions/aggregation/kurtosis.md)</td>
      <td>`KURTOSIS(col)`</td>
      <td>DOUBLE</td>
      <td>Kurtosis of values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FIRSTWITHTIME`](../../functions/aggregation/firstwithtime.md)</td>
      <td>`FIRSTWITHTIME(dataCol, timeCol, 'type')`</td>
      <td>varies</td>
      <td>Value associated with the earliest timestamp</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LASTWITHTIME`](../../functions/aggregation/lastwithtime.md)</td>
      <td>`LASTWITHTIME(dataCol, timeCol, 'type')`</td>
      <td>varies</td>
      <td>Value associated with the latest timestamp</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ANYVALUE`](../../functions/aggregation/anyvalue.md)</td>
      <td>`ANYVALUE(col)`</td>
      <td>varies</td>
      <td>Returns any arbitrary value from the group</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`BOOLAND`](../../functions/aggregation/booland.md)</td>
      <td>`BOOLAND(col)`</td>
      <td>BOOLEAN</td>
      <td>Logical AND across all values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`BOOLOR`](../../functions/aggregation/boolor.md)</td>
      <td>`BOOLOR(col)`</td>
      <td>BOOLEAN</td>
      <td>Logical OR across all values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`EXPRMIN`](../../functions/aggregation/exprmin.md)</td>
      <td>`EXPRMIN(measureCol, exprCol1, ...)`</td>
      <td>varies</td>
      <td>Columns at the row with minimum measure</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`EXPRMAX`](../../functions/aggregation/exprmax.md)</td>
      <td>`EXPRMAX(measureCol, exprCol1, ...)`</td>
      <td>varies</td>
      <td>Columns at the row with maximum measure</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FREQUENTSTRINGSSKETCH`](../../functions/sketch/frequentstringssketch.md)</td>
      <td>`FREQUENTSTRINGSSKETCH(col, maxMapSize)`</td>
      <td>STRING</td>
      <td>Frequent items sketch for strings</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FREQUENTLONGSSKETCH`](../../functions/sketch/frequentlongssketch.md)</td>
      <td>`FREQUENTLONGSSKETCH(col, maxMapSize)`</td>
      <td>STRING</td>
      <td>Frequent items sketch for longs</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FUNNELCOUNT`](../../functions/funnel/funnelcount.md)</td>
      <td>`FUNNELCOUNT(stepCol, corCol, settings, step1, step2, ...)`</td>
      <td>LONG[]</td>
      <td>Funnel step counts</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FUNNELMAXSTEP`](../../functions/funnel/funnelmaxstep.md)</td>
      <td>`FUNNELMAXSTEP(stepCol, corCol, settings, step1, step2, ...)`</td>
      <td>INT</td>
      <td>Maximum funnel step reached</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FUNNELCOMPLETECOUNT`](../../functions/funnel/funnelcompletecount.md)</td>
      <td>`FUNNELCOMPLETECOUNT(stepCol, corCol, settings, step1, step2, ...)`</td>
      <td>INT</td>
      <td>Count of completed funnels</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FUNNELSTEPDURATIONSTATS`](../../functions/aggregation/funnelstepdurationstats.md)</td>
      <td>`FUNNELSTEPDURATIONSTATS(stepCol, corCol, tsCol, settings, step1, step2, ...)`</td>
      <td>STRING</td>
      <td>Step duration statistics</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTSUM`](../../functions/aggregation/distinctsum.md)</td>
      <td>`DISTINCTSUM(col)`</td>
      <td>DOUBLE</td>
      <td>Sum of distinct values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DISTINCTAVG`](../../functions/aggregation/distinctavg.md)</td>
      <td>`DISTINCTAVG(col)`</td>
      <td>DOUBLE</td>
      <td>Average of distinct values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUMPRECISION`](../../functions/aggregation/sumprecision.md)</td>
      <td>`SUMPRECISION(col [, precision])`</td>
      <td>STRING</td>
      <td>High-precision sum using BigDecimal</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYAGG`](../../functions/aggregation/arrayagg.md)</td>
      <td>`ARRAYAGG(col, 'type' [, distinct])`</td>
      <td>ARRAY</td>
      <td>Aggregates values into an array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LISTAGG`](../../functions/aggregation/listagg.md)</td>
      <td>`LISTAGG(col [, delimiter])`</td>
      <td>STRING</td>
      <td>Aggregates values into delimited string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUMARRAYLONG`](../../functions/aggregation/sumarraylong.md)</td>
      <td>`SUMARRAYLONG(arrCol)`</td>
      <td>LONG[]</td>
      <td>Element-wise sum of long arrays</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUMARRAYDOUBLE`](../../functions/aggregation/sumarraydouble.md)</td>
      <td>`SUMARRAYDOUBLE(arrCol)`</td>
      <td>DOUBLE[]</td>
      <td>Element-wise sum of double arrays</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## String Functions

For full details, see [String Functions](../../functions/string/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`UPPER`](../../functions/string/upper.md)</td>
      <td>`UPPER(str)`</td>
      <td>STRING</td>
      <td>Converts string to uppercase</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LOWER`](../../functions/string/lower.md)</td>
      <td>`LOWER(str)`</td>
      <td>STRING</td>
      <td>Converts string to lowercase</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`INITCAP`](../../functions/string/initcap.md)</td>
      <td>`INITCAP(str)`</td>
      <td>STRING</td>
      <td>Capitalizes first letter of each word</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`REVERSE`](../../functions/string/reverse.md)</td>
      <td>`REVERSE(str)`</td>
      <td>STRING</td>
      <td>Reverses the string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUBSTR`](../../functions/string/substr.md)</td>
      <td>`SUBSTR(str, start [, end])`</td>
      <td>STRING</td>
      <td>Extracts substring by start/end position</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SUBSTRING`</td>
      <td>`SUBSTRING(str, start [, length])`</td>
      <td>STRING</td>
      <td>Extracts substring by start position and length</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LEFT`</td>
      <td>`LEFT(str, length)`</td>
      <td>STRING</td>
      <td>Returns leftmost N characters</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`RIGHT`</td>
      <td>`RIGHT(str, length)`</td>
      <td>STRING</td>
      <td>Returns rightmost N characters</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`CONCAT`](../../functions/string/concat.md)</td>
      <td>`CONCAT(str1, str2)`</td>
      <td>STRING</td>
      <td>Concatenates two strings</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TRIM`](../../functions/string/trim.md)</td>
      <td>`TRIM(str)`</td>
      <td>STRING</td>
      <td>Removes leading and trailing whitespace</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LTRIM`](../../functions/string/ltrim.md)</td>
      <td>`LTRIM(str)`</td>
      <td>STRING</td>
      <td>Removes leading whitespace</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`RTRIM`](../../functions/string/rtrim.md)</td>
      <td>`RTRIM(str)`</td>
      <td>STRING</td>
      <td>Removes trailing whitespace</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LPAD`](../../functions/string/lpad.md)</td>
      <td>`LPAD(str, size, pad)`</td>
      <td>STRING</td>
      <td>Left-pads string to specified size</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`RPAD`](../../functions/string/rpad.md)</td>
      <td>`RPAD(str, size, pad)`</td>
      <td>STRING</td>
      <td>Right-pads string to specified size</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LENGTH`](../../functions/string/length.md)</td>
      <td>`LENGTH(str)`</td>
      <td>INT</td>
      <td>Returns the length of the string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STRPOS`](../../functions/string/strpos.md)</td>
      <td>`STRPOS(str, find [, instance])`</td>
      <td>INT</td>
      <td>Returns position of substring</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`STRRPOS`</td>
      <td>`STRRPOS(str, find [, instance])`</td>
      <td>INT</td>
      <td>Returns last position of substring</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STARTSWITH`](../../functions/string/startswith.md)</td>
      <td>`STARTSWITH(str, prefix)`</td>
      <td>BOOLEAN</td>
      <td>Checks if string starts with prefix</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ENDSWITH`</td>
      <td>`ENDSWITH(str, suffix)`</td>
      <td>BOOLEAN</td>
      <td>Checks if string ends with suffix</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CONTAINS`</td>
      <td>`CONTAINS(str, substring)`</td>
      <td>BOOLEAN</td>
      <td>Checks if string contains substring</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`REPLACE`](../../functions/string/replace.md)</td>
      <td>`REPLACE(str, target, replacement)`</td>
      <td>STRING</td>
      <td>Replaces occurrences of target</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`REMOVE`](../../functions/string/remove.md)</td>
      <td>`REMOVE(str, search)`</td>
      <td>STRING</td>
      <td>Removes all occurrences of search string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SPLIT`</td>
      <td>`SPLIT(str, delimiter [, limit])`</td>
      <td>STRING[]</td>
      <td>Splits string by delimiter</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SPLITPART`</td>
      <td>`SPLITPART(str, delimiter, index)`</td>
      <td>STRING</td>
      <td>Returns Nth part after splitting</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`REPEAT`</td>
      <td>`REPEAT(str, times)`</td>
      <td>STRING</td>
      <td>Repeats string N times</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`REGEXP_EXTRACT`](../../functions/string/regexpextract.md)</td>
      <td>`REGEXP_EXTRACT(str, pattern [, group])`</td>
      <td>STRING</td>
      <td>Extracts regex match from string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`CHR`](../../functions/string/chr.md)</td>
      <td>`CHR(codepoint)`</td>
      <td>STRING</td>
      <td>Returns character for Unicode code point</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`CODEPOINT`](../../functions/string/codepoint.md)</td>
      <td>`CODEPOINT(str)`</td>
      <td>INT</td>
      <td>Returns Unicode code point of first character</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`NORMALIZE`</td>
      <td>`NORMALIZE(str [, form])`</td>
      <td>STRING</td>
      <td>Normalizes Unicode string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`STRCMP`</td>
      <td>`STRCMP(str1, str2)`</td>
      <td>INT</td>
      <td>Compares two strings lexicographically</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`HAMMINGDISTANCE`</td>
      <td>`HAMMINGDISTANCE(str1, str2)`</td>
      <td>INT</td>
      <td>Hamming distance between two strings</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LEVENSTEINDISTANCE`](../../functions/string/levenshtein_distance.md)</td>
      <td>`LEVENSTEINDISTANCE(str1, str2)`</td>
      <td>INT</td>
      <td>Levenshtein edit distance</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Math Functions

For full details, see [Math Functions](../../functions/math/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`ABS`](../../functions/math/abs.md)</td>
      <td>`ABS(val)`</td>
      <td>DOUBLE</td>
      <td>Absolute value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CEIL` / `CEILING`</td>
      <td>`CEIL(val)`</td>
      <td>DOUBLE</td>
      <td>Rounds up to nearest integer</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FLOOR`](../../functions/math/floor.md)</td>
      <td>`FLOOR(val)`</td>
      <td>DOUBLE</td>
      <td>Rounds down to nearest integer</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`EXP`](../../functions/math/exp.md)</td>
      <td>`EXP(val)`</td>
      <td>DOUBLE</td>
      <td>Euler's number raised to the power</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LN` / `LOG`</td>
      <td>`LN(val)`</td>
      <td>DOUBLE</td>
      <td>Natural logarithm</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LOG2`</td>
      <td>`LOG2(val)`</td>
      <td>DOUBLE</td>
      <td>Base-2 logarithm</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LOG10`</td>
      <td>`LOG10(val)`</td>
      <td>DOUBLE</td>
      <td>Base-10 logarithm</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SQRT`](../../functions/math/sqrt.md)</td>
      <td>`SQRT(val)`</td>
      <td>DOUBLE</td>
      <td>Square root</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SIGN`</td>
      <td>`SIGN(val)`</td>
      <td>DOUBLE</td>
      <td>Sign of a number (-1, 0, 1)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`POW` / `POWER`</td>
      <td>`POW(base, exp)`</td>
      <td>DOUBLE</td>
      <td>Raises base to exponent</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MOD`](../../functions/math/mod.md)</td>
      <td>`MOD(a, b)`</td>
      <td>DOUBLE</td>
      <td>Modulo operation</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ROUNDDECIMAL`</td>
      <td>`ROUNDDECIMAL(val [, scale])`</td>
      <td>DOUBLE</td>
      <td>Rounds to specified decimal places</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TRUNCATE`</td>
      <td>`TRUNCATE(val [, scale])`</td>
      <td>DOUBLE</td>
      <td>Truncates to specified decimal places</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`DIV` / `DIVIDE`</td>
      <td>`DIV(a, b [, default])`</td>
      <td>DOUBLE</td>
      <td>Division with optional default for divide-by-zero</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`INTDIV`</td>
      <td>`INTDIV(a, b)`</td>
      <td>LONG</td>
      <td>Integer division</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LEAST`</td>
      <td>`LEAST(a, b)`</td>
      <td>DOUBLE</td>
      <td>Returns the smaller of two values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`GREATEST`</td>
      <td>`GREATEST(a, b)`</td>
      <td>DOUBLE</td>
      <td>Returns the larger of two values</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`GCD`</td>
      <td>`GCD(a, b)`</td>
      <td>LONG</td>
      <td>Greatest common divisor</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LCM`</td>
      <td>`LCM(a, b)`</td>
      <td>LONG</td>
      <td>Least common multiple</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`HYPOT`</td>
      <td>`HYPOT(a, b)`</td>
      <td>DOUBLE</td>
      <td>Hypotenuse (sqrt(a^2 + b^2))</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`NEGATE`</td>
      <td>`NEGATE(val)`</td>
      <td>DOUBLE</td>
      <td>Negates the value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`RAND`</td>
      <td>`RAND([seed])`</td>
      <td>DOUBLE</td>
      <td>Random number between 0 and 1</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SIN`</td>
      <td>`SIN(val)`</td>
      <td>DOUBLE</td>
      <td>Sine</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`COS`</td>
      <td>`COS(val)`</td>
      <td>DOUBLE</td>
      <td>Cosine</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TAN`</td>
      <td>`TAN(val)`</td>
      <td>DOUBLE</td>
      <td>Tangent</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`COT`</td>
      <td>`COT(val)`</td>
      <td>DOUBLE</td>
      <td>Cotangent</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ASIN`</td>
      <td>`ASIN(val)`</td>
      <td>DOUBLE</td>
      <td>Inverse sine</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ACOS`</td>
      <td>`ACOS(val)`</td>
      <td>DOUBLE</td>
      <td>Inverse cosine</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ATAN`</td>
      <td>`ATAN(val)`</td>
      <td>DOUBLE</td>
      <td>Inverse tangent</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ATAN2`</td>
      <td>`ATAN2(y, x)`</td>
      <td>DOUBLE</td>
      <td>Two-argument inverse tangent</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`DEGREES`</td>
      <td>`DEGREES(radians)`</td>
      <td>DOUBLE</td>
      <td>Converts radians to degrees</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`RADIANS`</td>
      <td>`RADIANS(degrees)`</td>
      <td>DOUBLE</td>
      <td>Converts degrees to radians</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## DateTime Functions

For full details, see [DateTime Functions](../../functions/datetime/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`NOW`](../../functions/datetime/now.md)</td>
      <td>`NOW()`</td>
      <td>LONG</td>
      <td>Current timestamp in milliseconds</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`AGO`](../../functions/datetime/ago.md)</td>
      <td>`AGO('period')`</td>
      <td>LONG</td>
      <td>Timestamp for a period in the past</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TODATETIME`](../../functions/datetime/todatetime.md)</td>
      <td>`TODATETIME(millis, pattern [, tz])`</td>
      <td>STRING</td>
      <td>Converts epoch millis to formatted string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FROMDATETIME`](../../functions/datetime/fromdatetime.md)</td>
      <td>`FROMDATETIME(str, pattern [, tz])`</td>
      <td>LONG</td>
      <td>Parses datetime string to epoch millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHSECONDS`](../../functions/datetime/toepoch.md)</td>
      <td>`TOEPOCHSECONDS(millis)`</td>
      <td>LONG</td>
      <td>Converts millis to epoch seconds</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHMINUTES`](../../functions/datetime/toepoch.md)</td>
      <td>`TOEPOCHMINUTES(millis)`</td>
      <td>LONG</td>
      <td>Converts millis to epoch minutes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHHOURS`](../../functions/datetime/toepoch.md)</td>
      <td>`TOEPOCHHOURS(millis)`</td>
      <td>LONG</td>
      <td>Converts millis to epoch hours</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHDAYS`](../../functions/datetime/toepoch.md)</td>
      <td>`TOEPOCHDAYS(millis)`</td>
      <td>LONG</td>
      <td>Converts millis to epoch days</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FROMEPOCHSECONDS`](../../functions/datetime/fromepoch.md)</td>
      <td>`FROMEPOCHSECONDS(seconds)`</td>
      <td>LONG</td>
      <td>Converts epoch seconds to millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FROMEPOCHMINUTES`](../../functions/datetime/fromepoch.md)</td>
      <td>`FROMEPOCHMINUTES(minutes)`</td>
      <td>LONG</td>
      <td>Converts epoch minutes to millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FROMEPOCHHOURS`](../../functions/datetime/fromepoch.md)</td>
      <td>`FROMEPOCHHOURS(hours)`</td>
      <td>LONG</td>
      <td>Converts epoch hours to millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FROMEPOCHDAYS`](../../functions/datetime/fromepoch.md)</td>
      <td>`FROMEPOCHDAYS(days)`</td>
      <td>LONG</td>
      <td>Converts epoch days to millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHSECONDSROUNDED`](../../functions/datetime/toepochrounded.md)</td>
      <td>`TOEPOCHSECONDSROUNDED(millis, roundTo)`</td>
      <td>LONG</td>
      <td>Converts millis to rounded epoch seconds</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHMINUTESROUNDED`](../../functions/datetime/toepochrounded.md)</td>
      <td>`TOEPOCHMINUTESROUNDED(millis, roundTo)`</td>
      <td>LONG</td>
      <td>Converts millis to rounded epoch minutes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHHOURSROUNDED`](../../functions/datetime/toepochrounded.md)</td>
      <td>`TOEPOCHHOURSROUNDED(millis, roundTo)`</td>
      <td>LONG</td>
      <td>Converts millis to rounded epoch hours</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOEPOCHSECONDSBUCKET`](../../functions/datetime/toepochbucket.md)</td>
      <td>`TOEPOCHSECONDSBUCKET(millis, bucket)`</td>
      <td>LONG</td>
      <td>Buckets millis into epoch second intervals</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`FROMEPOCHSECONDSBUCKET`](../../functions/datetime/fromepochbucket.md)</td>
      <td>`FROMEPOCHSECONDSBUCKET(seconds, bucket)`</td>
      <td>LONG</td>
      <td>Converts bucketed epoch seconds to millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DATETRUNC`](../../functions/datetime/datetrunc.md)</td>
      <td>`DATETRUNC(unit, timeVal [, inputUnit [, tz [, outputUnit]]])`</td>
      <td>LONG</td>
      <td>Truncates timestamp to specified granularity</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`DATEBIN`</td>
      <td>`DATEBIN(binWidth, sourceTs, originTs)`</td>
      <td>TIMESTAMP</td>
      <td>Bins a timestamp into intervals</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TIMESTAMPADD` / `DATEADD`</td>
      <td>`TIMESTAMPADD(unit, interval, ts)`</td>
      <td>LONG</td>
      <td>Adds interval to timestamp</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TIMESTAMPDIFF` / `DATEDIFF`</td>
      <td>`TIMESTAMPDIFF(unit, ts1, ts2)`</td>
      <td>LONG</td>
      <td>Difference between two timestamps</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`EXTRACT`](../../functions/datetime/extract.md)</td>
      <td>`EXTRACT(field FROM ts)`</td>
      <td>INT</td>
      <td>Extracts date/time field from timestamp</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`YEAR`](../../functions/datetime/year.md)</td>
      <td>`YEAR(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts year</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`QUARTER`](../../functions/datetime/quarter.md)</td>
      <td>`QUARTER(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts quarter (1-4)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MONTH`](../../functions/datetime/month.md)</td>
      <td>`MONTH(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts month (1-12)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`WEEK`](../../functions/datetime/week.md)</td>
      <td>`WEEK(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts ISO week of year</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DAYOFYEAR`](../../functions/datetime/dayofyear.md)</td>
      <td>`DAYOFYEAR(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts day of year (1-366)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`DAYOFMONTH` / `DAY`</td>
      <td>`DAYOFMONTH(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts day of month (1-31)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DAYOFWEEK`](../../functions/datetime/dayofweek.md) / `DOW`</td>
      <td>`DAYOFWEEK(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts day of week (1-7)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`HOUR`](../../functions/datetime/hour.md)</td>
      <td>`HOUR(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts hour (0-23)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MINUTE`](../../functions/datetime/minute.md)</td>
      <td>`MINUTE(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts minute (0-59)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SECOND`](../../functions/datetime/second.md)</td>
      <td>`SECOND(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts second (0-59)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`MILLISECOND`](../../functions/datetime/millisecond.md)</td>
      <td>`MILLISECOND(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts millisecond (0-999)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`YEAROFWEEK`](../../functions/datetime/yearofweek.md)</td>
      <td>`YEAROFWEEK(millis [, tz])`</td>
      <td>INT</td>
      <td>Extracts ISO year-of-week</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TIMEZONEHOUR`](../../functions/datetime/timezonehour.md)</td>
      <td>`TIMEZONEHOUR(tzId [, millis])`</td>
      <td>INT</td>
      <td>UTC offset hours for timezone</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TIMEZONEMINUTE`](../../functions/datetime/timezoneminute.md)</td>
      <td>`TIMEZONEMINUTE(tzId [, millis])`</td>
      <td>INT</td>
      <td>UTC offset minutes for timezone</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TOTIMESTAMP`</td>
      <td>`TOTIMESTAMP(millis)`</td>
      <td>TIMESTAMP</td>
      <td>Converts millis to SQL Timestamp</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`FROMTIMESTAMP`</td>
      <td>`FROMTIMESTAMP(ts)`</td>
      <td>LONG</td>
      <td>Converts SQL Timestamp to millis</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`DATETIMECONVERT`](../../functions/datetime/datetimeconvert.md)</td>
      <td>`DATETIMECONVERT(col, inFormat, outFormat, granularity)`</td>
      <td>STRING/LONG</td>
      <td>Converts datetime between formats</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## JSON Functions

For full details, see [JSON Functions](../../functions/json/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`JSONPATH`](../../functions/json/jsonpath.md)</td>
      <td>`JSONPATH(obj, path)`</td>
      <td>OBJECT</td>
      <td>Evaluates JSONPath expression</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONPATHSTRING`](../../functions/json/jsonpathstring.md)</td>
      <td>`JSONPATHSTRING(obj, path [, default])`</td>
      <td>STRING</td>
      <td>Extracts string via JSONPath</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONPATHLONG`](../../functions/json/jsonpathlong.md)</td>
      <td>`JSONPATHLONG(obj, path [, default])`</td>
      <td>LONG</td>
      <td>Extracts long via JSONPath</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONPATHDOUBLE`](../../functions/json/jsonpathdouble.md)</td>
      <td>`JSONPATHDOUBLE(obj, path [, default])`</td>
      <td>DOUBLE</td>
      <td>Extracts double via JSONPath</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONPATHARRAY`](../../functions/json/jsonpatharray.md)</td>
      <td>`JSONPATHARRAY(obj, path)`</td>
      <td>OBJECT[]</td>
      <td>Extracts array via JSONPath</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONPATHARRAYDEFAULTEMPTY`](../../functions/json/jsonpatharraydefaultempty.md)</td>
      <td>`JSONPATHARRAYDEFAULTEMPTY(obj, path)`</td>
      <td>OBJECT[]</td>
      <td>Extracts array, returns empty if null</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONPATHEXISTS`](../../functions/json/jsonpathexists.md)</td>
      <td>`JSONPATHEXISTS(obj, path)`</td>
      <td>BOOLEAN</td>
      <td>Checks if JSONPath exists</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONEXTRACTKEY`](../../functions/json/jsonextractkey.md)</td>
      <td>`JSONEXTRACTKEY(obj, path)`</td>
      <td>STRING[]</td>
      <td>Extracts keys at JSONPath</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONEXTRACTSCALAR`](../../functions/json/jsonextractscalar.md)</td>
      <td>`JSONEXTRACTSCALAR(json, path, type [, default])`</td>
      <td>varies</td>
      <td>Extracts scalar value from JSON</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`JSONFORMAT`](../../functions/json/jsonformat.md)</td>
      <td>`JSONFORMAT(obj)`</td>
      <td>STRING</td>
      <td>Serializes object to JSON string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOJSONMAPSTR`](../../functions/json/tojsonmapstr.md)</td>
      <td>`TOJSONMAPSTR(map)`</td>
      <td>STRING</td>
      <td>Converts map to JSON string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`JSONSTRINGTOARRAY`</td>
      <td>`JSONSTRINGTOARRAY(jsonStr)`</td>
      <td>LIST</td>
      <td>Parses JSON string to array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`JSONSTRINGTOMAP`</td>
      <td>`JSONSTRINGTOMAP(jsonStr)`</td>
      <td>MAP</td>
      <td>Parses JSON string to map</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ISJSON`</td>
      <td>`ISJSON(str)`</td>
      <td>BOOLEAN</td>
      <td>Checks if string is valid JSON</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Array Functions

For full details, see [Array Functions](../../functions/array).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`ARRAY_AGG`</td>
      <td>`ARRAY_AGG(col, 'type' [, distinct])`</td>
      <td>ARRAY</td>
      <td>Aggregates values into an array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`LISTAGG`](../../functions/aggregation/listagg.md)</td>
      <td>`LISTAGG(col [, delimiter [, distinct]])`</td>
      <td>STRING</td>
      <td>Aggregates values into a delimited string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYLENGTH`](../../functions/array/arraylength.md)</td>
      <td>`ARRAYLENGTH(arr)`</td>
      <td>INT</td>
      <td>Returns the length of an array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYCONTAINSINT`](../../functions/array/arraycontainsint.md)</td>
      <td>`ARRAYCONTAINSINT(arr, val)`</td>
      <td>BOOLEAN</td>
      <td>Checks if integer array contains value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYCONTAINSSTRING`](../../functions/array/arraycontainsstring.md)</td>
      <td>`ARRAYCONTAINSSTRING(arr, val)`</td>
      <td>BOOLEAN</td>
      <td>Checks if string array contains value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYCONCATINT`](../../functions/array/arrayconcatint.md)</td>
      <td>`ARRAYCONCATINT(arr1, arr2)`</td>
      <td>INT[]</td>
      <td>Concatenates two integer arrays</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYCONCATSTRING`](../../functions/array/arrayconcatstring.md)</td>
      <td>`ARRAYCONCATSTRING(arr1, arr2)`</td>
      <td>STRING[]</td>
      <td>Concatenates two string arrays</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYDISTINCTINT`](../../functions/array/arraydistinctint.md)</td>
      <td>`ARRAYDISTINCTINT(arr)`</td>
      <td>INT[]</td>
      <td>Removes duplicates from integer array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYDISTINCTSTRING`](../../functions/array/arraydistinctstring.md)</td>
      <td>`ARRAYDISTINCTSTRING(arr)`</td>
      <td>STRING[]</td>
      <td>Removes duplicates from string array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYINDEXOFINT`](../../functions/array/arrayindexofint.md)</td>
      <td>`ARRAYINDEXOFINT(arr, val)`</td>
      <td>INT</td>
      <td>Index of value in integer array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYINDEXOFSTRING`](../../functions/array/arrayindexofstring.md)</td>
      <td>`ARRAYINDEXOFSTRING(arr, val)`</td>
      <td>INT</td>
      <td>Index of value in string array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYREMOVEINT`](../../functions/array/arrayremoveint.md)</td>
      <td>`ARRAYREMOVEINT(arr, val)`</td>
      <td>INT[]</td>
      <td>Removes first occurrence from integer array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYREMOVESTRING`](../../functions/array/arrayremovestring.md)</td>
      <td>`ARRAYREMOVESTRING(arr, val)`</td>
      <td>STRING[]</td>
      <td>Removes first occurrence from string array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYREVERSEINT`](../../functions/array/arrayreverseint.md)</td>
      <td>`ARRAYREVERSEINT(arr)`</td>
      <td>INT[]</td>
      <td>Reverses integer array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYREVERSESTRING`](../../functions/array/arrayreversestring.md)</td>
      <td>`ARRAYREVERSESTRING(arr)`</td>
      <td>STRING[]</td>
      <td>Reverses string array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYSLICEINT`](../../functions/array/arraysliceint.md)</td>
      <td>`ARRAYSLICEINT(arr, start, end)`</td>
      <td>INT[]</td>
      <td>Extracts subarray from integer array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYSLICESTRING`](../../functions/array/arrayslicestring.md)</td>
      <td>`ARRAYSLICESTRING(arr, start, end)`</td>
      <td>STRING[]</td>
      <td>Extracts subarray from string array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYSORTINT`](../../functions/array/arraysortint.md)</td>
      <td>`ARRAYSORTINT(arr)`</td>
      <td>INT[]</td>
      <td>Sorts integer array ascending</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYSORTSTRING`](../../functions/array/arraysortstring.md)</td>
      <td>`ARRAYSORTSTRING(arr)`</td>
      <td>STRING[]</td>
      <td>Sorts string array ascending</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYUNIONINT`](../../functions/array/arrayunionint.md)</td>
      <td>`ARRAYUNIONINT(arr1, arr2)`</td>
      <td>INT[]</td>
      <td>Union of two integer arrays (unique)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`ARRAYUNIONSTRING`](../../functions/array/arrayunionstring.md)</td>
      <td>`ARRAYUNIONSTRING(arr1, arr2)`</td>
      <td>STRING[]</td>
      <td>Union of two string arrays (unique)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ARRAYSOVERLAP`</td>
      <td>`ARRAYSOVERLAP(arr1, arr2)`</td>
      <td>BOOLEAN</td>
      <td>True if arrays share any element</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ARRAYSUMINT`</td>
      <td>`ARRAYSUMINT(arr)`</td>
      <td>INT</td>
      <td>Sum of integer array elements</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ARRAYSUMLONG`</td>
      <td>`ARRAYSUMLONG(arr)`</td>
      <td>LONG</td>
      <td>Sum of long array elements</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ARRAYTOSTRING`</td>
      <td>`ARRAYTOSTRING(arr, delimiter [, null])`</td>
      <td>STRING</td>
      <td>Joins array elements into string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUMARRAYLONG`](../../functions/aggregation/sumarraylong.md)</td>
      <td>`SUMARRAYLONG(arrCol)`</td>
      <td>LONG</td>
      <td>Aggregate: sums all elements across rows</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`SUMARRAYDOUBLE`](../../functions/aggregation/sumarraydouble.md)</td>
      <td>`SUMARRAYDOUBLE(arrCol)`</td>
      <td>DOUBLE</td>
      <td>Aggregate: sums all elements across rows</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Hash Functions

For full details, see [Hash Functions](../../functions/hash).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`SHA`</td>
      <td>`SHA(bytes)`</td>
      <td>STRING</td>
      <td>SHA-1 hash</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SHA224`</td>
      <td>`SHA224(bytes)`</td>
      <td>STRING</td>
      <td>SHA-224 hash</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SHA256`</td>
      <td>`SHA256(bytes)`</td>
      <td>STRING</td>
      <td>SHA-256 hash</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`SHA512`</td>
      <td>`SHA512(bytes)`</td>
      <td>STRING</td>
      <td>SHA-512 hash</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MD2`</td>
      <td>`MD2(bytes)`</td>
      <td>STRING</td>
      <td>MD2 hash</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MD5`</td>
      <td>`MD5(bytes)`</td>
      <td>STRING</td>
      <td>MD5 hash</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MURMURHASH2`</td>
      <td>`MURMURHASH2(bytes)`</td>
      <td>INT</td>
      <td>32-bit MurmurHash2</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MURMURHASH2UTF8`</td>
      <td>`MURMURHASH2UTF8(str)`</td>
      <td>INT</td>
      <td>32-bit MurmurHash2 for strings</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MURMURHASH3BIT32`</td>
      <td>`MURMURHASH3BIT32(bytes, seed)`</td>
      <td>INT</td>
      <td>32-bit MurmurHash3</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MURMURHASH3BIT64`</td>
      <td>`MURMURHASH3BIT64(bytes, seed)`</td>
      <td>LONG</td>
      <td>64-bit MurmurHash3</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`MURMURHASH3BIT128`</td>
      <td>`MURMURHASH3BIT128(bytes, seed)`</td>
      <td>BYTES</td>
      <td>128-bit MurmurHash3</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CRC32`</td>
      <td>`CRC32(bytes)`</td>
      <td>INT</td>
      <td>32-bit CRC checksum</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CRC32C`</td>
      <td>`CRC32C(bytes)`</td>
      <td>INT</td>
      <td>32-bit CRC32C (Castagnoli)</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`ADLER32`</td>
      <td>`ADLER32(bytes)`</td>
      <td>INT</td>
      <td>32-bit Adler checksum</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## URL Functions

For full details, see [URL Functions](../../functions/url).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`URLPROTOCOL`</td>
      <td>`URLPROTOCOL(url)`</td>
      <td>STRING</td>
      <td>Extracts protocol/scheme</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLDOMAIN`</td>
      <td>`URLDOMAIN(url)`</td>
      <td>STRING</td>
      <td>Extracts domain</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLDOMAINWITHOUTWWW`</td>
      <td>`URLDOMAINWITHOUTWWW(url)`</td>
      <td>STRING</td>
      <td>Extracts domain without www prefix</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLTOPLEVELDOMAIN`</td>
      <td>`URLTOPLEVELDOMAIN(url)`</td>
      <td>STRING</td>
      <td>Extracts top-level domain</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLPORT`</td>
      <td>`URLPORT(url)`</td>
      <td>INT</td>
      <td>Extracts port number</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLPATH`</td>
      <td>`URLPATH(url)`</td>
      <td>STRING</td>
      <td>Extracts path component</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLQUERYSTRING`</td>
      <td>`URLQUERYSTRING(url)`</td>
      <td>STRING</td>
      <td>Extracts query string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLFRAGMENT`</td>
      <td>`URLFRAGMENT(url)`</td>
      <td>STRING</td>
      <td>Extracts fragment identifier</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`EXTRACTURLPARAMETER`</td>
      <td>`EXTRACTURLPARAMETER(url, name)`</td>
      <td>STRING</td>
      <td>Extracts specific query parameter</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`EXTRACTURLPARAMETERS`</td>
      <td>`EXTRACTURLPARAMETERS(url)`</td>
      <td>STRING[]</td>
      <td>Extracts all query parameters</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLENCODE`</td>
      <td>`URLENCODE(url)`</td>
      <td>STRING</td>
      <td>URL-encodes a string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`URLDECODE`</td>
      <td>`URLDECODE(url)`</td>
      <td>STRING</td>
      <td>Decodes URL-encoded string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CUTWWW`</td>
      <td>`CUTWWW(url)`</td>
      <td>STRING</td>
      <td>Removes www prefix from URL</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CUTQUERYSTRING`</td>
      <td>`CUTQUERYSTRING(url)`</td>
      <td>STRING</td>
      <td>Removes query string from URL</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CUTFRAGMENT`</td>
      <td>`CUTFRAGMENT(url)`</td>
      <td>STRING</td>
      <td>Removes fragment from URL</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CUTURLPARAMETER`</td>
      <td>`CUTURLPARAMETER(url, name)`</td>
      <td>STRING</td>
      <td>Removes specific query parameter</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Binary Functions

For full details, see [Binary Functions](../../functions/binary/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`TOUTF8`</td>
      <td>`TOUTF8(str)`</td>
      <td>BYTES</td>
      <td>Converts string to UTF-8 bytes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`FROMUTF8`</td>
      <td>`FROMUTF8(bytes)`</td>
      <td>STRING</td>
      <td>Converts UTF-8 bytes to string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TOASCII`</td>
      <td>`TOASCII(str)`</td>
      <td>BYTES</td>
      <td>Converts string to ASCII bytes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`FROMASCII`</td>
      <td>`FROMASCII(bytes)`</td>
      <td>STRING</td>
      <td>Converts ASCII bytes to string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TOBASE64`</td>
      <td>`TOBASE64(bytes)`</td>
      <td>STRING</td>
      <td>Encodes bytes as Base64 string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`FROMBASE64`</td>
      <td>`FROMBASE64(str)`</td>
      <td>BYTES</td>
      <td>Decodes Base64 string to bytes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`BASE64ENCODE`</td>
      <td>`BASE64ENCODE(bytes)`</td>
      <td>BYTES</td>
      <td>Base64 encodes byte array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`BASE64DECODE`</td>
      <td>`BASE64DECODE(bytes)`</td>
      <td>BYTES</td>
      <td>Base64 decodes byte array</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`HEXTOBYTES`</td>
      <td>`HEXTOBYTES(hex)`</td>
      <td>BYTES</td>
      <td>Converts hex string to bytes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`BYTESTOHEX`</td>
      <td>`BYTESTOHEX(bytes)`</td>
      <td>STRING</td>
      <td>Converts bytes to hex string</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Geospatial Functions

For full details, see [GeoSpatial Functions](../../functions/geospatial/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`STPOINT`](../../functions/geospatial/stpoint.md)</td>
      <td>`STPOINT(lng, lat)`</td>
      <td>BYTES</td>
      <td>Creates a geometry point</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STPOLYGON`](../../functions/geospatial/stpolygon.md)</td>
      <td>`STPOLYGON(wkt)`</td>
      <td>BYTES</td>
      <td>Creates a polygon from WKT</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STDISTANCE`](../../functions/geospatial/stdistance.md)</td>
      <td>`STDISTANCE(geo1, geo2)`</td>
      <td>DOUBLE</td>
      <td>Distance between two geometries</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STCONTAINS`](../../functions/geospatial/stcontains.md)</td>
      <td>`STCONTAINS(geo1, geo2)`</td>
      <td>BOOLEAN</td>
      <td>Tests if first geometry contains second</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOMFROMTEXT`](../../functions/geospatial/stgeomfromtext.md)</td>
      <td>`STGEOMFROMTEXT(wkt)`</td>
      <td>BYTES</td>
      <td>Creates geometry from WKT</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOMFROMWKB`](../../functions/geospatial/stgeomfromwkb.md)</td>
      <td>`STGEOMFROMWKB(wkb)`</td>
      <td>BYTES</td>
      <td>Creates geometry from WKB</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOMFROMGEOJSON`](../../functions/geospatial/st_geomfromgeojson.md)</td>
      <td>`STGEOMFROMGEOJSON(json)`</td>
      <td>BYTES</td>
      <td>Creates geometry from GeoJSON</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOGFROMTEXT`](../../functions/geospatial/stgeogfromtext.md)</td>
      <td>`STGEOGFROMTEXT(wkt)`</td>
      <td>BYTES</td>
      <td>Creates geography from WKT</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOGFROMWKB`](../../functions/geospatial/stgeogfromwkb.md)</td>
      <td>`STGEOGFROMWKB(wkb)`</td>
      <td>BYTES</td>
      <td>Creates geography from WKB</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOGFROMGEOJSON`](../../functions/geospatial/st_geogfromgeojson.md)</td>
      <td>`STGEOGFROMGEOJSON(json)`</td>
      <td>BYTES</td>
      <td>Creates geography from GeoJSON</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STASTEXT`](../../functions/geospatial/stastext.md)</td>
      <td>`STASTEXT(geo)`</td>
      <td>STRING</td>
      <td>Converts geometry to WKT</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STASBINARY`](../../functions/geospatial/stasbinary.md)</td>
      <td>`STASBINARY(geo)`</td>
      <td>BYTES</td>
      <td>Converts geometry to WKB</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STASGEOJSON`](../../functions/geospatial/st_asgeojson.md)</td>
      <td>`STASGEOJSON(geo)`</td>
      <td>STRING</td>
      <td>Converts geometry to GeoJSON</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STGEOMETRYTYPE`](../../functions/geospatial/stgeometrytype.md)</td>
      <td>`STGEOMETRYTYPE(geo)`</td>
      <td>STRING</td>
      <td>Returns geometry type</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`TOSPHERICALGEOGRAPHY`](../../functions/geospatial/tosphericalgeography.md)</td>
      <td>`TOSPHERICALGEOGRAPHY(geo)`</td>
      <td>BYTES</td>
      <td>Converts geometry to spherical geography</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`IDSET`](../../functions/aggregation/idset.md)</td>
      <td>`IDSET(col [, params])`</td>
      <td>BYTES</td>
      <td>Serialized IdSet for use with IN_ID_SET filter</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>[`STUNION`](../../functions/geospatial/stunion.md)</td>
      <td>`STUNION(geoCol)`</td>
      <td>BYTES</td>
      <td>Aggregation: union of geometries</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Vector / Similarity Functions

For full details, see [Vector Functions](../../functions/vector/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`COSINEDISTANCE`</td>
      <td>`COSINEDISTANCE(arr1, arr2)`</td>
      <td>DOUBLE</td>
      <td>Cosine distance between two vectors</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`INNERPRODUCT`</td>
      <td>`INNERPRODUCT(arr1, arr2)`</td>
      <td>DOUBLE</td>
      <td>Inner (dot) product of two vectors</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`L1DISTANCE`</td>
      <td>`L1DISTANCE(arr1, arr2)`</td>
      <td>DOUBLE</td>
      <td>Manhattan distance between two vectors</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`L2DISTANCE`</td>
      <td>`L2DISTANCE(arr1, arr2)`</td>
      <td>DOUBLE</td>
      <td>Euclidean distance between two vectors</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`VECTORDIMS`</td>
      <td>`VECTORDIMS(arr)`</td>
      <td>INT</td>
      <td>Number of dimensions in a vector</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`VECTORNORM`</td>
      <td>`VECTORNORM(arr)`</td>
      <td>DOUBLE</td>
      <td>L2 norm (magnitude) of a vector</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## IP Address Functions

For full details, see [IP Address Functions](../../functions/ip-address/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[`ISSUBNETOF`](../../functions/misc/issubnetof.md)</td>
      <td>`ISSUBNETOF(prefix, addr)`</td>
      <td>BOOLEAN</td>
      <td>Checks if IP address is in subnet</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`IPPREFIX`</td>
      <td>`IPPREFIX(addr, prefixLen)`</td>
      <td>STRING</td>
      <td>Returns CIDR prefix for IP address</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`IPSUBNETMIN`</td>
      <td>`IPSUBNETMIN(prefix)`</td>
      <td>STRING</td>
      <td>Returns lowest IP in subnet</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`IPSUBNETMAX`</td>
      <td>`IPSUBNETMAX(prefix)`</td>
      <td>STRING</td>
      <td>Returns highest IP in subnet</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Null Handling Functions

For full details, see [Null Handling Functions](../../functions/null-handling/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`IS NULL`</td>
      <td>`col IS NULL`</td>
      <td>BOOLEAN</td>
      <td>True if value is null</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`IS NOT NULL`</td>
      <td>`col IS NOT NULL`</td>
      <td>BOOLEAN</td>
      <td>True if value is not null</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`COALESCE`</td>
      <td>`COALESCE(val1, val2, ...)`</td>
      <td>varies</td>
      <td>Returns first non-null value</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`NULLIF`</td>
      <td>`NULLIF(val1, val2)`</td>
      <td>varies</td>
      <td>Returns null if values are equal</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`IS DISTINCT FROM`</td>
      <td>`a IS DISTINCT FROM b`</td>
      <td>BOOLEAN</td>
      <td>Null-safe inequality comparison</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`IS NOT DISTINCT FROM`</td>
      <td>`a IS NOT DISTINCT FROM b`</td>
      <td>BOOLEAN</td>
      <td>Null-safe equality comparison</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`CASE WHEN`</td>
      <td>`CASE WHEN cond THEN val ... END`</td>
      <td>varies</td>
      <td>Conditional expression</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Type Conversion Functions

For full details, see [Type Conversion Functions](../../functions/type-conversion/).

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`CAST`</td>
      <td>`CAST(val AS type)`</td>
      <td>varies</td>
      <td>Converts value to specified type</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`BIGDECIMALTOBYTES`</td>
      <td>`BIGDECIMALTOBYTES(decimal)`</td>
      <td>BYTES</td>
      <td>Converts BigDecimal to bytes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`BYTESTOBIGDECIMAL`</td>
      <td>`BYTESTOBIGDECIMAL(bytes)`</td>
      <td>BIGDECIMAL</td>
      <td>Converts bytes to BigDecimal</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`HEXDECIMALTOLONG`</td>
      <td>`HEXDECIMALTOLONG(hex)`</td>
      <td>LONG</td>
      <td>Converts hex string to long</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`LONGTOHEXDECIMAL`</td>
      <td>`LONGTOHEXDECIMAL(val)`</td>
      <td>STRING</td>
      <td>Converts long to hex string</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`TOUUIDBYTES`</td>
      <td>`TOUUIDBYTES(uuid)`</td>
      <td>BYTES</td>
      <td>Converts UUID string to bytes</td>
      <td>Both</td>
    </tr>
    <tr>
      <td>`FROMUUIDBYTES`</td>
      <td>`FROMUUIDBYTES(bytes)`</td>
      <td>STRING</td>
      <td>Converts bytes to UUID string</td>
      <td>Both</td>
    </tr>
  </tbody>
</table>

---

## Window Functions

For full details, see [Window Functions](../../functions/window).

{% hint style="info" %}
Window functions require the [multi-stage query engine (v2)](../../configuration-reference/cluster.md).
{% endhint %}

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Signature</th>
      <th>Return Type</th>
      <th>Description</th>
      <th>Engine</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`ROW_NUMBER`</td>
      <td>`ROW_NUMBER() OVER (...)`</td>
      <td>LONG</td>
      <td>Sequential row number within partition</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`RANK`</td>
      <td>`RANK() OVER (...)`</td>
      <td>LONG</td>
      <td>Rank with gaps for ties</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`DENSE_RANK`</td>
      <td>`DENSE_RANK() OVER (...)`</td>
      <td>LONG</td>
      <td>Rank without gaps for ties</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`LAG`</td>
      <td>`LAG(col [, offset [, default]]) OVER (...)`</td>
      <td>varies</td>
      <td>Value from a preceding row</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`LEAD`</td>
      <td>`LEAD(col [, offset [, default]]) OVER (...)`</td>
      <td>varies</td>
      <td>Value from a following row</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`FIRST_VALUE`</td>
      <td>`FIRST_VALUE(col) OVER (...)`</td>
      <td>varies</td>
      <td>First value in the window frame</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`LAST_VALUE`</td>
      <td>`LAST_VALUE(col) OVER (...)`</td>
      <td>varies</td>
      <td>Last value in the window frame</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>[`SUM`](../../functions/aggregation/sum.md)</td>
      <td>`SUM(col) OVER (...)`</td>
      <td>DOUBLE</td>
      <td>Running/windowed sum</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>[`AVG`](../../functions/aggregation/avg.md)</td>
      <td>`AVG(col) OVER (...)`</td>
      <td>DOUBLE</td>
      <td>Running/windowed average</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>[`MIN`](../../functions/aggregation/min.md)</td>
      <td>`MIN(col) OVER (...)`</td>
      <td>DOUBLE</td>
      <td>Running/windowed minimum</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>[`MAX`](../../functions/aggregation/max.md)</td>
      <td>`MAX(col) OVER (...)`</td>
      <td>DOUBLE</td>
      <td>Running/windowed maximum</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>[`COUNT`](../../functions/aggregation/count.md)</td>
      <td>`COUNT(col) OVER (...)`</td>
      <td>LONG</td>
      <td>Running/windowed count</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`BOOL_AND`</td>
      <td>`BOOL_AND(col) OVER (...)`</td>
      <td>BOOLEAN</td>
      <td>Windowed boolean AND</td>
      <td>MSE</td>
    </tr>
    <tr>
      <td>`BOOL_OR`</td>
      <td>`BOOL_OR(col) OVER (...)`</td>
      <td>BOOLEAN</td>
      <td>Windowed boolean OR</td>
      <td>MSE</td>
    </tr>
  </tbody>
</table>
