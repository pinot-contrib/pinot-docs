---
description: Run your first SQL queries against Pinot using the Query Console and REST API.
---

# First query

## Outcome

Run your first SQL queries against Pinot and understand the query interface.

## Prerequisites

* You have completed either [First batch ingest](first-batch-ingest.md) or [First stream ingest](first-stream-ingest.md). The `transcript` table exists and contains data.
* The Pinot cluster is running (Controller on port 9000, Broker on port 8099).

## Steps

### 1. Open the Query Console

Navigate to [http://localhost:9000](http://localhost:9000) in your browser. Click **Query Console** in the left sidebar. You should see the `transcript` table listed in the table explorer on the left.

### 2. Run a simple SELECT

Paste the following query into the query editor and click **Run Query**:

```sql
SELECT * FROM transcript LIMIT 10
```

The results panel shows all columns in the `transcript` table -- `studentID`, `firstName`, `lastName`, `gender`, `subject`, `score`, and `timestamp`. The rows returned come from whichever data you loaded (batch, stream, or both). `LIMIT 10` caps the result set so the response is fast.

### 3. Run an aggregation

```sql
SELECT subject, AVG(score) AS avg_score
FROM transcript
GROUP BY subject
ORDER BY avg_score DESC
```

This query calculates the average score per subject and sorts the results from highest to lowest. Pinot executes aggregations directly on each server's segment data and merges the results at the Broker, making GROUP BY queries fast even on large datasets.

### 4. Run a count

```sql
SELECT COUNT(*) FROM transcript
```

This returns the total number of rows in the table. The exact count depends on which ingestion steps you completed:

* Batch ingest only -- 4 rows
* Stream ingest only -- the number of events you published (up to 12 in the tutorial)
* Both -- the combined total

### 5. Run a filter

```sql
SELECT firstName, lastName, score
FROM transcript
WHERE score > 3.5
```

This filters rows to show only students with a score above 3.5. Pinot pushes filter predicates down to the servers so only matching rows are scanned and returned.

### 6. Try the REST API

The Query Console UI is convenient for exploration, but production applications query Pinot through its REST API. Open a terminal and run:

```bash
curl -X POST http://localhost:8099/query/sql \
  -H 'Content-Type: application/json' \
  -d '{"sql": "SELECT * FROM transcript LIMIT 5"}'
```

Port 8099 is the Broker, which handles all query requests. The Query Console UI uses the same API under the hood. The response is a JSON object containing the result rows, schema, and query execution metadata.

## Verify

All five queries return results without errors. You have successfully completed the end-to-end onboarding flow: you set up a Pinot cluster, defined a schema and table, loaded data, and queried it through both the UI and the REST API.

## What's next

You have finished the linear Start Here path. From here, explore the areas most relevant to your use case:

* [Query Syntax](../../users/user-guide-query/query-syntax-overview.md) -- the full SQL reference for Pinot's query language
* [Multi-Stage Query Engine](../../users/user-guide-query/multi-stage-query/README.md) -- enable JOINs and complex queries across tables
* [Architecture](../../basics/architecture.md) -- understand how queries flow from Broker to Server and back
* [Stream Ingestion from Kafka](../../manage-data/data-import/pinot-stream-ingestion/import-from-apache-kafka.md) -- set up real-time ingestion for production workloads
