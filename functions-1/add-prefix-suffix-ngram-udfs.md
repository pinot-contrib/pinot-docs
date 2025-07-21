---
description: This section contains reference documentation for the add prefix, suffix and ngram UDFs.
---

# Add Prefix, Suffix & Ngram UDFs

Provides prefix, suffix and ngram functionality for advanced string manipulation and text matching. These UDFs enable efficient text search and pattern matching capabilities, especially useful for wildcard searches and text prefiltering to avoid full table scans.

## What is N-gram

N-gram breaks down text into overlapping sequences of N characters. For example:

**"Apache Pinot"** with 2-grams produces:
- `Ap`, `pa`, `ac`, `ch`, `he`, `e `, ` P`, `Pi`, `in`, `no`, `ot`

When matching `ngram(col, "ap")`, it searches for the substring "ap" within the generated n-grams.
When matching `ngram(col, 'apache')`, it generates n-grams from "apache" (ap, pa, ac, ch, he) and matches against the column's n-grams.

## When to Use N-gram

N-grams are particularly useful for:

- **Text matching** - Fast substring search
- **Wildcard queries** - Alternative to `REGEXP_LIKE` (which requires full scan)
- **Prefix matching** - More efficient than O(N * length of string) operations
- **Prefiltering** - Avoid full table scans by using n-gram indexing

### Performance Comparison
- `REGEXP_LIKE`: Full scan O(N)
- `Prefix matching`: O(N * length of string)
- `Wildcard matching`: O(N * length)
- **N-gram approach**: Enables prefiltering to avoid scanning all rows

## Signature

> NGRAM(col, n)
>
> PREFIX(col, prefixString)
>
> SUFFIX(col, suffixString)

### `col`
The input string column or expression to process.

### `n`
For n-gram operations, the length of each gram (typically 2 for bigrams, 3 for trigrams).

### `prefixString` / `suffixString`
The string to add as prefix or suffix to the input.

## Usage Examples

### N-gram Generation

```sql
SELECT NGRAM('Apache Pinot', 2) AS bigrams
FROM myTable
```

| bigrams |
| ------- |
| Ap,pa,ac,ch,he,e ,  P,Pi,in,no,ot |

```sql
SELECT NGRAM('fast', 3) AS trigrams
FROM myTable
```

| trigrams |
| -------- |
| fas,ast |

### Prefix Operations

```sql
SELECT PREFIX('Pinot', 'Apache ') AS name
FROM myTable
```

| name         |
| ------------ |
| Apache Pinot |

### Suffix Operations

```sql
SELECT SUFFIX('Apache', ' Pinot') AS name
FROM myTable
```

| name         |
| ------------ |
| Apache Pinot |

### Advanced Text Matching with N-grams

Using n-grams for efficient text search with prefiltering:

```sql
SELECT organizationUUID, confirmedEmployeeCount, name
FROM rta.rta.u4b_organizations
WHERE deletedAt IS NULL
  AND (IN_SERIALIZED_LIST(entityTypes, 'org!https://emoji.slack-edge.com/TQ3BASMK9/u4b/b32791585b8da8cc.jpg!organization'))
  AND (TEXT_MATCH(name, '/.pacific./ AND /.equity./')
       OR TEXT_MATCH(profileName, '/.pacific./ AND /.equity./'))
ORDER BY confirmedEmployeeCount DESC
OFFSET 0 LIMIT 10
```

### N-gram Based Wildcard Search

```sql
-- Traditional approach (slow - full scan)
SELECT * FROM documents
WHERE REGEXP_LIKE(content, '.*apache.*pinot.*')

-- N-gram approach (fast - with prefiltering)
SELECT * FROM documents
WHERE NGRAM(content, 2) LIKE '%ap%'
  AND NGRAM(content, 2) LIKE '%pi%'
  AND content LIKE '%apache%pinot%'
```

## Implementation Notes

### Simulated N-gram Approach

For optimal performance, consider using a simulated n-gram approach by storing n-grams in a dedicated column:

1. **Generate n-gram column** during ingestion using the UDF
2. **Translate queries** to use prefilters on the n-gram column
3. **Trade-off**: Increased disk size for faster query performance

For more details, see [GitHub PR #12392](https://github.com/apache/pinot/pull/12392).

### Best Practices

- Use **bigrams (n=2)** for most text search scenarios
- Use **trigrams (n=3)** for more precise matching with longer texts
- Combine n-gram prefiltering with exact string matching for optimal results
- Consider disk space impact when storing pre-computed n-grams
