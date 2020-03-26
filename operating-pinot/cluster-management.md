# Cluster Management

Pinot provides a web-based management console and a command-line utility \(`pinot-admin.sh`\) in order to help provision and manage pinot clusters.

## Pinot Management Console

The web based management console allows operations on tables, tenants, segments and schemas. You can access the console via `http://controller-host:port/help`. The console also allows you to enter queries for interactive debugging. Here are some screen-shots from the console.

![pinot-console](https://pinot.readthedocs.io/en/latest/_images/pinot-console.png)

Listing all the schemas in the Pinot cluster:

![list-schemas](https://pinot.readthedocs.io/en/latest/_images/list-schemas.png)

Rebalancing segments of a table:

![rebalance-table](https://pinot.readthedocs.io/en/latest/_images/rebalance-table.png)

#### Command line utility \(pinot-admin.sh\)

The command line utility \(`pinot-admin.sh`\) locates at the bin directory in Pinot binary package.

Here is an example of invoking the command to create a pinot table:

```text
$ bin/pinot-admin.sh AddTable  -schemaFile examples/batch/airlineStats/airlineStats_schema.json -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -exec
Executing command: AddTable -tableConfigFile examples/batch/airlineStats/airlineStats_offline_table_config.json -schemaFile examples/batch/airlineStats/airlineStats_schema.json -controllerHost 127.0.0.1 -controllerPort 9000 -exec
Sending request: http://127.0.0.1:9000/schemas to controller: 763e6d4b089e, version: Unknown
{"status":"Table airlineStats_OFFLINE succesfully added"}
```

Here is an example of executing a query on a Pinot table:

```text
bin/pinot-admin.sh PostQuery -query "select count(*) from baseballStats" -queryType sql  -brokerPort 8000
Executing command: PostQuery -brokerHost 172.19.0.3 -brokerPort 8000 -queryType sql -query select count(*) from baseballStats
Result: {"resultTable":{"dataSchema":{"columnDataTypes":["LONG"],"columnNames":["count(*)"]},"rows":[[97889]]},"exceptions":[],"numServersQueried":1,"numServersResponded":1,"numSegmentsQueried":1,"numSegmentsProcessed":1,"numSegmentsMatched":1,"numConsumingSegmentsQueried":0,"numDocsScanned":97889,"numEntriesScannedInFilter":0,"numEntriesScannedPostFilter":0,"numGroupsLimitReached":false,"totalDocs":97889,"timeUsedMs":11,"segmentStatistics":[],"traceInfo":{},"minConsumingFreshnessTimeMs":0}
```

