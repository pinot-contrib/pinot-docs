---
description: >-
  This section contains reference documentation for base64 encode and decode
  functions.
---

# Base64

Encoding scheme follows [java.util.Base64.Encoder](https://docs.oracle.com/javase/8/docs/api/java/util/Base64.Encoder.html)

* `toBase64` returns Base64 encoded string of input binary data (`bytes` type).
* `fromBase64` returns binary data (represented as a Hex string) from Base64-encoded string.

## Signature

> toBase64(bytesCol)
>
> fromBase64(stringCol)

## Usage Examples

{% hint style="info" %}
For better readability, the following examples converts string `hello!` into BYTES using [toUtf8](https://docs.pinot.apache.org/configuration-reference/functions/utf8) function and converts the decoded BYTES into string using [fromUtf8](https://docs.pinot.apache.org/configuration-reference/functions/utf8).
{% endhint %}

```sql
SELECT toBase64(toUtf8('hello!')) AS encoded
FROM ignoreMe
```

| encoded  |
| -------- |
| aGVsbG8h |

```sql
SELECT fromUtf8(fromBase64('aGVsbG8h')) AS decoded
FROM ignoreMe
```

| decoded |
| ------- |
| hello!  |

{% hint style="info" %}
Note that without UTF8 string conversion, returned BYTES will be represented as a Hex string following Pinot's [BYTES column representation](https://docs.pinot.apache.org/users/user-guide-query/querying-pinot#bytes-column). See the example below.
{% endhint %}

```sql
SELECT fromBase64('aGVsbG8h') AS decoded
FROM ignoreMe
```

| decoded      |
| ------------ |
| 68656c6c6f21 |

{% hint style="warning" %}
Note that the following query will throw compilation error as string is not a valid input type for `toBase64`.
{% endhint %}

```sql
SELECT toBase64('hello!') AS encoded
FROM ignoreMe
```
