# Upsert Compaction Task

The Upsert Compaction Task allows you reclaim disk space occupied by older version of your records. 

This task is only supported for REALTIME tables with upsert enabled.

### Task overview

The Upsert Compaction Task selects completed segments for compaction based on the provided task configuration and generates a replacement segment for each segment that meets the selection criteria.

However, if a completed segment only contains older records, then it is immediately deleted and no compaction task is generated.

The Upsert Compaction Task uses the Minion Task Framework, and therefore consists of Generator and Executor classes.

* **UpsertCompactionTaskGenerator**:  Invoked by the Pinot Controller according the specified schedule. It’s `generateTasks` method:
  * Retrieves segment metadata for the table’s completed segments.
  * Retrieves validDocIds from the servers hosting the completed segments.
  * In the default `validDocIdsValidationMode=STRICT`, only schedules a segment when the expected replicas are healthy, their CRC or data CRC matches ZooKeeper, and they satisfy the configured `validDocIdsConsensusMode`.
  * Processes validDocIds to determine which segments to compact or delete.
  * Generates a task for every completed segment.
* **UpsertCompactionTaskExecutor**: Invoked by a Pinot Minion.
  * Retrieves validDocIds for the segment specified in the task config.
  * Uses a `CompactedRecordReader` to generate a new segment with only the valid records.

### Configuration

1. Start a Pinot Minion.

2. Set up your REALTIME table. Add "UpsertCompactionTask" in the task configs, like this:
```
"tableName": "upsert_enabled_REALTIME",
"tableType": "REALTIME",
...
...
"task": {
    "taskTypeConfigsMap": {
        "UpsertCompactionTask": {
            "schedule": "0 */5 * ? * *",
            "bufferTimePeriod": "7d",
            "invalidRecordsThresholdPercent": "30",
            "invalidRecordsThresholdCount": "100000",
            "validDocIdsConsensusMode": "EQUAL",
            "validDocIdsValidationMode": "STRICT"
        }
    }
}
```

3. Enable PinotTaskManager (disabled by default) by adding the `controller.task` properties below to your [controller conf](../reference/configuration-reference/controller.md), and then restart the controller (required).

```
controller.task.scheduler.enabled=true
controller.task.frequencyPeriod=1h  #Alternative to "schedule" in task config. 
```

| Property                     | Description                                                                                                                            | Default |
| ---------------------------- |----------------------------------------------------------------------------------------------------------------------------------------|---------|
| bufferTimePeriod | The minimum amount of time that has elapsed since the segment was consuming | 7d |
| invalidRecordsThresholdPercent             | A limit to the amount of older records allowed in the completed segment represented as a percentage of the total number of records in the segment (i.e. old records / total records). Must be configured if invalidRecordsThresholdCount isn’t configured. | 0       |
| invalidRecordsThresholdCount | A limit to the amount of older records allowed in the completed segment represented as a record count. Must be configured if invalidRecordsThresholdPercent isn’t configured. | 0 |
| validDocIdsConsensusMode | Controls how Pinot chooses validDocIds when replicas disagree. `UNSAFE` uses the first healthy replica whose CRC or data CRC matches, `EQUAL` requires all expected healthy replicas to match on CRC or data CRC and valid-doc count, and `MOST_VALID_DOCS` keeps the strict health and CRC checks then picks the replica with the highest valid-doc count. | `EQUAL` |
| validDocIdsValidationMode | Controls generator-side validation before task scheduling. `STRICT` skips segments when replica health, CRC or data CRC, or validDocIds consensus checks fail. `EXECUTOR_ONLY` skips those pre-scheduling checks and lets the executor enforce the configured `validDocIdsConsensusMode` when the task runs. | `STRICT` |

{% hint style="info" %}
**Original design doc**: [https://docs.google.com/document/d/1tDFjyun81KiMfAVO-A7ZFL1mGNm1VEkXDcxqOov8aeI/edit?usp=sharing](https://docs.google.com/document/d/1tDFjyun81KiMfAVO-A7ZFL1mGNm1VEkXDcxqOov8aeI/edit?usp=sharing)

**Issue**: [https://github.com/apache/pinot/issues/6912](https://github.com/apache/pinot/issues/6912)
{% endhint %}
