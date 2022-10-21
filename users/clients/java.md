# Java

Pinot provides a native java client to execute queries on the cluster. The client makes it easier for user to query data. The client is also tenant-aware and thus is able to redirect the queries to the correct broker.

## Installation

You can use the client by including the following dependency -

{% tabs %}
{% tab title="Maven" %}
```java
<dependency>
    <groupId>org.apache.pinot</groupId>
    <artifactId>pinot-java-client</artifactId>
    <version>0.9.3</version>
</dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```java
include 'org.apache.pinot:pinot-java-client:0.5.0'
```
{% endtab %}
{% endtabs %}

You can also build [the code for java client](https://github.com/apache/pinot/tree/master/pinot-clients/pinot-java-client) locally and use it.

{% hint style="info" %}
Basic authorization for the JDBC client is not supported in Pinot JDBC 0.9.3 release or earlier. The JDBC client has been upgraded to support basic authentication in the Pinot 0.10.0 snapshot, which can currently be built from source.

You will not need to update your Pinot cluster to 0.10.0+ to support basic authentication, only the JDBC and Java client JARs.
{% endhint %}

## Usage

Here's an example of how to use the `pinot-java-client` to query Pinot.

```java
import org.apache.pinot.client.Connection;
import org.apache.pinot.client.ConnectionFactory;
import org.apache.pinot.client.Request;
import org.apache.pinot.client.ResultSetGroup;
import org.apache.pinot.client.ResultSet;

/**
 * Demonstrates the use of the pinot-client to query Pinot from Java
 */
public class PinotClientExample {

  public static void main(String[] args) {

    // pinot connection
    String zkUrl = "localhost:2181";
    String pinotClusterName = "PinotCluster";
    Connection pinotConnection = ConnectionFactory.fromZookeeper(zkUrl + "/" + pinotClusterName);

    String query = "SELECT COUNT(*) FROM myTable GROUP BY foo";

    // set queryType=sql for querying the sql endpoint
    Request pinotClientRequest = new Request("sql", query);
    ResultSetGroup pinotResultSetGroup = pinotConnection.execute(pinotClientRequest);
    ResultSet resultTableResultSet = pinotResultSetGroup.getResultSet(0);

    int numRows = resultTableResultSet.getRowCount();
    int numColumns = resultTableResultSet.getColumnCount();
    String columnValue = resultTableResultSet.getString(0, 1);
    String columnName = resultTableResultSet.getColumnName(1);

    System.out.println("ColumnName: " + columnName + ", ColumnValue: " + columnValue);
  }
}
```

## Connection Factory

The client provides a `ConnectionFactory` class to create connections to a Pinot cluster. The factory supports the following methods to create a connection -

* **Zookeeper (Recommended)** - Comma seperated list of zookeeper of the cluster. This is the recommended method which can redirect queries to appropriate brokers based on tenant/table.
* **Broker list** - Comma seperated list of the brokers in the cluster. This should only be used in standalone setups or for POC, unless you have a load balancer setup for brokers.
* **Controller URL** - (v 0.11.0+) Controller URL. This will use periodic controller API calls to keep the table level broker list updated (hence there might be delay b/w the broker mapping changing and the client state getting updated).
* **Properties file** -  You can also put the broker list as `brokerList` in a properties file and provide the path to that file to the factory.  This should only be used in standalone setups or for POC, unless you have a load balancer setup for brokers.

Here's an example demonstrating all methods of Connection factory -

```java
Connection connection = ConnectionFactory.fromZookeeper
  ("some-zookeeper-server:2191/zookeeperPath");

Connection connection = ConnectionFactory.fromProperties("demo.properties");

Connection connection = ConnectionFactory.fromHostList
  ("broker-1:1234", "broker-2:1234", ...);

Connection connection = ConnectionFactory.fromController
    ("http", "controller-url", 9000)
```

## Query Methods

You can run the query in both blocking as well as async manner. Use

* `Connection.execute(org.apache.pinot.client.Request)` for blocking queries
* `Connection.executeAsync(org.apache.pinot.client.Request)` for asynchronous queries that return a future object.

```java
ResultSetGroup resultSetGroup = 
  connection.execute(new Request("sql", "select * from foo..."));
// OR
Future<ResultSetGroup> futureResultSetGroup = 
  connection.executeAsync(new Request("sql", "select * from foo..."));
```

You can also use `PreparedStatement` to escape query parameters. We don't store the Prepared Statement in the database and hence it won't increase the subsequent query performance.

```java
PreparedStatement statement = 
    connection.prepareStatement(new Request("sql", "select * from foo where a = ?"));
statement.setString(1, "bar");

ResultSetGroup resultSetGroup = statement.execute();
// OR
Future<ResultSetGroup> futureResultSetGroup = statement.executeAsync();
```

## Result Set

Results can be obtained with the various get methods in the first ResultSet, obtained through the `getResultSet(int)` method:

```java
Request request = new Request("sql", "select foo, bar from baz where quux = 'quuux'");
ResultSetGroup resultSetGroup = connection.execute(request);
ResultSet resultTableResultSet = pinotResultSetGroup.getResultSet(0);

for (int i = 0; i < resultSet.getRowCount(); ++i) {
  System.out.println("foo: " + resultSet.getString(i, 0));
  System.out.println("bar: " + resultSet.getInt(i, 1));
}
```

### PQL Queries

If queryFormat `pql` is used in the `Request`, there are some differences in how the results can be accessed, depending on the query.

In the case of aggregation, each aggregation function is within its own ResultSet. A query with multiple aggregation function will return one result set per aggregation function, as they are computed in parallel.

```java
ResultSetGroup resultSetGroup = 
    connection.execute(new Request("pql", "select max(foo), min(foo) from bar"));

System.out.println("Number of result groups:" +
    resultSetGroup.getResultSetCount(); // 2, min(foo) and max(foo)
ResultSet resultSetMax = resultSetGroup.getResultSet(0);
System.out.println("Max foo: " + resultSetMax.getInt(0));
ResultSet resultSetMin = resultSetGroup.getResultSet(1);
System.out.println("Min foo: " + resultSetMin.getInt(0));
```

In case of aggregation with `GROUP BY`, there will be as many ResultSets as the number of aggregations, each of which will contain multiple results grouped by a grouping key.

```java
ResultSetGroup resultSetGroup = 
    connection.execute(
        new Request("pql", "select min(foo), max(foo) from bar group by baz"));

System.out.println("Number of result groups:" +
    resultSetGroup.getResultSetCount(); // 2, min(foo) and max(foo)

ResultSet minResultSet = resultSetGroup.getResultSet(0);
for(int i = 0; i < minResultSet.length(); ++i) {
    System.out.println("Minimum foo for " + minResultSet.getGroupKeyString(i, 1) +
        ": " + minResultSet.getInt(i));
}

ResultSet maxResultSet = resultSetGroup.getResultSet(1);
for(int i = 0; i < maxResultSet.length(); ++i) {
    System.out.println("Maximum foo for " + maxResultSet.getGroupKeyString(i, 1) +
        ": " + maxResultSet.getInt(i));
}
```

{% hint style="warning" %}
This section is only applicable for PQL endpoint, which is deprecated and will be deleted soon. For more information about the endpoints, visit [Querying Pinot](../api/querying-pinot-using-standard-sql/).
{% endhint %}

## Authentication

Pinot supports [basic HTTP authorization](../../operators/tutorials/authentication-authorization-and-acls.md#controller-authentication-and-authorization), which can be enabled for your cluster using configuration. To support basic HTTP authorization in your client-side Java applications, make sure you are using Pinot Java Client 0.10.0+ or building from the latest Pinot snapshot. The following code snippet shows you how to connect to and query a Pinot cluster that has basic HTTP authorization enabled when using the Java client.

```java
final String username = "admin";
final String password = "verysecret";

// Concatenate username and password and use base64 to encode the concatenated string
String plainCredentials = username + ":" + password;
String base64Credentials = new String(
    Base64.getEncoder().encode(plainCredentials.getBytes()));

String authorizationHeader = "Basic " + base64Credentials;

Map<String, String> headers = new HashMap();
headers.put("Authorization", authorizationHeader);
JsonAsyncHttpPinotClientTransportFactory factory = 
    new JsonAsyncHttpPinotClientTransportFactory();
factory.setHeaders(headers);
PinotClientTransport clientTransport = factory
    .buildTransport();

Connection connection = ConnectionFactory.fromProperties(
        Collections.singletonList("localhost:8000"), clientTransport);
String query = "select count(*) FROM baseballStats limit 1";

ResultSetGroup rs = connection.execute(query);
System.out.println(rs);
connection.close();
```

## Configuring client time-out

The following timeouts can be set:

* brokerConnectTimeoutMs (default 2000)
* brokerReadTimeoutMs (default 60000)
* brokerHandshakeTimeoutMs (default 2000)
* controllerConnectTimeoutMs (default 2000)
* controllerReadTimeoutMs (default 60000)
* controllerHandshakeTimeoutMs (default 2000)

Timeouts for the Java connector can be added as a connection properties. The following example configures a very low timeout of 10ms:

```java
Properties connectionProperties = new Properties();
connectionProperties.setProperty("controllerReadTimeoutMs", "10");
connectionProperties.setProperty("controllerHandshakeTimeoutMs", "10");
connectionProperties.setProperty("controllerConnectTimeoutMs", "10");
connectionProperties.setProperty("brokerReadTimeoutMs", "10");
connectionProperties.setProperty("brokerHandshakeTimeoutMs", "10");
connectionProperties.setProperty("brokerConnectTimeoutMs", "10");

// Register new Pinot JDBC driver
DriverManager.registerDriver(new PinotDriver());

// Get a client connection and set the connection timeouts
Connection connection = DriverManager.getConnection(DB_URL, connectionProperties);

// Test that your query successfully times out
Statement statement = connection.createStatement();
ResultSet rs = statement.executeQuery("SELECT count(*) FROM baseballStats LIMIT 1;");

while (rs.next()) {
    String result = rs.getString("count(*)");
    System.out.println(result);
}
```
