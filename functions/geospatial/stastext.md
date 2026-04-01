---
description: This section contains reference documentation for the ST_AsText function.
---

# ST\_AsText

Returns the WKT representation of the geometry/geography.

## Signature

> ST\_AsText(geometryObject)

## Usage Examples

```sql
select stAsText(
    STPOINT(-122, 37)
) AS value
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
      <td>POINT (-122 37)</td>
    </tr>
  </tbody>
</table>

```sql
select stAsText(
    ST_GeogFromText('LINESTRING (30 10, 10 30, 40 40)')
) AS value
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
      <td>LINESTRING (30 10, 10 30, 40 40)</td>
    </tr>
  </tbody>
</table>
