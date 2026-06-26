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

The `TIMESTAMP` type supports milliseconds epoch precision. Nanoseconds are not supported.

All schema data types are comparable, and ordering must be consistent with equality. Pinot normalizes a few edge cases to preserve that property:

- For `FLOAT` and `DOUBLE`, negative zero (`-0.0`) becomes `0.0`.
- For `FLOAT` and `DOUBLE`, `NaN` becomes the default null value.
- For `BIG_DECIMAL`, trailing zeros are stripped unless `allowTrailingZeros` is enabled.

## Field Specs

Pinot groups columns into dimension, metric, date-time, and complex field specs. The field spec controls column behavior during ingestion, storage, and query execution.

All field-spec families also accept optional metadata keys `fieldId` and `aliases`. Pinot preserves these values in schema JSON and omits them when unset, but it does not currently use them to validate backward-compatible schema updates or to rewrite ingestion and query paths automatically.

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
| `dataType` | Data type of the dimension column. Supported types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, `BOOLEAN`, `TIMESTAMP`, `STRING`, `BYTES`, and `JSON`. |
| `defaultNullValue` | Value Pinot should write when the source record is null. If omitted, Pinot uses the internal default for the type. |
| `singleValueField` | Whether the column is single-valued. If `false`, Pinot stores a multi-value list, preserves order, and allows duplicates. This includes `BIG_DECIMAL` and `BYTES` dimension columns. The default null value for a multi-value column is a single-element list containing the configured or internal null value. |

## MetricFieldSpecs

Define one metric field spec for each metric column.

| Property | Description |
| --- | --- |
| `name` | Name of the metric column. |
| `description` | Optional human-readable description of the column. |
| `tags` | Optional list of tags for categorizing the column. |
| `fieldId` | Optional stable, name-independent identifier for the column. |
| `aliases` | Optional list of alternate or historical names for the column. |
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
| `dataType` | Complex data type. Currently supports `MAP` and `OPEN_STRUCT`. |
| `fieldType` | Must be `COMPLEX`. |
| `notNull` | Whether the column can contain null values. |
| `childFieldSpecs` | For `MAP`, define the `key` and `value` sub-fields. For `OPEN_STRUCT`, this object is optional and can declare known child fields by name. |

## childFieldSpecs

The `childFieldSpecs` object describes the structure of the `key` and `value` entries inside a `MAP`. For `OPEN_STRUCT`, `childFieldSpecs` is optional: omit it, set it to `{}`, or use it to declare known child fields and their types.

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

## Advanced Fields

These advanced properties are available across field specs:

| Property | Description |
| --- | --- |
| `fieldId` | Optional stable, name-independent identifier for a field spec. Pinot preserves it in schema JSON but does not currently use it for compatibility validation or automatic rename handling. |
| `aliases` | Optional list of alternate or historical names for a field spec. Pinot omits empty alias lists from stored JSON and preserves non-empty values as metadata only. |
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
