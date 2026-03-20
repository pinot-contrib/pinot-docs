---
description: Comprehensive reference for all Apache Pinot APIs organized by functional area.
---

# API Reference

Apache Pinot exposes REST APIs on the controller (default port 9000) and broker (default port 8099) for querying data, managing schemas and tables, operating segments, and administering the cluster. The controller also hosts an interactive Swagger UI at `http://<controller-host>:<port>/help` where you can explore and test every endpoint.

This page provides a categorized overview of the most commonly used APIs. Each section lists key endpoints with their HTTP method and path, along with links to detailed documentation.

## Query APIs

Pinot supports querying through HTTP REST endpoints on the broker and an optional gRPC interface. All query endpoints accept standard SQL.

| Method | Endpoint | Component | Description |
| ------ | -------- | --------- | ----------- |
| `POST` | `/query/sql` | Broker | Primary query endpoint for single-stage SQL queries |
| `POST` | `/query` | Broker | Multi-stage query engine endpoint (supports JOINs and other advanced SQL) |
| `POST` | `/query/sql?getCursor=true` | Broker | Submit a query and receive results as a cursor for paginated retrieval |
| `GET`  | `/responseStore/{requestId}/results` | Broker | Fetch a page of results from a cursor-based query |
| `GET`  | `/responseStore/{requestId}` | Broker | Get metadata for a stored cursor response |
| `DELETE` | `/responseStore/{requestId}` | Broker | Delete a stored cursor response |

**Detailed docs:**

* [Broker Query API](querying-pinot-using-standard-sql/README.md) -- REST and CLI query examples, response format
* [Query Response Format](querying-pinot-using-standard-sql/response-format.md)
* [Query using Cursors](../user-guide-query/query-using-cursors.md) -- paginated result retrieval with the ResponseStore API
* [Broker gRPC API](broker-grpc-api.md) -- high-throughput gRPC query interface with compression and Arrow encoding

## Schema Management

Schemas define the columns, data types, and field classifications (dimension, metric, date-time) for Pinot tables. Schema APIs are served by the controller.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/schemas` | List all schema names in the cluster |
| `GET`    | `/schemas/{schemaName}` | Get a schema by name |
| `POST`   | `/schemas` | Create a new schema |
| `PUT`    | `/schemas/{schemaName}` | Update an existing schema |
| `DELETE` | `/schemas/{schemaName}` | Delete a schema (fails if a table still references it) |
| `POST`   | `/schemas/validate` | Validate a schema without creating it |

**Detailed docs:**

* [Controller API Reference](controller-api-reference.md#delete-schemas-less-than-schemaname-greater-than) -- delete schema details

## Table Management

Table APIs let you create, configure, and manage both OFFLINE and REALTIME tables. These endpoints are served by the controller.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/tables` | List all tables in the cluster |
| `GET`    | `/tables/{tableName}` | Get table configuration |
| `POST`   | `/tables` | Create a new table |
| `PUT`    | `/tables/{tableName}` | Update table configuration |
| `DELETE` | `/tables/{tableName}` | Delete a table (supports `retention` parameter, e.g. `retention=0d` for immediate deletion) |
| `POST`   | `/tableConfigs/validate` | Validate a table config with cluster-aware checks (tenant, minion, active tasks) |
| `GET`    | `/tables/{tableName}/state` | Get table state (enabled/disabled) |
| `GET`    | `/tables/{tableName}/size` | Get table storage size |
| `GET`    | `/tables/{tableName}/idealstate` | Get table ideal state (supports `segmentNames` filter) |
| `GET`    | `/tables/{tableName}/externalview` | Get table external view (supports `segmentNames` filter) |
| `POST`   | `/tables/{tableName}/rebalance` | Trigger table rebalance (supports `dryRun`, `preChecks`, `minimizeDataMovement`) |

### Logical Tables

Logical tables provide a unified view over multiple physical tables with UNION semantics.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/logicalTables` | List all logical table names |
| `GET`    | `/logicalTables/{tableName}` | Get logical table configuration |
| `POST`   | `/logicalTables` | Create a logical table |
| `PUT`    | `/logicalTables/{tableName}` | Update a logical table |
| `DELETE` | `/logicalTables/{tableName}` | Delete a logical table (does not delete underlying physical tables) |

**Detailed docs:**

* [Controller API Reference](controller-api-reference.md) -- table delete, rebalance, validation, and logical table details
* [Controller Admin API](pinot-rest-admin-interface.md) -- walkthrough of the Swagger UI for table and schema operations

## Segment Management

Segments are the fundamental data storage units in Pinot. These controller APIs let you upload, list, reload, and delete segments.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/segments/{tableName}` | List all segments for a table |
| `GET`    | `/segments/{tableName}/metadata` | Get metadata for all segments |
| `GET`    | `/segments/{tableName}/{segmentName}/metadata` | Get metadata for a specific segment |
| `POST`   | `/segments` | Upload a segment (multipart form data) |
| `POST`   | `/segments?downloadUri=...` | Upload a segment from a URI |
| `POST`   | `/segments/{tableName}/{segmentName}/reload` | Reload a specific segment |
| `POST`   | `/segments/{tableName}/reload` | Reload all segments for a table |
| `DELETE` | `/segments/{tableName}/{segmentName}` | Delete a specific segment |
| `DELETE` | `/segments/{tableName}` | Delete all segments for a table (use with `type` parameter) |
| `GET`    | `/segments/{tableName}/{segmentName}` | Download a segment |
| `GET`    | `/segments/{tableName}/crc` | Get CRC values for all segments |
| `GET`    | `/tables/{tableName}/badSegments` | List bad segments grouped by partition |

## Cluster Management

These controller APIs manage cluster-wide configuration, tenants, instances, and leadership.

### Cluster Configuration

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/cluster/configs` | List all cluster-level configs |
| `POST`   | `/cluster/configs` | Add or update cluster configs |
| `DELETE` | `/cluster/configs/{configName}` | Delete a cluster config |
| `GET`    | `/cluster/info` | Get cluster name and metadata |

### Tenant Management

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/tenants` | List all tenants |
| `GET`    | `/tenants/{tenantName}` | Get tenant details |
| `POST`   | `/tenants` | Create a new tenant |
| `PUT`    | `/tenants/{tenantName}` | Update a tenant |
| `DELETE` | `/tenants/{tenantName}` | Delete a tenant |
| `GET`    | `/tenants/{tenantName}/tables` | List tables for a tenant (supports `withTableProperties`) |

### Instance Management

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/instances` | List all instances |
| `GET`    | `/instances/{instanceName}` | Get instance details |
| `POST`   | `/instances` | Add a new instance |
| `PUT`    | `/instances/{instanceName}` | Update instance tags or configuration |
| `DELETE` | `/instances/{instanceName}` | Remove an instance |

### Leadership

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/leader/tables` | Get leader-to-table mapping for all resources |
| `GET`    | `/leader/tables/{tableName}` | Get leader info for a specific table |

**Detailed docs:**

* [Controller API Reference](controller-api-reference.md) -- cluster config, leader, and tenant API details

## Task Management

Pinot uses a minion-based task framework for background operations such as segment merge, purge, and conversion. These controller APIs manage task scheduling and monitoring.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/tasks/taskqueues` | List all task queues |
| `GET`    | `/tasks/taskqueue/{taskType}/state` | Get the state of a task queue |
| `PUT`    | `/tasks/taskqueue/{taskType}` | Start, stop, or resume a task queue |
| `POST`   | `/tasks/schedule` | Schedule tasks for all tables |
| `POST`   | `/tasks/schedule?tableName={tableName}` | Schedule tasks for a specific table |
| `GET`    | `/tasks/{taskType}/{tableNameWithType}/state` | Get task states for a table |
| `GET`    | `/tasks/{taskType}/{tableNameWithType}/metadata` | Get task metadata |
| `PUT`    | `/tasks/schedulerJobDetails` | Get cron scheduler job details |
| `DELETE` | `/tasks/taskqueue/{taskType}` | Clean up a finished task queue |

## Data Ingestion

These controller APIs allow you to ingest data from files or URIs into existing tables.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST`   | `/ingestFromFile` | Ingest data from an uploaded file into a table |
| `POST`   | `/ingestFromURI` | Ingest data from a remote URI into a table |

### Real-time Ingestion Control

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `POST`   | `/tables/{tableName}/pauseConsumption` | Pause real-time consumption for a table |
| `POST`   | `/tables/{tableName}/resumeConsumption` | Resume real-time consumption |
| `GET`    | `/tables/{tableName}/pauseStatus` | Get pause status for a table |
| `POST`   | `/tables/{tableName}/removeIngestionMetrics` | Remove stale ingestion metrics |

## Application Quotas

Application-level query quotas limit the queries per second (QPS) for different applications connecting to Pinot. Applications are identified by the `applicationName` query option.

| Method | Endpoint | Description |
| ------ | -------- | ----------- |
| `GET`    | `/applicationQuotas` | List all application QPS quotas |
| `GET`    | `/applicationQuotas/{appName}` | Get quota for a specific application |
| `POST`   | `/applicationQuotas/{appName}` | Create or update an application quota |

**Detailed docs:**

* [Controller API Reference](controller-api-reference.md#application-quotas) -- full request/response examples
* [Query Quotas](../user-guide-query/query-quotas.md) -- how application quotas interact with table and database quotas

## Monitoring and Debugging

These endpoints help you check the health of Pinot components and debug table-level issues.

| Method | Endpoint | Component | Description |
| ------ | -------- | --------- | ----------- |
| `GET`  | `/health` | Controller, Broker, Server | Health check (returns `OK` or error) |
| `GET`  | `/debug/tables/{tableName}` | Controller | Debug info including segment status, ingestion state, and server/broker health |
| `GET`  | `/debug/serverRoutingStats` | Controller | Server routing statistics |
| `GET`  | `/responseStore` | Broker | List all active cursor response stores |
| `GET`  | `/tables/{tableName}/size` | Controller | Table storage size (reported and estimated) |
| `GET`  | `/version` | Controller | Pinot version information |

## Additional Resources

* **Swagger UI**: Access the full interactive API documentation at `http://<controller-host>:<port>/help`
* [Controller Admin API](pinot-rest-admin-interface.md) -- visual walkthrough of the admin interface
* [Controller API Reference](controller-api-reference.md) -- detailed request/response examples for many endpoints
* [External Clients](../clients/README.md) -- JDBC, Java, and Go client libraries for programmatic access
