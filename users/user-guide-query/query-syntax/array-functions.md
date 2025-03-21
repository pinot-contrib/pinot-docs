# Array Functions

### `arrayReverseInt`

Reverses the order of elements in an integer array. Returns a new array; original remains unmodified.

**Parameters:**

* `values` (INT ARRAY): Integer array to reverse

**Returns:**\
INT ARRAY

**Example:**

```sql
arrayReverseInt(ARRAY[1, 2, 3]) → ARRAY[3, 2, 1]
```

***

### `arrayReverseString`

Reverses the order of elements in a string array.

**Parameters:**

* `values` (STRING ARRAY): String array to reverse

**Returns:**\
STRING ARRAY

**Example:**

```sql
arrayReverseString(ARRAY['a', 'b', 'c']) → ARRAY['c', 'b', 'a']
```

***

### `arraySortInt`

Sorts an integer array in ascending order. Returns a new sorted array.

**Parameters:**

* `values` (INT ARRAY): Integer array to sort

**Returns:**\
INT ARRAY

**Example:**

```sql
arraySortInt(ARRAY[3, 1, 2]) → ARRAY[1, 2, 3]
```

***

### `arraySortString`

Sorts a string array lexicographically.

**Parameters:**

* `values` (STRING ARRAY): String array to sort

**Returns:**\
STRING ARRAY

**Example:**

```sql
arraySortString(ARRAY['banana', 'apple']) → ARRAY['apple', 'banana']
```

***

### `arrayIndexOfInt`

Returns the first 0-based index of a value in an integer array. Returns `-1` if not found.

**Parameters:**

* `values` (INT ARRAY): Array to search
* `valueToFind` (INT): Value to locate

**Returns:**\
INT

**Example:**

```sql
arrayIndexOfInt(ARRAY[10, 20, 30], 20) → 1
```

***

### `arrayIndexOfString`

Finds the first index of a string in a string array.

**Parameters:**

* `values` (STRING ARRAY): Array to search
* `valueToFind` (STRING): Value to locate

**Returns:**\
INT

**Example:**

```sql
arrayIndexOfString(ARRAY['a', 'b'], 'b') → 1
```

***

### `arrayIndexesOfInt`

Returns all 0-based indices where a value appears in an integer array.

**Parameters:**

* `values` (INT ARRAY): Array to search
* `valueToFind` (INT): Value to locate

**Returns:**\
INT ARRAY

**Example:**

```sql
arrayIndexesOfInt(ARRAY[5, 3, 5], 5) → ARRAY[0, 2]
```

***

### `intersectIndices`

Finds common indices between two sorted arrays. Used for multi-column queries.

**Parameters:**

* `values1` (INT ARRAY): First sorted index array
* `values2` (INT ARRAY): Second sorted index array

**Returns:**\
INT ARRAY

**Example:**

```sql
intersectIndices(ARRAY[1, 3, 5], ARRAY[3, 5]) → ARRAY[3, 5]
```

***

### `arrayContainsInt`

Checks if a value exists in an integer array.

**Parameters:**

* `values` (INT ARRAY): Array to search
* `valueToFind` (INT): Value to check

**Returns:**\
BOOLEAN

**Example:**

```sql
arrayContainsInt(ARRAY[1, 2], 3) → false
```

***

### `arraySliceInt`

Extracts a subarray from `start` (inclusive) to `end` (exclusive).

**Parameters:**

* `values` (INT ARRAY): Array to slice
* `start` (INT): 0-based start index
* `end` (INT): 0-based end index

**Returns:**\
INT ARRAY

**Example:**

```sql
arraySliceInt(ARRAY[1, 2, 3, 4], 1, 3) → ARRAY[2, 3]
```

***

### `arrayDistinctInt`

Returns unique elements preserving first occurrence order.

**Parameters:**

* `values` (INT ARRAY): Input array

**Returns:**\
INT ARRAY

**Example:**

```sql
arrayDistinctInt(ARRAY[3, 1, 3]) → ARRAY[3, 1]
```

***

### `arrayRemoveInt`

Removes the first occurrence of an element.

**Parameters:**

* `values` (INT ARRAY): Input array
* `element` (INT): Element to remove

**Returns:**\
INT ARRAY

**Example:**

```sql
arrayRemoveInt(ARRAY[5, 3, 7], 3) → ARRAY[5, 7]
```

***

### `arrayUnionInt`

Combines two arrays and returns distinct elements.

**Parameters:**

* `values1` (INT ARRAY): First array
* `values2` (INT ARRAY): Second array

**Returns:**\
INT ARRAY

**Example:**

```sql
arrayUnionInt(ARRAY[1, 2], ARRAY[2, 3]) → ARRAY[1, 2, 3]
```

***

### `arrayConcatInt`

Concatenates two integer arrays.

**Parameters:**

* `values1` (INT ARRAY): First array
* `values2` (INT ARRAY): Second array

**Returns:**\
INT ARRAY

**Example:**

```sql
arrayConcatInt(ARRAY[1], ARRAY[2, 3]) → ARRAY[1, 2, 3]
```

***

### `arrayElementAtInt`

Returns element at 1-based index. Returns null placeholder if invalid.

**Parameters:**

* `arr` (INT ARRAY): Input array
* `idx` (INT): 1-based index

**Returns:**\
INT

**Example:**

```sql
arrayElementAtInt(ARRAY[10, 20], 2) → 20
```

***

### `arraySumInt`

Sums all elements in an integer array.

**Parameters:**

* `arr` (INT ARRAY): Input array

**Returns:**\
INT

**Example:**

```sql
arraySumInt(ARRAY[1, 2, 3]) → 6
```

***

### `array` / `arrayValueConstructor`

Constructs an array from elements. Automatically detects type.

**Parameters:**\
Variable arguments (e.g., 1, 2, 3)

**Returns:**\
ARRAY

**Examples:**

```sql
array(1, 2) → ARRAY[1, 2]
array('a', 'b') → ARRAY['a', 'b']
```

***

### `generateIntArray`

Generates an integer sequence from `start` to `end` with `inc` increment.

**Parameters:**

* `start` (INT): Start value
* `end` (INT): End value (inclusive)
* `inc` (INT): Increment step

**Returns:**\
INT ARRAY

**Example:**

```sql
generateIntArray(1, 5, 2) → ARRAY[1, 3, 5]
```

***

### `arrayToString`

Joins array elements with a delimiter. Handles nulls.

**Parameters:**

* `values` (STRING ARRAY): Input array
* `delimiter` (STRING): Separator
* `nullString` (STRING) \[Optional]: Replacement for nulls

**Returns:**\
STRING

**Examples:**

```sql
arrayToString(ARRAY['a', 'b'], '-') → 'a-b'
arrayToString(ARRAY['a', NULL], '|', 'NA') → 'a|NA'
```

***
