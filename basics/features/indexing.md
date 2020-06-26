---
description: This page describes the different indexing techniques available in Pinot
---

# Indexing

Pinot currently supports the following index techniques, where each of them have their own advantages in different query scenarios. By default, Pinot will use `dictionary-encoded forward index` for each column.

## Forward index

### Dictionary-encoded forward index with bit compression \(default\)

For each unique value from a column, we assign an id to it, and build a dictionary from the id to the value. Then in the forward index, we only store the bit-compressed ids instead of the values. With few number of unique values, dictionary-encoding can significantly improve the space efficiency of the storage.

The below diagram shows the dictionary encoding for two columns with `integer` and `string` types. As seen in the `colA`, dictionary encoding will save significant amount of space for duplicated values. On the other hand, `colB` has no duplicated data. Dictionary encoding will not compress much data in this case where there are a lot of unique values in the column. For `string` type, we pick the length of the longest value and use it as the length for dictionary’s fixed length value array. In this case, padding overhead can be high if there are a large number of unique values for a column.

![\_images/dictionary.png](https://pinot.readthedocs.io/en/latest/_images/dictionary.png)

### Raw value forward index

In contrast to the dictionary-encoded forward index, raw value forward index directly stores values instead of ids.

Without the dictionary, the dictionary lookup step can be skipped for each value fetch. Also, the index can take advantage of the good locality of the values, thus improve the performance of scanning large number of values.

A typical use case to apply raw value forward index is when the column has a large number of unique values and the dictionary does not provide much compression. As seen the above diagram for dictionary encoding, scanning values with a dictionary involves a lot of random access because we need to perform dictionary look up. On the other hand, we can scan values sequentially with raw value forward index and this can improve performance a lot when applied appropriately.

![\_images/no-dictionary.png](https://pinot.readthedocs.io/en/latest/_images/no-dictionary.png)

Raw value forward index can be configured for a table by setting it in the table config as

```javascript
{
    "tableIndexConfig": {
        "noDictionaryColumns": [
            "column_name",
            ...
        ],
        ...
    }
}
```

#### Sorted forward index with run-length encoding

When a column is physically sorted, Pinot uses a sorted forward index with run-length encoding on top of the dictionary-encoding. Instead of saving dictionary ids for each document id, we store a pair of start and end document id for each value. \(The below diagram does not include dictionary encoding layer for simplicity.\)

![\_images/sorted-forward.png](https://pinot.readthedocs.io/en/latest/_images/sorted-forward.png)

Sorted forward index has the advantages of both good compression and data locality. Sorted forward index can also be used as inverted index.

Sorted index can be configured for a table by setting it in the table config as

```javascript
{
    "tableIndexConfig": {
        "sortedColumn": [
            "column_name"
        ],
        ...
    }
}
```

Real-time server will sort data on `sortedColumn` when generating segment internally. For offline push, input data needs to be sorted before running Pinot segment conversion and push job.

When applied correctly, one can find the following information on the segment metadata.

```bash
$ grep memberId <segment_name>/v3/metadata.properties | grep isSorted
column.memberId.isSorted = true
```

## Inverted index

### Bitmap inverted index

When inverted index is enabled for a column, Pinot maintains a map from each value to a bitmap, which makes value lookup to be constant time. When you have a column that is used for filtering frequently, adding an inverted index will improve the performance greatly.

Inverted index can be configured for a table by setting it in the table config as

```javascript
{
    "tableIndexConfig": {
        "invertedIndexColumns": [
            "column_name",
            ...
        ],
        ...
    }
}
```

### Sorted inverted index

Sorted forward index can directly be used as inverted index, with `log(n)` time lookup and it can benefit from data locality.

For the below example, if the query has a filter on `memberId`, Pinot will perform binary search on `memberId` values to find the range pair of docIds for corresponding filtering value. If the query requires to scan values for other columns after filtering, values within the range docId pair will be located together; therefore, we can benefit a lot from data locality.![\_images/sorted-inverted.png](https://pinot.readthedocs.io/en/latest/_images/sorted-inverted.png)

Sorted index performs much better than inverted index; however, it can only be applied to one column. When the query performance with inverted index is not good enough and most of queries have a filter on a specific column \(e.g. memberId\), sorted index can improve the query performance.

## Star-tree index

Unlike other index techniques which work on single column, Star-Tree index is built on multiple columns, and utilize the pre-aggregated results to significantly reduce the number of values to be processed, thus improve the query performance. 

One of the biggest challenges in realtime OLAP systems is achieving and maintaining tight SLA’s on latency and throughput on large data sets. Existing techniques such as sorted index or inverted index help improve query latencies, but speed-ups are still limited by number of documents necessary to process for computing the results. On the other hand, pre-aggregating the results ensures a constant upper bound on query latencies, but can lead to storage space explosion.

Here we introduce **star-tree** index to utilize the pre-aggregated documents in a smart way to achieve low query latencies but also use the storage space efficiently for aggregation/group-by queries.

### Existing solutions

Consider the following data set as an example to discuss the existing approaches:

| Country | Browser | Locale | Impressions |
| :--- | :--- | :--- | :--- |
| CA | Chrome | en | 400 |
| CA | Firefox | fr | 200 |
| MX | Safari | es | 300 |
| MX | Safari | en | 100 |
| USA | Chrome | en | 600 |
| USA | Firefox | es | 200 |
| USA | Firefox | en | 400 |

#### Sorted index

In this approach, data is sorted on a primary key, which is likely to appear as filter in most queries in the query set.

This reduces the time to search the documents for a given primary key value from linear scan _O\(n\)_ to binary search _O\(logn\)_, and also keeps good locality for the documents selected.

While this is a good improvement over linear scan, there are still a few issues with this approach:

* While sorting on one column does not require additional space, sorting on additional columns would require additional storage space to re-index the records for the various sort orders.
* While search time is reduced from _O\(n\)_ to _O\(logn\)_, overall latency is still a function of total number of documents need to be processed to answer a query.

#### Inverted index

In this approach, for each value of a given column, we maintain a list of document id’s where this value appears.

Below are the inverted indexes for columns ‘Browser’ and ‘Locale’ for our example data set:

| Browser | Doc Id |
| :--- | :--- |
| Firefox | 1,5,6 |
| Chrome | 0,4 |
| Safari | 2,3 |

| Locale | Doc Id |
| :--- | :--- |
| en | 0,3,4,6 |
| es | 2,5 |
| fr | 1 |

For example, if we want to get all the documents where ‘Browser’ is ‘Firefox’, we can simply look up the inverted index for ‘Browser’ and identify that it appears in documents \[1, 5, 6\].

Using inverted index, we can reduce the search time to constant time _O\(1\)_. However, the query latency is still a function of the selectivity of the query, i.e. increases with the number of documents need to be processed to answer the query.

#### Pre-aggregation

In this technique, we pre-compute the answer for a given query set upfront.

In the example below, we have pre-aggregated the total impressions for each country:

| Country | Impressions |
| :--- | :--- |
| CA | 600 |
| MX | 400 |
| USA | 1200 |

Doing so makes answering queries about total impressions for a country just a value lookup, by eliminating the need of processing a large number of documents. However, to be able to answer with multiple predicates implies pre-aggregating for various combinations of different dimensions. This leads to exponential explosion in storage space.

### Star-tree solution

On one end of the spectrum we have indexing techniques that improve search times with limited increase in space, but do not guarantee a hard upper bound on query latencies. On the other end of the spectrum we have pre-aggregation techniques that offer hard upper bound on query latencies, but suffer from exponential explosion of storage space.![../\_images/space-time.png](https://pinot.readthedocs.io/en/latest/_images/space-time.png)

Space-Time Trade Off Between Different Techniques

We propose the Star-Tree data structure that offers a configurable trade-off between space and time and allows us to achieve hard upper bound for query latencies for a given use case. In the following sections we will define the Star-Tree data structure, and discuss how it is utilized within Pinot for achieving low latencies with high throughput.

### Definitions

**Tree structure**

Star-tree is a tree data structure that is consisted of the following properties:![../\_images/structure.png](https://pinot.readthedocs.io/en/latest/_images/structure.png)

Star-tree Structure

* **Root Node** \(Orange\): Single root node, from which the rest of the tree can be traversed.
* **Leaf Node** \(Blue\): A leaf node can containing at most _T_ records, where _T_ is configurable.
* **Non-leaf Node** \(Green\): Nodes with more than _T_ records are further split into children nodes.
* **Star-Node** \(Yellow\): Non-leaf nodes can also have a special child node called the Star-Node. This node contains the pre-aggregated records after removing the dimension on which the data was split for this level.
* **Dimensions Split Order** \(\[D1, D2\]\): Nodes at a given level in the tree are split into children nodes on all values of a particular dimension. The dimensions split order is an ordered list of dimensions that is used to determine the dimension to split on for a given level in the tree.

**Node properties**

The properties stored in each node are as follows:

* **Dimension**: The dimension which the node is split on
* **Start/End Document Id**: The range of documents this node points to
* **Aggregated Document Id**: One single document which is the aggregation result of all documents pointed by this node

### Index generation

Star-tree index is generated in the following steps:

* The data is first projected as per the _dimensionsSplitOrder_. Only the dimensions from the split order are reserved, others are dropped. For each unique combination of reserved dimensions, metrics are aggregated per configuration. The aggregated documents are written to a file and served as the initial Star-Tree documents \(separate from the original documents\).
* Sort the Star-Tree documents based on the _dimensionsSplitOrder_. It is primary-sorted on the first dimension in this list, and then secondary sorted on the rest of the dimensions based on their order in the list. Each node in the tree points to a range in the sorted documents.
* The tree structure can be created recursively \(starting at root node\) as follows:
  * If a node has more than _T_ records, it is split into multiple children nodes, one for each value of the dimension in the split order corresponding to current level in the tree.
  * A Star-Node can be created \(per configuration\) for the current node, by dropping the dimension being split on, and aggregating the metrics for rows containing dimensions with identical values. These aggregated documents are appended to the end of the Star-Tree documents.

    If there is only one value for the current dimension, Star-Node won’t be created because the documents under the Star-Node are identical to the single node.
* The above step is repeated recursively until there are no more nodes to split.
* Multiple Star-Trees can be generated based on different configurations \(_dimensionsSplitOrder_, _aggregations_, _T_\)

#### Aggregation

Aggregation is configured as a pair of aggregation function and the column to apply the aggregation.

All types of aggregation function with bounded-sized intermediate result are supported.

**Supported functions**

* COUNT
* MIN
* MAX
* SUM
* AVG
* MINMAXRANGE
* DISTINCTCOUNTHLL
* PERCENTILEEST
* PERCENTILETDIGEST

**Unsupported functions**

* DISTINCTCOUNT: Intermediate result _Set_ is unbounded
* PERCENTILE: Intermediate result _List_ is unbounded

#### Index generation configuration

Multiple index generation configurations can be provided to generate multiple star-trees. Each configuration should contain the following properties:

* **dimensionsSplitOrder**: An ordered list of dimension names can be specified to configure the split order. Only the dimensions in this list are reserved in the aggregated documents. The nodes will be split based on the order of this list. For example, split at level _i_ is performed on the values of dimension at index _i_ in the list.
* **skipStarNodeCreationForDimensions** \(Optional, default empty\): A list of dimension names for which to not create the Star-Node.
* **functionColumnPairs**: A list of aggregation function and column pairs \(split by double underscore “\_\_”\). E.g. **SUM\_\_Impressions** \(_SUM_ of column _Impressions_\)
* **maxLeafRecords** \(Optional, default 10000\): The threshold _T_ to determine whether to further split each node.

#### Example

For our example data set, with the following example configuration, the tree and documents should be something like below.

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
    "maxLeafRecords": 1
  }],
  ...
}
```

#### **Default index generation configuration**

Default star-tree index can be added to the segment with a boolean config _**enableDefaultStarTree**_ under the _tableIndexConfig_. 

The default star-tree will have the following configuration:

* All dictionary-encoded single-value dimensions with cardinality smaller or equal to a threshold \(10000\) will be included in the _dimensionsSplitOrder_, sorted by their cardinality in descending order.
* All dictionary-encoded Time/DateTime columns will be appended to the _dimensionsSplitOrder_ following the dimensions, sorted by their cardinality in descending order. Here we assume that time columns will be included in most queries as the range filter column and/or the group by column, so for better performance, we always include them as the last elements in the _dimensionsSplitOrder_.
* Include COUNT\(\*\) and SUM for all numeric metrics in the _functionColumnPairs._
* Use default _maxLeafRecords_ ****\(10000\).

#### **Tree structure**

The values in the parentheses are the aggregated sum of _Impressions_ for all the documents under the node.

![../\_images/example.png](https://pinot.readthedocs.io/en/latest/_images/example.png)

**Star-tree documents**

| Country | Browser | Locale | SUM\_\_Impressions |
| :--- | :--- | :--- | :--- |
| CA | Chrome | en | 400 |
| CA | Firefox | fr | 200 |
| MX | Safari | en | 100 |
| MX | Safari | es | 300 |
| USA | Chrome | en | 600 |
| USA | Firefox | en | 400 |
| USA | Firefox | es | 200 |
| CA | \* | en | 400 |
| CA | \* | fr | 200 |
| CA | \* | \* | 600 |
| MX | Safari | \* | 400 |
| USA | Firefox | \* | 600 |
| USA | \* | en | 1000 |
| USA | \* | es | 200 |
| USA | \* | \* | 1200 |
| \* | Chrome | en | 1000 |
| \* | Firefox | en | 400 |
| \* | Firefox | es | 200 |
| \* | Firefox | fr | 200 |
| \* | Firefox | \* | 800 |
| \* | Safari | en | 100 |
| \* | Safari | es | 300 |
| \* | Safari | \* | 400 |
| \* | \* | en | 1500 |
| \* | \* | es | 500 |
| \* | \* | fr | 200 |
| \* | \* | \* | 2200 |

### Query execution

For query execution, the idea is to first check metadata to determine whether the query can be solved with the Star-Tree documents, then traverse the Star-Tree to identify documents that satisfy all the predicates. After applying any remaining predicates that were missed while traversing the Star-Tree to the identified documents, apply aggregation/group-by on the qualified documents.

The algorithm to traverse the tree can be described as follows:

* Start from root node.
* For each level, what child node\(s\) to select depends on whether there are any predicates/group-by on the split dimension for the level in the query.
  * If there is no predicate or group-by on the split dimension, select the Star-Node if exists, or all child nodes to traverse further.
  * If there are predicate\(s\) on the split dimension, select the child node\(s\) that satisfy the predicate\(s\).
  * If there is no predicate, but there is a group-by on the split dimension, select all child nodes except Star-Node.
* Recursively repeat the previous step until all leaf nodes are reached, or all predicates are satisfied.
* Collect all the documents pointed by the selected nodes.
  * If all predicates and group-bys are satisfied, pick the single aggregated document from each selected node.
  * Otherwise, collect all the documents in the document range from each selected node.

### Notes on index tuning

If your use case is not site facing with a strict low latency requirement, inverted index will perform good enough for the most of use cases. We recommend to start with adding inverted index and if the query does not perform good enough, a user can consider to use more advanced indices such as sorted column and star-tree index.  


