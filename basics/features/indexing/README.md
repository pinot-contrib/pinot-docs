---
description: This page describes the different indexing techniques available in Pinot
---

# Indexing

Pinot currently supports the following indexing techniques, where each of them have their own advantages in different query scenarios.

* [Forward Index](forward-index.md)
  * Dictionary-encoded forward index with bit compression
  * Raw value forward index
  * Sorted forward index with run-length encoding
* [Inverted Index](inverted-index.md)
  * Bitmap inverted index
  * Sorted inverted index
* [Star-tree Index](star-tree-index.md)
* [Range Index](range-index.md)

By default, Pinot will use `dictionary-encoded forward index` for each column. 

### Tuning Index

{% hint style="info" %}
If your use case is not site facing with a strict low latency requirement, inverted index will provide good performance for the most of use cases.   
  
You should start by adding an inverted index and if the query does not perform as per the expectations switch to  advanced indices such as sorted column and star-tree index.
{% endhint %}

