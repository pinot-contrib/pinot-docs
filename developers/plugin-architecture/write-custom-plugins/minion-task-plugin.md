---
description: >-
  Write a custom Minion task plugin with a task generator and task executor.
---

# Minion Task Plugin

Minion tasks execute background maintenance and data processing jobs in Pinot. Each task type has two components: a **Task Generator** (runs on the Controller) that creates task configurations, and a **Task Executor** (runs on the Minion) that performs the work.

## Architecture

```
Controller                          Minion
┌────────────────────┐             ┌────────────────────┐
│  PinotTaskGenerator│  ─ Helix ─> │ PinotTaskExecutor  │
│  - generateTasks() │  schedules  │ - executeTask()    │
│  - getTaskType()   │             │ - cancel()         │
└────────────────────┘             └────────────────────┘
```

1. The Controller runs the Task Generator on a schedule or via ad-hoc API call
2. The Generator creates `PinotTaskConfig` objects describing the work
3. The Controller schedules tasks via Helix
4. Minion instances pick up tasks based on tag/routing
5. The Minion executes the task using the Task Executor
6. Results are returned to the Controller

## Step 1: Implement the Task Executor

The executor runs on the Minion and performs the actual work.

### Task Executor Factory

```java
import org.apache.pinot.minion.executor.PinotTaskExecutorFactory;
import org.apache.pinot.minion.executor.PinotTaskExecutor;
import org.apache.pinot.spi.annotations.minion.TaskExecutorFactory;

@TaskExecutorFactory(enabled = true)
public class MyTaskExecutorFactory implements PinotTaskExecutorFactory {

  @Override
  public void init(MinionTaskZkMetadataManager zkMetadataManager, MinionConf minionConf) {
    // Initialize resources needed by the executor
  }

  @Override
  public String getTaskType() {
    return "MyCustomTask";  // Must match the generator's task type
  }

  @Override
  public PinotTaskExecutor create() {
    return new MyTaskExecutor();
  }
}
```

### Task Executor

```java
import org.apache.pinot.minion.executor.PinotTaskExecutor;
import org.apache.pinot.core.minion.PinotTaskConfig;

public class MyTaskExecutor implements PinotTaskExecutor {

  private volatile boolean _cancelled = false;

  @Override
  public Object executeTask(PinotTaskConfig pinotTaskConfig) throws Exception {
    String tableName = pinotTaskConfig.getTableName();
    Map<String, String> config = pinotTaskConfig.getConfig();

    // Perform the task work here
    // Check _cancelled periodically for long-running tasks

    return "Task completed successfully";
  }

  @Override
  public void cancel() {
    _cancelled = true;
  }
}
```

{% hint style="info" %}
The executor factory class must be annotated with `@TaskExecutorFactory(enabled = true)` for auto-registration. The class must be in a package matching `org.apache.pinot.*.plugin.minion.tasks.*`.
{% endhint %}

## Step 2: Implement the Task Generator

The generator runs on the Controller and decides when and how to create tasks.

```java
import org.apache.pinot.controller.helix.core.minion.generator.PinotTaskGenerator;
import org.apache.pinot.spi.annotations.minion.TaskGenerator;
import org.apache.pinot.spi.config.table.TableConfig;
import org.apache.pinot.core.minion.PinotTaskConfig;

@TaskGenerator(enabled = true)
public class MyTaskGenerator implements PinotTaskGenerator {

  private ClusterInfoAccessor _clusterInfoAccessor;

  @Override
  public void init(ClusterInfoAccessor clusterInfoAccessor) {
    _clusterInfoAccessor = clusterInfoAccessor;
  }

  @Override
  public String getTaskType() {
    return "MyCustomTask";  // Must match the executor's task type
  }

  // Called on schedule for all tables with this task type enabled
  @Override
  public List<PinotTaskConfig> generateTasks(List<TableConfig> tableConfigs) {
    List<PinotTaskConfig> tasks = new ArrayList<>();
    for (TableConfig tableConfig : tableConfigs) {
      Map<String, String> taskConfig = new HashMap<>();
      taskConfig.put("myParam", "myValue");

      tasks.add(new PinotTaskConfig(
          getTaskType(),
          tableConfig.getTableName(),
          taskConfig));
    }
    return tasks;
  }

  // Called for ad-hoc task execution via API
  @Override
  public List<PinotTaskConfig> generateTasks(
      TableConfig tableConfig, Map<String, String> taskConfigs) throws Exception {
    return List.of(new PinotTaskConfig(
        getTaskType(),
        tableConfig.getTableName(),
        taskConfigs));
  }
}
```

### Optional Generator Overrides

<table>
  <thead>
    <tr>
      <th>Method</th>
      <th>Default</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`getTaskTimeoutMs(String minionTag)`</td>
      <td>3,600,000 (1 hour)</td>
      <td>Task timeout in milliseconds</td>
    </tr>
    <tr>
      <td>`getNumConcurrentTasksPerInstance(String minionTag)`</td>
      <td>1</td>
      <td>Max concurrent tasks per Minion</td>
    </tr>
    <tr>
      <td>`getMaxAttemptsPerTask(String minionTag)`</td>
      <td>1 (no retry)</td>
      <td>Max retry attempts</td>
    </tr>
    <tr>
      <td>`getMinionInstanceTag(TableConfig tableConfig)`</td>
      <td>`UNTAGGED_MINION_INSTANCE`</td>
      <td>Tag for routing tasks to specific Minion instances</td>
    </tr>
    <tr>
      <td>`validateTaskConfigs(TableConfig, Schema, Map)`</td>
      <td>no-op</td>
      <td>Validate task-specific configs at table creation time</td>
    </tr>
  </tbody>
</table>

## Step 3: Enable the Task in Table Config

Add the task configuration to the table config:

```json
{
  "tableName": "myTable_OFFLINE",
  "task": {
    "taskTypeConfigsMap": {
      "MyCustomTask": {
        "schedule": "0 0 * * * ?",
        "myParam": "myValue"
      }
    }
  }
}
```

The `schedule` property uses a CRON expression to define when the task generator runs. Without it, the task can only be triggered via the Controller API.

## Step 4: Trigger Tasks via API

To manually trigger task generation:

```bash

# Generate tasks for all tables with this task type

POST /tasks/schedule?taskType=MyCustomTask

# Generate tasks for a specific table

POST /tasks/execute?taskType=MyCustomTask&tableName=myTable_OFFLINE
```

## Built-in Task Types

Pinot includes several built-in Minion tasks:

<table>
  <thead>
    <tr>
      <th>Task Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`RealtimeToOfflineSegmentsTask`</td>
      <td>Converts realtime segments to offline segments</td>
    </tr>
    <tr>
      <td>`UpsertCompactionTask`</td>
      <td>Compacts segments in upsert-enabled tables</td>
    </tr>
    <tr>
      <td>`UpsertCompactMergeTask`</td>
      <td>Merges and compacts upsert segments</td>
    </tr>
    <tr>
      <td>`PurgeTask`</td>
      <td>Purges records matching a purge function</td>
    </tr>
    <tr>
      <td>`MergeRollupTask`</td>
      <td>Merges and rolls up small segments</td>
    </tr>
    <tr>
      <td>`SegmentGenerationAndPushTask`</td>
      <td>Generates and pushes segments from external data</td>
    </tr>
    <tr>
      <td>`RefreshSegmentTask`</td>
      <td>Refreshes segments from deep store</td>
    </tr>
  </tbody>
</table>

For more details on built-in tasks, see [Minion Merge Rollup Task](../../../operators/operating-pinot/minion-merge-rollup-task.md) and [Upsert Compaction Task](../../../operators/operating-pinot/upsert-compaction-task.md).
