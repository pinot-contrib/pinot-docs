---
description: This section contains reference documentation for the add prefix, suffix and ngram UDFs.
---

# Add Prefix, Suffix & Ngram UDFs

Adding ngram, prefix, postfix UDFs to improve query throughput by enabling efficient text search through derived columns with inverted indexes.

## Context

We were aiming to increase query throughput for a matching use case. Initial testing shows that the current approaches using `REGEXP_LIKE` and `TEXT_MATCH` queries have reached their performance limits, and further improvements in QPS cannot be achieved with these methods. The representative queries under evaluation are as follows:

```sql
SELECT col1, col2 FROM table WHERE REGEXP_LIKE(col3, '^data*')
SELECT col1, col2 FROM table WHERE REGEXP_LIKE(col3, 'data$')
SELECT col1, col2 FROM table WHERE REGEXP_LIKE(col3, '*data*')
SELECT col1, col2 FROM table WHERE TEXT_MATCH(col3, '/data*/')
```

The plan is to generate derived columns that persist prefix, postfix, and ngram to use inverted indexes to filter results fast, and add text match indexes to do validation after filtering to avoid false positive results.

## What is N-gram

N-gram breaks down text into overlapping sequences of characters. For example:

**"Apache pinot"** produces:
- `ap`, `pa`, `ac`, `ch`, `he`, `e `, ` p`, ...

When you match `ngram(col, "ap")`, it searches for the substring "ap" within the generated n-grams.

When you match `ngram(col, 'apache')`, it generates n-grams from "apache" (`ap`, `pa`, `ac`, etc.) and matches against the column's n-grams.

## When to Use N-gram

N-grams solve performance issues with:
- **Text match** - Avoid full scans
- **REGEXP_LIKE** - Currently requires full scan
- **Prefix matching** - Reduce O(N * length of string) complexity
- **Wildcard matching** - Reduce O(N * length) complexity

### How to Make Wildcards Fast

Need to do prefiltering to avoid full scan of all rows.
**How to prefilter → use ngram!**

## Function Parameters

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Parameters</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`prefixes`</td>
      <td>`String input, int maxlength`</td>
      <td>Generate array of prefix strings shorter than maxlength</td>
    </tr>
    <tr>
      <td>`prefixesWithPrefix`</td>
      <td>`String input, int maxlength, @Nullable String prefix`</td>
      <td>Generate array of prefix matchers with prepended prefix (e.g. '^' for regex)</td>
    </tr>
    <tr>
      <td>`suffixes`</td>
      <td>`String input, int maxlength`</td>
      <td>Generate array of suffix strings shorter than maxlength</td>
    </tr>
    <tr>
      <td>`suffixesWithSuffix`</td>
      <td>`String input, int maxlength, @Nullable String suffix`</td>
      <td>Generate array of suffix matchers with appended suffix (e.g. '$' for regex)</td>
    </tr>
    <tr>
      <td>`uniqueNgrams`</td>
      <td>`String input, int length`</td>
      <td>Generate array of unique ngrams of exact specified length</td>
    </tr>
    <tr>
      <td>`uniqueNgrams`</td>
      <td>`String input, int minGram, int maxGram`</td>
      <td>Generate array of unique ngrams within length range [minGram, maxGram]</td>
    </tr>
  </tbody>
</table>

## Usage Examples

### Example Query

```sql
SELECT organizationUUID, confirmedEmployeeCount, name
FROM rta.rta.u4b_organizations
WHERE deletedAt IS NULL
  AND (IN_SERIALIZED_LIST(entityTypes, 'org:u4b:organization'))
  AND (TEXT_MATCH(name, '/.*pacific.*/ AND /.*equity.*/')
       OR TEXT_MATCH(profileName, '/.*pacific.*/ AND /.*equity.*/'))
ORDER BY confirmedEmployeeCount DESC
OFFSET 0 LIMIT 10
```

### Prefix Operations

```sql
SELECT prefixes('data', 3) AS result
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>["d", "da", "dat"]</td>
    </tr>
  </tbody>
</table>

```sql
SELECT prefixesWithPrefix('data', 3, '^') AS result
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>["^d", "^da", "^dat"]</td>
    </tr>
  </tbody>
</table>

### Suffix Operations

```sql
SELECT suffixes('data', 3) AS result
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>["a", "ta", "ata"]</td>
    </tr>
  </tbody>
</table>

```sql
SELECT suffixesWithSuffix('data', 3, '$') AS result
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>["a$", "ta$", "ata$"]</td>
    </tr>
  </tbody>
</table>

### N-gram Generation

#### Table Config with Transformation

Instead of using SQL UDF, configure n-gram generation during ingestion using `transformationConfig`:

```json
{
  "tableName": "myTable",
  "tableType": "OFFLINE",
  "ingestionConfig": {
    "transformationConfigs": [
      {
        "columnName": "content_bigrams",
        "transformFunction": "uniqueNgrams(content, 2)"
      },
      {
        "columnName": "content_ngrams",
        "transformFunction": "uniqueNgrams(content, 2, 4)"
      }
    ]
  }
}
```

#### Query Examples

```sql
SELECT uniqueNgrams('Apache pinot', 2) AS bigrams
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>bigrams</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>["Ap", "pa", "ac", "ch", "he", "e ", " p", "pi", "in", "no", "ot"]</td>
    </tr>
  </tbody>
</table>

```sql
SELECT uniqueNgrams('data', 2, 4) AS ngrams
FROM myTable
```

<table>
  <thead>
    <tr>
      <th>ngrams</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>["da", "at", "ta", "dat", "ata", "data"]</td>
    </tr>
  </tbody>
</table>

**Using Generated N-grams**

```sql
-- Traditional approach (slow)
SELECT * FROM T WHERE REGEXP_LIKE(field, '*pino.*')

-- Optimized approach with n-gram prefiltering
SELECT * FROM T
WHERE ngram = 'pin' AND ngram = 'ino' AND ngram = 'not'
  AND REGEXP_LIKE(field, '*pino.*')
```

```sql
-- Traditional approach for short strings
SELECT * FROM T WHERE REGEXP_LIKE(field, '*pi.*')

-- Optimized approach (no validation needed when search string ≤ ngram length)
SELECT * FROM T WHERE ngram = 'pi'
```

## How to Use N-gram

### Simulated N-gram Approach

This patch creates a simulated ngram approach by storing the grams into a column:

1. **First, use the UDF to generate a ngram column** during data ingestion
2. **Translate the query with prefilters** to use the ngram column for fast filtering
3. **Trade-off**: Disk size will grow, but query performance improves significantly

### Implementation Steps

1. Generate derived columns with prefix, postfix, and ngram values
2. Create inverted indexes on these derived columns
3. Use prefiltering with ngram indexes to reduce candidate rows
4. Apply original text match validation to avoid false positives

For more details, see [GitHub PR #12392](https://github.com/apache/pinot/pull/12392).
