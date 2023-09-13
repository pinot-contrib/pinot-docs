---
description: Batch ingestion of data into Apache Pinot using dimension tables.
---

# Dimension table

Dimension tables are a special kind of offline tables from which data can be looked up via the [lookup UDF](../../../users/user-guide-query/lookup-udf-join.md), providing join-like functionality.

Dimension tables are replicated on all the hosts for a given tenant to allow faster lookups.

To mark an offline table as a dimension table, `isDimTable` should be set to _true_ and `segmentsConfig.segementPushType` should be set to _REFRESH_ in the table config, like this:

```json
{
  "OFFLINE": {
    "tableName": "dimBaseballTeams_OFFLINE",
    "tableType": "OFFLINE",
    "segmentsConfig": {
      "schemaName": "dimBaseballTeams",
      "segmentPushType": "REFRESH"
    },
    "metadata": {},
    "quota": {
      "storage": "200M"
    },
    "isDimTable": true
  }
}
```

As dimension tables are used to perform lookups of dimension values, they are required to have a primary key (can be a composite key).

```json
{
  "dimensionFieldSpecs": [
    {
      "dataType": "STRING",
      "name": "teamID"
    },
    {
      "dataType": "STRING",
      "name": "teamName"
    }
  ],
  "schemaName": "dimBaseballTeams",
  "primaryKeyColumns": ["teamID"]
}
```

When a table is marked as a dimension table, it will be replicated on all the hosts, which means that these tables must be small in size.

The maximum size quota for a dimension table in a cluster is controlled by the `controller.dimTable.maxSize` controller property. Table creation will fail if the storage quota exceeds this maximum size.

A dimension table cannot be part of a [hybrid table](../../components/table/#hybrid-table).
