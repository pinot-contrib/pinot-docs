# Java

Pinot provides a native Java query client for broker-routed SQL queries. The client is tenant-aware, supports blocking and async execution, and can discover brokers through ZooKeeper or the controller.

For controller REST operations such as table, schema, segment, tenant, instance, or task management, use the [Java admin client](java-admin-client.md).

## Installation

You can use the client by including the following dependency:

{% tabs %}
{% tab title="Maven" %}
```java
<dependency>
    <groupId>org.apache.pinot</groupId>
    <artifactId>pinot-java-client</artifactId>
    <version>1.4.0</version>
</dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```java
include 'org.apache.pinot:pinot-java-client:1.4.0'
```
{% endtab %}
{% endtabs %}

You can also build [the code for java client](https://github.com/apache/pinot/tree/master/pinot-clients/pinot-java-client) locally and use it.

{% hint style="info" %}
Basic authorization is supported in the JDBC and Java clients since Pinot 0.10.0. Make sure you are using client JARs from that release or later.
{% endhint %}

## Usage

Here's an example of how to use `pinot-java-client` to query Pinot.

```java
import org.apache.pinot.client.Connection;
import org.apache.pinot.client.ConnectionFactory;
import org.apache.pinot.client.ResultSetGroup;
import org.apache.pinot.client.ResultSet;

/**
 * Demonstrates the use of pinot-java-client to query Pinot from Java.
 */
public class PinotClientExample {

  public static void main(String[] args) {

    // Pinot connection
    String zkUrl = "localhost:2181";
    String pinotClusterName = "PinotCluster";
    Connection pinotConnection = ConnectionFactory.fromZookeeper(zkUrl + "/" + pinotClusterName);

    String query = "SELECT COUNT(*) FROM myTable GROUP BY foo";
    ResultSetGroup pinotResultSetGroup = pinotConnection.execute(query);
    ResultSet resultTableResultSet = pinotResultSetGroup.getResultSet(0);

    int numRows = resultTableResultSet.getRowCount();
    int numColumns = resultTableResultSet.getColumnCount();
    String columnValue = resultTableResultSet.getString(0, 1);
    String columnName = resultTableResultSet.getColumnName(1);

    System.out.println("ColumnName: " + columnName + ", ColumnValue: " + columnValue);
  }
}
```

## ConnectionFactory

The client provides a `ConnectionFactory` class to create connections to a Pinot cluster. The current source supports the following query-connection patterns:

* **ZooKeeper (recommended)**: `ConnectionFactory.fromZookeeper(...)` dynamically resolves brokers from Helix external view and routes queries by table.
* **Broker list**: `ConnectionFactory.fromHostList(...)` uses a fixed broker list. This is mainly useful for simple deployments, load-balanced brokers, or local testing.
* **Controller address**: `ConnectionFactory.fromController(...)` periodically refreshes broker mappings from the controller instead of watching ZooKeeper directly.
* **Properties object**: `ConnectionFactory.fromProperties(Properties)` reads a `brokerList` property and builds a fixed broker-list connection.

For `fromController(...)` and `fromControllerGrpc(...)`, pass the controller as `host:port`. The client applies `http` or `https` from the `scheme` property.

{% hint style="info" %}
If your Pinot cluster is running inside Kubernetes and you're trying to connect to it from outside Kubernetes, the Zookeeper method will probably return internal host names that can't be resolved.\
\
For Kubernetes deployments, it's therefore recommended to pass in the host-name of a load balancer sitting in front of the brokers.
{% endhint %}

Example:

```java
Properties properties = new Properties();
properties.setProperty("brokerList", "broker-1:8099,broker-2:8099");

Connection zkConnection =
    ConnectionFactory.fromZookeeper("some-zookeeper-server:2181/zookeeperPath/pinot-cluster");

Connection controllerConnection =
    ConnectionFactory.fromController("controller.example.com:9000");

Connection brokerConnection =
    ConnectionFactory.fromHostList("broker-1:8099", "broker-2:8099");

Connection propertiesConnection = ConnectionFactory.fromProperties(properties);
```

## gRPC Connections

The Java client also exposes gRPC broker connections via `ConnectionFactory.fromControllerGrpc(...)`, `fromZookeeperGrpc(...)`, and `fromHostListGrpc(...)`.

```java
Properties properties = new Properties();
properties.setProperty("usePlainText", "false");
properties.setProperty("maxInboundMessageSizeBytes", "134217728");
properties.setProperty("channelKeepAliveTimeSeconds", "60");
properties.setProperty("channelKeepAliveTimeoutSeconds", "20");
properties.setProperty("channelKeepAliveWithoutCalls", "true");
properties.setProperty("channelShutdownTimeoutSeconds", "10");
properties.setProperty("tls.truststore.path", "/path/to/grpc-truststore.jks");
properties.setProperty("tls.truststore.password", "changeit");

GrpcConnection connection = ConnectionFactory.fromControllerGrpc(properties, "localhost:9000");
ResultSetGroup resultSetGroup = connection.execute(
    "SELECT COUNT(*) FROM myTable",
    Map.of("blockRowSize", "10000", "encoding", "JSON", "compression", "ZSTD"));
```

The gRPC transport properties below are read directly from the connection `Properties` through `GrpcConfig`. TLS settings use the `tls.*` namespace, not `pinot.*.tls.*`.

| Property | Default | Notes |
| --- | --- | --- |
| `usePlainText` | `true` | Use plaintext gRPC transport. Set to `false` to enable TLS. |
| `maxInboundMessageSizeBytes` | `134217728` (128 MB) | Maximum inbound gRPC message size accepted by the client. |
| `channelKeepAliveTimeSeconds` | `-1` (disabled) | Keepalive ping interval. Set a positive value to enable keepalive. |
| `channelKeepAliveTimeoutSeconds` | `20` | Timeout waiting for keepalive acknowledgements. |
| `channelKeepAliveWithoutCalls` | `true` | Allows keepalive pings even without active RPCs. |
| `channelShutdownTimeoutSeconds` | `10` | How long the client waits for the gRPC channel to terminate on close. |
| `tls.keystore.type` | JVM default keystore type (`KeyStore.getDefaultType()`) | Client keystore type for mutual TLS. |
| `tls.keystore.path` | None | Client keystore path for mutual TLS. |
| `tls.keystore.password` | None | Client keystore password. |
| `tls.truststore.type` | JVM default keystore type (`KeyStore.getDefaultType()`) | Truststore type used to validate the broker certificate. |
| `tls.truststore.path` | None | Truststore path used to validate the broker certificate. |
| `tls.truststore.password` | None | Truststore password. |
| `tls.ssl.provider` | `JDK` | SSL provider used when building the gRPC client SSL context. |
| `tls.insecure` | `false` | Skip broker certificate verification. Only appropriate for non-production testing. |
| `tls.protocols` | JVM TLS defaults | Comma-separated TLS protocol allowlist such as `TLSv1.2,TLSv1.3`. |

For default metadata such as auth headers, use the `headers.<name>` property prefix. Query-specific gRPC metadata such as `blockRowSize`, `compression`, and `encoding` should be passed in the metadata map for `execute(..., metadataMap)` or `executeGrpc(..., metadataMap)`.

## Query Methods

You can run the query in both blocking as well as async manner. Use

* `Connection.execute(String)` for blocking queries
* `Connection.executeAsync(String)` for asynchronous queries that return a future object.

```java
ResultSetGroup resultSetGroup = 
  connection.execute("select * from foo...");
// OR
Future<ResultSetGroup> futureResultSetGroup = 
  connection.executeAsync("select * from foo...");
```

You can also use `PreparedStatement` to escape query parameters. We don't store the Prepared Statement in the database and hence it won't increase the subsequent query performance.

```java
PreparedStatement statement = 
    connection.prepareStatement("select * from foo where a = ?");
statement.setString(1, "bar");

ResultSetGroup resultSetGroup = statement.execute();
// OR
Future<ResultSetGroup> futureResultSetGroup = statement.executeAsync();
```

`Connection.execute(...)` also has overloads that accept an explicit table name or iterable of table names. Those overloads let the client choose the broker without re-parsing SQL.

## Cursor Pagination

The HTTP transport behind `Connection` implements cursor pagination. Use `openCursor(query, pageSize)` when a query can return a large result set and you want page-by-page navigation instead of loading everything into one response.

```java
try (ResultCursor cursor = connection.openCursor(
    "SELECT playerName, yearID FROM baseballStats ORDER BY yearID", 1000)) {
  CursorResultSetGroup firstPage = cursor.getCurrentPage();

  while (cursor.hasNext()) {
    CursorResultSetGroup nextPage = cursor.next();
    // Process nextPage.getResultSet(...)
  }
}
```

The cursor API supports:

* `getCurrentPage()` to inspect the currently loaded page
* `next()` / `nextAsync()` and `previous()` / `previousAsync()` for navigation
* `seekToPage()` / `seekToPageAsync()` for direct page jumps
* `getCursorId()`, `getCurrentPageNumber()`, `getTotalRows()`, and `isExpired()` for cursor metadata
* `close()` to delete the server-side cursor and free resources

Cursor pagination is available only when the underlying transport implements `CursorCapable`, which the default HTTP transport does.

## Result Set

Results can be obtained with the various getter methods on the first `ResultSet`, obtained through `getResultSet(int)`:

```java
String query = "select foo, bar from baz where quux = 'quuux'";
ResultSetGroup resultSetGroup = connection.execute(query);
ResultSet resultSet = resultSetGroup.getResultSet(0);

for (int i = 0; i < resultSet.getRowCount(); ++i) {
  System.out.println("foo: " + resultSet.getString(i, 0));
  System.out.println("bar: " + resultSet.getInt(i, 1));
}
```

## Authentication

Pinot supports [basic HTTP authorization](../../../operate-pinot/authentication/basic-auth-access-control.md), which can be enabled for your cluster using configuration. To support basic HTTP authorization in your client-side Java applications, make sure you are using Pinot Java Client 0.10.0 or later. The following code snippet shows you how to connect to and query a Pinot cluster that has basic HTTP authorization enabled when using the Java client.

```java
final String username = "admin";
final String password = "verysecret";

// Concatenate username and password and use base64 to encode the concatenated string
String plainCredentials = username + ":" + password;
String base64Credentials = new String(
    Base64.getEncoder().encode(plainCredentials.getBytes()));

String authorizationHeader = "Basic " + base64Credentials;

Map<String, String> headers = new HashMap<>();
headers.put("Authorization", authorizationHeader);
JsonAsyncHttpPinotClientTransportFactory factory = 
    new JsonAsyncHttpPinotClientTransportFactory();
factory.setHeaders(headers);
PinotClientTransport clientTransport = factory
    .buildTransport();

Properties properties = new Properties();
properties.put("brokerList", "localhost:8000,localhost:8001");
Connection connection = ConnectionFactory.fromProperties(properties, clientTransport);
String query = "select count(*) FROM baseballStats limit 1";

ResultSetGroup rs = connection.execute(query);
System.out.println(rs);
connection.close();
```

## Connection Properties

The Java query client reads the following connection properties directly from `Properties`:

| Property | Default | Used by | Notes |
| --- | --- | --- | --- |
| `brokerConnectTimeoutMs` | `2000` | HTTP broker transport | Broker connect timeout in milliseconds |
| `brokerReadTimeoutMs` | `60000` | HTTP broker transport and cursor fetches | Broker read timeout in milliseconds |
| `brokerHandshakeTimeoutMs` | `2000` | HTTP broker transport | TLS handshake timeout in milliseconds |
| `controllerConnectTimeoutMs` | `2000` | Controller-based broker cache | Controller connect timeout for `fromController(...)` |
| `controllerReadTimeoutMs` | `60000` | Controller-based broker cache | Controller read timeout for broker-map refresh |
| `controllerHandshakeTimeoutMs` | `2000` | Controller-based broker cache | Controller TLS handshake timeout |
| `headers.<name>` | None | HTTP broker transport and controller broker cache | Adds default HTTP headers such as `headers.Authorization` |
| `scheme` | `http` | HTTP broker transport and controller broker cache | Set to `https` for TLS-enabled brokers and controller |
| `queryOptions` | Empty string | HTTP broker transport | Injected into the JSON request body as Pinot query options |
| `useMultistageEngine` | `false` | HTTP broker transport | Switches HTTP requests from `/query/sql` to `/query` |
| `appId` | None | HTTP broker transport and controller broker cache | Prefixes the generated user agent string |
| `failOnExceptions` | `true` | `Connection` | Throw `PinotClientException` when the broker response includes query-processing exceptions |
| `preferTLS` | `false` | ZooKeeper-based broker discovery | Prefer broker TLS ports when discovering brokers from Helix |
| `useGrpcPort` | `false` | ZooKeeper/controller broker discovery | Prefer broker gRPC ports when building broker lists |
| `pinot.java_client.tls.*` | None | HTTP broker transport and controller broker cache | TLS config namespace consumed by `TlsUtils.extractTlsConfig(...)` |
| `brokerTlsV10Enabled` | `false` | HTTP broker transport | Re-enable TLSv1.0 for broker requests |
| `controllerTlsV10Enabled` | `false` | Controller broker cache | Re-enable TLSv1.0 for controller requests |

Example:

```java
Properties properties = new Properties();
properties.setProperty("scheme", "https");
properties.setProperty("headers.Authorization", "Basic <base64-credentials>");
properties.setProperty("queryOptions", "timeoutMs=10000");
properties.setProperty("brokerReadTimeoutMs", "10000");
properties.setProperty("controllerReadTimeoutMs", "10000");
properties.setProperty("pinot.java_client.tls.truststore.path", "/path/to/truststore.jks");
properties.setProperty("pinot.java_client.tls.truststore.password", "changeit");

Connection connection = ConnectionFactory.fromController(properties, "controller.example.com:9000");
```

When you customize `JsonAsyncHttpPinotClientTransportFactory` directly, the `scheme` property only overrides the factory when you set `scheme` in `Properties`. If `scheme` is absent, `withConnectionProperties(...)` keeps any scheme you already set on the factory and falls back to `http` only when neither the factory nor the properties specify one.

## Request Tracing

The Java client (`JsonAsyncHttpPinotClientTransport`) automatically attaches an `X-Correlation-Id` header — a unique UUID per request — to every HTTP query. This ID:

- Is logged at `DEBUG` level by the client under `org.apache.pinot.client`
- Appears in broker access logs, enabling end-to-end tracing across proxies and load balancers

No configuration is required. To see correlation IDs in client logs, set the log level:

```properties
log4j.logger.org.apache.pinot.client=DEBUG
```
