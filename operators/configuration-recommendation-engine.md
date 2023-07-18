---
description: >-
  This page describes the automated mechanisms we have for recommending a
  suitable configuration for your deployment.
---

# Configuration Recommendation Engine

## Overview

Recommendation Engine is a rule based engine that recommends optimal configuration options for Pinot tables. The configuration options currently covered by the engine are mostly TableConfig related (e.g indexes, real-time config). Note that not all configuration options in TableConfig are currently covered. The following table shows the ones that are currently covered.

| Rule                                | Config Entity            | Config Name                                                                                                                                                                                                                                               | Applicable Table Type |
| ----------------------------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| Kafka Partitions                    | Kafka                    | <ul><li><code>num.partitions</code></li></ul>                                                                                                                                                                                                             | Real-time             |
| Table Partitioning                  | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>segmentPartitionConfig</code></li></ul>                                                                                                                                                                       | Real-time & Offline   |
| Inverted Sorted Index Joint         | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>invertedIndexColumns</code></li><li><code>tableIndexConfig</code>→<code>sortedColumn</code></li></ul>                                                                                                         | Real-time & Offline   |
| NoDictionary OnHeapDictionary Joint | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>noDictionaryColumns</code></li><li><code>tableIndexConfig</code>→<code>onHeapDictionaryColumns</code></li></ul>                                                                                               | Real-time & Offline   |
| Bloom Filter                        | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>bloomFilterColumns</code></li></ul>                                                                                                                                                                           | Real-time & Offline   |
| Varied Length Dictionary            | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>variedLengthDictionaryColumns</code></li></ul>                                                                                                                                                                | Real-time & Offline   |
| Segment Size                        | Segment Build & Push Job | <p>Recommendations on:</p><ul><li>Segment size in Bytes</li><li>Number of segments</li><li>Number of rows per segment</li></ul>                                                                                                                           | Offline               |
| Aggregate Metrics                   | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>aggregateMetrics</code></li></ul>                                                                                                                                                                             | Real-time             |
| Real-time Provisioning              | Table Config             | <ul><li><code>tableIndexConfig</code>→<code>streamConfigs</code>→<code>realtime.segment.flush.threshold.time</code></li><li><code>tableIndexConfig</code>→<code>streamConfigs</code>→<code>realtime.segment.flush.threshold.segment.size</code></li></ul> | Real-time             |
| Real-time Provisioning              | Host Management          | Number of hosts needed in terms of memory consumption                                                                                                                                                                                                     | Real-time             |

Recommendation Engine can be used to optimize the configuration parameters for both new and existing tables. Also since the recommendation engine tries to generate near-optimal configurations, users are strongly encouraged to provide the input information to the best of their knowledge. It is ok if the information is not fully accurate. However, random/arbitrary and incomplete information will not help the Recommendation Engine’s algorithms.

Also see the section on [RealtimeProvisioningHelper](operating-pinot/tuning/realtime.md#realtimeprovisioninghelper).

## How to use the engine

The engine is currently accessible by a REST endpoint on Pinot Controller. It's a PUT endpoint under `/tables/recommender` path which takes a json as its input and produce a json as its output. You can try it out in Swagger REST API section of Pinot Web UI.

## Input

The input needs to be provided in json format. Different fields of the input can be categorized into the following four groups.

### 1. Data Characteristics

Data characteristics is defined in "schema" field. The content of this field is an extended version of Pinot Schema which has some additional metadata that's inserted into the definition of each column:

* **Cardinality**: Total number of unique values for this dimension. Provide cardinality to the best of your knowledge to help generate the best possible recommendations.
* **numValuesPerEntry**: For multi-value columns only, this is the average number of values per column value. Note that:
  * For multi-value columns, other than numValuesPerEntry, singleValueField has to be defined as false.
  * For single-value columns, numValuesPerEntry and singleValueField should not be specified.
  * Metric columns cannot be defined as multi-value.
  * Columns of type BYTES cannot be defined as multi-value.
* **averageLength**: For data type of BYTES or STRING only, this is the average length of the column value.

### 2. Table Characteristics

* For real-time/hybrid tables,
  * **Kafka partitions** \[Optional] Fill this field with the partition count suggested by Kafka team. If this field is not provided, the engine tries to recommend the optimal number of partitions for the Kafka topic.
  * **Kafka messages per second** \[Required] Average number of messages go to the Kafka topic per second.
* For offline/hybrid tables the following is required :
  * **Records per push**
* For all tables, the following are required :
  * **Expected QPS**
  * **Latency SLA in ms**
  * **Query pattern** This should be filled out to the best of your knowledge. Many performance-impactful configs (e.g. indices, partitioning, sorting) are generated using query patterns.

### 3. Rules

In this section, lets describe the rules which generate recommendations for different configurations:

* **Segment Size** - This rule recommends the following parameters for offline tables: 1) number of segments, 2) number of records in each segment, and 3) size of each segment. For new tables, the rule uses the provided data characteristics to find the optimal values for these parameters. If your table already exists in production, you can obtain the following information from existing segments: number of rows in segment and segment size. Then add them as actualSegmentSize and numRowsInActualSegment parameters of segment size rule. You'll see an example for this in Overrides section.
* **Kafka Partitions** - If the number of Kafka partitions is not already determined/provided, this rules recommends a value for it. It requires topic aggregate message rate (number of messages per seconds across all partitions of the topic) to drive the optimal number of partitions.
* **Inverted Sorted Index Join** - This rule recommends which columns should have sorted index or inverted index.
* **Table Partitioning** - Partitioning parameters for real-time and offline parts of the table are normally the same, but some use cases might have different parameters. For the real-time part, this rules mirrors the output of the Kafka Partitions rule. For offline, this rule recommends a value for the number of partitions parameter which is determined based on the optimal number of segments - refer to Segment Size rule on how it’s calculated. This rule also recommends which column gives the best performance for partitioning by going over the query patterns and find out which column appears more - of course proportional to the weight of the query pattern - in IN or EQUALITY filters.
* **Bloom Filter** - Bloom filters are useful for the columns that appear frequently in EQUALITY filters. This rule recommends which columns should have Bloom filters. It skips the columns with high cardinality as their corresponding Bloom filter memory footprint is large.
* **NoDictionary OnHeapDictionary Joint** - This rule recommends which columns should be defined as NoDictionary columns and also which columns should have on-heap dictionary indices. Dictionary encoding can be helpful for efficient query processing and saving storage. However, unnecessary creation of dictionary can also add to storage and sometimes performance penalty. Based on the query pattern user provides, the rule attempts to find the best set of columns that will benefit from dictionary encoding. For on-heap dictionary part, the columns that are heavily queried and also have low cardinalities - for which the on-heap memory footprint is acceptably small - can have on-heap dictionary. The on-heap dictionary can result in more performant query execution.
* **Varied Length Dictionary** - This rule recommends that for data types with varied length, i.e. STRING or BYTES, varied length dictionaries should be used. Using these dictionaries results in better performance.
* **Flag Queries** - This rule flags query patterns that are not valid.
* **Aggregate Metrics** - This rule checks the provided queries and suggests the value for ‘AggregateMetrics’ flag in table config. It looks at selection columns and if all of them are SUM function, the flag should be true, otherwise it’s false. It also checks if all column names appearing in sum function are in fact metric columns.
* **Real-time Provisioning** - This rule gives some recommendations useful for provisioning real-time tables. Specifically it provides some insights on optimal segments size, total memory used per host, and memory used for consuming segments per host based on the provided characteristics of the data and Kafka ingestion rate. The ultimate goal of this rule is to find out required consumption duration as well as the required number of hosts which leads to a desired real-time segment size.

All rules run by default. You have the option to select the ones you want to run.

Note that the following rules only apply to real-time or hybrid tables:

* Kafka Partitions
* Real-time Provisioning
* Aggregate Metrics

And the following rule only applies to offline or hybrid tables:

* Segment Size

### 4. Overrides

Each rule may have some parameters with default values. You can change these default values and consequently change the behavior of the rules. As an example, in the Recommend Table Partitioning rule, we do not recommend partitioning for low QPS tables. To change the default behavior, you can use the followings:

```javascript
"partitionRuleParams": {
  "THRESHOLD_MIN_QPS_PARTITION":300
}
```

As a second example, let’s look at Segment Size rule. This rule generates a segment based on the provided data characteristics. Parameter numRowsInGeneratedSegment controls the size of the generated segment. Parameter desiredSegmentSizeMB specifies the desired ideal segment size. The default values are 50,000 rows and 500MB:

```javascript
"segmentSizeRuleParams": {
    "desiredSegmentSizeMB":200,
    "numRowsInGeneratedSegment":10000
}
```

Or in case your table is already in production and you know the actual segment size and number of rows in an actual segment, you can do:

```javascript
"segmentSizeRuleParams": {
    "desiredSegmentSizeMB": 200,
    "actualSegmentSizeMB": 250,
    "numRowsInActualSegment": 3500000
}
```

The detailed list and usages of the parameters are documented in detail in [source code](https://github.com/apache/pinot/tree/master/pinot-controller/src/main/java/org/apache/pinot/controller/recommender/rules/io/params) and this [wiki](https://cwiki.apache.org/confluence/display/PINOT/Automated+Inverted+Index+Recommendation+for+Pinot) page.

One last item to explain for the input json is the overridden configs. You can instruct the recommendation engine to not recommend some config values and instead use your provided values for those configs. This way, the Rule Engine tries to find the optimal value for other parameter with respsect to the fixed parameters that you have provided. As an example, you can say I want the followings to be my inverted index columns and range index columns:

```javascript
"overWrittenConfigs": {
    "indexConfig":{
        "invertedIndexColumns":["a","b"],
        "rangeIndexColumns":["f"]
    }
}
```

## Output

Currently, the engine recommends the following configs:

* Indexing Config:
  * **Inverted Index Columns** The columns to apply inverted (bitmap) indices on.
  * **Primary Sorted Column** The ONE column used to sort all the data during the segment generation.
  * **Bloom Filter Columns** The columns to add the bloom filter on.
  * **No Dictionary Columns** The columns not to add a dictionary on.
  * **On Heap Dictionary Columns** The dictionaries to put on-heap.
  * **Varied Length Dictionary Columns** The columns to create varied length dictionaries.
* Segment Partition Config：
  * **Number of Kafka Partitions** This value will be equal to the Kafka partition counts if provided.
  * **Primary Partitioning Column** The ONE column used to partition all the data during the segment generation.
  * **Number of Real-time Partitions** Number of partitions for real-time side of the table.
  * **Number of Offline Partitions** Number of partitions for offline side of the table.
* Segment Size Recommendations:
  * **Segment Size Recommended** size for offline segments in Byte.
  * **Number of Segments** Recommended number for offline segments.
  * **Number of Rows per Segment** Recommended number of rows for offline segments.
* Real-time Provisioning Recommendations:
  * Each of the following recommendations is basically a 2D matrix of number of hosts and number of consumption hours. The goal is to give user insight to help find out how many real-time hosts are required to handle Kafka ingestion. Also the value for two streamConfig parameters `realtime.segment.flush.threshold.segment.size` and `realtime.segment.flush.threshold.time` can be determined based the provided information.
    * **Optimal Segment Size** Matrix of real-time segment size for each combination of numHost and numConsumptionHour.
    * **Consuming Memory per Host** Matrix of memory size for only consuming segments.
    * **Total Memory Used per Host** Matrix of total memory size for all real-time segments including consuming ones.
* Flagged Queries:
  * Flags the invalid or expensive queries.

We are planning to add more rules in the near future.

## Sample run

Input:

```javascript
{
  "schema":{
    "dimensionFieldSpecs": [
      {
        "cardinality": 10000,
        "dataType": "LONG",
        "name": "studentID"
      },
      {
        "averageLength": 8,
        "cardinality": 2000,
        "dataType": "STRING",
        "name": "firstName"
      },
      {
        "averageLength": 12,
        "cardinality": 2000,
        "dataType": "STRING",
        "name": "lastName"
      },
      {
        "averageLength": 6,
        "cardinality": 2,
        "dataType": "STRING",
        "name": "gender"
      },
      {
        "averageLength": 25,
        "cardinality": 100,
        "dataType": "STRING",
        "name": "subject"
      }
    ],
    "metricFieldSpecs": [
      {
        "cardinality": 5000,
        "dataType": "FLOAT",
        "name": "score"
      }
    ],
    "schemaName": "transcript"
  },
  "queriesWithWeights":{
    "select subject, count(*) from transcript where score > 3 and gender = 'MALE' group by subject": 0.5,
    "select subject, score from transcript where firstName = 'Tsubasa' and lastName = 'Oozora'": 0.5
  },
  "tableType": "OFFLINE",
  "numRecordsPerPush":100000000,
  "qps": 5,
  "latencySLA": 1000,
  "rulesToExecute": {
    "recommendRealtimeProvisioning": false
  }
}
```

Output:

```javascript
{
  "aggregateMetrics": false,
  "flaggedQueries": {
    "flaggedQueries": {}
  },
  "indexConfig": {
    "bloomFilterColumns": [],
    "invertedIndexColumns": [
      "gender"
    ],
    "noDictionaryColumns": [
      "studentID",
      "score"
    ],
    "onHeapDictionaryColumns": [],
    "rangeIndexColumns": [
      "score"
    ],
    "sortedColumn": "firstName",
    "sortedColumnOverwritten": true,
    "variedLengthDictionaryColumns": [
      "firstName",
      "lastName",
      "gender",
      "subject"
    ]
  },
  "partitionConfig": {
    "numKafkaPartitions": 0,
    "numPartitionsOffline": 1,
    "numPartitionsOfflineOverwritten": false,
    "numPartitionsRealtime": 1,
    "numPartitionsRealtimeOverwritten": false,
    "partitionDimension": "",
    "partitionDimensionOverwritten": false
  },
  "realtimeProvisioningRecommendations": {},
  "segmentSizeRecommendations": {
    "message": null,
    "numRowsPerSegment": 33333333,
    "numSegments": 3,
    "segmentSize": 482736662
  }
}
```
