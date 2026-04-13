# Vector Query Execution Semantics

Apache Pinot supports advanced vector query capabilities including filtered approximate nearest-neighbor (ANN) search, distance-based threshold filtering, and compound retrieval strategies. This document explains the execution modes, query options, and filtering patterns available for vector queries.

## Overview

Vector queries in Pinot support:

1. **Distance Threshold Filtering** via `vectorDistanceThreshold` query option
2. **Filtered ANN** combining `VECTOR_SIMILARITY` with metadata filters
3. **8 explicit execution modes** visible in EXPLAIN output
4. **Per-backend capabilities** for different vector index types (HNSW, IVF_FLAT, IVF_PQ, IVF_ON_DISK)

## Vector Distance Threshold Query Option

The `vectorDistanceThreshold` query option enables distance-based filtering in vector similarity queries. This allows you to retrieve all vectors within a specified distance threshold instead of a fixed top-K result set.

### Syntax

```sql
SET vectorDistanceThreshold = <threshold_value>;

SELECT <columns>
FROM <table>
WHERE VECTOR_SIMILARITY(column, ARRAY[...], topK)
ORDER BY <distance_function> ASC
LIMIT <limit>;
```

### Usage

When `vectorDistanceThreshold` is set, Pinot returns all results within the specified distance rather than being limited to the top-K. This is useful for semantic search, similarity detection, and other tasks where you need all relevant matches beyond a certain confidence level.

### Example: Threshold-Based Search

Find all products similar to a query embedding within a cosine distance of 0.3:

```sql
SET vectorDistanceThreshold = 0.3;

SELECT ProductId,
       Summary,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 100)
ORDER BY dist ASC
LIMIT 1000;
```

In this example:
- The `VECTOR_SIMILARITY` predicate retrieves up to 100 ANN candidates
- The `vectorDistanceThreshold = 0.3` filter applied to the distance function results
- Only products with cosine distance <= 0.3 are returned
- Results are ordered by distance ascending

## Execution Modes

Pinot uses 8 distinct execution modes for vector queries, each selected based on the query structure and available indexes. The execution mode is visible in the EXPLAIN output via the `executionMode` field.

### 1. ANN_TOP_K (Default)

**When selected:** Simple `VECTOR_SIMILARITY` without metadata filters or distance threshold

**Behavior:**
- Executes pure approximate nearest-neighbor search
- Returns exactly top-K results by vector similarity
- No filtering applied after ANN lookup
- Fastest execution path

**Example query:**
```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 10)
ORDER BY dist ASC
LIMIT 10;
```

**EXPLAIN output:**
```
executionMode: ANN_TOP_K
```

---

### 2. ANN_TOP_K_WITH_RERANK

**When selected:** `VECTOR_SIMILARITY` with `vectorExactRerank=true`

**Behavior:**
- Retrieves ANN candidates using vector index
- Re-ranks candidates using exact distance calculation from forward index
- Improves accuracy at the cost of additional exact distance computations
- Recommended for IVF_PQ (enabled by default) where index distances are approximate

**Example query:**
```sql
SET vectorExactRerank = true;

SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 20)
ORDER BY dist ASC
LIMIT 10;
```

**EXPLAIN output:**
```
executionMode: ANN_TOP_K_WITH_RERANK
```

---

### 3. ANN_THEN_FILTER

**When selected:** `VECTOR_SIMILARITY` combined with non-vector metadata filters (no distance threshold)

**Behavior:**
- Executes ANN on vector similarity to get top-K candidates
- Applies metadata filters (e.g., `AND category = 'electronics'`) to the results
- Does NOT rerank by distance; filtering happens after ANN
- Useful for combining semantic search with attribute-based filtering

**Example query:**
```sql
SELECT ProductId,
       Summary,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 50)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 10;
```

**EXPLAIN output:**
```
executionMode: ANN_THEN_FILTER
```

---

### 4. ANN_THEN_FILTER_THEN_RERANK

**When selected:** `VECTOR_SIMILARITY` with metadata filters AND `vectorExactRerank=true`

**Behavior:**
- Executes ANN to get candidates
- Applies metadata filters
- Re-ranks filtered results using exact distance
- Best accuracy for filtered queries with approximate indexes

**Example query:**
```sql
SET vectorExactRerank = true;

SELECT ProductId,
       Summary,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 50)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 10;
```

**EXPLAIN output:**
```
executionMode: ANN_THEN_FILTER_THEN_RERANK
```

---

### 5. FILTER_THEN_ANN

**When selected:** `VECTOR_SIMILARITY` combined with highly selective metadata filters on a backend that supports filter-aware search (HNSW, IVF_FLAT, IVF_ON_DISK). The adaptive planner selects this mode when filter selectivity is low (fewer than 30% of rows pass the filter).

**Behavior:**
- Evaluates the metadata filter first to build a bitmap of matching row IDs
- Passes the bitmap to the vector index via `FilterAwareVectorIndexReader`
- The ANN traversal considers only vectors in the bitmap, improving recall on selective filters
- Returns up to top-K results from the filtered vector space

**Example query:**
```sql
SELECT ProductId,
       Brand,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 10)
  AND category = 'rare_collectibles'
ORDER BY dist ASC
LIMIT 10;
```

**EXPLAIN output:**
```
executionMode: FILTER_THEN_ANN
```

{% hint style="info" %}
The adaptive planner in `FilterPlanNode` automatically chooses between `FILTER_THEN_ANN` and `ANN_THEN_FILTER` based on filter selectivity. You do not need to set a query option — Pinot picks the faster strategy per segment.
{% endhint %}

---

### 6. ANN_THRESHOLD_SCAN

**When selected:** `VECTOR_SIMILARITY` with `vectorDistanceThreshold` (no metadata filters)

**Behavior:**
- Executes ANN search
- Applies distance threshold filter to returned candidates
- Returns all results within the distance threshold
- Useful for confidence-based retrieval

**Example query:**
```sql
SET vectorDistanceThreshold = 0.3;

SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 100)
ORDER BY dist ASC
LIMIT 1000;
```

**EXPLAIN output:**
```
executionMode: ANN_THRESHOLD_SCAN
```

---

### 7. ANN_THRESHOLD_THEN_FILTER

**When selected:** `VECTOR_SIMILARITY` with BOTH `vectorDistanceThreshold` AND metadata filters

**Behavior:**
- Executes ANN search
- Applies distance threshold filter
- Applies metadata filters to threshold-filtered results
- Combines confidence-based and attribute-based filtering

**Example query:**
```sql
SET vectorDistanceThreshold = 0.3;

SELECT ProductId,
       Summary,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 100)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 1000;
```

**EXPLAIN output:**
```
executionMode: ANN_THRESHOLD_THEN_FILTER
```

---

### 8. EXACT_SCAN

**When selected:** Segment lacks a vector index (e.g., realtime segments with IVF_FLAT, IVF_PQ, or IVF_ON_DISK)

**Behavior:**
- Falls back to exact forward-index scan
- Scans all vectors and computes distances for the entire segment
- Slower than ANN but provides exact results
- Automatically applied for segments without vector indexes
- IVF_FLAT, IVF_PQ, and IVF_ON_DISK do not support realtime/mutable segments; HNSW supports both

**When this occurs:**
- Newly ingested data in realtime segments before segment rollover
- Tables without vector index configured
- Intentional fallback due to missing index

**EXPLAIN output:**
```
executionMode: EXACT_SCAN
fallbackReason: ivf_pq_index_unavailable
```

## Filtered ANN: Combining Vector and Metadata Filters

Pinot automatically detects and optimizes patterns where `VECTOR_SIMILARITY` is combined with metadata filters in an AND expression. This enables efficient filtered nearest-neighbor search.

### Pattern: AND(VECTOR_SIMILARITY, non-vector-filter)

When a query contains both a vector similarity predicate and other non-vector filters in an AND clause, Pinot's FilterPlanNode optimizes execution as follows:

1. **ANN Lookup Phase:** Use vector index to retrieve candidates
2. **Filter Phase:** Apply metadata filters to the candidate set
3. **Rerank Phase** (optional): Exact rerank if enabled

### Example: Finding Similar Products in a Category

```sql
SELECT ProductId,
       Brand,
       Price,
       l2Distance(embedding, ARRAY[0.1, 0.2, 0.3, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.1, 0.2, 0.3, ...], 50)
  AND category = 'electronics'
  AND price < 200
ORDER BY dist ASC
LIMIT 10;
```

**Execution flow:**
1. **ANN:** Retrieve up to 50 products closest to the query embedding
2. **Metadata Filter:** Keep only those where `category = 'electronics'` AND `price < 200`
3. **Rank:** Sort by exact L2 distance
4. **Limit:** Return top 10

**EXPLAIN output shows:**
```
executionMode: ANN_THEN_FILTER
```

### Example: Filtered ANN with Exact Reranking

For better accuracy with approximate indexes (especially IVF_PQ):

```sql
SET vectorExactRerank = true;

SELECT ProductId,
       Brand,
       l2Distance(embedding, ARRAY[0.1, 0.2, 0.3, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.1, 0.2, 0.3, ...], 100)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 10;
```

**Execution flow:**
1. **ANN:** Retrieve 100 candidates
2. **Metadata Filter:** Keep only electronics
3. **Exact Rerank:** Compute exact distances for filtered candidates
4. **Rank & Limit:** Return top 10 by exact distance

**EXPLAIN output shows:**
```
executionMode: ANN_THEN_FILTER_THEN_RERANK
```

## Viewing Execution Mode with EXPLAIN

Use the `EXPLAIN` statement with `explainAskingServers=true` to see the vector query execution plan, including the execution mode and backend details.

### Basic EXPLAIN

```sql
EXPLAIN PLAN FOR
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 10)
ORDER BY dist ASC
LIMIT 10;
```

### Verbose EXPLAIN with Server Plans

```sql
SET explainAskingServers = true;

EXPLAIN PLAN FOR
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 50)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 10;
```

**Output includes:**
- **executionMode:** Which of the 8 modes is used (e.g., `ANN_THEN_FILTER`)
- **backend:** Vector index type (HNSW, IVF_FLAT, IVF_PQ, IVF_ON_DISK, or EXACT)
- **distanceFunction:** Configured distance metric (COSINE, EUCLIDEAN, etc.)
- **nprobe:** Number of clusters probed (IVF_FLAT/IVF_PQ only)
- **exactRerank:** Whether exact reranking is enabled
- **candidateCount:** Number of candidates examined
- **fallbackReason:** If applicable (e.g., `ivf_pq_index_unavailable`)

## Query Option Reference for Vector Queries

When working with vector queries, these query options control execution behavior:

| Option | Effect | Default |
|--------|--------|---------|
| `vectorDistanceThreshold` | Return all results within this distance threshold | Not set (uses top-K) |
| `vectorExactRerank` | Re-rank ANN candidates using exact distances | `true` for IVF_PQ; `false` for HNSW/IVF_FLAT |
| `vectorNprobe` | Number of clusters to probe (IVF_FLAT, IVF_PQ, IVF_ON_DISK) | 4 |
| `vectorMaxCandidates` | Max ANN candidates to examine before exact reranking | topK * 10 |
| `vectorEfSearch` | HNSW search beam width — controls how many nodes the graph traversal visits | From index config |
| `vectorUseRelativeDistance` | HNSW competitive pruning toggle — disabling can improve recall on some data distributions | `true` |
| `vectorUseBoundedQueue` | HNSW bounded top-K collector toggle | `true` |
| `explainAskingServers` | Include segment-level execution plan in EXPLAIN | `false` |

### Setting Query Options

```sql
SET vectorDistanceThreshold = 0.3;
SET vectorExactRerank = true;
SET vectorNprobe = 8;
SET explainAskingServers = true;

SELECT ProductId, cosineDistance(embedding, ARRAY[...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[...], 50)
ORDER BY dist ASC
LIMIT 10;
```

## Compound Retrieval Strategies

Compound retrieval combines multiple filtering and ranking techniques to balance accuracy and performance.

### Strategy 1: High-Recall ANN with Reranking

Retrieve more candidates and rerank for better accuracy:

```sql
SET vectorExactRerank = true;

SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 100)
ORDER BY dist ASC
LIMIT 10;
```

**Tradeoff:** Higher latency but better accuracy, especially with approximate indexes.

---

### Strategy 2: Filtered ANN with Metadata

Combine vector and attribute filtering for domain-specific search:

```sql
SELECT ProductId,
       Brand,
       l2Distance(embedding, ARRAY[0.1, 0.2, 0.3, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.1, 0.2, 0.3, ...], 50)
  AND inStock = true
  AND rating >= 4.0
ORDER BY dist ASC
LIMIT 10;
```

**Benefits:** Narrows candidate set early, reduces reranking cost.

---

### Strategy 3: Threshold-Based Retrieval

Return all results meeting a confidence threshold:

```sql
SET vectorDistanceThreshold = 0.2;

SELECT ProductId,
       Summary,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 200)
ORDER BY dist ASC;
```

**Use case:** All "relevant enough" results rather than fixed top-K.

---

### Strategy 4: Filtered Threshold Search

Combine threshold filtering with metadata filters:

```sql
SET vectorDistanceThreshold = 0.25;

SELECT ProductId,
       Summary,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 200)
  AND category = 'Books'
ORDER BY dist ASC;
```

**Use case:** All relevant results in a specific category.

## Performance Considerations

### When to Use Each Execution Mode

| Mode | Best For | Latency | Accuracy |
|------|----------|---------|----------|
| **ANN_TOP_K** | Simple similarity search | Fast | Good (depends on index) |
| **ANN_TOP_K_WITH_RERANK** | Approximate indexes (IVF_PQ) | Slower | Excellent |
| **ANN_THEN_FILTER** | Category/attribute filtering (non-selective filters) | Medium | Good |
| **ANN_THEN_FILTER_THEN_RERANK** | Accurate filtered search | Slower | Excellent |
| **FILTER_THEN_ANN** | Highly selective filters (removes >70% of rows) | Medium | Excellent |
| **ANN_THRESHOLD_SCAN** | Confidence-based filtering | Varies | Good |
| **ANN_THRESHOLD_THEN_FILTER** | Confidence + category filters | Slower | Good |
| **EXACT_SCAN** | No index available | Very slow | Perfect |

### Tuning Tips

1. **For IVF_PQ:** Enable `vectorExactRerank = true` (the default) to compensate for quantization loss
2. **For filtered queries:** Retrieve more candidates (larger topK) and let Pinot filter; this is faster than smaller topK
3. **For threshold queries:** Retrieve enough candidates to ensure you get all threshold matches; use a generous topK
4. **For high-dimensional vectors:** Consider IVF_PQ for memory efficiency, IVF_ON_DISK for unlimited scale without the 2 GB heap limit, or HNSW for best accuracy

## See Also

- [Vector Index Documentation](../indexing/vector-index.md) — Configure and tune vector indexes
- [Vector / Similarity Functions](../../functions/vector/) — Distance functions and VECTOR_SIMILARITY syntax
- [Query Options](query-execution-controls/query-options.md) — Full reference of query-time settings
- [Query Execution](querying-pinot.md) — General query execution concepts
