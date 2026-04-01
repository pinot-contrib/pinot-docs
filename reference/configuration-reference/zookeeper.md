# Zookeeper

ZooKeeper stores Pinot cluster metadata.

That includes schemas, table configs, segment metadata, and Helix state.

### When you need to care

You can keep ZooKeeper “default” for quickstarts.

You should tune and secure it for production.

Typical reasons:

* You run a multi-node Pinot cluster.
* You want TLS for ZooKeeper client connections.
* You use ZooKeeper ACLs / SASL auth.
* Your cluster metadata outgrows the default znode limit (1 MB).

### Recommended baseline configuration

Run a ZooKeeper ensemble in production.

Use an odd number of nodes (3 or 5).

Put `dataDir` on fast local disk.

Turn on snapshot cleanup to avoid disk-full incidents.

{% hint style="info" %}
Pinot depends on ZooKeeper for cluster coordination.

Treat it like “control plane” infrastructure.
{% endhint %}

#### Example `zoo.cfg` baseline

Use this as a starting point.

Adapt paths, ports, and node lists.

```properties
# Core
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181

# Ensemble (example)
initLimit=10
syncLimit=5
server.1=zk-1:2888:3888
server.2=zk-2:2888:3888
server.3=zk-3:2888:3888

# Cleanup
autopurge.snapRetainCount=10
autopurge.purgeInterval=24
```

### Point Pinot at ZooKeeper

All Pinot components need the ZooKeeper connection string.

* In scripts and containers, this is usually `-zkAddress`.
* In `controller.conf`, it’s `controller.zk.str`.

You can optionally use a chroot path to isolate clusters:

```
zk-1:2181,zk-2:2181,zk-3:2181/pinot-prod
```

### Secure ZooKeeper with TLS

ZooKeeper can serve TLS on a separate port (recommended).

This avoids breaking legacy clients on `clientPort`.

You need to do two things:

1. Enable TLS on ZooKeeper servers.
2. Configure Pinot JVMs to use ZooKeeper TLS.

#### 1) ZooKeeper server: enable TLS client port

ZooKeeper TLS settings can be configured in `zoo.cfg`.

Exact keys vary by ZooKeeper version.

Common options (ZooKeeper 3.5+):

```properties
secureClientPort=2281

# Key material (server side)
ssl.keyStore.location=/etc/zookeeper/keystore.p12
ssl.keyStore.password=changeit
ssl.keyStore.type=PKCS12

ssl.trustStore.location=/etc/zookeeper/truststore.p12
ssl.trustStore.password=changeit
ssl.trustStore.type=PKCS12

# Optional hardening
ssl.hostnameVerification=true
ssl.clientAuth=none
```

{% hint style="warning" %}
Always validate the exact property names against your ZooKeeper version.

See the ZooKeeper Admin Guide for your release.
{% endhint %}

#### 2) Pinot JVM: ZooKeeper TLS Java options

Pinot (Helix) uses the ZooKeeper Java client.

The ZooKeeper client is configured via JVM system properties.

Set these JVM options on **every Pinot component** (controller, broker, server, minion):

```
-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
-Dzookeeper.client.secure=true
-Dzookeeper.ssl.keyStore.location=/etc/pinot/keystore.p12
-Dzookeeper.ssl.keyStore.password=changeit
-Dzookeeper.ssl.keyStore.type=PKCS12
-Dzookeeper.ssl.trustStore.location=/etc/pinot/truststore.p12
-Dzookeeper.ssl.trustStore.password=changeit
-Dzookeeper.ssl.trustStore.type=PKCS12
```

How you set them depends on your runtime:

* **pinot-admin.sh / launcher scripts**: set `JAVA_OPTS` (or equivalent) before starting.
* **Kubernetes**: add them to `JAVA_OPTS` in the container env.
* **Systemd**: add them to the service unit environment.

Then point Pinot at the TLS port:

```
zk-1:2281,zk-2:2281,zk-3:2281/pinot-prod
```

{% hint style="info" %}
These are ZooKeeper-client properties, not Pinot properties.

They work because Pinot runs on the JVM.
{% endhint %}

### Secure ZooKeeper with auth (SASL / JAAS)

ZooKeeper supports ACL enforcement and SASL authentication.

This is common with Kerberos-backed environments.

High-level steps:

1. Enable SASL auth on ZooKeeper.
2. Provide a JAAS config to Pinot JVMs.
3. Restart ZooKeeper and Pinot.

#### ZooKeeper server: enable SASL provider

Example `zoo.cfg`:

```properties
authProvider.1=org.apache.zookeeper.server.auth.SASLAuthenticationProvider
requireClientAuthScheme=sasl
```

#### Pinot JVM: SASL Java options

Set JVM options on every Pinot component:

```
-Dzookeeper.sasl.client=true
-Djava.security.auth.login.config=/etc/pinot/zk_client_jaas.conf
```

If you run multiple JAAS contexts, you may also need:

```
-Dzookeeper.sasl.clientconfig=Client
```

{% hint style="danger" %}
Helix expects to read and write znodes.

If ACLs deny writes, Pinot will fail in non-obvious ways.
{% endhint %}

### Related Pinot guides

* [Configuring TLS/SSL](../../operate-pinot/configuring-tls-ssl.md)
* [Authentication](../../operate-pinot/authentication)

### Increase znode size for large clusters (large tables)

ZooKeeper limits the maximum znode payload size.

The default is 1 MB.

Large Pinot tables can exceed this when:

* You have very high segment counts.
* Your Helix `IDEALSTATE` / `EXTERNALVIEW` becomes large.

Symptoms include:

```
java.io.ioexception: packet len ... is out of range!
```

#### Fix: increase `jute.maxbuffer` everywhere

Set `jute.maxbuffer` on:

* **All ZooKeeper servers**
* **All Pinot components** (ZooKeeper clients)

Example (4 MB):

```
-Djute.maxbuffer=4000000
```

Restart order:

1. Rolling restart ZooKeeper ensemble.
2. Rolling restart Pinot components.

For deeper troubleshooting and alternatives, see [Troubleshoot issues with ZooKeeper znodes](../../operate-pinot/troubleshooting/troubleshoot-zookeeper.md).

#### Prefer fewer segments over bigger znodes

Increasing `jute.maxbuffer` is a safety valve.

It is not a scaling strategy.

Also do at least one of these:

* Create bigger segments via [Segment threshold](../../basics/concepts/segment-threshold.md).
* Merge small segments via the [Minion merge rollup task](../../operators/operating-pinot/minion-merge-rollup-task.md).
* Delete old segments via table retention.
