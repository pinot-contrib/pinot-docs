# Controller

Most of the properties in Pinot are set in Zookeeper via Helix. However, you can also set properties in `controller.conf` file. You can specify the path to config file at the startup time as follows -

```text
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

`Controller.conf` can have the following properties - 

### Primary Configuration

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
      <td style="text-align:left">controller.vip.host</td>
      <td style="text-align:left">same as <code>controller.host</code>
      </td>
      <td style="text-align:left">The VIP hostname used to set the download URL for segments</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.vip.port</td>
      <td style="text-align:left">same as <code>controller.port</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.vip.protocol</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.host</td>
      <td style="text-align:left">localhost</td>
      <td style="text-align:left">The ip of the host on which controller is running</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.port</td>
      <td style="text-align:left">9000</td>
      <td style="text-align:left">The port on which controller should run</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocol</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.data.dir</td>
      <td style="text-align:left">${java.io.tmpdir}/PinotController</td>
      <td style="text-align:left">
        <p></p>
        <p>Directory to host segment data</p>
        <p></p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.local.temp.dir</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.zk.str</td>
      <td style="text-align:left">localhost:2181</td>
      <td style="text-align:left">zookeeper host:port string to connect</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.update_segment_state_model</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.helix.cluster.name</td>
      <td style="text-align:left"></td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tenant.isolation.enable</td>
      <td style="text-align:left">true</td>
      <td style="text-align:left">Enable Tenant Isolation, default is single tenant cluste</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.enable.split.commit</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.query.console.useHttps</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left">use https instead of http for cluster</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.upload.onlineToOfflineTimeout</td>
      <td style="text-align:left">2 minutes</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.mode</td>
      <td style="text-align:left"><code>dual</code>
      </td>
      <td style="text-align:left">Should be one of <code>helix_only</code>, <code>pinot_only</code> or <code>dual</code> 
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.resource.rebalance.strategy</td>
      <td style="text-align:left"><code>org.apache.helix.controller.<br />rebalancer.strategy.AutoRebalanceStrategy</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.realtime.segment.commit.timeoutSeconds</td>
      <td style="text-align:left">120 seconds</td>
      <td style="text-align:left">request timeout for segment commit</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.deleted.segments.retentionInDays</td>
      <td style="text-align:left">7 days</td>
      <td style="text-align:left">duration for which to retain deleted segments</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.admin.access.control.factory.class</td>
      <td style="text-align:left"><code>org.apache.pinot.controller.<br />api.access.AllowAllAccessFactory</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.segment.upload.timeoutInMillis</td>
      <td style="text-align:left">10 minutes</td>
      <td style="text-align:left">timeout for upload of segments.</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.realtime.segment.metadata.commit.numLocks</td>
      <td style="text-align:left">64</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.enable.storage.quota.check</td>
      <td style="text-align:left">true</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.enable.batch.message.mode</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.allow.hlc.tables</td>
      <td style="text-align:left">true</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.storage.factory.class.file</td>
      <td style="text-align:left"><code>org.apache.pinot.spi.<br />filesystem.LocalPinotFS</code>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">table.minReplicas</td>
      <td style="text-align:left">1</td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols</td>
      <td style="text-align:left">http</td>
      <td style="text-align:left">Ingress protocols to access controller (http or https or http,https)</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.http.port</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">Port to access controller via http</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.broker.protocols.https</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">Port to access controller via https</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.broker.protocol</td>
      <td style="text-align:left">http</td>
      <td style="text-align:left">protocol for forwarding query requests (http or https)</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.broker.port.override</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">override for broker port when forwarding query requests (use in multi-ingress scenarios)</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.keystore.path</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">Path to controller TLS keystore</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.keystore.password</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">keystore password</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.truststore.path</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">Path to controller TLS truststore</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.truststore.password</td>
      <td style="text-align:left"></td>
      <td style="text-align:left">truststore password</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.client.auth</td>
      <td style="text-align:left">false</td>
      <td style="text-align:left">toggle for requiring TLS client auth</td>
    </tr>
  </tbody>
</table>



### Periodic Tasks Configuration

| Property | Default | Description |
| :--- | :--- | :--- |
| controller.retention.frequencyInSeconds | 6 hours | frequency at which to trigger retention checking tasks |
| controller.validation.frequencyInSeconds \(Deprecated\) | 1 hour |  |
| controller.offline.segment.interval.checker.frequencyInSeconds | 24 hours |  |
| controller.realtime.segment.validation.frequencyInSeconds | 1 hour |  |
| controller.broker.resource.validation.frequencyInSeconds | 1 hour |  |
| controller.broker.resource.validation.initialDelayInSeconds | 120-300 seconds |  |
| controller.statuschecker.frequencyInSeconds | 5 minutes |  |
| controller.statuschecker.waitForPushTimeInSeconds | 10 minutes |  |
| controller.task.frequencyInSeconds | -1 \(disabled\) |  |
| controller.realtime.segment.relocator.frequency | 1 hour |  |
| controller.segment.level.validation.intervalInSeconds | 24 hours |  |
| controller.statuschecker.intialDelayInSeconds | 120-300 seconds |  |
| controller.retentionManager.initialDelayInSeconds | 120-300 seconds |  |
| controller.offlineSegmentIntervalChecker.initialDelayInSeconds | 120-300 seconds |  |
| controller.realtimeSegmentRelocation.initialDelayInSeconds | 120-300 seconds |  |

