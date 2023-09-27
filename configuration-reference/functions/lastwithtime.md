---
description: This section contains reference documentation for the lastwithtime function.
---

# lastwithtime

Get the last value of `dataColumn` where the `timeColumn` is used to define the time of `dataColumn` and the `dataType` specifies the type of `dataColumn`, which can be `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`

## Signature

> LASTWITHTIME(dataColumn, timeColumn, 'dataType')

## Usage Examples

This example is based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select LASTWITHTIME(Dest, ArrTime, 'STRING')
from airlineStats 
```

| value |
| ----- |
| CPR   |

```sql
select LASTWITHTIME(AirTime, ArrTime, 'INT')
from airlineStats 
```

| value |
| ----- |
| 38    |
