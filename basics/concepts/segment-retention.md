---
description: In this Apache Pinot concepts guide, we'll learn how segment retention works.
---

# Segment Retention

Segments in Pinot tables have a retention time, after which the segments are deleted. 
Typically, offline tables will retain segments for a longer period of time than real-time tables.

The removal of segments is done by the retention manager.
By default, the retention manager runs once every 6 hours.

The retention manager purges two types of segments:

* Expired segments - Segments whose end time has exceeded the retention period.
* Replaced segments - Segments that have been replaced as part of the [merge roll-up](../recipes/merge-small-segments.md) process.

<Callout type="info">
There are a couple of scenarios where segments in offline tables won't be purged:

* If the segment doesn't have an end time.
This would happen if the segment doesn't contain a time column.
* If the segment's table has a `segmentIngestionType` of `REFRESH`. 

In addition, segments will not be purged in real-time or offline tables if the retention period isn't specified.
</Callout>

The retention manager initially moves these segments into a _Deleted Segments_ area, from where they will eventually be permanently removed.