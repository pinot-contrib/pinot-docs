# DateTime Functions

### Convert Epoch Milliseconds to other Time Granular

***

#### toEpochSeconds

Converts epoch milliseconds to epoch seconds.

**Syntax**

```
toEpochSeconds(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* LONG: Epoch timestamp in seconds.

**Example**

```sql
SELECT toEpochSeconds(1700000000000) FROM myTable
-- Returns 1700000000
```

***

#### toEpochSecondsMV

Converts an array of epoch milliseconds to epoch seconds.

**Syntax**

```
toEpochSecondsMV(millisArray)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.

**Returns**

* LONG\[]: Array of epoch timestamps in seconds.

***

#### toEpochMinutes

Converts epoch milliseconds to epoch minutes.

**Syntax**

```
toEpochMinutes(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* LONG: Epoch timestamp in minutes.

**Example**

```sql
SELECT toEpochMinutes(1700000000000) FROM myTable
-- Returns 28333333
```

***

#### toEpochMinutesMV

Converts an array of epoch milliseconds to epoch minutes.

**Syntax**

```
toEpochMinutesMV(millisArray)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.

**Returns**

* LONG\[]: Array of epoch timestamps in minutes.

***

#### toEpochHours

Converts epoch milliseconds to epoch hours.

**Syntax**

```
toEpochHours(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* LONG: Epoch timestamp in hours.

**Example**

```sql
SELECT toEpochHours(1700000000000) FROM myTable
-- Returns 472222
```

***

#### toEpochHoursMV

Converts an array of epoch milliseconds to epoch hours.

**Syntax**

```
toEpochHoursMV(millisArray)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.

**Returns**

* LONG\[]: Array of epoch timestamps in hours.

***

#### toEpochDays

Converts epoch milliseconds to epoch days.

**Syntax**

```sql
toEpochDays(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* LONG: Epoch timestamp in days.

**Example**

```sql
SELECT toEpochDays(1700000000000) FROM myTable
-- Returns 1967
```

***

#### toEpochDaysMV

Converts an array of epoch milliseconds to epoch days.

**Syntax**

```
toEpochDaysMV(millisArray)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.

**Returns**

* LONG\[]: Array of epoch timestamps in days.

***

### Round Epoch Milliseconds to other Time Granular

***

#### toEpochSecondsRounded

Converts epoch milliseconds to epoch seconds, then rounds down to the nearest specified bucket size.

**Syntax**

```
toEpochSecondsRounded(millis, roundToNearest)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* roundToNearest (LONG): Bucket size in seconds for rounding.

**Returns**

* LONG: Rounded epoch time in seconds.

**Example**

```sql
SELECT toEpochSecondsRounded(1700000001234, 60) FROM myTable
-- Returns 1700000000
```

***

#### toEpochSecondsRoundedMV

Converts an array of epoch milliseconds to epoch seconds, then rounds each to the nearest specified bucket size.

**Syntax**

```
toEpochSecondsRoundedMV(millisArray, roundToNearest)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* roundToNearest (LONG): Bucket size in seconds for rounding.

**Returns**

* LONG\[]: Array of rounded epoch timestamps in seconds.

***

#### toEpochMinutesRounded

Converts epoch milliseconds to epoch minutes, then rounds down to the nearest specified bucket size.

**Syntax**

```
toEpochMinutesRounded(millis, roundToNearest)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* roundToNearest (LONG): Bucket size in minutes for rounding.

**Returns**

* LONG: Rounded epoch time in minutes.

**Example**

```sql
SELECT toEpochMinutesRounded(1700000001234, 15) FROM myTable
-- Returns 28333320
```

***

#### toEpochMinutesRoundedMV

Converts an array of epoch milliseconds to epoch minutes, then rounds each to the nearest specified bucket size.

**Syntax**

```
toEpochMinutesRoundedMV(millisArray, roundToNearest)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* roundToNearest (LONG): Bucket size in minutes for rounding.

**Returns**

* LONG\[]: Array of rounded epoch timestamps in minutes.

***

#### toEpochHoursRounded

Converts epoch milliseconds to epoch hours, then rounds down to the nearest specified bucket size.

**Syntax**

```
toEpochHoursRounded(millis, roundToNearest)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* roundToNearest (LONG): Bucket size in hours for rounding.

**Returns**

* LONG: Rounded epoch time in hours.

**Example**

```sql
SELECT toEpochHoursRounded(1700000001234, 2) FROM myTable
-- Returns 472222
```

***

#### toEpochHoursRoundedMV

Converts an array of epoch milliseconds to epoch hours, then rounds each to the nearest specified bucket size.

**Syntax**

```
toEpochHoursRoundedMV(millisArray, roundToNearest)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* roundToNearest (LONG): Bucket size in hours for rounding.

**Returns**

* LONG\[]: Array of rounded epoch timestamps in hours.

***

#### toEpochDaysRounded

Converts epoch milliseconds to epoch days, then rounds down to the nearest specified bucket size.

**Syntax**

```
toEpochDaysRounded(millis, roundToNearest)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* roundToNearest (LONG): Bucket size in days for rounding.

**Returns**

* LONG: Rounded epoch time in days.

**Example**

```sql
SELECT toEpochDaysRounded(1700000001234, 7) FROM myTable
-- Returns 1967
```

***

#### toEpochDaysRoundedMV

Converts an array of epoch milliseconds to epoch days, then rounds each to the nearest specified bucket size.

**Syntax**

```
toEpochDaysRoundedMV(millisArray, roundToNearest)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* roundToNearest (LONG): Bucket size in days for rounding.

**Returns**

* LONG\[]: Array of rounded epoch timestamps in days.

***

### Convert Epoch Milliseconds to other Time Granular then into Buckets

***

#### toEpochSecondsBucket

Converts epoch milliseconds to epoch seconds, then divides by a bucket to compute the number of buckets since the epoch.

**Syntax**

```
toEpochSecondsBucket(millis, bucket)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* bucket (LONG): Size of each time bucket in seconds.

**Returns**

* LONG: Number of bucket-sized seconds since epoch.

**Example**

```sql
SELECT toEpochSecondsBucket(1700000001234, 60) FROM myTable
-- Returns 28333333
```

***

#### toEpochSecondsBucketMV

Converts an array of epoch milliseconds to epoch seconds, then divides each by a bucket.

**Syntax**

```
toEpochSecondsBucketMV(millisArray, bucket)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* bucket (LONG): Size of each time bucket in seconds.

**Returns**

* LONG\[]: Array of bucket-sized seconds since epoch.

***

#### toEpochMinutesBucket

Converts epoch milliseconds to epoch minutes, then divides by a bucket to compute the number of buckets since the epoch.

**Syntax**

```
toEpochMinutesBucket(millis, bucket)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* bucket (LONG): Size of each time bucket in minutes.

**Returns**

* LONG: Number of bucket-sized minutes since epoch.

**Example**

```sql
SELECT toEpochMinutesBucket(1700000001234, 5) FROM myTable
-- Returns 5666666
```

***

#### toEpochMinutesBucketMV

Converts an array of epoch milliseconds to epoch minutes, then divides each by a bucket.

**Syntax**

```
toEpochMinutesBucketMV(millisArray, bucket)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* bucket (LONG): Size of each time bucket in minutes.

**Returns**

* LONG\[]: Array of bucket-sized minutes since epoch.

***

#### toEpochHoursBucket

Converts epoch milliseconds to epoch hours, then divides by a bucket to compute the number of buckets since the epoch.

**Syntax**

```
toEpochHoursBucket(millis, bucket)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* bucket (LONG): Size of each time bucket in hours.

**Returns**

* LONG: Number of bucket-sized hours since epoch.

**Example**

```sql
SELECT toEpochHoursBucket(1700000001234, 4) FROM myTable
-- Returns 118055
```

***

#### toEpochHoursBucketMV

Converts an array of epoch milliseconds to epoch hours, then divides each by a bucket.

**Syntax**

```
toEpochHoursBucketMV(millisArray, bucket)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* bucket (LONG): Size of each time bucket in hours.

**Returns**

* LONG\[]: Array of bucket-sized hours since epoch.

***

#### toEpochDaysBucket

Converts epoch milliseconds to epoch days, then divides by a bucket to compute the number of buckets since the epoch.

**Syntax**

```
toEpochDaysBucket(millis, bucket)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* bucket (LONG): Size of each time bucket in days.

**Returns**

* LONG: Number of bucket-sized days since epoch.

**Example**

```sql
SELECT toEpochDaysBucket(1700000001234, 7) FROM myTable
-- Returns 281
```

***

#### toEpochDaysBucketMV

Converts an array of epoch milliseconds to epoch days, then divides each by a bucket.

**Syntax**

```
toEpochDaysBucketMV(millisArray, bucket)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.
* bucket (LONG): Size of each time bucket in days.

**Returns**

* LONG\[]: Array of bucket-sized days since epoch.

***

### Any Time Granular to Epoch Milliseconds

***

#### fromEpochSeconds

Converts epoch seconds to epoch milliseconds.

**Syntax**

```
fromEpochSeconds(seconds)
```

**Parameters**

* seconds (LONG): Epoch timestamp in seconds.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromEpochSeconds(1700000000) FROM myTable
-- Returns 1700000000000
```

***

#### fromEpochSecondsMV

Converts an array of epoch seconds to epoch milliseconds.

**Syntax**

```
fromEpochSecondsMV(secondsArray)
```

**Parameters**

* secondsArray (LONG\[]): Array of epoch timestamps in seconds.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### fromEpochMinutes

Converts epoch minutes to epoch milliseconds.

**Syntax**

```
fromEpochMinutes(minutes)
```

**Parameters**

* minutes (LONG): Epoch timestamp in minutes.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromEpochMinutes(28333333) FROM myTable
-- Returns 1700000000000
```

***

#### fromEpochMinutesMV

Converts an array of epoch minutes to epoch milliseconds.

**Syntax**

```
fromEpochMinutesMV(minutesArray)
```

**Parameters**

* minutesArray (LONG\[]): Array of epoch timestamps in minutes.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### fromEpochHours

Converts epoch hours to epoch milliseconds.

**Syntax**

```
fromEpochHours(hours)
```

**Parameters**

* hours (LONG): Epoch timestamp in hours

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromEpochHours(472222) FROM myTable
-- Returns 1700000000000
```

***

#### fromEpochHoursMV

Converts an array of epoch hours to epoch milliseconds.

**Syntax**

```
fromEpochHoursMV(hoursArray)
```

**Parameters**

* hoursArray (LONG\[]): Array of epoch timestamps in hours.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### fromEpochDays

Converts epoch days to epoch milliseconds.

**Syntax**

```
fromEpochDays(days)
```

**Parameters**

* days (LONG): Epoch timestamp in days.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromEpochDays(1967) FROM myTable
-- Returns 1700000000000
```

***

#### fromEpochDaysMV

Converts an array of epoch days to epoch milliseconds.

**Syntax**

```
fromEpochDaysMV(daysArray)
```

**Parameters**

* daysArray (LONG\[]): Array of epoch timestamps in days.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

### Any Bucketed Time Granular to Epoch Milliseconds

***

Converts a bucketed count of epoch seconds back to epoch milliseconds.

**Syntax**

```
fromEpochSecondsBucket(nSecondsSinceEpoch, bucket)
```

**Parameters**

* nSecondsSinceEpoch (LONG): Seconds-since-epoch divided by a bucket.
* bucket (LONG): Size of each time bucket in seconds.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromEpochSecondsBucket(28333333, 60) FROM myTable
-- Returns 1700000000000
```

***

#### fromEpochSecondsBucketMV

Converts an array of bucketed epoch seconds back to epoch milliseconds.

**Syntax**

```
fromEpochSecondsBucketMV(nSecondsArray, bucket)
```

**Parameters**

* nSecondsArray (LONG\[]): Array of bucketed epoch seconds.
* bucket (LONG): Size of each time bucket in seconds.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### fromEpochMinutesBucket

Converts a bucketed count of epoch minutes back to epoch milliseconds.

**Syntax**

```
fromEpochMinutesBucket(nMinutesSinceEpoch, bucket)
```

**Parameters**

* nMinutesSinceEpoch (LONG): Minutes-since-epoch divided by a bucket.
* bucket (LONG): Size of each time bucket in minutes.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromEpochMinutesBucket(5666666, 5) FROM myTable
-- Returns 1700000000000
```

***

#### fromEpochMinutesBucketMV

Converts an array of bucketed epoch minutes back to epoch milliseconds.

**Syntax**

```
fromEpochMinutesBucketMV(nMinutesArray, bucket)
```

**Parameters**

* nMinutesArray (LONG\[]): Array of bucketed epoch minutes.
* bucket (LONG): Size of each time bucket in minutes.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### fromEpochHoursBucket

Converts a bucketed count of epoch hours back to epoch milliseconds.

**Syntax**

```
fromEpochHoursBucket(nHoursSinceEpoch, bucket)
```

**Parameters**

* nHoursSinceEpoch (LONG): Hours-since-epoch divided by a bucket.
* bucket (LONG): Size of each time bucket in hours.

**Returns**

* LONG: Epoch timestamp in milliseconds.

***

#### fromEpochHoursBucketMV

Converts an array of bucketed epoch hours back to epoch milliseconds.

**Syntax**

```
fromEpochHoursBucketMV(nHoursArray, bucket)
```

**Parameters**

* nHoursArray (LONG\[]): Array of bucketed epoch hours.
* bucket (LONG): Size of each time bucket in hours.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### fromEpochDaysBucket

Converts a bucketed count of epoch days back to epoch milliseconds.

**Syntax**

```
fromEpochDaysBucket(nDaysSinceEpoch, bucket)
```

**Parameters**

* nDaysSinceEpoch (LONG): Days-since-epoch divided by a bucket.
* bucket (LONG): Size of each time bucket in days.

**Returns**

* LONG: Epoch timestamp in milliseconds.

***

#### fromEpochDaysBucketMV

Converts an array of bucketed epoch days back to epoch milliseconds.

**Syntax**

```
fromEpochDaysBucketMV(nDaysArray, bucket)
```

**Parameters**

* nDaysArray (LONG\[]): Array of bucketed epoch days.
* bucket (LONG): Size of each time bucket in days.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

### ISO 8601 Conversion Functions

These functions allow converting between ISO 8601 date-time strings and epoch timestamps in milliseconds.

***

#### fromIso8601

Converts an ISO 8601 date-time string to epoch milliseconds.

**Syntax**

```
fromIso8601(iso8601)
```

**Parameters**

* iso8601 (STRING): A timestamp in ISO 8601 format (e.g., '2023-08-20T13:00:00Z').

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromIso8601('2023-08-20T13:00:00Z') FROM myTable
-- Returns 1692536400000
```

***

#### fromIso8601MV

Converts an array of ISO 8601 date-time strings to epoch milliseconds.

**Syntax**

```
fromIso8601MV(iso8601Array)
```

**Parameters**

* iso8601Array (STRING\[]): Array of ISO 8601 formatted date-time strings.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

#### toIso8601

Converts epoch milliseconds to an ISO 8601 formatted string.

**Syntax**

```
toIso8601(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* STRING: ISO 8601 formatted date-time string.

**Example**

```sql
SELECT toIso8601(1692536400000) FROM myTable
-- Returns '2023-08-20T13:00:00Z'
```

***

#### toIso8601MV

Converts an array of epoch milliseconds to ISO 8601 formatted strings.

**Syntax**

```
toIso8601MV(millisArray)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.

**Returns**

* STRING\[]: Array of ISO 8601 formatted date-time strings.

***

### Timestamp Conversion Functions

These functions allow converting between Java Timestamp objects and epoch timestamps in milliseconds. They are primarily useful when interfacing with SQL-compatible UDFs or timestamp-typed columns in Pinot.

***

#### toTimestamp

Converts epoch milliseconds to a Java Timestamp object.

**Syntax**

```
toTimestamp(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* TIMESTAMP: A Java Timestamp object representing the given epoch time.

**Example**

```sql
SELECT toTimestamp(1700000000000) FROM myTable
-- Returns TIMESTAMP '2023-11-14 22:13:20.000'
```

***

#### toTimestampMV

Converts an array of epoch milliseconds to Java Timestamp objects.

**Syntax**

```
toTimestampMV(millisArray)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps in milliseconds.

**Returns**

* TIMESTAMP\[]: Array of Java Timestamp objects.

***

#### fromTimestamp

Converts a Java Timestamp to epoch milliseconds.

**Syntax**

```
fromTimestamp(timestamp)
```

**Parameters**

* timestamp (TIMESTAMP): A Java Timestamp object.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromTimestamp(TIMESTAMP '2023-11-14 22:13:20.000') FROM myTable
-- Returns 1700000000000
```

***

#### fromTimestampMV

Converts an array of Java Timestamp objects to epoch milliseconds.

**Syntax**

```
fromTimestampMV(timestampArray)
```

**Parameters**

* timestampArray (TIMESTAMP\[]): Array of Java Timestamp objects.

**Returns**

* LONG\[]: Array of epoch timestamps in milliseconds.

***

### Pattern-Based DateTime Conversion Functions

These functions allow conversions between epoch timestamps and formatted DateTime strings using custom patterns and optional time zones. Patterns must follow [Java DateTimeFormatter](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html) syntax.

***

#### toDateTime

Converts epoch milliseconds to a DateTime string using a specified pattern.

**Syntax**

```
toDateTime(millis, pattern)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* pattern (STRING): DateTime format pattern.

**Returns**

* STRING: Formatted DateTime string.

**Example**

```sql
SELECT toDateTime(1700000000000, 'yyyy-MM-dd HH:mm:ss') FROM myTable
-- Returns '2023-11-14 22:13:20'
```

***

#### toDateTimeMV

Converts an array of epoch milliseconds to formatted DateTime strings using a pattern.

**Syntax**

```
toDateTimeMV(millisArray, pattern)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps.
* pattern (STRING): DateTime format pattern.

**Returns**

* STRING\[]: Array of formatted DateTime strings.

***

#### toDateTime (with Time Zone)

Converts epoch milliseconds to a DateTime string using a specified pattern and time zone.

**Syntax**

```
toDateTime(millis, pattern, timezoneId)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.
* pattern (STRING): DateTime format pattern.
* timezoneId (STRING): Time zone ID (e.g., 'UTC', 'America/Los\_Angeles').

**Returns**

* STRING: Formatted DateTime string in the specified time zone.

**Example**

```sql
SELECT toDateTime(1700000000000, 'yyyy-MM-dd HH:mm:ss', 'America/New_York') FROM myTable
-- Returns '2023-11-14 17:13:20'
```

***

#### toDateTimeMV (with Time Zone)

Converts an array of epoch milliseconds to formatted DateTime strings using a pattern and time zone.

**Syntax**

```
toDateTimeMV(millisArray, pattern, timezoneId)
```

**Parameters**

* millisArray (LONG\[]): Array of epoch timestamps.
* pattern (STRING): DateTime format pattern.
* timezoneId (STRING): Time zone ID.

**Returns**

* STRING\[]: Array of formatted DateTime strings.

***

#### fromDateTime

Parses a DateTime string (formatted per pattern) to epoch milliseconds.

**Syntax**

```
fromDateTime(dateTimeString, pattern)
```

**Parameters**

* dateTimeString (STRING): Input DateTime string.
* pattern (STRING): DateTime format pattern.

**Returns**

* LONG: Epoch timestamp in milliseconds.

**Example**

```sql
SELECT fromDateTime('2023-11-14 22:13:20', 'yyyy-MM-dd HH:mm:ss') FROM myTable
-- Returns 1700000000000
```

***

#### fromDateTimeMV

Parses an array of formatted DateTime strings to epoch milliseconds.

**Syntax**

```
fromDateTimeMV(dateTimeArray, pattern)
```

**Parameters**

* dateTimeArray (STRING\[]): Array of DateTime strings.
* pattern (STRING): DateTime format pattern.

**Returns**

* LONG\[]: Array of epoch timestamps.

***

#### fromDateTime (with Time Zone)

Parses a DateTime string to epoch milliseconds using a specified time zone.

**Syntax**

```
fromDateTime(dateTimeString, pattern, timeZoneId)
```

**Parameters**

* dateTimeString (STRING): Input DateTime string.
* pattern (STRING): DateTime format pattern.
* timeZoneId (STRING): Time zone ID.

**Returns**

* LONG: Epoch timestamp in milliseconds.

***

#### fromDateTime (with Time Zone and Default Value)

Parses a DateTime string to epoch milliseconds using time zone and returns a default if parsing fails.

**Syntax**

```
fromDateTime(dateTimeString, pattern, timeZoneId, defaultVal)
```

**Parameters**

* dateTimeString (STRING): Input DateTime string.
* pattern (STRING): DateTime format pattern.
* timeZoneId (STRING): Time zone ID.
* defaultVal (LONG): Fallback value (in millis) if parsing fails.

**Returns**

* LONG: Epoch milliseconds or defaultVal on failure.

***

#### fromDateTimeMV (with Time Zone)

Parses an array of formatted DateTime strings to epoch milliseconds using a time zone.

**Syntax**

```
fromDateTimeMV(dateTimeArray, pattern, timeZoneId)
```

**Parameters**

* dateTimeArray (STRING\[]): Array of DateTime strings.
* pattern (STRING): DateTime format pattern.
* timeZoneId (STRING): Time zone ID.

**Returns**

* LONG\[]: Array of epoch timestamps.

***

### Generic Time Rounding Functions

These functions round time values to the nearest multiple of a given unit, useful for custom bucketing or alignment.

***

#### round

Rounds the given time value down to the nearest multiple of roundToNearest.

**Syntax**

```
round(timeValue, roundToNearest)
```

**Parameters**

* timeValue (LONG): A time value, typically in milliseconds, seconds, etc.
* roundToNearest (LONG): Unit of rounding (e.g., 60, 1000, etc.).

**Returns**

* LONG: The original value rounded down to the nearest multiple of roundToNearest.

**Example**

```sql
SELECT round(1700000000123, 1000) FROM myTable
-- Returns 1700000000000
```

***

#### roundMV

Rounds each value in an array of time values to the nearest multiple of roundToNearest.

**Syntax**

```
roundMV(timeArray, roundToNearest)
```

**Parameters**

* timeArray (LONG\[]): Array of time values.
* roundToNearest (LONG): Unit of rounding.

**Returns**

* LONG\[]: Array of rounded values.

***

### Time Utility Functions for now() and ago()

These scalar functions return or manipulate timestamps based on the current system time or durations. Useful for debugging, time-based filters, and dynamic comparisons.

***

#### now

Returns the current system time in epoch milliseconds.

**Syntax**

```
now()
```

**Parameters**

* _None_

**Returns**

* LONG: Current time in milliseconds since epoch.

**Example**

```
SELECT now() FROM myTable
-- Returns something like 1700000000000
```

***

#### sleep

Sleeps the current thread for the given number of milliseconds, returning the same value.

This function only works when assertions are enabled and is mostly intended for debugging and testing.

**Syntax**

```
sleep(millis)
```

**Parameters**

* millis (LONG): Duration to sleep (in milliseconds).

**Returns**

* LONG: Returns the same millis value after sleep completes.

***

#### ago

Returns the epoch millis representing the time before now by the given ISO-8601 duration.

**Syntax**

```
ago(periodString)
```

**Parameters**

* periodString (STRING): Duration string in ISO-8601 format (e.g., 'PT10H', 'P2DT3H4M').

**Returns**

* LONG: Epoch time in milliseconds representing now minus the given duration.

**Example**

```sql
SELECT ago('PT1H') FROM myTable
-- Returns current time minus one hour in millis
```

***

#### agoMV

Applies the ago() logic on an array of ISO-8601 duration strings.

**Syntax**

```
agoMV(periodArray)
```

**Parameters**

* periodArray (STRING\[]): Array of duration strings in ISO-8601 format.

**Returns**

* LONG\[]: Epoch times in milliseconds for each duration subtracted from current time.

***

### Time Zone Offset Functions

These functions return the hour or minute component of a time zone’s offset from UTC, based on a time zone ID. They support static (current offset) and dynamic (offset at a specific timestamp) evaluations, including daylight saving time adjustments.

> ℹ️ The timezoneId must follow [Joda-Time time zone IDs](https://www.joda.org/joda-time/timezones.html) (e.g., 'America/Los\_Angeles', 'UTC', 'Asia/Kolkata').

***

#### timezoneHour

Returns the hour offset of the specified time zone at the epoch (UTC).

**Syntax**

```
timezoneHour(timezoneId)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.

**Returns**

* INT: Hour offset from UTC (e.g., -8, 0, 5).

**Example**

```sql
SELECT timezoneHour('America/New_York') FROM myTable
-- Returns -5 or -4 depending on DST
```

***

#### timezoneHourMV

Returns the hour offset from UTC for an array of time zone IDs.

**Syntax**

```
timezoneHourMV(timezoneIdArray)
```

**Parameters**

* timezoneIdArray (STRING\[]): Array of time zone IDs.

**Returns**

* INT\[]: Hour offsets from UTC.

***

#### timezoneHour (at timestamp)

Returns the hour offset of the time zone at a specific UTC timestamp (in millis), respecting daylight saving time.

**Syntax**

```
timezoneHour(timezoneId, millis)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.
* millis (LONG): UTC timestamp in milliseconds.

**Returns**

* INT: Hour offset from UTC at that moment.

***

#### timezoneHourMV (at timestamp)

Returns hour offsets for the specified time zone ID at each of the provided timestamps.

**Syntax**

```
timezoneHourMV(timezoneId, millisArray)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.
* millisArray (LONG\[]): Array of UTC timestamps in milliseconds.

**Returns**

* INT\[]: Hour offsets at the corresponding timestamps.

***

#### timezoneMinute

Returns the minute offset of the specified time zone at the epoch (UTC).

**Syntax**

```
timezoneMinute(timezoneId)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.

**Returns**

* INT: Minute component of the time zone offset (e.g., 30 for IST, 0 for UTC).

***

#### timezoneMinuteMV

Returns minute offsets from UTC for an array of time zone IDs.

**Syntax**

```
timezoneMinuteMV(timezoneIdArray)
```

**Parameters**

* timezoneIdArray (STRING\[]): Array of time zone IDs.

**Returns**

* INT\[]: Minute components of UTC offset.

***

#### timezoneMinute (at timestamp)

Returns the minute offset of the time zone at a specific UTC timestamp (in millis), accounting for DST.

**Syntax**

```
timezoneMinute(timezoneId, millis)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.
* millis (LONG): UTC timestamp in milliseconds.

**Returns**

* INT: Minute offset from UTC at the given timestamp.

***

#### timezoneMinuteMV (at timestamp)

Returns minute offsets for the specified time zone ID at each timestamp.

**Syntax**

```
timezoneMinuteMV(timezoneId, millisArray)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.
* millisArray (LONG\[]): Array of UTC timestamps.

**Returns**

* INT\[]: Minute offsets from UTC.

***

### Date and Time Component Functions

These functions extract specific components (year, month, day, hour, etc.) from an epoch timestamp in milliseconds. They support both UTC (default) and custom time zones using [Joda-Time zone IDs](https://www.joda.org/joda-time/timezones.html). MV variants apply the same logic to arrays of timestamps.

***

#### year(millis)

Returns the calendar year in UTC.

**Syntax**

```
year(millis)
```

**Parameters**

* millis (LONG): Epoch timestamp in milliseconds.

**Returns**

* INT: Year (e.g., 2024)

***

#### year(millis, timezoneId)

Returns the calendar year in the specified time zone.

**Syntax**

```
year(millis, timezoneId)
```

**Parameters**

* timezoneId (STRING): Joda-Time-compatible time zone ID.

**Returns**

* INT: Year (e.g., 2024)

***

#### yearMV(millisArray) / yearMV(millisArray, timezoneId)

Returns years from an array of timestamps.

**Returns**

* INT\[]: Array of years

***

#### yearOfWeek(millis) / yow(millis)

Returns the ISO week-based year in UTC.

**Returns**

* INT: Week-based year (e.g., 2024)

***

#### yearOfWeek(millis, timezoneId)

Returns ISO week-based year in a specified time zone.

***

#### yearOfWeekMV(...) / yowMV(...)

Multi-value variants.

***

#### quarter(millis\[, timezoneId])

Returns the quarter of the year (1 to 4).

**Returns**

* INT: 1 = Q1, 2 = Q2, 3 = Q3, 4 = Q4

***

#### month(millis\[, timezoneId]) / monthOfYear(...)

Returns the month of the year (1 to 12).

***

#### week(millis\[, timezoneId]) / weekOfYear(...)

Returns the ISO week of the year (1 to 53).

***

#### dayOfYear(millis\[, timezoneId]) / doy(...)

Returns the day of the year (1 to 366).

***

#### dayOfMonth(millis\[, timezoneId]) / day(...)

Returns the day of the month (1 to 31).

***

#### dayOfWeek(millis\[, timezoneId]) / dow(...)

Returns the day of the week (1 = Monday to 7 = Sunday).

***

#### hour(millis\[, timezoneId])

Returns the hour of the day (0 to 23).

***

#### minute(millis\[, timezoneId])

Returns the minute of the hour (0 to 59).

***

#### second(millis\[, timezoneId])

Returns the second of the minute (0 to 59).

***

#### millisecond(millis\[, timezoneId])

Returns the millisecond of the second (0 to 999).

***

#### MV Variants

All of the above functions have MV counterparts that operate on arrays of epoch timestamps and return arrays of corresponding extracted values.

**Example**

```sql
SELECT dayOfWeekMV([1700000000000, 1700003600000], 'America/Los_Angeles')
-- Returns [3, 3] if both fall on the same Wednesday in that time zone.
```

***

### Generalized Date/Time Extraction Function

This function extracts specific components (e.g., year, month, day, hour) from a timestamp using a flexible string-based interval specifier.

***

#### extract(interval, timestamp)

Returns the specified date/time component from the given epoch timestamp.

**Syntax**

```
extract(interval, timestamp)
```

**Parameters**

* interval (STRING): The component to extract. Supported values depend on DateTimeUtils.ExtractFieldType and typically include:
  *   YEAR, QUARTER, MONTH, WEEK, DAY, DOY, DOW,

      HOUR, MINUTE, SECOND, MILLISECOND
* timestamp (LONG): The epoch time in milliseconds.

**Returns**

* INT: Extracted component as an integer.

**Examples**

```sql
SELECT extract('YEAR', 1700000000000)
-- Returns: 2023

SELECT extract('MONTH', 1700000000000)
-- Returns: 11

SELECT extract('DOW', 1700000000000)
-- Returns: 3 (Wednesday, if using ISO standard)
```

> ℹ️ This function provides a flexible alternative to the dedicated year(), month(), hour(), etc., functions when the field to extract is dynamically determined.

***

### Timestamp Truncation(DateTrunc) Functions

These functions round down (truncate) a timestamp to the start of a specified time unit (e.g., to the start of the hour, day, or month). They support flexible input/output units and optional time zone handling.

***

#### dateTrunc(unit, timeValue)

Truncates a timestamp to the start of the specified unit in UTC, returning milliseconds since epoch.

**Syntax**

```
dateTrunc(unit, timeValue)
```

**Parameters**

* unit (STRING): One of millisecond, second, minute, hour, day, week, month, quarter, year.
* timeValue (LONG): Timestamp in milliseconds.

**Returns**

* LONG: Truncated timestamp in milliseconds.

**Example**

```sql
SELECT dateTrunc('minute', 1700001234567)
-- Returns 1700001180000 (start of the minute)

SELECT dateTrunc('day', 1700001234567)
-- Returns 1700000000000 (start of the day in UTC)
```

***

#### dateTrunc(unit, timeValue, inputTimeUnit)

Truncates a timestamp using an input unit (e.g., seconds, hours). Output remains in the same unit.

**Syntax**

```
dateTrunc(unit, timeValue, inputTimeUnit)
```

**Parameters**

* inputTimeUnit (STRING): Time unit of timeValue. Values include MILLISECONDS, SECONDS, MINUTES, etc.

**Example**

```sql
SELECT dateTrunc('hour', 1700000000, 'SECONDS')
-- Returns 1700000000 (start of hour in seconds)

SELECT dateTrunc('day', 1700000000, 'SECONDS')
-- Returns: 1699910400 (start of day in seconds)
```

***

#### dateTrunc(unit, timeValue, inputTimeUnit, timezone)

Truncates timestamp to unit, considering time zone offset and DST.

**Syntax**

```
dateTrunc(unit, timeValue, inputTimeUnit, timezone)
```

**Parameters**

* timezone (STRING): Time zone ID (e.g., America/Los\_Angeles).

**Example**

```sql
SELECT dateTrunc('day', 1700000000000, 'MILLISECONDS', 'Asia/Kolkata')
-- Returns start of day in IST.
```

***

#### dateTrunc(unit, timeValue, inputTimeUnit, timezone, outputTimeUnit)

Full-featured truncation including conversion of both input and output units and time zone.

**Syntax**

```
dateTrunc(unit, timeValue, inputTimeUnit, timezone, outputTimeUnit)
```

**Example**

```sql
SELECT dateTrunc('month', 1700000000, 'SECONDS', 'America/New_York', 'SECONDS')
-- Returns start of the month in New York in seconds.
```

***

#### dateTruncMV(...)

All above variants have corresponding multi-value (MV) forms:

* dateTruncMV(unit, timeArray)
* dateTruncMV(unit, timeArray, inputTimeUnit)
* dateTruncMV(unit, timeArray, inputTimeUnit, timeZone)
* dateTruncMV(unit, timeArray, inputTimeUnit, timeZone, outputTimeUnit)

**Returns**

* LONG\[]: Array of truncated timestamps.

**Example**

```sql
SELECT dateTruncMV('minute', [1700001234567, 1700001288888])
-- Returns [1700001180000, 1700001240000]
```

***

### Date Binning Functions

These functions align a given timestamp to the nearest fixed-width time bin based on a specified duration and an origin timestamp. They are useful for windowed aggregations, histograms, or time-based bucketing.

***

#### dateBin(binWidthStr, sourceTimestamp, originTimestamp)

Aligns a sourceTimestamp to the nearest lower bin boundary of the given binWidthStr starting from the specified originTimestamp.

**Syntax**

```
dateBin(binWidthStr, sourceTimestamp, originTimestamp)
```

**Parameters**

* binWidthStr (STRING): The bin width as a duration string. Supported formats include:
  * ISO-8601 durations (e.g., 'PT15M' for 15 minutes, 'P1D' for 1 day)
  * Shortened forms (e.g., '15m', '2h', '1d') if supported by TimeUtils.convertPeriodToMillis.
* sourceTimestamp (TIMESTAMP): The timestamp to align.
* originTimestamp (TIMESTAMP): The origin (start) time for bin alignment.

**Returns**

* TIMESTAMP: Aligned timestamp that falls at the start of the corresponding bin.

***

**Examples**

```sql
-- Align 2024-01-01 12:37:00 to the nearest 15-minute bin from 2024-01-01 00:00:00
SELECT dateBin('PT15M', TIMESTAMP '2024-01-01 12:37:00', TIMESTAMP '2024-01-01 00:00:00')
-- Returns: TIMESTAMP '2024-01-01 12:30:00'

-- Align a time to the start of its 2-day bin
SELECT dateBin('P2D', TIMESTAMP '2024-01-03 10:00:00', TIMESTAMP '2024-01-01 00:00:00')
-- Returns: TIMESTAMP '2024-01-03 00:00:00'

-- Align to 1-hour bins from a non-midnight origin
SELECT dateBin('PT1H', TIMESTAMP '2024-01-01 11:47:00', TIMESTAMP '2024-01-01 06:15:00')
-- Returns: TIMESTAMP '2024-01-01 11:15:00'
```

***

### Timestamp Arithmetic Functions

These functions support performing arithmetic operations on timestamps in epoch milliseconds—such as adding durations to a timestamp or calculating the difference between two timestamps.

Multi-value (MV) variants operate over arrays of timestamps.

***

#### timestampAdd(unit, interval, timestamp)

Aliases: dateAdd

Adds a specified amount of time to a timestamp.

**Syntax**

```
timestampAdd(unit, interval, timestamp)
```

**Parameters**

*   unit (STRING): The time unit to add. Supported values include:

    milliseconds, seconds, minutes, hours, days, weeks, months, quarters, years.
* interval (LONG): The amount of time to add. Can be negative to subtract.
* timestamp (LONG): The input timestamp in epoch milliseconds.

**Returns**

* LONG: The resulting timestamp, also in epoch milliseconds.

**Examples**

```sql
-- Add 3 days to the given timestamp
SELECT timestampAdd('days', 3, 1700000000000)

-- Subtract 6 hours
SELECT timestampAdd('hours', -6, 1700000000000)
```

***

#### timestampAddMV(unit, interval, timestampArray)

Aliases: dateAddMV

Vectorized version of timestampAdd, applying the operation to an array of timestamps.

**Parameters**

* timestampArray (LONG\[]): Array of input timestamps.

**Returns**

* LONG\[]: Resulting timestamps.

**Example**

```sql
SELECT timestampAddMV('days', 1, [1700000000000, 1700086400000])
-- Returns: [1700086400000, 1700172800000]
```

***

#### timestampDiff(unit, timestamp1, timestamp2)

Aliases: dateDiff

Computes the difference between timestamp2 and timestamp1, expressed in the specified unit.

> Positive values indicate timestamp2 is later than timestamp1.

**Syntax**

```
timestampDiff(unit, timestamp1, timestamp2)
```

**Parameters**

* unit (STRING): Time unit for the result (days, hours, months, etc.).
* timestamp1 (LONG): Starting timestamp (in epoch millis).
* timestamp2 (LONG): Ending timestamp (in epoch millis).

**Returns**

* LONG: Time difference in the given unit.

**Example**

```sql
-- Difference between two timestamps in days
SELECT timestampDiff('days', ago('10D'), ago('2D'))
-- Returns: 8
```

***

#### timestampDiffMV(unit, timestampArray1, timestamp2)

Aliases: dateDiffMV

Computes the difference between each timestamp in the first array and a single second timestamp.

**Returns**

* LONG\[]: Differences in specified unit.

**Example**

```sql
SELECT timestampDiffMV('hours', [1700000000000, 1700003600000], 1700010800000)
-- Returns: [3, 2]
```

***

#### timestampDiffMVReverse(unit, timestamp1, timestampArray2)

Aliases: dateDiffMVReverse

Computes the difference between a single first timestamp and each timestamp in the second array.

**Returns**

* LONG\[]: Differences in specified unit.

**Example**

```sql
SELECT timestampDiffMVReverse('days', 1700000000000, [1700086400000, 1700172800000])
-- Returns: [1, 2]
```

***

## Additional Reference Pages

| Function | Function |
| --- | --- |
| [ago](ago.md) | [DATETIMECONVERT](datetimeconvert.md) |
| [DATETRUNC](datetrunc.md) | [day](day.md) |
| [dayOfWeek](dayofweek.md) | [dayOfYear](dayofyear.md) |
| [Extract](extract.md) | [FromDateTime](fromdatetime.md) |
| [FromEpoch](fromepoch.md) | [FromEpochBucket](fromepochbucket.md) |
| [hour](hour.md) | [millisecond](millisecond.md) |
| [minute](minute.md) | [month](month.md) |
| [now](now.md) | [quarter](quarter.md) |
| [second](second.md) | [TIMECONVERT](timeconvert.md) |
| [timezoneHour](timezonehour.md) | [timezoneMinute](timezoneminute.md) |
| [ToDateTime](todatetime.md) | [ToEpoch](toepoch.md) |
| [ToEpochBucket](toepochbucket.md) | [ToEpochRounded](toepochrounded.md) |
| [week](week.md) | [year](year.md) |
| [yearOfWeek](yearofweek.md) |  |
