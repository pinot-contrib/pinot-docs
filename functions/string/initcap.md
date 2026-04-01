---
description: This section contains reference documentation for the initcap function.
---

# initcap

Converts the first letter of each word in a string to uppercase and the rest to lowercase.

## Signature

> INITCAP(col)

## Usage Examples

```sql
select INITCAP('hello world') AS name
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Hello World</td>
    </tr>
  </tbody>
</table>

```sql
select INITCAP('APACHE PINOT') AS name
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Apache Pinot</td>
    </tr>
  </tbody>
</table>

```sql
select INITCAP('tHiS iS a TeSt') AS name
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>This Is A Test</td>
    </tr>
  </tbody>
</table>
