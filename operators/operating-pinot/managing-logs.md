# Managing Logs

## Dynamic Log Levels

Pinot supports inspecting and modifying Log4J log levels dynamically in production environments through REST. This can often be helpful when debugging an issue that is transient in nature and restarting the server with new configurations files could alter the behavior.

### Supported Operations

#### List All Loggers

```
GET /loggers
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept: application/json"` is recommended</td>
    </tr>
  </tbody>
</table>

Sample Usage:

```
$ curl -X GET -H "accept: application/json" localhost:8000/loggers
["root","org.reflections","org.apache.pinot.tools.admin"]
```

#### Fetch Specific Logger

```
GET /loggers/{loggerName}
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept: application/json"` is recommended</td>
    </tr>
    <tr>
      <td>Path Parameter</td>
      <td>`loggerName` string</td>
      <td>The name of the logger (fully qualified path)</td>
    </tr>
  </tbody>
</table>

Sample Usage:

```
> curl -X GET -H "accept: application/json" localhost:8000/loggers/root
{"filter":null,"level":"INFO","name":"root"}
```

#### Set Logger Level

```
PUT /loggers/{loggerName}?level={level}
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept: application/json"` is recommended</td>
    </tr>
    <tr>
      <td>Path Parameter</td>
      <td>`loggerName` string</td>
      <td>The name of the logger (fully qualified path)</td>
    </tr>
    <tr>
      <td>Query Parameter</td>
      <td>`level` string</td>
      <td>the log level (such as `DEBUG` or `INFO`</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept: application/json"` is recommended</td>
    </tr>
  </tbody>
</table>

#### Download a Log File

```
GET /loggers/download?filePath={filePath}
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept: application/octet_string"` is recommended</td>
    </tr>
    <tr>
      <td>Query Parameter</td>
      <td>`filePath` string</td>
      <td>The path to the file, can be obtained using `GET /loggers/files`</td>
    </tr>
  </tbody>
</table>

### Remote Log APIs

{% hint style="info" %}
These APIs are only supported on the Controller
{% endhint %}

#### List Log Files on All Instances

```
GET /loggers/instances
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept": application/json"` is recommended</td>
    </tr>
  </tbody>
</table>

#### List Log Files on a Specific Instance

```
GET /loggers/instances/{instanceName}
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept": application/json"` is recommended</td>
    </tr>
    <tr>
      <td>Path Parameter</td>
      <td>`instanceName` string</td>
      <td>Indicates which instance to collect logs from</td>
    </tr>
  </tbody>
</table>

#### Download Remote Log From Given Instance

```
GET /loggers/instances/{instanceName}/download?filePath={filePath}
```

<table>
  <thead>
    <tr>
      <th>Parameter Type</th>
      <th>Parameter Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Header</td>
      <td>`accept` string</td>
      <td>Setting to `"accept: application/octet`</td>
    </tr>
    <tr>
      <td>Path Parameter</td>
      <td>`instanceName` string</td>
      <td>Indicates which instance to collect logs from</td>
    </tr>
    <tr>
      <td>Query Parameter</td>
      <td>`filePath` string</td>
      <td>Indicates which file to download</td>
    </tr>
  </tbody>
</table>
