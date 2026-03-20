---
description: In this Apache Pinot concepts guide, we'll learn how segment retention works.
---

# Segment retention

Segments in Pinot tables have a retention time, after which the segments are deleted. Typically, offline tables retain segments for a longer period of time than real-time tables.

The removal of segments is done by the retention manager. By default, the retention manager runs once every 6 hours.

The retention manager purges two types of segments:

* Expired segments: Segments whose end time has exceeded the retention period.
* Replaced segments: Segments that have been replaced as part of the [merge rollup task. ](../../operators/operating-pinot/minion-merge-rollup-task.md)

There are a couple of scenarios where segments in offline tables won't be purged:

* If the segment doesn't have an end time. This would happen if the segment doesn't contain a time column.
* If the segment's table has a `segmentIngestionType` of `REFRESH`.

If the retention period isn't specified, segments aren't purged from tables.

The retention manager initially moves these segments into a _Deleted Segments_ area, from where they will eventually be permanently removed. The duration that deleted segments are kept is controlled by the `controller.deleted.segments.retentionInDays` configuration (default: 7 days).

When deleting a table via the API, you can override this behavior by passing a `retention` query parameter. For example, `DELETE /tables/{tableName}?retention=0d` deletes all segments immediately without moving them to the deleted-segments area. See the [Controller API Reference](../../users/api/controller-api-reference.md#delete-tables-less-than-tablename-greater-than) for more details.
