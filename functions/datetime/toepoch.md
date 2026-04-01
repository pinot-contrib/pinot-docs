---
description: This section contains reference documentation for the toEpoch functions.
---

# ToEpoch

Convert epoch milliseconds to epoch . The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> ToEpoch\<TIME\_UNIT>(timeInMillis)

## Usage Examples

```sql
select ToEpochSeconds(1613472303000) AS epochSeconds
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
      <td>1613472303</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochMinutes(1613472303000) AS epochMins
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
      <td>26891205</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochHours(1613472303000) AS epochHours
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
      <td>448186</td>
    </tr>
  </tbody>
</table>

```sql
select ToEpochDays(1613472303000) AS epochDays
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
      <td>18674</td>
    </tr>
  </tbody>
</table>
