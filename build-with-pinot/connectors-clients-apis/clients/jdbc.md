# JDBC

Pinot offers a standard JDBC interface for broker-routed SQL queries. This makes it easier to integrate Pinot with SQL tooling and JVM applications that expect a JDBC driver.

## Installation

You can include the JDBC dependency in your code as follows:

{% tabs %}
{% tab title="Maven" %}
```java
<dependency>
    <groupId>org.apache.pinot</groupId>
    <artifactId>pinot-jdbc-client</artifactId>
    <version>1.4.0</version>
</dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```java
implementation "org.apache.pinot:pinot-jdbc-client:1.4.0"
```
{% endtab %}
{% endtabs %}

You can also compile the [JDBC code](https://github.com/apache/pinot/tree/master/pinot-clients/pinot-jdbc-client) into a JAR and place the JAR in the Drivers directory of your application.

There is no need to register the driver manually as it will automatically register itself at the startup of the application.

## Usage

Here's an example of how to use `pinot-jdbc-client` for querying. The JDBC URL points at the controller, not directly at a broker.

```java
String dbUrl = "jdbc:pinot://localhost:9000";

try (Connection conn = DriverManager.getConnection(dbUrl);
     Statement statement = conn.createStatement();
     ResultSet rs = statement.executeQuery(
         "SELECT UPPER(playerName) AS name FROM baseballStats LIMIT 10")) {
  while (rs.next()) {
    String playerName = rs.getString("name");
    System.out.println(playerName);
  }
}
```

The driver auto-registers itself, so manual `DriverManager.registerDriver(...)` calls are not required.

## Connection URL and routing

The current driver recognizes two JDBC schemes:

* `jdbc:pinot://<controller-host>:<controller-port>` for the HTTP query path
* `jdbc:pinotgrpc://<controller-host>:<controller-port>` for the broker gRPC query path

Optional URL and property keys that affect routing:

| Key | Default | Notes |
| --- | --- | --- |
| `tenant` | `DefaultTenant` | Restricts broker discovery to one Pinot tenant |
| `brokers` | None | Semicolon-separated broker override such as `broker-1:8099;broker-2:8099`. When present on the HTTP path, the driver uses the provided brokers instead of controller broker lookup. |
| `scheme` | `http` | Switches controller and broker HTTP transport to HTTPS |

Example:

```java
String dbUrl =
    "jdbc:pinot://controller.example.com:9000?tenant=DefaultTenant&brokers=broker-1:8099;broker-2:8099";
Connection conn = DriverManager.getConnection(dbUrl);
```

You can also use `PreparedStatement`. Placeholder parameters are represented using `?`.

```java
Connection conn = DriverManager.getConnection(DB_URL);
PreparedStatement statement = conn.prepareStatement("SELECT UPPER(playerName) AS name FROM baseballStats WHERE age = ?");
statement.setInt(1, 20);

ResultSet rs = statement.executeQuery();
Set<String> results = new HashSet<>();

while(rs.next()){
 String playerName = rs.getString("name");
 results.add(playerName);
}

conn.close();
```

## gRPC Connections

To use the broker gRPC transport from JDBC, switch the scheme from `jdbc:pinot://` to `jdbc:pinotgrpc://`.

```java
Properties connectionProperties = new Properties();
connectionProperties.setProperty("usePlainText", "false");
connectionProperties.setProperty("tls.truststore.path", "/path/to/grpc-truststore.jks");
connectionProperties.setProperty("tls.truststore.password", "changeit");

Connection conn = DriverManager.getConnection(
    "jdbc:pinotgrpc://localhost:9000?blockRowSize=10000&encoding=JSON&compression=ZSTD",
    connectionProperties);
```

The `pinotgrpc` driver accepts the following gRPC transport properties through either the JDBC URL query string or the `Properties` object passed to `DriverManager.getConnection(...)`. TLS settings use the `tls.*` namespace, not broker-side keys such as `pinot.broker.tls.*`.

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

The JDBC gRPC path also forwards these per-request settings when they appear in the URL query string or connection properties:

* Metadata options: `blockRowSize`, `encoding`, `compression`, `Authorization`
* Header-prefixed metadata: `headers.<name>`
* Query options: `enableNullHandling`, `useMultistageEngine`

## Authentication

Pinot supports [basic HTTP authorization](../../../operate-pinot/authentication/basic-auth-access-control.md), which can be enabled for your cluster using configuration. The JDBC driver supports authentication through:

* `headers.Authorization`
* `user` and `password` URL parameters
* `user` and `password` connection properties

Auth precedence in the current driver is:

1. `headers.Authorization`
2. `user` and `password` in the JDBC URL
3. `user` and `password` in the `Properties` object

Example with an explicit auth header:

```java
final String username = "admin";
final String password = "verysecret";

// Concatenate username and password and use base64 to encode the concatenated string
String plainCredentials = username + ":" + password;
String base64Credentials = new String(Base64.getEncoder().encode(plainCredentials.getBytes()));

// Create authorization header
String authorizationHeader = "Basic " + base64Credentials;
Properties connectionProperties = new Properties();
connectionProperties.setProperty("headers.Authorization", authorizationHeader);

// Register new Pinot JDBC driver
DriverManager.registerDriver(new PinotDriver());

// Get a client connection and set the encoded authorization header
Connection connection = DriverManager.getConnection(DB_URL, connectionProperties);

// Test that your query successfully authenticates
Statement statement = connection.createStatement();
ResultSet rs = statement.executeQuery("SELECT count(*) FROM baseballStats LIMIT 1;");

while (rs.next()) {
    String result = rs.getString("count(*)");
    System.out.println(result);
}
```

The same auth flow also works for `jdbc:pinotgrpc://...`. In the gRPC path, the driver forwards `Authorization` as gRPC request metadata.

## Connection Properties

The JDBC driver currently reads these connection properties:

| Property | Default | Used by | Notes |
| --- | --- | --- | --- |
| `tenant` | `DefaultTenant` | HTTP and gRPC JDBC | Limits controller broker discovery to one tenant |
| `brokers` | None | HTTP and gRPC JDBC | Semicolon-separated broker override |
| `scheme` | `http` | HTTP broker transport and controller transport | Set to `https` for TLS-enabled controller and HTTP brokers |
| `headers.<name>` | None | HTTP and gRPC JDBC | Adds default headers or metadata such as `headers.Authorization` |
| `user` | None | HTTP and gRPC JDBC | Used for basic auth when no explicit auth header is set |
| `password` | None | HTTP and gRPC JDBC | Used for basic auth when no explicit auth header is set |
| `brokerConnectTimeoutMs` | `2000` | HTTP broker transport | Broker connect timeout in milliseconds |
| `brokerReadTimeoutMs` | `60000` | HTTP broker transport | Broker read timeout in milliseconds |
| `brokerHandshakeTimeoutMs` | `2000` | HTTP broker transport | Broker TLS handshake timeout |
| `controllerConnectTimeoutMs` | `2000` | Controller transport | Controller connect timeout in milliseconds |
| `controllerReadTimeoutMs` | `60000` | Controller transport | Controller read timeout in milliseconds |
| `controllerHandshakeTimeoutMs` | `2000` | Controller transport | Controller TLS handshake timeout |
| `controllerTlsV10Enabled` | `false` | Controller transport | Re-enable TLSv1.0 for controller requests |
| `pinot.jdbc.tls.*` | None | HTTP broker transport and controller transport | TLS config namespace consumed by the JDBC driver |

Example:

```java
String dbUrl =
    "jdbc:pinot://controller.example.com:9000?scheme=https&brokerReadTimeoutMs=10000&controllerReadTimeoutMs=10000";
```

## Limitation

The JDBC client doesn't support `INSERT`, `DELETE` or `UPDATE` statements due to the database limitations. You can only use the client to query the database.\
The driver is also not completely ANSI SQL 92 compliant.

{% hint style="warning" %}
If you integrate Pinot through JDBC, check `Connection.getMetaData()` and other `DatabaseMetaData` methods in your consuming tool. Pinot is an OLAP database, and some JDBC features expected by ANSI SQL tools are intentionally unsupported.
{% endhint %}
