---
description: This section contains reference documentation for the JSONEXTRACTKEY function.
---

# jsonextractkey

Extracts all matched JSON field keys based on 'jsonPath' into a STRING\_ARRAY.

## Signature

> JSONEXTRACTKEY(jsonField, 'jsonPath', \[paramString])

| Arguments       | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jsonField`     | An **Identifier**/**Expression** contains JSON documents.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `'jsonPath'`    | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `'paramString'` | <p>Parameter-based configuration for advanced options using semicolon-delimited key-value pairs.</p><ul><li><p>MAXDEPTH: Controls maximum extraction depth to prevent overly deep traversals</p><ul><li>Example: jsonExtractKey(json, '$..**', 'MAXDEPTH=2') - Extract keys up to 2 levels deep</li><li>Default: Unlimited depth (Integer.MAX_VALUE)</li><li>Non-positive values treated as unlimited</li></ul></li><li><p>DOTNOTATION: Toggle between JsonPath and dot notation output formats</p><ul><li>Example: jsonExtractKey(json, '$..**', 'DOTNOTATION=true')</li><li>JsonPath format: $['a']['b']['c']</li><li>Dot notation: a.b.c</li><li>Default: false (JsonPath format)</li></ul></li></ul> |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers**.
{% endhint %}

## Usage Examples

The examples in this section are based on the [Batch JSON Quick Start](../basics/getting-started/quick-start.md#batch-json). In particular we'll be querying the row `WHERE id = 7044874109`.

```sql
select id, repo, JSONEXTRACTKEY(repo, '$.*') AS keys
from githubEvents 
WHERE id = 7044874109
```



| id         | repo                                                                                           | keys                                   |
| ---------- | ---------------------------------------------------------------------------------------------- | -------------------------------------- |
| 7044874109 | {"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"} | `["$['id']", "$['name']", "$['url']"]` |

```sql
select id, repo, JSONEXTRACTKEY(repo, '$.*', 'dotNotation=true') AS keys
from githubEvents 
WHERE id = 7044874109
```

| id         | repo                                                                                           | keys                    |
| ---------- | ---------------------------------------------------------------------------------------------- | ----------------------- |
| 7044874109 | {"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"} | `["id", "name", "url"]` |





More examples

```sql
-- Basic key extraction (existing functionality)
SELECT jsonExtractKey(repo, '$.*') FROM table

-- Extract keys with depth limit
SELECT jsonExtractKey(repo, '$..**', 'MAXDEPTH=2') FROM table

-- Extract keys in dot notation format
SELECT jsonExtractKey(repo, '$..**', 'DOTNOTATION=true') FROM table

-- Combined parameters
SELECT jsonExtractKey(repo, '$..**', 'MAXDEPTH=3;DOTNOTATION=true') FROM table
```



