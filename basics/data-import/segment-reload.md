---
description: Reload a table segment in Apache Pinot.
---

# Reload a table segment from the deep store

When Pinot writes data to segments in a table, it saves those segments to a deep store location specified in your [table configuration](../../configuration-reference/table.md), such as a storage drive or Amazon S3 bucket.

To reload segments from your deep store, use the Pinot Controller API or Pinot Admin Console.

## Use the Pinot Controller API to reload segments

To reload all segments from a table, use:

```
POST /segments/{tableName}/reload
```

To reload a specific segment from a table, use:

```
POST /segments/{tableName}/{segmentName}/reload
```

A successful API call returns the following response:

```json
{
    "status": "200"
}
```

## Use the Pinot Admin Console to reload segments

To use the Pinot Admin Console, do the following:

1. From the left navigation menu, select **Cluster Manager**.

1. Under **TENANTS**, select the **Tenant Name**.

1. From the list of tables in the tenant, select the **Table Name**.

1. Do one of the following:
    * To reload all segments, under **OPERATIONS**, click **Reload All Segments**.
    * To reload a specific segment, under **SEGMENTS**, select the **Segment Name**, and then in the new **OPERATIONS** section, select **Reload Segment**.