# Query Cancellation

/Although Pinot is designed for short-lived queries, it may be useful to cancel queries before they finish. In order to do that, first you need to enable the query tracking feature by setting the following options (which requires a restart):

```
pinot.server.enable.query.cancellation=true // false by default
pinot.broker.enable.query.cancellation=true // false by default
```

Once query tracking is enabled, queries can be killed in two different ways: Using the internal id assigned by brokers or using client query ids.

### Cancel by internal ID

When brokers receive queries, they assign a random query ID to each one. The query ID of all queries running at a given time can be obtained by calling the `GET /queries` endpoint on the controllers. This returns a JSON object where each key is the broker name and the values are objects whose keys are the internal IDs and the values the query text. For example, it could return:

```json
{
  "Broker_192.168.0.105_8000": {
    "7": "select G_old from baseballStats limit 10",
    "8": "select G_old from baseballStats limit 100"
  }
}
```

Then you can cancel queries by executing a DELETE request on `/query/{brokerId}/{queryId}[?verbose=false/true]` , which returns a text like:

```
Cancelled query: 8 with responses from servers: 
{192.168.0.105:7501=404, 192.168.0.105:7502=200, 192.168.0.105:7500=200}
```

This method requires several steps and you also need to specify the broker that executes the query. This is why canceling by client query ID is recommended.

### Cancel by client query ID

Cancel by client query ID is the recommended way to cancel queries. To do so, you need to specify a client query ID for each of your queries first. This can be done by including the `clientQueryId` query option.

Any query with client query ID can be cancelled by calling the DELETE `/queryClient/{clientQueryId}`  endpoint. This method cancels the queries with the given ID running on any cluster.

Remember that the value used for `clientQueryId` should be unique among the cluster, but Pinot doesn't verify that. This is why values with high entropy, like UUIDs, are recommended. In the event that there are multiple queries with the same client query ID, the behavior of the cancel query method is unspecified, meaning that any, both, or none of the queries may be killed.

The `clientQueryId` option is also used as [query-correlation-id.md](query-correlation-id.md).&#x20;



