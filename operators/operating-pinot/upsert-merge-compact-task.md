# Upsert Compact Merge Task (Small Segment Merger)

The Upsert Compact Merge Task, also known as the small segment merger, allows you to merge small segments into larger ones for upsert-enabled real-time tables, reducing the total segment count while maintaining storage efficiency.

This task is only supported for REALTIME tables with upsert enabled.

> **ℹ️ New in Pinot 1.3.0**: This task was introduced in version 1.3.0 to address segment proliferation in upsert tables. It works alongside the existing UpsertCompactionTask but focuses on merging multiple small segments rather than compacting individual segments.

> **⚠️ Important Bug Fix**: An issue was identified ([#15846](https://github.com/apache/pinot/issues/15846)) in the initial implementation, which has been fixed via [PR #16034](https://github.com/apache/pinot/pull/16034) and [PR #16086](https://github.com/apache/pinot/pull/16086). These fixes are not present in Pinot 1.3.0. If you plan to use this task, make sure to cherry-pick these PRs or wait for Pinot 1.4.0 release.

## Task overview

The Upsert Compact Merge Task (small segment merger) addresses the challenge of segment proliferation in upsert tables, where the number of segments can grow continuously over time, leading to operational challenges and performance degradation. While individual segments may be efficiently compacted by the UpsertCompactionTask, the overall segment count continues to increase.

### Relationship to UpsertCompactionTask

The Upsert Compact Merge Task complements the existing UpsertCompactionTask:
- **UpsertCompactionTask**: Compacts individual segments by removing invalid records within each segment
- **UpsertCompactMergeTask**: Merges multiple small segments into larger ones while simultaneously compacting each segment during the merge process, reducing both total segment count and invalid records

Both tasks can run independently and are designed to work together for optimal upsert table management.

Over time, upsert tables can accumulate thousands of segments, which creates several challenges:
- **ZooKeeper limitations**: Each segment stores metadata in ZooKeeper, and high segment counts can cause significant ZK latencies
- **Server restart/replacement risks**: More segments mean longer restart times and higher probability of loading failures
- **Operational complexity**: Table rebalancing and metadata operations become increasingly strained
- **Query performance degradation**: Higher disk I/O demands due to processing more segments simultaneously

### How it works

The Upsert Compact Merge Task uses the Minion Task Framework and consists of Generator and Executor classes:

* **UpsertCompactMergeTaskGenerator**: Invoked by the Pinot Controller according to the specified schedule. It:
  * Retrieves segment metadata for the table's completed segments
  * Retrieves validDocIds from the servers hosting the completed segments
  * Selects segments for merging based on the configured strategy (continuous time-based selection)
  * Generates tasks to merge multiple segments into fewer, larger segments

* **UpsertCompactMergeTaskExecutor**: Invoked by a Pinot Minion. It:
  * Downloads the segments specified in the task config from deep store or servers
  * Retrieves validDocIds snapshots from the servers
  * Uses a CompactedRecordReader to merge records from multiple segments
  * Creates new merged segments using UploadedRealtimeSegmentNameGenerator with "compacted" prefix
  * Uploads the new segments back to the controller

### Segment selection strategy

The task uses a **continuous time-based selection** approach:
1. Starts with the oldest segment and processes segments in chronological order
2. Groups continuous segments based on their invalid document ratios and merging feasibility
3. Continues selecting segments as long as the total valid records in chosen segments plus the next segment ≤ `maxNumRecordsPerSegment`
4. Respects the `maxNumSegmentsPerTask` limit to ensure reasonable task sizes
5. Maintains time-order continuity in segment selection
6. Once we have created multiple groups of segments that can be merged, we select the one with highest gain for each partitions for merging.

**Size-based selection (when outputSegmentMaxSize is configured)**:
- When `outputSegmentMaxSize` is specified, the task also considers segment size limits
- Segments are selected to fit within both record count and size constraints

### Segment cleanup approach

The task uses a safe two-phase approach for segment management:
1. **Phase 1**: Upload new merged segments without immediately deleting the original segments
2. **Phase 2**: Post one segment commit cycle when validDocIDSnapshot is updated, identify original segments with `validDocIDCount = 0` and delete them

This approach leverages ZooKeeper metadata and `enableSnapshot` runs to safely clean up old segments while avoiding data inconsistencies.

### Implementation details

**Segment naming**: New merged segments are created with the "compacted" prefix using the UploadedRealtimeSegmentNameGenerator.

**Size-based compaction**: When `outputSegmentMaxSize` is configured, the task performs both record-count-based and size-based segment selection.

**Batch processing**: To optimize performance, the task fetches validDocIds from servers in batches controlled by the `numSegmentsBatchPerServerRequest` parameter.

**CRC validation**: The task performs CRC (Cyclic Redundancy Check) validation to ensure data integrity during segment processing and merging operations.

**Partition constraints**: All segments selected for merging must belong to the same partition. The task validates this constraint before proceeding with the merge operation.

**validDocIds snapshot requirement**: The task requires validDocIds to be available from the servers hosting the segments. This depends on the `enableSnapshot` configuration being active.

## Configuration

1. Start a Pinot Minion.

2. Set up your REALTIME table with upsert enabled. Add "UpsertCompactMergeTask" in the task configs:

```json
"tableName": "upsert_enabled_REALTIME",
"tableType": "REALTIME",
"task": {
    "taskTypeConfigsMap": {
        "UpsertCompactMergeTask": {
            "schedule": "0 */6 * ? * *",
            "bufferTimePeriod": "2d",
            "maxNumRecordsPerSegment": "5000000",
            "maxNumRecordsPerTask": "50000000",
            "maxNumSegmentsPerTask": "10",
            "outputSegmentMaxSize": "200MB",
            "numSegmentsBatchPerServerRequest": "500"
        }
    }
}
```

3. Ensure your upsert table has snapshot enabled:

```json
"upsertConfig": {
    "mode": "FULL", // or "PARTIAL"
    "enableSnapshot": true
}
```

4. Enable PinotTaskManager (disabled by default) by adding the `controller.task` properties below to your [controller conf](../../configuration-reference/controller.md), and then restart the controller (required).

```
controller.task.scheduler.enabled=true
controller.task.frequencyPeriod=1h
```

## Configuration Properties

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>schedule</td>
      <td>Cron expression for task scheduling. Less frequent scheduling (e.g., every 6 hours) is recommended as this is a resource-intensive operation</td>
      <td>None (required)</td>
    </tr>
    <tr>
      <td>bufferTimePeriod</td>
      <td>Minimum time that must elapse since segment completion (endTime) before it becomes eligible for merging</td>
      <td>2d</td>
    </tr>
    <tr>
      <td>maxNumRecordsPerSegment</td>
      <td>Maximum number of valid rows to include in a merged segment. Controls the size of output segments</td>
      <td>5000000</td>
    </tr>
    <tr>
      <td>maxNumRecordsPerTask</td>
      <td>Maximum number of records to process in a single task. Prevents overly large tasks</td>
      <td>50000000</td>
    </tr>
    <tr>
      <td>maxNumSegmentsPerTask</td>
      <td>Maximum number of segments to merge in a single task. Prevents overly large tasks</td>
      <td>10</td>
    </tr>
    <tr>
      <td>outputSegmentMaxSize</td>
      <td>Maximum size of output segments in bytes. When specified, enables size-based segment merging in addition to record-count-based merging. Accepts formats like '200MB', '1GB', etc.</td>
      <td>None (size-based disabled by default)</td>
    </tr>
    <tr>
      <td>numSegmentsBatchPerServerRequest</td>
      <td>Number of segments to query in one batch when fetching validDocIds from servers</td>
      <td>500</td>
    </tr>
  </tbody>
</table>

## Prerequisites

- **Pinot version**: Requires Pinot version 1.3.0 or later
- **Upsert enabled**: Table must have upsert configuration with `enableSnapshot: true`
- **Completed segments**: Task only operates on completed (non-consuming) segments with validDocIds available
- **Same partition**: All segments being merged must belong to the same partition to maintain upsert consistency
- **Minion cluster**: At least one Pinot Minion must be running and accessible to the controller
- **Table validation**: The task validates table configuration during execution, ensuring upsert is enabled and snapshot functionality is available

## Example

Consider a table with the following characteristics:
- 16 Kafka partitions producing 4000 messages/second
- Upsert compaction running every 5 minutes with aggressive settings
- Segments are typically small (< 500K valid records) after compaction

Before UpsertCompactMergeTask:
- Table accumulates ~175 new segments per day
- After 6 months: ~31,500 segments total
- High ZooKeeper load and slow server restarts

After enabling UpsertCompactMergeTask with the above configuration:
- Task runs every 6 hours, merging 5-10 small segments into 1 larger segment
- Segment count growth rate reduced by 80-90%
- Improved server restart times and operational stability
- Maintained query performance while reducing segment management overhead


## Monitoring and Troubleshooting

### Task Progress and Monitoring

Monitor task execution through the following methods:

**Controller API**: Use the Pinot Controller API to check task status:
- `GET /tasks/{taskType}` - List all tasks for UpsertCompactMergeTask
- `GET /tasks/{taskType}/{taskId}` - Get specific task details and status

**Task State Tracking**: Tasks progress through these states:
- `IN_PROGRESS` - Task is currently executing on a Minion
- `COMPLETED` - Task finished successfully
- `FAILED` - Task encountered an error
- `TIMEOUT` - Task exceeded configured timeout

**Progress Notifications**: The task provides progress updates during execution showing:
- Number of segments being processed
- Current processing stage (downloading, merging, uploading)
- Estimated completion time

### Common Issues

**Task not generating**:
- Verify `enableSnapshot: true` in upsert config
- Check that segments meet the selection criteria (small enough and old enough based on `bufferTimePeriod`)
- Ensure completed segments exist for the table with validDocIds available
- Verify table configuration passes validation (upsert enabled, correct table type)

**Segments not being cleaned up**:
- Verify `enableSnapshot` is running between task executions
- Check ZooKeeper metadata for merge timestamps
- Original segments should be cleaned up in subsequent task runs when validDocIDCount = 0
- Ensure the two-phase cleanup process is completing properly

**Task failures**:
- Check Minion logs for CRC validation errors
- Verify all segments belong to the same partition
- Ensure sufficient resources on Minion nodes for segment processing
- Check deep store connectivity for segment download/upload operations

**Performance impact**:
- Consider reducing `maxNumSegmentsPerTask` or `maxNumRecordsPerTask` if tasks are taking too long
- Adjust `bufferTimePeriod` to balance segment count reduction with task frequency
- Use `outputSegmentMaxSize` to control output segment sizes when needed
- Tune `numSegmentsBatchPerServerRequest` for optimal validDocIds fetching performance
- Monitor server resources during task execution

**Configuration issues**:
- Ensure all numeric values are properly formatted (some accept string representations)
- Verify cron schedule format is correct
- Check that outputSegmentMaxSize uses proper size format (e.g., "200MB", "1GB")

## Limitations

- Only supports upsert-enabled REALTIME tables
- Requires `enableSnapshot: true` in upsert configuration
- Cannot merge segments across different partitions
- Original segments are not immediately deleted (cleaned up in subsequent runs)
- Resource-intensive operation that should be scheduled appropriately

## Best Practices

1. **Scheduling**: Use less frequent scheduling (6-12 hours) to balance effectiveness with resource usage
2. **Sizing**: Configure `maxNumRecordsPerSegment` and optionally `outputSegmentMaxSize` based on your query patterns and server resources
3. **Monitoring**: Track segment count trends and task execution metrics
4. **Coordination**: Coordinate with UpsertCompactionTask scheduling to avoid resource conflicts
5. **Testing**: Test the configuration on a smaller table first to understand the impact

> **ℹ️ Design doc**: The detailed technical design for this feature is available in the RFC document provided with this implementation.
>
> **Issue**: [https://github.com/apache/pinot/issues/14477](https://github.com/apache/pinot/issues/14477)
