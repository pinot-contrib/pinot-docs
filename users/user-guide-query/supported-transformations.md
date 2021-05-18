---
description: >-
  This document contains the list of all the transformation functions supported
  by Pinot SQ
---

# Supported Transformations

## Math Functions

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
| **SQRT\(**col1**\)** | Square root of a value | `SQRT(height)` |

## String Functions

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

## DateTime Functions

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
      <td style="text-align:left">Converts the value into another time unit. the column should be an epoch
        timestamp. Supported units are
        <br /><code>DAYS HOURS MINUTES SECONDS  MILLISECONDS MICROSECONDS NANOSECONDS</code>
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
          buckets time based on the given time granularity. Note that, for weeks/months/quarters/years,
          please use function: <b>DateTrunc</b>.</p>
        <p>The format is expressed as <code>&lt;time size&gt;:&lt;time unit&gt;:&lt;time format&gt;:&lt;pattern&gt;</code>
          <br
          />where,</p>
        <p><b><code>time size</code></b> - size of the time unit eg: 1, 10</p>
        <p><b><code>time unit</code></b> - <code>DAYS HOURS MINUTES SECONDS  MILLISECONDS MICROSECONDS NANOSECONDS</code> 
        </p>
        <p><b><code>time format</code></b> - <code>EPOCH</code> or <code>SIMPLE_DATE_FORMAT</code>
        </p>
        <p><code>pattern</code> - this is defined in case of <code>SIMPLE_DATE_FORMAT</code> eg: <code>yyyy-MM-dd</code>.
          A specific timezone can be passed using tz(timezone). Timezone can be long
          or short string format timezone. e.g. <code>Asia/Kolkata</code> or <code>PDT</code>
        </p>
        <p><b><code>granularity</code></b>  <b>-</b> specified in the format<code>&lt;time size&gt;:&lt;time unit&gt;</code>
        </p>
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
    <tr>
      <td style="text-align:left"><b>ToEpoch&lt;TIME_UNIT&gt;(timeInMillis)</b>
      </td>
      <td style="text-align:left">Convert epoch milliseconds to epoch &lt;Time Unit&gt;. Supported &lt;Time
        Unit&gt;: <code>SECONDS/MINUTES/HOURS/DAYS</code>
      </td>
      <td style="text-align:left">
        <p><code>ToEpochSeconds(tsInMillis):</code>Converts column <code>tsInMillis</code> value
          from epoch milliseconds to epoch seconds.</p>
        <p><code>ToEpochDays(tsInMillis):</code>Converts column <code>tsInMillis</code> value
          from epoch milliseconds to epoch days.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>ToEpoch&lt;TIME_UNIT&gt;Rounded(timeInMillis, bucketSize)</b>
      </td>
      <td style="text-align:left">Convert epoch milliseconds to epoch &lt;Time Unit&gt;, round to nearest
        rounding bucket(Bucket size is defined in &lt;Time Unit&gt;). Supported
        &lt;Time Unit&gt;: <code>SECONDS/MINUTES/HOURS/DAYS</code>
      </td>
      <td style="text-align:left">
        <p><code>ToEpochSecondsRound(tsInMillis, 10):</code>Converts column <code>tsInMillis</code> value
          from epoch milliseconds to epoch seconds and round to the 10-minute bucket
          value. E.g.<code>ToEpochSecondsRound(</code>1613472303000, 10) = 1613472300</p>
        <p></p>
        <p><code>ToEpochMinutesRound(tsInMillis, 1440):</code>Converts column <code>tsInMillis</code> value
          from epoch milliseconds to epoch Minutes, but round to 1-day bucket value.
          E.g.<code>ToEpochMinutesRound(</code>1613472303000, 1440) = 26890560</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>ToEpoch&lt;TIME_UNIT&gt;Bucket(timeInMillis, bucketSize)</b>
      </td>
      <td style="text-align:left">Convert epoch milliseconds to epoch &lt;Time Unit&gt;, and divided by
        bucket size(Bucket size is defined in &lt;Time Unit&gt;). Supported &lt;Time
        Unit&gt;: <code>SECONDS/MINUTES/HOURS/DAYS</code>
      </td>
      <td style="text-align:left">
        <p><code>ToEpochSecondsBucket(tsInMillis, 10):</code>Converts column <code>tsInMillis</code> value
          from epoch milliseconds to epoch seconds then divide by 10 to get the 10
          seconds since epoch value. E.g.</p>
        <p><code>ToEpochSecondsBucket(</code>1613472303000, 10) = 161347230</p>
        <p><code>ToEpochHoursBucket(tsInMillis, 24):</code>Converts column <code>tsInMillis</code> value
          from epoch milliseconds to epoch Hours, then divide by 24 to get 24 hours
          since epoch value.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>FromEpoch&lt;TIME_UNIT&gt;(timeIn&lt;Time_UNIT&gt;)</b>
      </td>
      <td style="text-align:left">Convert epoch &lt;Time Unit&gt; to epoch milliseconds. Supported &lt;Time
        Unit&gt;: <code>SECONDS/MINUTES/HOURS/DAYS</code>
      </td>
      <td style="text-align:left">
        <p><code>FromEpochSeconds(tsInSeconds):</code>Converts column <code>tsInSeconds</code> value
          from epoch seconds to epoch milliseconds. E.g.</p>
        <p><code>FromEpochSeconds(</code>1613472303) = 1613472303000</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>FromEpoch&lt;TIME_UNIT&gt;Bucket(timeIn&lt;Time_UNIT&gt;, bucketSizeIn&lt;Time_UNIT&gt;)</b>
      </td>
      <td style="text-align:left">Convert epoch &lt;Bucket Size&gt;&lt;Time Unit&gt; to epoch milliseconds.
        E.g. 10 seconds since epoch or 5 minutes since Epoch. Supported &lt;Time
        Unit&gt;: <code>SECONDS/MINUTES/HOURS/DAYS</code>
      </td>
      <td style="text-align:left">
        <p><code>FromEpochSecondsBucket(tsInSeconds, 10):</code>Converts column <code>tsInSeconds</code> value
          from epoch 10-seconds to epoch milliseconds. E.g.</p>
        <p><code>FromEpochSeconds(161347231)= 1613472310000</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>ToDateTime(timeInMillis, pattern)</b>
      </td>
      <td style="text-align:left">Convert epoch millis value to DateTime string represented by pattern.</td>
      <td
      style="text-align:left"><code>ToDateTime(tsInMillis, &apos;yyyy-MM-dd&apos;)</code>converts tsInMillis
        value to date time pattern <code>yyyy-MM-dd</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>FromDateTime(dateTimeString, pattern)</b>
      </td>
      <td style="text-align:left">Convert DateTime string represented by pattern to epoch millis.</td>
      <td
      style="text-align:left"><code>FromDateTime(dateTime, &apos;yyyy-MM-dd&apos;)</code>converts <code>dateTime</code> string
        value to millis epoch value</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>round(timeValue, bucketSize)</b>
      </td>
      <td style="text-align:left">Round the given time value to nearest bucket start value.</td>
      <td style="text-align:left"><code>round(tsInSeconds, 60)</code> round seconds epoch value to the start
        value of the 60 seconds bucket it belongs to. E.g. <code>round(161347231, 60)= 161347200</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>now()</b>
      </td>
      <td style="text-align:left">Return current time as epoch millis</td>
      <td style="text-align:left">Typically used in predicate to filter on timestamp for recent data. E.g.
        filter data on recent 1 day(86400 seconds).<code>WHERE tsInMillis &gt; now() - 86400000</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>timezoneHour(timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the hour of the time zone offset.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>timezoneMinute(timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the minute of the time zone offset.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>year(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the year from the given epoch millis in UTC timezone.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>year(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the year from the given epoch millis and timezone id.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>yearOfWeek(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the year of the ISO week from the given epoch millis in UTC timezone.
        Alias <code>yow</code>is also supported.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>yearOfWeek(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the year of the ISO week from the given epoch millis and timezone
        id. Alias <code>yow</code>is also supported.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>quarter(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the quarter of the year from the given epoch millis in UTC timezone.
        The value ranges from 1 to 4.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>quarter(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the quarter of the year from the given epoch millis and timezone
        id. The value ranges from 1 to 4.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>month(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the month of the year from the given epoch millis in UTC timezone.
        The value ranges from 1 to 12.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>month(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the month of the year from the given epoch millis and timezone
        id. The value ranges from 1 to 12.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>week(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the ISO week of the year from the given epoch millis in UTC timezone.
        The value ranges from 1 to 53. Alias <code>weekOfYear</code> is also supported.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>week(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the ISO week of the year from the given epoch millis and timezone
        id. The value ranges from 1 to 53. Alias <code>weekOfYear</code> is also
        supported.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>dayOfYear(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the day of the year from the given epoch millis in UTC timezone.
        The value ranges from 1 to 366. Alias <code>doy</code> is also supported.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>dayOfYear(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the day of the year from the given epoch millis and timezone id.
        The value ranges from 1 to 366. Alias <code>doy</code> is also supported.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>day(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the day of the month from the given epoch millis in UTC timezone.
        The value ranges from 1 to 31. Alias <code>dayOfMonth</code> is also supported.</td>
      <td
      style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>day(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the day of the month from the given epoch millis and timezone
        id. The value ranges from 1 to 31. Alias <code>dayOfMonth</code> is also
        supported.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>dayOfWeek(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the day of the week from the given epoch millis in UTC timezone.
        The value ranges from 1(Monday) to 7(Sunday). Alias <code>dow</code> is also
        supported.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>dayOfWeek(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the day of the week from the given epoch millis and timezone id.
        The value ranges from 1(Monday) to 7(Sunday). Alias <code>dow</code> is also
        supported.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>hour(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the hour of the day from the given epoch millis in UTC timezone.
        The value ranges from 0 to 23.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>hour(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the hour of the day from the given epoch millis and timezone id.
        The value ranges from 0 to 23.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>minute(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the minute of the hour from the given epoch millis in UTC timezone.
        The value ranges from 0 to 59.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>minute(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the minute of the hour from the given epoch millis and timezone
        id. The value ranges from 0 to 59.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>second(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the second of the minute from the given epoch millis in UTC timezone.
        The value ranges from 0 to 59.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>second(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the second of the minute from the given epoch millis and timezone
        id. The value ranges from 0 to 59.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>millisecond(tsInMillis)</b>
      </td>
      <td style="text-align:left">Returns the millisecond of the second from the given epoch millis in UTC
        timezone. The value ranges from 0 to 999.</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>millisecond(tsInMillis, timeZoneId)</b>
      </td>
      <td style="text-align:left">Returns the millisecond of the second from the given epoch millis and
        timezone id. The value ranges from 0 to 999.</td>
      <td style="text-align:left"></td>
    </tr>
  </tbody>
</table>



## JSON Functions

<table>
  <thead>
    <tr>
      <th style="text-align:left"><b>Function</b>
      </th>
      <th style="text-align:left">Type</th>
      <th style="text-align:left"><b>Description</b>
      </th>
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
      <td style="text-align:left">Transform</td>
      <td style="text-align:left">
        <p>Evaluates the <code>&apos;jsonPath&apos;</code> on <code>jsonField,</code>
        </p>
        <p>returns the result as the type <code>&apos;resultsType&apos;.</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p><b>JSONEXTRACTKEY</b>
        </p>
        <p><b>(</b>jsonField, &apos;jsonPath&apos;<b>)</b>
        </p>
      </td>
      <td style="text-align:left">Transform</td>
      <td style="text-align:left">
        <p>Extracts all matched JSON field keys based on <code>&apos;jsonPath&apos;</code>
        </p>
        <p>Into a<code>STRING_ARRAY.</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>TOJSONMAPSTR</b>(map)</td>
      <td style="text-align:left">Scalar</td>
      <td style="text-align:left">Convert map to JSON String</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>JSONFORMAT</b>(object)</td>
      <td style="text-align:left">Scalar</td>
      <td style="text-align:left">Convert object to JSON String</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>JSONPATH</b>(jsonField, &apos;jsonPath&apos;)</td>
      <td style="text-align:left">Scalar</td>
      <td style="text-align:left">Extracts the object value from <code>jsonField</code> based on <code>&apos;jsonPath&apos;</code>,
        the result type is inferred based on JSON value.</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>JSONPATHLONG</b>(jsonField, &apos;jsonPath&apos;, [defaultValue])</td>
      <td
      style="text-align:left">Scalar</td>
        <td style="text-align:left">Extracts the <b>Long</b> value from <code>jsonField</code> based on <code>&apos;jsonPath&apos;</code>,
          use optional <code>defaultValue</code>for null or parsing error.</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>JSONPATHDOUBLE</b>(jsonField, &apos;jsonPath&apos;, [defaultValue])</td>
      <td
      style="text-align:left">Scalar</td>
        <td style="text-align:left">Extracts the <b>Double</b> value from <code>jsonField</code> based on <code>&apos;jsonPath&apos;</code>,
          use optional <code>defaultValue</code>for null or parsing error.</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>JSONPATHSTRING</b>(jsonField, &apos;jsonPath&apos;, [defaultValue])</td>
      <td
      style="text-align:left">Scalar</td>
        <td style="text-align:left">Extracts the <b>String</b> value from <code>jsonField</code> based on <code>&apos;jsonPath&apos;</code>,
          use optional <code>defaultValue</code>for null or parsing error.</td>
    </tr>
    <tr>
      <td style="text-align:left"><b>JSONPATHARRAY</b>(jsonField, &apos;jsonPath&apos;)</td>
      <td style="text-align:left">Scalar</td>
      <td style="text-align:left">Extracts an array from <code>jsonField</code> based on <code>&apos;jsonPath&apos;</code>,
        the result type is inferred based on JSON value.</td>
    </tr>
  </tbody>
</table>

**Usage**

<table>
  <thead>
    <tr>
      <th style="text-align:left"><b><code>Arguments</code></b>
      </th>
      <th style="text-align:left"><b>Description</b>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><code>jsonField</code>
      </td>
      <td style="text-align:left">An <b>Identifier</b>/<b>Expression</b> contains JSON documents.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>&apos;jsonPath&apos;</code>
      </td>
      <td style="text-align:left">Follows <a href="https://goessner.net/articles/JsonPath/">JsonPath Syntax</a> to
        read values from JSON documents.</td>
    </tr>
    <tr>
      <td style="text-align:left"><code>&apos;results_type&apos;</code>
      </td>
      <td style="text-align:left">
        <p>One of the Pinot supported data types:<b><code>INT, LONG, FLOAT, DOUBLE, STRING,</code></b>
        </p>
        <p><b><code>INT_ARRAY, LONG_ARRAY, FLOAT_ARRAY, DOUBLE_ARRAY, STRING_ARRAY</code></b><code>.</code>
        </p>
      </td>
    </tr>
  </tbody>
</table>

{% hint style="warning" %}
**`'jsonPath'`**`and`**`'results_type'`**are **Literals.** Pinot uses single quotes to distinguish it from **Identifiers**.
{% endhint %}

{% hint style="warning" %}
**Transform** functions can only be used in Pinot SQL. **Scalar** functions can be used in table ingestion configs for column transformation.
{% endhint %}

E.g:

* `JSONEXTRACTSCALAR(profile_json_str, '$.name', 'STRING')`  is **Valid**.
* `JSONEXTRACTSCALAR(profile_json_str, "$.name", "STRING")`  is **Invalid**.

**Examples**

Below examples are based on 3 sample profile JSON documents:

```text
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

```text
SELECT
    JSONEXTRACTSCALAR(profile_json_str, '$.name', 'STRING')
FROM
    myTable
```

Results are

```text
["Bob", "Alice", "Mia"]
```

Query 2: Extract integer values from the field 'age'

```text
SELECT
    JSONEXTRACTSCALAR(profile_json_str, '$.age', 'INT')
FROM
    myTable
```

Results are

```text
[37, 25, 18]
```

Query 3: Extract Bob's age from the JSON profile.

```text
SELECT
    JSONEXTRACTSCALAR(myMapStr,'$.age','INT')
FROM
    myTable
WHERE
    JSONEXTRACTSCALAR(myMapStr,'$.name','STRING') = 'Bob'
```

Results are

```text
[37]
```

Query 4: Extract all field keys of JSON profile.

```text
SELECT
    JSONEXTRACTKEY(myMapStr,'$.*')
FROM
    myTable
```

Results are

```text
["name", "age", "gender", "location"]
```

Another **example** of extracting JSON fields from below JSON record:

```text
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

| Expression | Value |
| :--- | :--- |
| `JSONPATH(myJsonRecord, '$.name')` | `"Pete"` |
| `JSONPATH(myJsonRecord, '$.age')` | `24` |
| `JSONPATHSTRING(myJsonRecord, '$.age')` | `"24"` |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].name')` | `["maths", "english"]` |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].score')` | `[90, 70]` |
| `JSONPATHARRAY(myJsonRecord, '$.subjects[*].homework_grades[1]')` | `[85, 65]` |

## Binary Functions

| Function | Description | Example |
| :--- | :--- | :--- |
| **SHA\(**bytesCol**\)** | Return SHA-1 digest of binary column\(`bytes` type\) as hex string | `SHA(rawData)` |
| **SHA256\(**bytesCol**\)** | Return SHA-256 digest of binary column\(`bytes` type\) as hex string | `SHA256(rawData)` |
| **SHA512\(**bytesCol**\)** | Return SHA-512 digest of binary column\(`bytes` type\) as hex string | `SHA512(rawData)` |
| **MD5\(**bytesCol**\)** | Return MD5 digest of binary column\(`bytes` type\) as hex string | `MD5(rawData)` |

## Multi-value Column Functions

All of the functions mentioned till now only support single value columns. You can use the following functions to do operations on multi-value columns.

| Function | Description | Example |
| :--- | :--- | :--- |
| **ARRAYLENGTH** | Returns the length of a multi-value column |  |
| **MAP\_VALUE** | Select the value for a key from Map stored in Pinot. | `MAP_VALUE(mapColumn, 'myKey', valueColumn)` |
| **VALUEIN** | Takes at least 2 arguments, where the first argument is a multi-valued column, and the following arguments are constant values. The transform function will filter the value from the multi-valued column with the given constant values. The `VALUEIN` transform function is especially useful when the same multi-valued column is both filtering column and grouping column. | `VALUEIN(mvColumn, 3, 5, 15)` |

## Advanced Queries

### Geospatial Queries

Pinot supports Geospatial queries on columns containing text-based geographies. Check out [Geospatial](../../basics/indexing/geospatial-support.md) for more details on the queries and how to enable them.

### Text Queries

Pinot supports Pattern matching on text-based columns as well. Only the columns mentioned as text columns in table config can be queried using this method. Check out [Text search support](../../basics/indexing/text-search-support.md) for more details on how to enable pattern matching.

