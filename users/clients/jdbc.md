# JDBC

The java client can be found in [pinot-clients/pinot-jdbc-client](https://github.com/apache/incubator-pinot/tree/master/pinot-clients/pinot-jdbc-client). Here's an example of how to use the `pinot-java-client` to query Pinot.

```java
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

You can also use PreparedStatements. The placeholder parameters are represented using **?** symbol.

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

