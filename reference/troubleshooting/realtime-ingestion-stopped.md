# Realtime Ingestion Stopped

## Symptons

When observed certain kafka partitioned stopped ingestion due to the segment commit failure.

Sample errrors:

```
2025/04/13 14:06:28.978 INFO [RealtimeSegmentDataManager_test_realtime_2__2__0__20250413T1148Z] [test_realtime_2__2__0__20250413T1148Z] Controller response {"buildTimeSec":-1,"streamPartitionMsgOffset":null,"status":"FAILED","isSplitCommitType":true} for http://pinot-controller-2.pinot-controller-headless.pinot.svc.cluster.local:9000/segmentUpload?segmentSizeBytes=242027065&reason=rowLimit&buildTimeMillis=47403&streamPartitionMsgOffset=1393724252&instance=Server_pinot-server-0.pinot-server-headless.pinot.svc.cluster.local_8098&name=test_realtime_2__2__0__20250413T1148Z&rowCount=10000000&memoryUsedBytes=519779170
2025/04/13 14:06:28.978 WARN [RealtimeSegmentDataManager_test_realtime_2__2__0__20250413T1148Z] [test_realtime_2__2__0__20250413T1148Z] Controller response was FAILED and not COMMIT_SUCCESS
2025/04/13 14:06:28.978 INFO [RealtimeSegmentDataManager_test_realtime_2__2__0__20250413T1148Z] [test_realtime_2__2__0__20250413T1148Z] Could not commit segment. Retrying after hold
```

Usually here are the steps that a partition got stopped ingestion:

1. servers tell controller to commit,
2. controller ack and ask the lead server to commit
3. lead server failed to commit due to many reason( segment build time longer than the controller lease, server oom, etc)
4. the other server got permission to build and try to commit and also failed
5. you got a partition completely stopped

## Mitigations

To mitigate, we suggest below steps to ensure your setup is scalable and stable.

1. Ensure Pinot server directly save segments to deep store, avoid controller in the critical data path. Ref link: [Decoupling Controller from the Data Path](../../operators/operating-pinot/decoupling-controller-from-the-data-path.md) .  This is the most critical fix as it will remove controller as the bottleneck for data commit:
   1. controller receive segment tarball from pinot server
   2. uncompress it
   3. extract segment metadata
   4. upload segment tarball to deep store
   5. update zookeeper segment metadata
   6. complete the protocol
2. For large realtime segment, suggest to use `DOWNLOAD` for `completionMode` so the other server replicas won't waste CPU cycles to build segments. Ref: [Realtime Table Config -> SegmentsConfig](../../configuration-reference/table.md#segments-config)
3. Limit the concurrent realtime segment build by configure Pinot servers:&#x20;

```
realtime.max.parallel.segment.builds=2
```

This will reduce each segment build time to relief the segment commit timeout situation, as well the concurrent pressure on the controller side. Ref: [Server Config](../../configuration-reference/server.md)
