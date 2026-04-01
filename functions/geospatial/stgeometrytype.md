---
description: >-
  This section contains reference documentation for the ST_GeometryType
  function.
---

# ST\_GeometryType

Returns the type of the geometry as a string

## Signature

> ST\_GeometryType(geometry)

## Usage Examples

These examples are based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select location, ST_GeometryType(location) AS type
from meetupRsvp 
LIMIT 1
```

<table>
  <thead>
    <tr>
      <th>location</th>
      <th>type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>80c00dae147ae147ae404435c28f5c28f6</td>
      <td>Point</td>
    </tr>
  </tbody>
</table>
