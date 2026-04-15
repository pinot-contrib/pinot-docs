# FST index

The FST (Finite State Transducer) index accelerates regex queries on dictionary-encoded STRING columns. It reduces the on-disk index size by 4-6x compared to scanning the full dictionary.

## When to use

Use an FST index when your queries use `LIKE` or `REGEXP_LIKE` predicates on string columns. It is especially effective for prefix-matching patterns. For full-text search with tokenization, use the [text index](text-search-support.md) instead.

## Supported column types

- STRING columns only
- Must be single-valued
- Must be dictionary-encoded

## Limitations

- Only supports regex queries (`LIKE` and `REGEXP_LIKE` predicates).
- Only supported on stored or completed segments (not consuming segments in real-time tables).
- Only supported on dictionary-encoded columns.
- Works best for prefix queries. Suffix-only or infix-only patterns may not benefit as much.

{% hint style="info" %}
Lucene FST is **case-sensitive**. When using an FST index in queries, ensure your pattern matches the case stored in the data. For example, `WHERE colA LIKE '%Value%'` will match "Value" but not "value". For case-insensitive matching, use the [IFST index](#case-insensitive-fst-index-ifst) instead.
{% endhint %}

For more information on FST construction, see the [Lucene FST documentation](https://lucene.apache.org/core/9_10_0/core/org/apache/lucene/util/fst/FST.html).

## Configuration

To enable the FST index on a dictionary-encoded column:

{% code title="Recommended: fieldConfigList" %}
```json
{
  "fieldConfigList": [
    {
      "name": "text_col_1",
      "encodingType": "DICTIONARY",
      "indexType": "FST"
    }
  ]
}
```
{% endcode %}

The FST index generates one index file (`.lucene.fst`). If an inverted index is also enabled on the column, FST can take advantage of it for faster lookups.

## Query examples

Prefix match:

```sql
SELECT productName
FROM products
WHERE productName LIKE 'iPhone%'
```

Regex match:

```sql
SELECT email
FROM users
WHERE REGEXP_LIKE(email, '^admin.*@example\\.com$')
```

Infix match:

```sql
SELECT description
FROM products
WHERE description LIKE '%wireless%'
```

## Case-insensitive FST index (IFST)

The case-insensitive FST index (IFST) provides the same functionality as the standard FST index but with case-insensitive matching. This eliminates the need to handle case sensitivity manually in queries.

- Supports case-insensitive regex queries.
- Only supported on stored or completed segments (not consuming segments).
- Only supported on dictionary-encoded STRING columns.
- Works best for prefix queries with case-insensitive matching.

### Configuration

{% code title="IFST configuration" %}
```json
{
  "fieldConfigList": [
    {
      "name": "notes",
      "encodingType": "DICTIONARY",
      "indexes": {
        "ifst": {
          "enabled": true
        }
      }
    }
  ]
}
```
{% endcode %}

The case-insensitive FST index generates one index file (`.lucene.ifst`).

For more information about enabling indexes, see [enabling indexes](README.md#how-pinot-applies-indexes).
