# Vector index

## Overview

Apache Pinot now supports a Vector Index for efficient similarity searches over high-dimensional vector embeddings. This feature introduces the capability to store and query float array columns (multi-valued) using a vector similarity algorithm.

## When to use

Use the vector index when you need to find the most similar items in a high-dimensional vector space. Common use cases include semantic search, recommendation systems, image similarity, and retrieval-augmented generation (RAG) where text embeddings are stored alongside metadata.

## Supported column types

The vector index is supported on multi-valued FLOAT columns (float arrays). The column must be declared as `singleValueField: false` in the schema with `dataType: FLOAT`.

## Key Features

* Vector Index is implemented using HNSW (Hierarchical Navigable Small World) for approximate nearest neighbor (ANN) search.
* Adds support for a predicate and function:
  * VECTOR\_SIMILARITY(v1, v2, \[optional topK]) to retrieve the topK closest vectors based on similarity.
  * The similarity function can be used as part of a query to filter and rank results.

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

## Limitations

- Only HNSW is supported as the vector index type.
- The column must be a multi-valued FLOAT column.
- Maximum vector dimension is 2048 (configurable via the `maxDimensions` property).
- `VECTOR_SIMILARITY` is an approximate nearest-neighbor predicate; results are not exact.
- The vector index uses Lucene under the hood and generates Lucene index files per segment.

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

