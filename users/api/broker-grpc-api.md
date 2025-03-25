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
    GrpcConnection grpcConnection = ConnectionFactory.fromControllerGrpc(new Properties(), "localhost:9000");
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
    try (Connection connection = DriverManager.getConnection("jdbc:pinotgrpc://localhost:9000?blockRowSize=100");
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

