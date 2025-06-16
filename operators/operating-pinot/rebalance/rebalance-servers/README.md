# Rebalance Servers

The rebalance operation is used to recompute the assignment of brokers or servers in the cluster. This is not a single command, but rather a series of steps that need to be taken.

In the case of servers, rebalance operation is used to balance the distribution of the segments amongst the servers being used by a Pinot table. This is typically done after capacity changes or config changes such as replication or segment assignment strategies or table migration to a different tenant.

## Changes that require a rebalance

Below are changes that need to be followed by a rebalance.

1. Capacity changes
2. Increasing/decreasing replication for a table
3. Changing segment assignment for a table
4. Moving table from one tenant to a different tenant

### Capacity changes

These are typically done when downsizing/uplifting a cluster or replacing nodes of a cluster.

#### Tenants and tags

Every server added to the Pinot cluster has tags associated with it. A group of servers with the same tag forms a server tenant.

By default, a server in the cluster gets added to the `DefaultTenant` i.e. gets tagged as `DefaultTenant_OFFLINE` and `DefaultTenant_REALTIME`.

Below is an example of how this looks in the znode, as seen in ZooInspector.

![](../../../../.gitbook/assets/zookeeper-browser-server-tenant.png)

A Pinot table config has a tenants section, to define the tenant to be used by the table. The Pinot table will use all the servers which belong to the tenant as described in this config. For more details about this, see the [Tenants](../../../../basics/components/cluster/tenant.md) section.

```
 {   
    "tableName": "myTable_OFFLINE",
    "tenants" : {
      "broker":"DefaultTenant",
      "server":"DefaultTenant"
    }
  }
```

#### Updating tags

_**0.6.0 onwards**_

In order to change the server tags, use the following API.

`PUT /instances/{instanceName}/updateTags?tags=<comma separated tags>`

_**0.5.0 and prior**_

UpdateTags API is not available in 0.5.0 and prior. Instead, use this API to update the Instance.

`PUT /instances/{instanceName}`

For example,

```
curl -X PUT "http://localhost:9000/instances/Server_10.1.10.51_7000" 
    -H "accept: application/json" 
    -H "Content-Type: application/json" 
    -d "{ \"host\": \"10.1.10.51\", \"port\": \"7000\", \"type\": \"SERVER\", \"tags\": [ \"newName_OFFLINE\", \"DefaultTenant_REALTIME\" ]}"
```

{% hint style="danger" %}
**NOTE**

The output of GET and input of PUT don't match for this API. Make sure to use the right payload as shown in example above. Particularly, notice that the instance name "Server\_host\_port" gets split up into separate fields in this PUT API.
{% endhint %}

When upsizing/downsizing a cluster, you will need to make sure that the host names of servers are consistent. You can do this by setting the following config parameter:

```
pinot.set.instance.id.to.hostname=true
```

### Replication changes

In order to change the replication factor of a table, update the table config as follows:

OFFLINE table - update the `replication` field

REALTIME table - update the `replicasPerPartition` field

### Segment Assignment changes

The most common segment assignment change is moving from the default segment assignment to replica group segment assignment. Discussing the details of the segment assignment is beyond the scope of this page. More details can be found in [Routing](../../tuning/routing.md) and in this [FAQ question](../../../../basics/getting-started/frequent-questions/#docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3).

### Table Migration to a different tenant

In a scenario where you need to move table across tenants, for e.g table was assigned earlier to a different Pinot tenant and now you want to move it to a separate one, then you need to call the rebalance API with reassignInstances set to true.

To move a table to other tenants, modify the following configs in both realtime and offline tables:

{% tabs %}
{% tab title="REALTIME" %}
```
"REALTIME": {
  ...
  "tenants": {
    ...
    "server": "<tenant_name>",
    ...
  },
  ...
  "instanceAssignmentConfigMap": {
    ...
    "CONSUMING": {
      ...
      "tagPoolConfig": {
        ...
        "tag": "<tenant_name>_REALTIME",
        ...
      },
      ...
    },
    ...
    "COMPLETED": {
      ...
      "tagPoolConfig": {
        ...
        "tag": "<tenant_name>_REALTIME",
        ...
      },
      ...
    },
    ...
  },
  ...
}
```
{% endtab %}

{% tab title="OFFLINE" %}
```
"OFFLINE": {
  ...
  "tenants": {
    ...
    "server": "<tenant_name>",
    ...
  },
  ...
  "instanceAssignmentConfigMap": {
    ...
    "OFFLINE": {
      ...
      "tagPoolConfig": {
        ...
        "tag": "<tenant_name>_OFFLINE",
        ...
      },
      ...
    },
    ...
  },
  ...
}
```
{% endtab %}
{% endtabs %}

## Rebalance Algorithms

Currently, two rebalance algorithms are supported; one is the default algorithm and the other one is minimal data movement algorithm.

### The Default Algorithm

This algorithm is used for most of the cases. When `reassignInstances` parameter is set to true, the final lists of instance assignment will be re-computed, and the list of instances is sorted per partition per replica group. Whenever the table rebalance is run, segment assignment will respect the sequence in the sorted list and pick up the relevant instances.

### Minimal Data Movement Algorithm

This algorithm focuses more on minimizing the data movement during table rebalance. When `reassignInstances` parameter is set to true and this algorithm gets enabled, the position of instances which are still alive remains the same, and vacant seats are filled with newly added instances or last instances in the existing alive instance candidate. So only the instances which change the position will involve in data movement.

In order to switch to this table rebalance algorithm, just simply set the following config to the table config before triggering table rebalance:

```
"instanceAssignmentConfigMap": {
  ...
  "OFFLINE": {
    ...
    "replicaGroupPartitionConfig": {
      ...
      "minimizeDataMovement": true,
      ...
    },
    ...
  },
  ...
}
```

When `instanceAssignmentConfigMap` is not explicitly configured, `minimizeDataMovement` flag can also be set into the `segmentsConfig`:

```
"segmentsConfig": {
    ...
    "minimizeDataMovement": true,
    ...
}
```

## Running a Rebalance

After any of the above described changes are done, a rebalance is needed to make those changes take effect.

To run a rebalance, use the following API.

`POST /tables/{tableName}/rebalance?type=<OFFLINE/REALTIME>`

This API has a lot of parameters to control its behavior. Make sure to go over them and change the defaults as needed.

{% hint style="warning" %}
**Note**

Typically, the flags that need to be changed from the default values are

**includeConsuming=true** for REALTIME

**downtime=true** if you have only 1 replica, or prefer a faster rebalance at the cost of a momentary downtime
{% endhint %}

### Rebalance Parameters

| Query param                          | Default value | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------ | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dryRun                               | false         | If set to true, **rebalance is run as a dry-run** so that you can see the expected changes to the ideal state and instance partition assignment.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| preChecks                            | false         | If set to true, some pre-checks are performed and their status is returned. This can only be used with **dryRun=true.** See the section below for more details.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| includeConsuming                     | true          | <p>Applicable for REALTIME tables.</p><p><strong>CONSUMING segments are rebalanced only if this is set to true</strong>.<br>Moving a CONSUMING segment involves dropping the data consumed so far on old server, and re-consuming on the new server. If an application is sensitive to <strong>increased memory utilization due to re-consumption or to a momentary data staleness</strong>, they may choose to not include consuming in the rebalance. Whenever the CONSUMING segment completes, the completed segment will be assigned to the right instances, and the new CONSUMING segment will also be started on the correct instances. If you choose to includeConsuming=false and let the segments move later on, any downsized nodes need to remain untagged in the cluster, until the segment completion happens.</p>                                                                         |
| downtime                             | false         | <p><strong>This controls whether Pinot allows downtime while rebalancing.</strong><br>If downtime = true, all replicas of a segment can be moved around in one go, which could result in a momentary downtime for that segment (time gap between ideal state updated to new servers and new servers downloading the segments).<br>If downtime = false, Pinot will make sure to keep certain number of replicas (config in next row) always up. The rebalance will be done in multiple iterations under the hood, in order to fulfill this constraint.</p><p></p><p><strong>Warning:</strong> If peer-download is enabled for a REALTIME table, it is not recommended to rebalance with downtime=true or minAvailableReplicas=0 to avoid potential data loss.</p><p></p><p><strong>Note</strong>: <em>If you have only 1 replica for your table, rebalance with downtime=false is not possible.</em></p> |
| minAvailableReplicas                 | -1            | <p>Applicable for rebalance with downtime=false.</p><p>This is the <strong>minimum number of replicas that are expected to stay alive</strong> through the rebalance.</p><p></p><p><strong>Warning:</strong> If peer-download is enabled for a REALTIME table, it is not recommended to rebalance with downtime=true or minAvailableReplicas=0 to avoid potential data loss.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| lowDiskMode                          | false         | <p>Applicable for rebalance with downtime=false.<br>When enabled, segments will first be offloaded from servers, then added to servers after offload is done. It may increase the total time of the rebalance, but can be useful when servers are low on disk space, and we want to scale up the cluster and rebalance the table to more servers.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| bestEfforts                          | false         | <p>Applicable for rebalance with downtime=false.</p><p>If a no-downtime rebalance cannot be performed successfully, this flag <strong>controls whether to fail the rebalance or do a best-effort rebalance</strong>. <strong>Warning:</strong> <em>setting this flag to true can cause downtime under two scenarios: 1) any segments get into ERROR state and 2) EV-IS convergence times out</em></p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| reassignInstances                    | true          | Applicable to tables where the instance assignment has been persisted to zookeeper. Setting this to true will make the rebalance **first update the instance assignment, and then rebalance the segments**. This option should be set to true if the instance assignment will be changed (e.g. increasing replication or instances per replica for replicaGroup based assignment)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| minimizeDataMovement                 | ENABLE        | Whether to ENABLE minimizeDataMovement, DISABLE it, or DEFAULT to the value in the TableConfig. If enabled, it reduces the segments that will be moved by trying to minimize the changes to the instance assignment. For tables using implicit instance assignment (no INSTANCE\_PARTITIONS) this is a no-op.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| batchSizePerServer                   | -1            | How many maximum segment adds per server to update in the IdealState in each step. For non-strict replica group based assignment, this number will be capped at the batchSizePerServer value per rebalance step (some servers may get fewer segments). For strict replica group based assignment, this is a per-server best effort value since each partition of a replica group must be moved as a whole and at least one partition in a replica group should be moved. A value of -1 is used to disable batching (select as many segments as possible per incremental step in rebalance such that minAvailableReplicas is honored). Support for batching is available from commit [https://github.com/apache/pinot/pull/15617](https://github.com/apache/pinot/pull/15617) onwards.                                                                                                                   |
| bootstrap                            | false         | Rebalances all segments again, **as if adding segments to an empty table**. If this is false, then the rebalance will try to minimize segment movements. **Warning:** _Only use this option if a reshuffle of all segments is desirable._                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| externalViewCheckIntervalInMs        | 1000          | How often to check if external view converges with ideal states                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| externalViewStabilizationTimeoutInMs | 3600000       | Maximum time (in milliseconds) to wait for external view to converge with ideal states. It automatically extends the time if progress has been made                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| heartbeatIntervalInMs                | 300000        | How often to make a status update (i.e. heartbeat)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| heartbeatTimeoutInMs                 | 3600000       | How long to wait for next status update (i.e. heartbeat) before the job is considered failed                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| maxAttempts                          | 3             | Max number of attempts to rebalance                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| retryInitialDelayInMs                | 300000        | Initial delay to exponentially backoff retry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| updateTargetTier                     | false         | Whether to update segment target tier as part of the rebalance. Only relevant for tiered storage enabled tables.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

### Checking status

The following API is used to check the progress of a rebalance Job. The API takes the jobId of the rebalance job. The API to see the jobIds of rebalance Jobs for a table is shown next.

{% hint style="warning" %}
Note that rebalanceStatus API is available from this [commit](https://github.com/apache/pinot/pull/10359)
{% endhint %}

```
curl -X GET "https://localhost:9000/rebalanceStatus/ffb38717-81cf-40a3-8f29-9f35892b01f9" -H "accept: application/json"
```

```json
{"tableRebalanceProgressStats": {
    "startTimeMs": 1679073157779,
    "status": "DONE", // IN_PROGRESS/DONE/FAILED    
    "timeToFinishInSeconds": 0, // Time it took for the rebalance job after it completes/fails 
    "completionStatusMsg": "Finished rebalancing table: airlineStats_OFFLINE with minAvailableReplicas: 1, enableStrictReplicaGroup: false, bestEfforts: false in 44 ms."
     
     // The total amount of work required for rebalance 
    "initialToTargetStateConvergence": {
      "_segmentsMissing": 0, // Number of segments missing in the current state but present in the target state
      "_segmentsToRebalance": 31, // Number of segments that needs to be assigned to hosts so that the current state can get to the target state.
      "_percentSegmentsToRebalance": 100, // Total number of replicas that needs to be assigned to hosts so that the current state can get to the target state.
      "_replicasToRebalance": 279 // Remaining work to be done in %
    },
    
    // The pending work for rebalance
    "externalViewToIdealStateConvergence": {
      "_segmentsMissing": 0,
      "_segmentsToRebalance": 0,
      "_percentSegmentsToRebalance": 0,
      "_replicasToRebalance": 0
    },
    
    // Additional work to catch up with the new ideal state, when the ideal 
    // state shifts since rebalance started. 
    "currentToTargetConvergence": {
      "_segmentsMissing": 0,
      "_segmentsToRebalance": 0,
      "_percentSegmentsToRebalance": 0,
      "_replicasToRebalance": 0
    },
  },
  "timeElapsedSinceStartInSeconds": 28 // If rebalance is IN_PROGRESS, this gives the time elapsed since it started
  }
```

Below is the API to get the jobIds of rebalance jobs for a given table. The API takes the table name and jobType which is TABLE\_REBALANCE.

```
curl -X GET "https://localhost:9000/table/airlineStats_OFFLINE/jobstype=OFFLINE&jobTypes=TABLE_REBALANCE" -H "accept: application/json"
```

```json
 "ffb38717-81cf-40a3-8f29-9f35892b01f9": {
    "jobId": "ffb38717-81cf-40a3-8f29-9f35892b01f9",
    "submissionTimeMs": "1679073157804",
    "jobType": "TABLE_REBALANCE",
    "REBALANCE_PROGRESS_STATS": "{\"initialToTargetStateConvergence\":{\"_segmentsMissing\":0,\"_segmentsToRebalance\":31,\"_percentSegmentsToRebalance\":100.0,\"_replicasToRebalance\":279},\"externalViewToIdealStateConvergence\":{\"_segmentsMissing\":0,\"_segmentsToRebalance\":0,\"_percentSegmentsToRebalance\":0.0,\"_replicasToRebalance\":0},\"currentToTargetConvergence\":{\"_segmentsMissing\":0,\"_segmentsToRebalance\":0,\"_percentSegmentsToRebalance\":0.0,\"_replicasToRebalance\":0},\"startTimeMs\":1679073157779,\"status\":\"DONE\",\"timeToFinishInSeconds\":0,\"completionStatusMsg\":\"Finished rebalancing table: airlineStats_OFFLINE with minAvailableReplicas: 1, enableStrictReplicaGroup: false, bestEfforts: false in 44 ms.\"}",
    "tableName": "airlineStats_OFFLINE"
```

{% hint style="warning" %}
Note that rebalanceStatus API's result has changed from this [commit](https://github.com/apache/pinot/pull/15266) to add two sections to the existing stats. The goal is to eventually remove the existing stats in favor of these new ones.
{% endhint %}

From [commit](https://github.com/apache/pinot/pull/15266) onwards, the stats will include the following newly added sections to the original stats posted above:

```json
  "rebalanceProgressStatsOverall": { // Meant to be used to track overall progress of the rebalance job
    "totalSegmentsToBeAdded": 60, // Segments to be added overall as part of this rebalance job
    "totalSegmentsToBeDeleted": 60, // Segments to be deleted overall as part of this rebalance job
    "totalRemainingSegmentsToBeAdded": 21, // Segments that are yet to be added
    "totalRemainingSegmentsToBeDeleted": 15, // Segments that are yet to be deleted
    "totalRemainingSegmentsToConverge": 0, // Segments that belong to the correct instance but who's EV state doesn't match the expected IS state
    "totalCarryOverSegmentsToBeAdded": 0, // Segments adds carried over from the previous rebalance step
    "totalCarryOverSegmentsToBeDeleted": 0, // Segment deletes carried over from the previous rebalance step
    "totalUniqueNewUntrackedSegmentsDuringRebalance": 0, // Newly added segments detected but which are not yet monitored by the rebalance job, some of these may be monitored later
    "percentageRemainingSegmentsToBeAdded": 35, // Percentage segments yet to be added (including carry-over segments)
    "percentageRemainingSegmentsToBeDeleted": 25, // Percentage segments yet to be deleted (including carry-over segments)
    "estimatedTimeToCompleteAddsInSeconds": 10476.487, // Estimated time to complete segment adds in seconds based on historical time taken so far
    "estimatedTimeToCompleteDeletesInSeconds": 6485.444333333333, // Estimated time to complete segment deletes in seconds based on historical time taken so far
    "averageSegmentSizeInBytes": 5448028669, // Average segment size in bytes
    "totalEstimatedDataToBeMovedInBytes": 326881720140, // Total estimated data to be moved (total segments to be added * average segment size)
    "startTimeMs": 1744393492152 // Start time of the rebalance job
  },
  "rebalanceProgressStatsCurrentStep": { // Captures the stats of the current rebalance step being performed
    "totalSegmentsToBeAdded": 45, // Segments to be added as part of this rebalance step
    "totalSegmentsToBeDeleted": 45, // Segments to be deleted as part of this rebalance step
    "totalRemainingSegmentsToBeAdded": 6, // Segments that are yet to be added in this rebalance step
    "totalRemainingSegmentsToBeDeleted": 0, // Segments that are yet to be deleted in this rebalance step
    "totalRemainingSegmentsToConverge": 0, // Segments that belong to the correct instance but who's EV state doesn't match the expected IS state
    "totalCarryOverSegmentsToBeAdded": 0, // Segments adds carried over from the previous rebalance step
    "totalCarryOverSegmentsToBeDeleted": 0, // Segments deletes carried over from the previous rebalance step
    "totalUniqueNewUntrackedSegmentsDuringRebalance": 0, // Newly added segments detected but which are not yet monitored by the rebalance job, some of these may be monitored later
    "percentageRemainingSegmentsToBeAdded": 13.333333333333334, // Percentage segments yet to be added (including carry-over segments due to which it may show > 100%)
    "percentageRemainingSegmentsToBeDeleted": 0, // Percentage segments yet to be deleted (including carry-over segments due to which it may show > 100%)
    "estimatedTimeToCompleteAddsInSeconds": 2993.278923076923, // Estimated time to complete segment adds in seconds for the current step
    "estimatedTimeToCompleteDeletesInSeconds": 0, // Estimated time to complete segment deletes in seconds for the current step
    "averageSegmentSizeInBytes": 5448028669, // Average segment size in bytes
    "totalEstimatedDataToBeMovedInBytes": 245161290105, // Total estimated data to be moved (total segments to be added in this step * average segment size)
    "startTimeMs": 1744393492172 // Start time of the current rebalance step
  },
```

In the new stats above, `rebalanceProgressStatsOverall` is meant for tracking the overall progress of the rebalance job and is the main stats to monitor. The `rebalanceProgressStatsCurrentStep` are used to calculate the overall stats, but do not need to be monitored for obtaining the overall rebalance status since the overall stats will be updated regularly. The `rebalanceProgressStatsCurrentStep` can be used for debugging if needed.

## Canceling Rebalance Jobs

The need may arise to cancel a rebalance job. To do this an API exists which cancels all `IN_PROGRESS` jobs for the given table. Few caveats about cancellation which one should keep in mind are:

* Any updates to the `IdealState` that was already made as part of the rebalance job will continue to be processed. Cancellation prevents the `TableRebalancer` from making future updates to the `IdealState` as part of the rebalance job.
* Cancellation does not rollback the state of the cluster to what it was prior to triggering the rebalance, thus leaving the cluster in an inconsistent state.
* To fix the inconsistent state caused by a cancel, fix up the cluster components due to which the rebalance was canceled (if needed) and re-trigger a new rebalance job. The new job should help get the cluster into the final state.

Rebalance jobs for a given table can be canceled via the following API:

```
curl -X 'DELETE' 'http://localhost:9000/tables/airlineStats/rebalance?type=OFFLINE' -H 'accept: application/json'
```

The above API will return a list of `jobIds` that were canceled.

```
[
  "ffb38717-81cf-40a3-8f29-9f35892b01f9"
]
```

## Rebalance Pre-Checks

With options `dryRun=true, preChecks=true`, some pre-checks relevant to rebalance will be performed:

| Pre-check item name            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Result                                                                                                                                                                                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| isMinimizeDataMovement         | Check if the rebalance will run with `minimizeDataMovement=true` . This is an important flag for instance assignment strategies such as replicaGroups which controls how much data movement may occur.                                                                                                                                                                                                                                                                            | <p>PASS if enabled, or when this flag is irrelevant.<br><br>WARN if it's not enabled.</p>                                                                                                                                                                                  |
| diskUtilizationDuringRebalance | <p>Check if the disk utilization could become a problem "during" rebalance based on a default threshold defined by the config (defaulted to 0.9): <code>controller.rebalance.disk.utilization.threshold</code> .<br><br>Note that this pre-check could have false negatives. The pre-check passes but a server could still suffer from disk utilization problem, as there are other sources that increase the disk usage, especially under a long time running rebalance job.</p> | <p>PASS if the disk utilization of all servers in the rebalance will be within <code>controller.rebalance.disk.utilization.threshold</code> if all assigned segments added. <br><br>ERROR otherwise, and show the problematic servers.</p>                                 |
| diskUtilizationAfterRebalance  | <p>Similar to <code>diskUtilizationDuringRebalance</code> but checks the size "after" the rebalance.<br><br>This test could pass while <code>diskUtilizationDuringRebalance</code> fails. For example, a server gets segments but also will delete some, and the net size change falls in the threshold.</p>                                                                                                                                                                      | <p>PASS if the disk utilization of all servers in the rebalance will be within <code>controller.rebalance.disk.utilization.threshold</code> if all assigned segments added and unassigned segments removed. <br><br>ERROR otherwise, and show the problematic servers.</p> |
| needsReloadStatus              | Check if any of the servers needs to be reloaded (do the segments on these servers need to be updated based on the latest TableConfig and Schema).                                                                                                                                                                                                                                                                                                                                | <p>PASS if all servers assigned to the table don't need a reload.<br><br>WARN if any of the server need a reload.<br><br>ERROR if any of the server fails to answer the need reload status.</p>                                                                            |
| rebalanceConfigOptions         | Mark any parameters in the rebalance that need a double check, as they might cause performance impact                                                                                                                                                                                                                                                                                                                                                                             | <p>PASS if no rebalance parameter needs a double-check.<br><br>WARN if any rebalance parameter that is flagged is set, followed by the description.</p>                                                                                                                    |
| replicaGroupsInfo              | If replicaGroups are enabled, provides information about the number of replica groups and the number of instances per replica group, otherwise provides information about the replication factor. Provides information for OFFLINE, CONSUMING, COMPLETED and tier depending on what is enabled.                                                                                                                                                                                   | <p>PASS if replicaGroups are disabled or if enabled but the rebalance config reassignInstances=true<br><br>WARN if replicaGroups is enabled but the rebalance config reassignInstances=false</p>                                                                           |

For each check the return includes a `preCheckStatus`which is one of: `PASS`|`WARN`|`ERROR` and a message to explain what the status means from this OSS PR [https://github.com/apache/pinot/pull/15233](https://github.com/apache/pinot/pull/15233) onwards. Prior to this, these just returned `true`| `false`|`error` with no further explanation.

### Example

```json
  "preChecksResult": {
    "isMinimizeDataMovement": {
      "preCheckStatus": "PASS",
      "message": "minimizeDataMovement is enabled"
    },
    "diskUtilizationDuringRebalance" : {
      "preCheckStatus" : "PASS",
      "message" : "Within threshold (<90%)"
    },
    "diskUtilizationAfterRebalance" : {
      "preCheckStatus" : "PASS",
      "message" : "Within threshold (<90%)"
    },
    "replicaGroupsInfo": {
      "preCheckStatus": "PASS",
      "message": "COMPLETED segments - Replica Groups are not enabled, replication: 1\nCONSUMING segments - Replica Groups are not enabled, replication: 1"
    },
    "needsReloadStatus": {
      "preCheckStatus": "ERROR",
      "message": "Could not determine needReload status, run needReload API manually"
    },
    "rebalanceConfigOptions": {
      "preCheckStatus": "PASS",
      "message": "All rebalance parameters look good"
    }
  },
```

The `ERROR` status for `needsReloadStatus` above maybe due to errors returned by a subset of servers hosting the segments. In such cases, it is recommended to try again or run it manually via `needReload` API.

As part of  [PR #15360](https://github.com/apache/pinot/pull/15360), a fix was made to fetch the status from the servers currently assigned in the IdealState rather than relying on the tagged instances as this may change as part of rebalance. Prior to this PR, even for scenarios such as tenant move, `ERROR` status would be thrown.

## Rebalance Summary

Rebalance (without or without `dryRun=true`) will return a summary of the changes that will occur during the rebalance along with the usual instance and segment assignments. Right now, the summary has three different sections:

* Server level - captures information about changes occurring at the server level and also dumps per server information about changes taking place.
* Segment level - captures information about changes happening at the segment level
* Tag level - aggregate information about segment changes, grouped by server tags

Fields such as the `status` and `description` can be used to identify whether the rebalance will result in any change or not (`status=NO-OP` indicates that the table is already balanced), and can be a quick check prior to checking the summary.

See [examples-and-scenarios.md](examples-and-scenarios.md "mention") for how the rebalance summary looks under different scenarios.

### Server Level (serverInfo)

| Field                        | Description                                                                                                                                                                                                                                                                                                     |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| numServersGettingNewSegments | The number of servers that will get new segment replicas added as part of this rebalance.                                                                                                                                                                                                                       |
| numServers                   | The number of servers assigned to this table, including values before and after the rebalance.                                                                                                                                                                                                                  |
| serversAdded                 | A list of servers to be newly added to the assignment of this table in this rebalance.                                                                                                                                                                                                                          |
| serversRemoved               | A list of servers to be removed from the assignment of this table in this rebalance.                                                                                                                                                                                                                            |
| serversUnchanged             | A list of servers remaining unchanged in the assignment of this table in this rebalance.                                                                                                                                                                                                                        |
| serversGettingNewSegments    | A list of servers that will get new segment replicas added in this rebalance.                                                                                                                                                                                                                                   |
| serverSegmentChangeInfo      | A detail breakdown of the segment change information per server. This includes segments to be added, deleted, unchanged, the total segments assigned to this server before and after the rebalance, and the tag list for the given server. See [examples-and-scenarios.md](examples-and-scenarios.md "mention") |

### Segment Level (segmentInfo)

| Field                                                                               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| totalSegmentsToBeMoved                                                              | The number of segment replicas that will be added across all servers. This is essentially equivalent to how many segments the servers need to download.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| totalSegmentsToBeDeleted                                                            | The number of segment replicas that will be removed from across all servers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| maxSegmentsAddedToASingleServer                                                     | The maximum number of segment replicas added to a single server across all servers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| estimatedAverageSegmentSizeInBytes                                                  | The average size of a segment in one replica of this table.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| totalEstimatedDataToBeMovedInBytes                                                  | <p>Calculated by</p><p><code>segmentInfo.totalSegmentsToBeMoved * segmentInfo.estimatedAverageSegmentSizeInBytes</code></p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| replicationFactor                                                                   | The number of replications, including values before and after the rebalance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| numSegmentsInSingleReplica                                                          | The number of segments in a single replica, including values before and after the rebalance.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| numSegmentsAcrossAllReplicas                                                        | The total number of segment replicas, including values before and after the rebalance. Equivalent to `segmentInfo.replicationFactor * segmentInfo.numSegmentsInSingleReplica`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| consumingSegmentToBeMovedSummary.numConsumingSegmentsToBeMoved                      | <p>For REALTIME tables, the number of CONSUMING segment replicas that will be added to a server. A segment replica is a CONSUMING segment replica if none of the replica of the segment is ONLINE and any of the replica of the segment is CONSUMING.<br><br>OFFLINE tables do not have this field.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| consumingSegmentToBeMovedSummary.numServersGettingConsumingSegmentsAdded            | <p>For REALTIME tables, the number of servers that will get a new CONSUMING segment replicas.<br><br>OFFLINE tables do not have this field.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| consumingSegmentToBeMovedSummary.consumingSegmentsToBeMovedWithMostOffsetsToCatchUp | <p>For REALTIME tables, up to the top 10 CONSUMING segments with the largest offset difference between the start offset and the latest offset across all consuming segments being added servers. This determines how many offsets a server needs to re-consume from the stream after adding this CONSUMING segment replica. The actual overhead (memory / CPU utilization) of re-consuming depends on the data in the stream as the overhead varies across different streams.</p><p></p><p>This is meant to be an indicator for the amount of work (and thus additional resource utilization) that needs to be redone when the CONSUMING segment moves and can be used to decided whether a <code>forceCommit</code> is desirable prior to rebalance.</p><p><br>Note that only ingestion from Kafka has this information available as of now. If the information cannot be fetched, this field will not be included in the summary.<br><br>OFFLINE tables do not have this field.</p> |
| consumingSegmentToBeMovedSummary.consumingSegmentsToBeMovedWithOldestAgeInMinutes   | <p>For REALTIME tables, up to the top 10 oldest CONSUMING segments based on their segment creation time in the SegmentZkMetadata across all consuming segments being added to servers. This approximates the oldest data that will need to be re-consumed when the segment is moved and can give a high-level estimate of staleness.<br>Note that this is captured as the segment's creation time instead of the actual data age. The oldest event covered by the consuming segment might be older or newer than the segment's creation time and is dependent on the stream's data. If the information cannot be fetched, this field will not be included in the summary.</p><p></p><p>This is meant to be an indicator for the data staleness expected while running queries when the CONSUMING segment moves and can be used to decided whether a <code>forceCommit</code> is desirable prior to rebalance.</p><p><br>OFFLINE tables do not have this field.</p>                    |
| consumingSegmentToBeMovedSummary.serverConsumingSegmentSummary                      | <p>For REALTIME tables, a map from server name to its detailed information of consuming segments that are added to the server. Each has two fields <code>numConsumingSegmentsToBeAdded</code> and <code>totalOffsetsToCatchUpAcrossAllConsumingSegments</code> . If the offset information fails to be fetched, the latter will be set to <code>-1</code> .<br><br>OFFLINE tables do not have this field.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

### Tag Level (tagsInfo)

A list of aggregated segment and server related statistics grouped by tags. See [examples-and-scenarios.md](examples-and-scenarios.md "mention")\
\
All the tags present in the table config will be present here. It is possible that a server has multiple tags present in the tag list here. In this case, the statistics will be accounted for all relevant tags.\
\
If an assigned server does not contain any tag present in the table config (could happen when a table has instance partition and rebalanced with `reassignInstance=false`), it will be categorized under a special tag `OUTDATED_SERVERS`.

The fields of each entry will consist of:

| Field                 | Description                                                                    |
| --------------------- | ------------------------------------------------------------------------------ |
| tagName               | Name of the tag                                                                |
| numSegmentsToDownload | Number of segments that will be downloaded on servers tagged with this tagName |
| numSegmentsUnchanged  | Number of segments that will remain on the servers tagged with this tagName    |
| numServerParticipants | Total number of servers tagged wtih tagName                                    |

### Example Output

```json
"rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 1
      },
      "serversAdded": [],
      "serversRemoved": [
        "Server_7051"
      ],
      "serversUnchanged": [
        "Server_7050"
      ],
      "serversGettingNewSegments": [
        "Server_7050"
      ],
      "serverSegmentChangeInfo": {
        "Server_7051": {
          "serverStatus": "REMOVED",
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 5,
          "segmentsAdded": 0,
          "segmentsDeleted": 5,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE"
          ]
        },
        "Server_7050": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 10,
          "totalSegmentsBeforeRebalance": 5,
          "segmentsAdded": 5,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 5,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 5,
      "totalSegmentsToBeDeleted": 5,
      "maxSegmentsAddedToASingleServer": 5,
      "estimatedAverageSegmentSizeInBytes": 0,
      "totalEstimatedDataToBeMovedInBytes": 0,
      "replicationFactor": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 1
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 10,
        "expectedValueAfterRebalance": 10
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 10,
        "expectedValueAfterRebalance": 10
      },
      "consumingSegmentToBeMovedSummary": {
        "numConsumingSegmentsToBeMoved": 5,
        "numServersGettingConsumingSegmentsAdded": 1,
        "consumingSegmentsToBeMovedWithMostOffsetsToCatchUp": {
          "airlineStats__6__0__20250414T2046Z": 289,
          "airlineStats__4__0__20250414T2046Z": 287,
          "airlineStats__8__0__20250414T2046Z": 283,
          "airlineStats__2__0__20250414T2046Z": 270,
          "airlineStats__0__0__20250414T2046Z": 265
        },
        "consumingSegmentsToBeMovedWithOldestAgeInMinutes": {
          "airlineStats__8__0__20250414T2046Z": 45,
          "airlineStats__4__0__20250414T2046Z": 45,
          "airlineStats__2__0__20250414T2046Z": 45,
          "airlineStats__6__0__20250414T2046Z": 45,
          "airlineStats__0__0__20250414T2046Z": 45
        },
        "serverConsumingSegmentSummary": {
          "Server_7050": {
            "numConsumingSegmentsToBeAdded": 5,
            "totalOffsetsToCatchUpAcrossAllConsumingSegments": 1394
          }
        }
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_REALTIME",
        "numSegmentsToDownload": 5,
        "numSegmentsUnchanged": 5,
        "numServerParticipants": 1
      }
    ]
  },
```
