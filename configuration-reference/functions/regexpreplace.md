---
description: This section contains reference documentation for the regexpReplace function
---

# regexpReplace

Find and replace a string or regexp pattern with a target string or regexp pattern. If matchStr is not found, inputStr will be returned. By default, all occurrences of match pattern in the input string will be replaced. Default matching mode is case sensitive.

## Signature

> regexpReplace(inputStr, matchRegexp, replaceRegexp)
>
> regexpReplace(inputStr, matchRegexp, replaceRegexp, matchStartPos)
>
> regexpReplace(inputStr, matchRegexp, replaceRegexp, matchStartPos, occurrence)
>
> regexpReplace(inputStr, matchRegexp, replaceRegexp, matchStartPos, occurrence, flag)

### `inputStr`

The input string or the column name on which regexpReplace function should be applied.

### `matchRegexp`

The regular expression or string used to match against the input string or column value.

### `replaceRegexp`

The regular expression or string to replace if a match is found.

### `matchStartPos`

Index of inputStr from where matching should start. Counting starts and 0. Default value is 0 if not specified.

### `occurrence`

Controls which occurence of the matched pattern must be replaced. Counting starts at 0. Default value is -1 if not specified

### `flag`

Single character flag that controls how the regex finds matches in inputStr. If an incorrect flag is specified, the function applies default case sensitive match. Only one flag can be specified. Supported flags are:

* `i` -> case insensitive match

## Usage Examples

### Example 1

In the example below,  shows a simple string find and replace example where all occurrences of the matched string `o` is replaced with string `x`.&#x20;

```sql
select regexpReplace('foo', 'o', 'x') AS value
from myTable
```

| value |
| ----- |
| fxx   |

### Example 2

The example below shows how a regexp pattern containing consecutive digits is found and replaced with a simple string `bar`.&#x20;

```sql
select regexpReplace('foo123', '[0-9]+', 'bar') AS value
from myTable
```

| value  |
| ------ |
| foobar |

### Example 3

The example below shows how a regexp pattern containing consecutive non-digits is found and replaced with a simple string `bar`.&#x20;

```sql
select regexpReplace('foo123', '[^0-9]+', 'bar') AS value
from myTable
```

| value  |
| ------ |
| bar123 |

### Example 4

The following example demonstrates how `replaceStr` can contain backreferences to substrings captured by the `matchStr` regular expression. Backreferences are indicated by $n where n can range from 0-9.  In the example below, every character in the input is replaced by the character appended with a space. &#x20;

```sql
select regexpReplace('foo', '(.)', '$1 ') AS value
from myTable
```

| value  |
| ------ |
| f o o  |

### Example 5

This example shows how regexpReplace can be used to remove extra whitespaces between words in an input string.

```sql
select regexpReplace('Pinot is  blazing  fast', '( ){2,}', ' ') AS value
from myTable
```

| value                 |
| --------------------- |
| Pinot is blazing fast |

### Example 6

This example shows the power of backreferencing can be used in regexpReplace to format phone numbers.

```sql
select regexpReplace('11234567898','(\\d)(\\d{3})(\\d{3})(\\d{4})', '$1-($2) $3-$4') AS value
from myTable
```

| value            |
| ---------------- |
| 1-(123) 456-7898 |

### Example 7

This example shows how the `matchStartPos` parameter can be used. Since the `matchStartPos` is set to 4, pattern matching against the `inputStr` begins at index 4 there by leading to the string `healthy` not being replaced.

```sql
select regexpReplace('healthy, wealthy, stealthy and wise','\\w+thy', 'something', 4)  AS value
from myTable
```

| value                                  |
| -------------------------------------- |
| healthy, something, something and wise |

### Example 8

This example shows how the `occurence` parameter can be used. In the example below, the matchStr regular expression matches against three instances in the input - `healthy`, `wealthy` and `stealthy`. As the occurence is specified to 2, the second occurence (counting from zero)  `stealthy` is replaced with `something`

```sql
select regexpReplace('healthy, wealthy, stealthy and wise','\\w+thy', 'something', 0, 2)  AS value
from myTable
```

| value                                |
| ------------------------------------ |
| healthy, wealthy, something and wise |

### Example 9

The example below shows the usage of the `flag` parameter. Here the case insensitive flag `i` is specified.&#x20;

```sql
select regexpReplace('healthy, wealthy, stealthy and wise','\\w+THY', 'something', 0, 0, 'i')  AS value
from myTable
```

| value                                 |
| ------------------------------------- |
| something, wealthy, stealthy and wise |

### Example 10

The examples below show some sample queries  using regexpReplace in there `WHERE` clause of a query.

```sql
SELECT col1, col2
FROM myTable
WHERE regexpReplace(stateCode, '[VC]A', 'TEST') = 'TEST'
```

```sql
SELECT count(*)
FROM myTable
WHERE contains(regexpReplace(stateCode, '(C)(A)', '$1TEST$2'), 'CTESTA')
```
