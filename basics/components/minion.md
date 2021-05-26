# Minion

Pinot Minion is a standby component which leverages the [Helix Task Framework](https://engineering.linkedin.com/blog/2019/01/managing-distributed-tasks-with-helix-task-framework) to offload the computationally intensive tasks from other components. It can be attached to an existing Pinot cluster and then execute tasks as provided by the controller. Custom tasks can be plugged via annotations into the cluster. Some typical minion tasks are: segment creation, segment purge, segment merge etc.

## Starting a Minion

To be added

## Add Custom Tasks

### Interfaces

#### PinotTaskGenerator

PinotTaskGenerator interface defines the APIs for controller to generate tasks for minions to execute.

```java
public interface PinotTaskGenerator {

  /**
   * Initializes the task generator.
   */
  void init(ClusterInfoAccessor clusterInfoAccessor);

  /**
   * Returns the task type of the generator.
   */
  String getTaskType();

  /**
   * Generates a list of tasks to schedule based on the given table configs.
   */
  List<PinotTaskConfig> generateTasks(List<TableConfig> tableConfigs);

  /**
   * Returns the timeout in milliseconds for each task, 3600000 (1 hour) by default.
   */
  default long getTaskTimeoutMs() {
    return JobConfig.DEFAULT_TIMEOUT_PER_TASK;
  }

  /**
   * Returns the maximum number of concurrent tasks allowed per instance, 1 by default.
   */
  default int getNumConcurrentTasksPerInstance() {
    return JobConfig.DEFAULT_NUM_CONCURRENT_TASKS_PER_INSTANCE;
  }

  /**
   * Performs necessary cleanups (e.g. remove metrics) when the controller leadership changes.
   */
  default void nonLeaderCleanUp() {
  }
}
```

#### PinotTaskExecutorFactory

Factory for `PinotTaskExecutor` which defines the APIs for minion to execute the tasks.

```java
public interface PinotTaskExecutorFactory {

  /**
   * Initializes the task executor factory.
   */
  void init(MinionTaskZkMetadataManager zkMetadataManager);

  /**
   * Returns the task type of the executor.
   */
  String getTaskType();

  /**
   * Creates a new task executor.
   */
  PinotTaskExecutor create();
}
```

```java
public interface PinotTaskExecutor {

  /**
   * Executes the task based on the given task config and returns the execution result.
   */
  Object executeTask(PinotTaskConfig pinotTaskConfig)
      throws Exception;

  /**
   * Tries to cancel the task.
   */
  void cancel();
}
```

#### MinionEventObserverFactory

Factory for `MinionEventObserver` which defines the APIs for task event callbacks on minion.

```java
public interface MinionEventObserverFactory {

  /**
   * Initializes the task executor factory.
   */
  void init(MinionTaskZkMetadataManager zkMetadataManager);

  /**
   * Returns the task type of the event observer.
   */
  String getTaskType();

  /**
   * Creates a new task event observer.
   */
  MinionEventObserver create();
}
```

```java
public interface MinionEventObserver {

  /**
   * Invoked when a minion task starts.
   *
   * @param pinotTaskConfig Pinot task config
   */
  void notifyTaskStart(PinotTaskConfig pinotTaskConfig);

  /**
   * Invoked when a minion task succeeds.
   *
   * @param pinotTaskConfig Pinot task config
   * @param executionResult Execution result
   */
  void notifyTaskSuccess(PinotTaskConfig pinotTaskConfig, @Nullable Object executionResult);

  /**
   * Invoked when a minion task gets cancelled.
   *
   * @param pinotTaskConfig Pinot task config
   */
  void notifyTaskCancelled(PinotTaskConfig pinotTaskConfig);

  /**
   * Invoked when a minion task encounters exception.
   *
   * @param pinotTaskConfig Pinot task config
   * @param exception Exception encountered during execution
   */
  void notifyTaskError(PinotTaskConfig pinotTaskConfig, Exception exception);
}
```

### Plug-in Tasks

To plug-in a custom task, implement `PinotTaskGenerator`, `PinotTaskExecutorFactory` and `MinionEventObserverFactory` \(optional\) for the task type \(all of them should return the same string for `getTaskType()`\), and annotate them with the following annotations:

| Implementation | Annotation |
| :--- | :--- |
| PinotTaskGenerator | @TaskGenerator |
| PinotTaskExecutorFactory | @TaskExecutorFactory |
| MinionEventObserverFactory | @EventObserverFactory |

After annotating the classes, put them under the package of name `org.apache.pinot.*.plugin.minion.tasks.*`, then they will be auto-registered by the controller and minion.

## Enable Tasks

Tasks are enabled on a per-table basis. To enable a certain task type \(e.g. `myTask`\) on a table, update the table config to include the task type:

```javascript
{
  ...
  "task": {
    "taskTypeConfigsMap": {
      "myTask": {
        "myProperty1": "value1",
        "myProperty2": "value2"
      }
    }
  }
}
```

Under each enable task type, custom properties can be configured for the task type.

## Schedule Tasks

### Auto Schedule

Tasks can be scheduled periodically for all task types on all enabled tables. Enable auto task scheduling by configuring the schedule frequency in the controller config with key `controller.task.frequencyInSeconds`.

### Manual Schedule

Tasks can be manually scheduled using the following controller rest APIs:

| Rest API | Description |
| :--- | :--- |
| **POST /tasks/schedule** | Schedule tasks for all task types on all enabled tables |
| **POST /tasks/schedule?taskType=myTask** | Schedule tasks for the given task type on all enabled tables |
| **POST /tasks/schedule?tableName=myTable\_OFFLINE** | Schedule tasks for all task types on the given table |
| **POST /tasks/schedule?taskType=myTask&tableName=myTable\_OFFLINE** | Schedule tasks for the given task type on the given table |

## Example Tasks

### RealtimeToOfflineSegmentsTask

See [Pinot managed Offline flows](../../operators/operating-pinot/pinot-managed-offline-flows.md) for details.

### TestTask

See [SimpleMinionClusterIntegrationTest](https://github.com/apache/incubator-pinot/blob/master/pinot-integration-tests/src/test/java/org/apache/pinot/integration/tests/SimpleMinionClusterIntegrationTest.java) for details.

