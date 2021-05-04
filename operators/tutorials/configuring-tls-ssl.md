---
description: Set up TLS-secured connections inside and outside your cluster
---

# Configuring TLS/SSL

Pinot versions from 0.7.0+ support client-cluster and intra-cluster TLS. TLS-support comes in both 1-way and 2-way flavors. This guide walks through the relevant configuration options.

Looking to ingest from Kafka via secured connections? Check out [Kafka Streaming Ingestion with TLS/SSL](https://docs.pinot.apache.org/basics/data-import/pinot-stream-ingestion/import-from-apache-kafka#some-more-kafka-ingestion-configs).

### Listeners

In order to support incremental upgrades of unsecured pinot clusters towards TLS, we introduce multi-ingress support via listeners. Each listener accepts connections for a specific protocol on a specific port. For example, pinot-broker may be configured to accept both, **http** on port 8099 and **https** on port 8443 at the same time.

Existing configuration properties such as `controller.port` are still parsed and automatically translated to a http listener configuration to enable full backwards-compatibility. TLS-secured ingress must be configured through the new listener specifications.

### TLS upgrade

If you're bootstrapping a cluster from scratch, you can directly configure TLS-secured connections and you can forgo legacy http ingress. If you're upgrading an existing \(production\) cluster, you'll be able to perform the upgrade without downtime if your deployment is configured for high-availability.

On a high level, a zero-downtime upgrade includes the following 3 phases:

* adding a secondary TLS-secured ingress to pinot controllers, brokers, and servers
* switching client and internode egress to prefer TLS-secured connections
* disabling unsecured ingress

This requires a rolling restart of \(replicated\) service containers after each re-configuration phase. The sample listener specifications below will guide you through this process.

### Generating certificates

Apache Pinot leverages the JVM's native TLS infrastructure with all its benefits and limitations. Certificates should be generated to include the host IP, hostname, and fully-qualified domain names \(if accessed or identified this way\).

We support both, the JVM's default key/truststore, as well as configuration options to load certificates from secondary locations.

{% hint style="info" %}
Most JVM's default certificate store can be configured with command-line arguments:

`-Djavax.net.ssl.keyStore  
-Djavax.net.ssl.keyStorePassword  
-Djavax.net.ssl.trustStorecertificates  
-Djavax.net.ssl.trustStorePassword`
{% endhint %}

### Listener Specifications

This section contains a number of examples for common situations. The complete configuration reference can be found is each component's configuration reference.

If you're bootstrapping a new cluster, scroll down towards the end. We order this section for purposes of migrating an existing unsecured cluster to TLS-only.

#### Legacy HTTP config \(unsecured\)

This is a minimal example of network configuration options prior to 0.7.0. This specification is still supported for backwards-compatibility and translated internally to a listener specification.

| key | value |
| :--- | :--- |
| controller.port | 9000 |
| pinot.broker.client.queryPort | 8099 |
| pinot.server.netty.port | 8098 |
| pinot.server.adminapi.port | 8097 |

#### HTTP with listener specification \(unsecured\)

This HTTP listener specification is the equivalent of manually translating the legacy configuration above to a listener specification.

| key | value |
| :--- | :--- |
| controller.access.protocols | http |
| controller.access.protocols.http.port | 9000 |
| pinot.broker.client.access.protocols | http |
| pinot.broker.client.access.protocols.http.port | 8099 |
| pinot.server.netty.enabled | true |
| pinot.server.netty.port | 8098 |
| pinot.server.adminapi.access.protocols | http |
| pinot.server.adminapi.access.protocols.http.port | 8097 |

#### HTTP/HTTPS multi-ingress \(unsecured egress\)

This is a common scenario for development clusters and an intermediate phase during a zero-downtime migration of an unsecured cluster towards TLS. This configuration optionally accepts secure ingress on alternate ports, but still defaults to unsecured egress for all operations.

<table>
  <thead>
    <tr>
      <th style="text-align:left">key</th>
      <th style="text-align:left">value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">controller.tls.keystore.path</td>
      <td style="text-align:left">/path/to/keystore
        <br />(unset for JVM default)</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.keystore.password</td>
      <td style="text-align:left">
        <p>mykeystorepassword</p>
        <p>(unset for JVM default)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.truststore.path</td>
      <td style="text-align:left">/path/to/truststore
        <br />(unset for JVM default)</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.tls.truststore.password</td>
      <td style="text-align:left">
        <p>mytruststorepassword</p>
        <p>(unset for JVM default)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols</td>
      <td style="text-align:left">http,https</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.http.port</td>
      <td style="text-align:left">9000</td>
    </tr>
    <tr>
      <td style="text-align:left">controller.access.protocols.https.port</td>
      <td style="text-align:left">9443</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.tls.keystore.path</td>
      <td style="text-align:left">/path/to/keystore
        <br />(unset for JVM default)</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.tls.keystore.password</td>
      <td style="text-align:left">
        <p>mykeystorepassword</p>
        <p>(unset for JVM default)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.tls.truststore.path</td>
      <td style="text-align:left">/path/to/truststore
        <br />(unset for JVM default)</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.tls.truststore.password</td>
      <td style="text-align:left">
        <p>mytruststorepassword</p>
        <p>(unset for JVM default)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.client.access.protocols</td>
      <td style="text-align:left">http,https</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.client.access.protocols.http.port</td>
      <td style="text-align:left">8099</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker.client.access.protocols.https.port</td>
      <td style="text-align:left">8443</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.tls.keystore.path</td>
      <td style="text-align:left">/path/to/keystore
        <br />(unset for JVM default)</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.tls.keystore.password</td>
      <td style="text-align:left">
        <p>mykeystorepassword</p>
        <p>(unset for JVM default)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.tls.truststore.path</td>
      <td style="text-align:left">/path/to/truststore
        <br />(unset for JVM default)</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.tls.truststore.password</td>
      <td style="text-align:left">
        <p>mytruststorepassword</p>
        <p>(unset JVM default)</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.netty.enabled</td>
      <td style="text-align:left">true</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.netty.port</td>
      <td style="text-align:left">8098</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.nettytls.enabled</td>
      <td style="text-align:left">true</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.nettytls.port</td>
      <td style="text-align:left">8089</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.adminapi.access.protocols</td>
      <td style="text-align:left">http,https</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.adminapi.access.protocols.http.port</td>
      <td style="text-align:left">8097</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server.adminapi.access.protocols.https.port</td>
      <td style="text-align:left">7443</td>
    </tr>
  </tbody>
</table>

#### HTTP/HTTPS multi-ingress \(secure egress\)

After all pinot components have been configured and restarted to offer secure ingress, we can modify egress to default to secure connections internode. Clients, such as **pinot-admin.sh**, support an optional flag `-controllerProtocol https` to enable secure access. Ingestion jobs similarly support an optional `tlsSpec` key to configure key/trststores. Note, that any console clients must have access to appropriate certificates via the JVM's default key/truststore.

| key | value |
| :--- | :--- |
| controller.tls ... | \(see above\) |
| controller.access ... | \(see above\) |
| controller.broker.protocol | https |
| controller.broker.port.override | 8443 |
| controller.vip.protocol | https |
| controller.vip.port | 9443 |
| pinot.broker.tls ... | \(see above\) |
| pinot.broker.client.access ... | \(see above\) |
| pinot.broker.nettytls.enabled | true |
| pinot.server ... | \(see above\) |

#### TLS only

This is the default for a newly bootstrapped secure pinot cluster. It is also the final stage for any migration of an existing cluster. With this configuration applied, pinot's components will reject any unsecured connection attempt.

| key | value |
| :--- | :--- |
| controller.tls ... | \(see above\) |
| controller.access.protocols | https |
| controller.access.protocols.https.port | 9443 |
| controller.broker.protocol | https |
| controller.vip.protocol | https |
| controller.vip.port | 9443 |
| pinot.broker.tls ... | \(see above\) |
| pinot.broker.client.access.protocols | https |
| pinot.broker.client.access.protocols.https.port | 8443 |
| pinot.broker.nettytls.enabled | true |
| pinot.server.tls ... | \(see above\) |
| pinot.server.adminapi.access.protocols | https |
| pinot.server.adminapi.access.protocols.https.port | 7443 |
| pinot.server.netty.enabled | false |
| pinot.server.nettytls.enabled | true |
| pinot.server.nettytls.port | 8089 |

#### 2-way TLS

Apache Pinot also supports 2-way TLS for environments with high security requirements. This can be enabled per component with the optional `client.auth.enabled` flag. Bear in mind that any client \(or server\) interacting with a component expecting client auth must have access to both, a keystore and a truststore. This setting does NOT have apply to unsecured http or netty connections.

<table>
  <thead>
    <tr>
      <th style="text-align:left">key</th>
      <th style="text-align:left">value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left">controller ...</td>
      <td style="text-align:left">(see above)</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>controller.tls.client.auth.enabled</p>
        <p>(applies to client and internode connections)</p>
      </td>
      <td style="text-align:left">true</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.broker ...</td>
      <td style="text-align:left">(see above)</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>pinot.broker.tls.client.auth.enabled</p>
        <p>(applies to client and internode connections)</p>
      </td>
      <td style="text-align:left">true</td>
    </tr>
    <tr>
      <td style="text-align:left">pinot.server ...</td>
      <td style="text-align:left">(see above)</td>
    </tr>
    <tr>
      <td style="text-align:left">
        <p>pinot.server.tls.client.auth.enabled</p>
        <p>(applies to nettytls and adminapi)</p>
      </td>
      <td style="text-align:left">true</td>
    </tr>
  </tbody>
</table>

