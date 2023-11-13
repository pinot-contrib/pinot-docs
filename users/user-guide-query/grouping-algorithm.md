# Grouping Algorithm

In this guide we will learn about the heuristics used for trimming results in Pinot's grouping algorithm (used when processing `GROUP BY` queries) to make sure that the server doesn't run out of memory.

## Within segment

When grouping rows within a segment, Pinot keeps a maximum of `<numGroupsLimit>` groups per segment. This value is set to 100,000 by default and can be configured by the `pinot.server.query.executor.num.groups.limit` property.

If the number of groups of a segment reaches this value, the extra groups will be ignored and the results returned may not be completely accurate. The `numGroupsLimitReached` property will be set to `true` in the query response if the value is reached.

### Trimming tail groups

After the inner segment groups have been computed, the Pinot query engine optionally trims tail groups. Tail groups are ones that have a lower rank based on the `ORDER BY` clause used in the query.

This configuration is disabled by default, but can be enabled by configuring the `pinot.server.query.executor.min.segment.group.trim.size` property.

When segment group trim is enabled, the query engine will trim the tail groups and keep `max(<minSegmentGroupTrimSize>, 5 * LIMIT)` groups if it gets more groups. Pinot keeps at least `5 * LIMIT` groups when trimming tail groups to ensure the accuracy of results.

This value can be overridden on a query by query basis by passing the following option:

```sql
SELECT * 
FROM ...

OPTION(minSegmentGroupTrimSize=<minSegmentGroupTrimSize>)
```

## Cross segments

Once grouping has been done within a segment, Pinot will merge segment results and trim tail groups and keep `max(<minServerGroupTrimSize>, 5 * LIMIT)` groups if it gets more groups.

`<minServerGroupTrimSize>` is set to 5,000 by default and can be adjusted by configuring the `pinot.server.query.executor.min.server.group.trim.size` property. When setting the configuration to `-1`, the cross segments trim can be disabled.

This value can be overridden on a query by query basis by passing the following option:

```sql
SELECT * 
FROM ...

OPTION(minServerGroupTrimSize=<minServerGroupTrimSize>)
```

When cross segments trim is enabled, the server will trim the tail groups before sending the results back to the broker. It will also trim the tail groups when the number of groups reaches the `<trimThreshold>`.

This configuration is set to 1,000,000 by default and can be adjusted by configuring the `pinot.server.query.executor.groupby.trim.threshold` property.

A higher threshold reduces the amount of trimming done, but consumes more heap memory. If the threshold is set to more than 1,000,000,000, the server will only trim the groups once before returning the results to the broker.

## At Broker

When broker performs the final merge of the groups returned by various servers, there is another level of trimming that takes place. The tail groups are trimmed and  `max(<minBrokerGroupTrimSize>, 5 * LIMIT)` groups are retained.&#x20;

Default value of `<minBrokerGroupTrimSize>` is set to 5000. This can be adjusted by configuring  `pinot.broker.min.group.trim.size` property.

## GROUP BY behavior

Pinot sets a default `LIMIT` of 10 if one isn't defined and this applies to `GROUP BY` queries as well. Therefore, if no limit is specified, Pinot will return 10 groups.

Pinot will trim tail groups based on the `ORDER BY` clause to reduce the memory footprint and improve the query performance. It keeps at least `5 * LIMIT` groups so that the results give good enough approximation in most cases. The configurable min trim size can be used to increase the groups kept to improve the accuracy but has a larger extra memory footprint.

## HAVING behavior

If the query has a `HAVING` clause, it is applied on the merged `GROUP BY` results that already have the tail groups trimmed. If the `HAVING` clause is the opposite of the `ORDER BY` order, groups matching the condition might already be trimmed and not returned. e.g.

```sql
SELECT SUM(colA) 
FROM myTable 
GROUP BY colB 
HAVING SUM(colA) < 100 
ORDER BY SUM(colA) DESC 
LIMIT 10
```

Increase min trim size to keep more groups in these cases.

## Configuration Parameters

| Parameter                                                                                                                                                            | Default                        | Query Override                                              | Description |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------- | ----------- |
| <p><code>pinot.server.query.executor.num.groups.limit</code><br>The maximum number of groups allowed per segment.</p>                                                | 100,000                        | `OPTION(numGroupsLimit=<numGroupsLimit>)`                   |             |
| <p><code>pinot.server.query.executor.min.segment.group.trim.size</code><br>The minimum number of groups to keep when trimming groups at the segment level.</p>       | -1 (trim disabled)             | `OPTION(minSegmentGroupTrimSize=<minSegmentGroupTrimSize>)` |             |
| <p><code>pinot.server.query.executor.min.server.group.trim.size</code><br>The minimum number of groups to keep when trimming groups at the server level.</p>         | 5,000                          | `OPTION(minServerGroupTrimSize=<minServerGroupTrimSize>)`   |             |
| <p><code>pinot.server.query.executor.groupby.trim.threshold</code><br>The number of groups to trigger the server level trim.</p>                                     | 1,000,000                      | `OPTION(groupTrimThreshold=<groupTrimThreshold>)`           |             |
| <p><code>pinot.server.query.executor.max.execution.threads</code><br>The maximum number of execution threads (parallelism of segment processing) used per query.</p> | -1 (use all execution threads) | `OPTION(maxExecutionThreads=<maxExecutionThreads>)`         |             |
| <p><code>pinot.broker.min.group.trim.size</code><br><br>The minimum number of groups to keep when trimming groups at the broker.</p>                                 | 5000                           | N/A                                                         |             |
