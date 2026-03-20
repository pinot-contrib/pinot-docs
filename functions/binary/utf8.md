---
description: >-
  This section contains reference documentation for UTF8 encode/decode
  functions.
---

# UTF8

* `fromUtf8` returns UTF8 encoded string of input binary data (`bytes` type).
* `toUtf8` returns binary data (represented as a Hex string) from a UTF8 encoded string.

## Signature

> fromUtf8(bytesCol)
>
> toUtf8(string)

## Usage Examples

```sql
SELECT bytesCol1, fromUtf8(bytesCol1) AS utf8Str
FROM testTable
LIMIT 1
```

| bytesCol1    | utf8Str |
| ------------ | ------- |
| 68656c6c6f21 | hello!  |

```sql
SELECT toUtf8('hello!') AS binaryOutput
FROM ignoreMe
```

| binaryOutput |
| ------------ |
| 68656c6c6f21 |
