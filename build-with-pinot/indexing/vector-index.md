---
description: Configure vector indexes (HNSW, IVF_FLAT, IVF_PQ, IVF_ON_DISK) for approximate nearest-neighbor search, radius search, and filter-aware ANN lookups.
---

# Vector Index

Apache Pinot supports vector indexes for efficient approximate nearest-neighbor (ANN) search on embedding columns. This document covers index configuration, query patterns, Phase 4 features including filter-aware ANN, radius search, quantizers, and runtime tuning options.

## Overview

Vector indexes accelerate similarity search by partitioning the vector space into clusters or graphs, enabling sub-linear lookup instead of scanning all vectors. Pinot supports four vector index types:

- **HNSW** (Hierarchical Navigable Small World): Graph-based, excellent accuracy, moderate memory
- **IVF_FLAT**: Inverted File with flat quantization, fast index build
- **IVF_PQ**: Inverted File with Product Quantization, balanced speed/memory
- **IVF_ON_DISK**: Disk-backed Inverted File, unlimited scale without 2GB limit (Phase 4)

## Final Phase Completion Notes (Pinot 1.6.0+)

As of PR #18168, the Pinot vector stack now includes complete final-phase implementations:

### Quantizer Real-Path Integration

SQ8 and SQ4 quantizers are now **fully integrated** through the entire IVF creator, reader, and search paths:
- **SQ8**: 1 byte per dimension, 8-bit scalar quantization
- **SQ4**: 0.5 bytes per dimension, 4-bit scalar quantization
- Both are now real backend capabilities, not just validation-only features

### HNSW Runtime Controls on Both Mutable and Immutable

The following query-time controls now affect real HNSW search behavior on both **mutable and immutable** segments:
- `vectorEfSearch`: Controls the search beam width (visit budget) at query time
- `vectorUseRelativeDistance`: Enables/disables competitive pruning during graph traversal
- `vectorUseBoundedQueue`: Toggles bounded top-K collector behavior

These controls allow fine-tuning HNSW search without rebuilding indexes.

### IVF_ON_DISK Filter-Aware ANN Parity

`IVF_ON_DISK` now has full `FILTER_THEN_ANN` support with:
- Pre-filter bitmap computation before ANN traversal
- Explain/debug reporting showing filter selectivity
- Consistent behavior with in-memory IVF_FLAT and IVF_PQ

### Backend-Aware Approximate Radius

Approximate radius capabilities are now **truthfully advertised** only where real backend support exists:
- Backend capability flags are checked before reporting approximate-radius support
- `VECTOR_SIMILARITY_RADIUS(...)` uses exact scan on backends without index-assisted radius support
- Mixed immutable/mutable segments fallback gracefully with explicit explain visibility


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
            "beamWidth": "200"
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

### IVF_ON_DISK Configuration (Phase 4)

Disk-backed IVF using FileChannel random-access reads, enabling unlimited scale without 2GB JVM limit:

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

## Distance Functions

| Function | Use Case | Range |
|----------|----------|-------|
| **COSINE** | Normalized text embeddings (OpenAI, BERT) | [0, 2] |
| **EUCLIDEAN** | Unnormalized embeddings or geometric data | [0, ∞) |
| **DOT_PRODUCT** | Pre-normalized, higher score = more similar | (-∞, ∞) |
| **L2** | Alias for EUCLIDEAN | [0, ∞) |

## Quantizer Types (Phase 4)

Generic quantizer framework supporting multiple quantization strategies:

| Quantizer | Memory | Speed | Use Case |
|-----------|--------|-------|----------|
| **FLAT** | 4 bytes × dimension | Fastest | High memory budget |
| **SQ8** | 1 byte × dimension | Fast | 8-bit quantization |
| **SQ4** | 0.5 bytes × dimension | Very fast | 4-bit quantization |
| **PQ** | Variable | Medium | Large scale |

### SQ4 Example (IVF_ON_DISK)

See [IVF_ON_DISK Configuration](#ivf_on_disk-configuration-phase-4) above for SQ4 integration with disk-backed indexes.

## SQL Functions

### VECTOR_SIMILARITY (Basic ANN)

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 10)
ORDER BY dist ASC
LIMIT 10;
```

### VECTOR_SIMILARITY_RADIUS (Phase 4)

Distance-based filtering without fixed top-K:

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY_RADIUS(embedding, ARRAY[0.12, 0.34, 0.56, ...], 0.3)
ORDER BY dist ASC;
```

Returns all vectors within the distance threshold. Automatically falls back to brute-force on segments without a vector index.

## Filter-Aware ANN (FILTER_THEN_ANN) — Phase 4

Pre-filters vectors using a bitmap before ANN lookup for improved recall on selective filters:

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
1. Metadata filter builds a bitmap (`category = 'electronics'`)
2. Bitmap passed to HNSW/IVF via `FilterAwareVectorIndexReader`
3. Index prunes vectors before ANN traversal
4. Better recall than post-ANN filtering

**When to use:**
- Selective filters removing 70%+ of rows
- Combine with exact reranking for best accuracy

## HNSW Runtime Tuning (Phase 4)

`vectorEfSearch` query option for runtime HNSW search beam width tuning without rebuilding:

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
- `100–150`: Low latency (real-time)
- `200–300`: Balanced (default)
- `400–800`: High recall (semantic search)

Higher efSearch = better accuracy, slower queries.

## Adaptive Query Planner (Phase 4)

Automatically selects optimal execution mode via `VectorSearchStrategy` in `FilterPlanNode`:

| Filter Selectivity | Mode | Strategy |
|-------------------|------|----------|
| None | `ANN_TOP_K` | Pure ANN |
| Low (<30%) | `FILTER_THEN_ANN` | Filter bitmap → ANN |
| High (>70%) | `ANN_THEN_FILTER` | ANN → filter |
| No index | `EXACT_SCAN` | Brute-force scan |

## Vector Search Metrics (Phase 4)

`VectorSearchMetrics` singleton tracks:
- `vectorAnnCandidatesRetrieved`: ANN candidates retrieved
- `vectorExactRerankCount`: Vectors re-ranked with exact distance
- `vectorFilteredOutCount`: Vectors filtered by pre-filter bitmap
- `vectorSearchLatencyMs`: End-to-end search latency

## Query Options

| Option | Default | Description |
|--------|---------|-------------|
| `vectorNprobe` | `4` | Clusters to probe (IVF_FLAT, IVF_PQ, IVF_ON_DISK) |
| `vectorExactRerank` | `true` (IVF_PQ) | Boolean override for exact rerank of ANN candidates |
| `vectorMaxCandidates` | `topK * 10` | Positive integer cap for ANN candidates |
| `vectorDistanceThreshold` | Not set | Finite float threshold on raw Pinot vector distance |
| `vectorEfSearch` | From config | HNSW-only: positive integer visit budget for search |
| `vectorUseRelativeDistance` | `true` | HNSW-only: boolean toggle for relative-distance pruning |
| `vectorUseBoundedQueue` | `true` | HNSW-only: boolean toggle for bounded top-K collector |

## Index Type Comparison

| Index | Memory | Build Time | Speed | Recall | Quantization | Disk-Backed |
|-------|--------|-----------|-------|--------|--------------|------------|
| HNSW | Medium | Moderate | Fast | Excellent | Optional | No |
| IVF_FLAT | High | Fast | Medium | Good | Optional | No |
| IVF_PQ | Low | Moderate | Medium | Fair | Product Quantization | No |
| IVF_ON_DISK | Low | Moderate | Medium | Good | FLAT/SQ8/SQ4/PQ | Yes |

## Example: Semantic Product Search

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

### Table Config

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

### Runtime Tuning

```sql
SET vectorEfSearch = 500;

SELECT ProductId,
       cosineDistance(embedding, ARRAY[-0.0013, -0.0110, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[-0.0013, -0.0110, ...], 20)
ORDER BY dist ASC
LIMIT 10;
```

## Sample SQL Queries with Runtime Controls

### Basic Top-K ANN

```sql
SELECT cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56], 10)
ORDER BY dist ASC LIMIT 10;
```

### HNSW Runtime Controls

Tune HNSW search behavior at query-time without rebuilding:

```sql
SET vectorEfSearch = 128;
SET vectorUseRelativeDistance = false;
SET vectorUseBoundedQueue = false;
SELECT cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56], 10)
ORDER BY dist ASC LIMIT 10;
```

### IVF Runtime Controls with Exact Rerank

Control IVF search breadth and candidate selection:

```sql
SET vectorNprobe = 16;
SET vectorMaxCandidates = 500;
SET vectorExactRerank = true;
SELECT l2Distance(embedding, ARRAY[1.0, 2.0, 3.0]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[1.0, 2.0, 3.0], 20)
ORDER BY dist ASC LIMIT 20;
```

### Distance Threshold Search

Return all vectors within a distance threshold without fixed top-K:

```sql
SET vectorDistanceThreshold = 0.75;
SET vectorMaxCandidates = 500;
SELECT l2Distance(embedding, ARRAY[1.0, 2.0, 3.0]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY(embedding, ARRAY[1.0, 2.0, 3.0], 200)
ORDER BY dist ASC LIMIT 200;
```

### Radius Predicate (Phase 4)

Direct radius search without top-K requirement:

```sql
SELECT l2Distance(embedding, ARRAY[1.0, 2.0, 3.0]) AS dist, doc_id
FROM my_table
WHERE VECTOR_SIMILARITY_RADIUS(embedding, ARRAY[1.0, 2.0, 3.0], 0.75)
ORDER BY dist ASC LIMIT 200;
```

## Related Pages

- [Vector / Similarity Functions](../../functions/vector/) — SQL function reference
- [Vector Query Execution Semantics](../querying-and-sql/vector-query-execution.md) — Execution modes
- [Query Options](../querying-and-sql/query-execution-controls/query-options.md) — Full query options reference
- [Schema and Table Configuration](../../reference/configuration-reference/table.md) — Configuration reference
