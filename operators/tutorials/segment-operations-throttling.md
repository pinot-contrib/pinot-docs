# Segment Operations Throttling

## Throttling

Segments undergo a series of operations such as download, untar, index rebuild, and much more before they are ready to serve data for queries. These operations can be resource intensive (CPU + memory) especially during operations such as server restarts and table rebalance. Throttling configurations can be added to control the concurrency of how many segments can undergo a specific operation at any given point of time to limit the resource utilization.

Each config added related to throttling come in two variants:

* Before serving queries - the maximum parallel segments that can undergo the given operation before the server is marked as ready to server queries. These configurations will include `before.serving.queries`in the config name.&#x20;
* After serving queries - the maximum parallel segments that can undergo the given operation after the server is marked as ready to server queries. These configurations will not include `before.serving.queries`in the config name.

It is recommended to set the after serving queries variant to be <= the before serving queries variant, since once the server starts serving queries, resources are needed for query processing to provide lower query latencies.

## Configurations

<table><thead><tr><th width="267">Config</th><th width="130">Allowed Values</th><th width="82">Default</th><th>Description</th></tr></thead><tbody><tr><td><pre data-overflow="wrap"><code>pinot.server.max.segment.preprocess.parallelism
</code></pre></td><td>0 &#x3C; value &#x3C;= Integer.MAX_VALUE</td><td>100</td><td>The maximum parallelism to perform index rebuild operations on a segment across all indexes <strong>after</strong> the server is ready to serve queries.</td></tr><tr><td><pre data-overflow="wrap" data-full-width="false"><code>pinot.server.max.segment.preprocess.parallelism.before.serving.queries
</code></pre></td><td>0 &#x3C; value &#x3C;= Integer.MAX_VALUE</td><td>100</td><td>The maximum parallelism to perform index rebuild operations on a segment across all indexes <strong>before</strong> the server is ready to serve queries (start up).</td></tr><tr><td><pre data-overflow="wrap"><code>pinot.server.max.segment.startree.preprocess.parallelism
</code></pre></td><td>0 &#x3C; value &#x3C;= Integer.MAX_VALUE</td><td>100</td><td>The maximum parallelism to perform StarTree index rebuild operations on a segment <strong>after</strong> the server is ready to serve queries. StarTree index rebuild can be more resource intensive than other index operations.</td></tr><tr><td><pre data-overflow="wrap"><code>pinot.server.max.segment.startree.preprocess.parallelism.before.serving.queries
</code></pre></td><td>0 &#x3C; value &#x3C;= Integer.MAX_VALUE</td><td>100</td><td>The maximum parallelism to perform StarTree index rebuild operations on a segment <strong>before</strong> the server is ready to serve queries (start up). StarTree index rebuild can be more resource intensive than other index operations.</td></tr><tr><td><pre data-overflow="wrap"><code>pinot.server.max.segment.download.parallelism
</code></pre></td><td>0 &#x3C; value &#x3C;= Integer.MAX_VALUE</td><td>100</td><td>The maximum parallelism to download and untar segments from deep store or peer servers <strong>after</strong> the server is ready to serve queries.</td></tr><tr><td><pre data-overflow="wrap"><code><strong>pinot.server.max.segment.download.parallelism.before.serving.queries
</strong></code></pre></td><td>0 &#x3C; value &#x3C;= Integer.MAX_VALUE</td><td>100</td><td>The maximum parallelism to download and untar segments from deep store or peer servers <strong>before</strong> the server is ready to serve queries (start up).</td></tr></tbody></table>

The above configurations can be updated via adding them as [cluster configurations](../../configuration-reference/cluster.md). No server restart is required for these configurations to take effect. Setting any of these to a large value effectively disables throttling (Apache Helix max threads for processing state transitions defaults to 40, which means at most 40 segment operations can occur in parallel on a given server). It is recommended to set both the before and after serving queries override in the ZK cluster configs if overriding to prevent unwanted defaults from getting picked up during / after the server is marked as ready to serve queries.

There also exists a [table level download throttle config](performance-optimization-configurations.md) which limits the segments that can be downloaded for each table. This applies first to ensure no table faces starvation in terms of segment download, and the server level download throttle mentioned in the table above applies next to ensure the server is protected from too many downloads across all tables. These can be configured independently.

## Relevant OSS PRs

* Segment index rebuild across all index types: [https://github.com/apache/pinot/pull/14894](https://github.com/apache/pinot/pull/14894)
* StarTree segment index rebuild across all index types: [https://github.com/apache/pinot/pull/14943](https://github.com/apache/pinot/pull/14943)
* Segment download at server level: [https://github.com/apache/pinot/pull/15001](https://github.com/apache/pinot/pull/15001)
