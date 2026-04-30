---
description: This section contains reference documentation for the soundex function.
---

# soundex

Returns the four-character Soundex code for a string.

Pinot returns `0000` for the empty string. If the input is `null`, Pinot returns `null`.

## Signature

> soundex(string) -> string

## Usage Examples

```sql
SELECT soundex('Robert') AS value
FROM ignoreMe
```

| value |
| ----- |
| R163  |

```sql
SELECT soundex('Rupert') AS value
FROM ignoreMe
```

| value |
| ----- |
| R163  |

```sql
SELECT soundex('Ashcraft') AS value
FROM ignoreMe
```

| value |
| ----- |
| A261  |

```sql
SELECT soundex('') AS value
FROM ignoreMe
```

| value |
| ----- |
| 0000  |

## Notes

- `soundex('Robert')` and `soundex('Rupert')` return the same code because the function is designed for phonetic matching.
- Pinot derives this behavior from `StringFunctions.soundex(...)` in `apache/pinot` merge commit `51e610d486bf8aadd647b4b69f34e9c70ef0ebea`.
