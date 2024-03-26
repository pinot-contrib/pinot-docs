---
description: Batch ingestion of data into Apache Pinot using dimension tables.
---

# Dimension table

Dimension tables are a special kind of offline tables from which data can be looked up via the [lookup UDF](../../../users/user-guide-query/query-syntax/lookup-udf-join.md), providing join-like functionality.

Dimension tables are replicated on all the hosts for a given tenant to allow faster lookups. When a table is marked as a dimension table, it will be replicated on all the hosts, which means that these tables must be small in size.

A dimension table cannot be part of a [hybrid table](../../concepts/components/table/#hybrid-table).

Configure dimension tables using following properties in the table configuration:

* `isDimTable`: Set to `true.`
* `segmentsConfig.segmentPushType`: Set to `REFRESH`.
* `dimensionTableConfig.disablePreload`: By default, dimension tables are preloaded to allow for fast lookups. Set to `true` to trade off speed for memory by storing only the segment reference and docID. Otherwise, the whole row is stored in the Dimension table hash map.
* `controller.dimTable.maxSize`: Determines the maximum size quota for a dimension table in a cluster. Table creation will fail if the storage quota exceeds this maximum size.
* `dimensionFieldSpecs`: To look up dimension values, dimension tables need a primary key. For details, see [`dimensionFieldSpecs`](https://docs.pinot.apache.org/configuration-reference/schema#dimensionfieldspec).

### Example dimension table configuration

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
    }.
    "dimensionTableConfig": {
      "disablePreload": true
      }
  }
}
...
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

