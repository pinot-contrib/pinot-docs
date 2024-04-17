# Managed offline flows


Managed offline flows allow you to transition data from real-time to offline tables. This feature automatically manage the movement of the data to a corresponding OFFLINE table, so you don't have to write any offline jobs.

The most common use case for Pinot is providing real-time analytics based on streaming data with a real-time table. However, there's a few reasons you might want to also have that data available in an offline table, including the following examples:

  * In real-time tables, you can't easily replace segments or remove duplicate columns because all data must come in through streaming.
  * In real-time tables, there's no way to backfill a specific day's data, whereas for offline tables, you can run a one-off backfill job.
  * In real-time tables, the data tends to be highly granular. Offline tables let you look at bigger windows of data, including rollups for the time column, aggregations across common dimensions, better compression, and dedup.

## How it works

There are two parts to the process: task generation and task execution.

### Task generation

Once the real-time to offline job has been scheduled, the task generator (running on the Pinot controller) will create tasks to be run by a [Pinot minion](https://docs.pinot.apache.org/basics/components/minion).

The generator determines the window start and end time based on the provided configuration.
It will then check to see if any of the completed segments are eligible by checking their start and end time, starting from the segment with the earliest time.
Eligible segments must overlap with that window, as shown in the diagram below:

<p>
    <img src="/img/realtime-offline.png" alt="Real-Time to Offline Job - Selecting eligible segments" />
    <em>Real-Time to Offline Job - Selecting eligible segments</em>
</p>

<Callout>
There must be at least one completed/flushed segment in the real-time table, otherwise the task won't try to create any offline segments.
</Callout> 

As long as some segments match the window, a task will be created and sent to the Minion. 
If no matching segments are found for the window, the generator will move to the next time window and repeat the process.

<Callout type="info">
When the generator is checking the most recently completed segment, it will make sure that the segment crosses over the end of the window to make sure that the consuming segment doesn't contain some portion of the window.
</Callout>

### Task execution

Once the minion receives a task to execute, it does the following steps:

1. Downloads the existing segments.
2. Filter records based on the time window
3. Round the time value in the records (optional)
4. Partition the records if partitioning is enabled in the table config
5. Merge records based on the merge type
6. Sort records if sorting is enabled in the table config
7. Uploads new segments to the Pinot Controller.
Managed offline flows moves records from the real-time table to the offline table one `time window` at a time. 

For example, if the real-time table has records with timestamp starting 10-24-2020T13:56:00, then the Pinot managed offline flows will move records for the time window \[10-24-2020, 10-25-2020) in the first run, followed by \[10-25-2020, 10-26-2020) in the next run, followed by \[10-26-2020, 10-27-2020) in the next run, and so on. This **window length** of one day is just the default, and it can be configured to any length of your choice.

{% hint style="warning" %}
**Note**

Only completed (ONLINE) segments of the real-time table are used for movement. If the window's data falls into the CONSUMING segment, that run will be skipped. That window will be processed in a future run when all data has made it to the completed segments.
{% endhint %}

![RealtimeToOfflineSegmentsTask](../../.gitbook/assets/Paper.Journal.15.png)


### Configure the real-time to offline job

This feature uses the **pinot-minions** and **the Helix Task Executor framework**. This feature consists of two parts

- **RealtimeToOfflineSegmentsTaskGenerator** - This is the minion task scheduler, which schedules tasks of type "**RealtimeToOfflineSegmentsTask**". This task is scheduled by the controller periodic task - **PinotTaskManager**.
   A **watermark is maintained in zookeeper**, which is the end time of the time window last successfully processed. The task generator refers to this watermark, to determine the start of the time window, for the next task it generates. The end time is calculated based on the window length (configurable, 1d default). The task generator will find all segments which have data in \[start, end), and set it into the **task configs**, along with the start and end.\
   The generator will not schedule a new task, unless the previous task has COMPLETED (or been stuck for over 24h). This is to ensure that we always move records in sequential time windows (exactly mimicking offline flows), because out-of-order data pushes will mess with the time boundary calculation of the hybrid table.
- **RealtimeToOfflineSegmentsTaskExecutor** - This is a minion task executor to execute the RealtimeToOfflineSegmentsTask generated by the task generator. These **tasks are run by the pinot-minion** component.\
   The task executor will download all segments from the REALTIME table, as indicated in the task config. Using the SegmentProcessorFramework, it will **extract data for \[start, end), build the segments, and push them to the OFFLINE table**. The segment processor framework will **do any required partitioning & sorting based on the OFFLINE table config**.\
   Before exiting from the task, it will **update the watermark in zookeeper**, to reflect the end time of the time window processed.


1. Start a Pinot minion (link).

2. Set up your real-time table. Add "RealtimeToOfflineSegmentsTask" in the task configs

```
"tableName": "myTable_REALTIME",
"tableType": "REALTIME",
...
...
"task": {
    "taskTypeConfigsMap": {
      "RealtimeToOfflineSegmentsTask": {
      }
    }
  }
```

3. Create the corresponding OFFLINE table

4. Enable `PinotTaskManager`.

The PinotTaskManager periodic task is disabled by default. Enable this using one of the 2 methods described in [Auto-Schedule](https://docs.pinot.apache.org/basics/components/minion#auto-schedule) section. Set the frequency to some reasonable value (frequently is better, as extra tasks will not be scheduled unless required). Controller will need a restart after setting this config.

**Step 4**: Advanced configs

If needed, you can add more configs to the task configs in the REALTIME table, such as

```
"task": {
    "taskTypeConfigsMap": {
      "RealtimeToOfflineSegmentsTask": {
        "bucketTimePeriod": "6h",
        "bufferTimePeriod": "5d",
        "roundBucketTimePeriod": "1h",
        "mergeType": "rollup",
        "score.aggregationType": "max",
        "maxNumRecordsPerSegment": "100000"
      }
    }
  }
```

| Property                     | Description                                                                                                                                                                                                                                                                                                                                                                           | Default   |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| bucketTimePeriod             | Time window size for each run. For example, if set to `1h`, each task will process one hour of data at a time. Adjust this to change the time window.                                                                                                                                                                                                                                 | 1d        |
| bufferTimePeriod             | Buffer time. The job won't schedule tasks unless the time window is older than this buffer. Configure this property according to how late you expect your data. For example, if your system can emit events later than three days, set this to `3d` to make sure those are included. Note that once a given time window has been processed, it will never be processed again.         | 2d        |
| roundBucketTimePeriod        | Determines whether to round the time value before merging the rows. This is useful if time column is highly granular in the real-time table and not needed. In the offline table, you can roll up the time values. For example, if you have milliseconds granularity in real-time table, but you're okay with minute level granularity in the application, set this property to `1m`. | None      |
| mergeType                    | Set to one of the following options: - `concat`: No aggregations - `rollup`: Perform metrics aggregations across common dimensions and time - `dedup`: Deduplicate rows with the same values                                                                                                                                                                                          | concat    |
| {metricName}.aggregationType | If you set `mergeType` to `rollup`, this property determines the aggregation function to apply to the specified metric. Only applicable for `rollup` case. Enter `sum`, `max`, or `min`.                                                                                                                                                                                              | sum       |
| maxNumRecordsPerSegment      | Determines the maximum number of records allowed in a  generated segment. Useful if the time window has many records, but you don't want them all in the same segment.                                                                                                                                                                                                                | 5,000,000 |