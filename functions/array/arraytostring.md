---
description: >-
  This section contains reference documentation for the arrayToString
  function.
---

# arrayToString

Joins a string array into a single string using a delimiter.

## Signature

> arrayToString(values, delimiter)

> arrayToString(values, delimiter, nullString)

The 3-argument form replaces null or empty-string placeholder elements with `nullString` before joining.

## Usage Examples

These examples are based on Pinot's array function tests.

```sql
SELECT arrayToString(stringArray, '::') AS joinedValues
FROM myTable
```

Returns `3::2::10::6::1::12` when `stringArray` is `['3', '2', '10', '6', '1', '12']`.

```sql
SELECT arrayToString(stringArrayWithNulls, '::', '*') AS joinedValues
FROM myTable
```

Returns `3::2::10::6::1::12::*::*` when `stringArrayWithNulls` is `['3', '2', '10', '6', '1', '12', '', null]`.
