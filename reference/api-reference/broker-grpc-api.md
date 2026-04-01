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

## Client Options

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Default</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`blockRowSize`</td>
      <td>`10000`</td>
      <td>Rows per response block</td>
    </tr>
    <tr>
      <td>`compression`</td>
      <td>`ZSTD`</td>
      <td>Wire compression choice</td>
    </tr>
    <tr>
      <td>`encoding`</td>
      <td>`JSON`</td>
      <td>Result transport encoding; `ARROW` is also supported</td>
    </tr>
  </tbody>
</table>

## Client Examples

The gRPC Java and JDBC clients use the `pinotgrpc` scheme.

```java
GrpcConnection grpcConnection = ConnectionFactory.fromControllerGrpc(properties, "localhost:9000");
ResultSetGroup resultSetGroup = grpcConnection.execute("SELECT * FROM airlineStats limit 1000");
```

```java
try (Connection connection = DriverManager.getConnection("jdbc:pinotgrpc://localhost:9000?blockRowSize=10000&encoding=JSON&compression=ZSTD")) {
  // execute queries
}
```

## Operational Notes

- Use the same `--add-opens` JVM flag when running Arrow-based clients.
- Connection establishment performs a lightweight validation query.
- Request headers can be attached with the `headers.` prefix.

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
