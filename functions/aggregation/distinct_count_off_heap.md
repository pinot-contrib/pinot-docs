---
description: >-
  This section contains reference documentation for the DISTINCT_COUNT_OFF_HEAP
  function.
---

# DISTINCT\_COUNT\_OFF\_HEAP

Returns the count of distinct values. The values are stored using off-heap memory.

## Signature

> DISTINCT\_COUNT\_OFF\_HEAP(col\[, params])

* `col` (required): Name of the column to aggregate on.
* `params` (optional): Semicolon-separated parameter key-value pairs:
  * `initialCapacity`: The initial capacity of the set for non-dictionary-encoded case (default _10000_).
  * `hashbits`: Number of bits for _murmur3_: _32_/_64_/_128_ (default _64_)
* Example: `DISTINCT_COUNT_OFF_HEAP(col, 'initialCapacity=100000;hashbits=128')`

## Note

* For variable length data types such as `STRING` and `BYTES`, _murmur3_ hash values are used to represent the values.
* Currently it only supports aggregate without group-by. For MV column, it only supports fixes lengh types.
