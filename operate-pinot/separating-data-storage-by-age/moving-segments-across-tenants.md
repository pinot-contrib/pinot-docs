# Using multiple tenants

With this feature, **you can create multiple tenants, such that each tenant has servers of different specs**, and use them in the same table. In this way, you'll bring down the cost of the historical data by using a lower spec of node such as HDDs instead of SSDs for storage and compute, while trading off slight latency.\\

### Config

You can configured separate tenants for the table by setting this config in your table config json.

#### Example

```
{
  "tableName": "myTable",
  "tableType": ...,
  "tenants": {
    "server": "base_OFFLINE",
    "broker": "base_BROKER"
  },
  "tierConfigs": [{
    "name": "ssdGroup",
    "segmentSelectorType": "time",
    "segmentAge": "7d",
    "segmentAgeField": "endTime",
    "storageType": "pinot_server",
    "serverTag": "ssd_OFFLINE"
  }, {
    "name": "hddGroup",
    "segmentSelectorType": "time",
    "segmentAge": "15d",
    "storageType": "pinot_server",
    "serverTag": "hdd_OFFLINE"
  }] 
}
```

In this example, the table uses servers tagged with `base_OFFLINE`. We have created two tenants of Pinot servers, tagged with `ssd_OFFLINE` and `hdd_OFFLINE`. Segments older than 7 days will move from `base_OFFLINE` to `ssd_OFFLINE`, and segments older than 15 days will move to `hdd_OFFLINE`.

|                     |                                                                                                                                                                                        |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                | Name of the server group. Every group in the list must have a unique name                                                                                                              |
| segmentSelectorType | The strategy used for selecting segments. The only supported strategy as of now is `time`, which will pick segments based on segment age.                                              |
| segmentAge          | This property is required when `segmentSelectorType` is `time`. Set a period string, eg. 15d, 24h, 60m. Segments which are older than the age will be moved to the the specific tenant |
| segmentAgeField     | Optional timestamp used to calculate age for the `time` selector: `endTime` (the default and the segment's newest data), `startTime` (oldest data), or `creationTime` (when the segment was built). Values are case-insensitive; `end_time`, `start_time`, and `creation_time` are also accepted. |
| storageType         | The type of storage. The only supported type is `pinot_server`                                                                                                                         |
| serverTag           | This property is required when `storageType` is `pinot_server`. Set the tag of the Pinot servers you want to use for this selection criteria.                                          |

Use `creationTime` when loading historical batch data but you want lifecycle transitions to begin when Pinot builds the segment. With the default `endTime`, a newly built segment whose data timestamps are old can qualify for an age-based tier immediately. Segments created before creation-time metadata was recorded are treated as already aged. Use `startTime` when the transition should be based on the oldest data in each segment.

### Selecting All Segments with a Wildcard

Tables without a time column cannot use time-based segment selection because it relies on segment start/end timestamps. For these tables, use `FixedTierSegmentSelector` with the special `"*"` wildcard in `segmentList` to move all completed segments to a tier:

```json
{
  "tierName": "coldTier",
  "segmentSelectorType": "fixed",
  "segmentList": ["*"],
  "storageType": "pinot_server",
  "serverTag": "DefaultTenant_OFFLINE_cold"
}
```

When `segmentList` contains `"*"`, the selector treats all completed (non-consuming) segments as matching, regardless of name. This is particularly useful for dimension tables or event tables that lack a dedicated time column.

### How does data move from one tenant to another?

On adding this config, the [Segment Relocator](../../reference/configuration-reference/controller.md#segmentrelocator) periodic task will move segments from one tenant to another, as and when the segment crosses the segment age.

Under the hood, this job runs a rebalance. So you can achieve the same effect as a manual trigger by running a [rebalance](../rebalance/rebalance-servers/#running-a-rebalance)
