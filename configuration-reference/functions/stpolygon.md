---
description: This section contains reference documentation for the ST_Polygon function.
---

# ST_Polygon

Returns a geometry type polygon object from [Well-Known Text representation or extended (WKT)](https://en.wikipedia.org/wiki/Well-known\_text\_representation\_of\_geometry). 


{% hint style="info" %}
This function only works for WKT formatted polygons. 
{% endhint %}

## Signature

> ST_Polygon(wkt)

## Usage Examples

These examples are based on the [Streaming Quick Start](../../basics/getting-started/quick-start.md#streaming).

```sql
select ST_Polygon('POLYGON ((2 2, 2 6, 6 6, 6 2, 2 2))') AS value
from meetupRsvp 
LIMIT 1
```

| value | 
| ------------- | 
|040000000100000005000000004000000000000000400000000000000040000000000000004018000000000000401800000000000040180000000000004018000000000000400000000000000040000000000000004000000000000000 | 


```sql
select ST_Polygon('POLYGON EMPTY') AS value
from meetupRsvp 
LIMIT 1
```

| value | 
| ------------- | 
|040000000000000000 | 

This function doesn't accept values that represent non polygons.
It will throw an exception if passed other primitives or geometries:

```sql
select ST_Polygon('LINESTRING (30 10, 10 30, 40 40)') AS value
from meetupRsvp 
LIMIT 1
```

```text
[
  {
    "message": "QueryExecutionError:\njava.lang.IllegalArgumentException: The geometry object must be polygon\n\tat shaded.com.google.common.base.Preconditions.checkArgument(Preconditions.java:122)\n\tat org.apache.pinot.core.geospatial.transform.function.StPolygonFunction.transformToBytesValuesSV(StPolygonFunction.java:58)\n\tat org.apache.pinot.core.operator.docvalsets.TransformBlockValSet.getBytesValuesSV(TransformBlockValSet.java:95)\n\tat org.apache.pinot.core.common.RowBasedBlockValueFetcher.createFetcher(RowBasedBlockValueFetcher.java:66)",
    "errorCode": 200
  }
]
```

To create geometry objects for non polygons, see [ST_GeomFromText](stgeomfromtext.md).