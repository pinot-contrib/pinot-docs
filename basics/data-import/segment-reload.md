---
description: Reload a table segment in Apache Pinot.
---

# Reload a table segment from the deep store

Once data is pushed or pulled into Apache Pinot and written into segments in a table, those segments will eventually be stored away in a deep store, using a location you designate, such as on a storage drive or in Amazon S3. That storage is defined in your [table configuration](../../configuration-reference/table.md).

To reload segments from your deep store, you can use calls from the Pinot Controller API or do this from the Pinot Admin Console.

## Use the Pinot Controller API to reload segments

To reload all segments from a table, use:

```
POST /segments/{tableName}/reload
```

To reload a specific segment from a table, use:

```
POST /segments/{tableName}/{segmentName}/reload
```

Either API call will return a JSON response like this one for a successful operation:

```json
{
    "status": "200"
}
```

## Use the Pinot Admin Console to reload segments

To use the Pinot Admin Console, do the following:

1. From the left sidebar menu, select the **Cluster Manager**.

1. From the **TENANTS** section, select the **Tenant Name**.

1. From the list of tables in the tenant, select the **Table Name**.

1. Do one of the following:
    * To reload all segments, from the **OPERATIONS** section, click **Reload All Segments**.
    or
    * To reload a specific segment, from the **SEGMENTS** section, select the **Segment Name**, then from the new **OPERATIONS** section, select **Reload Segment**.