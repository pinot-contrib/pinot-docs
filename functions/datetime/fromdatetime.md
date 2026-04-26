---
description: This section contains reference documentation for the FromDateTime function.
---

# FromDateTime

Converts a formatted date-time string to milliseconds, based on the provided [Joda-Time pattern](https://www.joda.org/joda-time/apidocs/org/joda/time/format/DateTimeFormat.html).

## Signature

FromDateTime(dateTimeString, pattern)

## Usage Examples

```sql
SELECT FromDateTime('2019-08-07', 'yyyy-MM-dd') AS epochMillis
FROM ignoreMe
```

| epochMillis   |
| ------------- |
| 1565136000000 |

```sql
SELECT FromDateTime(
    '2019-08-07 3:12:13 PM', 
    'yyyy-MM-dd hh:mm:ss a'
    ) AS epochMillis
FROM ignoreMe
```

| epochMillis   |
| ------------- |
| 1565190733000 |

```sql
SELECT FromDateTime(
    '2019-08-07T15:12:13', 
    'yyyy-MM-dd''T''HH:mm:ss'
    ) AS epochMillis
FROM ignoreMe
```

| epochMillis   |
| ------------- |
| 1565190733000 |

```sql
SELECT FromDateTime(
    '2019-08-07T07:12:13-0800', 
    'yyyy-MM-dd''T''HH:mm:ssZ'
    ) AS epochMillis
FROM ignoreMe
```

| epochMillis   |
| ------------- |
| 1565190733000 |

## DST Handling

When the parsed wall-clock time falls in a daylight saving time (DST) spring-forward gap (where a local time does not exist in the target timezone), `FromDateTime()` automatically shifts the time forward to the next valid instant. This behavior aligns with standard implementations in Trino, Spark, and BigQuery.

**Example:** In 2026, Africa/Cairo observes a DST transition where midnight (00:00) does not exist on April 24th, jumping directly to 01:00. Parsing with this date returns the instant for 01:00 Cairo time:

```sql
SELECT FromDateTime('2026-04-24', 'yyyy-MM-dd', 'Africa/Cairo') AS epochMillis
FROM ignoreMe
```

**Behavior Change:** The 4-argument overload `FromDateTime(ts, pattern, tz, defaultVal)` previously returned the `defaultVal` when encountering a DST-gap input. As of this change, it now returns the resolved instant instead, consistent with the 3-argument overload.

**Error Handling:** Other parsing errors (unparseable input, out-of-range field values) continue to surface as exceptions, unchanged from previous behavior.
