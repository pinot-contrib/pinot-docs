---
description: Pinot controller admin UI reference.
---

# Controller Admin API

The controller admin UI at `http://<controller-host>:<port>/help` is the quickest way to inspect and exercise Pinot's administrative endpoints. Use it for schema, table, and segment operations when you want the interactive Swagger surface instead of raw curl examples.

## What It Covers

| Area | Typical task |
| --- | --- |
| Tables | List, inspect, delete, and update table configs |
| Schemas | List, inspect, create, and delete schemas |
| Segments | List, inspect, upload, and reload segments |

## Operational Reminder

Controller APIs are for administrative tasks. Use the broker query API for querying Pinot, even if the controller UI also exposes a query console.

## What this page covered

- The controller Swagger UI entry point.
- Which administrative tasks belong in the controller UI.
- Why the broker query API still owns SQL execution.

## Next step

Use the Swagger UI to confirm the endpoint shape, then jump to the controller API examples page when you need exact curl payloads.

## Related pages

- [API Reference](README.md)
- [Controller API Examples](controller-api.md)
- [Broker Query API](query-api.md)
- [Query Response Format](query-response-format.md)
# Controller Admin API

The [Pinot Admin UI](http://localhost:9000/help) contains all the APIs that you will need to operate and manage your cluster. It provides a set of APIs for Pinot cluster management including health check, instances management, schema and table management, data segments management.

Note: The controller API's are primarily for admin tasks. Even though the UI console queries Pinot when running queries from the query console, use the [Broker Query API](../../README.md) for querying Pinot.

![](<../../.gitbook/assets/pinot-admin-ui.png>)

Let's check out the tables in this cluster by going to [Table -> List all tables in cluster](http://localhost:9000/help#!/Table/listTableConfigs) and click on `Try it out!`. We can see the `baseballStats` table listed here. We can also see the exact `curl` call made to the controller API.

![List all tables in cluster](<../../.gitbook/assets/list-all-tables.png>)

You can look at the configuration of this table by going to [Tables -> Get/Enable/Disable/Drop a table](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig), type in `baseballStats` in the table name, and click `Try it out!`

Let's check out the schemas in the cluster by going to [Schema -> List all schemas in the cluster](http://localhost:9000/help#!/Schema/listSchemaNames) and click `Try it out!`. We can see a schema called `baseballStats` in this list.

![List all schemas in the cluster](<../../.gitbook/assets/list-all-schemas.png>)

Take a look at the schema by going to [Schema -> Get a schema](http://localhost:9000/help#!/Schema/getSchema), type `baseballStats` in the schema name, and click `Try it out!`.

```
{
  "schemaName": "baseballStats",
  "dimensionFieldSpecs": [
    {
      "name": "playerID",
      "dataType": "STRING"
    },
    {
      "name": "yearID",
      "dataType": "INT"
    },
    {
      "name": "teamID",
      "dataType": "STRING"
    },
    {
      "name": "league",
      "dataType": "STRING"
    },
    {
      "name": "playerName",
      "dataType": "STRING"
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "playerStint",
      "dataType": "INT"
    },
    {
      "name": "numberOfGames",
      "dataType": "INT"
    },
    {
      "name": "numberOfGamesAsBatter",
      "dataType": "INT"
    },
    {
      "name": "AtBatting",
      "dataType": "INT"
    },
    {
      "name": "runs",
      "dataType": "INT"
    },
    {
      "name": "hits",
      "dataType": "INT"
    },
    {
      "name": "doules",
      "dataType": "INT"
    },
    {
      "name": "tripples",
      "dataType": "INT"
    },
    {
      "name": "homeRuns",
      "dataType": "INT"
    },
    {
      "name": "runsBattedIn",
      "dataType": "INT"
    },
    {
      "name": "stolenBases",
      "dataType": "INT"
    },
    {
      "name": "caughtStealing",
      "dataType": "INT"
    },
    {
      "name": "baseOnBalls",
      "dataType": "INT"
    },
    {
      "name": "strikeouts",
      "dataType": "INT"
    },
    {
      "name": "intentionalWalks",
      "dataType": "INT"
    },
    {
      "name": "hitsByPitch",
      "dataType": "INT"
    },
    {
      "name": "sacrificeHits",
      "dataType": "INT"
    },
    {
      "name": "sacrificeFlies",
      "dataType": "INT"
    },
    {
      "name": "groundedIntoDoublePlays",
      "dataType": "INT"
    },
    {
      "name": "G_old",
      "dataType": "INT"
    }
  ]
}
```

Finally, let's checkout the data segments in the cluster by going to [List all segments](http://localhost:9000/help#!/Segment/getSegments), type in `baseballStats` in the table name, and click `Try it out!`. There's 1 segment for this table, called `baseballStats_OFFLINE_0`.

## Deleting tables and schemas

You can delete tables and schemas using the REST API or the Pinot Data Explorer UI.

### Using the API

To delete a table, send a `DELETE` request to `/tables/{tableName}`. By default, segments are moved to a deleted-segments area and retained for a period (default 7 days) before permanent removal. To delete segments immediately with no retention, pass `retention=0d`:

```
curl -X DELETE "http://localhost:9000/tables/baseballStats?retention=0d" -H "accept: application/json"
```

To also delete the schema after deleting the table, send a separate `DELETE` request:

```
curl -X DELETE "http://localhost:9000/schemas/baseballStats" -H "accept: application/json"
```

{% hint style="warning" %}
Using `retention=0d` permanently deletes all data immediately with no possibility of recovery. Only use this for development, testing, or cleanup scenarios where the data is no longer needed.
{% endhint %}

For more details on the delete table API and its parameters, see the [Controller API Examples](controller-api.md#delete-tables-less-than-tablename-greater-than).

### Using the Data Explorer UI

In the Pinot Data Explorer, navigate to a table and click **Delete Table**. The delete dialog provides two options:

* **Delete Immediately** -- Bypasses the default segment retention period and deletes all segments right away. This is equivalent to passing `retention=0d` in the API. This is useful for large tables where the default delete operation might time out.
* **Delete Schema** -- After successfully deleting the table, also deletes the associated schema. This only works if no other tables are using the same schema.

You might have figured out by now, in order to get data into the Pinot cluster, we need a table, a schema, and segments. Continue with [First table and schema](../../basics/getting-started/first-table-and-schema.md) and then [First batch ingest](../../basics/getting-started/first-batch-ingest.md) to create them for your own data.
