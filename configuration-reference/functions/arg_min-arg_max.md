---
description: >-
  This section contains reference documentation for the ARG_MIN and ARG_MAX
  function.
---

# ARG\_MIN / ARG\_MAX

This function scans the given dataset to identify the maximum and minimum values in the specified measuring columns. Once these extreme values (the maxima and minima) are found, the function locates the corresponding entries in the projection column. These entries are associated with the rows where the extreme values were found in the measuring columns. The function then returns these projection column values, providing a way to link the extreme measurements with their corresponding data in another part of the dataset.

## Signature

> ARG\_MIN (measuringCol1, measuringCol2, measuringCol3, projectionCol)
>
> ARG\_MAX (measuringCol1, measuringCol2, measuringCol3, projectionCol)

## Usage Examples

Find the user with maximum activity. If there are multiple users, break the tie with their last\_activity\_date. If still a tie, break with user\_id. And project user\_id.

```sql
SELECT ARG_MAX(activity, last_activity_date, user_id, user_id)
FROM userEngagmentTable
```

More useful is that this multiple such aggregation function can be used with GROUP BY

```sql
SELECT user_region, ARG_MAX(activity, last_activity_date, user_id, user_id),
    ARG_MIN(user_satisfaction, user_id)
FROM userEngagmentTable
GROUP BY user_region
```

Note:&#x20;

1. In cases where multiple rows share the same extreme values in the measuring columns, all such rows will be returned by the function.&#x20;
2. If the goal is to project multiple different columns that correspond to the same set of measuring columns, you can achieve this by invoking the function multiple times, each time specifying a different projection column.
3. This impl does not work with AS clause (e.g. `SELECT argmin(longCol, doubleCol) AS argmin` won't work)
4. Putting `argmin/argmax` column inside order by clause (e.g. `SELECT intCol, argmin(longCol, doubleCol) FROM table GROUP BY intCol ORDER BY argmin(longCol, doubleCol)`) is not supported as semantically ordering multi-column multi-row `argmin/argmax` results doesn't make sense
5. Currently projecting MV bytes column doesn't work for now due to an issue

For more detailed examples, see: [https://github.com/apache/pinot/pull/10636](https://github.com/apache/pinot/pull/10636)  &#x20;
