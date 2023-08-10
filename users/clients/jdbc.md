# JDBC

Pinot offers standard JDBC interface to query the database. This makes it easier to integrate Pinot with other applications such as Tableau.

## Installation

You can include the JDBC dependency in your code as follows -

{% tabs %}
{% tab title="Maven" %}
```java
<dependency>
    <groupId>org.apache.pinot</groupId>
    <artifactId>pinot-jdbc-client</artifactId>
    <version>0.8.0</version>
</dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```java
include 'org.apache.pinot:pinot-jdbc-client:0.8.0'
```
{% endtab %}
{% endtabs %}

You can also compile the [JDBC code](https://github.com/apache/pinot/tree/master/pinot-clients/pinot-jdbc-client) into a JAR and place the JAR in the Drivers directory of your application.

There is no need to register the driver manually as it will automatically register itself at the startup of the application.

## Usage

Here's an example of how to use the `pinot-jdbc-client` for querying. The client only requires the controller URL.

```java
public static final String DB_URL = "jdbc:pinot://localhost:9000"
DriverManager.registerDriver(new PinotDriver());
Connection conn = DriverManager.getConnection(DB_URL);
Statement statement = conn.createStatement();
Integer limitResults = 10;
ResultSet rs = statement.executeQuery(String.format("SELECT UPPER(playerName) AS name FROM baseballStats LIMIT %d", limitResults));
Set<String> results = new HashSet<>();

while(rs.next()){
 String playerName = rs.getString("name");
 results.add(playerName);
}

conn.close();
```

You can also use PreparedStatements. The placeholder parameters are represented using `?` _\*\*_ (question mark) symbol.

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

## Authentication

Pinot supports [basic HTTP authorization](broken-reference), which can be enabled for your cluster using configuration. To support basic HTTP authorization in your client-side JDBC applications, make sure you are using Pinot JDBC 0.10.0+ or building from the latest Pinot snapshot. The following code snippet shows you how to connect to and query a Pinot cluster that has basic HTTP authorization enabled when using the JDBC client.

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

## Configuring client time-out

The following timeouts can be set:

* brokerConnectTimeoutMs (default 2000)
* brokerReadTimeoutMs (default 60000)
* brokerHandshakeTimeoutMs (default 2000)
* controllerConnectTimeoutMs (default 2000)
* controllerReadTimeoutMs (default 60000)
* controllerHandshakeTimeoutMs (default 2000)

Timeouts for the JDBC connector can be added as a parameter to the JDBC Connection URL. The following example enables https and configures a very low timeout of 10ms:

## Configuring client time-out

The following timeouts can be set:

* brokerConnectTimeoutMs (default 2000)
* brokerReadTimeoutMs (default 60000)
* brokerHandshakeTimeoutMs (default 2000)
* controllerConnectTimeoutMs (default 2000)
* controllerReadTimeoutMs (default 60000)
* controllerHandshakeTimeoutMs (default 2000)

Timeouts for the JDBC connector can be added as a parameter to the JDBC Connection URL. The following example enables https and configures a very low timeout of 10ms:

```java
final String DB_URL = "jdbc:pinot://hostname?brokerConnectTimeoutMs=10&brokerReadTimeoutMs=10&brokerHandshakeTimeoutMs=10&controllerConnectTimeoutMs=10&controllerReadTimeoutMs=10&scheme=https";
```

## Limitation

The JDBC client doesn't support `INSERT`, `DELETE` or `UPDATE` statements due to the database limitations. You can only use the client to query the database.\
The driver is also not completely ANSI SQL 92 compliant.

{% hint style="warning" %}
If you want to use JDBC driver to integrate Pinot with other applications, do make sure to check JDBC ConnectionMetadata in your code. This will help in determining which features cannot be supported by Pinot since it is an OLAP database.
{% endhint %}
