# Rebalance Tenant

Usually when we tag/untag servers to a tenant it gets tedious to rebalance each table under that tenant. This operation becomes impossible to handle if the tenant has large number of tables. The tenant rebalance operation allows us to do server rebalance on all the tables on a tenant and track the individual table rebalance progress with minimal operational overhead.

## Changes that require a rebalance

Basically all the factors which require server rebalance apply here. The only difference with this operation is it can address those changes over multiple tables with a single operation.

## How the tenant rebalance works

The tenant rebalance operation just provides a tunable orchestration of server rebalancing on multiple tables. Under the hood it leverages the existing server rebalance operation to perform the actual rebalance on each table. It provides the user a way to perform server rebalance on tables selectively in series and parallel. This is achieved using additional tuning parameters on top of usual [rebalance parameters](rebalance-servers/#rebalance-parameters).

![img.png](../../../.gitbook/assets/tenant-rebalance-flow.png)

## Control which tables to rebalance

By default, all tables that are associated with the specified tenant will be included to run rebalance operations.

A table can be associated with a tenant `{tenantName}` in multiple ways, in the table config:

1. If `tenant.server` is set to `{tenantName}`
2. If `tenant.tagOverrideConfig.realtimeConsuming` or `tenant.tagOverrideConfig.realtimeCompleted` is set to `{tenantName}_REALTIME` or `{tenantName}_OFFLINE`
3. If `instanceAssignmentConfigMap[].tagPoolConfig.tag` is set to `{tenantName}_REALTIME` or `{tenantName}_OFFLINE`&#x20;
4. If `tierConfigs[].serverTag` is set to  `{tenantName}_REALTIME` or `{tenantName}_OFFLINE`&#x20;

To explicitly select certain tables to rebalance, you can set `includeTables` and `excludeTables` . The rebalancer will first acquire the list of table of `includeTables` (default to all associated tables if not specified), then excludes all tables given in `excludeTables` . Notice that if a table given in `includeTables` is not associated with the tenant, it will not be rebalanced.

## Running a Rebalance

To run a tenant rebalance, use the following API. `POST /tenants/{tenantName}/rebalance`&#x20;

These are the available query parameters:

| Query param         | Default vale | Description                                                                                                                                                                                                                                                                                         |
| ------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| degreeOfParallelism | 1            | Number of tables to rebalance in parallel at a time                                                                                                                                                                                                                                                 |
| includeTables       | `[]`         | <p>Comma separated list of tables with type that should be included in this tenant rebalance job. Leaving blank defaults to include all tables from the tenant. Example: "table1_REALTIME, table2_REALTIME"<br><br>Notice that a table will not be included if it doesn't belong to the tenant.</p> |
| excludeTables       | `[]`         | Comma separated list of tables with type that would be excluded in this tenant rebalance job. These tables will be removed from includeTables (that said, if a table appears in both list, it will be excluded). Example: "table1\_REALTIME, table2\_REALTIME"                                      |
| parallelWhitelist   | `[]`         | Comma separated list of tables with type that are allowed to be rebalanced in parallel. Leaving blank defaults to allow any table of this tenant to run in parallel.                                                                                                                                |
| parallelBlacklist   | `[]`         | Comma separated list of tables with type that are restricted to be rebalanced in single thread. These tables will be removed from parallelWhitelist (that said, if a table appears in both list, it will be run in single thread)                                                                   |
| verboseResult       | false        | When set to true it will return all the server rebalance output for each table. When set to false it will only return the server rebalance job tracking id and status                                                                                                                               |

The request body is the same set of [parameters](rebalance-servers/#rebalance-parameters) as the server rebalance API.&#x20;

```json
{
  "diskUtilizationThreshold": 0.85,
  "externalViewCheckIntervalInMs": 1000,
  "externalViewStabilizationTimeoutInMs": 3600000,
  "forceCommitBatchStatusCheckIntervalMs": 5000,
  "forceCommitBatchStatusCheckTimeoutMs": 180000,
  "minimizeDataMovement": "ENABLE",
  "maxAttempts": 3,
  "bestEfforts": false,
  "minAvailableReplicas": 1,
  "includeConsuming": true,
  "bootstrap": false,
  "updateTargetTier": false,
  "batchSizePerServer": 100,
  "reassignInstances": true,
  "preChecks": false,
  "downtime": false,
  "lowDiskMode": false,
  "heartbeatIntervalInMs": 300000,
  "heartbeatTimeoutInMs": 3600000,
  "retryInitialDelayInMs": 300000,
  "forceCommit": false,
  "forceCommitBatchSize": 2147483647,
  "dryRun": false
}
```

Alternatively, the above parameters, if not specified via query parameters, can also be passed in the body. For example:

```json

{
  "degreeOfParallelism": 2,
  "includeTables": [],
  "excludeTables": [],
  "parallelWhitelist": [
    "airlineStats1_OFFLINE",
    "airlineStats2_OFFLINE"
  ],
  "parallelBlacklist": [
    "airlineStats1_REALTIME"
  ],
  "verboseResult": false,
  "diskUtilizationThreshold": 0.85,
  "externalViewCheckIntervalInMs": 1000,
  "externalViewStabilizationTimeoutInMs": 3600000,
  "forceCommitBatchStatusCheckIntervalMs": 5000,
  "forceCommitBatchStatusCheckTimeoutMs": 180000,
  "minimizeDataMovement": "ENABLE",
  "maxAttempts": 3,
  "bestEfforts": false,
  "minAvailableReplicas": 1,
  "includeConsuming": true,
  "bootstrap": false,
  "updateTargetTier": false,
  "batchSizePerServer": 100,
  "reassignInstances": true,
  "preChecks": false,
  "downtime": false,
  "lowDiskMode": false,
  "heartbeatIntervalInMs": 300000,
  "heartbeatTimeoutInMs": 3600000,
  "retryInitialDelayInMs": 300000,
  "forceCommit": false,
  "forceCommitBatchSize": 2147483647,
  "dryRun": true
}
```

Sample response:

```json
{
  "totalTables": 9,
  "statusSummary": {
    "NO_OP": 1,
    "DONE": 8
  },
  "aggregatedPreChecksResult": {
    "isMinimizeDataMovement": {
      "tablesPassedCount": 9,
      "tablesWarnedCount": 0,
      "tablesErroredCount": 0,
      "passedTables": {
        "meetupRsvpJson_REALTIME": "Instance assignment not allowed, no need for minimizeDataMovement",
        "meetupRsvp_REALTIME": "Instance assignment not allowed, no need for minimizeDataMovement",
        "upsertMeetupRsvp_REALTIME": "minimizeDataMovement is enabled",
        "githubEvents_REALTIME": "Instance assignment not allowed, no need for minimizeDataMovement",
        "upsertPartialMeetupRsvp_REALTIME": "minimizeDataMovement is enabled",
        "upsertJsonMeetupRsvp_REALTIME": "minimizeDataMovement is enabled",
        "dailySales_REALTIME": "Instance assignment not allowed, no need for minimizeDataMovement",
        "meetupRsvpComplexType_REALTIME": "Instance assignment not allowed, no need for minimizeDataMovement",
        "airlineStats_REALTIME": "Instance assignment not allowed, no need for minimizeDataMovement"
      },
      "warnedTables": {},
      "erroredTables": {}
    },
    "diskUtilizationDuringRebalance": {
      "tablesPassedCount": 9,
      "tablesWarnedCount": 0,
      "tablesErroredCount": 0,
      "passedTables": {
        "meetupRsvpJson_REALTIME": "Within threshold (<90%)",
        "meetupRsvp_REALTIME": "Within threshold (<90%)",
        "upsertMeetupRsvp_REALTIME": "Within threshold (<90%)",
        "githubEvents_REALTIME": "Within threshold (<90%)",
        "upsertPartialMeetupRsvp_REALTIME": "Within threshold (<90%)",
        "upsertJsonMeetupRsvp_REALTIME": "Within threshold (<90%)",
        "dailySales_REALTIME": "Within threshold (<90%)",
        "meetupRsvpComplexType_REALTIME": "Within threshold (<90%)",
        "airlineStats_REALTIME": "Within threshold (<90%)"
      },
      "warnedTables": {},
      "erroredTables": {}
    },
    ... more pre-checks
  },
  "aggregatedRebalanceSummary": {
    "serverInfo": {
      "serverSegmentChangeInfo": {
        "Server_<REDACTED>_7051": {
          "serverStatus": "UNCHANGED",
          "segmentsAdded": 23,
          "segmentsDeleted": 8,
          "segmentsUnchanged": 5,
          "totalSegmentsAfterRebalance": 28,
          "totalSegmentsBeforeRebalance": 13,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_<REDACTED>_7052": {
          "serverStatus": "REMOVED",
          "segmentsAdded": 0,
          "segmentsDeleted": 14,
          "segmentsUnchanged": 0,
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 14,
          "tagList": [
            "new_REALTIME"
          ]
        },
        "Server_<REDACTED>_7050": {
          "serverStatus": "REMOVED",
          "segmentsAdded": 0,
          "segmentsDeleted": 9,
          "segmentsUnchanged": 0,
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 9,
          "tagList": [
            "new_REALTIME"
          ]
        },
        "Server_<REDACTED>_7053": {
          "serverStatus": "UNCHANGED",
          "segmentsAdded": 8,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 21,
          "totalSegmentsAfterRebalance": 29,
          "totalSegmentsBeforeRebalance": 21,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      },
      "numServers": {
        "valueBeforeRebalance": 4,
        "expectedValueAfterRebalance": 2
      },
      "serversUnchanged": [
        "Server_<REDACTED>_7051",
        "Server_<REDACTED>_7053"
      ],
      "serversRemoved": [
        "Server_<REDACTED>_7052",
        "Server_<REDACTED>_7050"
      ],
      "serversAdded": [],
      "numServersGettingNewSegments": 2,
      "serversGettingNewSegments": [
        "Server_<REDACTED>_7051",
        "Server_<REDACTED>_7053"
      ]
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 31,
      "maxSegmentsAddedToASingleServer": 23,
      "totalSegmentsToBeDeleted": 31,
      "estimatedAverageSegmentSizeInBytes": 0,
      "totalEstimatedDataToBeMovedInBytes": -1,
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 57,
        "expectedValueAfterRebalance": 57
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 57,
        "expectedValueAfterRebalance": 57
      },
      "consumingSegmentToBeMovedSummary": {
        "numConsumingSegmentsToBeMoved": 27,
        "numServersGettingConsumingSegmentsAdded": 2,
        "consumingSegmentsToBeMovedWithMostOffsetsToCatchUp": {
          "upsertMeetupRsvp__0__0__20250620T2326Z": 402,
          "upsertJsonMeetupRsvp__0__0__20250620T2326Z": 394,
          "upsertPartialMeetupRsvp__1__0__20250620T2326Z": 371,
          "meetupRsvp__3__0__20250620T2326Z": 105,
          "meetupRsvpJson__9__0__20250620T2326Z": 88,
          "meetupRsvpComplexType__1__0__20250620T2326Z": 85,
          "dailySales__0__0__20250620T2326Z": 10,
          "githubEvents__0__4__20250620T2326Z": 0
        },
        "consumingSegmentsToBeMovedWithOldestAgeInMinutes": {
          "meetupRsvpComplexType__9__0__20250620T2326Z": 12,
          "meetupRsvpJson__1__0__20250620T2326Z": 12,
          "meetupRsvp__4__0__20250620T2326Z": 12,
          "upsertJsonMeetupRsvp__0__0__20250620T2326Z": 12,
          "githubEvents__0__4__20250620T2326Z": 12,
          "dailySales__0__0__20250620T2326Z": 12,
          "upsertPartialMeetupRsvp__1__0__20250620T2326Z": 12,
          "upsertMeetupRsvp__0__0__20250620T2326Z": 12
        },
        "serverConsumingSegmentSummary": {
          "Server_<REDACTED>_7051": {
            "totalOffsetsToCatchUpAcrossAllConsumingSegments": 2272,
            "numConsumingSegmentsToBeAdded": 19
          },
          "Server_<REDACTED>_7053": {
            "totalOffsetsToCatchUpAcrossAllConsumingSegments": 529,
            "numConsumingSegmentsToBeAdded": 8
          }
        }
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_REALTIME",
        "numSegmentsUnchanged": 26,
        "numSegmentsToDownload": 31,
        "numServerParticipants": 2
      }
    ]
  },
  "rebalanceTableResults": {
    "meetupRsvpJson_REALTIME": {
      "jobId": "f097be29-6ad2-4849-a5f7-4761cef6f450",
      "status": "DONE",
      "description": "Dry-run mode"
    },
    "meetupRsvp_REALTIME": {
      "jobId": "98281d96-3fbd-4ec8-8731-3a5879cf4017",
      "status": "DONE",
      "description": "Dry-run mode"
    },
    ...more tables
  }
}
```

## Observability

On tenant rebalance job submission it will return the job id for the tenant rebalance job to track the tenant rebalance progress along with all the individual table server rebalance job ids to track individual table rebalance progress.

### Tenant rebalance progress

To list the historical tenant rebalance jobs, use `GET /tenants/{tenantName}/rebalanceJobs`

To track the tenant rebalance progress of a specific job, use the below API `GET /tenants/rebalanceStatus/{jobId}` \
Sample response:

```json
{
  "tenantRebalanceProgressStats": {
    "startTimeMs": 1689679866904,
    "timeToFinishInSeconds": 2345,
    "completionStatusMsg": "Successfully rebalanced tenant DefaultTenant.",
    "tableStatusMap": {
      "airlineStats1_OFFLINE": "Table is already balanced",
      "airlineStats2_OFFLINE": "Table rebalance in progress",
      "airlineStats1_REALTIME": "Table is already balanced"
    },
    "totalTables": 3,
    "remainingTables": 1,
    "tableRebalanceJobIdMap": {
      "airlineStats1_OFFLINE": "2d4dc2da-1071-42b5-a20c-ac38a6d53fc4",
      "airlineStats2_OFFLINE": "2d4dc2da-497d-82a7-a20c-a113dfbbebb7",
      "airlineStats1_REALTIME": "9284f137-29c1-4c5a-a113-17b90a484403"
    }
  },
  "timeElapsedSinceStartInSeconds": 12345
}
```

### Table rebalance progress

Use the same API mentioned in [server rebalance status tracking](rebalance-servers/#checking-status)
