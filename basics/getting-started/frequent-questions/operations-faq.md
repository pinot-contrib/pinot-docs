# Operations FAQ

## Memory

### How much heap should I allocate for my Pinot instances?

Typically, Pinot components try to use as much off-heap (MMAP/DirectMemory) wherever possible. For example, Pinot servers load segments in memory-mapped files in MMAP mode (recommended), or direct memory in HEAP mode. Heap memory is used mostly for query execution and storing some metadata. We have seen production deployments with high throughput and low-latency work well with just 16 GB of heap for Pinot servers and brokers. Pinot controller may also cache some metadata (table configs etc) in heap, so if there are just a few tables in the Pinot cluster, a few GB of heap should suffice.

## DR

### Does Pinot provide any backup/restore mechanism?

Pinot relies on deep-storage for storing backup copy of segments (offline as well as real-time). It relies on Zookeeper to store metadata (table configs, schema, cluster state, etc). It does not explicitly provide tools to take backups or restore these data, but relies on the deep-storage (ADLS/S3/GCP/etc), and ZK to persist these data/metadata.

## Alter Table

### Can I change a column name in my table, without losing data?

Changing a column name or data type is considered backward incompatible change. While Pinot does support schema evolution for backward compatible changes, it does not support backward incompatible changes like changing name/data-type of a column.

### How to change number of replicas of a table?

You can change the number of replicas by updating the table config's [segmentsConfig](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1) section. Make sure you have at least as many servers as the replication.

For offline tables, update [replication](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1)

```
{ 
    "tableName": "pinotTable", 
    "tableType": "OFFLINE", 
    "segmentsConfig": {
      "replication": "3", 
      ... 
    }
    ..
```

For real-time tables, update [replicasPerPartition](https://docs.pinot.apache.org/basics/components/table#segmentsconfig)

```
{ 
    "tableName": "pinotTable", 
    "tableType": "REALTIME", 
    "segmentsConfig": {
      "replicasPerPartition": "3", 
      ... 
    }
    ..
```

After changing the replication, run a [table rebalance](./#how-to-run-a-rebalance-on-a-table).

## Rebalance

### How to run a rebalance on a table?

Refer to [Rebalance](../../../operators/operating-pinot/rebalance/).

### Why does my real-time table not use the new nodes I added to the cluster?

Likely explanation: num partitions \* num replicas < num servers

In real-time tables, **segments of the same partition always continue to remain on the same node**. This sticky assignment is needed for replica groups and is critical if using upserts. For instance, if you have 3 partitions, 1 replica, and 4 nodes, only ¾ nodes will be used, and all of p0 segments will be on 1 node, p1 on 1 node, and p2 on 1 node. One server will be unused, and will remain unused through rebalances.

There’s nothing we can do about CONSUMING segments, they will continue to use only 3 nodes if you have 3 partitions. But we can rebalance such that completed segments use all nodes. If you want to **force the completed segments of the table to use the new server**, use this config

```
"instanceAssignmentConfigMap": {
      "COMPLETED": {
        "tagPoolConfig": {
          "tag": "DefaultTenant_OFFLINE"
        },
        "replicaGroupPartitionConfig": {
        }
      }
    },
```

## Segments

### How to control number of segments generated?

The number of segments generated depends on the number of input files. If you provide only 1 input file, you will get 1 segment. If you break up the input file into multiple files, you will get as many segments as the input files.

### What are the common reasons my segment is in a BAD state ?

This typically happens when the server is unable to load the segment. Possible causes: Out-Of-Memory, no-disk space, unable to download segment from deep-store, and similar other errors. Please check server logs for more information.

### How to reset a segment when it runs into a BAD state?

Use the segment reset controller REST API to reset the segment:

```
curl -X POST "{host}/segments/{tableNameWithType}/{segmentName}/reset"
```

### How do I pause real-time ingestion?

Refer to [Pause Stream Ingestion](https://docs.pinot.apache.org/basics/data-import/pinot-stream-ingestion#pause-stream-ingestion).

### What's the difference between Reset, Refresh, and Reload?

RESET: this gets a segment in ERROR state back to ONLINE or CONSUMING state. Behind the scenes, Pinot controller takes the segment to OFFLINE state, waits for External View to stabilize, and then moves it back to ONLINE/CONSUMING state, thus effectively resetting segments or consumers in error states.

REFRESH: this replaces the segment with a new one, with the same name but often different data. Under the hood, Pinot controller sets new segment metadata in Zookeeper, and notifies brokers and servers to check their local states about this segment and update accordingly. Servers also download the new segment to replace the old one, when both have different checksums. There is no separate rest API for refreshing, and it is done as part of SegmentUpload API today.

RELOAD: this reloads the segment, often to generate a new index as updated in table config. Underlying, Pinot server gets the new table config from Zookeeper, and uses it to guide the segment reloading. In fact, the last step of REFRESH as explained above is to load the segment into memory to serve queries. There is a dedicated rest API for reloading. By default, it doesn't download segment. But option is provided to force server to download segment to replace the local one cleanly.

In addition, RESET brings the segment OFFLINE temporarily; while REFRESH and RELOAD swap the segment on server atomically without bringing down the segment or affecting ongoing queries.

## Tenants

### How can I make brokers/servers join the cluster without the DefaultTenant tag?

Set this property in your controller.conf file

```
cluster.tenant.isolation.enable=false
```

Now your brokers and servers should join the cluster as `broker_untagged` and `server_untagged` . You can then directly use the `POST /tenants` API to create the desired tenants

```
curl -X POST "http://localhost:9000/tenants" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{\"tenantRole\":\"BROKER\",\"tenantName\":\"foo\",\"numberOfInstances\":1}"
```

## Minion

### How do I tune minion task timeout and parallelism on each worker?

There are two task configs but set as part of cluster configs like below. One controls task's overall timeout (1hr by default) and one for how many tasks to run on a single minion worker (1 by default). The \<taskType> is the task to tune, e.g. MergeRollupTask or RealtimeToOfflineSegmentsTask etc.

```
Using "POST /cluster/configs" API on CLUSTER tab in Swagger, with this payload
{
	"<taskType>.timeoutMs": "600000",
	"<taskType>.numConcurrentTasksPerInstance": "4"
}
```

### How to I manually run a Periodic Task?

Refer to [Running a Periodic Task Manually](../../components/cluster/controller.md#running-the-periodic-task-manually)

## Tuning and Optimizations

### Do replica groups work for real-time? <a href="#docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3" id="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3"></a>

Yes, replica groups work for real-time. There's 2 parts to enabling replica groups:

1. Replica groups segment assignment
2. Replica group query routing

**Replica group segment assignment**

Replica group segment assignment is achieved in real-time, if number of servers is a multiple of number of replicas. The partitions get uniformly sprayed across the servers, creating replica groups.\
\
For example, consider we have 6 partitions, 2 replicas, and 4 servers.

|    | r1 | r2 |
| -- | -- | -- |
| p1 | S0 | S1 |
| p2 | S2 | S3 |
| p3 | S0 | S1 |
| p4 | S2 | S3 |
| p5 | S0 | S1 |
| p6 | S2 | S3 |

As you can see, the set (S0, S2) contains r1 of every partition, and (s1, S3) contains r2 of every partition. The query will only be routed to one of the sets, and not span every server.\
If you are are adding/removing servers from an existing table setup, you have to run [rebalance](./#how-to-run-a-rebalance-on-a-table) for segment assignment changes to take effect.

**Replica group query routing**

Once replica group segment assignment is in effect, the query routing can take advantage of it. For replica group based query routing, set the following in the table config's [routing](https://docs.pinot.apache.org/basics/components/table#routing) section, and then restart brokers

```
{
    "tableName": "pinotTable", 
    "tableType": "REALTIME",
    "routing": {
        "instanceSelectorType": "replicaGroup"
    }
    ..
}
```

### Overwrite index configs at tier level

When using [tiered storage](https://docs.pinot.apache.org/operators/operating-pinot/separating-data-storage-by-age), user may want to have different encoding and indexing types for a column in different tiers to balance query latency and cost saving more flexibly. For example, segments in the hot tier can use dict-encoding, bloom filter and all kinds of relevant index types for very fast query execution. But for segments in the cold tier, where cost saving matters more than low query latency, one may want to use raw values and bloom filters only.

The following two examples show how to overwrite encoding type and index configs for tiers. Similar changes are also demonstrated in the [MultiDirQuickStart example](https://github.com/apache/pinot/blob/master/pinot-tools/src/main/java/org/apache/pinot/tools/MultiDirQuickstart.java).&#x20;

1. Overwriting single-column index configs using `fieldConfigList`. All top level fields in [FieldConfig class](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/config/table/FieldConfig.java#L88) can be overwritten, and fields not overwritten are kept intact.

```
{
  ...
  "fieldConfigList": [    
    {
      "name": "ArrTimeBlk",
      "encodingType": "DICTIONARY",
      "indexes": {
        "inverted": {
          "enabled": "true"
        }
      },
      "tierOverwrites": {
        "hotTier": {
          "encodingType": "DICTIONARY",
          "indexes": { // change index types for this tier
            "bloom": {
              "enabled": "true"
            }
          }
        },
        "coldTier": {
          "encodingType": "RAW", // change encoding type for this tier
          "indexes": { } // remove all indexes
        }
      }
    }
  ],
```

2. Overwriting StarTree index configs using `tableIndexConfig`. The StarTreeIndexConfigs is overwritten as a whole. In fact, all top level fields defined in [IndexingConfig class](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/config/table/IndexingConfig.java#L29) can be overwritten, so single-column index configs defined in `tableIndexConfig` can also be overwritten but it's less clear than using `fieldConfigList`. &#x20;

```
  "tableIndexConfig": {
    "starTreeIndexConfigs": [
      {
        "dimensionsSplitOrder": [
          "AirlineID",
          "Origin",
          "Dest"
        ],
        "skipStarNodeCreationForDimensions": [],
        "functionColumnPairs": [
          "COUNT__*",
          "MAX__ArrDelay"
        ],
        "maxLeafRecords": 10
      }
    ],
...
    "tierOverwrites": {
      "hotTier": {
        "starTreeIndexConfigs": [ // create different STrTree index on this tier
          {
            "dimensionsSplitOrder": [
              "Carrier",
              "CancellationCode",
              "Origin",
              "Dest"
            ],
            "skipStarNodeCreationForDimensions": [],
            "functionColumnPairs": [
              "MAX__CarrierDelay",
              "AVG__CarrierDelay"
            ],
            "maxLeafRecords": 10
          }
        ]
      },
      "coldTier": {
        "starTreeIndexConfigs": [] // removes ST index for this tier
      }
    }
  },
 ...
```

## Credential

### How do I update credentials for real-time upstream without downtime?

1. [Pause the stream ingestion](https://docs.pinot.apache.org/basics/data-import/pinot-stream-ingestion#pause-stream-ingestion)
2. Wait for the pause status to success
3. Update the credential in the table config
4. Resume the consumption

