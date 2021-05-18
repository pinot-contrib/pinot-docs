# Operations FAQ

## Operations

## How much heap should I allocate for my Pinot instances?

Typically, Pinot components try to use as much off-heap \(MMAP/DirectMemory\) where ever possible. For example, Pinot servers load segments in memory-mapped files in MMAP mode \(recommended\), or direct memory in HEAP  mode. Heap memory is used mostly for query execution and storing some metadata. We have seen production deployments with high throughput and low-latency work well with just 16 GB of heap for Pinot servers and brokers. Pinot controller may also cache some metadata \(table configs etc\) in heap, so if there are just a few tables in the Pinot cluster, a few GB of heap should suffice.

### Can I change a column name in my table, without losing data?

### How to change number of replicas of a table?

You can change the number of replicas by updating the table config's [segmentsConfig](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1) section. Make sure you have at least as many servers as the replication.

For OFFLINE table, update [replication](https://docs.pinot.apache.org/basics/components/table#segmentsconfig-1)

```text
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

```text
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

### How to run a rebalance on a table?

Refer to [Rebalance](../../../operators/operating-pinot/rebalance/).

### How to control number of segments generated?

The number of segments generated depends on the number of input files. If you provide only 1 input file, you will get 1 segment. If you break up the input file into multiple files, you will get as many segments as the input files. 

### What are the common reasons my segment is in a BAD state ?

This typically happens when the server is unable to load the segment. Possible causes: Out-Of-Memory, no-disk space, unable to download segment from deep-store, and similar other errors. Please check server logs for more information. 

## Tuning and Optimizations

### Do replica groups work for real-time? <a id="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3"></a>

Yes, replica groups work for realtime. There's 2 parts to enabling replica groups:

1. Replica groups segment assignment
2. Replica group query routing

**Replica group segment assignment**

Replica group segment assignment is achieved in realtime, if number of servers is a multiple of number of replicas. The partitions get uniformly sprayed across the servers, creating replica groups.  
  
For example, consider we have 6 partitions, 2 replicas, and 4 servers.

|  | r1 | r2 |
| :--- | :--- | :--- |
| p1 | S0 | S1 |
| p2 | S2 | S3 |
| p3 | S0 | S1 |
| p4 | S2 | S3 |
| p5 | S0 | S1 |
| p6 | S2 | S3 |

As you can see, the set \(S0, S2\) contains r1 of every partition, and \(s1, S3\) contains r2 of every partition. The query will only be routed to one of the sets, and not span every server.  
If you are are adding/removing servers from an existing table setup, you have to run [rebalance](./#how-to-run-a-rebalance-on-a-table) for segment assignment changes to take effect.

**Replica group query routing**

Once replica group segment assignment is in effect, the query routing can take advantage of it. For replica group based query routing, set the following in the table config's [routing](https://docs.pinot.apache.org/basics/components/table#routing) section, and then restart brokers

```text
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

