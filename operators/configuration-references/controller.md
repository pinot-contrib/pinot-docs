# Advanced Configurations for Pinot Controller

For advanced configurations, the Pinot Controller can be configure with a property file 
refered with the `-configFileName` argument of `pinot-admin.sh`.

```bash
bin/pinot-admin.sh StartController -configFileName ~/controller.properties
```

## **Controller Properties References**

<table>
  <thead>
    <tr>
      <th style="text-align:left">Property</th>
      <th style="text-align:left">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">controller.zk.str</td>
      <td style="text-align:left">
        <p>Zookeeper address string</p>
        <p>Example : `localhost:2181`</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.helix.cluster.name</td>
      <td style="text-align:left">
        <p>Name of the Pinot Cluster</p>
        <p>Example : `my-pinot-cluster`</p></td>
    </tr>
    <tr>
      <td style="text-align:left">controller.host</td>
      <td style="text-align:left">
        <p>Used with the http server port to establish an Helix identity.</p>
        <p>Example : `my-controller-server`</p></td>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.port</td>
      <td style="text-align:left">
        <p>Port of the http server. This configurations enables a vanilla http listener which will answer to all requests.</p>
        <p>This property also fullfil a second role by being used with `controller.host` to establish an Helix identity.</p>
        <p>For advanced usage like activating `https` and or restricting requests to specific hostnames, see `controller.access.protocols` property.</p>
        <p>Optional if `controller.access.protocols` is configured.</p>
        <p>Example : `9000`</p></td>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols</td>
      <td style="text-align:left">
        <p>
          Command seperated list of supported protocols. Values may only be `http` or `https`. Once define, 
          each protocol may be customized with their dedicated extended property namespace.
        <p>Example : `http,https`</p></td>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.&lt;protocol&gt;.port</td>
      <td style="text-align:left">
        <p>Port for which the specified protocol will be bound.</p>
        <p>If `controller.port` is not defined, the first configured port will be used with `controller.host` to establish the Helix identify.</p>
        <p>Example : `9443`</p></td>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.&lt;protocol&gt;.host</td>
      <td style="text-align:left">
        <p>
          Configures the protocol listener to a specific host. Useful for scenarios where it may be 
          acceptable to trust the internal network with http while forcing https on a public listener with
          a public DNS hostname define as host.
        </p>
        <p>Default : `0.0.0.0`</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.https.tls.keystore.path</td>
      <td style="text-align:left">
        <p>Path to a `jks` key store containing the certificate served by the http server.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.https.tls.keystore.password</td>
      <td style="text-align:left">
        <p>Password for the key store used by the http server</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.https.tls.truststore.path</td>
      <td style="text-align:left">
        <p>Path to a `jks` trust store containing CA certificates to be trusted by the http server.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.https.tls.truststore.password</td>
      <td style="text-align:left">
        <p>Password for the trust store used by the http server</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.https.tls.requires_client_auth</td>
      <td style="text-align:left">
        <p>Forces clients to connect with mutual TLS</p>
        <p>Default: `false`</p>
    </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.mode</td>
      <td style="text-align:left">
        <p>Sets the roles fulfield by the Controller. Allows to select if the instance participate in the workload of Pinot, Helix or both.</p>
        <p>Available configurations: `DUAL, PINOT_ONLY, HELIX_ONLY`</p>
        <p>Default: `DUAL`</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">cluster.tenant.isolation.enable</td>
      <td style="text-align:left">
        <p>Enables multi tenancy for Pinot.</p>
        <p>Default: `false`</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.query.console.useHttps</td>
      <td style="text-align:left">
        <p>
          Advertises the Http Server in Swagger as `https` even if the http server is configured with `http`. 
          Useful for scenarios such as having a reverse proxy with achieving TLS termination.
        </p>
        <p>Default: `false`</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.data.dir</td>
      <td style="text-align:left">
        <p>Path of the directory used for data persistence.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.local.temp.dir</td>
      <td style="text-align:left">
        <p>Path of the temporary director used for file manipulation (upload, download and uncompression).</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.update_segment_state_model</td>
      <td style="text-align:left">
        <p>If enabled, updates the segment state model on Controller startup even if already exists in Helix.
        <p>Defaut: `false`</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.upload.onlineToOfflineTimeout</td>
      <td style="text-align:left">
        <p>Timeout in milliseconds for which the Controller will wait for a segment update to confirm it went from online to offline.</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.resource.rebalance.strategy</td>
      <td style="text-align:left">
        <p>
          Class name for an implementation of `org.apache.helix.controller.rebalancer.strategy.RebalanceStrategy` 
          used when initializing the Helix lead controller resource.</p>
        <p>Default: `org.apache.helix.controller.rebalancer.strategy.AutoRebalanceStrategy`</p>
      </td>
    </tr>
  </tbody>
</table>