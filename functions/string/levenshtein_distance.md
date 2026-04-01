---
description: This section contains reference documentation for the levenshtein_distance function.
---

# levenshtein_distance

Returns the Levenshtein edit distance of string1 and string2, i.e. the minimum number of single-character edits (insertions, deletions or substitutions) needed to change string1 into string2.

## Signature

> levenshtein_distance(string1, string2) → bigint

## Usage Examples

```sql
SELECT levenshtein_distance('kitten', 'sitting') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>3</td>
    </tr>
  </tbody>
</table>

```sql
SELECT levenshtein_distance('hello', 'world') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>4</td>
    </tr>
  </tbody>
</table>

```sql
SELECT levenshtein_distance('same', 'same') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0</td>
    </tr>
  </tbody>
</table>

```sql
SELECT levenshtein_distance('', 'abc') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>3</td>
    </tr>
  </tbody>
</table>

```sql
SELECT levenshtein_distance('abc', '') AS value
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>3</td>
    </tr>
  </tbody>
</table>
