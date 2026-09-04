---
description: Configure vector indexes (HNSW, IVF_FLAT, IVF_PQ, IVF_ON_DISK) for approximate nearest-neighbor search, radius search, and filter-aware ANN lookups.
---

# Vector Index

Apache Pinot supports vector indexes for efficient approximate nearest-neighbor (ANN) search on embedding columns. This document covers all supported index types, configuration options, quantizers, query patterns, and runtime tuning.

## Overview

Vector indexes accelerate similarity search by partitioning the vector space into clusters or graphs, enabling sub-linear lookup instead of scanning all vectors. Pinot supports four vector index types:

- **HNSW** (Hierarchical Navigable Small World): Graph-based, excellent accuracy, moderate memory
- **IVF_FLAT**: Inverted File with flat quantization, fast index build
- **IVF_PQ**: Inverted File with Product Quantization, balanced speed/memory
- **IVF_ON_DISK**: Disk-backed Inverted File, unlimited scale without the 2 GB JVM limit

## Index Configuration

Vector indexes are configured in the table's field-level `indexes` section using raw encoding.

### Minimal HNSW Configuration

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "HNSW",
          "vectorDimension": 512,
          "vectorDistanceFunction": "COSINE",
          "version": 1
        }
      }
    }
  ]
}
```

### Full HNSW Configuration with Tuning

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "HNSW",
          "vectorDimension": 1536,
          "vectorDistanceFunction": "COSINE",
          "version": 1,
          "properties": {
            "maxCon": "16",
            "beamWidth": "200",
            "storeInSegmentFile": "true"
          }
        }
      }
    }
  ]
}
```

### IVF_FLAT Configuration

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexType": "VECTOR",
      "properties": {
        "vectorIndexType": "IVF_FLAT",
        "vectorDimension": 768,
        "vectorDistanceFunction": "EUCLIDEAN",
        "version": 1,
        "nlist": "128",
        "trainSampleSize": "20000",
        "quantizer": "SQ8"
      }
    }
  ]
}
```

### IVF_PQ Configuration

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexType": "VECTOR",
      "properties": {
        "vectorIndexType": "IVF_PQ",
        "vectorDimension": 768,
        "vectorDistanceFunction": "EUCLIDEAN",
        "version": 1,
        "nlist": "256",
        "trainSampleSize": "50000",
        "pqM": "32",
        "pqNbits": "8",
        "quantizer": "PQ"
      }
    }
  ]
}
```

### IVF_ON_DISK Configuration

Disk-backed IVF for large indexes. Supports all quantizer types and full filter-aware ANN.

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexType": "VECTOR",
      "properties": {
        "vectorIndexType": "IVF_ON_DISK",
        "vectorDimension": 768,
        "vectorDistanceFunction": "EUCLIDEAN",
        "version": 1,
        "nlist": "256",
        "trainSampleSize": "50000",
        "quantizer": "SQ4"
      }
    }
  ]
}
```

## Store Vector Indexes in `columns.psf`

Set `storeInSegmentFile` in the vector index `properties` map to store vector index payloads in the segment's combined index file (`columns.psf`) on V3 segments instead of leaving backend-specific files beside it. The default is `false`. Pinot supports this for `HNSW`, `IVF_FLAT`, `IVF_PQ`, and `IVF_ON_DISK`.

- When the flag changes from `false` to `true`, Pinot absorbs the existing vector index into `columns.psf` on the next segment load.
- When the flag changes from `true` to `false`, Pinot extracts the vector index back to the legacy on-disk layout on the next segment load.
- When `storeInSegmentFile` is `true`, Pinot can load the vector index directly from `columns.psf` even when the segment directory is non-local or remote-backed, such as tiered storage on S3, so no local legacy sidecar files are required.
- The query surface does not change. This flag only changes how Pinot stores the segment index bytes.

For HNSW-style configs, add the property under `indexes.vector.properties`. For IVF-style configs, add it to the vector index `properties` map.

## Distance Functions

| Function | Use Case | Range |
|----------|----------|-------|
| **COSINE** | Normalized text embeddings (OpenAI, BERT) | [0, 2] |
| **EUCLIDEAN** | Unnormalized embeddings or geometric data | [0, ∞) |
| **DOT_PRODUCT** | Pre-normalized, higher score = more similar | (-∞, ∞) |
| **L2** | Alias for EUCLIDEAN | [0, ∞) |

## Quantizers

Pinot supports a generic quantizer framework for trading memory consumption against search speed. Quantizers apply to IVF-family indexes (`IVF_FLAT`, `IVF_PQ`, `IVF_ON_DISK`).

| Quantizer | Memory per dimension | Speed | Use Case |
|-----------|---------------------|-------|----------|
| **FLAT** | 4 bytes | Fastest | High memory budget, maximum accuracy |
| **SQ8** | 1 byte | Fast | 8-bit scalar quantization |
| **SQ4** | 0.5 bytes | Very fast | 4-bit scalar quantization, maximum compression |
| **PQ** | Variable | Medium | Large-scale with product quantization |

SQ8 and SQ4 are fully integrated through the IVF creator, reader, and search paths — they are real backend capabilities, not validation-only features.

## SQL Functions

### VECTOR_SIMILARITY — Top-K ANN Search

Returns the `k` nearest neighbors using the configured vector index:

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 10)
ORDER BY dist ASC
LIMIT 10;
```

### VECTOR_SIMILARITY_RADIUS — Distance-Based Search

Returns all vectors within a distance threshold, without requiring a fixed top-K:

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY_RADIUS(embedding, ARRAY[0.12, 0.34, 0.56, ...], 0.3)
ORDER BY dist ASC;
```

Automatically falls back to brute-force scan on segments without a vector index. Approximate radius support is advertised only for backends where real index-assisted radius search is available.

## Filter-Aware ANN

When a query combines a vector predicate with metadata filters, Pinot can constrain vector candidate generation to the matching row IDs. This improves recall and correctness compared to selecting ANN candidates first and filtering them afterward. HNSW supports this behavior for immutable (offline) and mutable (consuming) segments.

```sql
SELECT ProductId,
       Brand,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 50)
  AND category = 'electronics'
  AND inStock = true
ORDER BY dist ASC
LIMIT 10;
```

**How it works:**
1. The metadata filter (`category = 'electronics'`) builds a bitmap of matching row IDs.
2. Pinot passes that required scope into vector candidate generation instead of applying it as a post-filter.
3. For a sparse required scope, Pinot uses an exact scan over only the matching forward-index rows when the forward index is available.
4. For a denser scope, or when the forward index is disabled, Pinot passes the bitmap to filtered ANN.
5. Only matching vectors can consume top-K candidate slots.

For FULL-upsert tables, the valid-doc-ID bitmap is also part of the required scope. Mutable HNSW therefore excludes obsolete row versions while selecting candidates from consuming segments. The mutable index uses a near-real-time searcher, so newly indexed consuming rows remain visible to filtered searches.

**When to use filter-aware vector search:**
- Combine vector predicates with metadata filters normally; the planner selects exact search or filtered ANN per segment.
- Keep the vector column's forward index when sparse-filter performance matters, because it enables the exact scan over matching rows.
- Combine ANN with exact reranking when you need better ranking accuracy.

`IVF_ON_DISK` has full `FILTER_THEN_ANN` support with pre-filter bitmap computation, explain/debug reporting showing filter selectivity, and consistent behavior with in-memory IVF_FLAT and IVF_PQ.

## HNSW Runtime Tuning

The following query options control HNSW search behavior at runtime without rebuilding the index. They apply to both mutable (consuming) and immutable (offline) segments.

### `vectorEfSearch` — Search Beam Width

Controls how many nodes HNSW visits during graph traversal:

```sql
SET vectorEfSearch = 500;

SELECT ProductId,
       cosineDistance(embedding, ARRAY[...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[...], 10)
ORDER BY dist ASC
LIMIT 10;
```

**Typical values:**
- `100–150`: Low latency (real-time applications)
- `200–300`: Balanced (default)
- `400–800`: High recall (semantic search)

Higher `efSearch` improves accuracy at the cost of query latency.

### `vectorUseRelativeDistance` — Competitive Pruning

Enables or disables competitive pruning during HNSW graph traversal. Disabling can improve recall on some data distributions:

```sql
SET vectorEfSearch = 128;
SET vectorUseRelativeDistance = false;
SET vectorUseBoundedQueue = false;

SELECT cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56], 10)
ORDER BY dist ASC LIMIT 10;
```

## Adaptive Query Planner

Pinot selects the execution mode per segment based on the required scope and available indexes:

| Required scope | Available data | Strategy |
|----------------|----------------|----------|
| None | Vector index | Pure ANN without a required-scope filter |
| Sparse | Forward index | Exact scan over matching row IDs |
| Dense | Filter-aware vector index | Filtered ANN using the required-scope bitmap |
| Sparse, but forward index disabled | Filter-aware vector index | Filtered ANN so the query remains executable |
| Any | No usable vector index | Exact scan using the forward index |

No strategy configuration is required. A required scope is never applied only after ANN candidate selection, so filtered-out or obsolete upsert rows cannot consume top-K slots.

## Query Options

| Option | Default | Description |
|--------|---------|-------------|
| `vectorNprobe` | `4` | Clusters to probe (IVF_FLAT, IVF_PQ, IVF_ON_DISK) |
| `vectorExactRerank` | `true` (IVF_PQ) | Override for exact reranking of ANN candidates |
| `vectorMaxCandidates` | `topK * 10` | Cap on ANN candidates considered |
| `vectorDistanceThreshold` | Not set | Distance threshold on raw Pinot vector distance |
| `vectorEfSearch` | From index config | HNSW only: visit budget for search beam |
| `vectorUseRelativeDistance` | `true` | HNSW only: toggle relative-distance competitive pruning |
| `vectorUseBoundedQueue` | `true` | HNSW only: toggle bounded top-K collector |

## Vector Search Metrics

`VectorSearchMetrics` tracks the following server-side counters:

| Metric | Description |
|--------|-------------|
| `vectorAnnCandidatesRetrieved` | Number of ANN candidates retrieved from the index |
| `vectorExactRerankCount` | Vectors re-ranked with exact distance computation |
| `vectorFilteredOutCount` | Vectors eliminated by the pre-filter bitmap |
| `vectorSearchLatencyMs` | End-to-end search latency |

## Index Type Comparison

| Index | Memory | Build Time | Query Speed | Recall | Quantization | Disk-Backed |
|-------|--------|-----------|-------------|--------|--------------|------------|
| HNSW | Medium | Moderate | Fast | Excellent | — | No |
| IVF_FLAT | High | Fast | Medium | Good | FLAT/SQ8/SQ4 | No |
| IVF_PQ | Low | Moderate | Medium | Fair | Product Quantization | No |
| IVF_ON_DISK | Low | Moderate | Medium | Good | FLAT/SQ8/SQ4/PQ | Yes |

## Complete Example: Semantic Product Search

### Schema

```json
{
  "schemaName": "products",
  "dimensionFieldSpecs": [
    { "name": "ProductId", "dataType": "STRING" },
    { "name": "Category", "dataType": "STRING" },
    {
      "name": "embedding",
      "dataType": "FLOAT",
      "singleValueField": false
    }
  ]
}
```

### Table Configuration

```json
{
  "tableName": "products_OFFLINE",
  "fieldConfigList": [
    {
      "name": "Category",
      "indexes": { "inverted": {} }
    },
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "HNSW",
          "vectorDimension": 1536,
          "vectorDistanceFunction": "COSINE",
          "version": 1,
          "properties": {
            "maxCon": "32",
            "beamWidth": "200",
            "efConstruction": "400"
          }
        }
      }
    }
  ]
}
```

### Basic Top-K Query

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[-0.0013, -0.0110, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[-0.0013, -0.0110, ...], 10)
ORDER BY dist ASC
LIMIT 10;
```

### Filter-Aware ANN Query

```sql
SELECT ProductId,
       Category,
       cosineDistance(embedding, ARRAY[-0.0013, -0.0110, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[-0.0013, -0.0110, ...], 50)
  AND Category = 'Electronics'
ORDER BY dist ASC
LIMIT 10;
```

### Radius Search

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[-0.0013, -0.0110, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY_RADIUS(embedding, ARRAY[-0.0013, -0.0110, ...], 0.25)
ORDER BY dist ASC;
```

### IVF with Exact Reranking

```sql
SET vectorNprobe = 16;
SET vectorMaxCandidates = 500;
SET vectorExactRerank = true;

SELECT l2Distance(embedding, ARRAY[1.0, 2.0, 3.0]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[1.0, 2.0, 3.0], 20)
ORDER BY dist ASC LIMIT 20;
```

### Distance Threshold Without Fixed Top-K

```sql
SET vectorDistanceThreshold = 0.75;
SET vectorMaxCandidates = 500;

SELECT l2Distance(embedding, ARRAY[1.0, 2.0, 3.0]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[1.0, 2.0, 3.0], 200)
ORDER BY dist ASC LIMIT 200;
```

## Related Pages

- [Vector / Similarity Functions](../../functions/vector/) — SQL function reference
- [Vector Query Execution Semantics](../querying-and-sql/vector-query-execution.md) — Execution modes
- [Query Options](../querying-and-sql/query-execution-controls/query-options.md) — Full query options reference
- [Schema and Table Configuration](../../reference/configuration-reference/table.md) — Configuration reference
