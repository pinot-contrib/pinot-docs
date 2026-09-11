---
description: >-
  Query Apache Pinot from a Jupyter notebook using JupySQL magics, plot results,
  and keep them as pandas DataFrames for EDA.
---

# Query Pinot from Jupyter with JupySQL

This tutorial shows how to use [JupySQL](https://jupysql.ploomber.io/) and the
[pinotdb](https://pypi.org/project/pinotdb/) Python client to query Apache Pinot
from a Jupyter notebook: SQL magics, plots, and DataFrames for EDA.

A runnable notebook lives in the Pinot source tree:

[contrib/jupyter-jupysql](https://github.com/apache/pinot/tree/master/contrib/jupyter-jupysql)

## Prerequisites

* Python 3.10+
* A running Pinot **batch quickstart** (loads the `baseballStats` table)
* Jupyter, JupySQL, pinotdb, pandas, and matplotlib

The batch and Docker quickstarts expose the **broker SQL API on port 8000** and
the controller UI on port 9000. Do not use port 8099 unless you started a
cluster that binds the broker there.

### Start Pinot (Docker)

```bash
docker run --name pinot-quickstart \
  -p 2123:2123 -p 9000:9000 -p 8000:8000 \
  -d apachepinot/pinot:latest QuickStart -type batch
```

Wait until http://localhost:9000 is up.

### Start Pinot (local build)

From an apache/pinot checkout after a binary build:

```bash
./build/bin/quick-start-batch.sh
```

### Install Python packages

```bash
pip install pinotdb jupysql pandas matplotlib jupyter sqlalchemy
```

Or, from the Pinot repo:

```bash
pip install -r contrib/jupyter-jupysql/requirements.txt
```

## Connect from the notebook

JupySQL talks to Pinot through SQLAlchemy and pinotdb. Create an engine and pass
it to `%sql` (more reliable than embedding a non-standard URL in the magic):

```python
from sqlalchemy import create_engine

%matplotlib inline
%load_ext sql

%config SqlMagic.autopandas = True
%config SqlMagic.feedback = False
%config SqlMagic.displaycon = False

engine = create_engine(
    "pinot://localhost:8000/query/sql?controller=http://localhost:9000/",
    connect_args={"use_multistage_engine": "true"},
)
%sql engine
```

Enable the [multi-stage query engine](https://docs.pinot.apache.org/developers/advanced/v2-multi-stage-query-engine)
on the connection. JupySQL `%sqlplot` rewrites plots as `WITH ...` queries, which
the single-stage engine rejects.

The URL shape is:

```text
pinot://<broker-host>:<broker-port>/query/sql?controller=http://<controller-host>:<controller-port>/
```

## Query with SQL magics

`%%sql` sends the statement to the broker `POST /query/sql` endpoint.

Scan a few rows:

```sql
%%sql
SELECT playerName, teamID, yearID, runs, homeRuns
FROM baseballStats
LIMIT 5
```

Aggregate with `GROUP BY` / `ORDER BY`:

```sql
%%sql
SELECT playerName, SUM(runs) AS sum_runs
FROM baseballStats
WHERE yearID >= 2000
GROUP BY playerName
ORDER BY sum_runs DESC
LIMIT 10
```

## Plot from SQL

With `SqlMagic.autopandas = True`, a `%sql` assignment is a pandas DataFrame:

```python
top_teams = %sql SELECT teamID, SUM(runs) AS total_runs FROM baseballStats GROUP BY teamID ORDER BY total_runs DESC LIMIT 10

ax = top_teams.plot.bar(x="teamID", y="total_runs", legend=False)
ax.set_title("Top 10 teams by total runs")
ax.set_xlabel("teamID")
ax.set_ylabel("total runs")
```

You can also save a result and use JupySQL's `%sqlplot`:

```sql
%%sql --save top_teams_sql
SELECT teamID, SUM(runs) AS total_runs
FROM baseballStats
GROUP BY teamID
ORDER BY total_runs DESC
LIMIT 10
```

```python
%sqlplot bar --table top_teams_sql --column teamID
```

## Use Pinot results in EDA or modeling

Keep the DataFrame and continue in Python (further EDA, sklearn, and so on).
This tutorial stops at the DataFrame — it does not train a model.

```python
player_runs = %sql SELECT playerName, SUM(runs) AS sum_runs, SUM(homeRuns) AS sum_hr FROM baseballStats WHERE yearID >= 2000 GROUP BY playerName ORDER BY sum_runs DESC LIMIT 20

player_runs.head()
```

## Next steps

* Full notebook: [pinot_jupysql_eda.ipynb](https://github.com/apache/pinot/blob/master/contrib/jupyter-jupysql/pinot_jupysql_eda.ipynb)
* [Python client (pinotdb)](../../build-with-pinot/connectors-clients-apis/clients/python.md)
* [10-minute quickstart](../../basics/getting-started/ten-minute-quickstart.md)
