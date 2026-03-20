# Vector / Similarity Functions

Pinot provides built-in vector similarity and utility functions for working with float array columns. These functions are useful for nearest-neighbor search, recommendation systems, and any use case involving embedding vectors.

Both input vectors must have the same number of dimensions. Passing `null` or mismatched-length vectors will result in an error.

## cosineDistance

```sql
cosineDistance(vector1, vector2)
cosineDistance(vector1, vector2, defaultValue)
```

Returns the cosine distance between two vectors, defined as `1 - cosine_similarity`. The result ranges from 0 (identical direction) to 2 (opposite direction). If either vector has a norm of zero, the two-argument form returns `NaN` while the three-argument form returns the specified `defaultValue`.

```sql
SELECT cosineDistance(
  embedding,
  ARRAY(0.1, 0.2, 0.3),
  0.0
)
FROM products
WHERE category = 'electronics'
-- Returns 0.0 for identical vectors, up to 2.0 for opposite vectors
```

## innerProduct

```sql
innerProduct(vector1, vector2)
```

Returns the inner product (sum of element-wise products) of two vectors.

```sql
SELECT productName,
       innerProduct(embedding, ARRAY(0.5, 0.5, 0.5)) AS score
FROM products
ORDER BY score DESC
LIMIT 10
```

## l1Distance

```sql
l1Distance(vector1, vector2)
```

Returns the L1 distance (Manhattan distance) between two vectors, computed as the sum of absolute differences of their components.

```sql
SELECT l1Distance(
  userEmbedding,
  ARRAY(1.0, 2.0, 3.0)
) AS manhattan_dist
FROM users
LIMIT 10
```

## l2Distance

```sql
l2Distance(vector1, vector2)
```

Returns the L2 distance (Euclidean distance with square root) between two vectors.

```sql
SELECT l2Distance(
  embedding,
  ARRAY(0.1, 0.2, 0.3)
) AS dist
FROM products
ORDER BY dist ASC
LIMIT 5
```

## euclideanDistance

```sql
euclideanDistance(vector1, vector2)
```

Returns the squared Euclidean distance between two vectors (the sum of squared differences without taking the square root). This is faster than `l2Distance` when you only need to compare relative distances.

```sql
SELECT euclideanDistance(
  embedding,
  ARRAY(0.1, 0.2, 0.3)
) AS squared_dist
FROM products
ORDER BY squared_dist ASC
LIMIT 5
```

## dotProduct

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

## vectorDims

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

## vectorNorm

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
