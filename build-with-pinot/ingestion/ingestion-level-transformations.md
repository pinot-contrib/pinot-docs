# Ingestion Transformations

Raw source data often needs to undergo some transformations before it is pushed to Pinot.

Transformations include extracting records from nested objects, applying simple transform functions on certain columns, filtering out unwanted columns, as well as more advanced operations like joining between datasets.

A preprocessing job is usually needed to perform these operations. In streaming data sources, you might write a Samza job and create an intermediate topic to store the transformed data.

For simple transformations, this can result in inconsistencies in the batch/stream data source and increase maintenance and operator overhead.

To make things easier, Pinot supports transformations that can be applied via the [table config](../../reference/configuration-reference/table.md).

{% hint style="warning" %}
If you **add or change a transformed column** while realtime consumers are running, the current consuming segment can keep using the old transform plan until it commits. Use the [add a new column during ingestion](ingestion-level-transformations.md#add-a-new-column-during-ingestion) steps (or the [schema evolution decision table](../data-modeling/schema-evolution.md#decision-table-add-a-column-on-an-existing-table)) — pause is recommended for transform changes, but plain default-only columns often only need reload / forceCommit.
{% endhint %}

## Transformation functions

Pinot supports the following functions:

* Groovy functions
* Built-in functions

{% hint style="warning" %}
A transformation function cannot mix Groovy and built-in functions; only use one type of function at a time.
{% endhint %}

### Groovy functions

Groovy functions can be defined using the syntax:

```javascript
Groovy({groovy script}, argument1, argument2...argumentN)
```

Any valid Groovy expression can be used.

:warning: **Enabling Groovy**

Allowing executable Groovy in ingestion transformation can be a security vulnerability. To enable Groovy for ingestion, set the following controller configuration:

`controller.disable.ingestion.groovy=false`

If not set, Groovy for ingestion transformation is disabled by default.

#### Groovy static analysis

Pinot can also apply static analysis to Groovy scripts before compiling them. This is configured with cluster-level Groovy analyzer configs:

- `pinot.groovy.all.static.analyzer`: default analyzer for both query-time and ingestion-time Groovy
- `pinot.groovy.ingestion.static.analyzer`: ingestion-specific override used when Pinot validates Groovy in table configs
- `pinot.groovy.query.static.analyzer`: query-specific override used when Pinot validates Groovy in broker queries

If the ingestion-specific or query-specific config is not set, Pinot falls back to `pinot.groovy.all.static.analyzer`. If none of these cluster configs are set, Groovy static analysis is disabled.

Each static analyzer config is a JSON object with these fields:

- `allowedReceivers`: fully qualified receiver classes Groovy method calls can target
- `allowedImports`: fully qualified imports allowed in the script
- `allowedStaticImports`: fully qualified static imports allowed in the script
- `disallowedMethodNames`: method names Pinot rejects even if the receiver is otherwise allowed
- `methodDefinitionAllowed`: whether Groovy method definitions are allowed inside the script

Static analysis does not enable Groovy by itself. You still need `controller.disable.ingestion.groovy=false` to use Groovy in ingestion transforms.

Use the controller API to inspect and update these configs:

- `GET /cluster/configs/groovy/staticAnalyzerConfig/default` returns Pinot's built-in sample config
- `GET /cluster/configs/groovy/staticAnalyzerConfig` returns the cluster's current Groovy static analyzer config overrides
- `POST /cluster/configs/groovy/staticAnalyzerConfig` updates one or more of the Groovy analyzer configs

The full request and response examples for these endpoints are in the [controller API reference](../../reference/api-reference/controller-api.md#groovy-static-analysis-configs).

### Built-in Pinot functions

Pinot supports registered scalar functions for ingestion transformations. Functions are annotated with `@ScalarFunction`; for example, [toEpochSeconds](https://github.com/apache/pinot/blob/02cb2d4970c71a2ea5b4c140a860fbf220e11bd3/pinot-common/src/main/java/org/apache/pinot/common/function/scalar/DateTimeFunctions.java#L78).

#### Immutable function requirement

New or changed persisted ingestion transforms can use only scalar functions whose result depends solely on their explicit arguments (`IMMUTABLE` functions). Pinot applies this rule to:

- `ingestionConfig.transformConfigs` in table configs
- schema-level `transformFunction` definitions
- `upsertConfig.postPartialUpsertTransformConfigs` for partial-upsert tables

The check includes nested scalar function calls. For example, `now()`, `ago()`, `agoMV()`, and unseeded `rand()` are not valid in a new or changed persisted transform because they can produce different values for the same input. `rand(seed)` is valid because its result is derived from its explicit seed.

Pinot keeps exact existing transform definitions running for compatibility. If you add or modify a persisted transform, replace any non-immutable function with an input-derived alternative before submitting the schema or table config. This validation does not change the functions' query-time behavior. Groovy expressions continue through Pinot's existing Groovy validation rather than scalar-function volatility metadata.

Below are some commonly used built-in Pinot functions for ingestion transformations.

#### DateTime functions

These functions enable time transformations.

**toEpochXXX**

Converts from epoch milliseconds to a higher granularity.

| Function name  | Description                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------ |
| toEpochSeconds | Converts epoch millis to epoch seconds. Usage:`"toEpochSeconds(millis)"` |
| toEpochMinutes | Converts epoch millis to epoch minutes Usage: `"toEpochMinutes(millis)"` |
| toEpochHours | Converts epoch millis to epoch hours Usage: `"toEpochHours(millis)"` |
| toEpochDays | Converts epoch millis to epoch days Usage: `"toEpochDays(millis)"` |

**toEpochXXXRounded**

Converts from epoch milliseconds to another granularity, rounding to the nearest rounding bucket. For example, `1588469352000` (2020-05-01 42:29:12) is `26474489` minutesSinceEpoch. `` `toEpochMinutesRounded(1588469352000) = 26474480 `` (2020-05-01 42:20:00)

| Function Name         | Description                                                                                                      |
| --------------------- | ---------------------------------------------------------------------------------------------------------------- |
| toEpochSecondsRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochSecondsRounded(millis, 30)"` |
| toEpochMinutesRounded | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochMinutesRounded(millis, 10)"` |
| toEpochHoursRounded   | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochHoursRounded(millis, 6)"`    |
| toEpochDaysRounded    | Converts epoch millis to epoch seconds, rounding to nearest rounding bucket`"toEpochDaysRounded(millis, 7)"`     |

**fromEpochXXX**

Converts from an epoch granularity to milliseconds.

| Function Name    | Description                                                                                                 |
| ---------------- | ----------------------------------------------------------------------------------------------------------- |
| fromEpochSeconds | Converts from epoch seconds to milliseconds `"fromEpochSeconds(secondsSinceEpoch)"` |
| fromEpochMinutes | Converts from epoch minutes to milliseconds `"fromEpochMinutes(minutesSinceEpoch)"` |
| fromEpochHours | Converts from epoch hours to milliseconds `"fromEpochHours(hoursSinceEpoch)"` |
| fromEpochDays | Converts from epoch days to milliseconds `"fromEpochDays(daysSinceEpoch)"` |

**Simple date format**

Converts simple date format strings to milliseconds and vice versa, per the provided pattern string.

| Function name                                     | Description                                                                                                                                                              |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [ToDateTime](../../functions/datetime/todatetime.md) | Converts from milliseconds to a formatted date time string, as per the provided pattern `"toDateTime(millis, 'yyyy-MM-dd')"` |
| [FromDateTime](../../functions/datetime/fromdatetime.md) | Converts a formatted date time string to milliseconds, as per the provided pattern `"fromDateTime(dateTimeStr, 'EEE MMM dd HH:mm:ss ZZZ yyyy')"` |

{% hint style="info" %}
**Note**

Letters that are not part of Simple Date Time legend ([https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)) need to be escaped. For example:

`"transformFunction": "fromDateTime(dateTimeStr, 'yyyy-MM-dd''T''HH:mm:ss')"`
{% endhint %}

#### JSON functions

| Function name | Description                                                                                                                                                                                                                                                                                                       |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| json\_format | Converts a JSON/AVRO complex object to a string. This json map can then be queried using [jsonExtractScalar](../../functions/transformations.md) function. `"json_format(jsonMapField)"` |

#### Geospatial functions

Geospatial scalar functions are available as ingestion transforms. Use them to materialize points, parse WKT/WKB/GeoJSON, convert geometry/geography, or compute H3 grid ids at ingest time. Geometry and geography values are stored as `BYTES` in the schema.

| Function name | Returns | Description |
| ------------- | ------- | ----------- |
| [ST_Point](../../functions/geospatial/stpoint.md) / `stPoint` | `BYTES` (Point) | Builds a point from `x`/`y` coordinates; optional third arg marks geography. |
| [ST_Polygon](../../functions/geospatial/stpolygon.md) | `BYTES` (Polygon) | Parses polygon WKT into a planar polygon geometry. |
| [ST_GeomFromText](../../functions/geospatial/stgeomfromtext.md) / `stGeomFromText` | `BYTES` (Geometry) | Parses a WKT string into a geometry. |
| [ST_GeogFromText](../../functions/geospatial/stgeogfromtext.md) / `stGeogFromText` | `BYTES` (Geography) | Parses a WKT string into a geography. |
| [ST_GeomFromWKB](../../functions/geospatial/stgeomfromwkb.md) / `stGeomFromWKB` | `BYTES` (Geometry) | Parses WKB bytes into a geometry. |
| [ST_GeogFromWKB](../../functions/geospatial/stgeogfromwkb.md) / `stGeogFromWKB` | `BYTES` (Geography) | Parses WKB bytes into a geography. |
| [ST_GeomFromGeoJSON](../../functions/geospatial/st_geomfromgeojson.md) / `stGeomFromGeoJson` | `BYTES` (Geometry) | Parses a GeoJSON string into a geometry. |
| [ST_GeogFromGeoJSON](../../functions/geospatial/st_geogfromgeojson.md) / `stGeogFromGeoJson` | `BYTES` (Geography) | Parses a GeoJSON string into a geography. |
| [ST_AsText](../../functions/geospatial/stastext.md) / `stAsText` | `STRING` | Serializes geometry/geography to WKT. |
| [ST_AsBinary](../../functions/geospatial/stasbinary.md) / `stAsBinary` | `BYTES` | Serializes geometry/geography to WKB. |
| [ST_AsGeoJSON](../../functions/geospatial/st_asgeojson.md) / `stAsGeoJson` | `STRING` | Serializes geometry/geography to GeoJSON. |
| [ST_GeometryType](../../functions/geospatial/stgeometrytype.md) / `stGeometryType` | `STRING` | Returns the geometry type name (for example, `Point`, `Polygon`). |
| `ST_Area` / `stArea` | `DOUBLE` | Computes planar area for geometry or spherical area in square meters for geography. |
| [ST_Distance](../../functions/geospatial/stdistance.md) / `stDistance` | `DOUBLE` | Distance between two geometries (cartesian) or geographies (meters). |
| [ST_Contains](../../functions/geospatial/stcontains.md) / `stContains` | `INT` (0/1) | Whether the first geometry/geography contains the second. |
| `ST_Equals` / `stEquals` | `INT` (0/1) | Whether two geometries are equal. |
| `ST_Within` / `stWithin` | `INT` (0/1) | Whether the first geometry is completely inside the second. |
| [toSphericalGeography](../../functions/geospatial/tosphericalgeography.md) | `BYTES` (Geography) | Converts a geometry object to spherical geography. |
| [toGeometry](../../functions/geospatial/togeometry.md) | `BYTES` (Geometry) | Converts a spherical geography object to geometry. |
| `geoToH3` | `LONG` | H3 cell id from `(longitude, latitude, resolution)` or from a point `BYTES` plus resolution. |
| [gridDistance](../../functions/geospatial/griddistance.md) | `LONG` | H3 grid distance between two H3 indexes. |
| [gridDisk](../../functions/geospatial/griddisk.md) | `LONG[]` | H3 indexes within `k` grid steps of an origin index. |

{% hint style="info" %}
Function names are case-insensitive in transforms. The full geospatial function reference (including query-time usage and aggregates such as [ST_Union](../../functions/geospatial/stunion.md)) is in [Geospatial functions](../../functions/geospatial/README.md).
{% endhint %}

**Example: materialize a point and an H3 grid id from longitude/latitude columns**

```javascript
"ingestionConfig": {
  "transformConfigs": [
    {
      "columnName": "location",
      "transformFunction": "ST_Point(lon, lat, 1)"
    },
    {
      "columnName": "h3Index",
      "transformFunction": "geoToH3(lon, lat, 7)"
    }
  ]
}
```

Add `location` as a `BYTES` dimension and `h3Index` as a `LONG` dimension in the schema. The third argument to `ST_Point` marks the value as geography (`1`/`true`) rather than planar geometry.

**Example: parse WKT and derive H3 from an existing point column**

```javascript
"ingestionConfig": {
  "transformConfigs": [
    {
      "columnName": "geom",
      "transformFunction": "ST_GeomFromText(wkt)"
    },
    {
      "columnName": "h3FromPoint",
      "transformFunction": "geoToH3(location, 9)"
    }
  ]
}
```

## Types of transformation

### Filtering

Records can be filtered as they are ingested. A filter function can be specified in the filterConfigs in the ingestionConfigs of the table config.

```javascript
"tableConfig": {
    "tableName": ...,
    "tableType": ...,
    "ingestionConfig": {
        "filterConfig": {
            "filterFunction": "<expression>"
        }
    }
}
```

If the expression evaluates to true, the record will be filtered out. The expressions can use any of the transform functions described in the previous section.

Consider a table that has a column `timestamp`. If you want to filter out records that are older than timestamp 1589007600000, you could apply the following function:

```javascript
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": "Groovy({timestamp < 1589007600000}, timestamp)"
    }
}
```

Consider a table that has a string column `campaign` and a multi-value column double column `prices`. If you want to filter out records where campaign = 'X' or 'Y' and sum of all elements in prices is less than 100, you could apply the following function:

```javascript
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": "Groovy({(campaign == \"X\" || campaign == \"Y\") && prices.sum() < 100}, prices, campaign)"
    }
}
```

Filter config also supports SQL-like expression of built-in [scalar functions](../../functions/udf#scalar-functions) for filtering records (starting v 0.11.0+). Example:

```javascript
"ingestionConfig": {
    "filterConfig": {
        "filterFunction": "strcmp(campaign, 'X') = 0 OR strcmp(campaign, 'Y') = 0 OR timestamp < 1589007600000"
    }
}
```

### Column transformation

Transform functions can be defined on columns in the ingestion config of the table config.

{% hint style="info" %}
Pinot evaluates ingestion transforms against normalized extractor values, not the raw source-format encoding. For typed input formats such as Avro, Parquet, ORC, Thrift, and Protocol Buffers, booleans stay `Boolean`, `Byte` and `Short` values widen to `Integer`, logical dates and times surface as `java.time.LocalDate`, `java.time.LocalTime`, or `java.sql.Timestamp`, multi-value fields surface as `Object[]`, and maps or nested records surface as `Map<Object, Object>`. Pinot coerces those intermediate values to the column's declared schema type after the transform step.

If you have an older transform that depended on format-specific quirks such as stringified booleans or raw epoch date and time values, update the transform to handle the normalized value or cast it explicitly.

For `JSONPATHSTRING`, `JSONPATHSTRINGFAST`, and `JSONPATHSTRINGFIRSTMATCH`, this means typed leaves on those already-materialized trees now render `UUID`, `LocalDate`, and `LocalTime` values as unquoted canonical or ISO-8601 strings instead of JSON-quoted strings. The change is specific to ingestion-time typed objects and does not change behavior for normal JSON-string input.
{% endhint %}

```javascript
{ "tableConfig": {
    "tableName": ...,
    "tableType": ...,
    "ingestionConfig": {
        "transformConfigs": [{
          "columnName": "fieldName",
          "transformFunction": "<expression>"
        }]
    },
    ...
}
```

For example, imagine that our source data contains the `prices` and `timestamp` fields. We want to extract the maximum price and store that in the `maxPrices` field and convert the timestamp into the number of hours since the epoch and store it in the `hoursSinceEpoch` field. You can do this by applying the following transformation:

{% code title="pinot-table-offline.json" %}
```javascript
{
"tableName": "myTable",
...
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "maxPrice",
      "transformFunction": "Groovy({prices.max()}, prices)" // groovy function
    },
    {
      "columnName": "hoursSinceEpoch",
      "transformFunction": "toEpochHours(timestamp)" // built-in function
    }]
  }
}
```
{% endcode %}

Below are some examples of commonly used functions.

#### String concatenation

Concat `firstName` and `lastName` to get `fullName`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "fullName",
      "transformFunction": "Groovy({firstName+' '+lastName}, firstName, lastName)"
    }]
}
```

#### Find an element in an array

Find max value in array `bids`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "maxBid",
      "transformFunction": "Groovy({bids.max{ it.toBigDecimal() }}, bids)"
    }]
}
```

#### Time transformation

Convert `timestamp` from `MILLISECONDS` to `HOURS`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "hoursSinceEpoch",
      "transformFunction": "Groovy({timestamp/(1000*60*60)}, timestamp)"
    }]
}
```

#### Column name change

Change name of the column from `user_id` to `userId`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "userId",
      "transformFunction": "user_id"
    }]
}
```

#### Rename fields from a Kafka JSON message

Kafka JSON payloads often use keys that aren’t great Pinot column names. Common examples are keys containing `-`, such as `event-id`.

Map the source key to a schema-friendly column using `transformConfigs`. Reference the source key with a quoted identifier.

```javascript
"ingestionConfig": {
  "transformConfigs": [
    {
      "columnName": "event_id",
      "transformFunction": "\"event-id\""
    },
    {
      "columnName": "event_timestamp",
      "transformFunction": "\"event-timestamp\""
    },
    {
      "columnName": "user_id",
      "transformFunction": "\"user-id\""
    }
  ]
}
```

{% hint style="info" %}
Add the destination columns (for example, `event_id`) to your Pinot schema.
{% endhint %}

#### Extract value from a column containing space

Pinot doesn't support columns that have spaces, so if a source data column has a space, we'll need to store that value in a column with a supported name. To extract the value from `first Name` into the column `firstName`, run the following:

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "firstName",
      "transformFunction": "\"first Name \""
    }]
}
```

#### Ternary operation

If `eventType` is `IMPRESSION` set `impression` to `1`. Similar for `CLICK`.

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "impressions",
      "transformFunction": "Groovy({eventType == 'IMPRESSION' ? 1: 0}, eventType)"
    },
    {
      "columnName": "clicks",
      "transformFunction": "Groovy({eventType == 'CLICK' ? 1: 0}, eventType)"
    }]
}
```

#### AVRO Map

Store an AVRO Map in Pinot as two multi-value columns. Sort the keys, to maintain the mapping.\
1\) The keys of the map as `map_keys`\
2\) The values of the map as `map_values`

```javascript
"ingestionConfig": {
    "transformConfigs": [{
      "columnName": "map2_keys",
      "transformFunction": "Groovy({map2.sort()*.key}, map2)"
    },
    {
      "columnName": "map2_values",
      "transformFunction": "Groovy({map2.sort()*.value}, map2)"
    }]
}
```

#### Chaining transformations

Transformations can be chained. This means that you can use a field created by a transformation in another transformation function.

For example, we might have the following JSON document in the `data` field of our source data:

```json
{
  "userId": "12345678__foo__othertext"
}
```

We can apply one transformation to extract the `userId` and then another one to pull out the numerical part of the identifier:

```javascript
"ingestionConfig": {
    "transformConfigs": [
      {
        "columnName": "userOid",
        "transformFunction": "jsonPathString(data, '$.userId')"
      },
      {
        "columnName": "userId",
        "transformFunction": "Groovy({Long.valueOf(userOid.substring(0, 8))}, userOid)"
      }
   ]
}
```

Pinot validates these chains by dependency, not by list order. A transform can consume a column produced by another transform even if the consumer appears earlier in `transformConfigs`, as long as the dependency graph is valid.

{% hint style="info" %}
Intermediate transform outputs do not need schema columns when they are only consumed by later transforms. Final outputs that Pinot stores or aggregates still need schema columns.

For example, the following pattern is valid even when `message_obj` is not in the schema:

```json
"ingestionConfig": {
  "transformConfigs": [
    {
      "columnName": "message_obj",
      "transformFunction": "JSONEXTRACTOBJECT(message)"
    },
    {
      "columnName": "level",
      "transformFunction": "JSONPATHSTRING(message_obj, '$.level', null)"
    },
    {
      "columnName": "msg_time",
      "transformFunction": "JSONPATHSTRING(message_obj, '$.time', null)"
    }
  ]
}
```

In this example, `message_obj` is an intermediate column, so Pinot materializes it during transformation and drops it before indexing. The leaf columns such as `level` and `msg_time` are the stored outputs, so those columns still belong in the schema.
{% endhint %}

### Flattening

There are 2 kinds of flattening:

#### One record into many

This is not natively supported as of yet. You can **write a custom Decoder/RecordReader if you want to use this**. Once the Decoder generates the multiple GenericRows from the provided input record, a List\<GenericRow> should be set into the destination GenericRow, with the key `$MULTIPLE_RECORDS_KEY$`. The segment generation drivers will treat this as a special case and handle the multiple records case.

#### Extract attributes from complex objects

The multi-stage query engine (MSE) supports flattening array columns at query time using `CROSS JOIN UNNEST(...)`. This is the recommended approach for expanding array fields without pre-flattening data at ingestion.

```sql
SET useMultistageEngine=true;

SELECT t.id, elem
FROM myTable AS t
CROSS JOIN UNNEST(t.arrayColumn) AS u(elem)
```

For full syntax including `WITH ORDINALITY`, filtering, and aggregation after unnesting, see the [Unnest operator](../querying-and-sql/multi-stage-query/operator-types/unnest.md) page.

## Add a new column during ingestion

This section applies when the new or changed column is populated through **ingestion transforms** (or you change transform logic) on a **realtime** table. The active consuming segment builds its transform pipeline when the mutable segment starts. Mid-segment schema/config updates do not rewrite rows already indexed in that consumer, so values in the current consuming segment can be wrong or missing until you start a new consumer.

You do **not** always need a full pause for every schema add. Use the [schema evolution decision table](../data-modeling/schema-evolution.md#decision-table-add-a-column-on-an-existing-table):

| Change | Typical action |
| --- | --- |
| Plain column / `defaultNullValue` only | Update schema, then reload (consuming reload requests a force commit when allowed) or use [forceCommit](../../reference/api-reference/controller-api.md#post-tablestablenameforcecommit) and poll it |
| New or changed **transform** | Prefer pause → apply schema + table config → reload completed segments → resume; or apply schema/config → forceCommit and poll → reload the segments committed under the old plan |
| Partial-upsert strategy for the new column | Update schema and strategy config together, then use a controlled server restart; immutable core upsert settings require a new table and reingestion. See [schema evolution](../data-modeling/schema-evolution.md). |

### Transform-safe procedure (pause boundary)

To ensure accurate transformed values with a clean consumer boundary:

1. Pause consumption (and wait for pause status success):

   ```bash
   curl -X POST {controllerHost}/tables/{tableName}/pauseConsumption
   curl -X GET  {controllerHost}/tables/{tableName}/pauseStatus
   ```

2. Apply new table or schema configurations.

3. [Reload segments](../../operate-pinot/segment-reload.md) using the [Pinot Controller API](../../operate-pinot/segment-reload.md#use-the-pinot-controller-api-to-reload-segments) or [Pinot Admin Console](../../operate-pinot/segment-reload.md#use-the-pinot-admin-console-to-reload-segments).

4. Resume consumption:

   ```bash
   curl -X POST {controllerHost}/tables/{tableName}/resumeConsumption
   ```

### Alternative: force commit without a long pause

After applying the new schema and table config, if you can tolerate committing current consumers immediately:

```bash
curl -X POST {controllerHost}/tables/{tableName}/forceCommit
curl -X GET  {controllerHost}/tables/forceCommitStatus/{jobId}
```

Wait until `numberOfSegmentsYetToBeCommitted` is `0`, then reload the segments committed under the old transform plan so Pinot recomputes the new column. Details: [Force commit API](../../reference/api-reference/controller-api.md#post-tablestablenameforcecommit).
