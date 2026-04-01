---
description: This section contains reference documentation for the hour function.
---

# hour

Returns the hour of the day from the given epoch millis in UTC or specified timezone. The value ranges from 0 to 23.

## Signature

> hour(tsInMillis)
>
> hour(tsInMillis, timeZoneId)

## Usage Examples

```sql
select hour(1639351800000) AS hour
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>23</td>
    </tr>
  </tbody>
</table>

```sql
select hour(1639351800000, 'CET') AS hour
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>hour</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
    </tr>
  </tbody>
</table>
