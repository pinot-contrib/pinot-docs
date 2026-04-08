---
description: This section contains reference documentation for the filterMv function.
---

# filterMv

Evaluates each element of a multi-value column against a predicate and returns a filtered multi-value array containing only elements that satisfy the condition.

## Signature

> filterMv(mvColumn, 'predicate')

## Arguments

* **mvColumn** - A multi-value column to filter
* **predicate** - A string containing a predicate expression that uses `v` as the placeholder for each element. The predicate is evaluated for each element in the array.

## Supported Operators

The predicate supports the following operators:

* Comparison: `=`, `!=`, `>`, `>=`, `<`, `<=`
* Set membership: `IN`, `NOT IN`
* Range: `BETWEEN`
* Pattern matching: `REGEXP_LIKE`
* Logical: `AND`, `OR`, `NOT`

## Returns

A multi-value array containing only the elements that satisfy the predicate condition.

## Usage Examples

### Filter integers with comparison operators

```sql
SELECT filterMv(intArrayCol, 'v > 10 AND v < 50') AS filtered
FROM myTable
LIMIT 10
```

Result: Returns elements from `intArrayCol` that are greater than 10 and less than 50.

### Filter strings with REGEXP_LIKE

```sql
SELECT filterMv(stringArrayCol, 'REGEXP_LIKE(v, ''^/api/.*'')')
FROM myTable
LIMIT 10
```

Result: Returns elements from `stringArrayCol` that match the regex pattern starting with `/api/`.

### Filter with IN operator

```sql
SELECT filterMv(categoryCol, 'v IN (''A'', ''B'', ''C'')')
FROM myTable
LIMIT 10
```

Result: Returns elements from `categoryCol` that are either 'A', 'B', or 'C'.

### Filter with BETWEEN

```sql
SELECT filterMv(scoreCol, 'v BETWEEN 70 AND 90')
FROM myTable
LIMIT 10
```

Result: Returns elements from `scoreCol` where values are between 70 and 90 (inclusive).

### Filter with aggregation in GROUP BY

```sql
SELECT
  userId,
  COUNT(*) as count,
  filterMv(eventTypes, 'v = ''click''') as clickEvents
FROM events
GROUP BY userId
LIMIT 10
```

Result: For each user, returns the filtered array containing only 'click' events.

## Notes

* The predicate must use `v` as the placeholder for the element being evaluated.
* String values in predicates must be single-quoted or escaped appropriately.
* `filterMv` is useful for element-level filtering without requiring `CROSS JOIN UNNEST`.
* The order of elements in the filtered result matches their order in the original array.
* Empty or NULL arrays remain unchanged.
