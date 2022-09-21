---
description: >-
  This page talks about native text indices and corresponding search
  functionality in Pinot
---

# Native Text Index

## History Of Text Indexing And Search in Pinot

Pinot supports text indexing and search by building Lucene indices as "sidecars" to the main Pinot segments. While this is a great technique, it essentially limits the avenues of optimizations that can be done for Pinot specific use cases of text search.

## How Is Pinot Different?

Pinot, or any other database/OLAP engine, do not need to conform to the entire full text search DSL that is traditionally used by FTS engines like ElasticSearch and Solr. Looking at traditional SQL like text search use cases, majority of text searches comprise of three patterns -- prefix wildcard queries, postfix wildcard queries and term queries.

## Native Text Indices in Pinot

Native text indices are built from the ground up. They use a custom text indexing engine, coupled with Pinot's powerful inverted indices, to provide a super fast text search experience.

## Benefits of Native Text Indices

Native text indices are 80-120% faster than Lucene based indices for the text search use cases mentioned above. They are also 40% smaller on disk.

## Real Time Indexing And Search

A new feature that native text indices support are real time text search. For REALTIME tables, native text indices allow data to be indexed in memory in the text index, while concurrently supporting text searches on the same index.

Historically, most text indices depend on the in memory text index being written to first and then sealed, before searches are possible. This limits the freshness of the search, being near real time at best.

Native text indices come with a custom in memory text index, which allows for real time indexing and search.

## Searching Native Text Indices

A new function, TEXT\_CONTAINS, is introduced for supporting text search on native text indices.

```
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, <search_expression>)
```

Examples:

```
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, "foo.*")
```

```
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, ".*bar")
```

```
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, "foo")
```

TEXT\_CONTAINS can be combined using standard boolean operators

```
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS ("col1", "foo") AND TEXT_CONTAINS ("col2", "bar")
```

Note that TEXT\_CONTAINS supports regex and term queries for now. Also, TEXT\_CONTAINS will work only on native indices.

**Note that TEXT\_CONTAINS supports standard regex patterns (as used by LIKE in SQL Standard). So there might be some syntatical changes from Lucene queries**

## Creating Native Text Indices

Native text indices are a type of text search index that Pinot supports, hence are created through the regular way of using field configs to configure a text index on a given field. To indicate that the index type is native, an additional property in the field config has to be specified:

```
"fieldConfigList":[
  {

     "name":"text_col_1",
     "encodingType":"RAW",
     "indexType":"TEXT",
     "properties":[{"fstType":"native"}]
  }
]
```
