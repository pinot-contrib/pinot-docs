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

Specifies the type of vector index to use. Currently supports HNSW.

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

IVF_FLAT supports query-time parameters to fine-tune the accuracy-performance trade-off:

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

* **vectorNprobe**: Number of inverted file lists to probe. Higher values increase recall at the cost of more computation. Start with nlist/4 and adjust based on query performance.
* **vectorExactRerank**: When enabled, candidate vectors are re-ranked using exact distance computation for improved accuracy. Recommended when recall is critical.
* **vectorMaxCandidates**: Maximum number of vectors to examine during candidate generation. Useful for controlling query latency.

### IVF_FLAT vs HNSW

| Aspect | IVF_FLAT | HNSW |
| --- | --- | --- |
| **Index Build Speed** | Fast | Slower |
| **Memory Overhead** | Lower | Higher (maintains graph structure) |
| **Recall** | Good with proper tuning | Excellent |
| **Query Latency** | Faster (with vectorNprobe tuning) | Consistent |
| **Use Case** | Large-scale similarity search, memory-constrained | High-accuracy retrieval |

## Backward Compatibility

Existing HNSW configurations continue to work without modification. The vector index implementation is fully backward compatible:

* Existing tables with HNSW indexes will continue to function as before
* Both HNSW and IVF_FLAT can coexist in the same Pinot cluster
* You can migrate individual tables from HNSW to IVF_FLAT by updating the table configuration and reindexing

## Limitations

- Supported vector index types: HNSW and IVF_FLAT. IVF_FLAT does not support mutable segments in phase 1; segments must be immutable.
- The column must be a multi-valued FLOAT column.
- Maximum vector dimension is 2048 (configurable via the `maxDimensions` property for HNSW).
- `VECTOR_SIMILARITY` is an approximate nearest-neighbor predicate; results are not exact unless `vectorExactRerank=true` is set.
- HNSW uses Lucene under the hood and generates Lucene index files per segment.
- IVF_FLAT does not support online index updates; segments must be immutable.

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

