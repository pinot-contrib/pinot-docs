---
description: This section contains reference documentation for the lastwithtime function.
---

# LASTWITHTIME

Returns the value of `dataColumn` with the largest `timeColumn` value where:

* `timeColumn` is used to define the time of `dataColumn`, which can be of type `TIMESTAMP`, `INT`, `LONG`
* `dataColumn` must be single-value. Supported data types are `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`, `TIMESTAMP`, `BIG_DECIMAL`, `BYTES`, `UUID` and `JSON`.

## Signature

> LASTWITHTIME(dataColumn, timeColumn, 'dataType')

> LAST_WITH_TIME(dataColumn, timeColumn)

Both query engines support the two-argument form, inferring the data column's type. The explicit three-argument form remains supported. `LASTWITHTIME` and `LAST_WITH_TIME` are equivalent spellings.

## Example

This example is based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select LAST_WITH_TIME(group_name, __metadata$recordTimestamp)
from meetupRsvp 
```

| value                |
| -------------------- |
| group\_name809822304 |
