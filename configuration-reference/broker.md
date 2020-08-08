# Broker

You can set broker properties in a configuration file. The file can be provided during startup time as follows - 

```text
bin/pinot-admin.sh StartBroker -configFileName /path/to/broker.conf
```

`broker.conf` can have the following properties. All properties are defined in this class.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Default</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">pinot.broker.delayShutdownTimeMs</td>
      <td style="text-align:left">10 seconds</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.enableTableLevelMetrics</td>
      <td style="text-align:left">true</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.query.response.limit</td>
      <td style="text-align:left">Integer.MAX_VALUE</td>
      <td style="text-align:left">When config <code>pinot.broker.enable.query.limit.override</code>is enabled,
        reset limit for selection query if it exceeds this value.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.query.log.length</td>
      <td style="text-align:left">Integer.MAX_VALUE</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.query.log.maxRatePerSecond</td>
      <td style="text-align:left">10000.0</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.timeoutMs</td>
      <td style="text-align:left">10 seconds</td>
      <td style="text-align:left">
        <p></p>
        <p>Timeout for Broker Query in Milliseconds</p>
        <p></p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.startup.minResourcePercent</td>
      <td style="text-align:left">100</td>
      <td style="text-align:left">Configuration to consider the broker ServiceStatus as being STARTED if
        the percent of resources (tables) that are ONLINE for this this broker
        has crossed the threshold percentage of the total number of tables that
        it is expected to serve</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.enable.query.limit.override</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left">Configuration to enable Query LIMIT Override to protect Pinot Broker and
        Server from fetch too many records back.</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.client.queryPort</td>
      <td style="text-align:left">8099</td>
      <td style="text-align:left">Port to query broker</td>
    </tr>
  </tbody>
</table>





