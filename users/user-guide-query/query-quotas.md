# Query Quotas

Pinot allows a way to limit the queries fired by providing a way to set quotas on the query rate.
Below are the possible ways of setting query quotas in pinot.

## Table Level Query Quota

User can limit the queries made to a table by imposing query quota on the table.

### How to configure

The table level query quota is configured in table config itself.

```json
{
  "tableName": "pinotTable",
  "tableType": "OFFLINE",
  "quota": {
    "maxQueriesPerSecond": 300
  },
  ...
}
```

### How it is imposed

There are few factors that affect the way the query quota is imposed on the incoming queries on the table.

| Affecting factors | Description                                                                                                                                                                                                                                                                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Number of brokers | The provided query quota is distributed among all the active brokers that serve the table. That means if there are 5 brokers that serve a table and query quota is provided as 300, each broker will get a quota of 60 qps and will fail queries that goes over it                                                                            |
| Table types       | In case of a hybrid table (table with both OFFLINE and REALTIME counterparts) user can provide quotas to each of them separately in their respective table configs. But if a query is made on table name without type, that will contribute to the quota limits of both the tables. If any one of the quotas are reached the query will fail. |
| Multi stage query | As multi stage query can span across multiple tables, this will contribute to the quota limits of all the tables being queried. If quota limit of any of the table is breached the query will fail                                                                                                                                            |


## Database Level Query Quota

User can limit the queries made across all tables under a database. This quota is useful to isolate and limit the query traffic for each database.

### How to configure

There are 2 ways to configure the database level query quota.

1. default quota : to set a default quota for all the databases across the cluster. This helps to avoid the maintenance overhead of specifying quota for each database when we just want a similar quota across all databases
2. database specific quota : to apply a specific quota on a database. This will override the default quota if present.

For providing the default quota we need to provide the below cluster config
```shell
curl -X POST \
  'http://localhost:9000/cluster/configs' \
  -d '{
    "databaseMaxQueriesPerSecond" : "1000"
  }'
```

For database specific quota we can leverage the controller endpoints

```shell
# to set database specific quota
curl -X POST 'http://localhost:9000/databases/{databaseName}/quotas?maxQueriesPerSecond=1200'
```

```shell
# to get the effective quota on a database
curl -X GET 'http://localhost:9000/databases/{databaseName}/quotas'
```

### How it is imposed

There are few factors that affect the way the database query quota is imposed.

| Affecting factors | Description                                                                                                                                                                                                                                      |
|-------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Number of brokers | The provided query quota is distributed among all the active brokers. That means if there are total 5 brokers online and database query quota is provided as 300, each broker will get a quota of 60 qps and will fail queries that goes over it |
| Tables            | When a table is queried under a particular database the rate limiter is incremented for that database if database query quota is configured.                                                                                                     |
| Multi stage query | As multi stage query can span across multiple tables in a database (cross database query is not allowed), this will contribute just to the database query quota of the database which the tables belong to.                                      |

## What happens when multiple query quotas are configured?

If user sets a query quota at table level as well as database level then

- First the query is validated against the database query quota, if there is a breach it will fail the query right away without going for the table level quota
- If database query quota is satisfied, the query is validated against the table query quota. Based on the validation the query is either allowed or failed
- Note that even if table level query quota is available for a table the query will fail if database query quota limit has reached
