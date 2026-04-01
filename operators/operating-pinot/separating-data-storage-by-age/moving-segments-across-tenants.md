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

<table>
  <thead>
    <tr>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>name</td>
      <td>Name of the server group. Every group in the list must have a unique name</td>
    </tr>
    <tr>
      <td>segmentSelectorType</td>
      <td>The strategy used for selecting segments. The only supported strategy as of now is `time`, which will pick segments based on segment age.</td>
    </tr>
    <tr>
      <td>segmentAge</td>
      <td>This property is required when `segmentSelectorType` is `time`. Set a period string, eg. 15d, 24h, 60m. Segments which are older than the age will be moved to the the specific tenant</td>
    </tr>
    <tr>
      <td>storageType</td>
      <td>The type of storage. The only supported type is `pinot_server`</td>
    </tr>
    <tr>
      <td>serverTag</td>
      <td>This property is required when `storageType` is `pinot_server`. Set the tag of the Pinot servers you want to use for this selection criteria.</td>
    </tr>
  </tbody>
</table>

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

On adding this config, the [Segment Relocator](../../../basics/components/cluster/controller.md#segmentrelocator) periodic task will move segments from one tenant to another, as and when the segment crosses the segment age.

Under the hood, this job runs a rebalance. So you can achieve the same effect as a manual trigger by running a [rebalance](../rebalance/rebalance-servers/#running-a-rebalance)
