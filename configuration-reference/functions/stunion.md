---
description: This section contains reference documentation for the ST_Union function.
---

# ST_Union

An aggregation function that returns a MULTI geometry or NON-MULTI geometry from a set of geometries. 
It ignores NULL geometries.

## Signature

> ST_Union(geometry[])

## Usage Examples

These examples are based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).



```sql
select group_city, ST_AsText(STUnion(location)) AS unionString
from meetupRsvp 
GROUP BY group_city
ORDER BY STUnion(location) DESC
LIMIT 5
```

| group_city | unionString | 
| ------------- | ------------- |
|London |	MULTIPOINT ((-0.21 51.54), (-0.19 51.5), (-0.19 51.56), (-0.18 51.49), (-0.18 51.51), (-0.18 51.52), (-0.16 51.52), (-0.14 51.54), (-0.13 51.5), (-0.13 51.51), (-0.13 51.52), (-0.13 51.53), (-0.12 51.51), (-0.12 51.53), (-0.11 51.53), (-0.1 51.5), (-0.1 51.52), (-0.09 51.|5), (-0.09 51.52), (-0.07 51.52), (-0.02 51.49), (0.06 51.51)) |
|New York |	MULTIPOINT ((-74 40.72), (-74 40.74), (-73.99 40.73), (-73.99 40.75), (-73.99 40.76), (-73.98 40.75), (-73.98 40.79), (-73.97 40.75), (-73.94 40.81)) |
|Austin	| MULTIPOINT ((-97.76 30.24), (-97.75 30.22), (-97.74 30.27), (-97.74 30.32), (-97.73 30.35), (-97.71 30.27), (-97.71 30.38), (-97.71 30.42)) |
|Denver	| MULTIPOINT ((-105.08 39.7), (-105.01 39.77), (-104.99 39.75), (-104.98 39.73), (-104.96 39.68), (-104.93 39.7), (-104.92 39.68)) |
|Atlanta	| MULTIPOINT ((-84.47 33.86), (-84.44 33.79), (-84.4 33.86), (-84.39 33.75), (-84.38 33.77), (-84.32 33.82), (-84.25 33.89)) |