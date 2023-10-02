---
description: This section contains reference documentation for the firstwithtime function.
---

# firstwithtime

This function is used for FirstWithTime calculations.

The function will return the value of `dataColumn` with the smallest `timeColumn` value where:
- `timeColumn` is used to define the time of `dataColumn`, which can be of type `TIMESTAMP`, `INT`, `LONG`
- `dataType` specifies the type for `dataColumn`, which can be `BOOLEAN`, `INT`, `LONG`, `FLOAT`, `DOUBLE`, `STRING`

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
