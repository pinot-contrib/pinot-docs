---
description: Pinot broker gRPC query reference.
---

# Broker gRPC API

Pinot's broker gRPC API is the transport alternative to HTTP query submission. It is primarily useful when client libraries want lower overhead, Arrow encoding, or connection-level compression controls.

## Enablement

```properties
pinot.broker.grpc.port=8010
pinot.broker.grpc.tls.enabled=true
pinot.broker.grpc.tls.port=8020
```

If you expose the secure broker gRPC listener, the current broker startup path reuses the TLS material under `pinot.broker.tls.*` for the keystore and truststore. See the [broker configuration reference](../configuration-reference/broker.md#broker-grpc-transport) for the full listener and TLS setup.

## Client Options

The Java gRPC client and the JDBC `pinotgrpc` driver both use `GrpcConfig` for connection transport settings. That means the same transport property names work in Java `Properties` and JDBC URL query parameters.

### Request Metadata Options

| Option | Default | Notes |
| --- | --- | --- |
| `blockRowSize` | `10000` | Rows per response block |
| `compression` | `ZSTD` | Wire compression choice |
| `encoding` | `JSON` | Result transport encoding; `ARROW` is also supported |
| `headers.<name>` | None | Adds request metadata headers such as `headers.Authorization` |

### Transport Properties

| Property | Default | Notes |
| --- | --- | --- |
| `usePlainText` | `true` | Use plaintext gRPC transport. Set to `false` to enable TLS. |
| `maxInboundMessageSizeBytes` | `134217728` (128 MB) | Maximum inbound gRPC message size accepted by the client. |
| `channelKeepAliveTimeSeconds` | `-1` (disabled) | Keepalive ping interval. Set a positive value to enable keepalive. |
| `channelKeepAliveTimeoutSeconds` | `20` | Timeout waiting for keepalive acknowledgements. |
| `channelKeepAliveWithoutCalls` | `true` | Allows keepalive pings even when no RPC is active. |
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

## Client Examples

The gRPC Java and JDBC clients use the `pinotgrpc` scheme.

```java
Properties properties = new Properties();
properties.setProperty("usePlainText", "false");
properties.setProperty("tls.truststore.path", "/path/to/grpc-truststore.jks");
properties.setProperty("tls.truststore.password", "changeit");

GrpcConnection grpcConnection = ConnectionFactory.fromControllerGrpc(properties, "localhost:9000");
ResultSetGroup resultSetGroup = grpcConnection.execute(
    "SELECT * FROM airlineStats LIMIT 1000",
    Map.of("blockRowSize", "10000", "encoding", "JSON", "compression", "ZSTD"));
```

```java
Properties properties = new Properties();
properties.setProperty("usePlainText", "false");
properties.setProperty("tls.truststore.path", "/path/to/grpc-truststore.jks");
properties.setProperty("tls.truststore.password", "changeit");

try (Connection connection = DriverManager.getConnection(
    "jdbc:pinotgrpc://localhost:9000?blockRowSize=10000&encoding=JSON&compression=ZSTD",
    properties)) {
  // execute queries
}
```

## Operational Notes

- Use the same `--add-opens` JVM flag when running Arrow-based clients.
- Connection establishment performs a lightweight validation query.
- Client TLS properties are namespaced under `tls.*`, not broker-side keys such as `pinot.broker.tls.*`.
- The Java gRPC client takes `blockRowSize`, `compression`, and `encoding` per request via the metadata map passed to `execute(..., metadataMap)` or `executeGrpc(..., metadataMap)`.
- The JDBC gRPC driver also accepts `blockRowSize`, `compression`, and `encoding` as URL parameters or connection properties and forwards them as request metadata.
- If the broker also uses `pinot.broker.request.handler.type=grpc` for broker-to-server communication, the similarly named top-level `broker.conf` keepalive and shutdown settings apply to the broker's outbound channels, not to Java/JDBC client connections.

## What this page covered

- How to enable broker gRPC.
- The client-side options that matter most.
- The connection and encoding behavior that client authors need to know.

## Next step

Use the Java or JDBC client docs when you need integration code, then validate the query path against the broker endpoint you plan to expose.

## Related pages

- [API Reference](README.md)
- [Query API](query-api.md)
- [Controller API](controller-api.md)
