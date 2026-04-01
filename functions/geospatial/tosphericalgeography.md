---
description: >-
  This section contains reference documentation for the toSphericalGeography
  function.
---

# toSphericalGeography

Converts a Geometry object to a spherical geography object.

## Signature

> toSphericalGeography(geometryObject)

## Usage Examples

```sql
select toSphericalGeography(
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
      <td>80c05e8000000000004042800000000000</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
You can create geometry objects using the [STPOINT](stpoint.md) and [ST\_GeomFromText](stgeomfromtext.md) functions.
{% endhint %}
