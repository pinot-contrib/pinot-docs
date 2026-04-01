# Segment Operations Throttling

## Throttling

Segments undergo a series of operations such as download, untar, index rebuild, and much more before they are ready to serve data for queries. These operations can be resource intensive (CPU + memory) especially during server restarts and table rebalance. Throttling configurations can be added to control the concurrency of how many segments can undergo a specific operation at any given point of time to limit the resource utilization. Throttling is done today via the use of semaphores.

Each config added related to throttling come in two variants:

* Before serving queries - the maximum parallel segments that can undergo the given operation before the server is marked as ready to serve queries. These configurations will include `before.serving.queries`in the config name.&#x20;
* After serving queries - the maximum parallel segments that can undergo the given operation after the server is marked as ready to serve queries. These configurations will not include `before.serving.queries`in the config name.

Two variants of each config were added due to the nature of requiring different characteristics depending on what the server is doing. During start up, servers are mostly trying to bring segments into a queryable state and using more resources to achieve this faster makes sense. Whereas once the server is ready to serve queries, more resources are required for query processing.

## Configurations

All throttling configurations are disabled by default by setting a very high parallelism of Integer.MAX\_VALUE.

| Config | Allowed Values | Default | Description |
| --- | --- | --- | --- |
| ``pinot.server.max.segment.preprocess.parallelism `` | 0 < value <= Integer.MAX_VALUE | Integer.MAX_VALUE | The maximum parallelism to perform index rebuild operations on a segment across all indexes **after** the server is ready to serve queries. |
| ``pinot.server.max.segment.preprocess.parallelism.before.serving.queries `` | 0 < value <= Integer.MAX_VALUE | Integer.MAX_VALUE | The maximum parallelism to perform index rebuild operations on a segment across all indexes **before** the server is ready to serve queries (start up). |
| ``pinot.server.max.segment.startree.preprocess.parallelism `` | 0 < value <= Integer.MAX_VALUE | Integer.MAX_VALUE | The maximum parallelism to perform StarTree index rebuild operations on a segment **after** the server is ready to serve queries. StarTree index rebuild can be more resource intensive than other index operations. |
| ``pinot.server.max.segment.startree.preprocess.parallelism.before.serving.queries `` | 0 < value <= Integer.MAX_VALUE | Integer.MAX_VALUE | The maximum parallelism to perform StarTree index rebuild operations on a segment **before** the server is ready to serve queries (start up). StarTree index rebuild can be more resource intensive than other index operations. |
| ``pinot.server.max.segment.download.parallelism `` | 0 < value <= Integer.MAX_VALUE | Integer.MAX_VALUE | The maximum parallelism to download and untar segments from deep store or peer servers **after** the server is ready to serve queries. |
| ``**pinot.server.max.segment.download.parallelism.before.serving.queries **`` | 0 < value <= Integer.MAX_VALUE | Integer.MAX_VALUE | The maximum parallelism to download and untar segments from deep store or peer servers **before** the server is ready to serve queries (start up). |

The above configurations can be updated via adding them as [cluster configurations](../reference/configuration-reference/cluster.md). No server restart is required for these configurations to take effect if updated  in ZooKeeper. Pinot Server logs will provide information about the change in these configs. An example log of updated configs for all the segment operations throttling configs are:

```
2025/04/21 15:22:36.532 INFO [SegmentAllIndexPreprocessThrottler] [thread-42] Updated config: pinot.server.max.segment.preprocess.parallelism from: 2147483647 to: 4
2025/04/21 15:22:36.532 INFO [SegmentAllIndexPreprocessThrottler] [thread-42] Updated total permits: 4
2025/04/21 15:22:36.532 INFO [SegmentAllIndexPreprocessThrottler] [thread-42] Updated config: pinot.server.max.segment.preprocess.parallelism.before.serving.queries from: 2147483647 to: 8
2025/04/21 15:22:36.532 INFO [SegmentStarTreePreprocessThrottler] [thread-42] Updated config: pinot.server.max.segment.startree.preprocess.parallelism from: 2147483647 to: 2
2025/04/21 15:22:36.532 INFO [SegmentStarTreePreprocessThrottler] [thread-42] Updated total permits: 2
2025/04/21 15:22:36.532 INFO [SegmentStarTreePreprocessThrottler] [thread-42] Updated config: pinot.server.max.segment.startree.preprocess.parallelism.before.serving.queries from: 2147483647 to: 4
2025/04/21 15:22:36.532 INFO [SegmentDownloadThrottler] [thread-42] Updated config: pinot.server.max.segment.download.parallelism from: 2147483647 to: 5
2025/04/21 15:22:36.532 INFO [SegmentDownloadThrottler] [thread-42] Updated total permits: 5
2025/04/21 15:22:36.532 INFO [SegmentDownloadThrottler] [thread-42] Updated config: pinot.server.max.segment.download.parallelism.before.serving.queries from: 2147483647 to: 10
```

An example of what cluster configurations overridden by setting them in ZooKeeper under `/CONFIGS/CLUSTER/<PinotClusterName>` looks like is shown below:

![](../../.gitbook/assets/Screenshot 2025-04-23 at 15.23.40.png)

*Overridden Cluster Configs in ZooKeeper for Segment Operations Throttle Configs*

Some recommendations on how to choose values for these are:

* The default was [updated](https://github.com/apache/pinot/pull/15126) to Integer.MAX\_VALUE, effectively disabling throttling by default. Lower throttling configurations if throttling is needed.
* It is recommended to set the after serving queries variant to be <= the before serving queries variant, since once the server starts serving queries, resources are needed for query processing. If too many resources are used up for processing segments, queries can see higher latencies and even exhaust resources.
  *   A related configuration controls the REST API invoked refresh (segment upload) and reload operations. This defaults to 1, but with the new throttling configurations mentioned in the table above, this can potentially be increased.

      ```
      pinot.server.instance.max.parallel.refresh.threads
      ```
* It is recommended to set both the before and after serving queries override in the ZK cluster configs if overriding to prevent unwanted defaults from getting picked up during / after the server is marked as ready to serve queries.
* Since StarTree index preprocessing is part of the overall index preprocessing step, if both configs are set, it is recommended to set the StarTree index specific value as <= overall index preprocessing value. Otherwise, the overall index preprocessing value will land up becoming the throttle value even for the StarTree indexes, since it will apply first.
* There also exists a [table level download throttle config](performance-optimization-configurations.md) which limits the segments that can be downloaded for each table. This applies first to ensure no table faces starvation in terms of segment download, and the server level download throttle mentioned in the table above applies next to ensure the server is protected from too many downloads across all tables. Table level throttling is disabled by default. These can be configured independently.

## Metrics

The following Gauge type metrics exist to monitor the segment operation threshold and count of number of segments undergoing a given operation:

| Segment Operation | Scope | Threshold Metric | Count Metric |
| --- | --- | --- | --- |
| All Index Rebuild | Global | `segmentAllPreprocessThrottleThreshold` | `segmentAllPreprocessCount` |
| StarTree Index Rebuild | Global | `segmentStartreePreprocessThreshold` | `segmentStartreePreprocessCount` |
| Segment Download | Global | `segmentDownloadThrottleThreshold` | `segmentDownloadCount` |
| Segment Download | Table-Level | `segmentTableDownloadThrottleThreshold` | `segmentTableDownloadCount` |

## Relevant OSS PRs

* Segment index rebuild across all index types: [https://github.com/apache/pinot/pull/14894](https://github.com/apache/pinot/pull/14894)
* StarTree segment index rebuild: [https://github.com/apache/pinot/pull/14943](https://github.com/apache/pinot/pull/14943)
* Segment download at server level: [https://github.com/apache/pinot/pull/15001](https://github.com/apache/pinot/pull/15001)
* Add metrics: [https://github.com/apache/pinot/pull/15392](https://github.com/apache/pinot/pull/15392)
