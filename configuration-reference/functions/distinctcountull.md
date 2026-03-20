---
description: >-
  This section contains reference documentation for the
  DISTINCTCOUNTULL function.
---

# DISTINCTCOUNTULL

The [UltraLogLog](https://github.com/dynatrace-oss/hash4j/blob/main/src/main/java/com/dynatrace/hash4j/distinctcount/UltraLogLog.java) sketch enables space-efficient cardinality estimation using the hash4j library. UltraLogLog provides similar accuracy to HyperLogLog but with reduced memory consumption and faster merge operations.

For exact distinct counting, see [DISTINCTCOUNT](../../functions-1/distinctcount.md).

## Signature

> distinctCountULL(**\<column>, \<p>**) -> Long

* `column` (required): Name of the column to aggregate on.
* `p` (optional): The precision parameter that controls the number of registers used by the sketch. Higher values give more accurate results but use more memory. Default is `12`.

## Usage Examples

```sql
SELECT distinctCountULL(teamID) AS value
FROM baseballStats
```

| value |
| ----- |
| 150   |

```sql
SELECT distinctCountULL(teamID, 14) AS value
FROM baseballStats
```

| value |
| ----- |
| 150   |


### Related Functions

| Function | Description |
| -------- | ----------- |
| [DISTINCTCOUNTULL](distinctcountull.md) | Returns the estimated distinct count as a Long |
| [DISTINCTCOUNTRAWULL](distinctcountrawull.md) | Returns the serialized UltraLogLog sketch as a Base64-encoded String |
| [DISTINCTCOUNTSMARTULL](#distinctcountsmartull) | Hybrid approach that uses a Set for low cardinality and converts to ULL when a threshold is exceeded |

## DISTINCTCOUNTRAWULL

Returns the serialized UltraLogLog sketch as a Base64-encoded string. The serialized sketch can be deserialized and merged with other sketches for multi-stage aggregation across tables.

### Signature

> distinctCountRawULL(**\<column>, \<p>**) -> String

* `column` (required): Name of the column to aggregate on.
* `p` (optional): The precision parameter. Default is `12`.

### Usage Example

```sql
SELECT distinctCountRawULL(teamID) AS sketchValue
FROM baseballStats
```

## DISTINCTCOUNTSMARTULL

A hybrid distinct count function that starts with exact counting using a HashSet for low-cardinality data and automatically switches to UltraLogLog estimation when the number of distinct values exceeds a configurable threshold.

### Signature

> distinctCountSmartULL(**\<column>, \<params>**) -> Integer

* `column` (required): Name of the column to aggregate on.
* `params` (optional): Semicolon-separated parameter string. Supported keys:
  * `threshold`: Number of distinct values before switching from exact Set to ULL. Default is `100000`. Set to a non-positive value to never switch.
  * `p`: Precision parameter for ULL when the switch occurs. Default is `12`.

### Usage Examples

```sql
SELECT distinctCountSmartULL(teamID) AS value
FROM baseballStats
```

```sql
SELECT distinctCountSmartULL(teamID, 'threshold=10000;p=14') AS value
FROM baseballStats
```

This function is useful when you have a mix of low-cardinality and high-cardinality columns and want exact counts for the former while still getting efficient approximate counts for the latter.
