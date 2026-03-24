---
description: Pinot controller API reference.
---

# Controller API Examples

The controller exposes the administrative API surface for cluster, schema, table, segment, tenant, and database operations. The detailed request and response examples live here instead of in the user guide so the reference tree can act as the canonical endpoint index.

## Endpoint Families

| Family | Representative endpoints |
| --- | --- |
| Cluster | `GET /cluster/configs`, `POST /cluster/configs`, `DELETE /cluster/configs/{configName}`, `GET /cluster/info` |
| Health and leadership | `GET /health`, `GET /leader/tables` |
| Schema | `GET /schemas`, `GET /schemas/{schemaName}`, `POST /schemas`, `PUT /schemas/{schemaName}`, `DELETE /schemas/{schemaName}` |
| Table | `GET /tables`, `POST /tables`, `PUT /tables/{tableName}`, `DELETE /tables/{tableName}`, `POST /tableConfigs/validate` |
| Logical tables | `GET /logicalTables`, `POST /logicalTables`, `PUT /logicalTables/{tableName}`, `DELETE /logicalTables/{tableName}` |
| Segments | `GET /segments/{tableName}`, `POST /segments`, `POST /segments/{tableName}/{segmentName}/reload`, `DELETE /segments/{tableName}` |
| Tenant and instance management | `GET /tenants`, `GET /tenants/{tenantName}`, `GET /instances`, `POST /instances` |

## Swagger UI

The controller hosts the interactive Swagger UI at `http://<controller-host>:<port>/help`. Use it to confirm exact request shapes before issuing destructive calls.

## Operational Examples

```bash
curl -X GET "http://localhost:9000/cluster/configs" -H "accept: application/json"
```

```bash
curl -X DELETE "http://localhost:9000/tables/baseballStats?retention=0d" -H "accept: application/json"
```

```bash
curl -X GET "http://localhost:9000/schemas/baseballStats" -H "accept: application/json"
```

## What this page covered

- The controller endpoint families and their top-level responsibilities.
- The interactive Swagger UI location.
- A few representative request examples for the most common admin flows.

## Next step

If you are about to modify cluster state, use the Swagger UI or the original controller examples page to confirm parameters before running the request.

## Related pages

- [API Reference](README.md)
- [Controller Admin API](controller-admin-api.md)
- [Broker Query API](query-api.md)
- [Broker gRPC API](broker-grpc-api.md)
