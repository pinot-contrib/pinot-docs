---
description: >-
  This section contains reference documentation for bitwise scalar functions.
---

# Bitwise Functions

Bitwise scalar functions perform bitwise operations on INT and LONG integer types.

## Type Behavior

- **INT inputs**: When all arguments are INT, the result is INT
- **Mixed or LONG inputs**: When any argument is LONG, the result is LONG
- **bitExtract**: Always returns INT, regardless of input types

## bitAnd / bit_and

Performs a bitwise AND operation on two values.

### Signature

> bitAnd(a, b)
> bit_and(a, b)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | First value |
| `b`      | INT or LONG | Second value |

Returns: **INT** (if both INT) or **LONG** (if any LONG)

### Usage Examples

```sql
SELECT bitAnd(12, 10) AS value
FROM myTable
```

| value |
| ----- |
| 8     |

```sql
SELECT bitAnd(intCol, 3) AS masked
FROM myTable
```

## bitOr / bit_or

Performs a bitwise OR operation on two values.

### Signature

> bitOr(a, b)
> bit_or(a, b)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | First value |
| `b`      | INT or LONG | Second value |

Returns: **INT** (if both INT) or **LONG** (if any LONG)

### Usage Examples

```sql
SELECT bitOr(8, 4) AS value
FROM myTable
```

| value |
| ----- |
| 12    |

```sql
SELECT bitOr(intCol, 8) AS flags
FROM myTable
```

## bitXor / bit_xor

Performs a bitwise XOR (exclusive OR) operation on two values.

### Signature

> bitXor(a, b)
> bit_xor(a, b)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | First value |
| `b`      | INT or LONG | Second value |

Returns: **INT** (if both INT) or **LONG** (if any LONG)

### Usage Examples

```sql
SELECT bitXor(12, 10) AS value
FROM myTable
```

| value |
| ----- |
| 6     |

```sql
SELECT bitXor(intCol, 1) AS toggled
FROM myTable
```

## bitNot

Performs a bitwise NOT operation, inverting all bits of a value.

### Signature

> bitNot(a)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | Value to invert |

Returns: **INT** (if INT) or **LONG** (if LONG)

### Usage Examples

```sql
SELECT bitNot(0) AS value
FROM myTable
```

| value  |
| ------ |
| -1     |

```sql
SELECT bitNot(intCol) AS inverted
FROM myTable
```

## bitMask

Creates a bitmask with a single bit set at position n.

### Signature

> bitMask(n)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `n`      | INT | Bit position (0-indexed) |

Returns: **INT**

### Usage Examples

```sql
SELECT bitMask(0) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT bitMask(3) AS value
FROM myTable
```

| value |
| ----- |
| 8     |

```sql
SELECT bitMask(6) AS flags
FROM myTable
```

## bitShiftLeft

Performs a left bit shift operation.

### Signature

> bitShiftLeft(a, n)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | Value to shift |
| `n`      | INT | Number of positions to shift |

Returns: **INT** (if a is INT) or **LONG** (if a is LONG)

### Usage Examples

```sql
SELECT bitShiftLeft(1, 2) AS value
FROM myTable
```

| value |
| ----- |
| 4     |

```sql
SELECT bitShiftLeft(intCol, 2) AS shifted
FROM myTable
```

## bitShiftRight

Performs an arithmetic right bit shift operation (sign-extending).

### Signature

> bitShiftRight(a, n)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | Value to shift |
| `n`      | INT | Number of positions to shift |

Returns: **INT** (if a is INT) or **LONG** (if a is LONG)

### Usage Examples

```sql
SELECT bitShiftRight(8, 2) AS value
FROM myTable
```

| value |
| ----- |
| 2     |

```sql
SELECT bitShiftRight(intCol, 1) AS shifted
FROM myTable
```

## bitShiftRightUnsigned / bitShiftRightLogical

Performs a logical (unsigned) right bit shift operation, filling with zeros.

### Signature

> bitShiftRightUnsigned(a, n)
> bitShiftRightLogical(a, n)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | Value to shift |
| `n`      | INT | Number of positions to shift |

Returns: **INT** (if a is INT) or **LONG** (if a is LONG)

### Usage Examples

```sql
SELECT bitShiftRightUnsigned(-1, 1) AS value
FROM myTable
```

| value |
| ----- |
| 2147483647 |

```sql
SELECT bitShiftRightUnsigned(intCol, 1) AS shifted
FROM myTable
```

## bitExtract / extractBit

Extracts the bit at position n, returning 1 if the bit is set, 0 otherwise.

### Signature

> bitExtract(a, n)
> extractBit(a, n)

| Argument | Type | Description |
| -------- | ---- | ----------- |
| `a`      | INT or LONG | Value to extract from |
| `n`      | INT | Bit position (0-indexed) |

Returns: **INT** (always, regardless of input type)

### Usage Examples

```sql
SELECT bitExtract(12, 2) AS value
FROM myTable
```

| value |
| ----- |
| 1     |

```sql
SELECT bitExtract(12, 0) AS value
FROM myTable
```

| value |
| ----- |
| 0     |

```sql
SELECT id FROM myTable WHERE bitExtract(flags, 2) = 1
```

## Combined Usage Example

```sql
SELECT 
  id,
  bitAnd(flags, 15) AS lower_nibble,
  bitOr(flags, 128) AS set_high_bit,
  bitExtract(status, 3) AS is_active,
  bitShiftLeft(count, 2) AS quad_count
FROM myTable
WHERE bitExtract(flags, 2) = 1
```
