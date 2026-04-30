---
description: This section contains reference documentation for the difference function.
---

# difference

Returns a similarity score from `0` to `4` by comparing the four-character Soundex codes for two strings.

A score of `4` means the Soundex codes are identical. A score of `0` means no Soundex positions match.

## Signature

> difference(string1, string2) -> int

## Usage Examples

```sql
SELECT difference('Robert', 'Rupert') AS value
FROM ignoreMe
```

| value |
| ----- |
| 4     |

```sql
SELECT difference('Smith', 'Johnson') AS value
FROM ignoreMe
```

| value |
| ----- |
| 1     |

```sql
SELECT difference('Ann', 'Ann') AS value
FROM ignoreMe
```

| value |
| ----- |
| 4     |

```sql
SELECT difference('', '') AS value
FROM ignoreMe
```

| value |
| ----- |
| 4     |

```sql
SELECT difference('Robert', '') AS value
FROM ignoreMe
```

| value |
| ----- |
| 0     |

## Notes

- `difference()` calls `soundex()` internally and compares the four Soundex characters position by position.
- Pinot null-propagates this function when either argument is `null`.
