# Operations FAQ

## Operations

### How much heap should I allocate for my Pinot instances?

Typically, Pinot components try to use as much off-heap (MMAP/DirectMemory) where ever possible. For example, Pinot servers load segments in memory-mapped files in MMAP mode (recommended), or direct memory in HEAP  mode. Heap memory is used mostly for query execution and storing some metadata. We have seen production deployments with high throughput and low-latency work well with just 16 GB of heap for Pinot servers and brokers. Pinot controller may also cache some metadata (table configs etc) in heap, so if there are just a few tables in the Pinot cluster, a few GB of heap should suffice.

### Does Pinot provide any backup/restore mechanism?

Pinot relies on deep-storage for storing backup copy of segments (offline as well as realtime). It relies on Zookeeper to store metadata (table configs, schema, cluster state, etc). It does not explicitly provide tools to take backups or restore these data, but relies on the deep-storage (ADLS/S3/GCP/etc), and ZK to persist these data/metadata.&#x20;

### Can I change a column name in my table, without losing data?

Changing a column name or data type is considered backward incompatible change. While Pinot does support schema evolution for backward compatible changes, it does not support backward incompatible changes like changing name/data-type of a column.

### How to change number of replicas of a table?

You can change the number of replicas by updating the table config's [segmentsConfig](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1) section. Make sure you have at least as many servers as the replication.

For OFFLINE table, update [replication](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1)

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

For REALTIME table update [replicasPerPartition](https://docs.pinot.apache.org/basics/components/table#segmentsconfig)

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

After changing the replication, run a [table rebalance](./#how-to-run-a-rebalance-on-a-table).&#x20;

### How to run a rebalance on a table?

Refer to [Rebalance](../../../operators/operating-pinot/rebalance/).

### How to control number of segments generated?

The number of segments generated depends on the number of input files. If you provide only 1 input file, you will get 1 segment. If you break up the input file into multiple files, you will get as many segments as the input files.&#x20;

### What are the common reasons my segment is in a BAD state ?

This typically happens when the server is unable to load the segment. Possible causes: Out-Of-Memory, no-disk space, unable to download segment from deep-store, and similar other errors. Please check server logs for more information.&#x20;

### How to reset a segment when it runs into a BAD state?

Use the segment reset controller REST API to reset the segment:

```
curl -X POST "{host}/segments/{tableNameWithType}/{segmentName}/reset"
```

### What's the difference to Reset, Refresh, or Reload a segment?

RESET: this gets a segment in ERROR state back to ONLINE or CONSUMING state. Behind the scenes, Pinot controller takes the segment to OFFLINE state, waits for External View to stabilize, and then moves it back to ONLINE/CONSUMING state, thus effectively resetting segments or consumers in error states.&#x20;

REFRESH: this replaces the segment with a new one, with the same name but often different data. Under the hood, Pinot controller sets new segment metadata in Zookeeper, and notifies brokers and servers to check their local states about this segment and update accordingly. Servers also download the new segment to replace the old one, when both have different checksums. There is no separate rest API for refreshing, and it is done as part of SegmentUpload API today.

RELOAD: this reloads the segment, often to generate a new index as updated in table config. Underlying, Pinot server gets the new table config from Zookeeper, and uses it to guide the segment reloading. In fact, the last step of REFRESH as explained above is to load the segment into memory to serve queries. There is a dedicated rest API for reloading. By default, it doesn't download segment. But option is provided to force server to download segment to replace the local one cleanly.

In addition, RESET brings the segment OFFLINE temporarily; while REFRESH and RELOAD swap the segment on server atomically without bringing down the segment or affecting ongoing queries.

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

## Tuning and Optimizations

### Do replica groups work for real-time? <a href="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3" id="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3"></a>

Yes, replica groups work for realtime. There's 2 parts to enabling replica groups:

1. Replica groups segment assignment
2. Replica group query routing

**Replica group segment assignment**

Replica group segment assignment is achieved in realtime, if number of servers is a multiple of number of replicas. The partitions get uniformly sprayed across the servers, creating replica groups.\
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

##
