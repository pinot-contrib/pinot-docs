---
description: This section contains reference documentation for the regexpExtract function.
---

# regexpExtract

Extracts values that match the provided regular expression

## Signature

> regexpExtract(value, regexp)
>
> regexpExtract(value, regexp, group)
>
> regexpExtract(value, regexp, group, defaultValue)

## Usage Examples

```sql
select regexpExtract('foo', '.*') AS value
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
      <td>foo</td>
    </tr>
  </tbody>
</table>

```sql
select regexpExtract('foo123', '[0-9]+') AS value
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
      <td>123</td>
    </tr>
  </tbody>
</table>

```sql
select regexpExtract('foo123', '[^0-9]+') AS value
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
      <td>foo</td>
    </tr>
  </tbody>
</table>

```sql
select regexpExtract('foo bar baz', '(\w+) (\w+)', 0) AS value
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
      <td>foo bar</td>
    </tr>
  </tbody>
</table>

```sql
select regexpExtract('foo bar baz', '(\w+) (\w+)', 2) AS value
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
      <td>bar</td>
    </tr>
  </tbody>
</table>

```sql
select regexpExtract('foo123', 'bar', 0, 'defaultValue') AS value
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
      <td>defaultValue</td>
    </tr>
  </tbody>
</table>
