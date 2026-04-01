# Vector / Similarity Functions

Pinot provides built-in vector similarity and utility functions for working with float array columns. These functions support nearest-neighbor search, recommendation systems, retrieval-augmented generation (RAG), and any use case involving embedding vectors.

Both input vectors must have the same number of dimensions. Passing `null` or mismatched-length vectors results in an error.

{% hint style="info" %}
To accelerate vector search queries with approximate nearest-neighbor (ANN) lookup, configure a [vector index](../../basics/indexing/vector-index.md) on your float array column and use the `VECTOR_SIMILARITY` predicate described below.
{% endhint %}

## VECTOR\_SIMILARITY

`VECTOR_SIMILARITY` is a **WHERE-clause predicate** that performs approximate nearest-neighbor (ANN) search using a vector index. It is not a standalone function—it acts as a filter that returns the top-K documents whose vectors are closest to the given query vector.

### Syntax

```sql
WHERE VECTOR_SIMILARITY(vectorColumn, queryVector, topK)
```

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`vectorColumn`</td>
      <td>identifier</td>
      <td>A multi-valued FLOAT column with a [vector index](../../basics/indexing/vector-index.md) configured.</td>
    </tr>
    <tr>
      <td>`queryVector`</td>
      <td>`ARRAY[...]`</td>
      <td>A float array literal representing the query embedding.</td>
    </tr>
    <tr>
      <td>`topK`</td>
      <td>integer literal</td>
      <td>Number of nearest neighbors to retrieve. Defaults to `10` if omitted.</td>
    </tr>
  </tbody>
</table>

### Prerequisites

`VECTOR_SIMILARITY` requires a vector index on the target column. Without a vector index the predicate will fail. See the [vector index documentation](../../basics/indexing/vector-index.md) for setup instructions.

**Minimal field config:**

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

### Examples

**Find the 5 nearest products to a query embedding and rank by cosine distance:**

```sql
SELECT ProductId,
       cosineDistance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM products
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 5)
ORDER BY dist ASC
LIMIT 5
```

**Combine with metadata filters — retrieve 20 ANN candidates and then filter by category:**

```sql
SELECT ProductId, Summary,
       l2Distance(embedding, ARRAY[0.12, 0.34, 0.56, ...]) AS dist
FROM fineFoodReviews
WHERE VECTOR_SIMILARITY(embedding, ARRAY[0.12, 0.34, 0.56, ...], 20)
  AND category = 'electronics'
ORDER BY dist ASC
LIMIT 10
```

{% hint style="warning" %}
`VECTOR_SIMILARITY` is an **approximate** nearest-neighbor predicate. Results may not be identical to an exact brute-force scan. To get better recall, request a larger `topK` than the final `LIMIT` and combine with an `ORDER BY` on a distance function.
{% endhint %}

## Distance Functions

### cosineDistance

```sql
cosineDistance(vector1, vector2)
cosineDistance(vector1, vector2, defaultValue)
```

Returns the cosine distance between two vectors, defined as `1 - cosine_similarity`. The result ranges from `0` (identical direction) to `2` (opposite direction).

If either vector has a norm of zero, the two-argument form returns `NaN` while the three-argument form returns the specified `defaultValue`.

```sql
SELECT cosineDistance(
  embedding,
  ARRAY[0.1, 0.2, 0.3],
  0.0
) AS dist
FROM products
WHERE category = 'electronics'
ORDER BY dist ASC
LIMIT 10
-- Returns 0.0 for identical vectors, up to 2.0 for opposite vectors
```

### innerProduct

```sql
innerProduct(vector1, vector2)
```

Returns the inner product (sum of element-wise products) of two vectors. Useful when embeddings are pre-normalized and higher scores indicate greater similarity.

```sql
SELECT ProductId,
       innerProduct(embedding, ARRAY[0.5, 0.5, 0.5]) AS score
FROM products
ORDER BY score DESC
LIMIT 10
```

### l1Distance

```sql
l1Distance(vector1, vector2)
```

Returns the L1 distance (Manhattan distance) between two vectors, computed as the sum of absolute differences of their components.

```sql
SELECT l1Distance(
  userEmbedding,
  ARRAY[1.0, 2.0, 3.0]
) AS manhattan_dist
FROM users
ORDER BY manhattan_dist ASC
LIMIT 10
```

### l2Distance

```sql
l2Distance(vector1, vector2)
```

Returns the L2 distance (Euclidean distance) between two vectors, computed as the square root of the sum of squared differences.

```sql
SELECT l2Distance(
  embedding,
  ARRAY[0.1, 0.2, 0.3]
) AS dist
FROM products
ORDER BY dist ASC
LIMIT 5
```

### euclideanDistance

```sql
euclideanDistance(vector1, vector2)
```

Returns the **squared** Euclidean distance between two vectors (the sum of squared differences without the square root). This is computationally cheaper than `l2Distance` when you only need to compare relative distances, since omitting the square root preserves the ordering.

```sql
SELECT euclideanDistance(
  embedding,
  ARRAY[0.1, 0.2, 0.3]
) AS squared_dist
FROM products
ORDER BY squared_dist ASC
LIMIT 5
```

### dotProduct

```sql
dotProduct(vector1, vector2)
```

Returns the dot product of two vectors. Functionally equivalent to `innerProduct`.

```sql
SELECT dotProduct(
  queryEmbedding,
  docEmbedding
) AS relevance
FROM documents
ORDER BY relevance DESC
LIMIT 10
```

## Utility Functions

### vectorDims

```sql
vectorDims(vector)
```

Returns the number of dimensions (length) of a vector.

```sql
SELECT vectorDims(embedding) AS dims
FROM products
LIMIT 1
-- Returns 128 for a 128-dimensional embedding
```

### vectorNorm

```sql
vectorNorm(vector)
```

Returns the L2 norm (Euclidean length) of a vector, computed as the square root of the sum of squared components.

```sql
SELECT vectorNorm(embedding) AS norm
FROM products
LIMIT 5
-- Returns the magnitude of each embedding vector
```

## End-to-End Example: Semantic Search

This example walks through setting up a table for semantic search over product reviews, from schema definition to querying.

### 1. Define the schema

The embedding column must be a multi-valued FLOAT field:

```json
{
  "schemaName": "fineFoodReviews",
  "dimensionFieldSpecs": [
    { "name": "ProductId", "dataType": "STRING" },
    { "name": "UserId", "dataType": "STRING" },
    { "name": "Score", "dataType": "INT" },
    { "name": "Summary", "dataType": "STRING" },
    { "name": "Text", "dataType": "STRING" },
    {
      "name": "embedding",
      "dataType": "FLOAT",
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
  ]
}
```

### 2. Configure the table with a vector index

Enable the HNSW vector index on the `embedding` column. Choose a distance function that matches how your embeddings were produced—`COSINE` is the most common choice for normalized text embeddings.

```json
{
  "tableName": "fineFoodReviews_OFFLINE",
  "tableType": "OFFLINE",
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

### 3. Query with vector similarity

Use `VECTOR_SIMILARITY` to retrieve nearest neighbors and a distance function to rank results:

```sql
SELECT ProductId,
       UserId,
       Summary,
       cosineDistance(embedding, ARRAY[-0.0013, -0.0110, 0.0247, ...]) AS dist
FROM fineFoodReviews
WHERE VECTOR_SIMILARITY(embedding, ARRAY[-0.0013, -0.0110, 0.0247, ...], 10)
ORDER BY dist ASC
LIMIT 5
```

This query first uses the HNSW index to retrieve the 10 approximate nearest neighbors, then orders those candidates by exact cosine distance and returns the top 5.

## Function Summary

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Return type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`VECTOR_SIMILARITY(col, query, topK)`</td>
      <td>predicate</td>
      <td>ANN filter — requires a vector index.</td>
    </tr>
    <tr>
      <td>`cosineDistance(v1, v2 [, default])`</td>
      <td>`DOUBLE`</td>
      <td>Cosine distance (`1 - cosine_similarity`).</td>
    </tr>
    <tr>
      <td>`innerProduct(v1, v2)`</td>
      <td>`DOUBLE`</td>
      <td>Inner product (sum of element-wise products).</td>
    </tr>
    <tr>
      <td>`l1Distance(v1, v2)`</td>
      <td>`DOUBLE`</td>
      <td>Manhattan distance.</td>
    </tr>
    <tr>
      <td>`l2Distance(v1, v2)`</td>
      <td>`DOUBLE`</td>
      <td>Euclidean distance (with square root).</td>
    </tr>
    <tr>
      <td>`euclideanDistance(v1, v2)`</td>
      <td>`DOUBLE`</td>
      <td>Squared Euclidean distance (no square root).</td>
    </tr>
    <tr>
      <td>`dotProduct(v1, v2)`</td>
      <td>`DOUBLE`</td>
      <td>Dot product (equivalent to `innerProduct`).</td>
    </tr>
    <tr>
      <td>`vectorDims(v)`</td>
      <td>`INT`</td>
      <td>Number of vector dimensions.</td>
    </tr>
    <tr>
      <td>`vectorNorm(v)`</td>
      <td>`DOUBLE`</td>
      <td>L2 norm (magnitude) of a vector.</td>
    </tr>
  </tbody>
</table>
