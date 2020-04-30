---
description: Ways to query Pinot
---

# Querying Pinot

### REST API on the Broker

Pinot can be queried via a broker endpoint as follows. This example assumes broker is running on `localhost:8099`

{% tabs %}
{% tab title="Standard-SQL endpoint" %}
The Pinot REST API can be accessed by invoking `POST` operation with a JSON body containing the parameter `sql` to the `/query/sql`  endpoint on a broker. 

```java
$ curl -H "Content-Type: application/json" -X POST \
   -d '{"sql":"select foo, count(*) from myTable group by foo limit 100"}' \
   http://localhost:8099/query/sql
```
{% endtab %}

{% tab title="PQL endpoint" %}
{% hint style="warning" %}
Note

This endpoint is deprecated, and will soon be removed. The standard-SQL endpoint is the recommended endpoint. 
{% endhint %}

The PQL endpoint can be accessed by invoking `POST` operation with a JSON body containing the parameter `pql` to the `/query`  endpoint on a broker. 

```java
$ curl -H "Content-Type: application/json" -X POST \
   -d '{"pql":"select count(*) from myTable group by foo top 100"}' \
   http://localhost:8099/query
```
{% endtab %}
{% endtabs %}

### Query Console 

Query Console can be used for running ad-hoc queries \(checkbox available to query the PQL endpoint\). The Query Console can be accessed by entering the `<controller host>:<controller port>` in your browser

![Pinot Query Console](../../../.gitbook/assets/image%20%2811%29.png)

### pinot-admin

You can also query using the `pinot-admin` scripts. Make sure you follow instructions in [Getting Pinot](../../../basics/getting-started/running-pinot-locally.md#getting-pinot) to get Pinot locally, and then

```bash
cd incubator-pinot/pinot-tools/target/pinot-tools-pkg 
bin/pinot-admin.sh PostQuery \
  -queryType sql \
  -brokerPort 8000 \
  -query "select count(*) from baseballStats"
2020/03/04 12:46:33.459 INFO [PostQueryCommand] [main] Executing command: PostQuery -brokerHost localhost -brokerPort 8000 -queryType sql -query select count(*) from baseballStats
2020/03/04 12:46:33.854 INFO [PostQueryCommand] [main] Result: {"resultTable":{"dataSchema":{"columnDataTypes":["LONG"],"columnNames":["count(*)"]},"rows":[[97889]]},"exceptions":[],"numServersQueried":1,"numServersResponded":1,"numSegmentsQueried":1,"numSegmentsProcessed":1,"numSegmentsMatched":1,"numConsumingSegmentsQueried":0,"numDocsScanned":97889,"numEntriesScannedInFilter":0,"numEntriesScannedPostFilter":0,"numGroupsLimitReached":false,"totalDocs":97889,"timeUsedMs":185,"segmentStatistics":[],"traceInfo":{},"minConsumingFreshnessTimeMs":0}
```

### Pinot Clients

Here's a list of the clients available to query Pinot from your application

1. [Java Client](https://apache-pinot.gitbook.io/apache-pinot-cookbook/pinot-user-guide/pinot-clients/java)
2. Coming soon - JDBC client
3. [Golang Client](../../clients/golang.md#pinot-client-go)

