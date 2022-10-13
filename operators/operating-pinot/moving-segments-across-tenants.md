# Moving data from one tenant to another based on segment age

In order to optimize for low latency, we often recommend using high performance SSDs as server nodes. But if such a use case has vast amount of data, and need the high performance only when querying few recent days of data, it might become desirable to keep only the recent time ranges on SSDs, and keep the less frequently queried ones on cheaper nodes such as HDDs.

With this feature, **you can create multiple tenants, such that each tenant has servers of different specs**, and use them in the same table. In this way, you'll bring down the cost of the historical data by using a lower spec of node such as HDDs instead of SSDs for storage and compute, while trading off slight latency.\


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
    "storageType": "pinot_server",
    "serverTag": "ssd_OFFLINE"
  }, {
    "name": "hddGroup",
    "segmentSelectorType": "TIME",
    "segmentAge": "15d",
    "storageType": "PINOT_SERVER",
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
| storageType         | The type of storage. The only supported type is `pinot_server`                                                                                                                         |
| serverTag           | This property is required when `storageType` is `pinot_server`. Set the tag of the Pinot servers you wish to use for this selection criteria.                                          |

### How does data move from one tenant to another?

On adding this config, the [Segment Relocator](https://docs.pinot.apache.org/basics/components/controller#segmentrelocator) periodic task will move segments from one tenant to another, as and when the segment crosses the segment age.&#x20;

Under the hood, this job runs a rebalance. So you can achieve the same effect as a manual trigger by running a [rebalance](rebalance/rebalance-servers.md#running-a-rebalance)

