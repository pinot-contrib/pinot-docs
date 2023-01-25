---
description: This section contains reference documentation for the DISTINCTSUMMV function.
---

# DISTINCTSUMMV

Returns the sum of the distinct row values in a group

## Signature

> DISTINCTSUMMV(colName)

### Usage Examples <a href="#usage-examples" id="usage-examples"></a>

These examples are based on the [Hybrid Quick Start](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/basics/getting-started/quick-start#hybrid).

```sql
SELECT DISTINCTSUMMV(DivLongestGTimes) AS VALUE
FROM airlineStats
WHERE arraylength(DivLongestGTimes) > 1
```

| VALUE |
| ----- |
| 1134  |
