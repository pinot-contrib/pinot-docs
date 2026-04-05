---
description: Use the Pinot Java admin client to call controller REST APIs from JVM code.
---

# Java admin client

The Pinot Java admin client is the controller-facing half of `org.apache.pinot:pinot-java-client`. Use it when JVM code needs to create or validate schemas and tables, inspect or reset segments, manage tenants and instances, or inspect Minion task state through the controller REST API.

Unlike the [Java query client](java.md), the admin client does not talk to brokers. Its entry point is `org.apache.pinot.client.admin.PinotAdminClient`, and it is constructed with a controller address such as `localhost:9000`.

## Installation

The admin client ships in the same artifact as the Java query client.

{% tabs %}
{% tab title="Maven" %}
```xml
<dependency>
  <groupId>org.apache.pinot</groupId>
  <artifactId>pinot-java-client</artifactId>
  <version>1.4.0</version>
</dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```groovy
implementation "org.apache.pinot:pinot-java-client:1.4.0"
```
{% endtab %}
{% endtabs %}

## Basic usage

Create the admin client against a controller, then grab the service client for the controller surface you need:

```java
import org.apache.pinot.client.admin.PinotAdminClient;

try (PinotAdminClient adminClient = new PinotAdminClient("localhost:9000")) {
  var tables = adminClient.getTableClient().listTables(null, null, null);
  var schemas = adminClient.getSchemaClient().listSchemaNames();
  var instances = adminClient.getInstanceClient().listInstances();
  var tenants = adminClient.getTenantClient().listTenants();
  var taskTypes = adminClient.getTaskClient().listTaskTypes();
}
```

## Available service clients

`PinotAdminClient` lazily exposes typed controller clients for the major admin surfaces:

| Method | Scope |
| --- | --- |
| `getTableClient()` | Table CRUD, table status, rebalance, validation, and related controller operations |
| `getSchemaClient()` | Schema CRUD and validation |
| `getInstanceClient()` | Instance listing, creation, config updates, and enable/disable state |
| `getSegmentClient()` | Segment listing, metadata, CRCs, reset, and delete operations |
| `getSegmentApiClient()` | Segment-selection APIs such as time-range segment selection and direct segment metadata lookup |
| `getTenantClient()` | Tenant CRUD, metadata, and tenant rebalance helpers |
| `getTaskClient()` | Task types, queue state, task metadata, task debug, and task state inspection |

Example:

```java
String schemaConfig =
    "{\"schemaName\":\"mySchema\",\"dimensionFieldSpecs\":[{\"name\":\"id\",\"dataType\":\"INT\"}]}";

try (PinotAdminClient adminClient = new PinotAdminClient("localhost:9000")) {
  String validation = adminClient.getSchemaClient().validateSchema(schemaConfig);
  String createResult = adminClient.getSchemaClient().createSchema(schemaConfig);
}
```

## Authentication

The admin client supports `NONE`, `BASIC`, `BEARER`, and `CUSTOM` authentication modes through `PinotAdminAuthentication.AuthType`.

Basic auth:

```java
import java.util.Map;
import java.util.Properties;
import org.apache.pinot.client.admin.PinotAdminAuthentication;
import org.apache.pinot.client.admin.PinotAdminClient;

Properties properties = new Properties();
properties.setProperty("pinot.admin.request.timeout.ms", "30000");

try (PinotAdminClient adminClient = new PinotAdminClient(
    "localhost:9000",
    properties,
    PinotAdminAuthentication.AuthType.BASIC,
    Map.of("username", "admin", "password", "password"))) {
  String tableConfig = adminClient.getTableClient().getTableConfig("myTable");
}
```

Bearer auth:

```java
try (PinotAdminClient adminClient = new PinotAdminClient(
    "localhost:9000",
    new Properties(),
    PinotAdminAuthentication.AuthType.BEARER,
    Map.of("token", "your-bearer-token"))) {
  var liveInstances = adminClient.getInstanceClient().listLiveInstances();
}
```

For `CUSTOM`, pass the header map you want sent to the controller.

## Transport settings

The admin transport reads its settings from the `Properties` object you pass to `PinotAdminClient`:

| Property | Default | Effect |
| --- | --- | --- |
| `pinot.admin.request.timeout.ms` | `60000` | Request timeout used for synchronous calls and the async HTTP client's request and read timeouts |
| `pinot.admin.scheme` | `http` | Controller scheme. Set this to `https` for TLS-enabled controllers |

The current transport implementation uses a fixed 10-second connect timeout and enables the JVM default SSL context when `pinot.admin.scheme=https`.

## Async operations and exceptions

The admin package includes asynchronous variants for many controller operations, such as `listTablesAsync`, `listSchemaNamesAsync`, `listInstancesAsync`, `listTenantsAsync`, `listTaskTypesAsync`, and segment-admin async methods. These return `CompletableFuture` and use the same transport configuration as the synchronous methods.

The main exception types are:

- `PinotAdminException` for general controller or transport failures
- `PinotAdminAuthenticationException` for invalid auth configuration or auth failures
- `PinotAdminNotFoundException` when the requested controller resource does not exist
- `PinotAdminValidationException` when Pinot rejects the submitted config or request

## Segment API helper

`PinotSegmentApiClient` is separate from `PinotSegmentAdminClient`. Use it for controller endpoints that are closer to segment-selection workflows than to segment CRUD, including time-range segment selection.

```java
try (PinotAdminClient adminClient = new PinotAdminClient("localhost:9000")) {
  var selection = adminClient.getSegmentApiClient()
      .selectSegments("myTable", "OFFLINE", 1709251200000L, 1709337600000L, false);
  var metadata = adminClient.getSegmentApiClient()
      .getSegmentMetadata("myTable_OFFLINE", "myTable_0");
}
```
