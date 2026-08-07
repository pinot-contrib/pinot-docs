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

Pinot also accepts the SQL-standard unsigned integer targets `TINYINT UNSIGNED`, `SMALLINT UNSIGNED`, and
`INTEGER UNSIGNED`. Because Pinot does not store unsigned integers, these casts return the narrowest signed type that
preserves the full range: `TINYINT UNSIGNED` and `SMALLINT UNSIGNED` behave like `INT`, while `INTEGER UNSIGNED`
behaves like `LONG`. `BIGINT UNSIGNED` is not supported; use `BIGINT` or `DECIMAL` instead.

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

## UUID functions

Pinot provides UUID-aware functions in both the single-stage and multi-stage query engines. The UUID semantic functions accept a `STRING`, a 16-byte `BYTES` value, or a logical `UUID` column. String inputs can use canonical dashed RFC 4122 text or 32 hexadecimal digits without dashes.

Use `UUID_TO_STRING` when you need a stable external representation: it always returns lowercase UUID text with dashes. `CAST(uuid_expression AS STRING)` uses the same canonical dashed representation for single-value and multi-value logical `UUID` expressions. Generic `BYTES` values are unchanged and still render as hexadecimal; Pinot decodes bytes as UUIDs only inside UUID-aware functions.

| Function | Input | Result | Behavior |
| --- | --- | --- | --- |
| `IS_UUID(value)` | `STRING`, `BYTES`, `UUID` | `BOOLEAN` | Returns `false` for an invalid non-null value. A valid byte value is exactly 16 bytes. |
| `TO_UUID(value)` | `STRING`, `BYTES`, `UUID` | `UUID` | Converts a UUID representation into Pinot's logical UUID type. |
| `BYTES_TO_UUID(bytes)` | `BYTES` only | `UUID` | Strictly converts a 16-byte UUID value. |
| `UUID_TO_STRING(value)` | `STRING`, `BYTES`, `UUID` | `STRING` | Returns canonical lowercase dashed UUID text. |
| `UUID_TO_BYTES(value)` | `STRING`, `BYTES`, `UUID` | `BYTES` | Returns the canonical 16-byte UUID representation. |
| `UUID_VERSION(value)` | `STRING`, `BYTES`, `UUID` | `INT` | Returns the 4-bit UUID version field. |
| `UUID_TIMESTAMP(value)` | `STRING`, `BYTES`, `UUID` | `LONG` | Returns Unix epoch milliseconds from a time-based version 1, 6, or 7 UUID; other versions cause an error. |
| `UUID_V4()` | No arguments | `UUID` | Generates a fresh random RFC 4122 version 4 UUID. |
| `UUID_V7()` | No arguments | `UUID` | Generates a fresh RFC 9562 version 7 UUID with the current Unix time in milliseconds in its leading 48 bits. |

The generators are non-deterministic: each invocation produces a new UUID. Version 7 values are k-sortable by timestamp, but UUIDs generated within the same millisecond are not guaranteed to be strictly ordered.

```sql
SELECT
  UUID_TO_STRING('550E8400-E29B-41D4-A716-446655440000') AS canonical_uuid,
  CAST(TO_UUID('550E8400-E29B-41D4-A716-446655440000') AS STRING) AS cast_uuid,
  UUID_TO_STRING(UUID_TO_BYTES('550e8400-e29b-41d4-a716-446655440000')) AS from_bytes,
  UUID_VERSION('550e8400-e29b-41d4-a716-446655440000') AS uuid_version;
```

`canonical_uuid`, `cast_uuid`, and `from_bytes` are `550e8400-e29b-41d4-a716-446655440000`, and `uuid_version` is `4`.

For UUID column configuration, ingestion, and query-result rendering, see [UUID columns](../../reference/configuration-reference/schema.md#uuid-columns).

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
