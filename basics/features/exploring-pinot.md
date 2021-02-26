---
description: Explore the data on our Pinot cluster
---

# Pinot data explorer

Now that the QuickStartCluster is setup, we can start exploring the data and the APIs. Head over to [http://localhost:9000](http://localhost:9000) in your browser.

![](../../.gitbook/assets/screen-shot-2020-02-28-at-9.46.33-am%20%282%29%20%282%29%20%282%29%20%282%29%20%282%29%20%281%29.png)

You are now connected to the Pinot controller. Let's take a look at the following two features.

## Query Console

[Query Console](http://localhost:9000/query#) let's us run queries on the data in the Pinot cluster

We can see our `baseballStats` table listed on the left \(you will see `meetupRSVP` or `airlineStats` if you used the streaming or the hybrid quick start\). Clicking on the table name should display all the names and data types of the columns of the table, and also execute a sample query `select * from baseballStats limit 10` . You can query this table by typing your query in the text box and clicking the `Run Query` button.

![Pinot Data Explorer](../../.gitbook/assets/screen-shot-2020-02-28-at-9.49.12-am.png)

Here's some other queries you can try out:

`select playerName, max(hits) from baseballStats group by playerName order by max(hits) desc`

`select sum(hits), sum(homeRuns), sum(numberOfGames) from baseballStats where yearID > 2010`

`select * from baseballStats order by league`

Pinot supports a subset of standard SQL. See [Pinot Query Language](../../users/user-guide-query/pinot-query-language/) for more information.

## Rest API

The [Pinot Admin UI](http://localhost:9000/help) contains all the APIs that you will need to operate and manage your cluster. It provides a set of APIs for Pinot cluster management including health check, instances management, schema and table management, data segments management.

![](../../.gitbook/assets/screen-shot-2020-02-28-at-10.00.43-am.png)

Let's check out the tables in this cluster by going to [Table -&gt; List all tables in cluster](http://localhost:9000/help#!/Table/listTableConfigs) and click on `Try it out!`. We can see the `baseballStats` table listed here. We can also see the exact `curl` call made to the controller API.

![List all tables in cluster](../../.gitbook/assets/screen-shot-2020-02-28-at-10.00.26-am.png)

You can look at the configuration of this table by going to [Tables -&gt; Get/Enable/Disable/Drop a table](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig), type in `baseballStats` in the table name, and click `Try it out!`

Let's check out the schemas in the cluster by going to [Schema -&gt; List all schemas in the cluster](http://localhost:9000/help#!/Schema/listSchemaNames) and click `Try it out!`. We can see a schema called `baseballStats` in this list.

![List all schemas in the cluster](../../.gitbook/assets/screen-shot-2020-02-28-at-10.09.18-am.png)

Take a look at the schema by going to [Schema -&gt; Get a schema](http://localhost:9000/help#!/Schema/getSchema), type `baseballStats` in the schema name, and click `Try it out!`.

```text
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

Finally, let's checkout the data segments in the cluster by going to [Segment -&gt; List all segments](http://localhost:9000/help#!/Segment/getSegments), type in `baseballStats` in the table name, and click `Try it out!`. There's 1 segment for this table, called `baseballStats_OFFLINE_0`.

You might have figured out by now, in order to get data into the Pinot cluster, we need a table, a schema and segments. Let's head over to [Batch upload sample data](../getting-started/pushing-your-data-to-pinot.md), to find out more about these components and learn how to create them for your own data.

