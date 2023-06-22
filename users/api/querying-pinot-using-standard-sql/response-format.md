# Query Response Format

### Standard-SQL response

Response is returned in a **SQL-like tabular structure.** Note, this is the response returned from the standard-SQL endpoint. For PQL endpoint response, skip to [PQL endpoint response](response-format.md#pql-endpoint-response)

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

| Response Field                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| resultTable                            | This contains everything needed to process the response                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| resultTable.dataSchema                 | This describes schema of the response (columnNames and their dataTypes)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| resultTable.dataSchema.columnNames     | columnNames in the response.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| resultTable.dataSchema.columnDataTypes | DataTypes for each column                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| resultTable.rows                       | Actual content with values. This is an array of arrays. number of rows depends on the limit value in the query. The number of columns in each row is equal to the length of (resultTable.dataSchema.columnNames)                                                                                                                                                                                                                                                                                                                                                                       |
| timeUsedms                             | Total time taken as seen by the broker before sending the response back to the client                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| totalDocs                              | This is number of documents/records in the table                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| numServersQueried                      | represents the number of servers queried by the broker (note that this may be less than the total number of servers since broker can apply some optimizations to minimize the number of servers)                                                                                                                                                                                                                                                                                                                                                                                       |
| numServersResponded                    | This should be equal to the numServersQueried. If this is not the same, then one of more servers might have timed out. If numServersQueried != numServersResponded the results can be considered partial and clients can retry the query with exponential back off.                                                                                                                                                                                                                                                                                                                    |
| numSegmentsQueried                     | Total number of segmentsQueried for this query. it may be less than the total number of segments since broker can apply optimizations.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| numSegmentsMatched                     | This is the number of segments processed with at least one document matched query response. In general numSegmentsQueried <= numSegmentsProcessed <= numSegmentsMatched.                                                                                                                                                                                                                                                                                                                                                                                                               |
| numSegmentsProcessed                   | Number of segment operators used to process segments. This is indicates the effectiveness of the pruning logic.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| numDocScanned                          | The number of docs/records that were selected after filter phase.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| numEntriesScannedInFilter              | <p>The number of entries scanned in the filtering phase of query execution. </p><p>It could be larger than the total scanned doc count because of multiple filtering predicate and/or multi-value entries. </p><p>It can also be smaller than the total scanned doc count if indexing is used for filtering. </p><p> </p><p>This along with numEntriesScannedInPostFilter should give an idea on where most of the time is spent during query processing. If this is high, enabling indexing for columns in tableConfig can be one way to bring it down.</p>                           |
| numEntriesScannedPostFilter            | <p>The number of entries scanned after the filtering phase of query execution, ie. aggregation and/or group-by phases. This is equivalent to numDocScanned * number of projected columns. </p><p></p><p>This along with numEntriesScannedInFilter should give an idea on where most of the time is spent during query processing. </p><p></p><p>A high number for this means the selectivity is low (i.e. pinot needs to scan a lot of records to answer the query). If this is high, adding regular inverted/bitmap index will not help. However, consider using star-tree index.</p> |
| numGroupsLimitReached                  | If the query has group by clause and top K, pinot drops new entries after the numGroupsLimit is reached. If this boolean is set to true then the query result may not be accurate. Note that the default value for numGroupsLimit is 100k and should be sufficient for most use cases.                                                                                                                                                                                                                                                                                                 |
| exceptions                             | Will contain the stack trace if there is any exception processing the query.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| segmentStatistics                      | N/A                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| traceInfo                              | If trace is enabled (can be enabled for each query), this will contain the timing for each stage and each segment. Advanced feature and intended for dev/debugging purposes                                                                                                                                                                                                                                                                                                                                                                                                            |

### PQL response

{% hint style="warning" %}
**Note**

PQL endpoint is deprecated, and will soon be removed. The standard sql endpoint is the recommended endpoint.
{% endhint %}

The response received from PQL endpoint is different depending on the type of the query.

{% tabs %}
{% tab title="Selections" %}
```javascript
curl -X POST \
  -d '{"pql":"select * from flights limit 3"}' \
  http://localhost:8099/query


{
 "selectionResults":{
    "columns":[
       "Cancelled",
       "Carrier",
       "DaysSinceEpoch",
       "Delayed",
       "Dest",
       "DivAirports",
       "Diverted",
       "Month",
       "Origin",
       "Year"
    ],
    "results":[
       [
          "0",
          "AA",
          "16130",
          "0",
          "SFO",
          [],
          "0",
          "3",
          "LAX",
          "2014"
       ],
       [
          "0",
          "AA",
          "16130",
          "0",
          "LAX",
          [],
          "0",
          "3",
          "SFO",
          "2014"
       ],
       [
          "0",
          "AA",
          "16130",
          "0",
          "SFO",
          [],
          "0",
          "3",
          "LAX",
          "2014"
       ]
    ]
 },
 "traceInfo":{},
 "numDocsScanned":3,
 "aggregationResults":[],
 "timeUsedMs":10,
 "segmentStatistics":[],
 "exceptions":[],
 "totalDocs":102
}
```
{% endtab %}

{% tab title="Aggregations" %}
```javascript
curl -X POST \
  -d '{"pql":"select count(*) from flights"}' \
  http://localhost:8099/query


{
 "traceInfo":{},
 "numDocsScanned":17,
 "aggregationResults":[
    {
       "function":"count_star",
       "value":"17"
    }
 ],
 "timeUsedMs":27,
 "segmentStatistics":[],
 "exceptions":[],
 "totalDocs":17
}
```
{% endtab %}

{% tab title="Group By" %}
```javascript
curl -X POST \
  -d '{"pql":"select count(*) from flights group by Carrier"}' \
  http://localhost:8099/query


{
 "traceInfo":{},
 "numDocsScanned":23,
 "aggregationResults":[
    {
       "groupByResult":[
          {
             "value":"10",
             "group":["AA"]
          },
          {
             "value":"9",
             "group":["VX"]
          },
          {
             "value":"4",
             "group":["WN"]
          }
       ],
       "function":"count_star",
       "groupByColumns":["Carrier"]
    }
 ],
 "timeUsedMs":47,
 "segmentStatistics":[],
 "exceptions":[],
 "totalDocs":23
}
```
{% endtab %}
{% endtabs %}
