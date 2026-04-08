---
description: >-
  To help understand rebalance and its output better, here are some examples
  with different scenarios with table rebalance.
---

# Examples and Scenarios

All examples below skip showing the instance assignment and segment assignment for brevity.

#### 1. Increase replication factor

Changes:

* Number of replicaGroups increased from 1 to 2 (replicaGroup based instance assignment)
* New server tagged with correct DefaultTenant tag

```json
{
  "jobId": "872d693f-07f2-48fd-9c11-98838ebaed6b",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 2
      },
      "serversAdded": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serversRemoved": [],
      "serversUnchanged": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-1_8098": {
          "serverStatus": "ADDED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 0,
          "segmentsAdded": 15,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 15,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 15,
      "maxSegmentsAddedToASingleServer": 15,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 7184757465,
      "replicationFactor": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 2
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 30
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_OFFLINE",
        "numSegmentsToDownload": 15,
        "numSegmentsUnchanged": 15,
        "numServerParticipants": 2
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

#### 2. Change instance assignment from balanced to replicaGroup based

Changes:

* Change TableConfig from balanced to replicaGroup based assignment by adding the instanceAssignmentConfigMap
  * Replication factor remains the same. Instances per replica group chosen as 1
* No change in tagged servers

```json
{
  "jobId": "35998b64-c1b2-439c-ab5b-da886874f0c2",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 1
      },
      "serversAdded": [],
      "serversRemoved": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serversUnchanged": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-1_8098": {
          "serverStatus": "REMOVED",
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 7,
          "segmentsAdded": 0,
          "segmentsDeleted": 7,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 8,
          "segmentsAdded": 7,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 8,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 7,
      "maxSegmentsAddedToASingleServer": 7,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 3352886817,
      "replicationFactor": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 1
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_OFFLINE",
        "numSegmentsToDownload": 7,
        "numSegmentsUnchanged": 8,
        "numServerParticipants": 1
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

#### 3. Increase instances per replicaGroup

Changes:

* Increase the number of instances per replica group from 1 to 2

```json
{
  "jobId": "deff09ea-85ca-4623-b34d-a37ea7eff6b7",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 2
      },
      "serversAdded": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serversRemoved": [],
      "serversUnchanged": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-1_8098": {
          "serverStatus": "ADDED",
          "totalSegmentsAfterRebalance": 7,
          "totalSegmentsBeforeRebalance": 0,
          "segmentsAdded": 7,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 8,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 7,
          "segmentsUnchanged": 8,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 7,
      "maxSegmentsAddedToASingleServer": 7,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 3352886817,
      "replicationFactor": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 1
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_OFFLINE",
        "numSegmentsToDownload": 7,
        "numSegmentsUnchanged": 8,
        "numServerParticipants": 2
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

#### 4. Move table to a different Tenant

Changes:

* Change the table's tenant tag to point to the new tenant tag
* Tag servers on new tenant with new tenant tag

```json
{
  "jobId": "1db14f0c-daf7-4e26-ae2a-fd52a5b86ac6",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 1
      },
      "serversAdded": [
        "Server_pinot-server-server-0-2_8098"
      ],
      "serversRemoved": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversUnchanged": [],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-2_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "REMOVED",
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 15,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-2_8098": {
          "serverStatus": "ADDED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 0,
          "segmentsAdded": 15,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 0,
          "tagList": [
            "NewDefaultTenant_OFFLINE",
            "NewDefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 15,
      "maxSegmentsAddedToASingleServer": 15,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 7184757465,
      "replicationFactor": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 1
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      }
    },
    "tagsInfo": [
      {
        "tagName": "NewDefaultTenant_OFFLINE",
        "numSegmentsToDownload": 15,
        "numSegmentsUnchanged": 0,
        "numServerParticipants": 1
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

#### 5. Scale Down table with balanced assignment

Changes:

* Untag servers that should no longer host the given table

```json
{
  "jobId": "6bebdafe-3e7d-445f-9b1f-f8fcd1aaab68",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 1
      },
      "serversAdded": [],
      "serversRemoved": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serversUnchanged": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-1_8098": {
          "serverStatus": "REMOVED",
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 7,
          "segmentsAdded": 0,
          "segmentsDeleted": 7,
          "segmentsUnchanged": 0,
          "tagList": [
            "NewDefaultTenant_OFFLINE",
            "NewDefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 8,
          "segmentsAdded": 7,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 8,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 7,
      "maxSegmentsAddedToASingleServer": 7,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 3352886817,
      "replicationFactor": {
        "valueBeforeRebalance": 1,
        "expectedValueAfterRebalance": 1
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_OFFLINE",
        "numSegmentsToDownload": 7,
        "numSegmentsUnchanged": 8,
        "numServerParticipants": 1
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

#### 6. minimizeDataMovement flag comparison for increasing replication factor of replicaGroup based assignment

Changes for both scenarios:

* Increase number of replicaGroups from 2 to 3, keep instances per replicaGroup the same
* Ensure enough servers are tagged with the tenant tag

For each scenario, note the server stats in terms of how the server topology is changing. This can have a large effect on how much data is moved as part of the rebalance, and checking the summary along with the pre-checks can help identify if the changes are as expected.&#x20;

Scenario 1: `minimizeDataMovement=false`

* 2 servers added, 1 removed

```json
{
  "jobId": "658761e6-b7fd-4e02-9e75-1dd0ce234648",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "preChecksResult": {
    "isMinimizeDataMovement": {
      "preCheckStatus": "WARN",
      "message": "minimizeDataMovement is enabled in table config but it's overridden with disabled"
    },
    ...
  },
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 2,
      "numServers": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 3
      },
      "serversAdded": [
        "Server_pinot-server-server-0-3_8098",
        "Server_pinot-server-server-0-2_8098"
      ],
      "serversRemoved": [
        "Server_pinot-server-server-0-1_8098"
      ],
      "serversUnchanged": [
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-3_8098",
        "Server_pinot-server-server-0-2_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-3_8098": {
          "serverStatus": "ADDED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 0,
          "segmentsAdded": 15,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-1_8098": {
          "serverStatus": "REMOVED",
          "totalSegmentsAfterRebalance": 0,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 15,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 15,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-2_8098": {
          "serverStatus": "ADDED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 0,
          "segmentsAdded": 15,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 30,
      "maxSegmentsAddedToASingleServer": 15,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 14369514930,
      "replicationFactor": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 3
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 30,
        "expectedValueAfterRebalance": 45
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_OFFLINE",
        "numSegmentsToDownload": 30,
        "numSegmentsUnchanged": 15,
        "numServerParticipants": 3
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

Scenario 2: `minimizeDataMovement=true`

* 1 server added

```json
{
  "jobId": "e0c4e81b-f680-44cd-880f-3c9469594b0b",
  "status": "DONE",
  "description": "Dry-run summary mode",
  "preChecksResult": {
    "isMinimizeDataMovement": {
      "preCheckStatus": "PASS",
      "message": "minimizeDataMovement is enabled"
    },
    ...
  },
  "rebalanceSummaryResult": {
    "serverInfo": {
      "numServersGettingNewSegments": 1,
      "numServers": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 3
      },
      "serversAdded": [
        "Server_pinot-server-server-0-2_8098"
      ],
      "serversRemoved": [],
      "serversUnchanged": [
        "Server_pinot-server-server-0-1_8098",
        "Server_pinot-server-server-0-0_8098"
      ],
      "serversGettingNewSegments": [
        "Server_pinot-server-server-0-2_8098"
      ],
      "serverSegmentChangeInfo": {
        "Server_pinot-server-server-0-1_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 15,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-0_8098": {
          "serverStatus": "UNCHANGED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 15,
          "segmentsAdded": 0,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 15,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        },
        "Server_pinot-server-server-0-2_8098": {
          "serverStatus": "ADDED",
          "totalSegmentsAfterRebalance": 15,
          "totalSegmentsBeforeRebalance": 0,
          "segmentsAdded": 15,
          "segmentsDeleted": 0,
          "segmentsUnchanged": 0,
          "tagList": [
            "DefaultTenant_OFFLINE",
            "DefaultTenant_REALTIME"
          ]
        }
      }
    },
    "segmentInfo": {
      "totalSegmentsToBeMoved": 15,
      "maxSegmentsAddedToASingleServer": 15,
      "estimatedAverageSegmentSizeInBytes": 478983831,
      "totalEstimatedDataToBeMovedInBytes": 7184757465,
      "replicationFactor": {
        "valueBeforeRebalance": 2,
        "expectedValueAfterRebalance": 3
      },
      "numSegmentsInSingleReplica": {
        "valueBeforeRebalance": 15,
        "expectedValueAfterRebalance": 15
      },
      "numSegmentsAcrossAllReplicas": {
        "valueBeforeRebalance": 30,
        "expectedValueAfterRebalance": 45
      }
    },
    "tagsInfo": [
      {
        "tagName": "DefaultTenant_OFFLINE",
        "numSegmentsToDownload": 15,
        "numSegmentsUnchanged": 30,
        "numServerParticipants": 3
      }
    ]
  },
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```

7. **Consuming segments rebalance in a REALTIME table**

Under a table with a default assignment strategy, untag one of the two servers, then rebalance.

```json
{
  "jobId": "e0c4e81b-f680-44cd-880f-3c9469594b0b",
  "status": "DONE",
  "description": "Dry-run summary mode",
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
  "instanceAssignment": {
    ...
  },
  "segmentAssignment": {
    ...
  }
}
```
