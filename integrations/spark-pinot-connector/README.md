---
description: Use the Spark-Pinot connector to read data from and write data to Pinot.
---

# Spark-Pinot Connector

Spark-pinot connector to read data from Pinot.

Detailed read model documentation is here: [spark-pinot-connector-read-model.md](spark-pinot-connector-read-model.md "mention")

The write model is Experimental and the documentation is here: [spark-pinot-connector-write-model.md](spark-pinot-connector-write-model.md "mention")

### Features

* Query realtime, offline or hybrid tables
* Distributed, parallel scan
* Streaming reads using gRPC (optional)
* SQL support instead of PQL
* Column and filter push down to optimize performance
* Overlap between realtime and offline segments is queried exactly once for hybrid tables
* Schema discovery
  * Dynamic inference
  * Static analysis of case class
* Supports query options
* HTTPS/TLS support for secure connections

### Quick Start

```
import org.apache.spark.sql.SparkSession

val spark: SparkSession = SparkSession
      .builder()
      .appName("spark-pinot-connector-test")
      .master("local")
      .getOrCreate()

import spark.implicits._

val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .load()
  .filter($"DestStateName" === "Florida")

data.show(100)
```

### Security Configuration

{% hint style="warning" %}
This feature is supported after 1.4.0 release, please use current master or wait for 1.5.0
{% endhint %}

You can secure both HTTP and gRPC using a unified switch or explicit flags.

* Unified: set `secureMode=true` to enable HTTPS and gRPC TLS together (recommended)
* Explicit: set `useHttps` for REST and `grpc.use-plain-text=false` for gRPC

#### Quick examples

```
// Unified secure mode (enables HTTPS + gRPC TLS by default)
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("secureMode", "true")
  .load()

// Explicit HTTPS only (gRPC remains plaintext by default)
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("useHttps", "true")
  .load()

// Explicit gRPC TLS only (REST remains HTTP by default)
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("grpc.use-plain-text", "false")
  .load()
```

#### HTTPS Configuration

When HTTPS is enabled (either via `secureMode=true` or `useHttps=true`), you can configure keystore/truststore as needed:

```
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("useHttps", "true")
  .option("keystorePath", "/path/to/keystore.jks")
  .option("keystorePassword", "keystorePassword")
  .option("truststorePath", "/path/to/truststore.jks")
  .option("truststorePassword", "truststorePassword")
  .load()
```

#### HTTPS Configuration Options

| Option               | Description                                                | Required | Default |
| -------------------- | ---------------------------------------------------------- | -------- | ------- |
| `secureMode`         | Unified switch to enable HTTPS and gRPC TLS                | No       | `false` |
| `useHttps`           | Enable HTTPS connections (overrides `secureMode` for REST) | No       | `false` |
| `keystorePath`       | Path to client keystore file (JKS format)                  | No       | None    |
| `keystorePassword`   | Password for the keystore                                  | No       | None    |
| `truststorePath`     | Path to truststore file (JKS format)                       | No       | None    |
| `truststorePassword` | Password for the truststore                                | No       | None    |

**Note:** If no truststore is provided when HTTPS is enabled, the connector will trust all certificates (not recommended for production use).

### Authentication Support

{% hint style="warning" %}
This feature is supported after 1.4.0 release, please use current master or wait for 1.5.0
{% endhint %}

The connector supports custom authentication headers for secure access to Pinot clusters:

```
// Using Bearer token authentication
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("authToken", "my-jwt-token")  // Automatically adds "Authorization: Bearer my-jwt-token"
  .load()

// Using custom authentication header
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("authHeader", "Authorization")
  .option("authToken", "Bearer my-custom-token")
  .load()

// Using API key authentication
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("authHeader", "X-API-Key")
  .option("authToken", "my-api-key")
  .load()
```

#### Authentication Configuration Options

{% hint style="warning" %}
This feature is supported after 1.4.0 release, please use current master or wait for 1.5.0
{% endhint %}

| Option       | Description                       | Required | Default                                        |
| ------------ | --------------------------------- | -------- | ---------------------------------------------- |
| `authHeader` | Custom authentication header name | No       | `Authorization` (when `authToken` is provided) |
| `authToken`  | Authentication token/value        | No       | None                                           |

**Note:** If only `authToken` is provided without `authHeader`, the connector will automatically use `Authorization: Bearer <token>`.

### Pinot Proxy Support

{% hint style="warning" %}
This feature is supported after 1.4.0 release, please use current master or wait for 1.5.0
{% endhint %}

The connector supports Pinot Proxy for secure cluster access where the proxy is the only exposed endpoint. When proxy is enabled, all HTTP requests to controllers/brokers and gRPC requests to servers are routed through the proxy.

#### Proxy Configuration Examples

```
// Basic proxy configuration
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("controller", "pinot-proxy:8080")  // Proxy endpoint
  .option("proxy.enabled", "true")
  .load()

// Proxy with authentication
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("controller", "pinot-proxy:8080")
  .option("proxy.enabled", "true")
  .option("authToken", "my-proxy-token")
  .load()

// Proxy with gRPC configuration
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("controller", "pinot-proxy:8080")
  .option("proxy.enabled", "true")
  .option("grpc.proxy-uri", "pinot-proxy:8094")  // gRPC proxy endpoint
  .load()
```

#### Proxy Configuration Options

| Option          | Description                                        | Required | Default |
| --------------- | -------------------------------------------------- | -------- | ------- |
| `proxy.enabled` | Use Pinot Proxy for controller and broker requests | No       | `false` |

**Note:** When proxy is enabled, the connector adds `FORWARD_HOST` and `FORWARD_PORT` headers to route requests to the actual Pinot services.

### gRPC Configuration

{% hint style="warning" %}
This feature is supported after 1.4.0 release, please use current master or wait for 1.5.0
{% endhint %}

The connector supports comprehensive gRPC configuration for secure and optimized communication with Pinot servers.

#### gRPC Configuration Examples

```
// Basic gRPC configuration
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("grpc.port", "8091")
  .option("grpc.max-inbound-message-size", "256000000")  // 256MB
  .load()

// gRPC with TLS (explicit)
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("grpc.use-plain-text", "false")
  .option("grpc.tls.keystore-path", "/path/to/grpc-keystore.jks")
  .option("grpc.tls.keystore-password", "keystore-password")
  .option("grpc.tls.truststore-path", "/path/to/grpc-truststore.jks")
  .option("grpc.tls.truststore-password", "truststore-password")
  .load()

// gRPC with proxy
val data = spark.read
  .format("pinot")
  .option("table", "airlineStats")
  .option("tableType", "offline")
  .option("proxy.enabled", "true")
  .option("grpc.proxy-uri", "pinot-proxy:8094")
  .load()
```

#### gRPC Configuration Options

| Option                          | Description                                                             | Required | Default |
| ------------------------------- | ----------------------------------------------------------------------- | -------- | ------- |
| `grpc.port`                     | Pinot gRPC port                                                         | No       | `8090`  |
| `grpc.max-inbound-message-size` | Max inbound message bytes when init gRPC client                         | No       | `128MB` |
| `grpc.use-plain-text`           | Use plain text for gRPC communication (overrides `secureMode` for gRPC) | No       | `true`  |
| `grpc.tls.keystore-type`        | TLS keystore type for gRPC connection                                   | No       | `JKS`   |
| `grpc.tls.keystore-path`        | TLS keystore file location for gRPC connection                          | No       | None    |
| `grpc.tls.keystore-password`    | TLS keystore password                                                   | No       | None    |
| `grpc.tls.truststore-type`      | TLS truststore type for gRPC connection                                 | No       | `JKS`   |
| `grpc.tls.truststore-path`      | TLS truststore file location for gRPC connection                        | No       | None    |
| `grpc.tls.truststore-password`  | TLS truststore password                                                 | No       | None    |
| `grpc.tls.ssl-provider`         | SSL provider                                                            | No       | `JDK`   |
| `grpc.proxy-uri`                | Pinot Rest Proxy gRPC endpoint URI                                      | No       | None    |

**Note:** When using gRPC with proxy, the connector automatically adds `FORWARD_HOST` and `FORWARD_PORT` metadata headers for proper request routing.

### Examples

There are examples under [https://github.com/apache/pinot/tree/master/pinot-connectors/pinot-spark-3-connector/examples](https://github.com/apache/pinot/tree/master/pinot-connectors/pinot-spark-3-connector/examples) .&#x20;

#### Prerequisites

* Apache Spark 3.x installed and `spark-shell` available in your PATH.
*   Setup PINOT\_HOME env variable:

    ```
    export PINOT_HOME=/path/to/pinot
    ```
*   The Pinot Spark 3 Connector shaded JAR built and available at:

    ```
    $PINOT_HOME/pinot-connectors/pinot-spark-3-connector/target/pinot-spark-3-connector-*-shaded.jar
    ```
*   Example Scala script located at:

    ```
    $PINOT_HOME/pinot-connectors/pinot-spark-3-connector/examples/read_pinot_from_proxy_with_auth_token.scala
    ```

#### Scala Script to read data from Pinot Proxy

{% code title="read_pinot_from_proxy_with_auth_token.scala" lineNumbers="true" %}
```scala
import org.apache.spark.sql.SparkSession

val spark = SparkSession.builder().appName("read-pinot-airlineStats").master("local[*]").getOrCreate()

val df = spark.read.
  format("org.apache.pinot.connector.spark.v3.datasource.PinotDataSource").
  option("table", "myTable").
  option("tableType", "offline").
  option("controller", "pinot-proxy:8080").
  option("secureMode", "true").
  option("authToken", "st-xxxxxxx").
  option("proxy.enabled", "true").
  option("grpc.proxy-uri", "pinot-proxy:8094").
  option("useGrpcServer", "true").
  load()

println("Schema:")
df.printSchema()

println("Sample rows:")
df.show(10, truncate = false)

println(s"Total rows: ${df.count()}")

spark.stop()
```
{% endcode %}

#### Run with spark-shell

Launch the example in `spark-shell` with the following command:

```bash
spark-shell 
    --master 'local[*]' \
    --name read-pinot \
    --jars "$PINOT_HOME/pinot-connectors/pinot-spark-3-connector/target/pinot-spark-3-connector-*-shaded.jar" < "$PINOT_HOME/pinot-connectors/pinot-spark-3-connector/examples/read_pinot_from_proxy_with_auth_token.scala"
```

#### Run with spark-submit

You can run the examples locally (e.g. using your IDE) in a standalone mode by starting a local Pinot cluster. See: [https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally)

You can also run the tests in _cluster mode_ using following command:

```
export SPARK_CLUSTER=<YOUR_YARN_OR_SPARK_CLUSTER>

# Edit the ExampleSparkPinotConnectorTest to get rid of `.master("local")` and rebuild the jar before running this command
spark-submit \
    --class org.apache.pinot.connector.spark.v3.datasource.ExampleSparkPinotConnectorTest \
    --jars ./target/pinot-spark-3-connector-1.3.0-shaded.jar \
    --master $SPARK_CLUSTER \
    --deploy-mode cluster \
  ./target/pinot-spark-3-connector-1.3.0-tests.jar
```

This example demonstrates how to use the Pinot Spark 3 Connector to read data from a Pinot cluster via a proxy with authentication token support.

### Security Best Practices

{% hint style="warning" %}
This feature is supported after 1.4.0 release, please use current master or wait for 1.5.0
{% endhint %}

#### Production HTTPS Configuration

* Always use HTTPS in production environments
* Store certificates in secure locations with appropriate file permissions
* Use proper certificate validation with valid truststore
* Rotate certificates regularly

#### Production Authentication

* Use service accounts with minimal required permissions
* Store authentication tokens securely (environment variables, secret management systems)
* Implement token rotation policies
* Monitor authentication failures

#### Production gRPC Configuration

* Enable TLS for gRPC communication in production
* Use certificate-based authentication when possible
* Configure appropriate message size limits based on your data
* Use connection pooling for high-throughput scenarios

### Future Works

* Add integration tests for read operation
* Add write support(pinot segment write logic will be changed in later versions of pinot)
