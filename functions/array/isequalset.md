---
description: >-
  This section contains reference documentation for the isEqualSet function.
---

# isEqualSet

Compares two multi-value columns (treated as sets) and returns `true` if they contain the same elements, regardless of order. Returns `false` if either argument is null.

## Signature

> isEqualSet(mvCol1, mvCol2)

<table>
  <thead>
    <tr>
      <th>Argument</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`mvCol1`</td>
      <td>Multi-value</td>
      <td>First collection</td>
    </tr>
    <tr>
      <td>`mvCol2`</td>
      <td>Multi-value</td>
      <td>Second collection</td>
    </tr>
  </tbody>
</table>

Returns: **BOOLEAN**

## Usage Examples

```sql
SELECT isEqualSet(tags, categories) AS sameSet
FROM myTable
```

Returns `true` when the `tags` and `categories` multi-value columns contain exactly the same set of values.

```sql
SELECT isEqualSet(
  ARRAY_SORT_INT(arrayA),
  ARRAY_SORT_INT(arrayB)
) AS sameSet
FROM myTable
```

{% hint style="info" %}
Two empty collections are considered equal. If either argument is null, the function returns `false`.
{% endhint %}
