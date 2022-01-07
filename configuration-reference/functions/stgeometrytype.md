---
description: This section contains reference documentation for the ST_GeometryType function.
---

# ST_GeometryType

Returns the type of the geometry as a string

## Signature

> ST_GeometryType(geometry)

## Usage Examples

These examples are based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select location, ST_GeometryType(location) AS type
from meetupRsvp 
LIMIT 1
```

| location   | type | 
| ------------- | -------------  | 
|80c00dae147ae147ae404435c28f5c28f6 | Point | 
