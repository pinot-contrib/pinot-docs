---
description: This section contains reference documentation for the toEpochBucket functions.
---

# ToEpochBucket

Convert epoch milliseconds to epoch , and divided by bucket size (Bucket size is defined in ). The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> ToEpoch\<TIME\_UNIT>Bucket(timeInMillis, bucketSize)

## Usage Examples

```sql
select ToEpochSecondsBucket(1613472303000, 1000) AS bucket
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>bucket</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1613472</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochMinutesBucket(1613472303000, 10) AS bucket
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>bucket</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2689120</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochHoursBucket(1613472303000, 5) AS bucket
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>bucket</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>89637</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochDaysBucket(1613472303000, 10) AS bucket
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>bucket</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1867</td>
    </tr>
  </tbody>
</table>
