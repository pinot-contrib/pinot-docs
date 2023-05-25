# Query Routing using Adaptive Server Selection

{% hint style="info" %}
[Design document](https://docs.google.com/document/d/1w8YVpKIj0S62NvwDpf1HgruwxJYJ6ODuKQLjGXupH8w/edit)

[Test Results and Performance](https://docs.google.com/document/d/1ZeU9n5sX6eBUmM4emSBRgzD82CvifqI7OWsUEIS6Wp4/edit#heading=h.lvnfmsqo8x29)
{% endhint %}

Adaptive Server Selection is a new routing capability for Pinot Brokers where incoming queries are routed to the best available server instead of following the default round robin approach while choosing servers. With this feature, Brokers will be sensitive to changes on the Servers like GC issues, slowness, network slowness, etc. The broker will thus adaptively route more queries to faster servers and lesser queries to slower servers

### How this works

There are two main components:

1. Stats Collection
2. Routing using Adaptive Server Selection

#### Stats Collection

Each broker maintains stats individually for all servers. These stats are collected at the broker during query processing when the query is routed to the servers and after the response is received from the servers. These stats are maintained in-memory. Some of the stats collected at broker per server are as follows:

1. Number of in-progress / in-flight queries&#x20;
2. EWMA (Exponential Weighted Moving Average) for latencies seen by queries
3. EWMA (Exponential Weighted Moving Average) for number of ongoing queries at any time

#### Adaptive Routing

When the broker receives a query, it will use the above stats to pick the best available server. This enables the broker  to automatically reduces the number of queries it sends to slow servers and increase the number of queries it sends to faster servers. We currently support the following  strategies:

1. **NO\_OP** : Uses the default RoundRobin approach. In other words, this will give existing behavior where stats are not used by broker when picking the servers to route the query to.
2. **NUM\_INFLIGHT\_REQ** : Uses the number of in-flight requests stat to determine the best server
3. **LATENCY** : Uses the EWMA latency stat to determine the best server
4. **HYBRID** : Uses a combination of in-flight requests and latency to determine the best server

The above strategies works in tandem with the following available Routing mechanisms today:

1. Balanced Routing
2. ReplicaGroup Routing

So, a table can be configured to use Balanced or Replica group segment assignment + routing and can still leverage the adaptive server selection feature.

### Configs

The configuration for enabling/disabling this feature and the knobs for performance tuning are present at the Broker instance level. The feature is currently turned off by default.&#x20;

#### Enabling Stats Collection and Adaptive Routing

1. To enable Stats Collection, set `pinot.broker.adaptive.server.selector.enable.stats.collection = true`. Note that setting this property alone will only enable stats collection and not perform Adaptive Routing
2. To enable an Adaptive Routing Strategy, use **one** of the following configs. The `HYBRID`  strategy works well for most use cases. Unless you are an advanced user, we recommend using the `HYBRID` strategy.
   1. `pinot.broker.adaptive.server.selector.type=HYBRID`
   2. `pinot.broker.adaptive.server.selector.type=NUM_INFLIGHT_REQ`
   3. `pinot.broker.adaptive.server.selector.type=LATENCY`

#### Tuning Knobs

The following configs are already set to default values that work well for most usecases. For advanced users, the following knobs are available to tune Adaptive Routing Strategies

{% hint style="info" %}
Prefix all the below properties with  `pinot.broker.adaptive.server.selector.`
{% endhint %}

<table><thead><tr><th width="280">Property</th><th width="300">Description</th><th>Default Value</th></tr></thead><tbody><tr><td><code>ewma.alpha</code></td><td>Alpha value for Exponential Moving Average. A higher value would provide more weightage to incoming values and lower weightage to older values</td><td>0.666</td></tr><tr><td><code>autodecay.window.ms</code></td><td>If the EWMA value has not been updated for a while, the duration after which the value should be decayed</td><td>10000</td></tr><tr><td><code>avg.initialization.val</code></td><td>Initial value for EWMA average</td><td>1.0</td></tr><tr><td><code>stats.manager.threadpool.size</code></td><td>Number of threads reserved to process Adaptive Server Selection Stats.</td><td>2</td></tr></tbody></table>
