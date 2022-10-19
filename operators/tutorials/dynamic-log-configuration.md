# Dynamic Log Configuration

Pinot supports inspecting and modifying Log4J log levels dynamically in production environments through REST. This can often be helpful when debugging an issue that is transient in nature and restarting the server with new configurations files may alter the desired behavior.

### Supported Operations

#### List All Loggers

```
GET /loggers
```

| Parameter Type | Parameter Name  | Description                                            |
| -------------- | --------------- | ------------------------------------------------------ |
| Header         | `accept` string | Setting to `"accept: application/json"` is recommended |

Sample Usage:

```
$ curl -X GET -H "accept: application/json" localhost:8000/loggers
["root","org.reflections","org.apache.pinot.tools.admin"]
```

#### Fetch Specific Logger

```
GET /loggers/${loggerName}
```

| Parameter Type | Parameter Name      | Description                                            |
| -------------- | ------------------- | ------------------------------------------------------ |
| Header         | `accept` string     | Setting to `"accept: application/json"` is recommended |
| Path Parameter | `loggerName` string | The name of the logger (fully qualified path)          |

Sample Usage:

```
> curl -X GET -H "accept: application/json" localhost:8000/loggers/root
{"filter":null,"level":"INFO","name":"root"}
```

#### Set Logger Level

```
PUT /loggers/${loggerName}
```

| Parameter Type  | Parameter Name      | Description                                            |
| --------------- | ------------------- | ------------------------------------------------------ |
| Header          | `accept` string     | Setting to `"accept: application/json"` is recommended |
| Path Parameter  | `loggerName` string | The name of the logger (fully qualified path)          |
| Query Parameter | `level` string      | the log level (such as `DEBUG` or `INFO`               |

Sample Usage

```
$ curl -X PUT -H "accept: application/json" localhost:8000/loggers/root?level=ERROR
{"filter":null,"level":"ERROR","name":"root"}
```
