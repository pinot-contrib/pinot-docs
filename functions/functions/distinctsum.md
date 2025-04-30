---
description: This section contains reference documentation for the DISTINCTSUM function.
---

# DISTINCTSUM

Returns the sum of distinct row values in a group

## Signature

`DISTINCTSUM(colName) or sum(distinct col)`

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
SELECT DISTINCTSUM(runs) AS VALUE
FROM baseballStats
```

| VALUE |
| ----- |
| 13922 |



```sql
SELECT SUM(DISTINCT AtBatting) AS VALUE
FROM baseballStats
```

| VALUE  |
| ------ |
| 244032 |
