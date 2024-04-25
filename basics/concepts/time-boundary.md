---
description: Learn about time boundaries in hybrid tables.
---

# Time boundary

Learn about time boundaries in hybrid tables. Hybrid tables are when we have offline and real-time tables with the same name.

When querying these tables, the Pinot broker decides which records to read from the offline table and which to read from the real-time table. It does this using the time boundary.

## How is the time boundary determined?

The time boundary is determined by looking at the maximum end time of the offline segments and the segment ingestion frequency specified for the offline table.

If it's set to hourly, then:

```
timeBoundary = Maximum end time of offline segments - 1 hour
```

Otherwise:

```
timeBoundary = Maximum end time of offline segments - 1 day
```

It is possible to force the hybrid table to use max(all offline segments' `end time`) by calling the API (V 0.12.0+)

```
curl -X POST \
  "http://localhost:9000/tables/{tableName}/timeBoundary" \
  -H "accept: application/json"
```

Note that this will not automatically update the time boundary as more segments are added to the offline table, and must be called each time a segment with more recent end time is uploaded to the offline table. You can revert back to using the derived time boundary by calling API:

```
curl -X DELETE \
  "http://localhost:9000/tables/{tableName}/timeBoundary" \
  -H "accept: application/json"
```

## Querying

When a Pinot broker receives a query for a hybrid table, the broker sends a time boundary annotated version of the query to the offline and real-time tables.

For example, if we executed the following query:

```sql
SELECT count(*)
FROM events
```

The broker would send the following query to the offline table:

```sql
SELECT count(*)
FROM events_OFFLINE
WHERE timeColumn <= $timeBoundary
```

And the following query to the real-time table:

```sql
SELECT count(*)
FROM events_REALTIME
WHERE timeColumn > $timeBoundary
```

The results of the two queries are merged by the broker before being returned to the client.
