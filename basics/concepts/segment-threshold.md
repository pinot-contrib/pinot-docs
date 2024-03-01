---
description: Learn how segment thresholds work in Pinot.
---

# Segment threshold

The segment threshold determines when a segment is committed in real-time tables.

When data is first ingested from a streaming provider like Kafka, Pinot stores the data in a consuming segment. 

This segment is on the disk of the server(s) processing a particular partition from the streaming provider.

However, it's not until a segment is committed that the segment is written to the [deep store](https://docs.pinot.apache.org/basics/components/deep-store). 
The segment threshold decides when that should happen.

## Why is the segment threshold important?

The segment threshold is important because it ensures segments are a reasonable size. 

When queries are processed, smaller segments may increase query latency due to more overhead (number of threads spawned, meta data processing, and so on). 

Larger segments may cause servers to run out of memory. When a server is restarted, the consuming segment must start consuming from the first row again, causing a lag between Pinot and the streaming provider.

<iframe width="560" height="315" src="https://www.youtube.com/embed/qBMv3CcKVsI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>

*Mark Needham explains the segment threshold*