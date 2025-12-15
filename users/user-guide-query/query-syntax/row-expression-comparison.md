# Row Expression Comparison 

***

## Row Expression

### ROW()

#### **Description**:

ROW value expressions is supported in Pinot in comparison contexts, enabling efficient keyset pagination queries. ROW expressions allow users to write cleaner multi-column comparisons like WHERE (col1, col2, col3) > (val1, val2, val3) instead of verbose nested conditions.
The evaluation of row expression is based on the ([JOOQ transformations](https://www.jooq.org/doc/latest/manual/sql-building/conditional-expressions/comparison-predicate-degree-n/)) for the comparison operators.


#### **Syntax**:

Pinot supports implicit ROW-style expressions in comparison predicates using a parenthesized list of expressions on both sides of the comparator:

WHERE (col1, col2, col3) > (val1, val2, val3)


Supported comparison operators:
```
=, <>, <, <=, >, >=
```

Note: Explicit use of the ROW() keyword (e.g., WHERE ROW(col1, col2) = ROW(1, 2)) is not yet supported due to the current SQL parser configuration (SqlConformanceEnum.BABEL). Future improvements may enable explicit row value constructors.


#### **Note**:

- ROW comparisons are lexicographic, not element-wise
- Pinot does not materialize row types — it rewrites comparisons at planning time
- Rewrite complexity grows linearly with the number of columns
- Mixed data types are supported as long as pairwise comparisons are valid


#### **Sample Example Usage**:

**Equality (=)**
```sql
WHERE (a, b, c) = (x, y, z)
```

is rewritten to

```sql
WHERE a = x
  AND b = y
  AND c = z
```


**Greater Than (>)**
```sql
WHERE (a, b, c) > (x, y, z)
```

is rewritten to 

```sql
WHERE a > x
   OR (a = x AND b > y)
   OR (a = x AND b = y AND c > z)
```

**Less Than (<)**
```sql
WHERE (a, b, c) < (x, y, z)
```

is rewritten to 
```sql
WHERE a < x
OR (a = x AND b < y)
OR (a = x AND b = y AND c < z)
```

