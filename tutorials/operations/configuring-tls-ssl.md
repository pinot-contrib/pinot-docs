---
description: Set up TLS-secured connections inside and outside your cluster
---

# Configuring TLS/SSL

Pinot versions from 0.7.0+ support client-cluster and intra-cluster TLS. TLS-support comes in both 1-way and 2-way flavors. This guide walks through the relevant configuration options.

Looking to ingest from Kafka via secured connections? Check out [Kafka Streaming Ingestion with TLS/SSL](../../manage-data/data-import/pinot-stream-ingestion/import-from-apache-kafka.md#some-more-kafka-ingestion-configs).

### Listeners

In order to support incremental upgrades of unsecured pinot clusters towards TLS, we introduce multi-ingress support via listeners. Each listener accepts connections for a specific protocol on a specific port. For example, pinot-broker may be configured to accept both, **http** on port 8099 and **https** on port 8443 at the same time.

Existing configuration properties such as `controller.port` are still parsed and automatically translated to a http listener configuration to enable full backwards-compatibility. TLS-secured ingress must be configured through the new listener specifications.

### TLS upgrade

If you're bootstrapping a cluster from scratch, you can directly configure TLS-secured connections and you can forgo legacy http ingress. If you're upgrading an existing (production) cluster, you'll be able to perform the upgrade without downtime if your deployment is configured for high-availability.

On a high level, a zero-downtime upgrade includes the following 3 phases:

* adding a secondary TLS-secured ingress to pinot controllers, brokers, and servers
* switching client and internode egress to prefer TLS-secured connections
* disabling unsecured ingress

This requires a rolling restart of (replicated) service containers after each re-configuration phase. The sample listener specifications below will guide you through this process.

### Generating certificates

Apache Pinot leverages the JVM's native TLS infrastructure with all its benefits and limitations. Certificates should be generated to include the host IP, hostname, and fully-qualified domain names (if accessed or identified this way).

We support both, the JVM's default key/truststore, as well as configuration options to load certificates from secondary locations. Note, that **some connector plugins require the default truststore** to contain any trusted certs since they do not parse pinot's configuration properties for external truststores.

{% hint style="info" %}
Most JVM's default certificate store can be configured with command-line arguments:

`-Djavax.net.ssl.keyStore`\
`-Djavax.net.ssl.keyStorePassword`\
`-Djavax.net.ssl.trustStore`\
`-Djavax.net.ssl.trustStorePassword`
{% endhint %}


### Listener Specifications

This section contains a number of examples for common situations. The complete configuration reference can be found is each component's configuration reference.

If you're bootstrapping a new cluster, scroll down towards the end. We order this section for purposes of migrating an existing unsecured cluster to TLS-only.

#### Legacy HTTP config (unsecured)

This is a minimal example of network configuration options prior to 0.7.0. This specification is still supported for backwards-compatibility and translated internally to a listener specification.

<table>
  <thead>
    <tr>
      <th>key</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller.port</td>
      <td>9000</td>
    </tr>
    <tr>
      <td>pinot.broker.client.queryPort</td>
      <td>8099</td>
    </tr>
    <tr>
      <td>pinot.server.netty.port</td>
      <td>8098</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.port</td>
      <td>8097</td>
    </tr>
  </tbody>
</table>

#### HTTP with listener specification (unsecured)

This HTTP listener specification is the equivalent of manually translating the legacy configuration above to a listener specification.

<table>
  <thead>
    <tr>
      <th>key</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller.access.protocols</td>
      <td>http</td>
    </tr>
    <tr>
      <td>controller.access.protocols.http.port</td>
      <td>9000</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols</td>
      <td>http</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols.http.port</td>
      <td>8099</td>
    </tr>
    <tr>
      <td>pinot.server.netty.enabled</td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server.netty.port</td>
      <td>8098</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols</td>
      <td>http</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols.http.port</td>
      <td>8097</td>
    </tr>
  </tbody>
</table>

#### HTTP/HTTPS multi-ingress (unsecured egress)

This is a common scenario for development clusters and an intermediate phase during a zero-downtime migration of an unsecured cluster towards TLS. This configuration optionally accepts secure ingress on alternate ports, but still defaults to unsecured egress for all operations.

<table>
  <thead>
    <tr>
      <th>key</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller.tls.keystore.path</td>
      <td><p>/path/to/keystore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>controller.tls.keystore.password</td>
      <td><p>mykeystorepassword</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>controller.tls.truststore.path</td>
      <td><p>/path/to/truststore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>controller.tls.truststore.password</td>
      <td><p>mytruststorepassword</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>controller.access.protocols</td>
      <td>http,https</td>
    </tr>
    <tr>
      <td>controller.access.protocols.http.port</td>
      <td>9000</td>
    </tr>
    <tr>
      <td>controller.access.protocols.https.port</td>
      <td>9443</td>
    </tr>
    <tr>
      <td>pinot.broker.tls.keystore.path</td>
      <td><p>/path/to/keystore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.broker.tls.keystore.password</td>
      <td><p>mykeystorepassword</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.broker.tls.keystore.type</td>
      <td><p>PKCS12<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.broker.tls.truststore.path</td>
      <td><p>/path/to/truststore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.broker.tls.truststore.password</td>
      <td><p>mytruststorepassword</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.tls.truststore.type</td>
      <td><p>PKCS12 </p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols</td>
      <td>http,https</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols.http.port</td>
      <td>8099</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols.https.port</td>
      <td>8443</td>
    </tr>
    <tr>
      <td>pinot.server.tls.keystore.path</td>
      <td><p>/path/to/keystore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.tls.keystore.password</td>
      <td><p>mykeystorepassword</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.tls.keystore.type</td>
      <td><p>PKCS12</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.tls.truststore.path</td>
      <td><p>/path/to/truststore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.tls.truststore.password</td>
      <td><p>mytruststorepassword</p><p>(unset JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.tls.truststore.type</td>
      <td><p>PKCS12</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.server.netty.enabled</td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server.netty.port</td>
      <td>8098</td>
    </tr>
    <tr>
      <td>pinot.server.nettytls.enabled</td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server.nettytls.port</td>
      <td>8089</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols</td>
      <td>http,https</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols.http.port</td>
      <td>8097</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols.https.port</td>
      <td>7443</td>
    </tr>
    <tr>
      <td>pinot.minion.tls.keystore.path</td>
      <td><p>/path/to/keystore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.minion.tls.keystore.password</td>
      <td><p>mykeystorepassword</p><p>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.minion.tls.truststore.path</td>
      <td><p>/path/to/truststore<br>(unset for JVM default)</p></td>
    </tr>
    <tr>
      <td>pinot.minion.tls.truststore.password</td>
      <td><p>mytruststorepassword</p><p>(unset JVM default)</p></td>
    </tr>
  </tbody>
</table>

#### HTTP/HTTPS multi-ingress (secure egress)

After all pinot components have been configured and restarted to offer secure ingress, we can modify egress to default to secure connections internode. Clients, such as **pinot-admin.sh**, support an optional flag `-controllerProtocol https` to enable secure access. Ingestion jobs similarly support an optional `tlsSpec` key to configure key/trststores. Note, that any console clients must have access to appropriate certificates via the JVM's default key/truststore.

<table>
  <thead>
    <tr>
      <th>key</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller.tls ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>controller.access ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>controller.broker.protocol</td>
      <td>https</td>
    </tr>
    <tr>
      <td>controller.broker.port.override</td>
      <td>8443</td>
    </tr>
    <tr>
      <td>controller.vip.protocol</td>
      <td>https</td>
    </tr>
    <tr>
      <td>controller.vip.port</td>
      <td>9443</td>
    </tr>
    <tr>
      <td>pinot.broker.tls ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>pinot.broker.nettytls.enabled</td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>pinot.minion ...</td>
      <td>(see above)</td>
    </tr>
  </tbody>
</table>

#### TLS only

This is the default for a newly bootstrapped secure pinot cluster. It is also the final stage for any migration of an existing cluster. With this configuration applied, pinot's components will reject any unsecured connection attempt.

<table>
  <thead>
    <tr>
      <th>key</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller.tls ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>controller.access.protocols</td>
      <td>https</td>
    </tr>
    <tr>
      <td>controller.access.protocols.https.port</td>
      <td>9443</td>
    </tr>
    <tr>
      <td>controller.broker.protocol</td>
      <td>https</td>
    </tr>
    <tr>
      <td>controller.vip.protocol</td>
      <td>https</td>
    </tr>
    <tr>
      <td>controller.vip.port</td>
      <td>9443</td>
    </tr>
    <tr>
      <td>pinot.broker.tls ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols</td>
      <td>https</td>
    </tr>
    <tr>
      <td>pinot.broker.client.access.protocols.https.port</td>
      <td>8443</td>
    </tr>
    <tr>
      <td>pinot.broker.nettytls.enabled</td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server.tls ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols</td>
      <td>https</td>
    </tr>
    <tr>
      <td>pinot.server.adminapi.access.protocols.https.port</td>
      <td>7443</td>
    </tr>
    <tr>
      <td>pinot.server.netty.enabled</td>
      <td>false</td>
    </tr>
    <tr>
      <td>pinot.server.nettytls.enabled</td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server.nettytls.port</td>
      <td>8089</td>
    </tr>
    <tr>
      <td>pinot.minon.tls ...</td>
      <td>(see above)</td>
    </tr>
  </tbody>
</table>

#### 2-way TLS

Apache Pinot also supports 2-way TLS for environments with high security requirements. This can be enabled per component with the optional `client.auth.enabled` flag. Bear in mind that any client (or server) interacting with a component expecting client auth must have access to both, a keystore and a truststore. This setting does NOT have apply to unsecured http or netty connections.

<table>
  <thead>
    <tr>
      <th>key</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>controller ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td><p>controller.tls.client.auth.enabled</p><p>(applies to client and internode connections)</p></td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.broker ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td><p>pinot.broker.tls.client.auth.enabled</p><p>(applies to client and internode connections)</p></td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.server ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td><p>pinot.server.tls.client.auth.enabled</p><p>(applies to nettytls and adminapi)</p></td>
      <td>true</td>
    </tr>
    <tr>
      <td>pinot.minion ...</td>
      <td>(see above)</td>
    </tr>
    <tr>
      <td>pinot.minion.tls.client.auth.enabled</td>
      <td>true</td>
    </tr>
  </tbody>
</table>

### Multi-stage query engine

TLS can be enabled for the multi-stage query engine by setting the cluster config `pinot.multistage.engine.tls.enabled` to `true`. This enabled TLS for gRPC connections between brokers and servers (query plan dispatch from brokers to servers and final query result from servers to brokers) as well as servers and servers (data shuffle / exchange during execution of multi-stage queries).&#x20;

The existing TLS related configurations prefixed with `pinot.broker.` and `pinot.server.` are used to configure TLS on the gRPC connections between brokers and servers. When configuring TLS for the multi-stage query engine, keep in mind that brokers and servers can be both gRPC clients as well as servers. Brokers are gRPC clients when dispatching a query plan to Pinot servers and gRPC servers when receiving the final query results from a Pinot server; Pinot servers can be both gRPC clients and servers during data shuffle / exchange in the execution of multi-stage queries.
