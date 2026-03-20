# Math Functions

​[**ADD(col1, col2, col3...)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/add) Sum of at least two values

​[**SUB(col1, col2)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/sub) Difference between two values

​[**MULT(col1, col2, col3...)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/mult) Product of at least two values

​[**DIV(col1, col2)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/div) Quotient of two values

​[**MOD(col1, col2)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/mod) Modulo of two values

​[**ABS(col1)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/abs) Absolute of a value

​[**CEIL(col1)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/ceil#signature) Rounded up to the nearest integer

​[**FLOOR(col1)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/floor) Rounded down to the nearest integer

​[**EXP(col1)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/exp) Euler's number(e) raised to the power of col.

​[**LN(col1)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/ln) Natural log of value

​[**SQRT(col1)**](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/sqrt) Square root of a value

​[**ROUNDDECIMAL(col1, col2)** ](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/~/changes/2166/functions-1/round-1)​Rounds value to a specified number of decimal places

**intDiv(col1, col2)**\
Returns the integer result of dividing col1 by col2, rounded down (floor division). Returns a `Long`.

Usage: `intDiv(col1, col2)`\
Example: `SELECT intDiv(10, 3) FROM myTable` returns `3`

**intDivOrZero(col1, col2)**\
Same as `intDiv` but returns zero when dividing by zero or when dividing a minimal negative number by minus one.

Usage: `intDivOrZero(col1, col2)`\
Example: `SELECT intDivOrZero(10, 0) FROM myTable` returns `0`

**isFinite(col)**\
Returns `1` if the value is finite (not infinite and not NaN), `0` otherwise.

Usage: `isFinite(col)`\
Example: `SELECT isFinite(salary) FROM myTable`

**isInfinite(col)**\
Returns `1` if the value is infinite (positive or negative infinity), `0` otherwise.

Usage: `isInfinite(col)`\
Example: `SELECT isInfinite(ratio) FROM myTable`

**ifNotFinite(valueToCheck, defaultValue)**\
Returns `valueToCheck` if it is finite, otherwise returns `defaultValue`.

Usage: `ifNotFinite(col, defaultValue)`\
Example: `SELECT ifNotFinite(ratio, 0) FROM myTable`

**isNaN(col)**\
Returns `1` if the value is NaN (Not a Number), `0` otherwise.

Usage: `isNaN(col)`\
Example: `SELECT isNaN(ratio) FROM myTable`

**moduloOrZero(col1, col2)**\
Same as `MOD` but returns zero when dividing by zero or when dividing a minimal negative number by minus one.

Usage: `moduloOrZero(col1, col2)`\
Example: `SELECT moduloOrZero(10, 0) FROM myTable` returns `0`

**positiveModulo(col1, col2)**\
Returns the modulo of two values, always returning a non-negative result.

Usage: `positiveModulo(col1, col2)`\
Example: `SELECT positiveModulo(-7, 3) FROM myTable` returns `2`

**negate(col)**\
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

**gcd(col1, col2)**\
Returns the greatest common divisor of two long values.

Usage: `gcd(col1, col2)`\
Example: `SELECT gcd(12, 8) FROM myTable` returns `4`

**lcm(col1, col2)**\
Returns the least common multiple of two long values.

Usage: `lcm(col1, col2)`\
Example: `SELECT lcm(4, 6) FROM myTable` returns `12`

**hypot(col1, col2)**\
Returns the hypotenuse of a right-angled triangle, i.e. `sqrt(col1^2 + col2^2)`, without intermediate overflow or underflow.

Usage: `hypot(col1, col2)`\
Example: `SELECT hypot(3, 4) FROM myTable` returns `5.0`

**byteswapInt(col)**\
Reverses the byte order of an integer value.

Usage: `byteswapInt(col)`\
Example: `SELECT byteswapInt(intCol) FROM myTable`

**byteswapLong(col)**\
Reverses the byte order of a long value.

Usage: `byteswapLong(col)`\
Example: `SELECT byteswapLong(longCol) FROM myTable`
