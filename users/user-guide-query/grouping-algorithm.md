# Grouping algorithm

In this guide we will learn about the heuristics used for trimming results in Pinot's grouping algorithm (used when processing `GROUP BY` queries) to make sure that the server doesn't run out of memory.

## Within segment

When grouping rows within a segment, Pinot keeps a maximum of `<numGroupsLimit>` groups per segment.
This value is set to 100,000 by default and can be configured by the `pinot.server.query.executor.num.groups.limit` property.

If a segment reaches or exceeds this value, the results returned may not be completely accurate.
The `numGroupsLimitReached` property will be set to `true` in the query response if the value is reached.

### Trimming tail groups

After the inner segments groups have been computed, the Pinot query engine optionally trims tail groups.
Tail groups are ones that have a lower rank based on the `ORDER BY` clause used in the query.

This configuration is disabled by default, but can be enabled by configuring the `pinot.server.query.executor.min.segment.group.trim.size` property.
It is recommended to set this value to `5 * LIMIT` to ensure the accuracy of results.

This value can be overriden on a query by query basis by passing the following option:

```sql
SELECT * 
FROM ...

OPTION(minSegmentGroupTrimSize=<minSegmentGroupTrimSize>)
```

## Cross segments

Once grouping has been done within a segment, Pinot will merge segment results and trim tail groups when the number of records for a group reaches `<minServerGroupTrimSize>`.
This configuration is set to 5,000 by default and can be adjusted by configuring the `pinot.server.query.executor.min.server.group.trim.size` property.
It is recommended to set this value to at least `5 * LIMIT` to ensure the accuracy of results.

This value can be overriden on a query by query basis by passing the following option:

```sql
SELECT * 
FROM ...

OPTION(minServerGroupTrimSize=<minServerGroupTrimSize>)
```

Pinot will only trim the tail groups when the number of records in a group reaches the `<trimThreshold>`.
This configuration is set to 1,000,000 by default and can be adjusted by configuring the `pinot.server.query.executor.groupby.trim.threshold` property.
A higher threshold reduce the amount of trimming done, but consumes more heap memory.
If the threshold is set to more than 1,000,000,000, it means only trim the groups once before the server returns the results to the broker.

## GROUP BY behavior

Pinot sets a default `LIMIT` of 10 if one isn't defined and this applies to `GROUP BY` queries as well.
Therefore, if no limit is specified, Pinot will return 10 groups.

Pinot will trim tail groups based on the `ORDER BY` clause to reduce the memory footprint and improve the query performance. 
It keeps at least (5 * LIMIT) groups so that the results give good enough approximation in most cases. 
The configurable min trim size can be used to increase the groups kept to improve the accuracy, but has a larger extra memory footprint.

## HAVING behavior

If the query has a `HAVING` clause, it is applied on the merged `GROUP BY` results that already have the tail groups trimmed. 
If the `HAVING` clause is opposite of the `ORDER BY` order, groups matching the condition might already be trimmed and not returned. 
e.g.

```sql
SELECT SUM(colA) 
FROM myTable 
GROUP BY colB 
ORDER BY SUM(colA) DESC 
HAVING SUM(colA) < 100 
LIMIT 10
```

## Configuraton Parameters

| Parameter                                                           | Description                                                  | Default | Query Override
| ---- | ---- | ---- |---- |
| `pinot.server.query.executor.num.groups.limit`                           | The maximum number of groups allowed per segment. | 100,000 | N/A |
| `pinot.server.query.executor.min.segment.group.trim.size` | The maximum number of records per group when a group is trimmed at a segment level.    | -1 | `OPTION(minSegmentGroupTrimSize=<minSegmentGroupTrimSize>)` |
| `pinot.server.query.executor.min.server.group.trim.size` | The maximum number of records per group when a group is trimmed at a server level.     | 5,000 | `OPTION(minServerGroupTrimSize=<minServerGroupTrimSize>)` |
| `pinot.server.query.executor.groupby.trim.threshold` | The number of records that a group must contain before trimming is done.    |1,000,000| N/A | 
| `pinot.server.query.executor.max.execution.threads` | The maximum number of queries used per query.   | -1 |  `OPTION(maxExecutionThreads=<maxExecutionThreads>)` |