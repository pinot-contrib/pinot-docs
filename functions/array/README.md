# Array Functions

***

## Array Aggregation

### arrayAgg

#### **Description**:

Concatenates the input values into an array. Optionally removes duplicates when isDistinct is set to true. This function is commonly used to aggregate multiple rows into a single array grouped by a dimension.

#### **Signature**:

```sql
ARRAY_AGG(dataColumn, 'dataType' [, isDistinct])
```

#### **Arguments**:

* dataColumn - The input column or expression to aggregate. Can be a scalar or an array type.
* 'dataType' - The element type of the resulting array. Must be a string literal (e.g., 'STRING', 'INT', 'LONG', 'DOUBLE').
* isDistinct _(optional) -_ Boolean flag to include only distinct elements. Defaults to false.

#### **Returns**:

An array of the specified dataType containing all aggregated values.

#### Example:

1. Aggregate scalar values into an array

```sql
SELECT ARRAY_AGG(firstName, 'STRING', true) AS firstNames
FROM transcript;
```

**Results**:

```sql
firstNames
-----------
["Bob", "Nick", "Lucy"]
```

2. Aggregate array values across rows

```sql
SELECT ARRAY_AGG(tags, 'STRING') AS allTags
FROM articles;
```

**Results**:

```sql
allTags
-------------------------------------
["news", "ai", "pinot", "open-source"]
```

#### Notes:

* When the input column is an array, all sub-arrays are flattened before aggregation.
* When isDistinct is true, duplicate elements are removed from the final array.
* The order of elements in the output array is not guaranteed.
* Supports both scalar and array input types for numeric and string data.

***

### LISTAGG

#### Description:

Concatenates the input values into a single string, with an optional delimiter.

Similar to ARRAY\_AGG, but produces a string instead of an array.

LISTAGG is useful for generating comma-separated lists or other delimited strings from multiple rows.

#### Signature:

```sql
LISTAGG(dataColumn [, delimiter] [, isDistinct])
```

#### Arguments:

* dataColumn — The input column or expression to concatenate.
* delimiter _(optional)_ — A string used to separate values in the output. Defaults to ','.
* isDistinct _(optional)_ — Boolean flag to include only distinct elements. Defaults to false.

#### Returns:

A single concatenated STRING containing all values (optionally distinct), separated by the given delimiter.

#### Examples:

1. Concatenate names with commas

```sql
SELECT LISTAGG(firstName, ', ', true) AS allNames
FROM transcript;
```

**Result**:

```sql
allNames
-------------------
Bob, Nick, Lucy
```

2. Concatenate array input

```sql
SELECT LISTAGG(tags, '|') AS tagList
FROM articles;
```

**Result**:

```sql
tagList
------------------------
news|ai|pinot|open-source
```

#### Notes:

* If the input column is an array, all sub-arrays are flattened before concatenation.
* When isDistinct is true, duplicate values are removed before joining.
* The output order of elements is not guaranteed.
* The delimiter argument is optional; default is a comma ','.

***

### sumArrayLong

#### Description:

Computes the sum of all elements in an array of LONG (or integer-compatible) values across all input rows.

This function is useful for aggregating numeric arrays, such as metrics or counters, into a single scalar value.

#### Signature:

```sql
sumArrayLong(arrayColumn)
```

#### Arguments:

* arrayColumn — Input column containing arrays of numeric (LONG or INT) values.

#### Returns:

A LONG representing the sum of all elements across all arrays in the group.

#### Examples:

1. Sum elements of arrays across rows

```sql
SELECT sumArrayLong(values) AS totalSum
FROM metrics;
```

**Input**:

```sql
values
-------
[1, 2, 3]
[4, 5, 6]
```

**Result**:

```sql
totalSum
---------
21
```

2. With GROUP BY

```sql
SELECT category, sumArrayLong(values) AS total
FROM metrics
GROUP BY category;
```

**Result**:

```sql
category | total
----------|------
A         | 15
B         | 27
```

#### Notes:

* NULL and empty arrays are ignored.
* All numeric values are coerced to LONG before summation.
* If any element is non-numeric, the query will fail.

***

### sumArrayDouble

#### Description:

Computes the sum of all elements in an array of DOUBLE (floating-point) values across all input rows.

This is the double-precision variant of sumArrayLong, and is typically used for aggregating numeric arrays with decimal values, such as scores, probabilities, or weights.

#### Signature:

```sql
sumArrayDouble(arrayColumn)
```

#### Arguments:

* arrayColumn — Input column containing arrays of numeric (DOUBLE or FLOAT) values.

#### Returns:

A DOUBLE representing the sum of all elements across all arrays in the group.

#### Examples:

1. Sum elements of arrays across rows

```sql
SELECT sumArrayDouble(weights) AS totalWeight
FROM model_output;
```

Input:

```sql
weights
------------
[1.2, 0.8]
[2.5, 3.0]
```

Result:

```sql
totalWeight
------------
7.5
```

2. With GROUP BY

```sql
SELECT experimentId, sumArrayDouble(scores) AS totalScore
FROM results
GROUP BY experimentId;
```

#### Notes:

* NULL and empty arrays are ignored.
* All numeric elements are coerced to DOUBLE before summation.
* Use sumArrayLong for integer data to avoid type conversion overhead.

***

## Array Filtering

### filterMv

Evaluates each element of a multi-value column against a predicate and returns a filtered multi-value array containing only elements that satisfy the condition.

**Signature**: `filterMv(mvColumn, 'predicate')`

**Supported Operators**: `=`, `!=`, `>`, `>=`, `<`, `<=`, `IN`, `NOT IN`, `BETWEEN`, `REGEXP_LIKE`, and logical operators `AND`, `OR`, `NOT`

**Example**:

```sql
SELECT filterMv(stringArrayCol, 'REGEXP_LIKE(v, ''^/api/.*'')')
FROM myTable
LIMIT 10
```

**Notes**:
* The predicate must use `v` as the placeholder for the element being evaluated.
* Useful for element-level filtering without requiring `CROSS JOIN UNNEST`.

For more details, see [filterMv](filtermv.md).



## Array Reversal

### arrayReverseInt

**Description**: Reverses the order of elements in an integer array.\
**Syntax**: `arrayReverseInt(int_array)`\
**Example**:

```sql
SELECT arrayReverseInt(ARRAY[1, 2, 3, 4, 5]);
-- Result: [5, 4, 3, 2, 1]
```

### arrayReverseString

**Description**: Reverses the order of elements in a string array.\
**Syntax**: `arrayReverseString(string_array)`\
**Example**:

```sql
SELECT arrayReverseString(ARRAY['apple', 'banana', 'cherry']);
-- Result: ['cherry', 'banana', 'apple']
```

***

## Array Sorting

### arraySortInt

**Description**: Sorts an integer array in ascending order.\
**Syntax**: `arraySortInt(int_array)`\
**Example**:

```sql
SELECT arraySortInt(ARRAY[4, 1, 3, 5, 2]);
-- Result: [1, 2, 3, 4, 5]
```

### arraySortString

**Description**: Sorts a string array lexicographically.\
**Syntax**: `arraySortString(string_array)`\
**Example**:

```sql
SELECT arraySortString(ARRAY['banana', 'apple', 'cherry']);
-- Result: ['apple', 'banana', 'cherry']
```

***

## Array Index Operations

### arrayIndexOfInt

**Description**: Returns the first 0-based index of an integer value.\
**Syntax**: `arrayIndexOfInt(int_array, value)`\
**Example**:

```sql
SELECT arrayIndexOfInt(ARRAY[10, 20, 3, 40], 3);
-- Result: 2
```

### arrayIndexOfString

**Description**: Returns the first 0-based index of a string value.\
**Syntax**: `arrayIndexOfString(string_array, value)`\
**Example**:

```sql
SELECT arrayIndexOfString(ARRAY['apple', 'banana', 'cherry'], 'cherry');
-- Result: 2
```

### arrayIndexesOfInt

**Description**: Returns all indices of an integer value.\
**Syntax**: `arrayIndexesOfInt(int_array, value)`\
**Example**:

```sql
SELECT arrayIndexesOfInt(ARRAY[5, 3, 5, 2, 5], 5);
-- Result: [0, 2, 4]
```

### arrayIndexesOfLong

**Description**: Returns all indices of a long value.\
**Syntax**: `arrayIndexesOfLong(long_array, value)`\
**Example**:

```sql
SELECT arrayIndexesOfLong(ARRAY[5000000000, 3000000000, 5000000000], 5000000000);
-- Result: [0, 2]
```

### arrayIndexesOfFloat

**Description**: Returns all indices of a float value.\
**Syntax**: `arrayIndexesOfFloat(float_array, value)`\
**Example**:

```sql
SELECT arrayIndexesOfFloat(ARRAY[1.5, 3.0, 1.5], 1.5);
-- Result: [0, 2]
```

### arrayIndexesOfDouble

**Description**: Returns all indices of a double value.\
**Syntax**: `arrayIndexesOfDouble(double_array, value)`\
**Example**:

```sql
SELECT arrayIndexesOfDouble(ARRAY[123.456, 789.012, 123.456], 123.456);
-- Result: [0, 2]
```

### arrayIndexesOfString

**Description**: Returns all indices of a string value.\
**Syntax**: `arrayIndexesOfString(string_array, value)`\
**Example**:

```sql
SELECT arrayIndexesOfString(ARRAY['a', 'b', 'a'], 'a');
-- Result: [0, 2]
```

***

## Array Intersection

### intersectIndices

**Description**: Returns common indices between two sorted integer arrays.\
**Syntax**: `intersectIndices(array1, array2)`\
**Example**:

```sql
SELECT intersectIndices(ARRAY[1, 3, 5], ARRAY[3, 5]);
-- Result: [3, 5]
```

***

### arraysOverlap

**Description**:&#x20;

Returns true if the two input arrays have at least one element in common, and false otherwise.

This function is useful for checking whether two arrays share any overlapping values — for example, to test whether a user’s assigned tags intersect with a set of filter tags.\


**Syntax**:&#x20;

&#x20;`arraysOverlap(array1, array2)`\


**Example**:

```sql
SELECT arraysOverlap(ARRAY[1, 3, 5], ARRAY[3, 5]);
-- Result: true
```

***

## Array Contains

### arrayContainsInt

**Description**: Checks if an integer array contains a value.\
**Syntax**: `arrayContainsInt(int_array, value)`\
**Example**:

```sql
SELECT arrayContainsInt(ARRAY[3, 7, 9], 7);
-- Result: true
```

### arrayContainsString

**Description**: Checks if a string array contains a value.\
**Syntax**: `arrayContainsString(string_array, value)`\
**Example**:

```sql
SELECT arrayContainsString(ARRAY['apple', 'banana'], 'apple');
-- Result: true
```

***

## Array Slicing

### arraySliceInt

**Description**: Extracts a subarray (start inclusive, end exclusive).\
**Syntax**: `arraySliceInt(int_array, start, end)`\
**Example**:

```sql
SELECT arraySliceInt(ARRAY[10, 20, 30, 40], 1, 3);
-- Result: [20, 30]
```

### arraySliceString

**Description**: Extracts a string subarray.\
**Syntax**: `arraySliceString(string_array, start, end)`\
**Example**:

```sql
SELECT arraySliceString(ARRAY['a', 'b', 'c', 'd'], 0, 2);
-- Result: ['a', 'b']
```

***

## Array Distinct

### arrayDistinctInt

**Description**: Removes duplicate integers.\
**Syntax**: `arrayDistinctInt(int_array)`\
**Example**:

```sql
SELECT arrayDistinctInt(ARRAY[1, 2, 2, 3, 1]);
-- Result: [1, 2, 3]
```

### arrayDistinctString

**Description**: Removes duplicate strings.\
**Syntax**: `arrayDistinctString(string_array)`\
**Example**:

```sql
SELECT arrayDistinctString(ARRAY['apple', 'banana', 'apple']);
-- Result: ['apple', 'banana']
```

***

## Array Remove

### arrayRemoveInt

**Description**: Removes the first occurrence of an integer.\
**Syntax**: `arrayRemoveInt(int_array, value)`\
**Example**:

```sql
SELECT arrayRemoveInt(ARRAY[2, 4, 2, 6], 2);
-- Result: [4, 2, 6]
```

### arrayRemoveString

**Description**: Removes the first occurrence of a string.\
**Syntax**: `arrayRemoveString(string_array, value)`\
**Example**:

```sql
SELECT arrayRemoveString(ARRAY['apple', 'banana', 'cherry'], 'banana');
-- Result: ['apple', 'cherry']
```

***

## Array Union

### arrayUnionInt

**Description**: Combines two integer arrays with unique values.\
**Syntax**: `arrayUnionInt(array1, array2)`\
**Example**:

```sql
SELECT arrayUnionInt(ARRAY[1, 2], ARRAY[2, 3]);
-- Result: [1, 2, 3]
```

### arrayUnionString

**Description**: Combines two string arrays with unique values.\
**Syntax**: `arrayUnionString(array1, array2)`\
**Example**:

```sql
SELECT arrayUnionString(ARRAY['a', 'b'], ARRAY['b', 'c']);
-- Result: ['a', 'b', 'c']
```

***

## Array Concatenation

### arrayConcatInt

**Description**: Concatenates two integer arrays.\
**Syntax**: `arrayConcatInt(array1, array2)`\
**Example**:

```sql
SELECT arrayConcatInt(ARRAY[1, 2], ARRAY[3, 4]);
-- Result: [1, 2, 3, 4]
```

### arrayConcatLong

**Description**: Concatenates two long arrays.\
**Syntax**: `arrayConcatLong(array1, array2)`\
**Example**:

```sql
SELECT arrayConcatLong(ARRAY[1000000000, 2000000000], ARRAY[3000000000]);
-- Result: [1000000000, 2000000000, 3000000000]
```

### arrayConcatFloat

**Description**: Concatenates two float arrays.\
**Syntax**: `arrayConcatFloat(array1, array2)`\
**Example**:

```sql
SELECT arrayConcatFloat(ARRAY[1.5, 2.0], ARRAY[3.5]);
-- Result: [1.5, 2.0, 3.5]
```

### arrayConcatDouble

**Description**: Concatenates two double arrays.\
**Syntax**: `arrayConcatDouble(array1, array2)`\
**Example**:

```sql
SELECT arrayConcatDouble(ARRAY[123.456], ARRAY[789.012]);
-- Result: [123.456, 789.012]
```

### arrayConcatString

**Description**: Concatenates two string arrays.\
**Syntax**: `arrayConcatString(array1, array2)`\
**Example**:

```sql
SELECT arrayConcatString(ARRAY['a', 'b'], ARRAY['c']);
-- Result: ['a', 'b', 'c']
```

***

## Array Element Access

### arrayElementAtInt

**Description**: Returns the 1-indexed integer element.\
**Syntax**: `arrayElementAtInt(array, index)`\
**Example**:

```sql
SELECT arrayElementAtInt(ARRAY[10, 20, 30], 2);
-- Result: 20
```

### arrayElementAtLong

**Description**: Returns the 1-indexed long element.\
**Syntax**: `arrayElementAtLong(array, index)`\
**Example**:

```sql
SELECT arrayElementAtLong(ARRAY[1000000000, 2000000000], 1);
-- Result: 1000000000
```

### arrayElementAtFloat

**Description**: Returns the 1-indexed float element.\
**Syntax**: `arrayElementAtFloat(array, index)`\
**Example**:

```sql
SELECT arrayElementAtFloat(ARRAY[1.5, 2.0], 2);
-- Result: 2.0
```

### arrayElementAtDouble

**Description**: Returns the 1-indexed double element.\
**Syntax**: `arrayElementAtDouble(array, index)`\
**Example**:

```sql
SELECT arrayElementAtDouble(ARRAY[123.456, 789.012], 1);
-- Result: 123.456
```

### arrayElementAtString

**Description**: Returns the 1-indexed string element.\
**Syntax**: `arrayElementAtString(array, index)`\
**Example**:

```sql
SELECT arrayElementAtString(ARRAY['alpha', 'beta', 'gamma'], 1);
-- Result: 'alpha'
```

***

## Array Summation

### arraySumInt

**Description**: Sums all integers in an array.\
**Syntax**: `arraySumInt(int_array)`\
**Example**:

```sql
SELECT arraySumInt(ARRAY[1, 2, 3, 4]);
-- Result: 10
```

### arraySumLong

**Description**: Sums all longs in an array.\
**Syntax**: `arraySumLong(long_array)`\
**Example**:

```sql
SELECT arraySumLong(ARRAY[1000000000, 2000000000]);
-- Result: 3000000000
```

***

## Array Construction

### arrayValueConstructor

**Description**: Constructs an array from elements.\
**Syntax**: `array(element1, element2, ...)`\
**Example**:

```sql
SELECT array(1, 2, 3) AS int_array, array('a', 'b') AS str_array;
-- Result:
-- int_array = [1, 2, 3]
-- str_array = ['a', 'b']
```

***

## Array Generation

### generateIntArray

**Description**: Generates an integer sequence.\
**Syntax**: `generateIntArray(start, end, increment)`\
**Example**:

```sql
SELECT generateIntArray(1, 5, 2);
-- Result: [1, 3, 5]
```

### generateLongArray

**Description**: Generates a long sequence.\
**Syntax**: `generateLongArray(start, end, increment)`\
**Example**:

```sql
SELECT generateLongArray(100, 300, 100);
-- Result: [100, 200, 300]
```

### generateFloatArray

**Description**: Generates a float sequence.\
**Syntax**: `generateFloatArray(start, end, increment)`\
**Example**:

```sql
SELECT generateFloatArray(0.5, 2.0, 0.5);
-- Result: [0.5, 1.0, 1.5, 2.0]
```

### generateDoubleArray

**Description**: Generates a double sequence.\
**Syntax**: `generateDoubleArray(start, end, increment)`\
**Example**:

```sql
SELECT generateDoubleArray(1.0, 2.5, 0.5);
-- Result: [1.0, 1.5, 2.0, 2.5]
```

***

## String Conversion

### arrayToString (2-argument)

**Description**: Joins elements with a delimiter.\
**Syntax**: `arrayToString(string_array, delimiter)`\
**Example**:

```sql
SELECT arrayToString(ARRAY['red', 'green', 'blue'], ',');
-- Result: 'red,green,blue'
```

### arrayToString (3-argument)

**Description**: Joins elements with null replacement.\
**Syntax**: `arrayToString(string_array, delimiter, nullString)`\
**Example**:

```sql
SELECT arrayToString(ARRAY['foo', NULL, 'bar'], '|', 'NA');
-- Result: 'foo|NA|bar'
```

## Additional Reference Pages

| Function | Function |
| --- | --- |
| [ARRAY_AGG](array_agg.md) | [arrayConcatDouble](arrayconcatdouble.md) |
| [arrayConcatFloat](arrayconcatfloat.md) | [arrayConcatInt](arrayconcatint.md) |
| [arrayConcatLong](arrayconcatlong.md) | [arrayConcatString](arrayconcatstring.md) |
| [arrayContainsInt](arraycontainsint.md) | [arrayContainsString](arraycontainsstring.md) |
| [arrayDistinctInt](arraydistinctint.md) | [arrayDistinctString](arraydistinctstring.md) |
| [arrayIndexOfInt](arrayindexofint.md) | [arrayIndexOfString](arrayindexofstring.md) |
| [ARRAYLENGTH](arraylength.md) | [arrayRemoveInt](arrayremoveint.md) |
| [arrayRemoveString](arrayremovestring.md) | [arrayReverseInt](arrayreverseint.md) |
| [arrayReverseString](arrayreversestring.md) | [arraySliceInt](arraysliceint.md) |
| [arraySliceString](arrayslicestring.md) | [arraySortInt](arraysortint.md) |
| [arraySortString](arraysortstring.md) | [arrayUnionInt](arrayunionint.md) |
| [arrayUnionString](arrayunionstring.md) | [isEqualSet](isequalset.md) |
