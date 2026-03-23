# RefreshSegmentTask

The RefreshSegmentTask is a Minion task that automatically reprocesses existing segments when the table configuration or schema changes. It ensures that segments stay up to date with the latest index definitions, column additions, and compatible data type changes without requiring a manual reload.

## Overview

When you update a table's schema (for example, adding a new column or changing a data type) or modify the table config (for example, adding a new index), existing segments may become stale. The RefreshSegmentTask detects these out-of-date segments and rebuilds them using the current table config and schema so that all segments benefit from the latest configuration.

## Key Features

- **Automatic staleness detection**: Compares each segment's last-refresh timestamp against the table config and schema modification times to determine which segments need reprocessing
- **New column handling**: Adds columns that exist in the schema but are missing from the segment
- **Index management**: Adds or removes indexes based on updated table config (for example, inverted index, range index)
- **Compatible data type changes**: Refreshes segments when a column's data type changes to a compatible type
- **Inverted index creation**: Enables inverted index creation during segment generation, which is disabled by default during initial ingestion
- **Concurrency control**: Limits the number of concurrent refresh tasks per table to avoid overwhelming the cluster

## Configuration

### Table Configuration

To enable RefreshSegmentTask on a table, add it to the table's task configuration:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "RefreshSegmentTask": {
        "tableMaxNumTasks": "10"
      }
    }
  }
}
```

### Configuration Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `tableMaxNumTasks` | Maximum number of concurrent refresh tasks per table per scheduling run | `20` |
| `schedule` | Cron expression for automatic task scheduling | None (manual only) |

## How It Works

1. **Task Generation**: The RefreshSegmentTaskGenerator identifies segments eligible for refresh by checking:
   - Whether the table config or schema has been modified since the segment was last refreshed
   - Whether a task is already running for the segment
   - Whether the maximum number of tasks per table has been reached

2. **Task Execution**: The RefreshSegmentTaskExecutor:
   - Downloads the segment to process
   - Loads the current table config and schema from the controller
   - Determines if the segment needs preprocessing (new indexes, column changes)
   - Identifies columns that need refresh (new columns, data type changes)
   - Rebuilds the segment from scratch using the updated schema and table config
   - Uploads the refreshed segment and updates the ZK metadata with a timestamp

3. **Staleness Check**: A segment is considered stale when:
   - The table config modification time is newer than the segment's last refresh timestamp
   - The schema modification time is newer than the segment's last refresh timestamp

## Example Usage

### Adding a New Index

After adding an inverted index to your table config:

```json
{
  "tableName": "events_OFFLINE",
  "tableIndexConfig": {
    "invertedIndexColumns": ["city", "country"]
  },
  "task": {
    "taskTypeConfigsMap": {
      "RefreshSegmentTask": {
        "tableMaxNumTasks": "10",
        "schedule": "0 0 3 * * ?"
      }
    }
  }
}
```

The RefreshSegmentTask will detect that the table config has changed and rebuild all existing segments with the new inverted index.

### Adding a New Column

After adding a new column to the schema, existing segments will not contain this column. The RefreshSegmentTask will rebuild these segments to include the new column with its default value.

## Scheduling

### Manual Scheduling

Use the Controller REST API to manually trigger RefreshSegmentTask:

```bash
# Schedule RefreshSegmentTask for all enabled tables
POST /tasks/schedule?taskType=RefreshSegmentTask

# Schedule RefreshSegmentTask for a specific table
POST /tasks/schedule?taskType=RefreshSegmentTask&tableName=myTable_OFFLINE
```

### Automatic Scheduling

Configure automatic scheduling using cron expressions:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "RefreshSegmentTask": {
        "schedule": "0 0 3 * * ?"
      }
    }
  }
}
```

## Important Considerations

- **Table types**: Supports both OFFLINE and REALTIME tables. For REALTIME tables, only completed (non-consuming) segments are processed.
- **Segment rebuild**: The task rebuilds segments from scratch using the existing data and the updated schema/config. This means it re-reads all records from the segment and creates a new segment file.
- **Creation time preservation**: The original segment creation time and time intervals are preserved during refresh.
- **CRC-based deduplication**: If the refreshed segment has the same CRC as the original, only the ZK metadata is updated (no segment upload occurs).
- **Resource usage**: Rebuilding segments is CPU and I/O intensive. Use `tableMaxNumTasks` to control concurrency and schedule during off-peak hours.

## Monitoring

RefreshSegmentTask generates standard Minion metrics for monitoring:

- Task execution time and success/failure rates
- Number of tasks in progress and queued
- Segment processing statistics (incomplete rows, dropped rows, sanitized rows)

Use the Pinot UI Task Manager to monitor RefreshSegmentTask execution and troubleshoot issues.

## Related pages

* [Segment management overview](../../operate-pinot/segment-management.md) -- assignment, lifecycle, rebalance, and Minion tasks
* [Reload a Table Segment](../../tutorials/operations/segment-reload.md) -- lighter-weight reload for index and metadata updates
* [Segment Lifecycle and Repair](segment-lifecycle-and-repair.md) -- when to reload vs. refresh vs. other operations
