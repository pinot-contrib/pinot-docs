---
description: >-
  This section contains reference documentation for the DISTINCTCOUNTRAWHLL
  function.
---

# DISTINCTCOUNTRAWHLL

Returns HLL response serialized as string. The serialized HLL can be converted back into an HLL and then aggregated with other HLLs. A common use case may be to merge HLL responses from different Pinot tables, or to allow aggregation after client-side batching.

## Signature

> DISTINCTCOUNTRAWHLL(colName, log2m)

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select DISTINCTCOUNTHLL(teamID) AS value
from baseballStats 
```

| value                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 00000008000000ac00000800000084000210000000000020001020220030042002100420002010020210000300008020040180400001300310001863024004220870800004400421040104610220080000020000040000030000800002108420000110400800000106000060000080020000082000218c0002000000020000010200100000018c0006000400022004a0000088000200800000320820021000000221842000000000025088000220080100009420 |

```sql
select DISTINCTCOUNTRAWHLL(teamID, 1) AS value
from baseballStats 
```

| value                    |
| ------------------------ |
| 000000010000000400000106 |
