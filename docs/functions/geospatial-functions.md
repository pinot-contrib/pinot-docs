# GeoSpatial Functions

For manipulating geospatial data, Pinot provides a set of functions for analyzing geometric components, determining spatial relationships, and manipulating geometries. In particular, geospatial functions that begin with the `ST_` prefix support the SQL/MM specification.

Following geospatial functions are available out of the box in Pinot:

### Aggregations

#### [**ST\_Union(geometry\[\] g1\_array) → Geometry**](../functions-1/stunion.md)&#x20;

This aggregate function returns a MULTI geometry or NON-MULTI geometry from a set of geometries. it ignores NULL geometries.

### Constructors

#### [**ST\_GeomFromText(String wkt) → Geometry**](../functions-1/stgeomfromtext.md)&#x20;

Returns a geometry type object from WKT representation, with the optional spatial system reference.

#### [**ST\_GeomFromWKB(bytes wkb) → Geometry**](../functions-1/stgeomfromwkb.md)&#x20;

Returns a geometry type object from WKB representation.

#### [**ST\_Point(double x, double y) → Point**](../functions-1/stpoint.md)&#x20;

Returns a geometry type point object with the given coordinate values.

#### [**ST\_Polygon(String wkt) → Polygon**](../functions-1/stpolygon.md)&#x20;

Returns a geometry type polygon object from [WKT representation](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry).

#### [**ST\_GeogFromWKB(bytes wkb) → Geography**](../functions-1/stgeogfromwkb.md)&#x20;

Creates a geography instance from a [Well-Known Binary geometry representation (WKB)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Well-known_binary)

#### [**ST\_GeogFromText(String wkt) → Geography**](../functions-1/stgeogfromtext.md)&#x20;

Returns a specified geography value from [Well-Known Text representation or extended (WKT)](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry).

### Measurements

#### **ST\_Area(Geometry/Geography g) → double**&#x20;

For geometry type, it returns the 2D Euclidean area of a geometry. For geography, returns the area of a polygon or multi-polygon in square meters using a spherical model for Earth.

#### [**ST\_Distance(Geometry/Geography g1, Geometry/Geography g2) → double**](../functions-1/stdistance.md)&#x20;

For geometry type, returns the 2-dimensional cartesian minimum distance (based on spatial ref) between two geometries in projected units. For geography, returns the great-circle distance in meters between two SphericalGeography points. Note that g1, g2 shall have the same type.

#### [**ST\_GeometryType(Geometry g) → String**](../functions-1/stgeometrytype.md)&#x20;

Returns the type of the geometry as a string. e.g.: `ST_Linestring`, `ST_Polygon`,`ST_MultiPolygon` etc.

### Outputs

#### [**ST\_AsBinary(Geometry/Geography g) → bytes**](../functions-1/stasbinary.md)&#x20;

Returns the WKB representation of the geometry.

#### [**ST\_AsText(Geometry/Geography g) → string**](../functions-1/stastext.md)&#x20;

Returns the WKT representation of the geometry/geography.

### Conversion

#### [**toSphericalGeography(Geometry g) → Geography**](../functions-1/tosphericalgeography.md)&#x20;

Converts a Geometry object to a spherical geography object.

#### [**toGeometry(Geography g) → Geometry**](../functions-1/togeometry.md)&#x20;

Converts a spherical geographical object to a Geometry object.

### Relationship

#### [**ST\_Contains(Geometry/Geography, Geometry/Geography) → boolean**](../functions-1/stcontains.md)&#x20;

Returns true if and only if no points of the second geometry/geography lie in the exterior of the first geometry/geography, and at least one point of the interior of the first geometry lies in the interior of the second geometry. **Warning: ST\_Contains on Geography only give close approximation**

#### **ST\_Equals(Geometry, Geometry) → boolean**&#x20;

Returns true if the given geometries represent the same geometry/geography.

#### **ST\_Within(Geometry, Geometry) → boolean**&#x20;

Returns true if first geometry is completely inside second geometry.
