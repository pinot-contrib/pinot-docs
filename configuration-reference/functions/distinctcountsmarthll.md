---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLL
  function.
---

# DISTINCTCOUNTSMARTHLL

## Signature

> DISTINCTCOUNTSMARTHLL(colName, log2m)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

## **DISTINCTCOUNTSMARTHLL considerations**

* `DISTINCTCOUNTHLL()`is faster than `DISTINCTCOUNT()`if data is pre-aggregated at ingestion or aggregated at a server with enough records. This performance improvement increases when comparing large datasets.
* If very few records are pre-aggregated, `DISTINCTCOUNTHLL()`will not be as fast as `DISTINCTCOUNT()`because the serialized HLL size is larger than sending individual values.
* `DISTINCTCOUNTHLLPLUS()`provides more precise results than `DISTINCTCOUNTHLL()`with the same performance.
* `DISTINCTCOUNTSMARTHLL()`automatically shifts to HLL when reaching a threshold, and comes with some overhead.

