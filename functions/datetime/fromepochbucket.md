---
description: >-
  This section contains reference documentation for the fromEpochBucket
  functions.
---

# FromEpochBucket

Convert epoch to epoch milliseconds. e.g. 10 seconds since epoch or 5 minutes since Epoch. The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> FromEpoch\<TIME\_UNIT>Bucket(timeInMillis, bucketSize)

## Usage Examples

```sql
select FromEpochSecondsBucket(1613472303, 1) AS bucket
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
      <td>1613472303000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochSecondsBucket(1613472303, 2) AS bucket
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
      <td>3226944606000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochMinutesBucket(2689120, 10) AS bucket
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
      <td>1613472000000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochHoursBucket(89637, 5) AS bucket
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
      <td>1613466000000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochDaysBucket(1867, 10) AS bucket
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
      <td>1613088000000</td>
    </tr>
  </tbody>
</table>
