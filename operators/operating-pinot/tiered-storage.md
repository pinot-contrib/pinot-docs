# Tiered Storage

Tiered storage allows you to split your server storage into tiers. 

Consider use cases which have Pinot tables with **very large retention,** but typically **only query the most recent segments**. Or use cases where very **low latency is expected when querying the recent data**, and are **tolerant of slightly higher latencies when querying older data**. In order to optimize for low latency, we often recommend using high performance SSDs. But if such a use case has 2 years of data, and need the high performance only when querying 1 month of data, it might become desirable to keep only the recent time ranges on SSDs, and keep the less frequently queried ones on cheaper and modest nodes \(say HDDs\).

This time based data tiers is just 1 example. The logic to split data into tiers may change depending on the use case. Similarly, using SSDs and HDDs is just 1 example of storage tiers. Again, depending on the usecase, you may want to use a different configuration of servers, or even move it to a deep store \(say S3\).

To configure tiered storage, set the `tieredConfigs` in your table config:

```text
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

where,

|  |  |
| :--- | :--- |
| name | Name of the tier. Every tier in the tierConfigs list must have a unique name |
| segmentSelectorType | The strategy used for selecting segments for tiers. The only supported strategy as of now is "time", which will pick segments based on segment age. In future, we expect to have strategies like "column\_value", etc |
| segmentAge | This property is required when `segmentSelectorType` is "time". Set a period string, eg. 15d, 24h, 60m |
| storageType | The type of storage. The only supported type as of now is "pinot\_server", which will use Pinot servers as storage for the tier. In future, we expect to have some deep store modes here  |
| serverTag | This property is required when `storageType` is "pinot\_server". Set the tag of the Pinot servers you wish to use for this tier. |

In the example above, the table uses servers tagged with "base\_OFFLINE". We have created 2 tiers of Pinot servers, tagged with "tier\_a\_OFFLINE" and "tier\_b\_OFFLINE". Segments older than 7 days will move from "base\_OFFLINE" to "tier\_a\_OFFLINE", and segments older than 15 days will move to "tier\_b\_OFFLINE".

