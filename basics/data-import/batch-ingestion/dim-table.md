---
description: Dimension tables in Apache Pinot.
---

# Batch Ingestion for Dimension Table 

Dimension tables are a spcial kind of offline tables from which data canbe looked up via the lookup UDF, providing a join like functionality. These dimension tables are replicated on all the hosts on a given tenant to allow faster lookups.

To mark an offline table as a dim table the configuration `isDimTable` should be set to true in the table config as shown below

```text

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

As dimension table are used ot perform lookups of dimension values, they are required to have a primary key (can be a composite key).

```text
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

As mentioned above, when a table is marked as a dimension table it will be replicated on all the hosts, because of this the size of the dim table has to be small. The maximum size quota for a dimension table in a cluster is controlled by `controller.dimTable.maxSize` controller property. Table creation will fail if the storage quota exceeds this maximum size.