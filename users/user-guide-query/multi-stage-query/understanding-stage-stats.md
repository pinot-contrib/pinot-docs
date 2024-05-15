---
description: Learn more about multi-stage stats and how to use them to improve your queries.
---

# Understanding multi-stage stats

Multi-stage stats are more complex but also more expressive than single-stage stats.
While in single-stage stats Apache Pinot returns a single set of statistics for the query, in multi-stage stats 
Apache Pinot returns a set of statistics for each operator of the query execution.

These stats can be seen when using Pinot controller UI by running the query and clicking on the `Show JSON format` 
button.
Then the whole JSON response will be shown and the multi-stage stats will be in a field called `stageStats`.
Different drivers may provide different ways to see the stats.

For example the following query:
```sql
SELECT playerName, teamName
FROM baseballStats_OFFLINE as playerStats
JOIN dimBaseballTeams_OFFLINE AS teams
    ON playerStats.teamID = teams.teamID
LIMIT 10
```

Returns the following `stageStats`:
```json
{
    "type": "MAILBOX_RECEIVE",
    "executionTimeMs": 222,
    "emittedRows": 10,
    "fanIn": 3,
    "rawMessages": 4,
    "deserializedBytes": 1688,
    "upstreamWaitMs": 651,
    "children": [
      {
        "type": "MAILBOX_SEND",
        "executionTimeMs": 210,
        "emittedRows": 10,
        "stage": 1,
        "parallelism": 3,
        "fanOut": 1,
        "rawMessages": 4,
        "serializedBytes": 338,
        "children": [
          {
            "type": "SORT_OR_LIMIT",
            "executionTimeMs": 585,
            "emittedRows": 10,
            "children": [
              {
                "type": "MAILBOX_RECEIVE",
                "executionTimeMs": 585,
                "emittedRows": 10,
                "fanIn": 3,
                "inMemoryMessages": 4,
                "rawMessages": 8,
                "deserializedBytes": 1775,
                "deserializationTimeMs": 1,
                "upstreamWaitMs": 1480,
                "children": [
                  {
                    "type": "MAILBOX_SEND",
                    "executionTimeMs": 397,
                    "emittedRows": 30,
                    "stage": 2,
                    "parallelism": 3,
                    "fanOut": 3,
                    "inMemoryMessages": 4,
                    "rawMessages": 8,
                    "serializedBytes": 1108,
                    "serializationTimeMs": 2,
                    "children": [
                      {
                        "type": "SORT_OR_LIMIT",
                        "executionTimeMs": 379,
                        "emittedRows": 30,
                        "children": [
                          {
                            "type": "TRANSFORM",
                            "executionTimeMs": 377,
                            "emittedRows": 5092,
                            "children": [
                              {
                                "type": "HASH_JOIN",
                                "executionTimeMs": 376,
                                "emittedRows": 5092,
                                "timeBuildingHashTableMs": 167,
                                "children": [
                                  {
                                    "type": "MAILBOX_RECEIVE",
                                    "executionTimeMs": 206,
                                    "emittedRows": 10000,
                                    "fanIn": 1,
                                    "inMemoryMessages": 4,
                                    "rawMessages": 21,
                                    "deserializedBytes": 649374,
                                    "deserializationTimeMs": 3,
                                    "downstreamWaitMs": 5,
                                    "upstreamWaitMs": 390,
                                    "children": [
                                      {
                                        "type": "MAILBOX_SEND",
                                        "executionTimeMs": 94,
                                        "emittedRows": 97889,
                                        "stage": 3,
                                        "parallelism": 1,
                                        "fanOut": 3,
                                        "inMemoryMessages": 4,
                                        "rawMessages": 20,
                                        "serializedBytes": 649076,
                                        "serializationTimeMs": 17,
                                        "children": [
                                          {
                                            "type": "LEAF",
                                            "table": "baseballStats_OFFLINE",
                                            "executionTimeMs": 75,
                                            "emittedRows": 97889,
                                            "numDocsScanned": 97889,
                                            "numEntriesScannedPostFilter": 195778,
                                            "numSegmentsQueried": 1,
                                            "numSegmentsProcessed": 1,
                                            "numSegmentsMatched": 1,
                                            "totalDocs": 97889,
                                            "threadCpuTimeNs": 19888000
                                          }
                                        ]
                                      }
                                    ]
                                  },
                                  {
                                    "type": "MAILBOX_RECEIVE",
                                    "executionTimeMs": 163,
                                    "emittedRows": 51,
                                    "fanIn": 1,
                                    "inMemoryMessages": 2,
                                    "rawMessages": 4,
                                    "deserializedBytes": 2330,
                                    "downstreamWaitMs": 14,
                                    "upstreamWaitMs": 162,
                                    "children": [
                                      {
                                        "type": "MAILBOX_SEND",
                                        "executionTimeMs": 17,
                                        "emittedRows": 51,
                                        "stage": 4,
                                        "parallelism": 1,
                                        "fanOut": 3,
                                        "inMemoryMessages": 1,
                                        "rawMessages": 4,
                                        "serializedBytes": 2092,
                                        "children": [
                                          {
                                            "type": "LEAF",
                                            "table": "dimBaseballTeams_OFFLINE",
                                            "executionTimeMs": 62,
                                            "emittedRows": 51,
                                            "numDocsScanned": 51,
                                            "numEntriesScannedPostFilter": 102,
                                            "numSegmentsQueried": 1,
                                            "numSegmentsProcessed": 1,
                                            "numSegmentsMatched": 1,
                                            "totalDocs": 51,
                                            "threadCpuTimeNs": 1919000,
                                            "systemActivitiesCpuTimeNs": 4677167
                                          }
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
```

Each node in the tree represents an operation that is executed and the tree structure form is similar (but not equal)
to the logical plan of the query that can be obtained with the `EXPLAIN PLAN` command.

As you can see, each operator has a type and the stats carried on the node depend on that type.
You can learn more about each operator types and their stats in the [Operator Types](./operator-types/README.md) section.