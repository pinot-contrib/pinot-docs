---
description: Dimension tables in Apache Pinot.
---

# Dimension Table

Dimension tables are a special kind of offline tables from which data can be looked up via the [lookup UDF](../../../users/user-guide-query/lookup-udf-join.md), providing join like functionality.&#x20;

Dimension tables are replicated on all the hosts for a given tenant to allow faster lookups.

To mark an offline table as a dim table, `isDimTable` should be set to true in the table config as shown below:

```
{
  "OFFLINE": {
    "tableName": "dimBaseballTeams_OFFLINE",
    "tableType": "OFFLINE",
    "segmentsConfig": {
      "schemaName": "dimBaseballTeams",
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

```
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

A dimension table cannot be part of a [hybrid table](../../components/table.md).
