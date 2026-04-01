---
description: This section contains reference documentation for the round function.
---

# round

Round the given time value to nearest bucket start value.

## Signature

> round(timeValue, bucketSize)

## Usage Examples

Round seconds epoch value to the start value of the 30 seconds bucket to which it belongs.

```sql
select round(1639144274, 30) AS rounded
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>rounded</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1639144260</td>
    </tr>
  </tbody>
</table>

Round milliseconds epoch value to the start value of the 5,000 milliseconds bucket to which it belongs.

```sql
select round(1639144274000, 5000) AS rounded
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>rounded</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1639144270000</td>
    </tr>
  </tbody>
</table>
