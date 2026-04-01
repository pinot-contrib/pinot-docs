# Null Handling Functions

Pinot provides functions for testing, handling, and propagating null values. The logical operators follow SQL standard three-valued logic with Trino-compatible null handling.

{% hint style="info" %}
Null handling must be enabled for your table to use these functions. Set `"enableColumnBasedNullHandling": true` in the table's index configuration.
{% endhint %}

## isNull

```sql
isNull(col)
```

Returns `true` if the value is `null`, `false` otherwise.

```sql
SELECT orderId, isNull(discount) AS has_no_discount
FROM orders
WHERE isNull(discount)
LIMIT 10
```

## isNotNull

```sql
isNotNull(col)
```

Returns `true` if the value is not `null`, `false` otherwise.

```sql
SELECT orderId, total
FROM orders
WHERE isNotNull(couponCode)
LIMIT 10
```

## isDistinctFrom

```sql
isDistinctFrom(col1, col2)
```

Returns `true` if the two values are different, treating `null` as a known value. Two `null` values are considered not distinct from each other (returns `false`), and a `null` compared to any non-null value is considered distinct (returns `true`).

```sql
SELECT isDistinctFrom(oldPrice, newPrice) AS price_changed
FROM priceHistory
LIMIT 10
-- Returns false when both are null, true when only one is null
```

## isNotDistinctFrom

```sql
isNotDistinctFrom(col1, col2)
```

Returns `true` if the two values are equal, treating `null` as a known value. Two `null` values are considered not distinct (returns `true`). This is the negation of `isDistinctFrom`.

```sql
SELECT isNotDistinctFrom(shippingAddr, billingAddr) AS same_address
FROM orders
LIMIT 10
```

## coalesce

```sql
coalesce(col1, col2, col3, ...)
```

Returns the first non-null value from the argument list. Returns `null` if all arguments are null.

```sql
SELECT coalesce(preferredName, firstName, 'Unknown') AS displayName
FROM users
LIMIT 10
```

## caseWhen

```sql
CASE WHEN condition1 THEN result1
     WHEN condition2 THEN result2
     ELSE defaultResult
END
```

Evaluates conditions in order and returns the result for the first `true` condition. Returns the `ELSE` value if no condition matches, or `null` if there is no `ELSE` clause.

```sql
SELECT orderId,
       CASE WHEN total > 1000 THEN 'premium'
            WHEN total > 100 THEN 'standard'
            ELSE 'basic'
       END AS tier
FROM orders
LIMIT 10
```

## nullIf

```sql
nullIf(value1, value2)
```

Returns `null` if `value1` equals `value2`, otherwise returns `value1`. Useful for converting sentinel values to null.

```sql
SELECT nullIf(status, 'N/A') AS status
FROM events
LIMIT 10
-- Returns null when status is 'N/A', otherwise returns the status value
```

## AND

```sql
bool_col1 AND bool_col2
```

Logical AND operator with three-valued logic. Returns `false` if either operand is `false`, `null` if either operand is `null` and the other is not `false`, and `true` only when both operands are `true`.

<table>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>a AND b</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TRUE</td>
      <td>TRUE</td>
      <td>TRUE</td>
    </tr>
    <tr>
      <td>TRUE</td>
      <td>FALSE</td>
      <td>FALSE</td>
    </tr>
    <tr>
      <td>TRUE</td>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <td>FALSE</td>
      <td>NULL</td>
      <td>FALSE</td>
    </tr>
    <tr>
      <td>NULL</td>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>

```sql
SELECT *
FROM orders
WHERE isPaid AND isShipped
LIMIT 10
```

## OR

```sql
bool_col1 OR bool_col2
```

Logical OR operator with three-valued logic. Returns `true` if either operand is `true`, `null` if either operand is `null` and the other is not `true`, and `false` only when both operands are `false`.

<table>
  <thead>
    <tr>
      <th>a</th>
      <th>b</th>
      <th>a OR b</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TRUE</td>
      <td>FALSE</td>
      <td>TRUE</td>
    </tr>
    <tr>
      <td>TRUE</td>
      <td>NULL</td>
      <td>TRUE</td>
    </tr>
    <tr>
      <td>FALSE</td>
      <td>FALSE</td>
      <td>FALSE</td>
    </tr>
    <tr>
      <td>FALSE</td>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
    <tr>
      <td>NULL</td>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>

```sql
SELECT *
FROM orders
WHERE isPaid OR isCOD
LIMIT 10
```

## NOT

```sql
NOT bool_col
```

Logical NOT operator. Returns `null` if the input is `null`, otherwise returns the boolean negation.

<table>
  <thead>
    <tr>
      <th>a</th>
      <th>NOT a</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>TRUE</td>
      <td>FALSE</td>
    </tr>
    <tr>
      <td>FALSE</td>
      <td>TRUE</td>
    </tr>
    <tr>
      <td>NULL</td>
      <td>NULL</td>
    </tr>
  </tbody>
</table>

```sql
SELECT *
FROM orders
WHERE NOT isCancelled
LIMIT 10
```
