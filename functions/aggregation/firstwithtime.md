---
description: This section contains reference documentation for the firstwithtime function.
---

# FIRSTWITHTIME

Returns the value of `dataColumn` with the smallest `timeColumn` value where:

* `timeColumn` is used to define the time of `dataColumn`, which can be of type `TIMESTAMP`, `INT`, `LONG`
* `dataColumn` must be single-value. Supported data types are `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`, `TIMESTAMP`, `BIG_DECIMAL`, `BYTES`, `UUID` and `JSON`.

## Signature

> FIRSTWITHTIME(dataColumn, timeColumn, 'dataType')

> FIRST_WITH_TIME(dataColumn, timeColumn)

Both query engines support the two-argument form, inferring the data column's type. The explicit three-argument form remains supported. `FIRSTWITHTIME` and `FIRST_WITH_TIME` are equivalent spellings.

## Example

This example is based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select FIRST_WITH_TIME(group_name, __metadata$recordTimestamp)
from meetupRsvp 
```

| value                 |
| --------------------- |
| group\_name1016303453 |
