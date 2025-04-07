---
description: >-
  This section contains reference documentation for the DISTINCT_COUNT_SMART_HLL
  function.
---

# DISTINCTCOUNTSMARTHLL

## Signature

> DISTINCT\_COUNT\_SMART\_HLL(col\[, params])

* `col` (required): Name of the column to aggregate on.
* `params` (optional): Semicolon-separated parameter key-value pairs:
  * `threshold`: The threshold to convert the value set into a _HyperLogLog_ (default _100\_000_).
  * `log2m`: _log2m_ for the _HyperLogLog_ (default _12_).
* Example: `DISTINCT_COUNT_SMART_HLL(col, 'threshold=10000;log2m=8')`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

## **DISTINCTCOUNTSMARTHLL considerations**

* `DISTINCTCOUNTHLL()`is faster than `DISTINCTCOUNT()`if data is pre-aggregated at ingestion or aggregated at a server with enough records. This performance improvement increases when comparing large datasets.
* If very few records are pre-aggregated, `DISTINCTCOUNTHLL()`will not be as fast as `DISTINCTCOUNT()`because the serialized HLL size is larger than sending individual values.
* `DISTINCTCOUNTHLLPLUS()`provides more precise results than `DISTINCTCOUNTHLL()`with the same performance.
* `DISTINCTCOUNTSMARTHLL()`automatically shifts to HLL when reaching a threshold, and comes with some overhead.

