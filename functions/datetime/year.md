---
description: This section contains reference documentation for the year function.
---

# year

Returns the year from the given epoch millis in UTC timezone.

## Signature

> year(tsInMillis)
>
> year(tsInMillis, timeZoneId)

## Usage Examples

```sql
select year(1609472186000) AS year
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2021</td>
    </tr>
  </tbody>
</table>

```sql
select year(1609472186000, 'America/Toronto') AS year
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2020</td>
    </tr>
  </tbody>
</table>
