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

Every server added to the Pinot cluster, has tags associated with it. A group of servers with the same tag forms a Server Tenant.

By default, a server in the cluster gets added to the `DefaultTenant` i.e. gets tagged as `DefaultTenant_OFFLINE` and `DefaultTenant_REALTIME`.

Below is an example of how this looks in the znode, as seen in ZooInspector.

![](<../../../.gitbook/assets/Screen Shot 2020-09-08 at 2.05.29 PM.png>)

A Pinot table config has a tenants section, to define the tenant to be used by the table. The Pinot table will use all the servers which belong to the tenant as described in this config. For more details about this, see the [Tenants](../../../basics/components/cluster/tenant.md) section.

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

In order to change the server tags, the following API can be used.

`PUT /instances/{instanceName}/updateTags?tags=<comma separated tags>`

![](<../../../.gitbook/assets/Screen Shot 2020-09-08 at 2.29.44 PM.png>)

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

The output of GET and input of PUT don't match for this API. Make sure to use the right payload as shown in example above. Particularly, notice that instance name "Server\_host\_port" gets split up into their own fields in this PUT API.
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

The most common segment assignment change is moving from the default segment assignment to replica group segment assignment. Discussing the details of the segment assignment is beyond the scope of this page. More details can be found in [Routing](../tuning/routing.md) and in this [FAQ question](../../../basics/getting-started/frequent-questions/#docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3).

### Table Migration to a different tenant

In a scenario where you need to move table across tenants, for e.g table was assigned earlier to a different Pinot tenant and now you want to move it to a separate one, then you need to call the rebalance API with reassignInstances set to true.

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

![](<../../../.gitbook/assets/Screen Shot 2020-09-08 at 2.53.48 PM.png>)

This API has a lot of parameters to control its behavior. Make sure to go over them and change the defaults as needed.

{% hint style="warning" %}
**Note**

Typically, the flags that need to be changed from defaults are

**includeConsuming=true** for REALTIME

**downtime=true** if you have only 1 replica, or prefer faster rebalance at the cost of a momentary downtime
{% endhint %}

| Query param          | Default value | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| -------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dryRun               | false         | If set to true, **rebalance is run as a dry-run** so that you can see the expected changes to the ideal state and instance partition assignment.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| includeConsuming     | false         | <p>Applicable for REALTIME tables.</p><p><strong>CONSUMING segments are rebalanced only if this is set to true</strong>.<br>Moving a CONSUMING segment involves dropping the data consumed so far on old server, and re-consuming on the new server. If an application is sensitive to <strong>increased memory utilization due to re-consumption or to a momentary data staleness</strong>, they may choose to not include consuming in the rebalance. Whenever the CONSUMING segment completes, the completed segment will be assigned to the right instances, and the new CONSUMING segment will also be started on the correct instances. If you choose to includeConsuming=false and let the segments move later on, any downsized nodes need to remain untagged in the cluster, until the segment completion happens.</p> |
| downtime             | false         | <p><strong>This controls whether Pinot allows downtime while rebalancing.</strong><br>If downtime = true, all replicas of a segment can be moved around in one go, which could result in a momentary downtime for that segment (time gap between ideal state updated to new servers and new servers downloading the segments).<br>If downtime = false, Pinot will make sure to keep certain number of replicas (config in next row) always up. The rebalance will be done in multiple iterations under the hood, in order to fulfill this constraint.</p><p><strong>Note</strong>: <em>If you have only 1 replica for your table, rebalance with downtime=false is not possible.</em></p>                                                                                                                                       |
| minAvailableReplicas | 1             | <p>Applicable for rebalance with downtime=false.</p><p>This is the <strong>minimum number of replicas that are expected to stay alive</strong> through the rebalance.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| bestEfforts          | false         | <p>Applicable for rebalance with downtime=false.</p><p>If a no-downtime rebalance cannot be performed successfully, this flag <strong>controls whether to fail the rebalance or do a best-effort rebalance</strong>.</p>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| reassignInstances    | false         | Applicable to tables where the instance assignment has been persisted to zookeeper. Setting this to true will make the rebalance **first update the instance assignment, and then rebalance the segments**.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| bootstrap            | false         | Rebalances all segments again, **as if adding segments to an empty table**. If this is false, then the rebalance will try to minimize segment movements.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |

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
