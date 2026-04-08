---
description: This section contains reference documentation for the gridDisk function.
---

# GridDisk

Returns the center H3 cell together with all cells within `k` grid steps of it.

## Signature

> gridDisk(h3Index, k)

| Arguments | Description |
| --- | --- |
| `h3Index` | Center H3 index. |
| `k` | Non-negative grid distance from the center cell. `0` returns only the input cell. |

## Usage Examples

```sql
SELECT gridDisk(0x8928308280fffff, 0) AS cells
FROM ignoreMe;
```

| cells |
| --- |
| `[617700169958293503]` |
