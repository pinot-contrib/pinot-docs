---
description: This section contains reference documentation for the JSONEXTRACTKEY function.
---

# jsonextractkey

Extracts all matched JSON field keys based on 'jsonPath' into a STRING\_ARRAY.

## Signature

> JSONEXTRACTKEY(jsonField, 'jsonPath')

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `jsonField`  | An **Identifier**/**Expression** contains JSON documents.                                              |
| `'jsonPath'` | Follows [JsonPath Syntax](https://goessner.net/articles/JsonPath/) to read values from JSON documents. |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers**.
{% endhint %}

## Usage Examples

The examples in this section are based on the [Batch JSON Quick Start](../../basics/getting-started/quick-start.md#batch-json). In particular we'll be querying the row `WHERE id = 7044874109`.

```sql
select id, repo, JSONEXTRACTKEY(repo, '$.*') AS keys
from githubEvents 
WHERE id = 7044874109
```

| id         | repo                                                                                           | keys                         |
| ---------- | ---------------------------------------------------------------------------------------------- | ---------------------------- |
| 7044874109 | {"id":115911530,"name":"LimeVista/Tapes","url":"https://api.github.com/repos/LimeVista/Tapes"} | `$['id'],$['name'],$['url']` |
