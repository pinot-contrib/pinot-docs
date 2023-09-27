---
description: This section contains reference documentation for the firstwithtime function.
---

# firstwithtime

Get the first value of `dataColumn` where the `timeColumn` is used to define the time of `dataColumn` and the `dataType` specifies the type of `dataColumn`, which can be `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`

## Signature

> FIRSTWITHTIME(dataColumn, timeColumn, 'dataType')

## Usage Examples

This example is based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select FIRSTWITHTIME(Dest, ArrTime, 'STRING')
from airlineStats 
```

| value |
| ----- |
| CPR   | * need to re-run quickstart and update this

```sql
select FIRSTWITHTIME(AirTime, ArrTime, 'INT')
from airlineStats 
```

| value |
| ----- |
| 38    | * need to re-run quickstart and update this
