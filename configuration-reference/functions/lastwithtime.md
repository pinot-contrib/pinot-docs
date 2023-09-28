---
description: This section contains reference documentation for the lastwithtime function.
---

# lastwithtime

Get the last value of `dataColumn` where the `timeColumn` is used to define the time of `dataColumn` and the `dataType` specifies the type of `dataColumn`, which can be `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`

## Signature

> LASTWITHTIME(dataColumn, timeColumn, 'dataType')

## Usage Example

This example is based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select LASTWITHTIME(group_name, __metadata$recordTimestamp, 'STRING')
from meetupRsvp 
```

| value               |
| ------------------- |
| group_name809822304 |
