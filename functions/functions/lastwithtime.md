---
description: This section contains reference documentation for the lastwithtime function.
---

# LASTWITHTIME

Returns the value of `dataColumn` with the largest `timeColumn` value where:

* `timeColumn` is used to define the time of `dataColumn`, which can be of type `TIMESTAMP`, `INT`, `LONG`
* `dataType` specifies the type for `dataColumn`, which can be `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`

## Signature

> LASTWITHTIME(dataColumn, timeColumn, 'dataType')

## Example

This example is based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select LASTWITHTIME(group_name, __metadata$recordTimestamp, 'STRING')
from meetupRsvp 
```

| value                |
| -------------------- |
| group\_name809822304 |
