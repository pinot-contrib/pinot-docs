---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTRAWULL
  function.
---

# DISTINCTCOUNTRAWULL

The [UltraLogLog Sketch](https://arxiv.org/abs/2308.16862) from Dynatrace is a variant of _HyperLogLog_ and is used for approximate distinct counts.  The UltraLogLog sketch shares many of the same properties of a typical HyperLogLog sketch but requires less space and also provides a simpler and faster estimator.

Pinot uses an production-ready Java implementation available in [Hash4j](https://github.com/dynatrace-oss/hash4j/tree/main) available under the Apache license.

For exact distinct counting, see [DISTINCTCOUNT](distinctcount.md).  This function call returns the sketch encoded as hexadecimal to the user.

## Signature

> distinctCountRawULL(**\<ullSketchColumn>, \<ullSketchPrecision>**) -> HexEncoded

* `ullSketchColumn` (required): Name of the column to aggregate on.
* `ullSketchPrecision` (optional): p which is the precision parameter, which controls both the size and accuracy of the sketch.  If not supplied, the Helix default is used.

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select distinctCountRawULL(teamID) AS value
from baseballStats 
```

| value                                     |
| ----------------------------------------- |
| AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA... |

```sql
select distinctCountRawULL(teamID, 14) AS value
from baseballStats 
```

| value                                     |
| ----------------------------------------- |
| AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA... |
