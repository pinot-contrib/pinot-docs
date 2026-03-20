---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTHLLPLUS
  function.
---

# DISTINCTCOUNTHLLPLUS



## Signature

> DISTINCTCOUNTHLLPLUS(colName, log2m)

## Usage Examples

## **DISTINCTCOUNTHLLPLUS considerations**

* `DISTINCTCOUNTHLL()`is faster than `DISTINCTCOUNT()`if data is pre-aggregated at ingestion or aggregated at a server with enough records. This performance improvement increases when comparing large datasets.
* If very few records are pre-aggregated, `DISTINCTCOUNTHLL()`will not be as fast as `DISTINCTCOUNT()`because the serialized HLL size is larger than sending individual values.
* `DISTINCTCOUNTHLLPLUS()`provides more precise results than `DISTINCTCOUNTHLL()`with the same performance.
* `DISTINCTCOUNTSMARTHLL()`automatically shifts to HLL when reaching a threshold, and comes with some overhead.
* `DISTINCTCOUNTSMARTHLLPLUS()`automatically shifts to HLLPlus when reaching a threshold, and comes with some overhead.

