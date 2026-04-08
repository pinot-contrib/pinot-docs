# Vector index

## Overview

Apache Pinot now supports a Vector Index for efficient similarity searches over high-dimensional vector embeddings. This feature introduces the capability to store and query float array columns (multi-valued) using a vector similarity algorithm.

## When to use

Use the vector index when you need to find the most similar items in a high-dimensional vector space. Common use cases include semantic search, recommendation systems, image similarity, and retrieval-augmented generation (RAG) where text embeddings are stored alongside metadata.

## Supported column types

The vector index is supported on multi-valued FLOAT columns (float arrays). The column must be declared as `singleValueField: false` in the schema with `dataType: FLOAT`.

## Key Features

* Vector Index supports multiple backend implementations for approximate nearest neighbor (ANN) search:
  * **HNSW** (Hierarchical Navigable Small World) - highly accurate graph-based approach
  * **IVF_FLAT** (Inverted File with Flat Quantization) - efficient vector partitioning approach
  * **IVF_PQ** (Inverted File with Product Quantization) - compressed ANN with up to 32× smaller index footprint
* Adds support for a predicate and function:
  * VECTOR\_SIMILARITY(v1, v2, \[optional topK]) to retrieve the topK closest vectors based on similarity.
  * The similarity function can be used as part of a query to filter and rank results.
* Query-time tuning options for optimizing accuracy and performance trade-offs

## Examples

Below is an example schema designed for a use case involving product reviews with vector embeddings for each review.

### Schema

```json
{
  "metricFieldSpecs": [],
  "dimensionFieldSpecs": [
    {
      "dataType": "STRING",
      "name": "ProductId"
    },
    {
      "dataType": "STRING",
      "name": "UserId"
    },
    {
      "dataType": "INT",
      "name": "Score"
    },
    {
      "dataType": "STRING",
      "name": "Summary"
    },
    {
      "dataType": "STRING",
      "name": "Text"
    },
    {
      "dataType": "STRING",
      "name": "combined"
    },
    {
      "dataType": "INT",
      "name": "n_tokens"
    },
    {
      "dataType": "FLOAT",
      "name": "embedding",
      "singleValueField": false
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "ts",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:TIMESTAMP",
      "granularity": "1:SECONDS"
    }
  ],
  "schemaName": "fineFoodReviews"
}
```

In this schema:

• The embedding column is a multi-valued float array designed to store high-dimensional vector embeddings (e.g., 1536 dimensions from an NLP model).

• Other fields, such as ProductId, UserId, and Text, store metadata and review text.



### Table Config

To enable the **Vector Index**, configure the table with the appropriate `fieldConfigList`. The embedding column is specified to use the Vector Index with HNSW for similarity searches.

```json
{
  ...
  "fieldConfigList": [
    {
      "encodingType": "RAW",
      "indexType": "VECTOR",
      "name": "embedding",
      "properties": {
        "vectorIndexType": "HNSW",
        "vectorDimension": 1536,
        "vectorDistanceFunction": "COSINE",
        "version": 1
      }
    }
  ]
}
```

Explanation of Properties:

1. vectorIndexType:

Specifies the type of vector index to use. Supported values: `HNSW`, `IVF_FLAT`, `IVF_PQ`.

2. vectorDimension:

Defines the dimensionality of the vectors stored in the column. (e.g., 1536 for typical embeddings from models like OpenAI or BERT).

3. vectorDistanceFunction:

Specifies the distance metric for similarity computation. Options include:

*   INNER\_PRODUCT:

    • Computes the inner product (dot product) of the two vectors.

    • Typically used when vectors are normalized and higher scores indicate greater similarity.
*   L2:

    • Measures the Euclidean distance between vectors.

    • Suitable for tasks where spatial closeness in high-dimensional space indicates similarity.
*   L1:

    • Measures the Manhattan distance between vectors (sum of absolute differences of coordinates).

    • Useful for some scenarios where simpler distance metrics are preferred.
*   COSINE:

    • Measures cosine similarity, which considers the angle between vectors.

    • Ideal for normalized vectors where orientation matters more than magnitude.&#x20;

4. version:

Specifies the version of the Vector Index implementation.

### HNSW tuning parameters

The HNSW index supports additional tuning via the `properties` map in the field config. These are passed through to the underlying Lucene HNSW implementation:

| Property | Default | Description |
| --- | --- | --- |
| `maxCon` | 16 | Maximum number of connections per node in the HNSW graph. Higher values improve recall but increase index size and build time. |
| `beamWidth` | 100 | Beam width used during index construction. Higher values improve recall at the cost of slower indexing. |
| `maxDimensions` | 2048 | Maximum number of vector dimensions supported. |
| `maxBufferSizeMB` | 16 | RAM buffer size for the Lucene index writer. |
| `useCompoundFile` | true | Whether to use Lucene compound file format. |
| `mode` | BEST_SPEED | Lucene codec mode. Options: `BEST_SPEED`, `BEST_COMPRESSION`. |

#### Recommended configuration (new format)

The recommended way to configure the vector index uses the `indexes` object in `fieldConfigList`:

{% code title="Recommended: fieldConfigList with indexes" %}
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
            "maxCon": "32",
            "beamWidth": "200"
          }
        }
      }
    }
  ]
}
```
{% endcode %}

## IVF_FLAT Vector Index

In addition to HNSW, Pinot now supports **IVF_FLAT** (Inverted File with Flat Quantization), a highly efficient vector indexing backend. IVF_FLAT is optimized for faster indexing and lower memory overhead while maintaining strong query performance through intelligent vector partitioning.

### IVF_FLAT Configuration

IVF_FLAT uses a clustering-based approach to partition vectors into groups (lists), enabling efficient filtering of candidate vectors during similarity search. Here's an example configuration:

{% code title="IVF_FLAT configuration in fieldConfigList" %}
```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "IVF_FLAT",
          "vectorDimension": 128,
          "vectorDistanceFunction": "EUCLIDEAN",
          "nlist": 64
        }
      }
    }
  ]
}
```
{% endcode %}

### IVF_FLAT Properties

| Property | Required | Description |
| --- | --- | --- |
| `vectorIndexType` | Yes | Set to `IVF_FLAT` |
| `vectorDimension` | Yes | Dimensionality of the vectors (e.g., 128, 768) |
| `vectorDistanceFunction` | Yes | Distance metric: `EUCLIDEAN` (L2), `COSINE`, `INNER_PRODUCT`, or `DOT_PRODUCT` |
| `nlist` | Yes | Number of inverted file lists (clusters). Higher values reduce search scope but increase memory. Typical range: 16-256 |

### Supported Distance Functions

IVF_FLAT supports the same distance functions as HNSW:

* **EUCLIDEAN** (L2): Euclidean distance in vector space
* **COSINE**: Cosine similarity, ideal for normalized vectors
* **INNER_PRODUCT**: Dot product, used for pre-normalized vectors
* **DOT_PRODUCT**: Equivalent to INNER_PRODUCT

### Query-Time Tuning Options

IVF_FLAT (and IVF_PQ) support query-time parameters to fine-tune the accuracy-performance trade-off:

```sql
-- Set the number of clusters to probe (default: 1)
SET vectorNprobe=16;

-- Enable exact reranking of candidate vectors (default: false)
SET vectorExactRerank=true;

-- Maximum number of candidate vectors to examine (default: depends on nlist)
SET vectorMaxCandidates=1000;

-- Execute the vector similarity query
SELECT ProductId,
       UserId,
       l2_distance(embedding, ARRAY[0.1, 0.2, ...]) AS l2_dist
FROM fineFoodReviews
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.1, 0.2, ...], 10)
ORDER BY l2_dist ASC
LIMIT 10;
```

**Query-time parameters explanation:**

* **vectorNprobe**: Number of inverted file lists to probe. Higher values increase recall at the cost of more computation. Start with nlist/4 and adjust based on query performance. Applies to IVF_FLAT and IVF_PQ; ignored for HNSW.
* **vectorExactRerank**: When enabled, Pinot re-ranks the ANN candidates using exact distance from the forward index. This improves accuracy, but it does not turn the query into a full exact scan. Defaults to `true` for IVF_PQ (since PQ distances are approximate) and `false` for HNSW and IVF_FLAT.
* **vectorMaxCandidates**: Maximum number of ANN candidates to examine before exact rerank. This only affects queries with `vectorExactRerank=true`.

If a segment does not have a vector index, Pinot falls back to an exact forward-index scan for that segment. In that path Pinot ignores IVF_FLAT-specific tuning such as `vectorNprobe` and `vectorMaxCandidates`.

### IVF_FLAT vs HNSW

| Aspect | IVF_FLAT | HNSW |
| --- | --- | --- |
| **Index Build Speed** | Fast | Slower |
| **Memory Overhead** | Lower | Higher (maintains graph structure) |
| **Recall** | Good with proper tuning | Excellent |
| **Query Latency** | Faster (with vectorNprobe tuning) | Consistent |
| **Use Case** | Large-scale similarity search, memory-constrained | High-accuracy retrieval |

## IVF_PQ Vector Index

**IVF_PQ** (Inverted File with Product Quantization) is a compressed ANN backend that uses product quantization to produce indexes up to 32× smaller than IVF_FLAT while maintaining strong query performance through intelligent vector partitioning and quantization. This phase 2 implementation includes a memory-bounded index creator, comprehensive query-time tuning, and support for multiple distance functions.

### Overview and Key Features

IVF_PQ combines:
* **Inverted File (IVF)** partitioning: Vectors are clustered into coarse groups (lists) via k-means, enabling efficient filtering of search scope
* **Product Quantization (PQ)**: Vectors are compressed into compact codes using PQ sub-quantizers, reducing index size and memory footprint
* **Memory-bounded creation**: A two-pass spill-to-disk design bounds heap memory to O(trainSampleSize × dimension) instead of O(N × dimension), making it feasible to build large indexes on single machines
* **Asymmetric distance tables**: Query-time distance computation uses asymmetric tables for efficient approximate and exact distance calculations across L2, inner product, and cosine distance functions
* **Recommended defaults helper**: Sensible defaults are provided so users don't have to hand-tune all IVF_PQ parameters

### IVF_PQ Configuration

{% code title="IVF_PQ configuration in fieldConfigList" %}
```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "IVF_PQ",
          "vectorDimension": 128,
          "vectorDistanceFunction": "EUCLIDEAN",
          "version": 1,
          "properties": {
            "nlist": "128",
            "pqM": "16",
            "pqNbits": "8",
            "trainSampleSize": "10000"
          }
        }
      }
    }
  ]
}
```
{% endcode %}

### IVF_PQ Properties

| Property | Required | Description |
| --- | --- | --- |
| `vectorIndexType` | Yes | Set to `IVF_PQ` |
| `vectorDimension` | Yes | Dimensionality of the vectors (e.g., 128, 768, 1536) |
| `vectorDistanceFunction` | Yes | Distance metric: `EUCLIDEAN` (L2), `COSINE`, `INNER_PRODUCT`, `DOT_PRODUCT`, or `L1` |
| `nlist` | Yes | Number of coarse clusters for inverted file partitioning. Typical range: 16–256. Higher values reduce search scope per probe but increase memory. |
| `pqM` | Yes | Number of PQ sub-quantizers. Must evenly divide `vectorDimension`. Example: dim=128 → pqM ∈ {1, 2, 4, 8, 16, 32, 64, 128} |
| `pqNbits` | Yes | Bits per PQ code: `4`, `6`, or `8`. Controls the trade-off between compression (4 bits is smallest) and accuracy (8 bits is most accurate). |
| `trainSampleSize` | Yes | Number of training vectors used for k-means centroid and PQ codebook construction. Must be ≥ `nlist`. Typical: 10,000–100,000. Larger samples improve model quality but increase build time. |
| `trainingSeed` | No | Random seed for reproducible k-means and PQ training. If not set, a random seed is used. |
| `version` | Yes | Version of the IVF_PQ format. Currently set to `1`. |

### IVF_PQ Validation Rules

* `pqM` must evenly divide `vectorDimension` (no remainder)
* `pqNbits` must be one of `4`, `6`, or `8`
* `trainSampleSize` must be ≥ `nlist` (need enough training samples for k-means)
* Backend-specific properties cannot be mixed across HNSW, IVF_FLAT, and IVF_PQ in the same field config
* Distance function must be one of the supported metrics listed above

### Supported Distance Functions

IVF_PQ supports all vector distance functions through asymmetric distance tables:

* **EUCLIDEAN (L2)**: Computes exact Euclidean distance using asymmetric tables
* **L1**: Manhattan distance via asymmetric tables
* **COSINE**: Cosine similarity with normalized vector support
* **INNER_PRODUCT**: Dot product via approximate asymmetric tables (good for unnormalized embeddings)
* **DOT_PRODUCT**: Equivalent to INNER_PRODUCT

### Recommended Defaults Helper

If you don't want to hand-tune all parameters, use the `VectorIndexConfigValidator.recommendedIvfPqDefaults()` helper method (available in the validation layer):

```java
Map<String, String> defaults = 
  VectorIndexConfigValidator.recommendedIvfPqDefaults(
    128,           // vectorDimension
    "EUCLIDEAN"    // vectorDistanceFunction
  );
```

This returns sensible defaults based on dimension and distance function:
* `nlist`: ~dimension / 8, min 16, max 256
* `pqM`: Optimal divisor of dimension close to dim / 8
* `pqNbits`: 8 (best accuracy for typical use)
* `trainSampleSize`: max(nlist × 40, 10000)

### Memory-Bounded Index Creation

The IVF_PQ creator uses a two-pass spill-to-disk design to bound memory usage:

**Pass 1 (Add)**:
* Vectors are streamed in and written to a temporary `.spill` file on disk
* Up to `trainSampleSize` vectors are reservoir-sampled in memory for later training
* Peak heap usage is O(trainSampleSize × dimension), not O(N × dimension)

**Pass 2 (Seal)**:
* K-means training is performed on the in-memory sample to compute coarse centroids
* PQ codebook is learned from the sample
* The `.spill` file is streamed back through memory to assign each vector to a cluster and encode it
* The final `.vector.ivfpq.index` file is written with:
  - Magic header (IVPQ), format version, dimension, vector count
  - Coarse centroids for k-means
  - PQ codebooks (one per dimension partition)
  - Per-list doc IDs and PQ-encoded vectors
* The temporary `.spill` file is deleted

**Typical memory footprint**:
* 10K vectors, dim=128, trainSampleSize=10K: ~6 MB heap
* 100K vectors, dim=128, trainSampleSize=100K: ~200 MB heap
* Compare to naive approach: 10M vectors would require ~19 GB with naive buffering

### IVF_PQ Runtime Behavior

* **Default exact rerank**: IVF_PQ defaults to `vectorExactRerank=true` (unlike HNSW and IVF_FLAT which default to `false`). Because PQ distances are approximate by construction (quantization loss), reranking with exact distances from the forward index significantly improves recall at acceptable latency.
* **Mutable segments**: IVF_PQ does not support mutable (realtime) segments. Realtime segments fall back to an exact forward-index scan with `fallbackReason=ivf_pq_index_unavailable` in the explain output.
* **Query-time tuning**: `vectorNprobe`, `vectorExactRerank`, and `vectorMaxCandidates` all apply to IVF_PQ the same way as IVF_FLAT.
* **Debug info**: The `getIndexDebugInfo()` method is available on all backends and provides per-list cardinality statistics, effective nprobe, and quantization metrics.

### Query-Time Tuning for IVF_PQ

IVF_PQ queries support the same runtime parameters as IVF_FLAT:

```sql
-- Probe more clusters for higher recall (default: 1)
SET vectorNprobe=16;

-- Disable exact rerank for lower latency if recall loss is acceptable
SET vectorExactRerank=false;

-- Limit candidates examined before rerank
SET vectorMaxCandidates=1000;

-- Run the query
SELECT ProductId, UserId, l2Distance(embedding, ARRAY[...]) AS dist
FROM myTable
WHERE vectorSimilarity(embedding, ARRAY[...], 10)
ORDER BY dist ASC LIMIT 10;
```

**nprobe tuning**: `vectorNprobe` controls the number of inverted lists (clusters) probed per query.
* Default: 1 (fastest, lowest recall)
* Recommended start: nlist / 8 to nlist / 4
* Higher values increase recall at the cost of latency
* Practical range: 1 to nlist

### Configuration Examples

#### Euclidean Distance (L2)

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "IVF_PQ",
          "vectorDimension": 128,
          "vectorDistanceFunction": "EUCLIDEAN",
          "version": 1,
          "properties": {
            "nlist": "128",
            "pqM": "16",
            "pqNbits": "8",
            "trainSampleSize": "10000",
            "trainingSeed": "42"
          }
        }
      }
    }
  ]
}
```

#### Cosine Distance (Normalized Vectors)

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "IVF_PQ",
          "vectorDimension": 512,
          "vectorDistanceFunction": "COSINE",
          "version": 1,
          "properties": {
            "nlist": "256",
            "pqM": "64",
            "pqNbits": "8",
            "trainSampleSize": "20000"
          }
        }
      }
    }
  ]
}
```

#### Inner Product (Approximate Dot Product)

```json
{
  "fieldConfigList": [
    {
      "name": "embedding",
      "encodingType": "RAW",
      "indexes": {
        "vector": {
          "vectorIndexType": "IVF_PQ",
          "vectorDimension": 1536,
          "vectorDistanceFunction": "INNER_PRODUCT",
          "version": 1,
          "properties": {
            "nlist": "128",
            "pqM": "192",
            "pqNbits": "8",
            "trainSampleSize": "10000"
          }
        }
      }
    }
  ]
}
```

### Disk Footprint Comparison

IVF_PQ achieves significant space savings through quantization:

| Backend | Bytes per vector (dim=128) | Compression vs IVF_FLAT |
| --- | --- | --- |
| IVF_FLAT | 512 bytes | 1× (baseline) |
| HNSW | ~640–800 bytes | 1.25–1.56× larger |
| IVF_PQ (pqM=16, pqNbits=8) | 16 bytes | 32× smaller |
| IVF_PQ (pqM=32, pqNbits=6) | 24 bytes | 21× smaller |
| IVF_PQ (pqM=16, pqNbits=4) | 8 bytes | 64× smaller |

For a 100M vector corpus at dim=512, IVF_PQ with 32× compression saves 20+ GB on disk.

### IVF_PQ vs IVF_FLAT vs HNSW

| Aspect | IVF_PQ | IVF_FLAT | HNSW |
| --- | --- | --- | --- |
| **Index Size** | Smallest (32× compression) | Medium (512 B/vec) | Largest (~700 B/vec) |
| **Build Speed** | Slower (PQ training, ~1–6K docs/s) | Fast (~18–163K docs/s) | Slower (~varies) |
| **Build Memory** | Bounded (spill-to-disk) | O(N × dim) buffering | Unbounded (graph structure) |
| **Raw ANN Recall** | Lower (quantization loss) | Good | Excellent |
| **Recall with Rerank** | Good (default rerank=true) | Good | Excellent |
| **Query Latency** | Fast (compact codes) | Fast | Consistent |
| **Memory Overhead** | Lowest | Medium | Highest |
| **Mutable Segments** | No (exact fallback) | No (exact fallback) | Yes (in-memory graph) |
| **Distance Functions** | L2, L1, COSINE, IP, DP | L2, COSINE, IP, DP | All supported |
| **Use Case** | Very large datasets, memory/disk-constrained | Large-scale similarity search | High-accuracy retrieval, realtime ingestion |

### When to Use IVF_PQ

**IVF_PQ is a good fit when**:
* Your corpus is very large (millions to billions of vectors)
* Memory and disk space are constrained
* You can tolerate approximate distances (mitigated by default exact rerank)
* You need >0.8 recall with exact reranking enabled
* You're building indexes offline on single machines

**IVF_PQ is not ideal when**:
* Your corpus is small (<100K vectors), where IVF_FLAT or exact scan is simpler
* You need >0.95 raw ANN recall without reranking
* You require realtime mutable segments (use HNSW instead)
* Query latency is extremely latency-sensitive and rerank overhead is unacceptable

### Explain Plan Output

When running `EXPLAIN PLAN` with `explainAskingServers=true`, IVF_PQ queries include detailed runtime information:

```sql
SET explainAskingServers=true;
SET vectorNprobe=16;
EXPLAIN PLAN FOR
SELECT l2Distance(embedding, ARRAY[...]) AS dist
FROM myTable
WHERE vectorSimilarity(embedding, ARRAY[...], 10)
ORDER BY dist ASC LIMIT 10;
```

The explain output includes:
* **backend**: `IVF_PQ`
* **distanceFunction**: Configured distance metric (e.g., `EUCLIDEAN`)
* **nprobe**: Effective number of inverted lists probed (respects `vectorNprobe` setting)
* **exactRerank**: Whether exact reranking is enabled (default `true` for IVF_PQ)
* **candidateCount**: Number of ANN candidates examined from index before rerank
* **fallbackReason**: Present when a segment falls back to exact scan (e.g., `ivf_pq_index_unavailable` for realtime segments)

### Index Debug Information

All vector backends (including IVF_PQ) support the `getIndexDebugInfo()` method via the REST API:

```
GET /tables/{tableName}/segments/{segmentName}/metadata
```

For IVF_PQ, debug info includes:
* **Index configuration**: Exact parameters used (nlist, pqM, pqNbits, trainSampleSize)
* **Dimension and vector count**: Total vectors in the index
* **Per-list cardinality**: Distribution of vectors across clusters (for imbalance diagnosis)
* **Effective nprobe**: Recommended nprobe value for balanced recall/latency
* **Compression metrics**: Codebook size, quantization error statistics

### Explain Plan Output

When `explainAskingServers=true`, the explain output for vector queries includes:

* **backend**: Which vector index backend is used (`HNSW`, `IVF_FLAT`, or `IVF_PQ`)
* **distanceFunction**: The configured distance metric
* **nprobe**: Effective number of inverted lists probed (IVF_FLAT and IVF_PQ only)
* **exactRerank**: Whether exact reranking is enabled
* **candidateCount**: Number of ANN candidates examined
* **fallbackReason**: Present when a segment falls back to exact scan (e.g., `ivf_pq_index_unavailable` for realtime segments)

```sql
SET explainAskingServers=true;
SET vectorNprobe=8;
EXPLAIN PLAN FOR
SELECT l2Distance(embedding, ARRAY[1.1, 1.1, ...]) AS dist
FROM myTable
WHERE vectorSimilarity(embedding, ARRAY[1.1, 1.1, ...], 10)
ORDER BY dist ASC LIMIT 10
```

## Index Debug Information

All vector index backends (HNSW, IVF_FLAT, and IVF_PQ) now support the `getIndexDebugInfo()` method, which provides detailed statistics and diagnostic information about the index. This is useful for monitoring, debugging, and understanding index behavior at runtime.

### Using getIndexDebugInfo()

The debug info is available through the Pinot segment metadata and includes:

* **Index configuration**: The exact parameters used to build the index
* **Index statistics**: Number of vectors indexed, memory usage, codebook information (for IVF_PQ)
* **Build time**: Time taken to construct the index
* **Backend-specific metrics**:
  * HNSW: Graph structure info (number of nodes, edges, layers)
  * IVF_FLAT: Cluster distribution and inverted list statistics
  * IVF_PQ: Quantization codebook details, compression metrics

### Accessing Debug Information

Debug information can be accessed through:

1. **Query explain output**: When running with `explainAskingServers=true`, segment-level index debug info is included
2. **REST API**: Via the segment metadata endpoint
3. **Pinot shell/client**: Using server-side utilities

Example REST endpoint:
```
GET /tables/{tableName}/segments/{segmentName}/metadata
```

This endpoint returns detailed segment metadata including vector index debug information.

## Backward Compatibility

Existing HNSW and IVF_FLAT configurations continue to work without modification. The vector index implementation is fully backward compatible:

* Existing tables with HNSW or IVF_FLAT indexes will continue to function as before
* All three backends (HNSW, IVF_FLAT, IVF_PQ) can coexist in the same Pinot cluster
* You can migrate individual tables between backends by updating the table configuration and reindexing

## Limitations

- Supported vector index types: HNSW, IVF_FLAT, and IVF_PQ.
- **Mutable segment support**: Only HNSW supports mutable (realtime) segments. IVF_FLAT and IVF_PQ do not support mutable segments; realtime segments fall back to an exact forward-index scan.
- The column must be a multi-valued FLOAT column.
- Maximum vector dimension is 2048 (configurable via the `maxDimensions` property for HNSW).
- When Pinot uses a vector index, `VECTOR_SIMILARITY` is an approximate nearest-neighbor predicate. `vectorExactRerank=true` only re-scores the ANN candidates returned by the index; it does not guarantee a full exact search. When a segment has no vector index, Pinot falls back to an exact forward-index scan for that segment.
- HNSW uses Lucene under the hood and generates Lucene index files per segment.
- IVF_PQ raw ANN recall is lower than IVF_FLAT and HNSW due to quantization; enable `vectorExactRerank=true` (the default for IVF_PQ) for better accuracy.

### **Query**

```sql
SELECT ProductId, 
       UserId, 
       l2_distance(embedding, ARRAY[-0.0013143676, -0.011042999, ...]) AS l2_dist, 
       n_tokens, 
       combined
FROM fineFoodReviews
WHERE VECTOR_SIMILARITY(embedding, ARRAY[-0.0013143676, -0.011042999, ...], 5)  
ORDER BY l2_dist ASC 
LIMIT 10;
```

**`VECTOR_SIMILARITY`**:

A predicate that retrieves the top k closest vectors to the query vector.

Inputs:

* embedding: The vector column.
* Query vector (literal array).
* Optional topK parameter (default: 10).


## Query Execution Modes and Options

For advanced vector query execution strategies, including filtered ANN, threshold search, and execution mode selection, see [Vector Query Execution Semantics](../querying-and-sql/vector-query-execution.md).

### Key Query Options

- **`vectorDistanceThreshold`**: Return all results within a specified distance rather than top-K
- **`vectorExactRerank`**: Re-rank ANN candidates using exact distance from forward index (improves accuracy, enabled by default for IVF_PQ)
- **`vectorNprobe`**: Control recall-vs-latency tradeoff for IVF_FLAT and IVF_PQ by adjusting cluster probe count
- **`vectorMaxCandidates`**: Limit how many ANN candidates to examine before exact reranking

### Filtered ANN Queries

Pinot automatically optimizes queries combining `VECTOR_SIMILARITY` with metadata filters:

```sql
SELECT ProductId, Summary,
       cosineDistance(embedding, ARRAY[0.1, 0.2, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.1, 0.2, ...], 50)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 10;
```

The vector index handles the ANN candidate retrieval, and metadata filters are applied to the result set. For best accuracy with approximate indexes, enable `vectorExactRerank = true`.

### Viewing Query Execution Plans

Use `EXPLAIN` with `explainAskingServers=true` to see which execution mode Pinot selected (one of: ANN_TOP_K, ANN_TOP_K_WITH_RERANK, ANN_THEN_FILTER, ANN_THEN_FILTER_THEN_RERANK, ANN_THRESHOLD_SCAN, ANN_THRESHOLD_THEN_FILTER, or EXACT_SCAN). The EXPLAIN output also shows the vector backend, distance function, and any fallback reasons.

See [Vector Query Execution Semantics](../querying-and-sql/vector-query-execution.md) for detailed documentation on all execution modes and query patterns.
