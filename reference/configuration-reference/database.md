# Database

The database concept in pinot allows users to create a logical isolation of tables so that single pinot cluster can be used by multiple teams/users at the same time without worrying about the operational aspects such as having a unique table name across cluster or accidental updates to similar looking table names owned by different users.

## How to enable the feature?

The feature is available since [1.2.0](https://github.com/apache/pinot/releases/tag/release-1.2.0) release.

## How to use the database concept?

Pinot does not have database as the first class entity yet. The logical bucketing is achieved through namespacing the table names with the database prefix like `<databaseName>.<tableName>` .  So basically the database creation will implicitly happen with the creation of a table under it.

{% hint style="info" %}
Existing tables or tables without any database prefix are classified under the "default" database
{% endhint %}

### Table Creation

To create a table under a database we can use the usual table creation endpoint but in addition to that we need to provide an extra header `Database : <databaseName>`  to make sure the table gets created under that database. You can skip adding the database prefix to the table name in the payload, the endpoint should take care of it.

Its convenient to use the swagger UI as there we have an option to configure the database header at one place and use it across all operations\


![](<../../.gitbook/assets/image (17).png>)

*Configure database header in Swagger UI*

{% hint style="info" %}
Pinot UI is not yet onboarded to handle database feature. We only tables under the default database in the UI. So we are heavily dependent on swagger UI to operate tables under different databases.
{% endhint %}

### Query the Table

#### Single stage query engine

You need to either **pass the database header** in the query request or write the query with fully qualified table name such as `select * from db1.tableA limit 10`&#x20;

#### Multi stage query engine

For MSQE its recommended not to use the fully qualified table name approach, either pass the database header with the query or we can also set the database as part of query such as&#x20;

```sql
set database='db1';
select * from tableA limit 10
```

{% hint style="info" %}
In case of MSQE you cannot query tables across different databases in a single query
{% endhint %}

As you may have noticed 2 users can have separate tables with the same name, say `tableA` , and will be able to manage and query them independently just by setting the right database context!

## Database Ops

Pinot exposes few APIs to get database level info

![](<../../.gitbook/assets/image (18).png>)

**

We can

* List all databases on the cluster
* Delete all the tables under a database
* Manage quotas like query rate and storage (check [this](../../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md#database-level-query-quota) out)&#x20;

Apart from this all the endpoints that deal with table, table config and schema is database aware and requires user to pass the right database in the header else the request will fail.

