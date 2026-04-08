---
description: This section contains reference documentation for the splitPart function.
---

# splitPart

Splits the input string by a delimiter and returns one element from the result.

Pinot supports both `splitPart(str, delimiter, index)` and `splitPart(str, delimiter, limit, index)`.
The snake-case alias `split_part(...)` is also accepted.
The index is 0-based. Negative indices count from the end of the split result.

## Signature

```sql
splitPart(str, delimiter, index)
splitPart(str, delimiter, limit, index)
```

## Parameters

- `str`: Input string to split.
- `delimiter`: Delimiter used to split the string.
- `index`: 0-based element index. Negative values count from the end.
- `limit`: Optional split limit applied before selecting the element.

## Returns

Returns the selected string element. If the index is out of bounds, Pinot returns the string literal `"null"`.

## Usage examples

These examples are derived from `StringFunctionsTest`.

```sql
SELECT splitPart('org.apache.pinot.common.function', '.', 2) AS value
```

Returns:

```text
pinot
```

```sql
SELECT splitPart('org.apache.pinot.common.function', '.', -1) AS value
```

Returns:

```text
function
```

```sql
SELECT splitPart('org.apache.pinot.common.function', '.', 3, -3) AS value
```

Returns:

```text
org
```

## Notes

- The 4-argument form applies the split limit first and then looks up the requested index.
- Multi-character delimiters are supported.
- Empty input strings return `"null"` when the delimiter is non-empty.
