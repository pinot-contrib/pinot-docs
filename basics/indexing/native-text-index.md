---
description: >-
  This page talks about native text indices and corresponding search
  functionality in Apache Pinot.
---

# Native Text Index

## Native text index

Pinot supports text indexing and search by building Lucene indices as _sidecars_ to the main Pinot segments. While this is a great technique, it essentially limits the avenues of optimizations that can be done for Pinot specific use cases of text search.

### How is Pinot different?

Pinot, like any other database/OLAP engine, does not need to conform to the entire full text search domain-specific language (DSL) that is traditionally used by full-text search (FTS) engines like ElasticSearch and Solr. In traditional SQL text search use cases, the majority of text searches belong to one of three patterns: prefix wildcard queries (like `pino*`), suffix wildcard queries (like `*inot`), and term queries (like `pinot`).

Pinot, like any other database/OLAP engine, does not need to conform to the entire full text search domain-specific language (DSL) that is traditionally used by full-text search (FTS) engines like ElasticSearch and Solr. In traditional SQL text search use cases, the majority of text searches belong to one of three patterns: prefix wildcard queries (like `pino*`), postfix or suffix wildcard queries (like `*inot`), and term queries (like `pinot`).

> > > > > > > 5718bf4 (Edits to five short indexing pages as part of site review) ======= Pinot, like any other database/OLAP engine, does not need to conform to the entire full text search domain-specific language (DSL) that is traditionally used by full-text search (FTS) engines like ElasticSearch and Solr. In traditional SQL text search use cases, the majority of text searches belong to one of three patterns: prefix wildcard queries (like `pino*`), suffix wildcard queries (like `*inot`), and term queries (like `pinot`). 586fc6f (Apply suggestions from code review)

### Native text indices in Pinot

In Pinot, native text indices are built from the ground up. They use a custom text-indexing engine, coupled with Pinot's powerful inverted indices, to provide a fast text search experience.

The benefits are that native text indices are 80-120% faster than Lucene-based indices for the text search use cases mentioned above. They are also 40% smaller on disk.

Native text indices support real-time text search. For `REALTIME` tables, native text indices allow data to be indexed in memory in the text index, while concurrently supporting text searches on the same index.

Historically, most text indices depend on the in-memory text index being written to first and then sealed, before searches are possible. This limits the freshness of the search, being near-real-time at best.

Native text indices come with a custom in-memory text index, which allows for real-time indexing and search.

### Searching Native Text Indices

The function, `TEXT\_CONTAINS`, supports text search on native text indices.

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, <search_expression>)
```

Examples:

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, "foo.*")
```

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, ".*bar")
```

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS (<column_name>, "foo")
```

`TEXT\_CONTAINS` can be combined using standard boolean operators

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_CONTAINS ("col1", "foo") AND TEXT_CONTAINS ("col2", "bar")
```

**Note:** `TEXT\_CONTAINS` supports regex and term queries and will work only on native indices. `TEXT\_CONTAINS` supports standard regex patterns (as used by `LIKE` in SQL Standard), so there might be some syntatical differences from Lucene queries.

### Creating Native Text Indices

Native text indices are created using field configurations. To indicate that an index type is native, specify it using `properties` in the field configuration:

```json
"fieldConfigList":[
  {
     "name":"text_col_1",
     "encodingType":"RAW",
     "indexTypes": ["TEXT"],
     "properties":{"fstType":"native"}
  }
]
```
