---
description: This page talks about geospatial support in Pinot.
---

# Geospatial

Pinot supports SQL/MM geospatial data and is compliant with the [Open Geospatial Consortium’s \(OGC\) OpenGIS Specifications](https://www.ogc.org/standards/sfs/). This includes:

* Geospatial data types, such as point, line and ploygon;
* Geospatial functions, for querying of spatial properties and relationships.
* \[Upcoming\] Geospatial indexing, used for efficient processing of spatial operations

## Geospatial data types

Geospatial data types abstract and encapsulate spatial structures such as boundary and dimension. In many respects, spatial data types can be understood simply as shapes. Pinot supports the Well-Known Text \(WKT\) and Well-Known Binary \(WKB\) form of geospatial objects, for example:

* `POINT (0, 0)`
* `LINESTRING (0 0, 1 1, 2 1, 2 2)`
* `POLYGON (0 0, 10 0, 10 10, 0 10, 0 0),(1 1, 1 2, 2 2, 2 1, 1 1)`
* `MULTIPOINT (0 0, 1 2)`
* `MULTILINESTRING ((0 0, 1 1, 1 2), (2 3, 3 2, 5 4))`
* `MULTIPOLYGON (((0 0, 4 0, 4 4, 0 4, 0 0), (1 1, 2 1, 2 2, 1 2, 1 1)), ((-1 -1, -1 -2, -2 -2, -2 -1, -1 -1)))`
* `GEOMETRYCOLLECTION(POINT(2 0),POLYGON((0 0, 1 0, 1 1, 0 1, 0 0)))`

### Geometry vs Geography

It is common to have data in which the coordinate are “geographics” or “latitude/longitude”. Unlike coordinates in Mercator or UTM, geographic coordinates are not Cartesian coordinates. Geographic coordinates do not represent a linear distance from an origin as plotted on a plane. Rather, these spherical coordinates describe angular coordinates on a globe. In spherical coordinates a point is specified by the angle of rotation from a reference meridian \(longitude\), and the angle from the equator \(latitude\). You can treat geographic coordinates as approximate Cartesian coordinates and continue to do spatial calculations. However, measurements of distance, length and area will be nonsensical. Since spherical coordinates measure angular distance, the units are in _degrees_.

Pinot supports both geometry and geography types, which can be constructed by the corresponding functions as shown in [section](geospatial-support.md#constructors). And for the geography types, the measurement functions such as `ST_Distance` and `ST_Area` calculate the spherical distance and area on earth respectively.

## Geospatial functions

For manipulating geospatial data, Pinot provides a set of functions for analyzing geometric components, determining spatial relationships, and manipulating geometries. In particular, geospatial functions that begin with the ST\_ prefix support the SQL/MM specification.

The geospatial functions can be grouped into one of the following categories:

### Aggregations

_ST\_Union\(geometry\[\] g1\_array\) → Geometry_   
 This aggregate function returns a MULTI geometry or NON-MULTI geometry from a set of geometries. it ignores NULL geometries.

### Constructors

_ST\_GeomFromText\(String wkt\) → Geometry_   
 Returns a geometry type object from WKT representation, with the optional spatial system reference.

_ST\_GeomFromWKB\(bytes wkb\) → Geometry_   
 Returns a geometry type object from WKB representation.

_ST\_Point\(double x, double y\) → Point_   
 Returns a geometry type point object with the given coordinate values.

_ST\_Polygon\(String wkt\) → Polygon_   
 Returns a geometry type polygon object from WKT representation.

_ST\_GeogFromWKB\(bytes wkb\) → Geography_   
 Creates a geography instance from a Well-Known Binary geometry representation \(WKB\)

_ST\_GeogFromText\(String wkt\) → Geography_   
 Return a specified geography value from Well-Known Text representation or extended \(WKT\).

### Measurements

_ST\_Area\(Geometry/Geography g\) → double_   
 For geometry type, it returns the 2D Euclidean area of a geometry. For geography, returns the area of a polygon or multi-polygon in square meters using a spherical model for Earth.

_ST\_Distance\(Geometry/Geography g1, Geometry/Geography g2\) → double_   
 For geometry type, returns the 2-dimensional cartesian minimum distance \(based on spatial ref\) between two geometries in projected units. For geography, returns the great-circle distance in meters between two SphericalGeography points. Note that g1, g2 shall have the same type.

_ST\_GeometryType\(Geometry g\) → String_   
 Returns the type of the geometry as a string. e.g.: `ST_Linestring`, `ST_Polygon`,`ST_MultiPolygon` etc.

### Outputs

_ST\_AsBinary\(Geometry/Geography g\) → bytes_   
 Returns the WKB representation of the geometry.

_ST\_AsText\(Geometry/Geography g\) → string_   
 Returns the WKT representation of the geometry/geography.

### Relationship

_ST\_Contains\(Geometry, Geometry\) → boolean_   
 Returns true if and only if no points of the second geometry/geography lie in the exterior of the first geometry/geography, and at least one point of the interior of the first geometry lies in the interior of the second geometry.

_ST\_Equals\(Geometry, Geometry\) → boolean_   
 Returns true if the given geometries represent the same geometry/geography.

_ST\_Within\(Geometry, Geometry\) → boolean_   
 Returns true if first geometry is completely inside second geometry.

