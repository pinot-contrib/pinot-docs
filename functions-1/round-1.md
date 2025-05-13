# roundDecimal

Rounds the given value to a specified number of decimal places

## Signature

> roundDecimal(decimal\_value, decimal\_places)

## Usage Examples

```sql
SELECT roundDecimal(3.14159, 2);  -- Output: 3.14
SELECT roundDecimal(12.34567, 3); -- Output: 12.346
SELECT roundDecimal(9.8765, 0);   -- Output: 10
```

## **Important Considerations:**

* The `roundDecimal` function is particularly useful in financial calculations, scientific computations, or any scenario where precise control over decimal precision is required.
* Be aware of potential rounding errors that can accumulate in complex calculations involving many rounded values.
