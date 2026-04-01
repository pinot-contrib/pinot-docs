---
description: This section contains reference documentation for the ST_GeomFromWKB function.
---

# ST\_GeomFromWKB

Returns a geometry type object from WKB representation.

## Signature

> ST\_GeomFromWKB(wkb)

## Usage Examples

```sql
select STPOINT(-122, 37) AS point,
       ST_GeomFromWKB(
         ST_AsBinary(STPOINT(-122, 37))
       ) AS value
from ignoreMe 
```

<table>
  <thead>
    <tr>
      <th>point</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>00c05e8000000000004042800000000000</td>
      <td>00c05e8000000000004042800000000000</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
You can create geometry objects in the WKB format using the [ST\_AsBinary](stasbinary.md) function.
{% endhint %}
