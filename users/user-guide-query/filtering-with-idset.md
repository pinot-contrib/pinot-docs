# Filtering with IdSet

A common use case is filtering on an id field with a list of values. This can be done with the IN clause, but this approach doesn't perform well with large lists of ids. In these cases, you can use an IdSet.

## Functions

### ID\_SET

> ID_SET(columnName, 'sizeThresholdInBytes=1000;expectedInsertions=10000;fpp=0.03' )

This function returns a base 64 encoded IdSet of the values for a single column. The IdSet implementation used depends on the column data type:

* INT - RoaringBitmap
* LONG - Roaring64NavigableMap
* Other types - Bloom Filter. Supports the following parameters:
  * _expectedInsertions_ - Number of expected insertions for the BloomFilter, must be positive
  * _fpp_ - Desired false positive probability for the BloomFilter, must be positive and < 1.0

### IN\_ID\_SET

> IN_ID_SET(columnName, base64EncodedIdSet)

This function returns 1 if a column contains a value specified in the IdSet and 0 if it does not.

### IN\_SUBQUERY

> IN_SUBQUERY(columnName, subQuery)

This function generates an IdSet from a subquery and then filters ids based on that IdSet on a Pinot broker.

### IN\__PARTITIONED\__SUBQUERY

> IN_PARTITIONED_SUBQUERY(columnName, subQuery)

This function generates an IdSet from a subquery and then filters ids based on that IdSet on a Pinot server.&#x20;

This function works best when the data is partitioned by the id column and each server contains all the data for a partition. The generated IdSet for the first query will be smaller as it will only contain the ids for the partitions served by the server. This will give better performance.

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

When creating an IdSet for values in non INT/LONG columns, we can configure the expectedInsertions and fpp parameters:

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
