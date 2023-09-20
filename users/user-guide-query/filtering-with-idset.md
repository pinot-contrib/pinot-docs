---
description: >-
  Learn how to look up IDs in a list of values. Filtering with IdSet is only
  supported with the single-stage query engine (v1).
---

# Filtering with IdSet



{% hint style="info" %}
Filtering with IdSet is **only supported with the single-stage query engine (v1)**.
{% endhint %}

A common use case is filtering on an id field with a list of values. This can be done with the IN clause, but using IN doesn't perform well with large lists of IDs. For large lists of IDs, we recommend using an IdSet.

## Functions

### ID\_SET

> ID\_SET(columnName, 'sizeThresholdInBytes=8388608;expectedInsertions=5000000;fpp=0.03' )

This function returns a base 64 encoded IdSet of the values for a single column. The IdSet implementation used depends on the column data type:

* INT - RoaringBitmap unless _sizeThresholdInBytes_ is exceeded, in which case Bloom Filter.
* LONG - Roaring64NavigableMap unless _sizeThresholdInBytes_ is exceeded, in which case Bloom Filter.
* Other types - Bloom Filter

The following parameters are used to configure the Bloom Filter:

* _expectedInsertions_ - Number of expected insertions for the BloomFilter, must be positive
* _fpp_ - Desired false positive probability for the BloomFilter, must be positive and < 1.0

Note that when a Bloom Filter is used, the filter results are approximate - you can get false-positive results (for membership in the set), leading to potentially unexpected results.

### IN\_ID\_SET

> IN\_ID\_SET(columnName, base64EncodedIdSet)

This function returns 1 if a column contains a value specified in the IdSet and 0 if it does not.

### IN\_SUBQUERY

> IN\_SUBQUERY(columnName, subQuery)

This function generates an IdSet from a subquery and then filters ids based on that IdSet on a Pinot broker.

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
