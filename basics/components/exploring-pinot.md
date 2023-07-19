---
description: >-
  Pinot Data Explorer is a user-friendly interface in Apache Pinot for
  interactive data exploration, querying, and visualization.
---

# Pinot Data Explorer

Once you have set up a cluster, you can start exploring the data and the APIs using the Pinot Data Explorer.

Navigate to [http://localhost:9000](http://localhost:9000) in your browser to open the Data Explorer UI.

## Cluster Manager

The first screen that you'll see when you open the Pinot Data Explorer is the Cluster Manager. The Cluster Manager provides a UI to operate and manage your cluster.

![Pinot Cluster Manager](<../../.gitbook/assets/Screenshot from 2021-11-25 10-47-54.png>)

If you want to view the contents of a server, click on its instance name. You'll then see the following:

![Pinot Server](<../../.gitbook/assets/image (58).png>)

To view the _baseballStats_ table, click on its name, which will show the following screen:

![baseballStats Table](<../../.gitbook/assets/image (2) (1).png>)

From this screen, we can edit or delete the table, edit or adjust its schema, as well as several other operations.

For example, if we want to add _yearID_ to the list of inverted indexes, click on **Edit Table,** add the extra column, and click **Save:**

![Edit Table](<../../.gitbook/assets/Screenshot from 2021-11-25 10-57-48.png>)

## Query Console

Let's run some queries on the data in the Pinot cluster. Navigate to [Query Console](http://localhost:9000/#/query) to see the querying interface.

We can see our `baseballStats` table listed on the left (you will see `meetupRSVP` or `airlineStats` if you used the streaming or the hybrid [quick start](https://docs.pinot.apache.org/basics/getting-started/running-pinot-in-docker)). Click on the table name to display all the names along with the data types of the columns of the table.

You can also execute a sample query `select * from baseballStats limit 10` by typing it in the text box and clicking the **Run Query** button.

`Cmd + Enter` can also be used to run the query when focused on the console.

![](../../.gitbook/assets/Pinot\_query\_console\_cropped.png)

Here are some sample queries you can try:

```sql
select playerName, max(hits) 
from baseballStats 
group by playerName 
order by max(hits) desc
```

```sql
select sum(hits), sum(homeRuns), sum(numberOfGames) 
from baseballStats 
where yearID > 2010
```

```sql
select * 
from baseballStats 
order by league
```

Pinot supports a subset of standard SQL. For more information, see [Pinot Query Language](../../users/user-guide-query/querying-pinot.md).

## Rest API

The [Pinot Admin UI](http://localhost:9000/help) contains all the APIs that you will need to operate and manage your cluster. It provides a set of APIs for Pinot cluster management including health check, instances management, schema and table management, data segments management.

![](<../../.gitbook/assets/Screen Shot 2020-02-28 at 10.00.43 AM.png>)

Let's check out the tables in this cluster by going to [Table -> List all tables in cluster](http://localhost:9000/help#/Table/listTables), click **Try it out**, and then click **Execute**. We can see the`baseballStats` table listed here. We can also see the exact cURL call made to the controller API.

![List all tables in cluster](<../../.gitbook/assets/image (32).png>)

You can look at the configuration of this table by going to [Tables -> Get/Enable/Disable/Drop a table](http://localhost:9000/help#!/Table/alterTableStateOrListTableConfig), click **Try it out**, type `baseballStats` in the table name, and then click **Execute**.

Let's check out the schemas in the cluster by going to [Schema -> List all schemas in the cluster](http://localhost:9000/help#!/Schema/listSchemaNames), click **Try it out**, and then click **Execute**. We can see a schema called `baseballStats` in this list.

![List all schemas in the cluster](<../../.gitbook/assets/image (25).png>)

Take a look at the schema by going to [Schema -> Get a schema](http://localhost:9000/help#!/Schema/getSchema), click **Try it out**, type `baseballStats` in the schema name, and then click **Execute**.

![baseballStats Schema](<../../.gitbook/assets/image (64).png>)

Finally, let's check out the data segments in the cluster by going to [Segment -> List all segments](http://localhost:9000/help#!/Segment/getSegments), click **Try it out**, type in `baseballStats` in the table name, and then click **Execute**. There's 1 segment for this table, called `baseballStats_OFFLINE_0`.

To learn how to upload your own data and schema, see [Batch Ingestion](../data-import/batch-ingestion/) or [Stream ingestion](../data-import/pinot-stream-ingestion/).
