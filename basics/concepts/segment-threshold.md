---
description: Learn how segment thresholds work in Pinot.
---

# Segment threshold

The segment threshold determines when a segment is committed in real-time tables.

When data is first ingested from a streaming provider like Kafka, it gets stored in a consuming segment. 
The data in the consuming segment is stored on the disk of the server(s) that are processing a particular partition from the streaming provider.

However, it's not until a segment is committed that the segment is written to the [deep store](https://docs.pinot.apache.org/basics/components/deep-store). 
The segment threshold decides when that should happen.

## Why should we care about it?

We care about the segment threshold because we want to make sure that our segments are a reasonable size.

* Queries are processed at the segment level, so if segments are too small it may result in higher query latencies as there is increased overhead when processing queries (in terms of number of threads spawned, meta data processing, etc).


* If they're too big, this may result in servers running out of memory. If a server is restarted the consuming segment will need to start consuming from the first row again, which will cause lag between Pinot and the streaming provider.

<iframe width="560" height="315" src="https://www.youtube.com/embed/qBMv3CcKVsI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>

*Mark Needham explains the segment threshold*