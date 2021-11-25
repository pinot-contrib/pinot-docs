---
description: This page talks about support for text search functionality in Pinot.
---

# Text search support

## Why do we need text search?

Pinot supports super-fast query processing through its indexes on non-BLOB like columns. Queries with exact match filters are run efficiently through a combination of dictionary encoding, inverted index, and sorted index.&#x20;

It would be useful for a query like the following:

```sql
SELECT COUNT(*) 
FROM Foo 
WHERE STRING_COL = "ABCDCD" 
AND INT_COL > 2000
```

This query does exact matches on two columns of type STRING and INT respectively.

For arbitrary text data that falls into the BLOB/CLOB territory, we need more than exact matches. Users are interested in doing regex, phrase, fuzzy queries on BLOB like data. Before 0.3.0, one had to use [regexp\_like](https://apache-pinot.gitbook.io/apache-pinot-cookbook/pinot-user-guide/pinot-query-language#wild-card-match-in-where-clause-only) to achieve this. However, this was scan based which was not performant and features like fuzzy search (edit distance search) were not possible.

In version 0.3.0, we added support for text indexes to efficiently do arbitrary search on STRING columns where each column value is a large BLOB of text. This can be achieved by using the new built-in function TEXT\_MATCH.

```sql
SELECT COUNT(*) 
FROM Foo 
WHERE TEXT_MATCH (<column_name>, <search_expression)
```

where \<column\_name> is the column text index is created on and **\<search\_expression>** can be:

| **Search Expression Type** | **Example**                                               |
| -------------------------- | --------------------------------------------------------- |
| Phrase query               | TEXT\_MATCH (\<column\_name>, '\\"distributed system\\"') |
| Term Query                 | TEXT\_MATCH (\<column\_name>, 'Java')                     |
| Boolean Query              | TEXT\_MATCH (\<column\_name>, 'Java and c++')             |
| Prefix Query               | TEXT\_MATCH (\<column\_name>, 'stream\*')                 |
| Regex Query                | TEXT\_MATCH (\<column\_name>, '/Exception.\*/')           |

## Sample Datasets

Text search should ideally be used on STRING columns where doing standard filter operations (EQUALITY, RANGE, BETWEEN) doesn't fit the bill because each column value is a reasonably large blob of text.

### Apache Access Log

Consider the following snippet from Apache access log. Each line in the log consists of arbitrary data (IP addresses, URLs, timestamps, symbols etc) and represents a column value. Data like this is a good candidate for doing text search.

Let's say the following snippet of data is stored in ACCESS\_LOG\_COL column in Pinot table.

```
109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-
109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
46.72.177.4 - - [12/Dec/2015:18:31:08 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
46.72.177.4 - - [12/Dec/2015:18:31:08 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
83.167.113.100 - - [12/Dec/2015:18:31:25 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
83.167.113.100 - - [12/Dec/2015:18:31:25 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
95.29.198.15 - - [12/Dec/2015:18:32:10 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
95.29.198.15 - - [12/Dec/2015:18:32:11 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
109.184.11.34 - - [12/Dec/2015:18:32:56 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
109.184.11.34 - - [12/Dec/2015:18:32:56 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
91.227.29.79 - - [12/Dec/2015:18:33:51 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"
```

Few examples of search queries on this data:

**Count the number of GET requests.**

```sql
SELECT COUNT(*) 
FROM MyTable 
WHERE TEXT_MATCH(ACCESS_LOG_COL, 'GET')
```

**Count the number of POST requests that have administrator in the URL (administrator/index)**

```sql
SELECT COUNT(*) 
FROM MyTable 
WHERE TEXT_MATCH(ACCESS_LOG_COL, 'post AND administrator AND index')
```

**Count the number of POST requests that have a particular URL and handled by Firefox browser**

```sql
SELECT COUNT(*) 
FROM MyTable 
WHERE TEXT_MATCH(ACCESS_LOG_COL, 'post AND administrator AND index AND firefox')
```

### Resume text

Consider another example of simple resume text. Each line in the file represents skill-data from resumes of different candidates

Let's say the following snippet of data is stored in _SKILLS\_COL_ column in Pinot table. Each line in the input text represents a column value.

```
Distributed systems, Java, C++, Go, distributed query engines for analytics and data warehouses, Machine learning, spark, Kubernetes, transaction processing
Java, Python, C++, Machine learning, building and deploying large scale production systems, concurrency, multi-threading, CPU processing
C++, Python, Tensor flow, database kernel, storage, indexing and transaction processing, building large scale systems, Machine learning
Amazon EC2, AWS, hadoop, big data, spark, building high performance scalable systems, building and deploying large scale production systems, concurrency, multi-threading, Java, C++, CPU processing
Distributed systems, database development, columnar query engine, database kernel, storage, indexing and transaction processing, building large scale systems
Distributed systems, Java, realtime streaming systems, Machine learning, spark, Kubernetes, distributed storage, concurrency, multi-threading
CUDA, GPU, Python, Machine learning, database kernel, storage, indexing and transaction processing, building large scale systems
Distributed systems, Java, database engine, cluster management, docker image building and distribution
Kubernetes, cluster management, operating systems, concurrency, multi-threading, apache airflow, Apache Spark,
Apache spark, Java, C++, query processing, transaction processing, distributed storage, concurrency, multi-threading, apache airflow
Big data stream processing, Apache Flink, Apache Beam, database kernel, distributed query engines for analytics and data warehouses
CUDA, GPU processing, Tensor flow, Pandas, Python, Jupyter notebook, spark, Machine learning, building high performance scalable systems
Distributed systems, Apache Kafka, publish-subscribe, building and deploying large scale production systems, concurrency, multi-threading, C++, CPU processing, Java
Realtime stream processing, publish subscribe, columnar processing for data warehouses, concurrency, Java, multi-threading, C++,
```

Few examples of search queries on this data:

**Count the number of candidates that have "machine learning" and "gpu processing"** - a phrase search (more on this further in the document) where we are looking for exact match of phrases "machine learning" and "gpu processing" not necessarily in the same order in original data.

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"Machine learning\" AND \"gpu processing\"')
```

**Count the number of candidates that have "distributed systems" and either 'Java' or 'C++'** - a combination of searching for exact phrase "distributed systems" along with other terms.

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"distributed systems\" AND (Java C++)')
```

### Query Log

Consider a snippet from a log file containing SQL queries handled by a database. Each line (query) in the file represents a column value in QUERY\_LOG\_COL column in Pinot table.

```sql
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1560988800000 AND 1568764800000 GROUP BY dimensionCol3 TOP 2500
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1560988800000 AND 1568764800000 GROUP BY dimensionCol3 TOP 2500
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1545436800000 AND 1553212800000 GROUP BY dimensionCol3 TOP 2500
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1537228800000 AND 1537660800000 GROUP BY dimensionCol3 TOP 2500
SELECT dimensionCol2, dimensionCol4, timestamp, dimensionCol5, dimensionCol6 FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1561366800000 AND 1561370399999 AND dimensionCol3 = 2019062409 LIMIT 10000
SELECT dimensionCol2, dimensionCol4, timestamp, dimensionCol5, dimensionCol6 FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1563807600000 AND 1563811199999 AND dimensionCol3 = 2019072215 LIMIT 10000
SELECT dimensionCol2, dimensionCol4, timestamp, dimensionCol5, dimensionCol6 FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1563811200000 AND 1563814799999 AND dimensionCol3 = 2019072216 LIMIT 10000
SELECT dimensionCol2, dimensionCol4, timestamp, dimensionCol5, dimensionCol6 FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1566327600000 AND 1566329400000 AND dimensionCol3 = 2019082019 LIMIT 10000
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1560834000000 AND 1560837599999 AND dimensionCol3 = 2019061805 LIMIT 0
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1560870000000 AND 1560871800000 AND dimensionCol3 = 2019061815 LIMIT 0
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1560871800001 AND 1560873599999 AND dimensionCol3 = 2019061815 LIMIT 0
SELECT count(dimensionCol2) FROM FOO WHERE dimensionCol1 = 18616904 AND timestamp BETWEEN 1560873600000 AND 1560877199999 AND dimensionCol3 = 2019061816 LIMIT 0
```

Few examples of search queries on this data:

**Count the number of queries that have GROUP BY**

```sql
SELECT COUNT(*) 
FROM MyTable 
WHERE TEXT_MATCH(QUERY_LOG_COL, '\"group by\"')
```

**Count the number of queries that have the SELECT count... pattern**

```sql
SELECT COUNT(*) 
FROM MyTable 
WHERE TEXT_MATCH(QUERY_LOG_COL, '\"select count\"')
```

**Count the number of queries that use BETWEEN filter on timestamp column along with GROUP BY**

```sql
SELECT COUNT(*) 
FROM MyTable 
WHERE TEXT_MATCH(QUERY_LOG_COL, '\"timestamp between\" AND \"group by\"')
```

[Further sections](https://apache-pinot.gitbook.io/apache-pinot-cookbook/text-search-support#writing-text-search-queries) in the document cover several concrete examples on each kind of query and step-by-step guide on how to write text search queries in Pinot.

## Current restrictions

Currently we support text search in a restricted manner. More specifically, we have the following constraints:

* The column type should be STRING.
* The column should be single-valued.
* Co-existence of text index with other Pinot indexes is currently not supported.

The last two restrictions are going to be relaxed very soon in the upcoming releases.

### Co-existence with other indexes

Currently, a column in Pinot can be dictionary encoded or stored RAW. Furthermore, we can create inverted index on the dictionary encoded column. We can also create a sorted index on the dictionary encoded column.

Text index is an addition to the type of **per-column indexes** users can create in Pinot. However, the current implementation supports text index on RAW column. In other words, the column should not be dictionary encoded. As we **relax this constraint in upcoming releases**, text index can be created on a dictionary encoded column that also has other indexes (inverted, sorted etc).

## How to enable text index?

Similar to other indexes, users can enable text index on a column through table config. As part of text-search feature, we have also introduced a new generic way of specifying the per-column encoding and index information. In the table config, there will be a new section with name "fieldConfigList".

{% hint style="warning" %}
`fieldConfigList`is currently ONLY used for text indexes. Our plan is to migrate all other indexes to this model. We are going to do that in upcoming releases and accordingly modify user documentation. So **please continue** to specify other index info in table config as you have done till now and use the `fieldConfigList` **only for text indexes**.
{% endhint %}

```javascript
"fieldConfigList":[
  {
     "name":"text_col_1",
     "encodingType":"RAW",
     "indexType":"TEXT"
  },
  {
     "name":"text_col_2",
     "encodingType":"RAW",
     "indexType":"TEXT"
  }
]
```

"fieldConfigList" will be a new section in table config. It is essentially a list of per-column encoding and index information. In the above example, the list contains text index information for two columns text\_col\_1 and text\_col\_2. Each object in fieldConfigList contains the following information

* name - Name of the column text index is enabled on
* encodingType - As mentioned earlier, we can store a column either as RAW or dictionary encoded. Since for now we have a restriction on the text index, this should always be RAW.
* indexType - This should be TEXT.

Since we haven't yet removed the old way of specifying the index info, each column that has a text index should also be specified as `noDictionaryColumns` in `tableIndexConfig`:

```javascript
"tableIndexConfig": {
   "noDictionaryColumns": [
     "text_col_1",
     "text_col_2"
 ]}
```

The above mechanism can be used to configure text indexes in the following scenarios:

* Adding a new table with text index enabled on one or more columns.
* Adding a new column with text index enabled to an existing table.
* Enabling text index on an existing column.

## Text Index Creation

Once the text index is enabled on one or more columns through table config, our segment generation code will pick up the config and automatically create text index (per column). This is exactly how other indexes in Pinot are created.

Text index is supported for both offline and real-time segments.

### Text parsing and tokenization

The original text document (a value in the column with text index enabled) is parsed, tokenized and individual "indexable" terms are extracted. These terms are inserted into the index.

Pinot's text index is built on top of Lucene. Lucene's **standard english text tokenizer** generally works well for most classes of text. We might want to build custom text parser and tokenizer to suit particular user requirements. Accordingly, we can make this configurable for the user to specify on per column text index basis.

## Writing Text Search Queries

A new built-in function TEXT\_MATCH has been introduced for using text search in SQL/PQL.

TEXT\_MATCH(text\_column\_name, search\_expression)

* text\_column\_name - name of the column to do text search on.&#x20;
* search\_expression - search query

We can use TEXT\_MATCH function as part of our queries in the WHERE clause. Examples:

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_MATCH(...)
SELECT * FROM Foo WHERE TEXT_MATCH(...)
```

We can also use the TEXT\_MATCH filter clause with other filter operators. For example:

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_MATCH(...) AND some_other_column_1 > 20000
SELECT COUNT(*) FROM Foo WHERE TEXT_MATCH(...) AND some_other_column_1 > 20000 AND some_other_column_2 < 100000
```

Combining multiple TEXT\_MATCH filter clauses

```sql
SELECT COUNT(*) FROM Foo WHERE TEXT_MATCH(text_col_1, ....) AND TEXT_MATCH(text_col_2, ...)
```

TEXT\_MATCH can be used in WHERE clause of all kinds of queries supported by Pinot

* Selection query which projects one or more columns
  * User can also include the text column name in select list
* Aggregation query
* Aggregation GROUP BY query

The search expression (second argument to TEXT\_MATCH function) is the query string that Pinot will use to perform text search on the column's text index. _\*\*_Following expression types are supported

### **Phrase Query**

This query is used to do exact match of a given phrase. Exact match implies that terms in the user-specified phrase should appear in the exact same order in the original text document. Note that document is referred to as the column value.

Let's take the example of resume text data containing 14 documents to walk through queries. The data is stored in column named SKILLS\_COL and we have created a text index on this column.

```
Java, C++, worked on open source projects, coursera machine learning
Machine learning, Tensor flow, Java, Stanford university,
Distributed systems, Java, C++, Go, distributed query engines for analytics and data warehouses, Machine learning, spark, Kubernetes, transaction processing
Java, Python, C++, Machine learning, building and deploying large scale production systems, concurrency, multi-threading, CPU processing
C++, Python, Tensor flow, database kernel, storage, indexing and transaction processing, building large scale systems, Machine learning
Amazon EC2, AWS, hadoop, big data, spark, building high performance scalable systems, building and deploying large scale production systems, concurrency, multi-threading, Java, C++, CPU processing
Distributed systems, database development, columnar query engine, database kernel, storage, indexing and transaction processing, building large scale systems
Distributed systems, Java, realtime streaming systems, Machine learning, spark, Kubernetes, distributed storage, concurrency, multi-threading
CUDA, GPU, Python, Machine learning, database kernel, storage, indexing and transaction processing, building large scale systems
Distributed systems, Java, database engine, cluster management, docker image building and distribution
Kubernetes, cluster management, operating systems, concurrency, multi-threading, apache airflow, Apache Spark,
Apache spark, Java, C++, query processing, transaction processing, distributed storage, concurrency, multi-threading, apache airflow
Big data stream processing, Apache Flink, Apache Beam, database kernel, distributed query engines for analytics and data warehouses
CUDA, GPU processing, Tensor flow, Pandas, Python, Jupyter notebook, spark, Machine learning, building high performance scalable systems
Distributed systems, Apache Kafka, publish-subscribe, building and deploying large scale production systems, concurrency, multi-threading, C++, CPU processing, Java
Realtime stream processing, publish subscribe, columnar processing for data warehouses, concurrency, Java, multi-threading, C++,
C++, Java, Python, realtime streaming systems, Machine learning, spark, Kubernetes, transaction processing, distributed storage, concurrency, multi-threading, apache airflow
Databases, columnar query processing, Apache Arrow, distributed systems, Machine learning, cluster management, docker image building and distribution
Database engine, OLAP systems, OLTP transaction processing at large scale, concurrency, multi-threading, GO, building large scale systems
```

**Example 1 -** Search in SKILL\_COL column to look for documents where each matching document MUST contain phrase "distributed systems" as is

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"Distributed systems\"')
```

The search expression is '\\"Distributed systems\\"'

* The search expression is **always specified within single quotes** '\<your expression>'
* Since we are doing a phrase search, the **phrase should be specified within double quotes** inside the single quotes and the **double quotes should be escaped**&#x20;
  * '\\"\<your phrase>\\"'

The above query will match the following documents:

```
Distributed systems, Java, C++, Go, distributed query engines for analytics and data warehouses, Machine learning, spark, Kubernetes, transaction processing
Distributed systems, database development, columnar query engine, database kernel, storage, indexing and transaction processing, building large scale systems
Distributed systems, Java, realtime streaming systems, Machine learning, spark, Kubernetes, distributed storage, concurrency, multi-threading
Distributed systems, Java, database engine, cluster management, docker image building and distribution
Distributed systems, Apache Kafka, publish-subscribe, building and deploying large scale production systems, concurrency, multi-threading, C++, CPU processing, Java
Databases, columnar query processing, Apache Arrow, distributed systems, Machine learning, cluster management, docker image building and distribution
```

But it won't match the following document:

```
Distributed data processing, systems design experience
```

This is because the phrase query looks for the phrase occurring in the original document **"as is"**. The terms as specified by the user in phrase should be in the **exact same order in the original document** for the document to be considered as a match.

**NOTE:** Matching is always done in a case-insensitive manner.

**Example 2 -** Search in SKILL\_COL column to look for documents where each matching document MUST contain phrase "query processing" as is

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"query processing\"')
```

The above query will match the following documents:

```
Apache spark, Java, C++, query processing, transaction processing, distributed storage, concurrency, multi-threading, apache airflow
Databases, columnar query processing, Apache Arrow, distributed systems, Machine learning, cluster management, docker image building and distribution"
```

### **Term Query**

Term queries are used to search for individual terms

**Example 3 -** Search in SKILL\_COL column to look for documents where each matching document MUST contain the term 'java'

As mentioned earlier, the search expression is always within single quotes. However, since this is a term query, we don't have to use double quotes within single quotes.

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, 'Java')
```

### Composite Query using Boolean Operators

Boolean operators AND, OR are supported and we can use them to build a composite query. Boolean operators can be used to combine phrase and term queries in any arbitrary manner

**Example 4 -** Search in SKILL\_COL column to look for documents where each matching document MUST contain phrases "distributed systems" and "tensor flow". This combines two phrases using AND boolean operator

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"Machine learning\" AND \"Tensor Flow\"')
```

The above query will match the following documents:

```
Machine learning, Tensor flow, Java, Stanford university,
C++, Python, Tensor flow, database kernel, storage, indexing and transaction processing, building large scale systems, Machine learning
CUDA, GPU processing, Tensor flow, Pandas, Python, Jupyter notebook, spark, Machine learning, building high performance scalable systems
```

**Example 5 -** Search in SKILL\_COL column to look for documents where each document MUST contain phrase "machine learning" and term 'gpu' and term 'python'. This combines a phrase and two terms using boolean operator

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"Machine learning\" AND gpu AND python')
```

The above query will match the following documents:

```
CUDA, GPU, Python, Machine learning, database kernel, storage, indexing and transaction processing, building large scale systems
CUDA, GPU processing, Tensor flow, Pandas, Python, Jupyter notebook, spark, Machine learning, building high performance scalable systems
```

When using Boolean operators to combine term(s) and phrase(s) or both, please note that:

* The matching document can contain the terms and phrases in any order.&#x20;
* The matching document may not have the terms adjacent to each other (if this is needed, please use appropriate phrase query for the concerned terms).

Use of OR operator is implicit. In other words, if phrase(s) and term(s) are not combined using AND operator in the search expression, OR operator is used by default:

**Example 6 -** Search in SKILL\_COL column to look for documents where each document MUST contain ANY one of:

* phrase "distributed systems" OR
* term 'java' OR
* term 'C++'.

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"distributed systems\" Java C++')
```

We can also do grouping using parentheses:

**Example 7 -** Search in SKILL\_COL column to look for documents where each document MUST contain

* phrase "distributed systems" AND
* at least one of the terms Java or C++

In the below query, we group terms Java and C++ without any operator which implies the use of OR. The root operator AND is used to combine this with phrase "distributed systems"

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, '\"distributed systems\" AND (Java C++)')
```

### Prefix Query

Prefix searches can also be done in the context of a single term. We can't use prefix matches for phrases.

**Example 8 -** Search in SKILL\_COL column to look for documents where each document MUST contain text like stream, streaming, streams etc

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE TEXT_MATCH(SKILLS_COL, 'stream*')
```

The above query will match the following documents:

```
Distributed systems, Java, realtime streaming systems, Machine learning, spark, Kubernetes, distributed storage, concurrency, multi-threading
Big data stream processing, Apache Flink, Apache Beam, database kernel, distributed query engines for analytics and data warehouses
Realtime stream processing, publish subscribe, columnar processing for data warehouses, concurrency, Java, multi-threading, C++,
C++, Java, Python, realtime streaming systems, Machine learning, spark, Kubernetes, transaction processing, distributed storage, concurrency, multi-threading, apache airflow
```

### Regular Expression Query

Phrase and term queries work on the fundamental logic of looking up the terms (aka tokens) in the text index. The original text document (a value in the column with text index enabled) is parsed, tokenized and individual "indexable" terms are extracted. These terms are inserted into the index.

Based on the nature of original text and how the text is segmented into tokens, it is possible that some terms don't get indexed individually. In such cases, it is better to use regular expression queries on the text index.

Consider server log as an example and we want to look for exceptions. A regex query is suitable for this scenario as it is unlikely that 'exception' is present as an individual indexed token.

Syntax of a regex query is slightly different from queries mentioned earlier. The regular expression is written between a pair of forward slashes (/).

```sql
SELECT SKILLS_COL 
FROM MyTable 
WHERE text_match(SKILLS_COL, '/.*Exception/')
```

The above query will match any text document containing exception.

### Deciding Query Types

Generally, a combination of phrase and term queries using boolean operators and grouping should allow us to build a complex text search query expression.

The key thing to remember is that phrases should be used when the order of terms in the document is important and if separating the phrase into individual terms doesn't make sense from end user's perspective.

An example would be phrase "machine learning".

```sql
TEXT_MATCH(column, '\"machine learning\"')
```

However, if we are searching for documents matching Java and C++ terms, using phrase query "Java C++" will actually result in in partial results (could be empty too) since now we are relying the on the user specifying these skills in the exact same order (adjacent to each other) in the resume text.

```sql
TEXT_MATCH(column, '\"Java C++\"')
```

Term query using boolean AND operator is more appropriate for such cases

```sql
TEXT_MATCH(column, 'Java AND C++')
```
