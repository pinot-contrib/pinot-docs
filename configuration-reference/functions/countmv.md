---
description: This section contains reference documentation for the COUNTMV function.
---

# COUNTMV

Get the count of rows in a group

## Signature

> COUNTMV(colName)

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).

The following query returns the documents that have a `DivTailNums` with more than one value:


```sql
select DivTailNums
from airlineStats 
where arraylength(DivTailNums) > 1
```

| DivTailNums   | 
| ------------- |
|N7713A,N7713A|
|N344AA,N344AA|
|N344AA,N344AA|
|N7713A,N7713A|

You can count the number of items in these rows by running the following query:

```sql
select COUNTMV(DivTailNums) AS value
from airlineStats 
where arraylength(DivTailNums) > 1
```

| value   | 
| ------------- |
| 8 | 
