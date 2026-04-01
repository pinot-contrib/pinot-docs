---
description: This section contains reference documentation for the minute function.
---

# minute

Returns the minute of the hour from the given epoch millis in UTC or specified timezone. The value ranges from 0 to 59.

## Signature

> minute(tsInMillis)
>
> minute(tsInMillis, timeZoneId)

## Usage Examples

```sql
select minute(1639351800000) AS minute
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>minute</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>30</td>
    </tr>
  </tbody>
</table>

```sql
select minute(1639351800000, 'America/St_Johns') AS minute
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>minute</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
    </tr>
  </tbody>
</table>
