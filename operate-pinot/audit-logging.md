# Audit Logging

{% hint style="info" %}
Audit logging is available starting in Apache Pinot 1.3.0. It is disabled by default and can be enabled at runtime without restarting Pinot components.
{% endhint %}

Audit logging records all REST API requests (and optionally responses) made to the controller and broker. Each event is written as a single-line JSON object to a dedicated log file (`pinot-audit.log`), capturing who performed what action, when, and from where. This provides an immutable trail for compliance, security investigations, and operational troubleshooting.

## How it works

Audit logging is implemented as a Jersey request/response filter that intercepts all HTTP calls to the controller and broker admin APIs.

1. A client sends an HTTP request to the controller or broker REST API.
2. The `AuditLogFilter` checks whether audit logging is enabled and whether the request URL matches the configured include/exclude patterns.
3. If the request should be audited, the filter extracts request metadata (endpoint, method, query parameters, headers, body) and resolves the user identity.
4. An `AuditEvent` is serialized as a single-line JSON object and written to the audit log at INFO level.
5. If response auditing is enabled, a second event is emitted after the response is sent, containing the HTTP status code, duration, and a `request_id` that correlates it with the original request event.

Audit logging is designed for graceful degradation -- if any error occurs during audit processing, the error is logged as a warning and the original request proceeds unaffected.

## Supported components

| Component | Audit logging support |
|-----------|----------------------|
| **Controller** | Supported |
| **Broker** | Supported |
| **Server** | Not yet supported |
| **Minion** | Not yet supported |

## Configuration

All audit logging configuration is stored in the ZooKeeper cluster config and can be updated at runtime via the controller REST API (`PUT /cluster/configs`). Changes take effect immediately on the next request -- no restart is required.

Configuration keys use a component-specific prefix:

```
pinot.audit.<component>.<setting>
```

Where `<component>` is `controller` or `broker`.

### Enable audit logging

```properties
# Enable audit logging on the controller
pinot.audit.controller.enabled=true

# Enable audit logging on the broker
pinot.audit.broker.enabled=true
```

### Configuration reference

{% tabs %}
{% tab title="Controller" %}

| Property | Default | Description |
|----------|---------|-------------|
| `pinot.audit.controller.enabled` | `false` | Enable or disable audit logging |
| `pinot.audit.controller.capture.request.payload.enabled` | `false` | Capture request body content |
| `pinot.audit.controller.request.payload.size.max.bytes` | `8192` | Maximum request body size to capture (absolute max: 65536) |
| `pinot.audit.controller.capture.request.headers` | _(empty)_ | Comma-separated list of headers to capture (allow-list) |
| `pinot.audit.controller.capture.response.enabled` | `false` | Emit a second audit event with response code and duration |
| `pinot.audit.controller.url.filter.include.patterns` | _(empty)_ | Comma-separated URL patterns to audit (allowlist; if empty, all URLs are audited) |
| `pinot.audit.controller.url.filter.exclude.patterns` | _(empty)_ | Comma-separated URL patterns to exclude from auditing (takes precedence over includes) |
| `pinot.audit.controller.userid.header` | _(empty)_ | HTTP header containing the user identity |
| `pinot.audit.controller.userid.jwt.claim` | _(empty)_ | JWT claim to extract as user identity (falls back to `sub`) |
| `pinot.audit.controller.token.resolver.class` | _(empty)_ | Fully qualified class name of a custom `AuditTokenResolver` implementation |

{% endtab %}
{% tab title="Broker" %}

| Property | Default | Description |
|----------|---------|-------------|
| `pinot.audit.broker.enabled` | `false` | Enable or disable audit logging |
| `pinot.audit.broker.capture.request.payload.enabled` | `false` | Capture request body content |
| `pinot.audit.broker.request.payload.size.max.bytes` | `8192` | Maximum request body size to capture (absolute max: 65536) |
| `pinot.audit.broker.capture.request.headers` | _(empty)_ | Comma-separated list of headers to capture (allow-list) |
| `pinot.audit.broker.capture.response.enabled` | `false` | Emit a second audit event with response code and duration |
| `pinot.audit.broker.url.filter.include.patterns` | _(empty)_ | Comma-separated URL patterns to audit (allowlist; if empty, all URLs are audited) |
| `pinot.audit.broker.url.filter.exclude.patterns` | _(empty)_ | Comma-separated URL patterns to exclude from auditing (takes precedence over includes) |
| `pinot.audit.broker.userid.header` | _(empty)_ | HTTP header containing the user identity |
| `pinot.audit.broker.userid.jwt.claim` | _(empty)_ | JWT claim to extract as user identity (falls back to `sub`) |
| `pinot.audit.broker.token.resolver.class` | _(empty)_ | Fully qualified class name of a custom `AuditTokenResolver` implementation |

{% endtab %}
{% endtabs %}

### Enabling at runtime

Use the controller REST API to enable audit logging without restarting any component:

```bash
# Enable audit logging on the controller
curl -X PUT "http://localhost:9000/cluster/configs" \
  -H "Content-Type: application/json" \
  -d '{"pinot.audit.controller.enabled": "true"}'

# Enable audit logging on the broker with request body capture
curl -X PUT "http://localhost:9000/cluster/configs" \
  -H "Content-Type: application/json" \
  -d '{
    "pinot.audit.broker.enabled": "true",
    "pinot.audit.broker.capture.request.payload.enabled": "true"
  }'
```

## Log format

Audit events are written as newline-delimited JSON (ndjson) to the `pinot-audit.log` file. Each line is a self-contained JSON object.

### Request event

```json
{
  "timestamp": "2025-09-01T12:00:00Z",
  "service_id": null,
  "endpoint": "/tables/myTable",
  "method": "POST",
  "origin_ip_address": null,
  "user_id": {
    "principal": "alice@example.com"
  },
  "request": {
    "query_params": {
      "type": "OFFLINE"
    },
    "headers": {
      "Content-Type": "application/json"
    },
    "body": "{\"tableName\": \"myTable\", ...}"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response event

When `capture.response.enabled` is `true`, a second event is emitted:

```json
{
  "timestamp": "2025-09-01T12:00:01Z",
  "endpoint": "/tables/myTable",
  "method": "POST",
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "response_code": 200,
  "duration_ms": 342
}
```

The `request_id` field links request and response events for the same API call.

### Event fields

| Field | Type | Present in | Description |
|-------|------|-----------|-------------|
| `timestamp` | String (ISO-8601) | Request, Response | Time the event was recorded |
| `service_id` | String | Request | Identifier of the Pinot component (not yet implemented) |
| `endpoint` | String | Request, Response | URL path of the API call |
| `method` | String | Request, Response | HTTP method (GET, POST, PUT, DELETE, etc.) |
| `origin_ip_address` | String | Request | Client IP address (not yet implemented) |
| `user_id` | Object | Request | Contains `principal` -- the resolved user identity |
| `request` | Object | Request | Contains `query_params`, `headers`, `body`, and `error` |
| `request_id` | String (UUID) | Request, Response | Unique identifier linking request and response events |
| `response_code` | Integer | Response | HTTP response status code |
| `duration_ms` | Long | Response | Request processing time in milliseconds |

## URL filtering

URL patterns control which API endpoints are audited. Patterns use Java NIO `PathMatcher` syntax and support both glob and regex.

### Pattern syntax

| Syntax | Example | Matches |
|--------|---------|---------|
| Glob (default) | `/tables/**` | All paths under `/tables/` |
| Glob wildcard | `/tables/*/segments` | `/tables/myTable/segments` |
| Character class | `/tables/[a-z]*` | Tables starting with lowercase letter |
| Alternatives | `/tables/{myTable,otherTable}` | Specific table names |
| Regex | `regex:/api/v[0-9]+/.*` | Prefix with `regex:` for full regex |

### Include and exclude rules

- If an endpoint matches any **exclude** pattern, it is **not** audited (exclude always takes precedence).
- If **include** patterns are defined and the endpoint does not match any, it is **not** audited (include acts as an allowlist).
- If no include patterns are defined, all endpoints are audited (subject to excludes).

```properties
# Only audit table and schema management APIs on the controller
pinot.audit.controller.url.filter.include.patterns=/tables/**,/schemas/**

# Exclude health check and metrics endpoints
pinot.audit.controller.url.filter.exclude.patterns=/health,/metrics

# Audit all broker queries except internal debug endpoints
pinot.audit.broker.url.filter.include.patterns=/query/**
pinot.audit.broker.url.filter.exclude.patterns=/debug/**
```

## User identity resolution

The audit logger resolves user identity using the following priority (first match wins):

1. **Custom header** -- if `userid.header` is configured, the value of that HTTP header is used as the principal.
2. **Custom SPI resolver** -- if `token.resolver.class` is configured, the class is loaded via Pinot's `PluginManager` and given the `Authorization` header value to resolve.
3. **JWT claim** -- if the request contains a `Bearer` token in the `Authorization` header, the claim specified by `userid.jwt.claim` is extracted. If no claim name is configured, the `sub` (subject) claim is used.

If no identity can be resolved, the `user_id` field is `null`.

### Examples

```properties
# Use a custom header set by an API gateway or reverse proxy
pinot.audit.controller.userid.header=X-User-Email

# Extract the "email" claim from JWT tokens
pinot.audit.broker.userid.jwt.claim=email
```

### Custom token resolver (SPI)

For non-JWT authentication schemes, implement the `AuditTokenResolver` interface:

```java
import org.apache.pinot.spi.audit.AuditTokenResolver;
import org.apache.pinot.spi.audit.AuditUserIdentity;

public class MyTokenResolver implements AuditTokenResolver {
    @Override
    public AuditUserIdentity resolve(String authHeaderValue) {
        // Parse your custom token format
        String userId = parseToken(authHeaderValue);
        return userId != null ? () -> userId : null;
    }
}
```

Configure the resolver class:

```properties
pinot.audit.controller.token.resolver.class=com.example.MyTokenResolver
```

The resolver is loaded via `PluginManager` and cached. If loading fails, the system falls back to JWT parsing.

## Request body capture

When `capture.request.payload.enabled` is `true`, the request body is included in the audit event.

- The maximum captured body size is controlled by `request.payload.size.max.bytes` (default: 8192 bytes, absolute maximum: 65536 bytes).
- If the body exceeds the configured limit, it is truncated and `...[truncated]` is appended.
- The request body stream is buffered and reset so that downstream handlers can still read it.

```properties
# Capture request payloads up to 16 KB
pinot.audit.controller.capture.request.payload.enabled=true
pinot.audit.controller.request.payload.size.max.bytes=16384
```

{% hint style="warning" %}
Enabling request body capture may log sensitive data such as query text, table configurations, or schema definitions. Ensure your audit log storage meets your organization's data handling requirements.
{% endhint %}

## Header capture

By default, no request headers are logged. Configure an allow-list of header names to capture:

```properties
# Capture specific headers (case-insensitive, comma-separated)
pinot.audit.controller.capture.request.headers=Content-Type,X-Request-ID,Authorization
```

Only headers in the allow-list appear in the audit event. Headers not in the list are omitted.

{% hint style="warning" %}
Be cautious when capturing the `Authorization` header, as it may contain credentials or tokens.
{% endhint %}

## Log file configuration

The audit log is written via SLF4J to the logger named `org.apache.pinot.audit`. The default Log4j2 configuration writes to a dedicated rolling file:

| Setting | Value |
|---------|-------|
| Log file | `${LOG_ROOT}/pinot-audit.log` |
| Roll pattern | Daily and size-based (19.5 MB per file) |
| Retention | Up to 10 rolled files |
| Format | `%m%n` (pure JSON, no timestamp prefix) |
| Log level | Controlled by `AUDIT_LOG_LEVEL` env var (default: `info`) |
| Additivity | `false` (audit events do not propagate to the root Pinot logger) |

The Log4j2 configuration in `pinot-tools/src/main/resources/log4j2.xml`:

```xml
<RollingFile name="auditLog" fileName="${env:LOG_ROOT}/pinot-audit.log"
             filePattern="${env:LOG_ROOT}/audit-%d{yyyy-MM-dd}-%i.log"
             immediateFlush="false">
  <PatternLayout pattern="%m%n"/>
  <Policies>
    <SizeBasedTriggeringPolicy size="19500KB"/>
    <TimeBasedTriggeringPolicy/>
  </Policies>
  <DefaultRolloverStrategy max="10"/>
</RollingFile>

<Logger name="org.apache.pinot.audit" level="${env:AUDIT_LOG_LEVEL:-info}" additivity="false">
  <AppenderRef ref="auditLog"/>
</Logger>
```

You can customize the log output (e.g., ship to a SIEM or centralized logging system) by modifying the Log4j2 configuration or adding additional appenders.

## Metrics

Audit logging exposes the following metrics on both the controller and broker:

| Metric | Type | Description |
|--------|------|-------------|
| `AUDIT_REQUEST_PROCESSING_TIME` | Timer | Time spent processing the request-phase audit filter |
| `AUDIT_RESPONSE_PROCESSING_TIME` | Timer | Time spent processing the response-phase audit filter |
| `AUDIT_REQUEST_FAILURES` | Meter | Number of exceptions during request audit processing |
| `AUDIT_RESPONSE_FAILURES` | Meter | Number of exceptions during response audit processing |
| `AUDIT_REQUEST_PAYLOAD_TRUNCATED` | Meter | Number of request bodies truncated due to size limits |

Use these metrics to monitor audit logging overhead and detect failures. See [Metrics and Monitoring](monitoring.md) for general guidance on Pinot metrics.

## What gets audited

Since audit logging is implemented as a Jersey filter, it covers **all REST API calls** to the controller and broker. This includes:

| Category | Example endpoints |
|----------|-------------------|
| Table management | `POST /tables`, `PUT /tables/{name}`, `DELETE /tables/{name}` |
| Schema management | `POST /schemas`, `PUT /schemas/{name}`, `DELETE /schemas/{name}` |
| Segment operations | `POST /segments`, `GET /segments/{table}`, `DELETE /segments/{table}/{segment}` |
| Tenant management | `POST /tenants`, `PUT /tenants`, `DELETE /tenants/{name}` |
| Cluster configuration | `GET /cluster/configs`, `PUT /cluster/configs` |
| Query execution | `POST /query/sql`, `POST /query` (broker) |
| Instance management | `POST /instances`, `PUT /instances/{name}` |

Audit logging does **not** currently cover:

- Internal Helix/ZooKeeper state changes
- Server-side segment loading and query execution
- Minion task execution
- Intra-cluster RPC communication

## Example: full audit setup

A common production configuration that audits all controller management APIs and all broker queries, with request body capture and response correlation:

```properties
# Controller -- audit all management APIs except health checks
pinot.audit.controller.enabled=true
pinot.audit.controller.capture.request.payload.enabled=true
pinot.audit.controller.request.payload.size.max.bytes=16384
pinot.audit.controller.capture.request.headers=Content-Type,X-Request-ID
pinot.audit.controller.capture.response.enabled=true
pinot.audit.controller.url.filter.exclude.patterns=/health,/metrics
pinot.audit.controller.userid.header=X-User-Email

# Broker -- audit all queries
pinot.audit.broker.enabled=true
pinot.audit.broker.capture.request.payload.enabled=true
pinot.audit.broker.capture.response.enabled=true
pinot.audit.broker.url.filter.include.patterns=/query/**
pinot.audit.broker.userid.jwt.claim=email
```

Apply via the cluster config API:

```bash
curl -X PUT "http://localhost:9000/cluster/configs" \
  -H "Content-Type: application/json" \
  -d '{
    "pinot.audit.controller.enabled": "true",
    "pinot.audit.controller.capture.request.payload.enabled": "true",
    "pinot.audit.controller.request.payload.size.max.bytes": "16384",
    "pinot.audit.controller.capture.request.headers": "Content-Type,X-Request-ID",
    "pinot.audit.controller.capture.response.enabled": "true",
    "pinot.audit.controller.url.filter.exclude.patterns": "/health,/metrics",
    "pinot.audit.controller.userid.header": "X-User-Email",
    "pinot.audit.broker.enabled": "true",
    "pinot.audit.broker.capture.request.payload.enabled": "true",
    "pinot.audit.broker.capture.response.enabled": "true",
    "pinot.audit.broker.url.filter.include.patterns": "/query/**",
    "pinot.audit.broker.userid.jwt.claim": "email"
  }'
```

## Performance considerations

- Audit logging runs in the request/response filter chain and adds minimal overhead. Monitor `AUDIT_REQUEST_PROCESSING_TIME` to measure impact.
- Request body capture requires buffering the input stream, which increases memory usage for large payloads. Set `request.payload.size.max.bytes` appropriately for your workload.
- Use URL filtering to reduce log volume by excluding high-frequency, low-value endpoints like health checks and metrics.
- The audit log file uses `immediateFlush=false` for better write performance. Events may be delayed slightly before being flushed to disk.
- Audit failures are swallowed -- they never affect the processing of the original request.

## Verifying audit logging

To confirm audit logging is working:

1. Enable audit logging via the cluster config API.
2. Make a REST API call to the controller or broker.
3. Check the `pinot-audit.log` file in the log directory:

```bash
# View recent audit events
tail -f ${LOG_ROOT}/pinot-audit.log | jq .
```

4. Each line should be a valid JSON object with the fields described in the [Log format](#log-format) section.
5. If response auditing is enabled, you should see paired request and response events with matching `request_id` values.
