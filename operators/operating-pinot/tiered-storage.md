# Tiered Storage

Tiered storage allows you to split your server storage into multiple tiers. All the tiers can use different filesystem to hold the data. Tiered storage can be used to optimise the cost to latency tradeoff in production Pinot systems.

Some example scenarios in which tiered storage can be used -&#x20;

* Tables with very long retention (more than 2 years) but most frequently queries are performed on the recent data.
* Reduce storage cost for older data while tolerating slightly higher latencies\
  \
  In order to optimize for low latency, we often recommend using high performance SSDs. But if such a use case has 2 years of data, and need the high performance only when querying 1 month of data, it might become desirable to keep only the recent time ranges on SSDs, and keep the less frequently queried ones on cheaper nodes such as HDDs or a DFS such as S3.

The data age based tiers is just one of the examples. The logic to split data into tiers may change depending on the use case.

### Tier Config

You can configured tiered storage by setting the `tieredConfigs` key in your table config json.

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
    "name": "tierA",
    "segmentSelectorType": "time",
    "segmentAge": "7d",
    "storageType": "pinot_server",
    "serverTag": "tier_a_OFFLINE"
  }, {
    "name": "tierB",
    "segmentSelectorType": "TIME",
    "segmentAge": "15d",
    "storageType": "PINOT_SERVER",
    "serverTag": "tier_b_OFFLINE"
  }] 
}
```

In this example, the table uses servers tagged with `base_OFFLINE`. We have created two tiers of Pinot servers, tagged with `tier_a_OFFLINE` and `tier_b_OFFLINE`. Segments older than 7 days will move from `base_OFFLINE` to `tier_a_OFFLINE`, and segments older than 15 days will move to `tier_b_OFFLINE`.

![](../../.gitbook/assets/screen-shot-2020-08-24-at-9.17.43-am.png)

Following properties are supported under `tierConfigs` -&#x20;

|                     |                                                                                                                                                                                                                      |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                | Name of the tier. Every tier in the tierConfigs list must have a unique name                                                                                                                                         |
| segmentSelectorType | The strategy used for selecting segments for tiers. The only supported strategy as of now is `time`, which will pick segments based on segment age. In future, we expect to have strategies like `column_value`, etc |
| segmentAge          | This property is required when `segmentSelectorType` is `time`. Set a period string, eg. 15d, 24h, 60m. Segments which are older than the age will be moved to the the specific tier                                 |
| storageType         | The type of storage. The only supported type is `pinot_server`, which will use Pinot servers as storage for the tier. In future, we expect to have some deep store modes here                                        |
| serverTag           | This property is required when `storageType` is `pinot_server`. Set the tag of the Pinot servers you wish to use for this tier.                                                                                      |

### How does data move from one tenant to another?

On adding tier config, a periodic task on the pinot-controller called "SegmentRelocator" will move segments from one tenant to another, as and when the segment crosses the segment age.&#x20;

This periodic task runs every hour by default. You can configure this frequency by setting the config with any period string (60s, 2h, 5d)

```
controller.segment.relocator.frequencyPeriod=10m
```

This job can also be triggered manually

```
curl -X GET "https://localhost:9000/periodictask/run?
    taskname=SegmentRelocator&tableName=myTable&type=OFFLINE" 
    -H "accept: application/json"
```

Under the hood, this job runs a rebalance. So you can achieve the same effect as a manual trigger by running a [rebalance](rebalance/rebalance-servers.md#running-a-rebalance)

