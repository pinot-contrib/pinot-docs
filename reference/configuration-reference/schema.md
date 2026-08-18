---
description: Schema configuration reference.
---

# Schema Configuration

This page is the flat reference for Pinot schema JSON. It brings the top-level schema object, field-spec tables, null-handling rules, date-time formats, `MAP` and `OPEN_STRUCT` support, and advanced column options into one place.

## Key Areas

| Area | What it covers | Jump |
| --- | --- | --- |
| Schema object | Top-level schema fields and a complete example | [Schema object](#schema-object) |
| Field specs | Dimension, metric, and date-time column definitions | [Field specs](#field-specs) |
| Null handling | `enableColumnBasedNullHandling` and default null values | [Null handling](#null-handling) |
| Complex fields | `MAP` and `OPEN_STRUCT` columns plus `childFieldSpecs` | [ComplexFieldSpecs](#complexfieldspecs) |
| Date-time formats | New and legacy format syntaxes | [New DateTime Formats](#new-datetime-formats) |

## Schema Object

Use a schema to define the column names, data types, null-handling behavior, and field groups for a Pinot table.

| Field | Release Version | Default | Description |
| --- | --- | --- | --- |
| `schemaName` | - | required | Name of the schema. This must match the table name without the `OFFLINE` or `REALTIME` suffix, so both physical tables of a hybrid table share one schema. |
| `description` | - | omitted | Optional human-readable description of the schema. |
| `tags` | - | omitted | Optional list of tags for categorizing the schema. |
| `enableColumnBasedNullHandling` | 1.1.0 | `false` | When `true`, enables column-based null handling. When `false`, Pinot uses table-based null handling. See [Null value support](../../build-with-pinot/querying-and-sql/null-value-support.md). |
| `dimensionFieldSpecs` | - | `[]` | Dimension-column definitions. See [DimensionFieldSpecs](#dimensionfieldspecs). |
| `metricFieldSpecs` | - | `[]` | Metric-column definitions. See [MetricFieldSpecs](#metricfieldspecs). |
| `dateTimeFieldSpecs` | - | `[]` | Time-column definitions. A schema can define multiple time columns. New schema submissions must use `dateTimeFieldSpecs`; controller REST validation rejects the deprecated `TimeFieldSpec` (`fieldType=TIME`). See [DateTimeFieldSpecs](#datetimefieldspecs). |
| `complexFieldSpecs` | - | `[]` | Complex-column definitions. Pinot currently supports `MAP` and `OPEN_STRUCT` through this section. See [ComplexFieldSpecs](#complexfieldspecs). |

## Example Schema

```json
{
  "schemaName": "flights",
  "description": "Tracks flight events and attributes.",
  "tags": ["production", "real-time"],
  "enableColumnBasedNullHandling": false,
  "dimensionFieldSpecs": [
    {
      "name": "flightNumber",
      "dataType": "LONG",
      "description": "Unique flight identifier."
    },
    {
      "name": "airline",
      "dataType": "STRING"
    },
    {
      "name": "tags",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": "null"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "price",
      "dataType": "DOUBLE",
      "defaultNullValue": 0
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "millisSinceEpoch",
      "dataType": "LONG",
      "format": "EPOCH",
      "granularity": "15:MINUTES"
    },
    {
      "name": "hoursSinceEpoch",
      "dataType": "INT",
      "format": "EPOCH|HOURS",
      "granularity": "1:HOURS"
    },
    {
      "name": "dateString",
      "dataType": "STRING",
      "format": "SIMPLE_DATE_FORMAT|yyyy-MM-dd",
      "granularity": "1:DAYS"
    }
  ],
  "complexFieldSpecs": [
    {
      "name": "attributes",
      "dataType": "MAP",
      "fieldType": "COMPLEX",
      "notNull": false,
      "childFieldSpecs": {
        "key": {
          "name": "key",
          "dataType": "STRING",
          "fieldType": "DIMENSION",
          "notNull": false
        },
        "value": {
          "name": "value",
          "dataType": "STRING",
          "fieldType": "DIMENSION",
          "notNull": false
        }
      }
    }
  ]
}
```

## Data Types

Pinot supports the following schema data types:

| Data Type | Default Dimension Value | Default Metric Value |
| --- | --- | --- |
| `INT` | [Integer.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE) | `0` |
| `LONG` | [Long.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE) | `0` |
| `FLOAT` | [Float.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY) | `0.0` |
| `DOUBLE` | [Double.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY) | `0.0` |
| `BIG_DECIMAL` | `0.0` | `0.0` |
| `BOOLEAN` | `0` (`false`) | N/A |
| `TIMESTAMP` | `0` (`1970-01-01 00:00:00 UTC`) | N/A |
| `STRING` | `"null"` | N/A |
| `JSON` | `"null"` | N/A |
| `BYTES` | byte array of length `0` | byte array of length `0` |
| `UUID` | nil UUID (`00000000-0000-0000-0000-000000000000`) | N/A |

The `TIMESTAMP` type supports milliseconds epoch precision. Nanoseconds are not supported.

### UUID columns

Use the `UUID` logical type for RFC 4122 identifiers. Pinot stores each UUID as a fixed-width 16-byte value. Use canonical lowercase UUID strings at ingestion and in external interfaces.

```json
{
  "name": "eventId",
  "dataType": "UUID",
  "fieldType": "DIMENSION"
}
```

For ingestion, use canonical UUID strings. Pinot also accepts `java.util.UUID` values and 16-byte values from record readers. Avro UUID logical types are mapped to `UUID`; see [Avro](../../build-with-pinot/ingestion/pinot-input-formats.md#avro).

For an upsert or dedup table with a UUID primary key, producers must send canonical lowercase RFC 4122 strings. This keeps equivalent UUID values on the same Kafka partition so Pinot can apply deduplication correctly.

Query results render `UUID` values, including multi-value UUID columns, as canonical lowercase RFC 4122 strings. This applies to JSON and Arrow responses from `SELECT`, `GROUP BY`, `DISTINCT`, and join queries.

Both the single-stage and multi-stage query engines support UUID literals and predicates. The multi-stage planner carries UUID literals through the existing 16-byte binary request encoding, while group-by, join, and dynamic-filter execution uses the UUID column's stored `BYTES` representation.

UUID columns can be used as `GROUP BY` keys and in `HAVING` predicates. For multi-value UUID group keys, keep the dictionary enabled. The single-stage query engine also supports UUID inputs for `DISTINCTCOUNT`, `DISTINCTCOUNTHLL`, `DISTINCTCOUNTHLLPLUS`, `DISTINCTCOUNTBITMAP`, `DISTINCTCOUNTTHETASKETCH`, and `DISTINCTCOUNTCPCSKETCH` on single-value and multi-value columns. `DISTINCTCOUNTULL` supports single-value UUID columns only.

Distinct-count sketches hash the stored 16-byte UUID value. Therefore, an approximate count or raw sketch over a UUID column is not expected to match the result of applying the same function to `CAST(uuidColumn AS STRING)`.

```sql
SELECT eventId, COUNT(*)
FROM events
GROUP BY eventId
HAVING eventId = '550e8400-e29b-41d4-a716-446655440000';

SELECT DISTINCTCOUNTHLL(eventId)
FROM events;
```

{% hint style="warning" %}
Treat UUID query results as an atomic-upgrade feature. An older broker or server cannot decode the UUID result-type token emitted by a newer node. Upgrade all brokers and servers before querying UUID columns, and do not roll back while UUID query results are in flight.
{% endhint %}

All schema data types are comparable, and ordering must be consistent with equality. Pinot normalizes a few edge cases to preserve that property:

- For `FLOAT` and `DOUBLE`, negative zero (`-0.0`) becomes `0.0`.
- For `FLOAT` and `DOUBLE`, `NaN` becomes the default null value.
- For `BIG_DECIMAL`, trailing zeros are stripped unless `allowTrailingZeros` is enabled.

## Field Specs

Pinot groups columns into dimension, metric, date-time, and complex field specs. The field spec controls column behavior during ingestion, storage, and query execution.

All field-spec families also accept optional `fieldId`, `aliases`, and `metadata` values. Pinot preserves non-empty values in schema JSON, omits empty alias lists and metadata maps, and does not currently use these fields for backward-compatible schema validation or automatic rename and rewrite handling.

## Null Handling

At schema level, null handling is controlled by `enableColumnBasedNullHandling` and by per-column `defaultNullValue` settings.

- Set `enableColumnBasedNullHandling` to `true` when you want Pinot to store null-ness per column.
- Leave it `false` to keep table-based null handling behavior.
- If a field does not define `defaultNullValue`, Pinot falls back to the internal default for that field type.

### Dimension Default Null Values

| Data Type | Internal Default Null Value |
| --- | --- |
| `INT` | [Integer.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE) |
| `LONG` | [Long.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE) |
| `FLOAT` | [Float.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY) |
| `DOUBLE` | [Double.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY) |
| `BOOLEAN` | `0` (`false`) |
| `TIMESTAMP` | `0` (`1970-01-01 00:00:00 UTC`) |
| `STRING` | `"null"` |
| `BYTES` | byte array of length `0` |
| `JSON` | `"null"` |
| `UUID` | nil UUID (`00000000-0000-0000-0000-000000000000`) |

### Metric Default Null Values

| Data Type | Internal Default Null Value |
| --- | --- |
| `INT` | `0` |
| `LONG` | `0` |
| `FLOAT` | `0.0` |
| `DOUBLE` | `0.0` |
| `BIG_DECIMAL` | `0.0` |
| `BYTES` | byte array of length `0` |

## DimensionFieldSpecs

Define one dimension field spec for each dimension column.

| Property | Description |
| --- | --- |
| `name` | Name of the dimension column. |
| `description` | Optional human-readable description of the column. |
| `tags` | Optional list of tags for categorizing the column. |
| `fieldId` | Optional stable, name-independent identifier for the column. |
| `aliases` | Optional list of alternate or historical names for the column. |
| `metadata` | Optional free-form string map for column metadata. Pinot preserves non-empty values in schema JSON, omits empty maps, and does not assign built-in semantics or use them for backward-compatibility checks. |
| `dataType` | Data type of the dimension column. Supported types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `BOOLEAN`, `TIMESTAMP`, `STRING`, `BYTES`, `UUID`, and `JSON`. |
| `defaultNullValue` | Value Pinot should write when the source record is null. If omitted, Pinot uses the internal default for the type. For `UUID`, the default is the nil UUID. |
| `singleValueField` | Whether the column is single-valued. If `false`, Pinot stores a multi-value list, preserves order, and allows duplicates. This includes `BIG_DECIMAL`, `BYTES`, and `UUID` dimension columns. The default null value for a multi-value column is a single-element list containing the configured or internal null value. |

## MetricFieldSpecs

Define one metric field spec for each metric column.

| Property | Description |
| --- | --- |
| `name` | Name of the metric column. |
| `description` | Optional human-readable description of the column. |
| `tags` | Optional list of tags for categorizing the column. |
| `fieldId` | Optional stable, name-independent identifier for the column. |
| `aliases` | Optional list of alternate or historical names for the column. |
| `metadata` | Optional free-form string map for column metadata. Pinot preserves non-empty values in schema JSON, omits empty maps, and does not assign built-in semantics or use them for backward-compatibility checks. |
| `dataType` | Data type of the metric column. Supported types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, and `BYTES` for serialized sketches such as HLL or TDigest. |
| `defaultNullValue` | Value Pinot should write when the source record is null. If omitted, Pinot uses the internal default for the type. |

## DateTimeFieldSpecs

Use date-time field specs to define time columns.

Pinot accepts legacy `TimeFieldSpec` objects when loading older schemas that are already stored in the cluster, but controller REST schema submission paths (`POST /schemas`, `PUT /schemas/{schemaName}`, and `/schemas/validate`) now reject new payloads that use `fieldType=TIME`. Use `DateTimeFieldSpec` for all new schema work.

| Property | Description |
| --- | --- |
| `name` | Name of the date-time column. |
| `description` | Optional human-readable description of the column. |
| `tags` | Optional list of tags for categorizing the column. |
| `fieldId` | Optional stable, name-independent identifier for the column. |
| `aliases` | Optional list of alternate or historical names for the column. |
| `metadata` | Optional free-form string map for column metadata. Pinot preserves non-empty values in schema JSON, omits empty maps, and does not assign built-in semantics or use them for backward-compatibility checks. |
| `dataType` | Data type of the date-time column. Supported types are `STRING`, `INT`, `LONG`, and `TIMESTAMP`. Internally `TIMESTAMP` is stored as `LONG` milliseconds since epoch. If you use `TIMESTAMP`, source data must be either `LONG` epoch values or JDBC timestamp strings such as `2021-01-01 01:01:01.123`. |
| `format` | Format in which the time value is stored. See [New DateTime Formats](#new-datetime-formats). |
| `granularity` | Bucket size and unit in `bucketSize:bucketUnit` form, for example `15:MINUTES`. This is descriptive metadata only; Pinot does not automatically round values to the declared granularity. |
| `defaultNullValue` | Value Pinot should write when the source record is null. String-based date-time fields default to `"null"`. `TIMESTAMP` defaults to epoch `0` (`1970-01-01 00:00:00 UTC`). For the primary time column named in table `segmentsConfig`, the default value must fall between `1971-01-01 UTC` and `2071-01-01 UTC`; otherwise Pinot uses segment creation time for segment-management features such as retention and time boundary. |

## New DateTime Formats

The current simplified syntax is:

```text
timeFormat|pattern/timeUnit|[timeZone/timeSize]
```

The bracketed fields are optional. `timeFormat` can be `EPOCH`, `SIMPLE_DATE_FORMAT`, or `TIMESTAMP`.

- `TIMESTAMP`
  Represents a timestamp in milliseconds. It is equivalent to `EPOCH|MILLISECONDS|1`.
  Example: `TIMESTAMP`
- `EPOCH`
  Represents time in a `TimeUnit` since `1970-01-01 00:00:00 UTC`.
  Examples: `EPOCH`, `EPOCH|SECONDS`, `EPOCH|SECONDS|5`
- `SIMPLE_DATE_FORMAT`
  Represents a string-formatted time using Joda `DateTimeFormat` syntax.
  Examples: `SIMPLE_DATE_FORMAT`, `SIMPLE_DATE_FORMAT|yyyy-MM-dd HH:mm:ss`, `SIMPLE_DATE_FORMAT|yyyy-MM-dd|America/Los_Angeles`

Only lexicographically ordered date-time patterns are supported. For example, `yyyy-MM-dd`, `MM-dd`, and `yyyy-dd` are valid, while `MM-dd-yyyy` is not.

## Old Date Time Formats

Legacy date-time formats are still supported for backward compatibility. New schemas should prefer the simplified formats above.

Use the following syntax:

```text
timeSize:timeUnit:timeFormat:pattern
```

- `timeSize`
  Interval size for `EPOCH` values. Pinot multiplies the stored value by this size and unit to compute the actual timestamp.
- `timeUnit`
  A [`TimeUnit`](https://docs.oracle.com/javase/8/docs/api/java/util/concurrent/TimeUnit.html) enum such as `HOURS` or `MINUTES`.
- `timeFormat`
  Either `EPOCH` or `SIMPLE_DATE_FORMAT`.
- `pattern`
  Optional Joda `DateTimeFormat` pattern string, used only with `SIMPLE_DATE_FORMAT`.

Examples:

- `1:MILLISECONDS:EPOCH`
- `1:HOURS:EPOCH`
- `1:DAYS:SIMPLE_DATE_FORMAT:yyyy-MM-dd`
- `1:HOURS:SIMPLE_DATE_FORMAT:EEE MMM dd HH:mm:ss ZZZ yyyy`

## ComplexFieldSpecs

Use complex field specs for complex data types. Pinot currently supports `MAP` and `OPEN_STRUCT`.

| Property | Description |
| --- | --- |
| `name` | Name of the complex column. |
| `description` | Optional human-readable description of the column. |
| `tags` | Optional list of tags for categorizing the column. |
| `fieldId` | Optional stable, name-independent identifier for the column. |
| `aliases` | Optional list of alternate or historical names for the column. |
| `metadata` | Optional free-form string map for column metadata. Pinot preserves non-empty values in schema JSON, omits empty maps, and does not assign built-in semantics or use them for backward-compatibility checks. |
| `dataType` | Complex data type. Currently supports `MAP` and `OPEN_STRUCT`. |
| `fieldType` | Must be `COMPLEX`. |
| `notNull` | Whether the column can contain null values. |
| `childFieldSpecs` | For `MAP`, define the `key` and `value` sub-fields. For `OPEN_STRUCT`, this object is optional and can declare known child fields by name. |

## childFieldSpecs

The `childFieldSpecs` object describes the structure of the `key` and `value` entries inside a `MAP`. For `OPEN_STRUCT`, `childFieldSpecs` is optional: omit it, set it to `{}`, or use it to declare known child fields and their types.

For `OPEN_STRUCT`, declared child fields are the stable contract for keys whose types you want Pinot to preserve exactly. Pinot can still ingest undeclared keys and infers a stored type from the observed values when possible.

### OPEN_STRUCT childFieldSpecs

`OPEN_STRUCT` accepts schema JSON such as the following:

```json
{
  "name": "attributes",
  "dataType": "OPEN_STRUCT",
  "fieldType": "COMPLEX"
}
```

You can also provide `childFieldSpecs` for keys whose types you want to declare up front:

```json
{
  "name": "attributes",
  "dataType": "OPEN_STRUCT",
  "fieldType": "COMPLEX",
  "childFieldSpecs": {
    "count": {
      "name": "count",
      "dataType": "INT",
      "fieldType": "DIMENSION"
    }
  }
}
```

When any schema field uses `OPEN_STRUCT`, `$` is reserved in every schema column name. Pinot uses `$` in the generated materialized child-column names such as `<column>$<key>` and the shared sparse column `<column>$__sparse__`.

### key childFieldSpec

Map keys are always strings.

| Property | Description |
| --- | --- |
| `name` | Must be `key`. |
| `dataType` | Must be `STRING`. |
| `fieldType` | Must be `DIMENSION`. |
| `notNull` | Whether the key can be null. In practice this is typically `false`. |

### value childFieldSpec

Map values can use several scalar types.

| Property | Description |
| --- | --- |
| `name` | Must be `value`. |
| `dataType` | Data type for the map value, for example `STRING`, `INT`, `LONG`, `FLOAT`, or `DOUBLE`. |
| `fieldType` | Should be `DIMENSION` for non-numeric values. |
| `notNull` | Whether the value can be null. |

## Built-in Virtual Columns

Pinot exposes several built-in virtual columns that you can query for debugging and inspection:

| Column Name | Column Type | Data Type | Description |
| --- | --- | --- | --- |
| `$hostName` | Dimension | `STRING` | Name of the server hosting the data. |
| `$segmentName` | Dimension | `STRING` | Name of the segment containing the record. |
| `$docId` | Dimension | `INT` | Document ID of the record within the segment. |
| `$partitionId` | Dimension | `INT` | Partition ID of the segment containing the record. |
| `$creationTime` | Dimension | `TIMESTAMP` | Segment creation time. |
| `$startTime` | Dimension | `TIMESTAMP` | Start of the segment time range, normalized from the time column's unit. |
| `$endTime` | Dimension | `TIMESTAMP` | End of the segment time range, normalized from the time column's unit. |
| `$totalDocs` | Dimension | `INT` | Number of documents physically stored in the segment. |
| `$crc` | Dimension | `LONG` | Segment CRC. |

Virtual columns are excluded from `SELECT *` and materialize only when you name them explicitly. For example, the following query can help identify document-count or CRC differences between segments:

```sql
SELECT $segmentName, $crc, $totalDocs, $creationTime
FROM myTable
GROUP BY 1, 2, 3, 4
```

Segment metadata that is not available is returned as SQL `NULL` when null handling is enabled. For example, a consuming segment has no `$startTime`, `$endTime`, or `$crc` until it is committed, and a table without a time column has no segment time range.

`$totalDocs` is the number of documents stored in the segment, not necessarily the number visible to a query. It includes replaced documents in upsert tables, and the broker time boundary can hide stored rows in hybrid tables.

## Advanced Fields

These advanced properties are available across field specs:

| Property | Description |
| --- | --- |
| `fieldId` | Optional stable, name-independent identifier for a field spec. Pinot preserves it in schema JSON but does not currently use it for compatibility validation or automatic rename handling. |
| `aliases` | Optional list of alternate or historical names for a field spec. Pinot omits empty alias lists from stored JSON and preserves non-empty values as metadata only. |
| `metadata` | Optional free-form string map for a field spec. Pinot preserves non-empty values in schema JSON, omits empty maps, and does not assign built-in semantics or use it for compatibility validation. |
| `maxLength` | Maximum length for `STRING`, `JSON`, and `BYTES` columns. |
| `maxLengthExceedStrategy` | Behavior when incoming values exceed `maxLength`. Supported values are `TRIM_LENGTH`, `SUBSTITUTE_DEFAULT_VALUE`, `NO_ACTION`, and `ERROR`. Defaults to `TRIM_LENGTH` for `STRING` and `NO_ACTION` for `JSON` and `BYTES`. |
| `allowTrailingZeros` | Whether `BIG_DECIMAL` should preserve trailing zeros. Defaults to `false`, which strips them. |
| `virtualColumnProvider` | Provider used to populate a virtual column value. |

For `JSON` columns, Pinot also supports cluster-wide or node-local fallback defaults when the field spec omits `maxLength` or `maxLengthExceedStrategy`. By default, Pinot uses `512` and `NO_ACTION`. You can override those defaults with `pinot.field.spec.default.json.max.length` and `pinot.field.spec.default.json.max.length.exceed.strategy`. Explicit field-spec values still take precedence.

## Related Pages

- [Configuration Reference](README.md)
- [Table Configuration](table.md)
- [First Table + Schema](../../basics/getting-started/first-table-and-schema.md)
- [Table Overview](../../basics/components/table/README.md)
- [Legacy Schema Page](schema.md)
