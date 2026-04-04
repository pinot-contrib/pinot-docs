---
description: This section contains reference documentation for the JSONKEYVALUEARRAYTOMAP function.
---

# JSONKEYVALUEARRAYTOMAP

Converts an array of objects into a map. By default, Pinot reads the `key` field as the map key and the `value` field as the map value. This function can be used in an [ingestion transformation function](../../build-with-pinot/ingestion/ingestion-level-transformations.md).

## Signature

> JSONKEYVALUEARRAYTOMAP(keyValueArray, \[keyColumnName], \[valueColumnName])

| Arguments | Description |
| --- | --- |
| `keyValueArray` | An **Identifier**/**Expression** containing an array of objects. |
| `keyColumnName` | Optional field name to use as the map key. Defaults to `key`. |
| `valueColumnName` | Optional field name to use as the map value. Defaults to `value`. |

## Usage Examples

```json
[
  {"key": "k1", "value": "v1"},
  {"key": "k2", "value": "v2"},
  {"key": "k3", "value": "v3"}
]
```

| Expression | Value |
| --- | --- |
| `JSONKEYVALUEARRAYTOMAP(input)` | `{"k1":"v1","k2":"v2","k3":"v3"}` |
| `JSONKEYVALUEARRAYTOMAP(input, 'key', 'value')` | `{"k1":"v1","k2":"v2","k3":"v3"}` |

This function can be used in the [table config](../../reference/configuration-reference/table.md) to materialize a `MAP` column during ingestion:

```json
{
  "tableConfig": {
    "ingestionConfig": {
      "transformConfigs": [
        {
          "columnName": "attributes",
          "transformFunction": "JSONKEYVALUEARRAYTOMAP(rawAttributes)"
        }
      ]
    }
  }
}
```
