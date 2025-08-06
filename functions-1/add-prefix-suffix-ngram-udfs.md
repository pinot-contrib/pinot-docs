---
description: This section contains reference documentation for the add prefix, suffix and ngram UDFs.
---

# Add Prefix, Suffix & Ngram UDFs

Adding ngram, prefix, postfix UDFs to improve query throughput by enabling efficient text search through derived columns with inverted indexes.

## Context

We are onboarding a use case and trying to increase query throughput. We tested that QPS cannot be further improved with existing `REGEXP_LIKE` queries or `TEXT_MATCH` queries. The queries are as follows:

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

## Signature

> NGRAM(col, n)
>
> PREFIX(col, prefixString)
>
> SUFFIX(col, suffixString)

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

### N-gram Generation

```sql
SELECT NGRAM('Apache pinot', 2) AS bigrams
FROM myTable
```

| bigrams |
| ------- |
| ap,pa,ac,ch,he,e , p,pi,in,no,ot |

### Prefix Operations

```sql
SELECT PREFIX('data', 'prefix_') AS result
FROM myTable
```

| result      |
| ----------- |
| prefix_data |

### Suffix (Postfix) Operations

```sql
SELECT SUFFIX('data', '_suffix') AS result
FROM myTable
```

| result      |
| ----------- |
| data_suffix |

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
