---
description: In this Apache Pinot concepts guide, we'll learn how segment retention works.
---

# Segment retention

Segments in Pinot tables have a retention time, after which the segments are deleted. Typically, offline tables retain segments for a longer period of time than real-time tables.

The removal of segments is done by the retention manager. By default, the retention manager runs once every 6 hours.

The retention manager purges two types of segments:

* Expired segments: Segments whose end time has exceeded the retention period.
* Replaced segments: Segments that have been replaced as part of the [merge rollup task. ](../../operate-pinot/minion-merge-rollup-task.md)

There are a couple of scenarios where segments in offline tables won't be purged:

* If the segment doesn't have an end time. This would happen if the segment doesn't contain a time column.
* If the segment's table has a `segmentIngestionType` of `REFRESH`.

## Handling segments with invalid end times

By default, when a segment's end time is invalid or missing, the retention manager skips it entirely, and the segment is never deleted regardless of the retention policy. To enable automatic cleanup of such segments, you can enable the creation time fallback by setting `controller.retentionManager.enableCreationTimeFallback` to `true` in the cluster configuration. When enabled, the retention manager will use the segment's creation time (`segmentZKMetadata.getCreationTime()`) as a fallback if the end time is invalid.

This configuration is **dynamic** and does not require a controller restart to take effect. It can be updated through the cluster config change listener.

If the retention period isn't specified, segments aren't purged from tables.

The retention manager initially moves these segments into a _Deleted Segments_ area, from where they will eventually be permanently removed. The duration that deleted segments are kept is controlled by the `controller.deleted.segments.retentionInDays` configuration (default: 7 days).

When deleting a table via the API, you can override this behavior by passing a `retention` query parameter. For example, `DELETE /tables/{tableName}?retention=0d` deletes all segments immediately without moving them to the deleted-segments area. See the [Controller API Examples](../../reference/api-reference/controller-api.md#delete-tablestablename) for more details.
