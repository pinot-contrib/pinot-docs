---
description: This section contains reference documentation for the ARRAYLENGTH function.
---

# ARRAYLENGTH

Returns the length of a multi-value column

## Signature

> ARRAYLENGTH('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

```sql
select ARRAYLENGTH(RandomAirports) AS length, count(*) 
from airlineStats 
GROUP BY length
ORDER BY count(*) DESC
LIMIT 5
```

<table>
  <thead>
    <tr>
      <th>length</th>
      <th>count(\*)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>5382</td>
    </tr>
    <tr>
      <td>37</td>
      <td>267</td>
    </tr>
    <tr>
      <td>33</td>
      <td>223</td>
    </tr>
    <tr>
      <td>17</td>
      <td>166</td>
    </tr>
    <tr>
      <td>22</td>
      <td>160</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
The `count(*)` values will increase each time we execute the query as data is constantly being ingested by the Hybrid Quick Start.
{% endhint %}
