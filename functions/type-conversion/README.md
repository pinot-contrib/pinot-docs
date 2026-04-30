# Type Conversion Functions

Pinot provides functions for converting values between data types, as well as encoding and decoding between binary, hex, and Base64 representations.

## CAST

```sql
CAST(value AS type)
```

Converts a value to the specified target type. This is the standard SQL cast syntax supported by Pinot.

**Supported target types:**

| Type | Aliases | Description |
|---|---|---|
| `INT` | `INTEGER` | 32-bit integer |
| `LONG` | `BIGINT` | 64-bit integer |
| `FLOAT` | | 32-bit floating point |
| `DOUBLE` | | 64-bit floating point |
| `BOOLEAN` | | Boolean value |
| `TIMESTAMP` | | Timestamp value |
| `STRING` | `VARCHAR` | String value |
| `BYTES` | `VARBINARY` | Byte array |
| `BIG_DECIMAL` | `DECIMAL` | Arbitrary-precision decimal |

For array-valued casts, Pinot supports `CAST(expr AS DECIMAL ARRAY)` in standard SQL. In the single-stage engine, Pinot also accepts the Pinot-specific target name `BIG_DECIMAL_ARRAY`.

```sql
SELECT CAST(revenue AS DOUBLE) AS revenue_double,
       CAST(zipCode AS VARCHAR) AS zip_string,
       CAST('12345' AS BIGINT) AS id_long
FROM orders
LIMIT 5
```

The function-call form `cast(value, 'TYPE')` is also supported:

```sql
SELECT cast(revenue, 'DOUBLE') AS revenue_double
FROM orders
LIMIT 5
```

When casting a `STRING` to `INT` or `LONG`, Pinot will first attempt direct integer parsing. If that fails, it will parse the string as a `DOUBLE` and truncate. For `LONG`, Pinot also attempts timestamp parsing before falling back to double conversion.

## bigDecimalToBytes

```sql
bigDecimalToBytes(bigDecimalCol)
```

Serializes a `BIG_DECIMAL` value to its byte array representation. The resulting bytes contain the unscaled value appended to the scale in big-endian order.

```sql
SELECT bigDecimalToBytes(price) AS priceBytes
FROM products
LIMIT 5
```

## bytesToBigDecimal

```sql
bytesToBigDecimal(bytesCol)
```

Deserializes a byte array (previously created by `bigDecimalToBytes`) back to a `BIG_DECIMAL` value.

```sql
SELECT bytesToBigDecimal(priceBytes) AS price
FROM products
LIMIT 5
```

## hexToBytes

```sql
hexToBytes(hexString)
```

Converts a plain hex string to a byte array.

```sql
SELECT hexToBytes('f0e1a3b2') AS rawBytes
FROM myTable
LIMIT 1
-- Converts hex string to 4-byte array
```

## bytesToHex

```sql
bytesToHex(bytesCol)
```

Converts a byte array to a plain hex string.

```sql
SELECT bytesToHex(rawData) AS hexString
FROM myTable
LIMIT 5
-- Returns hex representation such as 'f012be3c'
```

## base64Encode

```sql
base64Encode(bytesCol)
```

Encodes a byte array to its Base64 representation.

```sql
SELECT base64Encode(payload) AS encodedPayload
FROM events
LIMIT 5
```

## base64Decode

```sql
base64Decode(bytesCol)
```

Decodes a Base64-encoded byte array back to the original bytes.

```sql
SELECT base64Decode(encodedPayload) AS originalPayload
FROM events
LIMIT 5
```

## hexDecimalToLong

```sql
hexDecimalToLong(hexString)
```

Converts a hexadecimal string to its corresponding `LONG` value. Accepts strings with or without the `0x` prefix.

```sql
SELECT hexDecimalToLong('0x1a2b') AS longVal
FROM myTable
LIMIT 1
-- Returns 6699
```

## longToHexDecimal

```sql
longToHexDecimal(longCol)
```

Converts a `LONG` value to its hexadecimal string representation.

```sql
SELECT longToHexDecimal(6699) AS hexVal
FROM myTable
LIMIT 1
-- Returns '1a2b'
```
