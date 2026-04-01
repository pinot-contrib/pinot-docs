---
description: This section contains reference documentation for the ST_GeogFromWKB function.
---

# ST\_GeogFromWKB

Returns a geography type object from WKB representation.

## Signature

> ST\_GeogFromWKB(wkb)

## Usage Examples

```sql
select STPOINT(-122, 37) AS point,
       ST_GeogFromWKB(
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
      <td>80c05e8000000000004042800000000000</td>
    </tr>
  </tbody>
</table>

```sql
select STPOINT(-122, 37, 1) AS point,
       ST_GeogFromWKB(
         ST_AsBinary(STPOINT(-122, 37, 1))
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
      <td>80c05e8000000000004042800000000000</td>
      <td>80c05e8000000000004042800000000000</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
You can create geometry objects in the WKB format using the [ST\_AsBinary](stasbinary.md) function.
{% endhint %}
