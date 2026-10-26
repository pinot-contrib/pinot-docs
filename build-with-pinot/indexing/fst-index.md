# FST index

The FST (Finite State Transducer) index accelerates regex queries on STRING columns by building over dictionary
values. It reduces the on-disk index size by 4-6x compared to scanning the full dictionary.

## When to use

Use an FST index for case-sensitive `REGEXP_LIKE` predicates on string columns. It is especially effective for prefix-matching patterns. For case-insensitive `LIKE` or `REGEXP_LIKE` predicates, use the [IFST index](#case-insensitive-fst-index-ifst). For full-text search with tokenization, use the [text index](text-search-support.md) instead.

## Supported column types

- STRING columns only
- Must be single-valued
- Must have dictionary values available. This can come from a dictionary-encoded forward index, or from a standalone
  dictionary paired with a RAW forward index.

## Limitations

- Only supports case-sensitive `REGEXP_LIKE` predicates.
- Only supported on stored or completed segments (not consuming segments in real-time tables).
- Only supported on columns with dictionary values available.
- Works best for prefix queries. Suffix-only or infix-only patterns may not benefit as much.

{% hint style="info" %}
Lucene FST is **case-sensitive**. For example, `WHERE REGEXP_LIKE(colA, 'Value')` matches strings containing "Value" but not "value".

Pinot's `LIKE` operator is **case-insensitive**: `colA LIKE '%Value%'` matches both "Value" and "value". Pinot rewrites `LIKE` to `REGEXP_LIKE` with the `'i'` flag, which can use IFST but cannot use FST. Without IFST, Pinot falls back to dictionary or scan evaluation. Enabling FST does not change which rows `LIKE` matches.
{% endhint %}

For more information on FST construction, see the [Lucene FST documentation](https://lucene.apache.org/core/9_10_0/core/org/apache/lucene/util/fst/FST.html).

## Configuration

To enable the FST index on a column:

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

The FST index generates one index file (`.lucene.fst`). If you keep the forward index RAW, declare a dictionary for the column so Pinot can build the FST from dictionary values:

{% code title="RAW forward index with FST" %}
```json
{
  "fieldConfigList": [
    {
      "name": "text_col_1",
      "encodingType": "RAW",
      "indexTypes": ["FST"],
      "indexes": {
        "dictionary": {}
      }
    }
  ]
}
```
{% endcode %}

Do not keep the column in legacy `tableIndexConfig.noDictionaryColumns` or `tableIndexConfig.noDictionaryConfig` when enabling FST or IFST. Those settings disable the dictionary and Pinot rejects the table config. If an inverted index is also enabled on the column, FST can take advantage of it for faster lookups.

## Query examples

These examples are case-sensitive and can use FST.

Prefix match:

```sql
SELECT productName
FROM products
WHERE REGEXP_LIKE(productName, '^iPhone')
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
WHERE REGEXP_LIKE(description, 'wireless')
```

## Case-insensitive FST index (IFST)

The case-insensitive FST index (IFST) provides the same functionality as the standard FST index but with case-insensitive matching. This eliminates the need to handle case sensitivity manually in queries.

- Supports `LIKE` predicates and `REGEXP_LIKE` predicates with the `'i'` flag.
- Only supported on stored or completed segments (not consuming segments).
- Only supported on STRING columns with dictionary values available.
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

### Query examples

Both queries match strings beginning with "Us" regardless of case and can use IFST:

```sql
SELECT notes FROM products WHERE notes LIKE 'Us%';
SELECT notes FROM products WHERE REGEXP_LIKE(notes, '^Us', 'i');
```

For more information about enabling indexes, see [enabling indexes](README.md#how-pinot-applies-indexes).
