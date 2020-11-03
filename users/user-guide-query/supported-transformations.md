---
description: >-
  This document contains the list of all the transformation functions supported
  by Pinot Query Language (PQL).
---

# Supported Transformations

### Math Functions

| Function | Description | Example |
| :--- | :--- | :--- |
| **ADD\(**col1, col2, col3...**\)** | Sum of at least two values | `ADD(score_maths, score_science, score_history)` |
| **SUB\(**col1, col2**\)** | Difference between two values | `SUB(total_score, score_science)` |
| **MULT\(**col1, col2, col3...**\)** | Product of at least two values | `MUL(score_maths, score_science, score_history)` |
| **DIV\(**col1, col2**\)** | Quotient of two values | `SUB(total_score, total_subjects)` |
| **MOD\(**col1, col2\) | Modulo of two values | `MOD(total_score, total_subjects)` |
| **ABS\(**col1**\)** | Absolute of a value | `ABS(score)` |
| **CEIL\(**col1**\)** | Rounded up to the nearest integer. | `CEIL(percentage)` |
| **FLOOR\(**col1**\)** | Rounded down to the nearest integer. | `FLOOR(percentage)` |
| **EXP\(**col1**\)** | Euler’s number\(e\) raised to the power of col. | `EXP(age)` |
| **LN\(**col1**\)** | Natural log of value i.e. ln\(col1\) | `LN(age)` |
| **SQRT\(**col1**\)** | Square root of a value  | `SQRT(height)` |

### 

### String Functions

Multiple string functions are supported out of the box from release-0.5.0 .

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><b>UPPER</b>(col)</td>
      <td style="text-align:left">convert string to upper case</td>
      <td style="text-align:left"><code>UPPER(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>LOWER</b>(col)</td>
      <td style="text-align:left">convert string to lower case</td>
      <td style="text-align:left"><code>LOWER(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>REVERSE</b>(col)</td>
      <td style="text-align:left">reverse the string</td>
      <td style="text-align:left"><code>REVERSE(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>SUBSTR</b>(col, startIndex, endIndex)</td>
      <td style="text-align:left">get substring of the input string from start to endIndex.
        <br />Index begins at 0.
        <br />Set endIndex to -1 to calculate till end of the string</td>
      <td style="text-align:left">
        <p><code>SUBSTR(playerName, 1, -1)</code>
        </p>
        <p>&lt;code&gt;&lt;/code&gt;</p>
        <p><code>SUBSTR(playerName, 1, 4)</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>CONCAT</b>(col1, col2, seperator)</td>
      <td style="text-align:left">Concatenate two input strings using the seperator</td>
      <td style="text-align:left"><code>CONCAT(firstName, lastName, &apos;-&apos;)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>TRIM</b>(col)</td>
      <td style="text-align:left">trim spaces from both side of the string</td>
      <td style="text-align:left"><code>TRIM(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>LTRIM</b>(col)</td>
      <td style="text-align:left">trim spaces from left side of the string</td>
      <td style="text-align:left"><code>LTRIM(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>RTRIM</b>(col)</td>
      <td style="text-align:left">trim spaces from right side of the string</td>
      <td style="text-align:left"><code>RTRIM(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>LENGTH</b>(col)</td>
      <td style="text-align:left">calculate length of the string</td>
      <td style="text-align:left"><code>LENGTH(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>STRPOS</b>(col, find, N)</td>
      <td style="text-align:left">find Nth instance of <code>find</code> string in input.
        <br />Returns 0 if input string is empty. Returns -1 if the Nth instance is
        not found or input string is null.</td>
      <td style="text-align:left"><code>STRPOS(playerName, &apos;david&apos;, 1)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>STARTSWITH</b>(col, prefix)</td>
      <td style="text-align:left">returns <code>true</code> if columns starts with prefix string.</td>
      <td
      style="text-align:left"><code>STARTSWITH(playerName, &apos;david&apos;)</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>REPLACE</b>(col, find, substitute)</td>
      <td style="text-align:left">replace all instances of <code>find</code> with <code>replace</code> in input</td>
      <td
      style="text-align:left"><code>REPLACE(playerName, &apos;david&apos;, &apos;henry&apos;)</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>RPAD</b>(col, size, pad)</td>
      <td style="text-align:left">string padded from the right side with <code>pad</code> to reach final <code>size</code>
      </td>
      <td style="text-align:left"><code>RPAD(playerName, 20, &apos;foo&apos;)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>LPAD</b>(col, size, pad)</td>
      <td style="text-align:left">string padded from the left side with <code>pad</code> to reach final <code>size</code>
      </td>
      <td style="text-align:left"><code>LPAD(playerName, 20, &apos;foo&apos;)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>CODEPOINT</b>(col)</td>
      <td style="text-align:left">the Unicode codepoint of the first character of the string</td>
      <td style="text-align:left"><code>CODEPOINT(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>CHR</b>(codepoint)</td>
      <td style="text-align:left">the character corresponding to the Unicode codepoint</td>
      <td style="text-align:left"><code>CHR(68)</code>
      </td>
    </tr>
  </tbody>
</table>

### 

### DateTime Functions

Date time functions allow you to perform transformations on columns which contains timestamps or date.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><b>TIMECONVERT</b>
        </p>
        <p><b>(</b>col, fromUnit, toUnit<b>)</b>
        </p>
      </td>
      <td style="text-align:left">converts the value into another time unit. column should be timestamp.
        Supported units are
        <br /><code>DAYS HOURS MICROSECONDS MILLISECONDS MINUTES NANOSECONDS SECONDS </code>
      </td>
      <td style="text-align:left"><code>TIMECONVERT(time, &apos;MILLISECONDS&apos;, &apos;SECONDS&apos;)</code>This
        expression converts the value of column <code>time</code> (taken to be in
        milliseconds) to the nearest seconds (<em>i.e.</em> the nearest seconds
        that is lower than the value of <code>date</code> column)</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><b>DATETIMECONVERT</b>
        </p>
        <p>(columnName, inputFormat, outputFormat, outputGranularity)</p>
      </td>
      <td style="text-align:left">
        <p>Takes 4 arguments, converts the value into another date time format, and
          buckets time based on the given time granularity.</p>
        <p></p>
        <p>Format is expressed as <code>&lt;time size&gt;:&lt;time unit&gt;:&lt;time format&gt;:&lt;pattern&gt;</code>
          <br
          />where,</p>
        <p><b><code>time size</code></b> - size of the time unit eg: 1, 10</p>
        <p><b><code>time unit</code></b> - <code>HOURS</code>, <code>DAYS</code> etc</p>
        <p><b><code>time format</code></b> - <code>EPOCH</code> or <code>SIMPLE_DATE_FORMAT</code>
        </p>
        <p><code>pattern</code> - <b> </b>this is defined in case of <code>SIMPLE_DATE_FORMAT</code> eg: <code>yyyy-MM-dd</code>.
          A specific timezone can be passed using tz(timezone). Timezone can be long
          or short string format timezone. e.g. <code>Asia/Kolkata</code> or <code>PDT</code>
        </p>
        <p></p>
        <p><b><code>granularity</code></b>  <b>- </b> specified in format<code>&lt;time size&gt;:&lt;time unit&gt;</code>
        </p>
        <p></p>
      </td>
      <td style="text-align:left">
        <ul>
          <li><code>Date</code> from <code>hoursSinceEpoch</code> to <code>daysSinceEpoch</code> and
            bucket it to 1 day granularity
            <br />
            <br /><code>DATETIMECONVERT(Date, &apos;1:HOURS:EPOCH&apos;, &apos;1:DAYS:EPOCH&apos;, &apos;1:DAYS&apos;)<br /></code>
          </li>
          <li> <code>Date</code> to 15 minutes granularity
            <br />
            <br /><code>DATETIMECONVERT(Date, &apos;1:MILLISECONDS:EPOCH&apos;, &apos;1:MILLISECONDS:EPOCH&apos;, &apos;15:MINUTES&apos;)<br /></code>
          </li>
          <li> <code>Date</code> from <code>hoursSinceEpoch</code> to format <code>yyyyMdd</code> and
            bucket it to 1 days granularity
            <br />
            <br /><code>DATETIMECONVERT(Date, &apos;1:HOURS:EPOCH&apos;, &apos;1:DAYS:SIMPLE_DATE_FORMAT:yyyyMMdd&apos;, &apos;1:DAYS&apos;)<br /></code>
          </li>
          <li><code>Date</code> from format <code>yyyy/MM/dd</code> to <code>weeksSinceEpoch</code> and
            bucket it to 1 week granularity
            <br />
            <br /><code>DATETIMECONVERT(Date, &apos;1:DAYS:SIMPLE_DATE_FORMAT:yyyy/MM/dd&apos;, &apos;1:WEEKS:EPOCH&apos;, &apos;1:WEEKS&apos;)</code>
            <br
            />
          </li>
          <li> <code>Date</code> from milliseconds to format <code>yyyyMdd</code> in timezone
            PST
            <br />
            <br /><code>DATETIMECONVERT(Date, &apos;1:MILLISECONDS:EPOCH&apos;, &apos;1:DAYS:SIMPLE_DATE_FORMAT:yyyyMMdd tz(America/Los_Angeles)&apos;, &apos;1:DAYS&apos;)</code>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DATETRUNC</b>
      </td>
      <td style="text-align:left">
        <p>(Presto) SQL compatible date truncation, equivalent to the Presto function
          <a
          href="https://mode.com/blog/date-trunc-sql-timestamp-function-count-on">date_trunc</a>.
            <br />
        </p>
        <p>Takes at least 3 and upto 5 arguments, converts the value into a specified
          output granularity seconds since UTC epoch that is bucketed on a unit in
          a specified timezone.</p>
      </td>
      <td style="text-align:left">
        <p><code>DATETRUNC(&apos;week&apos;, time_in_seconds, &apos;SECONDS&apos;)</code> This
          expression converts the column <code>time_in_seconds</code>, which is a
          long containing seconds since UTC epoch truncated at <code>WEEK</code> (where
          a Week starts at Monday UTC midnight). The output is a long seconds since
          UTC epoch.
          <br />
        </p>
        <p><code>DATETRUNC(&apos;quarter&apos;, DIV(time_milliseconds/1000), &apos;SECONDS&apos;, &apos;America/Los_Angeles&apos;, &apos;HOURS&apos;)</code> This
          expression converts the expression <code>time_in_milliseconds/1000</code>into
          hours that are truncated to <code>QUARTER</code> at the Los Angeles time
          zone (where a Quarter begins on 1/1, 4/1, 7/1, 10/1 in Los Angeles timezone).
          The output is expressed as hours since UTC epoch (note that the output
          is not Los Angeles timezone)</p>
      </td>
    </tr>
  </tbody>
</table>

### 

### JSON Functions

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">
        <p><b>JSONEXTRACTSCALAR</b>
        </p>
        <p><b>(</b>jsonField, &apos;jsonPath&apos;, &apos;resultsType&apos;<b>)</b>
        </p>
      </td>
      <td style="text-align:left">
        <p>Evaluates the <code>jsonPath</code> on <code>jsonField</code> (a string containing
          JSON) and returns the result as a type <code>resultsType</code>
        </p>
        <p><code>jsonFieldName</code> is a String field with Json document.</p>
        <p>&lt;del&gt;&lt;/del&gt;</p>
        <p><code>jsonPath</code> is a <a href="https://goessner.net/articles/JsonPath/">JsonPath expression</a> to
          read from JSON document</p>
        <p><code>results_type - </code>can be <code>INT</code>, <code>LONG</code>, <code>FLOAT</code>, <code>DOUBLE</code>, <code>STRING</code>, <code>INT_ARRAY</code>, <code>LONG_ARRAY</code>, <code>FLOAT_ARRAY</code>, <code>DOUBLE_ARRAY</code>, <code>STRING_ARRAY</code>.</p>
        <p>&lt;code&gt;&lt;/code&gt;</p>
      </td>
      <td style="text-align:left">
        <ul>
          <li><code>JSONEXTRACTSCALAR(profile_json_str, &apos;$.name&apos;, &apos;STRING&apos;) -&gt; &quot;bob&quot;</code>
          </li>
          <li><code>JSONEXTRACTSCALAR(profile_json_str, &apos;$.age&apos;, &apos;INT&apos;) -&gt; 37</code>
          </li>
        </ul>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><b>JSONEXTRACTKEY</b>
        </p>
        <p><b>(</b>jsonField, &apos;jsonPath&apos;<b>)</b>
        </p>
      </td>
      <td style="text-align:left">
        <p> <code>E</code>xtracts all field names based on <code>jsonPath</code> as
          a <code>STRING_ARRAY.</code>
        </p>
        <p><code>jsonFieldName</code> is a String field with Json document.</p>
        <p><code>jsonPath</code> is a <a href="https://goessner.net/articles/JsonPath/">JsonPath expression</a> to
          read from JSON document</p>
      </td>
      <td style="text-align:left"><code>JSONEXTRACTSCALAR(profile_json_str, &apos;$.*&apos;) -&gt; [&quot;name&quot;, &quot;age&quot;, &quot;phone&quot;...]</code>
      </td>
    </tr>
  </tbody>
</table>

### 

### Binary Functions

| Function | Description | Example |
| :--- | :--- | :--- |
| **SHA\(**bytesCol**\)** | Return SHA-1 digest of binary column(`bytes` type) as hex string | `SHA(rawData)` |
| **SHA256\(**bytesCol**\)** | Return SHA-256 digest of binary column(`bytes` type) as hex string | `SHA256(rawData)` |
| **SHA512\(**bytesCol**\)** | Return SHA-512 digest of binary column(`bytes` type) as hex string | `SHA512(rawData)` |
| **MD5\(**bytesCol**\)** | Return MD5 digest of binary column(`bytes` type) as hex string | `MD5(rawData)` |


### 

### Multi-value Column Functions

All of the functions mentioned till now only support single value columns. You can use the following functions to do operations on multi-value columns.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><b>ARRAYLENGTH</b>
      </td>
      <td style="text-align:left">Returns the length of a multi-value column</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MAP_VALUE</b>
      </td>
      <td style="text-align:left">Select the value for a key from Map stored in Pinot.</td>
      <td style="text-align:left"><code>MAP_VALUE(mapColumn, &apos;myKey&apos;, valueColumn)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>VALUEIN</b>
      </td>
      <td style="text-align:left">Takes at least 2 arguments, where the first argument is a multi-valued
        column, and the following arguments are constant values. The transform
        function will filter the value from the multi-valued column with the given
        constant values. The <code>VALUEIN</code> transform function is especially
        useful when the same multi-valued column is both filtering column and grouping
        column.</td>
      <td style="text-align:left">
        <p></p>
        <p><code>VALUEIN(mvColumn, 3, 5, 15)</code>
        </p>
        <p></p>
      </td>
    </tr>
  </tbody>
</table>

### Advanced Queries

#### Geospatial Queries

Pinot supports Geospatial queries on columns containing text-based geographies. Check out [Geospatial](../../basics/indexing/geospatial-support.md) for more details on the queries and how to enable them.  


#### Text Queries

Pinot supports Pattern matching on text-based columns as well. Only the columns mentioned as text columns in table config can be queried using this method. Check out [Text search support](../../basics/indexing/text-search-support.md) for more details on how to enable pattern matching.



