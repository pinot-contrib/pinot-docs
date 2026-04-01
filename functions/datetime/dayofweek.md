---
description: This section contains reference documentation for the dayOfWeek function.
---

# dayOfWeek

Returns the day of the week from the given epoch millis in UTC timezone. The value ranges from 1(Monday) to 7(Sunday).

## Signature

> dayOfWeek(tsInMillis)
>
> dayOfWeek(tsInMillis, timeZoneId)
>
> dow(tsInMillis)
>
> dow(tsInMillis, timeZoneId)

## Usage Examples

```sql
select dayOfWeek(1639351800000) AS dayOfWeek
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>dayOfWeek</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7</td>
    </tr>
  </tbody>
</table>

```sql
select dayOfWeek(1639351800000, 'CET') AS dayOfWeek
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>dayOfWeek</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
    </tr>
  </tbody>
</table>

```sql
select dow(1639351800000) AS dayOfWeek
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>dayOfWeek</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>7</td>
    </tr>
  </tbody>
</table>

```sql
select dow(1639351800000, 'CET') AS dayOfWeek
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>dayOfWeek</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
    </tr>
  </tbody>
</table>
