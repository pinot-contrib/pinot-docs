---
description: Learn how to write fast queries for looking up IDs in a list of values.
---

# Filtering with IdSet



{% hint style="info" %}
`IDSET`, `IN_ID_SET`, and the string-subquery form `IN_SUBQUERY` work in both the single-stage and multi-stage query engines. In the multi-stage engine, `IN_ID_SET` can be used in leaf filters, post-join filters, join conditions, and `HAVING`. `IN_PARTITIONED_SUBQUERY` remains single-stage only.
{% endhint %}

A common use case is filtering on an id field with a list of values. This can be done with the IN clause, but using IN doesn't perform well with large lists of IDs. For large lists of IDs, we recommend using an IdSet.

Large base64 IdSet literals (including sets with millions of IDs) can be used in both query engines. For HTTP queries, a literal is still subject to the broker's approximately 20-million-character JSON string limit. In the multi-stage engine, a query carrying a large literal can also exceed the 64 MiB default gRPC message limits; increase the [server inbound plan limit](../../reference/configuration-reference/server.md) or [broker inbound dispatch limit](../../reference/configuration-reference/broker.md) only if the corresponding message exceeds its default.

## Functions

### ID\_SET

> ID\_SET(columnName, 'sizeThresholdInBytes=8388608;expectedInsertions=5000000;fpp=0.03' )

This function returns a base 64 encoded IdSet of the values for a single column. The IdSet implementation used depends on the column data type:

* INT - RoaringBitmap unless _sizeThresholdInBytes_ is exceeded, in which case Bloom Filter.
* LONG - Roaring64NavigableMap unless _sizeThresholdInBytes_ is exceeded, in which case Bloom Filter.
* Other types - Bloom Filter

The following parameters are used to configure the Bloom Filter:

* _expectedInsertions_ - Number of expected insertions for the BloomFilter, must be positive
* _fpp_ - False positive probability to use for the BloomFilter. Must be positive and less than 1.0.

Note that when a Bloom Filter is used, the filter results are approximate - you can get false-positive results (for membership in the set), leading to potentially unexpected results.

### IN\_ID\_SET

> IN\_ID\_SET(columnName, base64EncodedIdSet)

This function returns 1 if a column contains a value specified in the IdSet and 0 if it does not.

The lookup value must have the same stored type as the values used to build the IdSet. With null handling enabled, a NULL lookup value yields NULL for a non-empty set, but FALSE for an empty or NULL set. Thus `IN_ID_SET(nullableCol, <empty set>) = 0` also keeps NULL rows.

### IN\_SUBQUERY

> IN\_SUBQUERY(columnName, subQuery)

This function generates an IdSet from a subquery and then filters ids based on that IdSet on a Pinot broker.

#### Multi-stage subquery execution

```sql
SET useMultistageEngine = true;
SELECT COUNT(*) FROM orders
WHERE IN_SUBQUERY(customerId, 'SELECT IDSET(customerId) FROM customers WHERE active = 1') = 1;
```

The broker executes IdSet subqueries before compiling the outer query, replacing their results with `IN_ID_SET` literals so eligible filters can run at the leaf stage. `IN_SUBQUERY(expr, 'sql')` works in SELECT, WHERE, HAVING, JOIN ON, nested queries, CTEs, and set operations. `IN_ID_SET(expr, (SELECT ...))` is also pre-executed when its subquery validates independently, is uncorrelated, and references no enclosing WITH item; other scalar subqueries remain in the outer plan.

Each distinct subquery runs once per outer request, with its own MSE request ID and the time remaining before the outer deadline. It inherits query options except `dropResults`; SET options inside an IN_SUBQUERY string override inherited values, subject to `sqlOptionsMode`. Each subquery independently undergoes table authorization, quota, and throttling checks, is visible as a running query, and can be cancelled through the outer client query ID. Subqueries execute before the outer query's table-access and quota checks.

The result must contain one STRING column and at most one row, holding a serialized IdSet. No row or NULL means the empty set: `= 1` is false and `= 0` is true, including for NULL lookup values. Subquery errors or partial results fail the outer query rather than silently using an incomplete set. Matching stored types and Bloom-filter false-positive caveats still apply.

EXPLAIN does not execute these subqueries. It substitutes empty sets and reports the skipped SQL strings as a JSON array in `ID_SET_SUBQUERIES_NOT_RUN`; that plan is not evidence of actual subquery results. Compilation-only paths cannot discover tables embedded inside the SQL string. The `singleStageQueriesInvalidMultiStage` meter no longer counts single-stage IN_SUBQUERY queries as MSE-incompatible.

Pre-execution avoids sending the serialized set back through the client as SQL text, but does not remove plan-size limits. Each occurrence embeds a copy, even if the subquery ran once. All stage plans for one server share a gRPC message; the default `pinot.query.multistage.query.server.max.inbound.message.size.bytes` is 64 MB. Large or repeated sets can exceed it and fail dispatch with `RESOURCE_EXHAUSTED`.

For monitoring, window row-limit overflow in `BREAK` mode now marks `partialResult=true` and is logged as a partial result. The default `THROW` mode is unchanged.

*Source: [PR #19804](https://github.com/apache/pinot/pull/19804)*

### IN\_\_PARTITIONED\_\_SUBQUERY

> IN\_PARTITIONED\_SUBQUERY(columnName, subQuery)

This function generates an IdSet from a subquery and then filters ids based on that IdSet on a Pinot server.

This function works best when the data is partitioned by the id column and each server contains all the data for a partition. The generated IdSet for the subquery will be smaller as it will only contain the ids for the partitions served by the server. This will give better performance.

{% hint style="info" %}
The query passed to `IN_SUBQUERY` can be run on any table - they aren't restricted to the table used in the parent query.

The query passed to `IN__PARTITIONED__SUBQUERY` must be run on the same table as the parent query.
{% endhint %}

## Examples

### Create IdSet

You can create an IdSet of the values in the _yearID_ column by running the following:

```sql
SELECT ID_SET(yearID)
FROM baseballStats
WHERE teamID = 'WS1'
```

| idset(yearID)                                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ATowAAABAAAAAAA7ABAAAABtB24HbwdwB3EHcgdzB3QHdQd2B3cHeAd5B3oHewd8B30Hfgd/B4AHgQeCB4MHhAeFB4YHhweIB4kHigeLB4wHjQeOB48HkAeRB5IHkweUB5UHlgeXB5gHmQeaB5sHnAedB54HnwegB6EHogejB6QHpQemB6cHqAc= |

When creating an IdSet for values in non INT/LONG columns, we can configure the _expectedInsertions_:

```sql
SELECT ID_SET(playerName, 'expectedInsertions=10')
FROM baseballStats
WHERE teamID = 'WS1'
```

| idset(playerName)                |
| -------------------------------- |
| AwIBBQAAAAL///////////////////// |

```sql
SELECT ID_SET(playerName, 'expectedInsertions=100')
FROM baseballStats
WHERE teamID = 'WS1'
```

| idset(playerName)                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------------------------- |
| AwIBBQAAAAz///////////////////////////////////////////////9///////f///9/////7///////////////+/////////////////////////////////////////////8= |

We can also configure the fpp parameter:

```sql
SELECT ID_SET(playerName, 'expectedInsertions=100;fpp=0.01')
FROM baseballStats
WHERE teamID = 'WS1'
```

| idset(playerName)                                                                                                                                                            |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AwIBBwAAAA/////////////////////////////////////////////////////////////////////////////////////////////////////////9///////////////////////////////////////////////7//////8= |

### Filter by values in IdSet

We can use the _IN\_ID\_SET_ function to filter a query based on an IdSet. To return rows for _yearID_s in the IdSet, run the following:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_ID_SET(
 yearID,   
 'ATowAAABAAAAAAA7ABAAAABtB24HbwdwB3EHcgdzB3QHdQd2B3cHeAd5B3oHewd8B30Hfgd/B4AHgQeCB4MHhAeFB4YHhweIB4kHigeLB4wHjQeOB48HkAeRB5IHkweUB5UHlgeXB5gHmQeaB5sHnAedB54HnwegB6EHogejB6QHpQemB6cHqAc='
  ) = 1 
GROUP BY yearID
```

### Filter by values not in IdSet

To return rows for _yearID_s not in the IdSet, run the following:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_ID_SET(
  yearID,   
  'ATowAAABAAAAAAA7ABAAAABtB24HbwdwB3EHcgdzB3QHdQd2B3cHeAd5B3oHewd8B30Hfgd/B4AHgQeCB4MHhAeFB4YHhweIB4kHigeLB4wHjQeOB48HkAeRB5IHkweUB5UHlgeXB5gHmQeaB5sHnAedB54HnwegB6EHogejB6QHpQemB6cHqAc='
  ) = 0 
GROUP BY yearID
```

### Filter on broker

To filter rows for _yearID_s in the IdSet on a Pinot Broker, run the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 1
GROUP BY yearID  
```

To filter rows for _yearID_s not in the IdSet on a Pinot Broker, run the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 0
GROUP BY yearID  
```

### Filter on server

To filter rows for _yearID_s in the IdSet on a Pinot Server, run the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_PARTITIONED_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 1
GROUP BY yearID  
```

To filter rows for _yearID_s not in the IdSet on a Pinot Server, run the following query:

```sql
SELECT yearID, count(*) 
FROM baseballStats 
WHERE IN_PARTITIONED_SUBQUERY(
  yearID, 
  'SELECT ID_SET(yearID) FROM baseballStats WHERE teamID = ''WS1'''
  ) = 0
GROUP BY yearID  
```

##
