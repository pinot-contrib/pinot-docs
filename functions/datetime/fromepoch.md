---
description: This section contains reference documentation for the fromEpoch functions.
---

# FromEpoch

Convert epoch to epoch milliseconds. The following time units are supported:

* SECONDS
* MINUTES
* HOURS
* DAYS

## Signature

> FromEpoch\<TIME\_UNIT>(timeIn\<Time\_UNIT>)

## Usage Examples

```sql
select FromEpochSeconds(1613472303) AS epochMillis
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochMillis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1613472303000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochMinutes(26891205) AS epochMillis
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochMillis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1613472300000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochHours(448186) AS epochMillis
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochMillis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1613469600000</td>
    </tr>
  </tbody>
</table>

```sql
select FromEpochDays(18674) AS epochMillis
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>epochMillis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1613433600000</td>
    </tr>
  </tbody>
</table>
