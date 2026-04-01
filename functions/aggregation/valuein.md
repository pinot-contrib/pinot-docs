---
description: This section contains reference documentation for the VALUEIN function.
---

# VALUEIN

Takes at least 2 arguments, where the first argument is a multi-valued column, and the following arguments are constant values. The transform function will filter the value from the multi-valued column with the given constant values. The `VALUEIN` transform function is especially useful when the same multi-valued column is both filtering column and grouping column.

## Signature

> VALUEIN('colName', value1, value2,...)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
SELECT VALUEIN(RandomAirports, 'SEA') as airport, count(*)
FROM airlineStats
WHERE RandomAirports = 'SEA'
GROUP BY airport
```

<table>
  <thead>
    <tr>
      <th>airport</th>
      <th>count(\*)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SEA</td>
      <td>4858</td>
    </tr>
  </tbody>
</table>

```sql
SELECT VALUEIN(RandomAirports, 'SEA', 'PSC') as airport, count(*)
FROM airlineStats
WHERE RandomAirports IN ('SEA', 'PSC')
GROUP BY airport
```

<table>
  <thead>
    <tr>
      <th>airport</th>
      <th>count(\*)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PSC</td>
      <td>4832</td>
    </tr>
    <tr>
      <td>SEA</td>
      <td>4858</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
The `count(*)` values returned by these queries will increase each time we execute the query as data is constantly being ingested by the Hybrid Quick Start.
{% endhint %}
