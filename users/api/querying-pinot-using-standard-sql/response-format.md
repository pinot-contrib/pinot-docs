# Query Response Format

Find Pinot query response format examples for selection, aggregation, and group by queries formatted in a [SQL-like structure](response-format.md#standard-sql-response). Also find details about each field included in the Pinot [broker query response](response-format.md#broker-query-response-fields).

To learn more about how a Pinot broker routes and processes queries, computes the query explain plan, and ways to optimize queries, see the following topics:

* [Processing queries](../../../basics/architecture.md#query-processing)
* Query explain plans:
  * [Single-stage query engine](../../user-guide-query/explain-plan.md)
  * [Multi-stage query engine](../../user-guide-query/query-syntax/explain-plan-multi-stage.md)
* [Optimizing query routing](../../../operators/operating-pinot/tuning/routing.md#optimizing-routing)
  * [Use adaptive server selection](../../../operators/operating-pinot/tuning/query-routing-using-adaptive-server-selection.md)

### Standard-SQL response

The query response is returned in a **SQL-like tabular structure** from the standard-SQL endpoint.&#x20;

{% tabs %}
{% tab title="Selections" %}
```javascript
$ curl -H "Content-Type: application/json" -X POST \
   -d '{"sql":"SELECT moo, bar, foo FROM myTable ORDER BY foo DESC"}' \
   http://localhost:8099/query/sql
{
  "exceptions": [], 
  "minConsumingFreshnessTimeMs": 0, 
  "numConsumingSegmentsQueried": 0, 
  "numDocsScanned": 6, 
  "numEntriesScannedInFilter": 0, 
  "numEntriesScannedPostFilter": 18, 
  "numGroupsLimitReached": false, 
  "numSegmentsMatched": 2, 
  "numSegmentsProcessed": 2, 
  "numSegmentsQueried": 2, 
  "numServersQueried": 1, 
  "numServersResponded": 1, 
  "resultTable": {
    "dataSchema": {
      "columnDataTypes": [
        "LONG",
        "INT",
        "STRING"
      ], 
      "columnNames": [
        "moo", 
        "bar",
        "foo"
      ]
    }, 
    "rows": [
      [ 
        40015, 
        2019,
        "xyz"
      ], 
      [
        1002,
        2001,
        "pqr"
      ], 
      [
        20555,
        1988,
        "pqr"
      ],
      [ 
        203,
        2010,
        "pqr"
      ], 
      [
        500,
        2008,
        "abc"
      ], 
      [
        60, 
        2003,
        "abc"
      ]
    ]
  }, 
  "segmentStatistics": [], 
  "timeUsedMs": 4, 
  "totalDocs": 6, 
  "traceInfo": {}
}
```
{% endtab %}

{% tab title="Aggregations" %}
```javascript
$ curl -X POST \
  -d '{"sql":"SELECT SUM(moo), MAX(bar), COUNT(*) FROM myTable"}' \
  localhost:8099/query/sql -H "Content-Type: application/json" 
{
  "exceptions": [], 
  "minConsumingFreshnessTimeMs": 0, 
  "numConsumingSegmentsQueried": 0, 
  "numDocsScanned": 6, 
  "numEntriesScannedInFilter": 0, 
  "numEntriesScannedPostFilter": 12, 
  "numGroupsLimitReached": false, 
  "numSegmentsMatched": 2, 
  "numSegmentsProcessed": 2, 
  "numSegmentsQueried": 2, 
  "numServersQueried": 1, 
  "numServersResponded": 1, 
  "resultTable": {
    "dataSchema": {
      "columnDataTypes": [
        "DOUBLE", 
        "DOUBLE", 
        "LONG"
      ], 
      "columnNames": [
        "sum(moo)", 
        "max(bar)", 
        "count(*)"
      ]
    }, 
    "rows": [
      [
        62335, 
        2019.0, 
        6
      ]
    ]
  }, 
  "segmentStatistics": [], 
  "timeUsedMs": 87, 
  "totalDocs": 6, 
  "traceInfo": {}
}
```
{% endtab %}

{% tab title="Group By" %}
```javascript
$ curl -X POST \
  -d '{"sql":"SELECT SUM(moo), MAX(bar) FROM myTable GROUP BY foo ORDER BY foo"}' \
  localhost:8099/query/sql -H "Content-Type: application/json" 
{
  "exceptions": [], 
  "minConsumingFreshnessTimeMs": 0, 
  "numConsumingSegmentsQueried": 0, 
  "numDocsScanned": 6, 
  "numEntriesScannedInFilter": 0, 
  "numEntriesScannedPostFilter": 18, 
  "numGroupsLimitReached": false, 
  "numSegmentsMatched": 2, 
  "numSegmentsProcessed": 2, 
  "numSegmentsQueried": 2, 
  "numServersQueried": 1, 
  "numServersResponded": 1, 
  "resultTable": {
    "dataSchema": {
      "columnDataTypes": [
        "STRING", 
        "DOUBLE", 
        "DOUBLE"
      ], 
      "columnNames": [
        "foo", 
        "sum(moo)", 
        "max(bar)"
      ]
    }, 
    "rows": [
      [
        "abc", 
        560.0, 
        2008.0
      ], 
      [
        "pqr", 
        21760.0, 
        2010.0
      ], 
      [
        "xyz", 
        40015.0, 
        2019.0
      ]
    ]
  }, 
  "segmentStatistics": [], 
  "timeUsedMs": 15, 
  "totalDocs": 6, 
  "traceInfo": {}
}
```
{% endtab %}
{% endtabs %}

### Broker query response fields

<table><thead><tr><th width="362.5">Response Field</th><th>Description</th></tr></thead><tbody><tr><td>resultTable</td><td>Contains everything needed to process the response</td></tr><tr><td>resultTable.dataSchema</td><td>Describes the schema of the response, including <code>columnNames</code> and their <code>dataTypes</code></td></tr><tr><td>resultTable.dataSchema.columnNames</td><td><code>columnNames</code> in the response</td></tr><tr><td>resultTable.dataSchema.columnDataTypes</td><td><code>dataTypes</code> for each column</td></tr><tr><td>resultTable.rows</td><td>Actual content with values. This is an array of arrays. The number of rows depends on the limit value in the query. The number of columns in each row is equal to the length of <code>resultTable.dataSchema.columnNames</code></td></tr><tr><td>timeUsedms</td><td>Total time taken as seen by the broker before sending the response back to the client.</td></tr><tr><td>totalDocs</td><td>Number of documents/records in the table.</td></tr><tr><td>numServersQueried</td><td>Represents the number of servers queried by the broker (may be less than the total number of servers since the broker can apply some optimizations to minimize the number of servers).</td></tr><tr><td>numServersResponded</td><td>This should be equal to the <code>numServersQueried</code>. If this is not the same, then one of more servers might have timed out. If <code>numServersQueried != numServersResponded,</code> the results can be considered partial and clients can retry the query with exponential back off.</td></tr><tr><td>numSegmentsQueried</td><td><p>The total number of <code>segmentsQueried</code> for a query. May be less than the total number of segments if the broker applies optimizations. </p><p></p><p>The broker decides how many segments to query on each server, based on broker pruning logic. The server decides how many of these segments to actually look at, based on server pruning logic. After processing segments for a query, fewer may have the matching records. <br><br>In general, <code>numSegmentsQueried >= numSegmentsProcessed >= numSegmentsMatched.</code></p></td></tr><tr><td>numSegmentsMatched</td><td>The number of segments processed with at least one document matched in the query response. </td></tr><tr><td>numSegmentsProcessed</td><td><p>The number of segment operators used to process segments. Indicates the effectiveness of the pruning logic. For more information, see query plans for:</p><ul><li><a href="../../user-guide-query/explain-plan.md">Single-stage query engine</a></li><li><a href="../../user-guide-query/query-syntax/explain-plan-multi-stage.md">Multi-stage query engine</a></li></ul></td></tr><tr><td>numDocScanned</td><td>The number of docs/records selected <em>after</em> the filter phase.</td></tr><tr><td>numEntriesScannedInFilter</td><td><p>The number of entries scanned in the filtering phase of query execution. </p><p>Can be larger than the total scanned doc count because of multiple filtering predicates or multi-value entries. </p><p>Can also be smaller than the total scanned doc count if indexing is used for filtering. </p><p> </p><p>This along with <code>numEntriesScannedInPostFilter</code> indicates where most of the time is spent during query processing. If this value is high, enabling indexing for columns in <code>tableConfig</code> is a way to bring it down.</p></td></tr><tr><td>numEntriesScannedPostFilter</td><td><p>The number of entries scanned after the filtering phase of query execution, ie. aggregation and/or group-by phases. This is equivalent to <code>numDocScanned</code> * number of projected columns. </p><p></p><p>This along with <code>numEntriesScannedInFilter</code> indicates where most of the time is spent during query processing. </p><p></p><p>A high number for this means the selectivity is low (that is, Pinot needs to scan a lot of records to answer the query). If this is high, consider using star-tree index. (A regular inverted/bitmap index won't improve performance.)</p></td></tr><tr><td>numGroupsLimitReached</td><td>If the query has a <code>group by</code> clause and top K, Pinot drops new entries after the <code>numGroupsLimit</code> is reached. If this boolean is set to true, the query result may not be accurate. The default value for <code>numGroupsLimit</code> is 100k, and should be sufficient for most use cases.</td></tr><tr><td>exceptions</td><td>Will contain the stack trace if there is any exception processing the query.</td></tr><tr><td>segmentStatistics</td><td>N/A</td></tr><tr><td>traceInfo</td><td>If trace is enabled (can be enabled for each query), this contains the timing for each stage and each segment. Use for development and debugging purposes.</td></tr></tbody></table>







