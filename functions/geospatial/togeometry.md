---
description: This section contains reference documentation for the toGeometry function.
---

# toGeometry

Converts a spherical geographical object to a Geometry object.

## Signature

> toGeometry(geographyObject)

## Usage Examples

```sql
select toGeometry(
    STPOINT(-122, 37, 1)
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
      <td>00c05e8000000000004042800000000000</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
You can create geographical objects using the [STPOINT](stpoint.md) and [ST\_GeogFromText](stgeogfromtext.md) functions.
{% endhint %}
