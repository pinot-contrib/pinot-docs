---
description: This page describes the indexing techniques available in Apache Pinot.
---

# Star-tree index

In this page you will learn what a star-tree index is and gain a conceptual understanding of how one works.

Unlike other index techniques which work on a single column, the star-tree index is built on multiple columns and utilizes pre-aggregated results to significantly reduce the number of values to be processed, resulting in improved query performance.

One of the biggest challenges in real-time OLAP systems is achieving and maintaining tight SLAs on latency and throughput on large data sets. Existing techniques such as [sorted index](forward-index.md) or [inverted index](inverted-index.md) help improve query latencies, but speed-ups are still limited by the number of documents that need to be processed to compute results. On the other hand, pre-aggregating the results ensures a constant upper bound on query latencies, but can lead to storage space explosion.

Use the **star-tree** index to utilize pre-aggregated documents to achieve both low query latencies and efficient use of storage space for aggregation and group-by queries.

{% embed url="https://www.youtube.com/watch?v=bwO0HSXguFA" %}

## Existing solutions

Consider the following data set, which is used here as an example to discuss these indexes:

| Country | Browser | Locale | Impressions |
| ------- | ------- | ------ | ----------- |
| CA      | Chrome  | en     | 400         |
| CA      | Firefox | fr     | 200         |
| MX      | Safari  | es     | 300         |
| MX      | Safari  | en     | 100         |
| USA     | Chrome  | en     | 600         |
| USA     | Firefox | es     | 200         |
| USA     | Firefox | en     | 400         |

### Sorted index

In this approach, data is sorted on a primary key, which is likely to appear as filter in most queries in the query set.

This reduces the time to search the documents for a given primary key value from linear scan _O(n)_ to binary search _O(logn)_, and also keeps good locality for the documents selected.

While this is a significant improvement over linear scan, there are still a few issues with this approach:

* While sorting on one column does not require additional space, sorting on additional columns requires additional storage space to re-index the records for the various sort orders.
* While search time is reduced from _O(n)_ to _O(logn)_, overall latency is still a function of the total number of documents that need to be processed to answer a query.

### Inverted index

In this approach, for each value of a given column, we maintain a list of document id’s where this value appears.

Below are the inverted indexes for columns ‘Browser’ and ‘Locale’ for our example data set:

| Browser | Doc Id |
| ------- | ------ |
| Firefox | 1,5,6  |
| Chrome  | 0,4    |
| Safari  | 2,3    |

| Locale | Doc Id  |
| ------ | ------- |
| en     | 0,3,4,6 |
| es     | 2,5     |
| fr     | 1       |

For example, if we want to get all the documents where ‘Browser’ is ‘Firefox’, we can look up the inverted index for ‘Browser’ and identify that it appears in documents \[1, 5, 6].

Using an inverted index, we can reduce the search time to constant time _O(1)_. The query latency, however, is still a function of the selectivity of the query: it increases with the number of documents that need to be processed to answer the query.

### Pre-aggregation

In this technique, we pre-compute the answer for a given query set upfront.

In the example below, we have pre-aggregated the total impressions for each country:

| Country | Impressions |
| ------- | ----------- |
| CA      | 600         |
| MX      | 400         |
| USA     | 1200        |

With this approach, answering queries about total impressions for a country is a value lookup, because we have eliminated the need to process a large number of documents. However, to be able to answer queries that have multiple predicates means we would need to pre-aggregate for various combinations of different dimensions, which leads to an exponential increase in storage space.

## Star-tree solution

On one end of the spectrum we have indexing techniques that improve search times with a limited increase in space, but don't guarantee a hard upper bound on query latencies. On the other end of the spectrum, we have pre-aggregation techniques that offer a hard upper bound on query latencies, but suffer from exponential explosion of storage space

![](../../.gitbook/assets/space-time.png)

The star-tree data structure offers a configurable trade-off between space and time and lets us achieve a hard upper bound for query latencies for a given use case. The following sections cover the star-tree data structure, and explain how Pinot uses this structure to achieve low latencies with high throughput.

### Definitions

**Tree structure**

The star-tree index stores data in a structure that consists of the following properties:

![Star-tree index structure](../../.gitbook/assets/structure.png)

* **Root node** (Orange): Single root node, from which the rest of the tree can be traversed.
* **Leaf node** (Blue): A leaf node can containing at most _T_ records, where _T_ is configurable.
* **Non-leaf node** (Green): Nodes with more than _T_ records are further split into children nodes.
* **Star node** (Yellow): Non-leaf nodes can also have a special child node called the star node. This node contains the pre-aggregated records after removing the dimension on which the data was split for this level.
* **Dimensions split order** (\[D1, D2]): Nodes at a given level in the tree are split into children nodes on all values of a particular dimension. The dimensions split order is an ordered list of dimensions that is used to determine the dimension to split on for a given level in the tree.

**Node properties**

The properties stored in each node are as follows:

* **Dimension**: The dimension that the node is split on
* **Start/End Document Id**: The range of documents this node points to
* **Aggregated Document Id**: One single document that is the aggregation result of all documents pointed by this node

### Index generation

The star-tree index is generated in the following steps:

* The data is first projected as per the _dimensionsSplitOrder_. Only the dimensions from the split order are reserved, others are dropped. For each unique combination of reserved dimensions, metrics are aggregated per configuration. The aggregated documents are written to a file and served as the initial star-tree documents (separate from the original documents).
* Sort the star-tree documents based on the _dimensionsSplitOrder_. It is primary-sorted on the first dimension in this list, and then secondary sorted on the rest of the dimensions based on their order in the list. Each node in the tree points to a range in the sorted documents.
* The tree structure can be created recursively (starting at root node) as follows:
  * If a node has more than _T_ records, it is split into multiple children nodes, one for each value of the dimension in the split order corresponding to current level in the tree.
  *   A star node can be created (per configuration) for the current node, by dropping the dimension being split on, and aggregating the metrics for rows containing dimensions with identical values. These aggregated documents are appended to the end of the star-tree documents.

      If there is only one value for the current dimension, a star node won’t be created because the documents under the star node are identical to the single node.
* The above step is repeated recursively until there are no more nodes to split.
* Multiple star-trees can be generated based on different configurations (_dimensionsSplitOrder_, _aggregations_, _T_)

### Aggregation

Aggregation is configured as a pair of aggregation functions and the column to apply the aggregation.

All types of aggregation function that have a bounded-sized intermediate result are supported.

**Supported functions**

* COUNT
* MIN
* MAX
* SUM
* AVG
* MIN\_MAX\_RANGE
* DISTINCT\_COUNT\_HLL
* PERCENTILE\_EST
* PERCENTILE\_TDIGEST
* DISTINCT\_COUNT\_BITMAP
  * NOTE: The intermediate result _RoaringBitmap_ is not bounded-sized, use carefully on high cardinality columns.

**Unsupported functions**

* DISTINCT\_COUNT
  * Intermediate result _Set_ is unbounded.
* SEGMENT\_PARTITIONED\_DISTINCT\_COUNT:
  * Intermediate result _Set_ is unbounded.
* PERCENTILE
  * Intermediate result _List_ is unbounded.

**Functions to be supported**

* DISTINCT\_COUNT\_THETA\_SKETCH
* ST\_UNION

### Index generation configuration

Multiple index generation configurations can be provided to generate multiple star-trees. Each configuration should contain the following properties:

* **dimensionsSplitOrder**: An ordered list of dimension names can be specified to configure the split order. Only the dimensions in this list are reserved in the aggregated documents. The nodes will be split based on the order of this list. For example, split at level _i_ is performed on the values of dimension at index _i_ in the list.
  * The star-tree dimension does not have to be a dimension column in the table, it can also be time column, date-time column, or metric column if necessary.
  * The star-tree dimension column should be dictionary encoded in order to generate the star-tree index.
  * All columns in the filter and group-by clause of a query should be included in this list in order to use the star-tree index.
* **skipStarNodeCreationForDimensions** (Optional, default empty): A list of dimension names for which to not create the Star-Node.
* **functionColumnPairs**: A list of aggregation function and column pairs (split by double underscore “\_\_”). E.g. **SUM\_\_Impressions** (_SUM_ of column _Impressions_) or **COUNT\_\_\***.
  * The column within the function-column pair can be either dictionary encoded or raw.
  * All aggregations of a query should be included in this list in order to use the star-tree index.
* **maxLeafRecords** (Optional, default 10000): The threshold _T_ to determine whether to further split each node.

#### Default index generation configuration

A default star-tree index can be added to a segment by using the boolean config _**enableDefaultStarTree**_ under the _tableIndexConfig_.

A default star-tree will have the following configuration:

* All dictionary-encoded single-value dimensions with cardinality smaller or equal to a threshold (10000) will be included in the _dimensionsSplitOrder_, sorted by their cardinality in descending order.
* All dictionary-encoded Time/DateTime columns will be appended to the \_dimensionsSplitOrder \_following the dimensions, sorted by their cardinality in descending order. Here we assume that time columns will be included in most queries as the range filter column and/or the group by column, so for better performance, we always include them as the last elements in the _dimensionsSplitOrder_.
* Include COUNT(\*) and SUM for all numeric metrics in the _functionColumnPairs._
* Use default _maxLeafRecords_ (10000).

### Example

For our example data set, in order to solve the following query efficiently:

```javascript
SELECT SUM(Impressions) 
FROM myTable 
WHERE Country = 'USA' 
AND Browser = 'Chrome' 
GROUP BY Locale
```

We may config the star-tree index as follows:

```javascript
"tableIndexConfig": {
  "starTreeIndexConfigs": [{
    "dimensionsSplitOrder": [
      "Country",
      "Browser",
      "Locale"
    ],
    "skipStarNodeCreationForDimensions": [
    ],
    "functionColumnPairs": [
      "SUM__Impressions"
    ],
    "maxLeafRecords": 10000
  }],
  ...
}
```

The star-tree and documents should be something like below:

### Tree structure

The values in the parentheses are the aggregated sum of _Impressions_ for all the documents under the node.

![](../../.gitbook/assets/example.png)

**Star-tree documents**

| Country | Browser | Locale | SUM\_\_Impressions |
| ------- | ------- | ------ | ------------------ |
| CA      | Chrome  | en     | 400                |
| CA      | Firefox | fr     | 200                |
| MX      | Safari  | en     | 100                |
| MX      | Safari  | es     | 300                |
| USA     | Chrome  | en     | 600                |
| USA     | Firefox | en     | 400                |
| USA     | Firefox | es     | 200                |
| CA      | \*      | en     | 400                |
| CA      | \*      | fr     | 200                |
| CA      | \*      | \*     | 600                |
| MX      | Safari  | \*     | 400                |
| USA     | Firefox | \*     | 600                |
| USA     | \*      | en     | 1000               |
| USA     | \*      | es     | 200                |
| USA     | \*      | \*     | 1200               |
| \*      | Chrome  | en     | 1000               |
| \*      | Firefox | en     | 400                |
| \*      | Firefox | es     | 200                |
| \*      | Firefox | fr     | 200                |
| \*      | Firefox | \*     | 800                |
| \*      | Safari  | en     | 100                |
| \*      | Safari  | es     | 300                |
| \*      | Safari  | \*     | 400                |
| \*      | \*      | en     | 1500               |
| \*      | \*      | es     | 500                |
| \*      | \*      | fr     | 200                |
| \*      | \*      | \*     | 2200               |

## Query execution

For query execution, the idea is to first check metadata to determine whether the query can be solved with the star-tree documents, then traverse the Star-Tree to identify documents that satisfy all the predicates. After applying any remaining predicates that were missed while traversing the star-tree to the identified documents, apply aggregation/group-by on the qualified documents.

The algorithm to traverse the tree can be described as follows:

* Start from root node.
* For each level, what child node(s) to select depends on whether there are any predicates/group-by on the split dimension for the level in the query.
  * If there is no predicate or group-by on the split dimension, select the Star-Node if exists, or all child nodes to traverse further.
  * If there are predicate(s) on the split dimension, select the child node(s) that satisfy the predicate(s).
  * If there is no predicate, but there is a group-by on the split dimension, select all child nodes except Star-Node.
* Recursively repeat the previous step until all leaf nodes are reached, or all predicates are satisfied.
* Collect all the documents pointed by the selected nodes.
  * If all predicates and group-by's are satisfied, pick the single aggregated document from each selected node.
  * Otherwise, collect all the documents in the document range from each selected node.note

{% hint style="warning" %}
There is a known bug which can mistakenly apply a star-tree index to queries with the OR operator on top of nested AND or NOT operators in the filter that cannot be solved with star-tree, and cause wrong results. E.g. `SELECT COUNT(*) FROM myTable WHERE (A = 1 AND B = 2) OR A = 2`. This bug affects release `0.9.0`, `0.9.1`, `0.9.2`, `0.9.3`, `0.10.0`.
{% endhint %}
