---
description: This section contains reference documentation for the day function.
---

# day

Returns the day of the month from the given epoch millis in UTC or specified timezone. The value ranges from 1 to 31.

## Signature

> day(tsInMillis)
>
> day(tsInMillis, timeZoneId)
>
> dayOfMonth(tsInMillis)
>
> dayOfMonth(tsInMillis, timeZoneId)

## Usage Examples

```sql
select day(1639351800000) AS day
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>12</td>
    </tr>
  </tbody>
</table>

```sql
select day(1639351800000, 'CET') AS day
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13</td>
    </tr>
  </tbody>
</table>

```sql
select dayOfMonth(1639351800000) AS day
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>12</td>
    </tr>
  </tbody>
</table>

```sql
select dayOfMonth(1639351800000, 'CET') AS day
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>day</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13</td>
    </tr>
  </tbody>
</table>
