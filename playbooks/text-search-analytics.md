---
description: End-to-end guide for combining full-text search with OLAP aggregations in Apache Pinot.
---

# Text Search Analytics

This playbook covers workloads that combine full-text search with OLAP-style aggregations — searching logs for error patterns and then aggregating by service, filtering a product catalog by description text and then ranking by sales, or triaging support tickets by keyword and then grouping by severity.

## When to use this pattern

Use this playbook when:

- Your queries include both free-text predicates (keyword search, phrase match, fuzzy match) **and** structured filters/aggregations (GROUP BY, SUM, COUNT, time-range filters).
- You want a single system for text search and analytics instead of maintaining both Elasticsearch and a separate OLAP store.
- Text columns contain natural language (log messages, product descriptions, ticket bodies, user reviews) rather than short categorical values.
- You need real-time ingestion of text data with immediate searchability.

If your text columns are short, low-cardinality labels (e.g., status codes, country names), standard inverted indexes are sufficient — you do not need a text index.

## Architecture sketch

```
Log / event stream ──▶ Kafka ──▶ Pinot REALTIME table
                                      │
                              ┌───────┴────────┐
                              │ Servers with    │
                              │ text index on   │
                              │ message column  │
                              └────────────────┘
                                      │
                              TEXT_MATCH + OLAP
                              queries from app
```

Pinot supports two text index implementations:

| Index | Engine | Best for |
| --- | --- | --- |
| **Text index** (Lucene-based) | Apache Lucene | Full Lucene query syntax: phrase queries, fuzzy, regex, wildcard, proximity |
| **Native text index** | Pinot built-in | Simple keyword/phrase search with lower memory and faster ingestion |

This playbook covers both. Start with the native text index for simpler use cases, and switch to Lucene-based if you need advanced query syntax.

## Schema

```json
{
  "schemaName": "support_tickets",
  "dimensionFieldSpecs": [
    { "name": "ticketId",    "dataType": "STRING" },
    { "name": "customerId",  "dataType": "STRING" },
    { "name": "severity",    "dataType": "STRING" },
    { "name": "service",     "dataType": "STRING" },
    { "name": "assignee",    "dataType": "STRING" },
    { "name": "subject",     "dataType": "STRING" },
    { "name": "body",        "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "responseTimeMs", "dataType": "LONG" }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "createdAt",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

The `subject` and `body` columns will carry the text index. They must be declared as `STRING` type and should **not** have dictionary encoding (they go in the `noDictionaryColumns` list).

## Table configuration with Lucene-based text index

```json
{
  "tableName": "support_tickets",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "createdAt",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "180",
    "replication": "2"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "invertedIndexColumns": ["severity", "service", "assignee"],
    "rangeIndexColumns": ["createdAt"],
    "noDictionaryColumns": ["ticketId", "customerId", "subject", "body"],
    "bloomFilterColumns": ["ticketId"],
    "fieldConfigList": [
      {
        "name": "subject",
        "encodingType": "RAW",
        "indexTypes": ["TEXT"],
        "properties": {
          "fstType": "NATIVE"
        }
      },
      {
        "name": "body",
        "encodingType": "RAW",
        "indexTypes": ["TEXT"],
        "properties": {
          "fstType": "NATIVE"
        }
      }
    ],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "support-tickets",
      "stream.kafka.broker.list": "kafka:9092",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka30.KafkaConsumerFactory",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "realtime.segment.flush.threshold.rows": "250000",
      "realtime.segment.flush.threshold.time": "4h"
    }
  },
  "tenants": {
    "broker": "DefaultTenant",
    "server": "DefaultTenant"
  },
  "metadata": {}
}
```

### Configuration highlights

| Setting | Why |
| --- | --- |
| `fieldConfigList` with `indexTypes: ["TEXT"]` | Creates a Lucene-based text index on `subject` and `body` |
| `encodingType: RAW` | Text-indexed columns must use raw encoding, not dictionary |
| `noDictionaryColumns` includes text columns | Disables dictionary encoding, which is inefficient for long text |
| `invertedIndexColumns` on structured columns | Standard inverted indexes for the non-text filters (severity, service) |

## Alternative: native text index

For simpler search needs (keyword match, phrase match) with lower resource overhead:

```json
"fieldConfigList": [
  {
    "name": "body",
    "encodingType": "RAW",
    "indexTypes": ["NATIVE_TEXT"]
  }
]
```

The native text index does not use Lucene and has lower memory overhead, but does not support fuzzy matching, regex, proximity queries, or boosting. See [Native Text Index](../build-with-pinot/indexing/native-text-index.md) for a comparison.

## Query patterns

### TEXT_MATCH: keyword search with aggregation

Find tickets mentioning "timeout" and aggregate by service:

```sql
SELECT
  service,
  severity,
  COUNT(*) AS ticket_count,
  AVG(responseTimeMs) AS avg_response_time
FROM support_tickets
WHERE TEXT_MATCH(body, 'timeout')
  AND createdAt > ago('P7D')
GROUP BY service, severity
ORDER BY ticket_count DESC
LIMIT 50
```

### Phrase search

Find tickets with the exact phrase "connection refused":

```sql
SELECT ticketId, subject, createdAt
FROM support_tickets
WHERE TEXT_MATCH(body, '"connection refused"')
  AND severity = 'P1'
ORDER BY createdAt DESC
LIMIT 20
```

### Boolean text queries

Combine text predicates with AND, OR, NOT:

```sql
SELECT ticketId, subject, service
FROM support_tickets
WHERE TEXT_MATCH(body, '(timeout OR "connection refused") AND NOT retry')
  AND createdAt > ago('P30D')
LIMIT 100
```

### Wildcard and fuzzy search (Lucene index only)

```sql
-- Wildcard: matches "authenticate", "authentication", "authenticator"
SELECT ticketId, subject
FROM support_tickets
WHERE TEXT_MATCH(body, 'authenticat*')
LIMIT 50

-- Fuzzy: matches "recieve", "receive", "receieve" (edit distance 2)
SELECT ticketId, subject
FROM support_tickets
WHERE TEXT_MATCH(body, 'receive~2')
LIMIT 50
```

### Combining text search with OLAP aggregations

The power of this pattern is running text filters as part of a larger analytical query:

```sql
SELECT
  DATETRUNC('day', createdAt, 'MILLISECONDS') AS day,
  COUNT(*) AS error_tickets,
  PERCENTILEEST(responseTimeMs, 95) AS p95_response
FROM support_tickets
WHERE TEXT_MATCH(body, '"database error" OR "query timeout"')
  AND severity IN ('P1', 'P2')
  AND createdAt > ago('P14D')
GROUP BY day
ORDER BY day
LIMIT 100
```

{% hint style="info" %}
`TEXT_MATCH` is a predicate, not a scoring function. Pinot does not return relevance scores. If you need ranked search results, keep an external search engine for ranking and use Pinot for the analytical aggregation layer.
{% endhint %}

## Log analytics variant

For log analytics (e.g., Apache access logs, application logs), the schema typically has a `logMessage` text column and structured columns extracted at ingestion time:

```json
{
  "schemaName": "app_logs",
  "dimensionFieldSpecs": [
    { "name": "service",    "dataType": "STRING" },
    { "name": "level",      "dataType": "STRING" },
    { "name": "host",       "dataType": "STRING" },
    { "name": "logMessage", "dataType": "STRING" }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "logTimestamp",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

Use [ingestion transformations](../build-with-pinot/ingestion/ingestion-level-transformations.md) to extract structured fields from log lines during ingestion, and apply a text index on the raw `logMessage` for ad-hoc search.

For high-cardinality log data, consider [Stream Ingestion with CLP](../build-with-pinot/ingestion/stream-ingestion/clp.md) which provides compressed log storage with efficient search.

## Operational checklist

### Before go-live

- [ ] Confirm text-indexed columns are in `noDictionaryColumns` and use `encodingType: RAW` in `fieldConfigList`. Dictionary encoding on text columns wastes memory and breaks text indexing.
- [ ] Size your servers with extra heap for Lucene indexes. Each Lucene text index maintains in-memory data structures per segment. Budget 20-30% more heap than a comparable table without text indexes.
- [ ] Test query latency with realistic text queries. `TEXT_MATCH` on short keywords is fast; wildcard queries on large text columns can be slow.
- [ ] Set `realtime.segment.flush.threshold.rows` lower than usual (e.g., 250K) because text-heavy segments are larger in bytes per row.

### Monitoring

- **Lucene index size on disk**: Text indexes can be 1-3x the size of the raw text data. Monitor disk usage per server.
- **Query latency for TEXT_MATCH queries**: Lucene query execution time is included in the server-side query metrics. If P99 spikes, check for expensive wildcard or regex patterns.
- **Segment flush time**: Building text indexes during segment flush takes longer than standard indexes. If flush times grow, reduce `flush.threshold.rows`.

### Common pitfalls

| Pitfall | Fix |
| --- | --- |
| `TEXT_MATCH` returns no results | Verify the column has a text index configured (not just inverted index). Check `fieldConfigList` |
| High memory usage on servers | Lucene indexes are memory-intensive. Use the native text index if you only need keyword/phrase search |
| Slow wildcard queries with leading wildcards | Leading wildcards (`*error`) require scanning the entire term dictionary. Avoid them, or use an FST index for prefix queries |
| Text index on a low-cardinality column | Use a standard inverted index instead — text indexes are overkill for columns with few unique values |
| Search relevance ranking needed | Pinot's `TEXT_MATCH` is a filter, not a scorer. Use Elasticsearch or similar for relevance-ranked search and Pinot for the aggregation layer |

## Further reading

- [Text Search Support](../build-with-pinot/indexing/text-search-support.md)
- [Native Text Index](../build-with-pinot/indexing/native-text-index.md)
- [FST Index](../build-with-pinot/indexing/fst-index.md)
- [Stream Ingestion with CLP](../build-with-pinot/ingestion/stream-ingestion/clp.md)
- [Choosing Indexes](../build-with-pinot/indexing/choosing-indexes.md)
