---
description: This section contains reference documentation for the ARRAYLENGTH function.
---

# ARRAYLENGTH

Returns the length of a multi-value column

## Signature

> ARRAYLENGTH('colName')

## Usage Examples

These examples are based on the [Hybrid Quick Start](../../basics/getting-started/quick-start.md#hybrid).


```sql
select ARRAYLENGTH(RandomAirports) AS length, count(*) 
from airlineStats 
GROUP BY length
ORDER BY count(*) DESC
LIMIT 5
```

| length   | count(*) | 
| ------------- | ------------- |
|1	|5382|
|37	|267|
|33	|223|
|17	|166|
|22	|160|


{% hint style="info" %}
The `count(*)` values will increase each time we execute the query as data is constantly being ingested by the Hybrid Quick Start.
{% endhint %}
