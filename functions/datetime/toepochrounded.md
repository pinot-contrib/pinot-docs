---
description: >-
  This section contains reference documentation for the toEpochRounded
  functions.
---

# ToEpochRounded

Convert epoch milliseconds to epoch , round to nearest rounding bucket(Bucket size is defined in ) The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> ToEpoch\<TIME\_UNIT>Rounded(timeInMillis, bucketSize)

## Usage Examples

```sql
select ToEpochSecondsRounded(1613472303000, 1000) AS epochSeconds
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochSeconds</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1613472000</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochMinutesRounded(1613472303000, 10) AS epochMins
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochMins</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>26891200</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochHoursRounded(1613472303000, 5) AS epochHours
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochHours</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>448185</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochDaysRounded(1613472303000, 10) AS epochDays
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochDays</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>18670</td>
    </tr>
  </tbody>
</table>
