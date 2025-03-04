# Hash Functions

Here’s the revised documentation with **Syntax**, **Parameters**, **Returns**, and **Examples** clearly separated for each function:

***

## Apache Pinot Hash Functions Documentation

### Cryptographic Hash Functions

***

#### SHA

Computes the **SHA-1** hash of the input.

**Syntax**

```sql
SHA(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `STRING`: SHA-1 hash as a lowercase hex string.

**Example**

```sql
SELECT SHA(TO_UTF8('testString')) FROM myTable
-- Returns '956265657d0b637ef65b9b59f9f858eecf55ed6a'
```

***

#### SHA224

Computes the **SHA-224** hash of the input.

**Syntax**

```sql
SHA224(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `STRING`: SHA-224 hash as a lowercase hex string.

**Example**

```sql
SELECT SHA224(TO_UTF8('testString')) FROM myTable
-- Returns 'bb54d1095764bff72b570dcdc3172ed6d1b26695494528a0059c95ae'
```

***

#### SHA256

Computes the **SHA-256** hash of the input.

**Syntax**

```sql
SHA256(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `STRING`: SHA-256 hash as a lowercase hex string.

**Example**

```sql
SELECT SHA256(TO_UTF8('testString')) FROM myTable
-- Returns '4acf0b39d9c4766709a3689f553ac01ab550545ffa4544dfc0b2cea82fba02a3'
```

***

#### SHA512

Computes the **SHA-512** hash of the input.

**Syntax**

```sql
SHA512(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `STRING`: SHA-512 hash as a lowercase hex string.

**Example**

```sql
SELECT SHA512(TO_UTF8('testString')) FROM myTable
-- Returns 'c48af5a7f6d4a851fc8a434eed638ab1a6ef68e19dbcae894ac67c9fbc5bcb0182b8e7123b3df3c9e4dcb7690c23103f03dc17f54352071ceb2a4eb204b26b91'
```

***

#### MD2

Computes the **MD2** hash of the input.

**Syntax**

```sql
MD2(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `STRING`: MD2 hash as a lowercase hex string.

**Example**

```sql
SELECT MD2(TO_UTF8('testString')) FROM myTable
-- Returns '466c453913ba0d8325f96b2d47984fb5'
```

***

#### MD5

Computes the **MD5** hash of the input.

**Syntax**

```sql
MD5(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `STRING`: MD5 hash as a lowercase hex string.

**Example**

```sql
SELECT MD5(TO_UTF8('testString')) FROM myTable
-- Returns '536788f4dbdffeecfbb8f350a941eea3'
```

***

### Non-Cryptographic Hash Functions

***

#### MurmurHash2

Computes a **32-bit MurmurHash2** value.

**Syntax**

```sql
MURMURHASH2(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `INT`: 32-bit hash value (signed integer).

**Example**

```sql
SELECT MURMURHASH2(TO_UTF8('testString')) FROM myTable
-- Returns -534425817
```

***

#### MurmurHash2UTF8

Computes a **32-bit MurmurHash2** value for a UTF-8 string.

**Syntax**

```sql
MURMURHASH2UTF8(input)
```

**Parameters**

* `input` (`STRING`): Input string (converted to UTF-8 bytes).

**Returns**

* `INT`: 32-bit hash value (signed integer).

**Example**

```sql
SELECT MURMURHASH2UTF8('testString') FROM myTable
-- Returns -534425817
```

***

#### MurmurHash2Bit64

Computes a **64-bit MurmurHash2** value.\
**Two overloads are supported:**

**Syntax 1 (No Seed)**

```sql
MURMURHASH2BIT64(input)
```

**Syntax 2 (With Seed)**

```sql
MURMURHASH2BIT64(input, seed)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.
* `seed` (`INT`, optional): Seed value for the hash function.

**Returns**

* `LONG`: 64-bit hash value (signed long).

**Examples**

```sql
SELECT MURMURHASH2BIT64(TO_UTF8('testString')) FROM myTable
-- Returns 3907736674355139845

SELECT MURMURHASH2BIT64(TO_UTF8('testString'), 12345) FROM myTable
-- Returns -2138976126980760436
```

***

#### MurmurHash3Bit32

Computes a **32-bit MurmurHash3** value with a seed.

**Syntax**

```sql
MURMURHASH3BIT32(input, seed)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.
* `seed` (`INT`): Seed value for the hash function.

**Returns**

* `INT`: 32-bit hash value (signed integer).

**Example**

```sql
SELECT MURMURHASH3BIT32(TO_UTF8('testString'), 0) FROM myTable
-- Returns -1435605585
```

***

#### MurmurHash3Bit64

Computes a **64-bit MurmurHash3** value with a seed.

**Syntax**

```sql
MURMURHASH3BIT64(input, seed)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.
* `seed` (`INT`): Seed value for the hash function.

**Returns**

* `LONG`: 64-bit hash value (signed long).

**Example**

```sql
SELECT MURMURHASH3BIT64(TO_UTF8('testString'), 0) FROM myTable
-- Returns -3652179990542706350
```

***

#### MurmurHash3Bit128

Computes a **128-bit MurmurHash3** value with a seed.

**Syntax**

```sql
MURMURHASH3BIT128(input, seed)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.
* `seed` (`INT`): Seed value for the hash function.

**Returns**

* `BYTES`: 128-bit hash as a 16-byte array.

**Example**

```sql
SELECT MURMURHASH3BIT128(TO_UTF8('testString'), 0) FROM myTable
-- Returns byte array: [82, -103, -23, 15, -90, -39, 80, -51, 15, 73, -81, -28, 111, -21, -78, 108]
```

***

#### MurmurHash3X64Bit32 (x64 Optimized)

Computes a **32-bit MurmurHash3** optimized for x64 platforms.

**Syntax**

```sql
MURMURHASH3X64BIT32(input, seed)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.
* `seed` (`INT`): Seed value for the hash function.

**Returns**

* `INT`: 32-bit hash value (signed integer).

**Example**

```sql
SELECT MURMURHASH3X64BIT32(TO_UTF8('testString'), 0) FROM myTable
-- Returns -1096986291
```

***

#### MurmurHash3X64Bit128 (x64 Optimized)

Computes a **128-bit MurmurHash3** optimized for x64 platforms.

**Syntax**

```sql
MURMURHASH3X64BIT128(input, seed)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.
* `seed` (`INT`): Seed value for the hash function.

**Returns**

* `BYTES`: 128-bit hash as a 16-byte array.

**Example**

```sql
SELECT MURMURHASH3X64BIT128(TO_UTF8('testString'), 0) FROM myTable
-- Returns byte array: [-66, -99, 81, 77, -7, 29, 124, 76, 42, 38, -34, -42, -92, -83, 83, 13]
```

***

#### Adler32

Computes a **32-bit Adler checksum**.

**Syntax**

```sql
ADLER32(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `INT`: 32-bit Adler checksum (signed integer).

**Example**

```sql
SELECT ADLER32(TO_UTF8('testString')) FROM myTable
-- Returns 392102968
```

***

#### CRC32

Computes a **32-bit CRC (Cyclic Redundancy Check)**.

**Syntax**

```sql
CRC32(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `INT`: 32-bit CRC32 value (signed integer).

**Example**

```sql
SELECT CRC32(TO_UTF8('testString')) FROM myTable
-- Returns 418708744
```

***

#### CRC32C

Computes a **32-bit CRC32C (Castagnoli)**.

**Syntax**

```sql
CRC32C(input)
```

**Parameters**

* `input` (`BYTES`): Input byte array to hash.

**Returns**

* `INT`: 32-bit CRC32C value (signed integer).

**Example**

```sql
SELECT CRC32C(TO_UTF8('testString')) FROM myTable
-- Returns -1608760557
```

***

### Notes

1. **Input Conversion**: Use `TO_UTF8(string)` to convert strings to `BYTES` where required.
2. **Negative Values**: Hash functions return signed integers/longs. Use `CAST` to interpret them as unsigned if needed.
3. **Byte Arrays**: Functions like `MURMURHASH3BIT128` return `BYTES` as a 16-byte array.
4. **Platform-Specific Variants**:\
   Functions like `MURMURHASH3X64BIT32/64/128` are optimized for x64 architectures. The results could be different cross platform.
