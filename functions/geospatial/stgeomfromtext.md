---
description: >-
  This section contains reference documentation for the ST_GeomFromText
  function.
---

# ST\_GeomFromText

Returns a geometry type object from [Well-Known Text representation or extended (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry) representation, with the optional spatial system reference

## Signature

> ST\_GeomFromText(wkt)

## Usage Examples

```sql
select ST_GeomFromText('POINT (30 10)') AS value
from ignoreMe 
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>80403e0000000000004024000000000000</td>
    </tr>
  </tbody>
</table>

```sql
select ST_GeomFromText('LINESTRING (30 10, 10 30, 40 40)') AS value
from ignoreMe 
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>02000000010000000300000000403e00000000000040240000000000004024000000000000403e00000000000040440000000000004044000000000000</td>
    </tr>
  </tbody>
</table>

```sql
select ST_GeomFromText('POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))') AS value
from ignoreMe 
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>04000000010000000500000000403e0000000000004024000000000000402400000000000040340000000000004034000000000000404400000000000040440000000000004044000000000000403e0000000000004024000000000000</td>
    </tr>
  </tbody>
</table>
