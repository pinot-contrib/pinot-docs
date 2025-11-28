# Using multiple directories

With this feature, you can have a single tenant, but for servers in the tenant, **you can have multiple data directories on severs, like one data path backed by SSD to keep recent data; one data path backed by HDD to keep older data,** to bring down the cost of keeping long term historical data.



### Config

**The servers** should start with those configs to enable multi-datadir. In fact, only the first one is required. The `tierBased` directory loader is aware of the multiple data directories. The `tierNames` or `dataDir` specified for each tier are optional, but still recommended to set as server config so that they are consistent across the cluster for easy management. Their values can overwritten in TableConfig as shown below.&#x20;

```
pinot.server.instance.segment.directory.loader=tierBased
pinot.server.instance.tierConfigs.tierNames=hotTier,coldTier
pinot.server.instance.tierConfigs.hotTier.dataDir=/tmp/multidir_test/hotTier
pinot.server.instance.tierConfigs.coldTier.dataDir=/tmp/multidir_test/coldTier
```

**The controllers** should enable local tier migration for segment relocator.

```
controller.segmentRelocator.enableLocalTierMigration=true
// by the way,
// controller.segment.relocator.frequencyPeriod=3600s, by default
// controller.segmentRelocator.initialDelayInSeconds=random [120, 300), by default
```

**The tables** specify which data to be put on which storage tiers, as an exmaple below

```
{
  "tableName": "myTable",
  "tableType": ...,
  "tenants": {
    "server": "base_OFFLINE",
    "broker": "base_BROKER"
  },
  "tierConfigs": [{
    "name": "hotTier",
    "segmentSelectorType": "time",
    "segmentAge": "7d",
    "storageType": "pinot_server",
    "serverTag": "base_OFFLINE"
  }, {
    "name": "coldTier",
    "segmentSelectorType": "time",
    "segmentAge": "15d",
    "storageType": "pinot_server",
    "serverTag": "base_OFFLINE",
    "tierBackendProperties": { // overwriting is not recommended, but can be done as below
       "dataDir": "/tmp/multidir_test/my_custom_colddir" // assume path exists on servers.
    }        
  }] 
}
```

As in this example  Segments older than 7 days are kept on hotTier, under path: `/tmp/multidir_test/hotTier`; and segments older than 15 days are kept on coldTier, under data path `/tmp/multidir_test/my_custom_colddir` (due to overwriting, although not recommended).

The configs are same as seen in [Using multiple tenants](moving-segments-across-tenants.md). But instead of moving data across tenants, the data is moved across data paths on the servers locally, as driven by the SegmentRelocator, the periodic task running on the controller.&#x20;
