---
description: Use a timestamp index to speed up your time query with different granularities
---

# Timestamp Index

{% hint style="info" %}
This feature is supported from Pinot 0.11+.
{% endhint %}

## Background

The `TIMESTAMP` data type introduced in the [Pinot 0.8.0 release](../releases/0.8.0.md) stores value as millisecond epoch long value.

Typically, users won't need this low level granularity for analytics queries. Scanning the data and time value conversion can be costly for big data.

A common query pattern for timestamp columns is filtering on a time range and then grouping by using different time granularities(days/month/etc).

Typically, this requires the query executor to extract values, apply the transform functions then do filter/groupBy, with no leverage on the dictionary or index.

This was the inspiration for the Pinot timestamp index, which is used to improve the query performance for range query and group by queries on `TIMESTAMP` columns.

## Supported data type

A `TIMESTAMP` index can only be created on the `TIMESTAMP` data type.

## Timestamp Index

You can configure the granularity for a Timestamp data type column. Then:

1. Pinot will pre-generate one column per time granularity using a forward index and range index. The naming convention is `$${ts_column_name}$${ts_granularity}`, where the timestamp column `ts` with granularities `DAY`, `MONTH` will have two extra columns generated: `$ts$DAY` and `$ts$MONTH`.
2. Query overwrite for predicate and selection/group by:
   2.1 **GROUP BY**: Functions like `dateTrunc('DAY', ts)` will be translated to use the underly column `$ts$DAY` to fetch data.
   2.2 **PREDICATE**: range index is auto-built for all granularity columns.

Example query usage:

```sql
select count(*), 
       datetrunc('WEEK', ts) as tsWeek 
from airlineStats 
WHERE tsWeek > fromDateTime('2014-01-16', 'yyyy-MM-dd') 
group by tsWeek
limit 10
```

Some preliminary benchmarking shows the query performance across 2.7 billion records improved from 45 secs to 4.2 secs using a timestamp index and a query like this:

```sql
select dateTrunc('YEAR', event_time) as y, 
       dateTrunc('MONTH', event_time) as m,  
       sum(pull_request_commits) 
from githubEvents 
group by y, m 
limit 1000
Option(timeoutMs=3000000)
```

![Without Timestamp Index](https://user-images.githubusercontent.com/1202120/160910329-0d9ca637-dc95-4137-8c79-2f66cc8fbabf.png)

vs.

![With Timestamp Index](https://user-images.githubusercontent.com/1202120/160910364-48424875-1967-42d3-9a76-bdf1ee81a4ca.png)

## Usage

The timestamp index is configured on a per column basis inside the `fieldConfigList` section in the table configuration.

Specify `TIMESTAMP` as part of the `indexTypes`. Then, in the `timestampConfig` field, specify the granularities that you want to index.

Sample config:

```json
{
  "tableName": "airlineStats",
  "tableType": "OFFLINE",
  "segmentsConfig": {
    "timeColumnName": "DaysSinceEpoch",
    "timeType": "DAYS",
    "segmentPushType": "APPEND",
    "segmentAssignmentStrategy": "BalanceNumSegmentAssignmentStrategy",
    "replication": "1"
  },
  "tenants": {},
  "fieldConfigList": [
    {
      "name": "ts",
      "encodingType": "DICTIONARY",
      "indexTypes": ["TIMESTAMP"],
      "timestampConfig": {
        "granularities": [
          "DAY",
          "WEEK",
          "MONTH"
        ]
      }
    }
  ],
  "tableIndexConfig": {
    "loadMode": "MMAP"
  },
  "metadata": {
    "customConfigs": {}
  },
  "ingestionConfig": {}
}

```

