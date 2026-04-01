---
description: >-
  This section contains reference documentation for the h3_gridDistance
  function.
---

# GridDistance

Computes the H3 grid distance between two H3 indexes.

## Signature

> h3\_gridDistance(h3Index1, h3Index2)

## Usage Examples

```sql
SELECT h3_gridDistance(0x8928308280fffff, 0x8928308283fffff) AS distance
FROM ignoreMe;
```

<table>
  <thead>
    <tr>
      <th>distance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
The H3 grid distance is only defined for H3 indexes of the same resolution. If the indexes are not at the same resolution, the function will return an error.
{% endhint %}
