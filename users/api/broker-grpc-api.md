# Broker GRPC API

Apart from HTTP based query endpoint, Pinot also supports gRPC endpoint in broker.

## Enable GRPC query entrypoint in broker

Add gRPC port config in pinot broker to enable the [`BrokerGrpcServer`](https://github.com/apache/pinot/blob/master/pinot-broker/src/main/java/org/apache/pinot/broker/grpc/BrokerGrpcServer.java):

```editorconfig
pinot.broker.grpc.port=8010
```

if you want to enable TLS, then use below configs:

```editorconfig
pinot.broker.grpc.tls.enabled=true
pinot.broker.grpc.tls.port=8020

// Server side TLS is used. The client does not present a certificate.
// The server only verifies the client’s connection via its own certificate and doesn’t validate the client’s identity via TLS.
// Common in public APIs, where only the server needs to be trusted.
pinot.broker.grpctls.client.auth.enabled=false

// Config TLS keystore and truststore
pinot.broker.grpctls.keystore.path=/home/pinot/tls-store/keystore-internal.jks
pinot.broker.grpctls.keystore.password=changeit
pinot.broker.grpctls.keystore.type=JKS
pinot.broker.grpctls.truststore.path=/home/pinot/tls-store/truststore.jks
pinot.broker.grpctls.truststore.password=changeit
pinot.broker.grpctls.truststore.type=JKS
```



## Broker GRPC Clients

Below are the examples of usage for `pinot-java-client` and `pinot-jdbc-client` .

### Java Grpc Client

The main difference of the usage here is that `ConnectionFactory` will return a **`GrpcConnection`** instead of **`Connection`**.

{% hint style="warning" %}
If you want to use ARROW as the encoding type, you must start Java with

&#x20;`--add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED`&#x20;

(See https://arrow.apache.org/docs/java/install.html)
{% endhint %}

Below is a sample code to use the java client: **GrpcConnection**:

```java
package org.apache.pinot.client.examples;

import java.io.IOException;
import java.util.Properties;
import org.apache.pinot.client.ConnectionFactory;
import org.apache.pinot.client.ResultSetGroup;
import org.apache.pinot.client.grpc.GrpcConnection;


public class PinotBrokerGrpcClientExample {

  private PinotBrokerGrpcClientExample() {
  }
  
  public static void main(String[] args)
      throws IOException {
    Properties properties = new Properties();
    properties.put("encoding", "JSON");
    properties.put("compression", "ZSTD");
    properties.put("blockRowSize", "10000");
    GrpcConnection grpcConnection = ConnectionFactory.fromControllerGrpc(properties, "localhost:9000");
    // GrpcConnection grpcConnection = ConnectionFactory.fromZookeeperGrpc(properties, "localhost:2123/QuickStartCluster");
    // GrpcConnection grpcConnection = ConnectionFactory.fromHostListGrpc(properties, List.of("localhost:8010"));
    ResultSetGroup resultSetGroup = grpcConnection.execute("SELECT * FROM airlineStats limit 1000");
    for (int i = 0; i < resultSetGroup.getResultSetCount(); i++) {
      org.apache.pinot.client.ResultSet resultSet = resultSetGroup.getResultSet(i);
      for (int rowId = 0; rowId < resultSet.getRowCount(); rowId++) {
        System.out.print("Row Id: " + rowId + "\t");
        for (int colId = 0; colId < resultSet.getColumnCount(); colId++) {
          System.out.print(resultSet.getString(rowId, colId) + "\t");
        }
        System.out.println();
      }
    }
    grpcConnection.close();
  }
}
```

### JDBC Grpc Client

The main usage difference here is scheme is changed to `pinotgrpc`.

{% hint style="warning" %}
If you want to use ARROW as the encoding type, you must start Java with

&#x20;`--add-opens=java.base/java.nio=org.apache.arrow.memory.core,ALL-UNNAMED`&#x20;

(See https://arrow.apache.org/docs/java/install.html)
{% endhint %}



Below is a sample code to use JDBC driver.

```java
package org.apache.pinot.client.examples;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;


public class PinotBrokerGrpcJdbcClientExample {

  private PinotBrokerGrpcJdbcClientExample() {
  }

  public static void main(String[] args)
      throws IOException {
    try (Connection connection = DriverManager.getConnection("jdbc:pinotgrpc://localhost:9000?blockRowSize=10000&encoding=JSON&compression=ZSTD");
        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT * FROM airlineStats limit 1000")) {
      // Print results
      ResultSetMetaData metaData = resultSet.getMetaData();
      int columnCount = metaData.getColumnCount();
      while (resultSet.next()) {
        System.out.print("Row Id: " + resultSet.getRow() + "\t");
        for (int i = 1; i <= columnCount; i++) {
          System.out.print(metaData.getColumnName(i) + ": " + resultSet.getString(i) + "\t");
        }
        System.out.println();
      }
    } catch (SQLException e) {
      e.printStackTrace();
    }
  }
}
```



## Client Configurations

&#x20;Below are the parameters to set per connection basis:

1. **blockRowSize**: the number of rows per block that grpc response will return, **default** is **10000**.
2. **compression**: the compression algorithm over the wire, **default** is **ZSTD**, other options:&#x20;
   1. LZ4\_FAST: fast than LZ4\_HIGH but not as high compression rate
   2. LZ4\_HIGH
   3. **ZSTD (Default)**
   4. DEFLATE
   5. GZIP
   6. SNAPPY
   7. PASS\_THROUGH/NONE: no compression, fast but could be large data transfer over the wire.
3. **encoding**: how to do serialization and deserialization for ResultTable transport between BrokerGrpcServer and Grpc Client, **default** is **JSON**, other options:
   1. **JSON(Default)**
   2. ARROW

## Benchmark

We did a simple benchmark of query:&#x20;

```
SELECT * FROM airlineStats limit 1000
```

&#x20;Will compress **97k (9.2MB)** rows with block size **10K**.

### Compression

<table><thead><tr><th>CompressionType</th><th>Compression Ratio</th><th>Response Latency(ms)</th><th>Latency Ratio</th><th data-hidden></th></tr></thead><tbody><tr><td>LZ4_FAST</td><td><mark style="color:yellow;">42.19%</mark></td><td><mark style="color:green;">477.6</mark></td><td><mark style="color:green;">103.02%</mark></td><td></td></tr><tr><td>LZ4_HIGH</td><td><mark style="color:green;">30.04%</mark></td><td><mark style="color:yellow;">977.0</mark></td><td><mark style="color:red;">210.74%</mark></td><td></td></tr><tr><td>ZSTD</td><td><mark style="color:green;">26.10%</mark></td><td><mark style="color:green;">485.4</mark></td><td><mark style="color:green;">104.70%</mark></td><td></td></tr><tr><td>DEFLATE</td><td><mark style="color:green;">25.64%</mark></td><td><mark style="color:yellow;">810.0</mark></td><td><mark style="color:yellow;">174.72%</mark></td><td></td></tr><tr><td>GZIP</td><td><mark style="color:green;">25.64%</mark></td><td><mark style="color:yellow;">811.8</mark></td><td><mark style="color:yellow;">175.11%</mark></td><td></td></tr><tr><td>SNAPPY</td><td><mark style="color:yellow;">42.56%</mark></td><td><mark style="color:green;">461.2</mark></td><td><mark style="color:green;">99.48%</mark></td><td></td></tr><tr><td>NONE</td><td><mark style="color:red;">100%</mark></td><td><mark style="color:green;">463.6</mark></td><td><mark style="color:green;">100%</mark></td><td></td></tr></tbody></table>

### Block Size

We also tried for ZSTD the same data set with different block size:

| BlockRowSize | Compression Ratio                         | Avg Latency(ms)                          |
| ------------ | ----------------------------------------- | ---------------------------------------- |
| 100          | <mark style="color:yellow;">30.48%</mark> | <mark style="color:yellow;">539.6</mark> |
| 1000         | <mark style="color:green;">27.56%</mark>  | <mark style="color:green;">478.3</mark>  |
| 10000        | <mark style="color:green;">26.10%</mark>  | <mark style="color:green;">485.4</mark>  |
| 100000       | <mark style="color:green;">25.73%</mark>  | <mark style="color:yellow;">561.2</mark> |

### Encoding

Tested with ZSTD compression for the same query but different encoding and block size:

<table><thead><tr><th>BlockRowSize</th><th width="114.22998046875">Encoding</th><th width="123.03466796875">Compression</th><th width="150.7039794921875">Avg Latency(ms)</th><th width="98.7171630859375">Bytes</th><th width="160.693603515625">Compression Ratio</th></tr></thead><tbody><tr><td>1000</td><td>JSON</td><td>ZSTD</td><td><mark style="color:yellow;">473</mark></td><td><mark style="color:green;">2559246</mark></td><td><mark style="color:green;">27.56%</mark></td></tr><tr><td>10000</td><td>JSON</td><td>ZSTD</td><td><mark style="color:yellow;">473</mark></td><td><mark style="color:green;">2424082</mark></td><td><mark style="color:green;">26.10%</mark></td></tr><tr><td>100000</td><td>JSON</td><td>ZSTD</td><td><mark style="color:red;">594</mark></td><td><mark style="color:green;">2389717</mark></td><td><mark style="color:green;">25.73%</mark></td></tr><tr><td>1000</td><td>ARROW</td><td>ZSTD</td><td><mark style="color:green;">372</mark></td><td><mark style="color:yellow;">3054993</mark></td><td><mark style="color:yellow;">32.90%</mark></td></tr><tr><td>10000</td><td>ARROW</td><td>ZSTD</td><td><mark style="color:green;">367</mark></td><td><mark style="color:green;">2705245</mark></td><td><mark style="color:green;">29.13%</mark></td></tr><tr><td>100000</td><td>ARROW</td><td>ZSTD</td><td><mark style="color:yellow;">447</mark></td><td><mark style="color:yellow;">2809744</mark></td><td><mark style="color:yellow;">30.26%</mark></td></tr></tbody></table>



