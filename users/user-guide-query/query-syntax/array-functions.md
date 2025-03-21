# Array Functions

Pinot provides scalar functions for array manipulation. Functions support operations on integer, long, float, double, and string arrays.

***

### 1. Array Reversal

#### arrayReverseInt

**Description**: Returns reversed integer array\
**Syntax**: `arrayReverseInt(int_array)`

```sql
SELECT arrayReverseInt([1, 2, 3, 4, 5]) AS reversed_array;
-- Result: [5, 4, 3, 2, 1]
```

#### arrayReverseString

**Description**: Returns reversed string array\
**Syntax**: `arrayReverseString(string_array)`

```sql
SELECT arrayReverseString(['apple', 'banana', 'cherry']) 
-- Result: ['cherry', 'banana', 'apple']
```

***

### 2. Array Sorting

#### arraySortInt

**Description**: Returns sorted integer array (ascending)\
**Syntax**: `arraySortInt(int_array)`

```sql
SELECT arraySortInt([4, 1, 3, 5, 2])
-- Result: [1, 2, 3, 4, 5]
```

#### arraySortString

**Description**: Returns lexicographically sorted string array\
**Syntax**: `arraySortString(string_array)`

```sql
SELECT arraySortString(['banana', 'apple', 'cherry'])
-- Result: ['apple', 'banana', 'cherry']
```

***

### 3. Array Index Operations

#### arrayIndexOfInt

**Description**: Returns first occurrence index (0-based)\
**Syntax**: `arrayIndexOfInt(int_array, value)`

```sql
SELECT arrayIndexOfInt([10, 20, 3, 40], 3)
-- Result: 2
```

_Similar functions exist for:_

* `arrayIndexOfString`

#### arrayIndexesOfInt

**Description**: Returns all occurrence indices\
**Syntax**: `arrayIndexesOfInt(int_array, value)`

```sql
SELECT arrayIndexesOfInt([5, 1, 5, 2, 5], 5)
-- Result: [0, 2, 4]
```

_Similar functions exist for:_

* `arrayIndexesOfLong`
* `arrayIndexesOfFloat`
* `arrayIndexesOfDouble`
* `arrayIndexesOfString`

***

### 4. Array Intersection

#### intersectIndices

**Description**: Returns common indices from sorted arrays\
**Syntax**: `intersectIndices(array1, array2)`

```sql
SELECT intersectIndices(
    arrayIndexesOfString(col1, 'b'),
    arrayIndexesOfString(col2, 'd')
) 
-- Sample Input: 
-- col1 = ['a','b','a','b'], col2 = ['c','d','d','c']
-- Result: [1]
```

***

### 5. Array Membership Checks

#### arrayContainsInt

**Description**: Checks array membership\
**Syntax**: `arrayContainsInt(array, value)`

```sql
SELECT arrayContainsInt([3, 7, 9], 7)
-- Result: true
```

#### arrayContainsString

**Description**: Checks string array membership\
**Syntax**: `arrayContainsString(array, value)`

```sql
SELECT arrayContainsString(['banana', 'apple'], 'apple')
-- Result: true
```

***

### 6. Array Slicing

#### arraySliceInt

**Description**: Extracts subarray \[start, end)\
**Syntax**: `arraySliceInt(array, start, end)`

```sql
SELECT arraySliceInt([10, 20, 30, 40], 1, 3)
-- Result: [20, 30]
```

#### arraySliceString

**Description**: Extracts string subarray\
**Syntax**: `arraySliceString(array, start, end)`

```sql
SELECT arraySliceString(['a','b','c','d'], 0, 2)
-- Result: ['a', 'b']
```

***

### 7. Distinct Elements

#### arrayDistinctInt

**Description**: Returns unique integers\
**Syntax**: `arrayDistinctInt(array)`

```sql
SELECT arrayDistinctInt([1, 2, 2, 3, 1])
-- Result: [1, 2, 3]
```

#### arrayDistinctString

**Description**: Returns unique strings\
**Syntax**: `arrayDistinctString(array)`

```sql
SELECT arrayDistinctString(['apple','banana','apple'])
-- Result: ['apple', 'banana']
```

***

### 8. Element Removal

#### arrayRemoveInt

**Description**: Removes first occurrence\
**Syntax**: `arrayRemoveInt(array, value)`

```sql
SELECT arrayRemoveInt([2, 4, 2, 6], 2)
-- Result: [4, 2, 6]
```

#### arrayRemoveString

**Description**: Removes first string occurrence\
**Syntax**: `arrayRemoveString(array, value)`

```sql
SELECT arrayRemoveString(['apple','banana','cherry'], 'banana')
-- Result: ['apple', 'cherry']
```

***

### 9. Array Union

#### arrayUnionInt

**Description**: Combines unique elements\
**Syntax**: `arrayUnionInt(array1, array2)`

```sql
SELECT arrayUnionInt([1,2,3], [3,4,5])
-- Result: [1, 2, 3, 4, 5]
```

#### arrayUnionString

**Description**: Combines unique strings\
**Syntax**: `arrayUnionString(array1, array2)`

```sql
SELECT arrayUnionString(['a','b'], ['b','c'])
-- Result: ['a', 'b', 'c']
```

***

### 10. Array Concatenation

#### arrayConcatInt

**Description**: Concatenates arrays\
**Syntax**: `arrayConcatInt(array1, array2)`

```sql
SELECT arrayConcatInt([1,2], [3,4])
-- Result: [1, 2, 3, 4]
```

_Similar functions:_

* `arrayConcatLong`
* `arrayConcatFloat`
* `arrayConcatDouble`
* `arrayConcatString`

***

### 11. Element Access

#### arrayElementAtInt

**Description**: 1-indexed element access\
**Syntax**: `arrayElementAtInt(array, index)`

```sql
SELECT arrayElementAtInt([10,20,30], 2)
-- Result: 20
```

_Similar functions:_

* `arrayElementAtLong`
* `arrayElementAtFloat`
* `arrayElementAtDouble`
* `arrayElementAtString`

***

### 12. Array Summation

#### arraySumInt

**Description**: Sums array elements\
**Syntax**: `arraySumInt(array)`

```sql
SELECT arraySumInt([1,2,3,4])
-- Result: 10
```

#### arraySumLong

**Description**: Sums long array elements\
**Syntax**: `arraySumLong(array)`

```sql
SELECT arraySumLong([100,200,300])
-- Result: 600
```

***

### 13. Array Construction

#### arrayValueConstructor

**Description**: Creates array from elements\
**Syntax**: `array(element1, element2, ...)`

```sql
SELECT array(1,2,3), array('a','b','c')
-- Results: 
-- [1,2,3], ['a','b','c']
```

***

### 14. Sequence Generation

#### generateIntArray

**Description**: Generates integer sequence\
**Syntax**: `generateIntArray(start, end, increment)`

```sql
SELECT generateIntArray(1, 10, 2)
-- Result: [1,3,5,7,9]
```

_Similar functions:_

* `generateLongArray`
* `generateFloatArray`
* `generateDoubleArray`

***

### 15. String Conversion

#### arrayToString

**Description**: Joins elements with delimiter\
**Syntax**: `arrayToString(array, delimiter[, nullPlaceholder])`

```sql
SELECT 
    arrayToString(['red','green','blue'], ','),
    arrayToString(['foo',null,'bar'], ',', 'NULL')
-- Results:
-- "red,green,blue", "foo,NULL,bar"
```

