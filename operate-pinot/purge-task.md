# PurgeTask

The PurgeTask is a Minion task designed to remove or modify specific records from segments based on configurable criteria. It's essential for data retention management, compliance requirements (such as GDPR data deletion requests), and data quality maintenance.

## Overview

PurgeTask processes segments by applying custom logic to identify records for removal or modification, then generates new segments with the changes applied. The task automatically handles segment download, processing, upload, and metadata updates.

## Key Features

- **Data Retention Management**: Remove old or obsolete data from segments
- **Compliance Support**: Delete records to meet regulatory requirements (e.g., GDPR)
- **Data Quality**: Remove invalid or corrupted records
- **In-Place Modification**: Modify records without removing them
- **Smart Scheduling**: Only processes segments when sufficient time has passed since last purge
- **Zero-Record Cleanup**: Automatically deletes segments with no remaining records
- **Resource Management**: Configurable limits on concurrent tasks

## Configuration

### Table Configuration

To enable PurgeTask on a table, add it to the table's task configuration:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "PurgeTask": {
        "lastPurgeTimeThresholdPeriod": "14d",
        "tableMaxNumTasks": "5"
      }
    }
  }
}
```

### Configuration Parameters

| Parameter | Description | Default | Example |
|-----------|-------------|---------|---------|
| `lastPurgeTimeThresholdPeriod` | Minimum time between purge operations on the same segment (default: 14 days) | `"14d"` | `"7d"`, `"1h"`, `"30d"` |
| `tableMaxNumTasks` | Maximum number of concurrent purge tasks per table | `Integer.MAX_VALUE` | `"3"`, `"10"` |

## Implementation Requirements

PurgeTask requires custom implementation of one or both of these interfaces:

### RecordPurger Interface

Implement this interface to identify records that should be removed:

```java
public interface RecordPurger {
  /**
   * Returns true if the record should be purged (removed)
   */
  boolean shouldPurge(GenericRow record);
}
```

### RecordModifier Interface

Implement this interface to modify records in-place:

```java
public interface RecordModifier {
  /**
   * Modifies the record and returns true if changes were made
   */
  boolean modifyRecord(GenericRow record);
}
```

## How It Works

1. **Task Generation**: The PurgeTaskGenerator identifies segments eligible for purging based on:
   - Time since last purge (must exceed `lastPurgeTimeThresholdPeriod`)
   - Segment availability and status
   - Configured task limits

2. **Task Execution**: The PurgeTaskExecutor:
   - Downloads the segment to process
   - Applies purge and/or modification logic to each record
   - Creates a new segment if changes were made
   - Uploads the new segment and updates metadata

3. **Record Processing**: For each record in the segment:
   - Calls `RecordPurger.shouldPurge()` if configured
   - Calls `RecordModifier.modifyRecord()` if configured
   - Builds the output segment with remaining/modified records

## Example Usage

### Basic Configuration

```json
{
  "tableName": "events_OFFLINE",
  "task": {
    "taskTypeConfigsMap": {
      "PurgeTask": {
        "lastPurgeTimeThresholdPeriod": "7d",
        "tableMaxNumTasks": "3"
      }
    }
  }
}
```

### Custom Purge Logic

To implement custom purge logic, you need to create plugins that implement the `RecordPurger` and/or `RecordModifier` interfaces. These plugins follow Pinot's standard plugin architecture and must be packaged and deployed with your Pinot cluster.

For more information on developing Pinot plugins, see the [Plugin Architecture documentation](../developers/plugin-architecture/).

## Scheduling

### Manual Scheduling

Use the Controller REST API to manually trigger PurgeTask:

```bash
# Schedule PurgeTask for all enabled tables
POST /tasks/schedule?taskType=PurgeTask

# Schedule PurgeTask for a specific table
POST /tasks/schedule?taskType=PurgeTask&tableName=myTable_OFFLINE
```

### Automatic Scheduling

Configure automatic scheduling using cron expressions:

```json
{
  "task": {
    "taskTypeConfigsMap": {
      "PurgeTask": {
        "lastPurgeTimeThresholdPeriod": "14d",
        "schedule": "0 0 2 * * ?"
      }
    }
  }
}
```

## Important Considerations

- **Custom Logic Required**: You must implement either `RecordPurger` or `RecordModifier` interfaces
- **Resource Intensive**: Processing large segments requires sufficient Minion resources
- **Segment Replacement**: Creates entirely new segments when changes are made
- **Metadata Preservation**: Maintains original segment creation time and time intervals
- **Time-based Throttling**: Built-in protection against excessive processing of the same segments

## Monitoring

PurgeTask generates standard Minion metrics for monitoring:

- Task execution time and success/failure rates
- Number of tasks in progress and queued
- Resource utilization during segment processing

Use the Pinot UI Task Manager to monitor PurgeTask execution and troubleshoot issues.
