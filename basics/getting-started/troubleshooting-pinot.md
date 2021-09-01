# Troubleshooting Pinot

## Is there any debug information available in Pinot?

Pinot offers various ways to assist with troubleshooting and debugging problems that might happen. It is recommended to start off with the debug api which may quickly surface some of the commonly occurring problems. The debug api provides information such as tableSize, ingestion status, any error messages related to state transition in server, among other things.

The table debug api can be invoked via the Swagger UI as follows:

![Swagger - Table Debug Api](../../.gitbook/assets/image%20%281%29.png)

It can also be invoked directly by accessing the URL as follows. The api requires the `tableName`, and can optionally take `tableType (offline|realtime)`  and `verbosity` level.

```text
curl -X GET "http://localhost:9000/debug/tables/airlineStats?verbosity=0" -H "accept: application/json"
```

Pinot also provides a wide-variety of operational metrics that can be used for creating dashboards, alerting and [monitoring](https://docs.pinot.apache.org/operators/operating-pinot/monitoring). Also, all pinot components log debug information related to error conditions that can be used for troubleshooting.

## How do I debug a slow query or a query which keeps timing out

Please use these steps:

1. If the query executes, look at the query result. Specifically look at `numEntriesScannedInFilter` and `numDocsScanned`.
   1. If `numEntriesScannedInFilter` is very high, consider adding indexes for the corresponding columns being used in the filter predicates. You should also think about partitioning the incoming data based on the dimension most heavily used in your filter queries.
   2. If `numDocsScanned` is very high, that means the selectivity for the query is low and lots of documents need to be processed after the filtering. Consider refining the filter to increase the selectivity of the query.
2. If the query is not executing, you can extend the query timeout by appending a `timeoutMs` parameter to the query \(eg: `select * from mytable limit 10 option(timeoutMs=60000)`\). Then you can repeat step 1. 
3. You can also look at GC stats for the corresponding Pinot servers. If a particular server seems to be running full GC all the time, you can do a couple of things such as
   1. Increase JVM heap \(Xmx\)
   2. Consider using off-heap memory for segments
   3. Decrease the total number of segments per server \(by partitioning the data in a better way\)

## 



