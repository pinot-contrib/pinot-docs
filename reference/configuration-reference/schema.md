---
description: Schema configuration reference.
---

# Schema Configuration

This page is the flat reference for Pinot schema JSON. It brings the top-level schema object, field-spec tables, null-handling rules, date-time formats, MAP support, and advanced column options into one place.

## Key Areas

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>What it covers</th>
      <th>Jump</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Schema object</td>
      <td>Top-level schema fields and a complete example</td>
      <td>[Schema object](#schema-object)</td>
    </tr>
    <tr>
      <td>Field specs</td>
      <td>Dimension, metric, and date-time column definitions</td>
      <td>[Field specs](#field-specs)</td>
    </tr>
    <tr>
      <td>Null handling</td>
      <td>`enableColumnBasedNullHandling` and default null values</td>
      <td>[Null handling](#null-handling)</td>
    </tr>
    <tr>
      <td>Complex fields</td>
      <td>`MAP` columns and `childFieldSpecs`</td>
      <td>[ComplexFieldSpecs](#complexfieldspecs)</td>
    </tr>
    <tr>
      <td>Date-time formats</td>
      <td>New and legacy format syntaxes</td>
      <td>[New DateTime Formats](#new-datetime-formats)</td>
    </tr>
  </tbody>
</table>

## Schema Object

Use a schema to define the column names, data types, null-handling behavior, and field groups for a Pinot table.

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Release Version</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`schemaName`</td>
      <td>-</td>
      <td>required</td>
      <td>Name of the schema. This must match the table name without the `OFFLINE` or `REALTIME` suffix, so both physical tables of a hybrid table share one schema.</td>
    </tr>
    <tr>
      <td>`enableColumnBasedNullHandling`</td>
      <td>1.1.0</td>
      <td>`false`</td>
      <td>When `true`, enables column-based null handling. When `false`, Pinot uses table-based null handling. See [Null value support](../../developers/advanced/null-value-support.md).</td>
    </tr>
    <tr>
      <td>`dimensionFieldSpecs`</td>
      <td>-</td>
      <td>`[]`</td>
      <td>Dimension-column definitions. See [DimensionFieldSpecs](#dimensionfieldspecs).</td>
    </tr>
    <tr>
      <td>`metricFieldSpecs`</td>
      <td>-</td>
      <td>`[]`</td>
      <td>Metric-column definitions. See [MetricFieldSpecs](#metricfieldspecs).</td>
    </tr>
    <tr>
      <td>`dateTimeFieldSpecs`</td>
      <td>-</td>
      <td>`[]`</td>
      <td>Time-column definitions. A schema can define multiple time columns. See [DateTimeFieldSpecs](#datetimefieldspecs).</td>
    </tr>
    <tr>
      <td>`complexFieldSpecs`</td>
      <td>-</td>
      <td>`[]`</td>
      <td>Complex-column definitions. Pinot currently supports `MAP` through this section. See [ComplexFieldSpecs](#complexfieldspecs).</td>
    </tr>
  </tbody>
</table>

## Example Schema

```json
{
  "schemaName": "flights",
  "enableColumnBasedNullHandling": false,
  "dimensionFieldSpecs": [
    {
      "name": "flightNumber",
      "dataType": "LONG"
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

<table>
  <thead>
    <tr>
      <th>Data Type</th>
      <th>Default Dimension Value</th>
      <th>Default Metric Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`INT`</td>
      <td>[Integer.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE)</td>
      <td>`0`</td>
    </tr>
    <tr>
      <td>`LONG`</td>
      <td>[Long.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE)</td>
      <td>`0`</td>
    </tr>
    <tr>
      <td>`FLOAT`</td>
      <td>[Float.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY)</td>
      <td>`0.0`</td>
    </tr>
    <tr>
      <td>`DOUBLE`</td>
      <td>[Double.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY)</td>
      <td>`0.0`</td>
    </tr>
    <tr>
      <td>`BIG_DECIMAL`</td>
      <td>Not supported</td>
      <td>`0.0`</td>
    </tr>
    <tr>
      <td>`BOOLEAN`</td>
      <td>`0` (`false`)</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>`TIMESTAMP`</td>
      <td>`0` (`1970-01-01 00:00:00 UTC`)</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>`STRING`</td>
      <td>`"null"`</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>`JSON`</td>
      <td>`"null"`</td>
      <td>N/A</td>
    </tr>
    <tr>
      <td>`BYTES`</td>
      <td>byte array of length `0`</td>
      <td>byte array of length `0`</td>
    </tr>
  </tbody>
</table>

The `TIMESTAMP` type supports milliseconds epoch precision. Nanoseconds are not supported.

All schema data types are comparable, and ordering must be consistent with equality. Pinot normalizes a few edge cases to preserve that property:

- For `FLOAT` and `DOUBLE`, negative zero (`-0.0`) becomes `0.0`.
- For `FLOAT` and `DOUBLE`, `NaN` becomes the default null value.
- For `BIG_DECIMAL`, trailing zeros are stripped unless `allowTrailingZeros` is enabled.

## Field Specs

Pinot groups columns into dimension, metric, date-time, and complex field specs. The field spec controls column behavior during ingestion, storage, and query execution.

## Null Handling

At schema level, null handling is controlled by `enableColumnBasedNullHandling` and by per-column `defaultNullValue` settings.

- Set `enableColumnBasedNullHandling` to `true` when you want Pinot to store null-ness per column.
- Leave it `false` to keep table-based null handling behavior.
- If a field does not define `defaultNullValue`, Pinot falls back to the internal default for that field type.

### Dimension Default Null Values

<table>
  <thead>
    <tr>
      <th>Data Type</th>
      <th>Internal Default Null Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`INT`</td>
      <td>[Integer.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Integer.html#MIN_VALUE)</td>
    </tr>
    <tr>
      <td>`LONG`</td>
      <td>[Long.MIN_VALUE](https://docs.oracle.com/javase/7/docs/api/java/lang/Long.html#MIN_VALUE)</td>
    </tr>
    <tr>
      <td>`FLOAT`</td>
      <td>[Float.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Float.html#NEGATIVE_INFINITY)</td>
    </tr>
    <tr>
      <td>`DOUBLE`</td>
      <td>[Double.NEGATIVE_INFINITY](https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#NEGATIVE_INFINITY)</td>
    </tr>
    <tr>
      <td>`BOOLEAN`</td>
      <td>`0` (`false`)</td>
    </tr>
    <tr>
      <td>`TIMESTAMP`</td>
      <td>`0` (`1970-01-01 00:00:00 UTC`)</td>
    </tr>
    <tr>
      <td>`STRING`</td>
      <td>`"null"`</td>
    </tr>
    <tr>
      <td>`BYTES`</td>
      <td>byte array of length `0`</td>
    </tr>
    <tr>
      <td>`JSON`</td>
      <td>`"null"`</td>
    </tr>
  </tbody>
</table>

### Metric Default Null Values

<table>
  <thead>
    <tr>
      <th>Data Type</th>
      <th>Internal Default Null Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`INT`</td>
      <td>`0`</td>
    </tr>
    <tr>
      <td>`LONG`</td>
      <td>`0`</td>
    </tr>
    <tr>
      <td>`FLOAT`</td>
      <td>`0.0`</td>
    </tr>
    <tr>
      <td>`DOUBLE`</td>
      <td>`0.0`</td>
    </tr>
    <tr>
      <td>`BIG_DECIMAL`</td>
      <td>`0.0`</td>
    </tr>
    <tr>
      <td>`BYTES`</td>
      <td>byte array of length `0`</td>
    </tr>
  </tbody>
</table>

## DimensionFieldSpecs

Define one dimension field spec for each dimension column.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`name`</td>
      <td>Name of the dimension column.</td>
    </tr>
    <tr>
      <td>`dataType`</td>
      <td>Data type of the dimension column. Supported types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BOOLEAN`, `TIMESTAMP`, `STRING`, `BYTES`, and `JSON`.</td>
    </tr>
    <tr>
      <td>`defaultNullValue`</td>
      <td>Value Pinot should write when the source record is null. If omitted, Pinot uses the internal default for the type.</td>
    </tr>
    <tr>
      <td>`singleValueField`</td>
      <td>Whether the column is single-valued. If `false`, Pinot stores a multi-value list, preserves order, and allows duplicates. The default null value for a multi-value column is a single-element list containing the configured or internal null value.</td>
    </tr>
  </tbody>
</table>

## MetricFieldSpecs

Define one metric field spec for each metric column.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`name`</td>
      <td>Name of the metric column.</td>
    </tr>
    <tr>
      <td>`dataType`</td>
      <td>Data type of the metric column. Supported types are `INT`, `LONG`, `FLOAT`, `DOUBLE`, `BIG_DECIMAL`, and `BYTES` for serialized sketches such as HLL or TDigest.</td>
    </tr>
    <tr>
      <td>`defaultNullValue`</td>
      <td>Value Pinot should write when the source record is null. If omitted, Pinot uses the internal default for the type.</td>
    </tr>
  </tbody>
</table>

## DateTimeFieldSpecs

Use date-time field specs to define time columns.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`name`</td>
      <td>Name of the date-time column.</td>
    </tr>
    <tr>
      <td>`dataType`</td>
      <td>Data type of the date-time column. Supported types are `STRING`, `INT`, `LONG`, and `TIMESTAMP`. Internally `TIMESTAMP` is stored as `LONG` milliseconds since epoch. If you use `TIMESTAMP`, source data must be either `LONG` epoch values or JDBC timestamp strings such as `2021-01-01 01:01:01.123`.</td>
    </tr>
    <tr>
      <td>`format`</td>
      <td>Format in which the time value is stored. See [New DateTime Formats](#new-datetime-formats).</td>
    </tr>
    <tr>
      <td>`granularity`</td>
      <td>Bucket size and unit in `bucketSize:bucketUnit` form, for example `15:MINUTES`. This is descriptive metadata only; Pinot does not automatically round values to the declared granularity.</td>
    </tr>
    <tr>
      <td>`defaultNullValue`</td>
      <td>Value Pinot should write when the source record is null. String-based date-time fields default to `"null"`. `TIMESTAMP` defaults to epoch `0` (`1970-01-01 00:00:00 UTC`). For the primary time column named in table `segmentsConfig`, the default value must fall between `1971-01-01 UTC` and `2071-01-01 UTC`; otherwise Pinot uses segment creation time for segment-management features such as retention and time boundary.</td>
    </tr>
  </tbody>
</table>

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

Use complex field specs for complex data types. Pinot currently supports `MAP`.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`name`</td>
      <td>Name of the complex column.</td>
    </tr>
    <tr>
      <td>`dataType`</td>
      <td>Complex data type. Currently supports `MAP`.</td>
    </tr>
    <tr>
      <td>`fieldType`</td>
      <td>Must be `COMPLEX`.</td>
    </tr>
    <tr>
      <td>`notNull`</td>
      <td>Whether the column can contain null values.</td>
    </tr>
    <tr>
      <td>`childFieldSpecs`</td>
      <td>Definition of the map `key` and `value` sub-fields.</td>
    </tr>
  </tbody>
</table>

## childFieldSpecs

The `childFieldSpecs` object describes the structure of the `key` and `value` entries inside a `MAP`.

### key childFieldSpec

Map keys are always strings.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`name`</td>
      <td>Must be `key`.</td>
    </tr>
    <tr>
      <td>`dataType`</td>
      <td>Must be `STRING`.</td>
    </tr>
    <tr>
      <td>`fieldType`</td>
      <td>Must be `DIMENSION`.</td>
    </tr>
    <tr>
      <td>`notNull`</td>
      <td>Whether the key can be null. In practice this is typically `false`.</td>
    </tr>
  </tbody>
</table>

### value childFieldSpec

Map values can use several scalar types.

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`name`</td>
      <td>Must be `value`.</td>
    </tr>
    <tr>
      <td>`dataType`</td>
      <td>Data type for the map value, for example `STRING`, `INT`, `LONG`, `FLOAT`, or `DOUBLE`.</td>
    </tr>
    <tr>
      <td>`fieldType`</td>
      <td>Should be `DIMENSION` for non-numeric values.</td>
    </tr>
    <tr>
      <td>`notNull`</td>
      <td>Whether the value can be null.</td>
    </tr>
  </tbody>
</table>

## Built-in Virtual Columns

Pinot exposes several built-in virtual columns that you can query for debugging and inspection:

<table>
  <thead>
    <tr>
      <th>Column Name</th>
      <th>Column Type</th>
      <th>Data Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`$hostName`</td>
      <td>Dimension</td>
      <td>`STRING`</td>
      <td>Name of the server hosting the data.</td>
    </tr>
    <tr>
      <td>`$segmentName`</td>
      <td>Dimension</td>
      <td>`STRING`</td>
      <td>Name of the segment containing the record.</td>
    </tr>
    <tr>
      <td>`$docId`</td>
      <td>Dimension</td>
      <td>`INT`</td>
      <td>Document ID of the record within the segment.</td>
    </tr>
  </tbody>
</table>

## Advanced Fields

These advanced properties are available across field specs:

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`maxLength`</td>
      <td>Maximum length for `STRING`, `JSON`, and `BYTES` columns.</td>
    </tr>
    <tr>
      <td>`maxLengthExceedStrategy`</td>
      <td>Behavior when incoming values exceed `maxLength`. Supported values are `TRIM_LENGTH`, `SUBSTITUTE_DEFAULT_VALUE`, `NO_ACTION`, and `ERROR`. Defaults to `TRIM_LENGTH` for `STRING` and `NO_ACTION` for `JSON` and `BYTES`.</td>
    </tr>
    <tr>
      <td>`allowTrailingZeros`</td>
      <td>Whether `BIG_DECIMAL` should preserve trailing zeros. Defaults to `false`, which strips them.</td>
    </tr>
    <tr>
      <td>`virtualColumnProvider`</td>
      <td>Provider used to populate a virtual column value.</td>
    </tr>
  </tbody>
</table>

## Related Pages

- [Configuration Reference](README.md)
- [Table Configuration](table.md)
- [First Table + Schema](../../basics/getting-started/first-table-and-schema.md)
- [Table Overview](../../basics/components/table/README.md)
- [Legacy Schema Page](../../configuration-reference/schema.md)
