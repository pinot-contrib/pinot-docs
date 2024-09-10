# Visualize data with Redash

1. Install Redash and start a running instance, following the [Docker Based Developer Installation Guide](https://redash.io/help/open-source/dev-guide/docker).
2. Configure Redash to query Pinot, by doing the following:
   1. [Add pinotdb dependency](redash.md#add-pinot-db-dependency)
   2. [Add a Python data source for Pinot](redash.md#add-python-data-source-for-pinot)
3. Create visualizations, by doing the following:
   1. [Start Pinot](redash.md#start-pinot)
   2. [Query in Redash](redash.md#run-a-query-in-redash)
   3. [Add a visualization and dashboard in Redash](redash.md#add-a-visualization-and-dashboard-in-redash)

## Add pinot db dependency

Apache Pinot provides a Python client library `pinotdb` to query Pinot from Python applications. Install `pinotdb` inside the Redash worker instance to make network calls to Pinot.

1. Navigate to the root directory where you’ve cloned Redash. Run the following command to get the name of the Redash worker container (by default, `redash_worker_1`):

`docker-compose ps`

2. Run the following command (change `redash_worker_1` to your own Redash worker container name, if applicable):

```python
docker exec -it redash_worker_1 /bin/sh                                
pip install pinotdb
```

3. Restart **Docker**.

## Add Python data source for Pinot

1. In Redash, select **Settings > Data Sources**.
2. Select **New Data Source**, and then select **Python** from the list. ![Redash Settings - Data Sources](https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/recipes/redash-settings-data-source.png)
3. On the Redash **Settings - Data Source** page, add `Pinot` as the name of the data source, enter `pinotdb` in the **Modules to import prior to running the script** field.
4. Enter the following optional fields as needed:
   * **AdditionalModulesPaths**: Enter a comma-separated list of absolute paths on the Redash server to Python modules to make available when querying from Redash. Useful for private modules unavailable in `pip`.
   * **AdditionalBuiltins**: Specify additional built-in functions as needed. By default, Redash automatically includes 25 Python built-in functions.
5. Click **Save**.

## Start Pinot

Run the following command in a new terminal to spin up an Apache Pinot Docker container in the quick start mode with a baseball stats dataset built in.

```python
docker run \
  --name pinot-quickstart \
  -p 2123:2123 \
  -p 9000:9000 \
  -p 8000:8000 \
  apachepinot/pinot:0.9.3 QuickStart -type batch
```

## Run a query in Redash

1. In Redash, select **Queries > New Query**, and then select the Python data source you created in [Add a Python data source for Pinot](redash.md#add-python-data-source-for-pinot).
2. Add Python code to query data. For more information, see the [Python query runner](https://redash.io/help/data-sources/querying/python#Writing-Queries).
3. Click **Execute** to run the query and view results.

You can also include libraries like Pandas to perform more advanced data manipulation on Pinot’s data and visualize the output with Redash.

For more information, see [Querying](https://redash.io/help/user-guide/querying) in Redash documentation.

## Example Python queries

### Query top 10 teams by total runs

The following query connects to Pinot and queries the `baseballStats` table to retrieve the top ten players with the highest scores. The results are transformed into a dictionary format supported by Redash.

```python
from pinotdb import connect

conn = connect(host='host.docker.internal', port=8000, path='/query/sql', scheme='http')
curs = conn.cursor()
curs.execute("""
    select 
playerName, sum(runs) as total_runs
from baseballStats
group by playerName
order by total_runs desc
limit 10
""")

result = {}
result['columns'] = [
    {
      "name": "player_name",
      "type": "string",
      "friendly_name": "playerName"
    },
    {
      "name": "total_runs",
      "type": "integer",
      "friendly_name": "total_runs"
    }
  ]

rows = []

for row in curs:
    record = {}
    record['player_name'] = row[0]
    record['total_runs'] = row[1]


    rows.append(record)

result["rows"] = rows
```

### Query top 10 teams by total runs

```python
from pinotdb import connect

conn = connect(host='host.docker.internal', port=8000, path='/query/sql', scheme='http')
curs = conn.cursor()
curs.execute("""
    select 
teamID, sum(runs) as total_runs
from baseballStats
group by teamID
order by total_runs desc
limit 10
""")

result = {}
result['columns'] = [
    {
      "name": "teamID",
      "type": "string",
      "friendly_name": "Team"
    },
    {
      "name": "total_runs",
      "type": "integer",
      "friendly_name": "Total Runs"
    }
  ]

rows = []

for row in curs:
    record = {}
    record['teamID'] = row[0]
    record['total_runs'] = row[1]


    rows.append(record)

result["rows"] = rows
```

### Query total strikeouts by year

```python
from pinotdb import connect

conn = connect(host='host.docker.internal', port=8000, path='/query/sql', scheme='http')
curs = conn.cursor()
curs.execute("""
    select 
yearID, sum(strikeouts) as total_so
from baseballStats
group by yearID
order by yearID asc
limit 1000
""")

result = {}
result['columns'] = [
    {
      "name": "yearID",
      "type": "integer",
      "friendly_name": "Year"
    },
    {
      "name": "total_so",
      "type": "integer",
      "friendly_name": "Total Strikeouts"
    }
  ]

rows = []

for row in curs:
    record = {}
    record['yearID'] = row[0]
    record['total_so'] = row[1]


    rows.append(record)

result["rows"] = rows
```

## Add a visualization and dashboard in Redash

### Add a visualization

In Redash, after you've ran your query, click the **New Visualization** tab, and select the type of visualization your want to create, for example, **Bar Chart**. The Visualization Editor appears with your chart.

For example, you may want to create a bar chart to view the top 10 players with highest scores.

![Bar chart configuration](https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/recipes/bar-chart-config.png)

You may want to create a line chart to view the total variation in strikeouts over time.

For more information, see [Visualizations](https://redash.io/help/user-guide/visualizations).

### Add a dashboard

Create a dashboard with one or more visualizations (widgets).

1. In Redash, go to Dashboards > New Dashboards.
2. Add the widgets to your dashboard. For example, by adding the three visualizations from the [three example queries](redash.md#example-python-queries) above, you create a Baseball stats dashboard.

![Baseball stats dashboard](https://github.com/pinot-contrib/pinot-docs/blob/latest/basics/recipes/baseball-stats-dashboard.png)

For more information, see [Dashboards](https://redash.io/help/user-guide/dashboards) in the Redash documentation.
