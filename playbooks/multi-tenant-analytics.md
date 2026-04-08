---
description: End-to-end guide for serving multiple customers from a shared Pinot cluster with resource and data isolation.
---

# Multi-Tenant Analytics

This playbook covers serving analytics to many customers (tenants) from a single Pinot cluster. The pattern is common in B2B SaaS products where each customer gets their own dashboard but the infrastructure is shared for cost efficiency. It combines Pinot's tenant tagging, workload isolation, and application-level row filtering to deliver per-customer data isolation and fair resource allocation.

## When to use this pattern

Use this playbook when:

- You operate a SaaS product where each customer should only see their own data.
- You want to run a single Pinot cluster (lower operational overhead) rather than one cluster per customer.
- Different customers have different query volumes, and you need to prevent a heavy-hitter from degrading others.
- You need to enforce data isolation at the query layer (row-level security) alongside resource isolation at the infrastructure layer.

## Architecture sketch

```
Customer A ──▶ App backend ──▶ Broker pool A ──▶ Servers (tenant A)
Customer B ──▶ App backend ──▶ Broker pool B ──▶ Servers (shared)
Customer C ──▶ App backend ──▶ Broker pool B ──▶ Servers (shared)
                  │
          (injects tenant_id
           filter into every query)
```

There are two complementary isolation layers:

1. **Infrastructure isolation** via Pinot tenants — assign servers and brokers to named tenants so resource-hungry customers get dedicated compute.
2. **Data isolation** via application-level row filtering — the application layer injects a `WHERE tenant_id = '<customer>'` predicate into every query.

## Data model

### Single-table approach (recommended for most cases)

Store all tenants' data in one table with a `tenantId` dimension:

```json
{
  "schemaName": "saas_events",
  "dimensionFieldSpecs": [
    { "name": "tenantId",   "dataType": "STRING" },
    { "name": "eventType",  "dataType": "STRING" },
    { "name": "userId",     "dataType": "STRING" },
    { "name": "feature",    "dataType": "STRING" },
    { "name": "plan",       "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "durationMs", "dataType": "LONG" },
    { "name": "count",      "dataType": "INT" }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "eventTimestamp",
      "dataType": "TIMESTAMP",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

### Table-per-tenant approach (for extreme isolation)

For customers with strict compliance requirements, create a separate table per tenant. This gives full isolation (separate segments, servers, retention) but increases operational complexity. Use this only when regulatory requirements demand it.

## Table configuration

```json
{
  "tableName": "saas_events",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "eventTimestamp",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "90",
    "replication": "2",
    "segmentPushType": "APPEND"
  },
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "sortedColumn": ["tenantId"],
    "invertedIndexColumns": ["eventType", "feature", "plan"],
    "rangeIndexColumns": ["eventTimestamp"],
    "noDictionaryColumns": ["userId"],
    "bloomFilterColumns": ["tenantId"],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "saas-events",
      "stream.kafka.broker.list": "kafka:9092",
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "realtime.segment.flush.threshold.rows": "500000",
      "realtime.segment.flush.threshold.time": "6h"
    }
  },
  "tenants": {
    "broker": "SharedTenant",
    "server": "SharedTenant"
  },
  "metadata": {}
}
```

### Why `tenantId` is the sorted column

When `tenantId` is the sorted column, all rows for a single tenant are physically adjacent in each segment. This means a `WHERE tenantId = 'acme'` filter skips entire data pages without scanning, giving near-instant segment pruning. If a different column is a better sort key for your queries, use an inverted index on `tenantId` instead.

## Infrastructure isolation with Pinot tenants

### Assigning servers to tenants

Tag servers when adding them to the cluster:

```
PUT /instances/Server_host1_8098
{
  "host": "host1",
  "port": "8098",
  "type": "SERVER",
  "tags": ["PremiumTenant_REALTIME", "PremiumTenant_OFFLINE"]
}
```

Then assign high-value customers' tables to the `PremiumTenant`:

```json
"tenants": {
  "broker": "PremiumTenant",
  "server": "PremiumTenant"
}
```

Other customers share a `SharedTenant` pool. See [Tenant](../basics/components/cluster/tenant.md) for setup details.

### Workload-based query isolation

For finer-grained control within a shared tenant, use workload-based query resource isolation to limit CPU and memory per workload class:

```json
{
  "workloadConfig": {
    "workloads": {
      "free_tier": {
        "maxQueriesPerSecond": 10,
        "maxServerThreads": 2
      },
      "enterprise": {
        "maxQueriesPerSecond": 100,
        "maxServerThreads": 8
      }
    }
  }
}
```

The application backend sets the workload class in the query option:

```sql
SET workload = 'free_tier';
SELECT ...
```

See [Workload-Based Query Resource Isolation](../operate-pinot/tuning/workload-query-isolation.md) for configuration details.

### Broker-level query quotas

Apply per-table query rate limits at the broker to prevent any single tenant from monopolizing query resources:

```json
{
  "quotas": {
    "maxQueriesPerSecond": 50
  }
}
```

See [Query Quotas](../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md).

## Data isolation (row-level security)

Pinot has built-in row-level security (RLS) at the broker. You can configure per-principal, per-table filter predicates so Pinot rewrites incoming SQL queries before execution. This is the preferred enforcement point when the tenant policy maps cleanly to broker-authenticated principals.

### Implementation pattern

For Pinot-managed enforcement, define tenant-scoped RLS filters in broker access-control config:

```properties
pinot.broker.access.control.principals=tenant_app
pinot.broker.access.control.principals.tenant_app.password=verysecret
pinot.broker.access.control.principals.tenant_app.tables=events
pinot.broker.access.control.principals.tenant_app.events.rls=tenantId='tenant_123'
```

If your application needs to derive filters dynamically at request time, you can still enforce tenant filtering in the application layer that sits between the user and the Pinot broker. In that model, your application backend should:

1. Authenticate the user and determine their `tenantId`.
2. Inject `AND tenantId = '<tenantId>'` into every SQL query before sending it to the Pinot broker.
3. Never expose the Pinot broker directly to end users.

Example backend pseudocode:

```python
def query_pinot(user_query: str, tenant_id: str) -> dict:
    # Parse and inject tenant filter
    safe_query = inject_tenant_filter(user_query, tenant_id)
    # Send to Pinot broker
    return pinot_client.execute(safe_query)

def inject_tenant_filter(query: str, tenant_id: str) -> str:
    # Use a SQL parser to safely inject the filter
    # Never string-concatenate user input directly
    parsed = parse_sql(query)
    parsed.add_where_clause(f"tenantId = '{escape(tenant_id)}'")
    return parsed.to_sql()
```

{% hint style="warning" %}
Always use a SQL parser to inject the tenant filter. String concatenation is vulnerable to SQL injection. Validate that the rewritten query still contains the tenant filter before executing.
{% endhint %}

### Validating isolation

Write integration tests that:

1. Query with tenant A's filter and verify no tenant B data is returned.
2. Attempt queries without a tenant filter and verify they are rejected by your backend.
3. Attempt SQL injection in the tenant ID field and verify it is blocked.

## Query patterns

### Per-tenant dashboard aggregation

```sql
SELECT
  DATETRUNC('hour', eventTimestamp, 'MILLISECONDS') AS hour,
  eventType,
  COUNT(*) AS event_count,
  SUM(durationMs) AS total_duration
FROM saas_events
WHERE tenantId = 'acme'
  AND eventTimestamp > ago('PT24H')
GROUP BY hour, eventType
ORDER BY hour
LIMIT 1000
```

### Cross-tenant admin query (internal analytics)

For your own internal dashboards, query without the tenant filter:

```sql
SELECT tenantId, COUNT(*) AS events, SUM(count) AS total_actions
FROM saas_events
WHERE eventTimestamp > ago('PT1H')
GROUP BY tenantId
ORDER BY events DESC
LIMIT 100
```

Restrict access to this query pattern to internal admin users only.

## Operational checklist

### Before go-live

- [ ] Verify that `tenantId` is always present in every event. Null `tenantId` values bypass row-level filtering.
- [ ] Confirm the application backend injects the tenant filter for every query path — REST API, WebSocket, batch exports.
- [ ] Load test with realistic per-tenant query rates. Ensure workload isolation caps prevent cascading slowdowns.
- [ ] If using the single-table model, verify that `tenantId` as the sorted column delivers good pruning by running `EXPLAIN PLAN`.

### Monitoring

- **Per-tenant query rate**: Track via broker metrics, broken down by the `workload` query option. Alert if any tenant exceeds its quota.
- **Query latency by tenant**: A spike for one tenant without an overall spike indicates that tenant's query pattern changed (e.g., missing time filter).
- **Segment size per tenant**: If one tenant dominates the data volume, consider moving them to a dedicated tenant/server pool.

### Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Tenant filter missing on one API endpoint | Add a centralized query middleware that rejects any query without `tenantId` in the WHERE clause |
| One tenant's heavy queries slow everyone | Use workload isolation and per-table query quotas. Move the heavy tenant to a dedicated server tenant |
| Sorted column on `tenantId` hurts time-range queries | Use inverted index on `tenantId` instead, and keep time as the sorted column if time-range performance is more critical |
| Tenant data leaks via JOIN queries | If using multi-stage queries with JOINs, ensure the tenant filter is applied to both sides of the JOIN |

## Further reading

- [Tenant](../basics/components/cluster/tenant.md)
- [Workload-Based Query Resource Isolation](../operate-pinot/tuning/workload-query-isolation.md)
- [Query Quotas](../build-with-pinot/querying-and-sql/query-execution-controls/query-quotas.md)
- [Routing](../operate-pinot/tuning/routing.md)
- [Access Control](../operate-pinot/access-control.md)
