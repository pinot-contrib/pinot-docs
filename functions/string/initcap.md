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

| name        |
| ----------- |
| Hello World |

```sql
select INITCAP('APACHE PINOT') AS name
FROM ignoreMe
```

| name         |
| ------------ |
| Apache Pinot |

```sql
select INITCAP('tHiS iS a TeSt') AS name
FROM ignoreMe
```

| name           |
| -------------- |
| This Is A Test |
