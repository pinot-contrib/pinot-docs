---
description: This section contains reference documentation for the firstwithtime function.
---

# firstwithtime

Get the first value of `dataColumn` where the `timeColumn` is used to define the time of `dataColumn` and the `dataType` specifies the type of `dataColumn`, which can be `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`

## Signature

> FIRSTWITHTIME(dataColumn, timeColumn, 'dataType')

## Usage Example

This example is based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select FIRSTWITHTIME(group_name, __metadata$recordTimestamp, 'STRING')
from meetupRsvp 
```

| value                |
| -------------------- |
| group_name1016303453 | 
