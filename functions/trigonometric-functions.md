# Trigonometric Functions

Pinot provides standard trigonometric functions that operate on `double` values. Angles are expressed in radians unless otherwise noted. Use the `radians()` function to convert degrees to radians before passing values to trigonometric functions.

## sin

```sql
sin(col)
```

Returns the sine of the given angle (in radians).

```sql
SELECT sin(radians(30))
FROM myTable
-- Returns 0.49999999999999994
```

## cos

```sql
cos(col)
```

Returns the cosine of the given angle (in radians).

```sql
SELECT cos(radians(60))
FROM myTable
-- Returns 0.5000000000000001
```

## tan

```sql
tan(col)
```

Returns the tangent of the given angle (in radians).

```sql
SELECT tan(radians(45))
FROM myTable
-- Returns 0.9999999999999999
```

## cot

```sql
cot(col)
```

Returns the cotangent of the given angle (in radians), computed as `1 / tan(col)`.

```sql
SELECT cot(radians(45))
FROM myTable
-- Returns 1.0000000000000002
```

## asin

```sql
asin(col)
```

Returns the arc sine of a value, in radians. The input must be between -1 and 1.

```sql
SELECT asin(0.5)
FROM myTable
-- Returns 0.5235987755982989 (pi/6)
```

## acos

```sql
acos(col)
```

Returns the arc cosine of a value, in radians. The input must be between -1 and 1.

```sql
SELECT acos(0.5)
FROM myTable
-- Returns 1.0471975511965979 (pi/3)
```

## atan

```sql
atan(col)
```

Returns the arc tangent of a value, in radians.

```sql
SELECT atan(1)
FROM myTable
-- Returns 0.7853981633974483 (pi/4)
```

## atan2

```sql
atan2(y, x)
```

Returns the angle in radians between the positive x-axis and the point (x, y), using the signs of both arguments to determine the quadrant.

```sql
SELECT atan2(1, 1)
FROM myTable
-- Returns 0.7853981633974483 (pi/4)
```

## sinh

```sql
sinh(col)
```

Returns the hyperbolic sine of the given value.

```sql
SELECT sinh(1)
FROM myTable
-- Returns 1.1752011936438014
```

## cosh

```sql
cosh(col)
```

Returns the hyperbolic cosine of the given value.

```sql
SELECT cosh(1)
FROM myTable
-- Returns 1.5430806348152437
```

## tanh

```sql
tanh(col)
```

Returns the hyperbolic tangent of the given value.

```sql
SELECT tanh(1)
FROM myTable
-- Returns 0.7615941559557649
```

## degrees

```sql
degrees(col)
```

Converts an angle measured in radians to an approximately equivalent angle measured in degrees.

```sql
SELECT degrees(3.141592653589793)
FROM myTable
-- Returns 180.0
```

## radians

```sql
radians(col)
```

Converts an angle measured in degrees to an approximately equivalent angle measured in radians.

```sql
SELECT radians(180)
FROM myTable
-- Returns 3.141592653589793
```
