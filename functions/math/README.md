# Math Functions

​[**ADD(col1, col2, col3...)**](add.md) Sum of at least two values

​[**SUB(col1, col2)**](sub.md) Difference between two values

​[**MULT(col1, col2, col3...)**](mult.md) Product of at least two values

​[**DIV(col1, col2)**](div.md) Quotient of two values

​[**MOD(col1, col2)**](mod.md) Modulo of two values

​[**ABS(col1)**](abs.md) Absolute of a value

​[**CEIL(col1)**](ceil.md#signature) Rounded up to the nearest integer

​[**FLOOR(col1)**](floor.md) Rounded down to the nearest integer

​[**EXP(col1)**](exp.md) Euler's number(e) raised to the power of col.

​[**LN(col1)**](ln.md) Natural log of value

​[**SQRT(col1)**](sqrt.md) Square root of a value

​[**ROUNDDECIMAL(col1, col2)** ](round-1.md)​Rounds value to a specified number of decimal places

​[**ROUND(timeValue, bucketSize)**](round.md) Round epoch-style values to the nearest bucket start

[**intDiv(col1, col2)**](intdiv.md)\
Returns the integer result of dividing col1 by col2, rounded down (floor division). Returns a `Long`.

Usage: `intDiv(col1, col2)`\
Example: `SELECT intDiv(10, 3) FROM myTable` returns `3`

[**intDivOrZero(col1, col2)**](intdivorzero.md)\
Same as `intDiv` but returns zero when dividing by zero or when dividing a minimal negative number by minus one.

Usage: `intDivOrZero(col1, col2)`\
Example: `SELECT intDivOrZero(10, 0) FROM myTable` returns `0`

[**isFinite(col)**](isfinite.md)\
Returns `1` if the value is finite (not infinite and not NaN), `0` otherwise.

Usage: `isFinite(col)`\
Example: `SELECT isFinite(salary) FROM myTable`

[**isInfinite(col)**](isinfinite.md)\
Returns `1` if the value is infinite (positive or negative infinity), `0` otherwise.

Usage: `isInfinite(col)`\
Example: `SELECT isInfinite(ratio) FROM myTable`

[**ifNotFinite(valueToCheck, defaultValue)**](ifnotfinite.md)\
Returns `valueToCheck` if it is finite, otherwise returns `defaultValue`.

Usage: `ifNotFinite(col, defaultValue)`\
Example: `SELECT ifNotFinite(ratio, 0) FROM myTable`

[**isNaN(col)**](isnan.md)\
Returns `1` if the value is NaN (Not a Number), `0` otherwise.

Usage: `isNaN(col)`\
Example: `SELECT isNaN(ratio) FROM myTable`

[**moduloOrZero(col1, col2)**](moduloorzero.md)\
Same as `MOD` but returns zero when dividing by zero or when dividing a minimal negative number by minus one.

Usage: `moduloOrZero(col1, col2)`\
Example: `SELECT moduloOrZero(10, 0) FROM myTable` returns `0`

[**positiveModulo(col1, col2)**](positivemodulo.md)\
Returns the modulo of two values, always returning a non-negative result.

Usage: `positiveModulo(col1, col2)`\
Example: `SELECT positiveModulo(-7, 3) FROM myTable` returns `2`

[**negate(col)**](negate.md)\
Returns the negation of the value.

Usage: `negate(col)`\
Example: `SELECT negate(score) FROM myTable`

**least(col1, col2)**\
Returns the smaller of two values.

Usage: `least(col1, col2)`\
Example: `SELECT least(score1, score2) FROM myTable`

**greatest(col1, col2)**\
Returns the larger of two values.

Usage: `greatest(col1, col2)`\
Example: `SELECT greatest(score1, score2) FROM myTable`

**sign(col)**\
Returns the signum of a value: -1.0 if negative, 0.0 if zero, 1.0 if positive.

Usage: `sign(col)`\
Example: `SELECT sign(profit) FROM myTable`

**pow(col, exponent)** / **power(col, exponent)**\
Returns the value raised to the given exponent.

Usage: `pow(col, exponent)` or `power(col, exponent)`\
Example: `SELECT pow(score, 2) FROM myTable`

**truncate(col)** / **truncate(col, scale)**\
Truncates a value toward zero. When `scale` is provided, truncates to the given number of decimal places.

Usage: `truncate(col)` or `truncate(col, scale)`\
Example: `SELECT truncate(3.75) FROM myTable` returns `3.0`\
Example: `SELECT truncate(3.75, 1) FROM myTable` returns `3.7`

**rand()** / **rand(seed)**\
Returns a pseudo-random double value in the range [0.0, 1.0). When a seed is provided, the result is deterministic for the same seed value. Without a seed, the result is non-deterministic.

Usage: `rand()` or `rand(seed)`\
Example: `SELECT rand() FROM myTable`\
Example: `SELECT rand(42) FROM myTable`

**log2(col)**\
Returns the base-2 logarithm of a value.

Usage: `log2(col)`\
Example: `SELECT log2(8) FROM myTable` returns `3.0`

**log10(col)**\
Returns the base-10 logarithm of a value.

Usage: `log10(col)`\
Example: `SELECT log10(1000) FROM myTable` returns `3.0`

[**gcd(col1, col2)**](gcd.md)\
Returns the greatest common divisor of two long values.

Usage: `gcd(col1, col2)`\
Example: `SELECT gcd(12, 8) FROM myTable` returns `4`

[**lcm(col1, col2)**](lcm.md)\
Returns the least common multiple of two long values.

Usage: `lcm(col1, col2)`\
Example: `SELECT lcm(4, 6) FROM myTable` returns `12`

[**hypot(col1, col2)**](hypot.md)\
Returns the hypotenuse of a right-angled triangle, i.e. `sqrt(col1^2 + col2^2)`, without intermediate overflow or underflow.

Usage: `hypot(col1, col2)`\
Example: `SELECT hypot(3, 4) FROM myTable` returns `5.0`

[**byteswapInt(col)**](byteswapint.md)\
Reverses the byte order of an integer value.

Usage: `byteswapInt(col)`\
Example: `SELECT byteswapInt(intCol) FROM myTable`

[**byteswapLong(col)**](byteswaplong.md)\
Reverses the byte order of a long value.

Usage: `byteswapLong(col)`\
Example: `SELECT byteswapLong(longCol) FROM myTable`

## Bitwise Functions

[**bitAnd(a, b)** / **bit_and(a, b)**](bitwise.md)\
Performs a bitwise AND operation on two values.

Usage: `bitAnd(a, b)` or `bit_and(a, b)`\
Example: `SELECT bitAnd(12, 10) FROM myTable` returns `8`

[**bitOr(a, b)** / **bit_or(a, b)**](bitwise.md)\
Performs a bitwise OR operation on two values.

Usage: `bitOr(a, b)` or `bit_or(a, b)`\
Example: `SELECT bitOr(8, 4) FROM myTable` returns `12`

[**bitXor(a, b)** / **bit_xor(a, b)**](bitwise.md)\
Performs a bitwise XOR operation on two values.

Usage: `bitXor(a, b)` or `bit_xor(a, b)`\
Example: `SELECT bitXor(12, 10) FROM myTable` returns `6`

[**bitNot(a)**](bitwise.md)\
Performs a bitwise NOT operation, inverting all bits of a value.

Usage: `bitNot(a)`\
Example: `SELECT bitNot(0) FROM myTable` returns `-1`

[**bitMask(n)**](bitwise.md)\
Creates a bitmask with a single bit set at position n.

Usage: `bitMask(n)`\
Example: `SELECT bitMask(3) FROM myTable` returns `8`

[**bitShiftLeft(a, n)**](bitwise.md)\
Performs a left bit shift operation.

Usage: `bitShiftLeft(a, n)`\
Example: `SELECT bitShiftLeft(1, 2) FROM myTable` returns `4`

[**bitShiftRight(a, n)**](bitwise.md)\
Performs an arithmetic right bit shift operation (sign-extending).

Usage: `bitShiftRight(a, n)`\
Example: `SELECT bitShiftRight(8, 2) FROM myTable` returns `2`

[**bitShiftRightUnsigned(a, n)** / **bitShiftRightLogical(a, n)**](bitwise.md)\
Performs a logical (unsigned) right bit shift operation, filling with zeros.

Usage: `bitShiftRightUnsigned(a, n)` or `bitShiftRightLogical(a, n)`\
Example: `SELECT bitShiftRightUnsigned(intCol, 1) FROM myTable`

[**bitExtract(a, n)** / **extractBit(a, n)**](bitwise.md)\
Extracts the bit at position n, returning 1 if the bit is set, 0 otherwise. Always returns INT.

Usage: `bitExtract(a, n)` or `extractBit(a, n)`\
Example: `SELECT bitExtract(12, 2) FROM myTable` returns `1`
