---
description: >-
  To query using distributed joins, window functions, and other multi-stage
  operators in real time, turn on the multi-stage query engine (v2).
---

# Use the multi-stage query engine (v2)

To query using distributed joins, window functions, and other multi-stage operators in real time, you must enable the multi-stage query engine (v2). To enable v2, do any of the following:

* Enable the multi-stage query engine [in the Query Console](v2-multi-stage-query-engine.md#enable-the-multi-stage-query-engine-in-the-query-console)
* Programmatically access the multi-stage query engine:
  * Query [using REST APIs](v2-multi-stage-query-engine.md#use-rest-apis)
  * Query outside of the APIs [using the query option](v2-multi-stage-query-engine.md#use-the-query-option)

To learn more about what the multi-stage query engine is, see [Multi-stage query engine (v2)](../../reference/multi-stage-engine.md).

## Enable the multi-stage query engine in the Query Console

* To enable the multi-stage query engine, in the Pinot Query Console, select the **Use Multi-Stage Engine** check box.

<figure><img src="../../.gitbook/assets/pinot-query-console-multi-stage-enabled (2).png" alt=""><figcaption><p>Pinot Query Console with Use Multi Stage Engine enabled</p></figcaption></figure>

## Programmatically access the multi-stage query engine

To query the Pinot multi-stage query engine, use REST APIs or the query option:

### Use REST APIs

The Controller admin API and the Broker query API allow optional JSON payload for configuration. For example:

* [For Controller Admin API](../../users/api/pinot-rest-admin-interface.md)

```bash
curl -X POST http://localhost:9000/sql -d 
'
{
  "sql": "select * from baseballStats limit 10",
  "trace": false,
  "queryOptions": "useMultistageEngine=true"
}
'
```

* [For Broker Query API](../../users/api/querying-pinot-using-standard-sql/)

```bash
curl -X POST http://localhost:8000/query/sql -d '
{
  "sql": "select * from baseballStats limit 10",
  "trace": false,
  "queryOptions": "useMultistageEngine=true"
}
'
```

### Use the query option

To enable the multi-stage engine via a query outside of the API, add the `useMultistageEngine=true` option to the top of your query.

For example:

<pre class="language-sql"><code class="lang-sql"><strong>SET useMultistageEngine=true; -- indicator to enable the multi-stage engine.
</strong>SELECT * from baseballStats limit 10
</code></pre>
