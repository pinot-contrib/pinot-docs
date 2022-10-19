# Managing Logs

## Dynamic Log Levels

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
GET /loggers/{loggerName}
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
PUT /loggers/{loggerName}?level={level}
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

## Downloading Component Logs

Pinot supports downloading logs directly over HTTP in situations where the operator may not have access to the container, but has access to the rest endpoints.

If the operator has access to the Controller, they can download log files from any one of the other components.

### Supported Operations

#### List Available Log Files

```
GET /loggers/files
```

| Parameter Type | Parameter Name  | Description                                            |
| -------------- | --------------- | ------------------------------------------------------ |
| Header         | `accept` string | Setting to `"accept: application/json"` is recommended |

#### Download a Log File

```
GET /loggers/download?filePath={filePath}
```

| Parameter Type  | Parameter name    | Description                                                      |
| --------------- | ----------------- | ---------------------------------------------------------------- |
| Header          | `accept` string   | Setting to `"accept: application/octet_string"` is recommended   |
| Query Parameter | `filePath` string | The path to the file, can be obtained using `GET /loggers/files` |

### Remote Log APIs

{% hint style="info" %}
These APIs are only supported on the Controller
{% endhint %}

#### List Log Files on All Instances

```
GET /loggers/instances
```

| Parameter Type | Parameter Name  | Description                                             |
| -------------- | --------------- | ------------------------------------------------------- |
| Header         | `accept` string | Setting to `"accept": application/json"` is recommended |

#### List Log Files on a Specific Instance

```
GET /loggers/instances/{instanceName}
```

| Parameter Type | Parameter Name        | Description                                             |
| -------------- | --------------------- | ------------------------------------------------------- |
| Header         | `accept` string       | Setting to `"accept": application/json"` is recommended |
| Path Parameter | `instanceName` string | Indicates which instance to collect logs from           |

#### Download Remote Log From Given Instance

```
GET /loggers/instances/{instanceName}/download?filePath={filePath}
```

| Parameter Type  | Parameter Name        | Description                                   |
| --------------- | --------------------- | --------------------------------------------- |
| Header          | `accept` string       | Setting to `"accept: application/octet`       |
| Path Parameter  | `instanceName` string | Indicates which instance to collect logs from |
| Query Parameter | `filePath` string     | Indicates which file to download              |
