# Controller

Most of the properties in Pinot are set in Zookeeper via Helix. However, you can also set properties in `controller.conf` file. You can specify the path to config file at the startup time as follows -

```
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

`Controller.conf` can have the following properties -

## Primary Configuration

| Property                                             | Default                                                                  | Description                                                                              |
| ---------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| controller.vip.host                                  | same as `controller.host`                                                | The VIP hostname used to set the download URL for segments                               |
| controller.vip.port                                  | same as `controller.port`                                                |                                                                                          |
| controller.vip.protocol                              |                                                                          |                                                                                          |
| controller.host                                      | localhost                                                                | The ip of the host on which controller is running                                        |
| controller.port                                      | 9000                                                                     | The port on which controller should run                                                  |
| controller.access.protocol                           |                                                                          |                                                                                          |
| controller.data.dir                                  | ${java.io.tmpdir}/PinotController                                        | Directory to host segment data                                                           |
| controller.local.temp.dir                            |                                                                          |                                                                                          |
| controller.zk.str                                    | localhost:2181                                                           | zookeeper host:port string to connect                                                    |
| controller.update\_segment\_state\_model             | false                                                                    |                                                                                          |
| controller.helix.cluster.name                        |                                                                          | Pinot Cluster Name, required.                                                            |
| controller.tenant.isolation.enable                   | true                                                                     | Enable Tenant Isolation, default is single tenant cluste                                 |
| controller.enable.split.commit                       | false                                                                    |                                                                                          |
| controller.query.console.useHttps                    | false                                                                    | use https instead of http for cluster                                                    |
| controller.upload.onlineToOfflineTimeout             | 2 minutes                                                                |                                                                                          |
| controller.mode                                      | `dual`                                                                   | Should be one of `helix_only`, `pinot_only` or `dual`                                    |
| controller.resource.rebalance.strategy               | `org.apache.helix.controller. rebalancer.strategy.AutoRebalanceStrategy` |                                                                                          |
| controller.realtime.segment.commit.timeoutSeconds    | 120 seconds                                                              | request timeout for segment commit                                                       |
| controller.deleted.segments.retentionInDays          | 7 days                                                                   | duration for which to retain deleted segments                                            |
| controller.admin.access.control.factory.class        | `org.apache.pinot.controller. api.access.AllowAllAccessFactory`          |                                                                                          |
| controller.segment.upload.timeoutInMillis            | 10 minutes                                                               | timeout for upload of segments.                                                          |
| controller.realtime.segment.metadata.commit.numLocks | 64                                                                       |                                                                                          |
| controller.enable.storage.quota.check                | true                                                                     |                                                                                          |
| controller.enable.batch.message.mode                 | false                                                                    |                                                                                          |
| controller.allow.hlc.tables                          | true                                                                     |                                                                                          |
| controller.storage.factory.class.file                | `org.apache.pinot.spi. filesystem.LocalPinotFS`                          |                                                                                          |
| table.minReplicas                                    | 1                                                                        |                                                                                          |
| controller.access.protocols                          | http                                                                     | Ingress protocols to access controller (http or https or http,https)                     |
| controller.access.protocols.http.port                |                                                                          | Port to access controller via http                                                       |
| controller.broker.protocols.https.port               |                                                                          | Port to access controller via https                                                      |
| controller.broker.protocol                           | http                                                                     | protocol for forwarding query requests (http or https)                                   |
| controller.broker.port.override                      |                                                                          | override for broker port when forwarding query requests (use in multi-ingress scenarios) |
| controller.tls.keystore.path                         |                                                                          | Path to controller TLS keystore                                                          |
| controller.tls.keystore.password                     |                                                                          | keystore password                                                                        |
| controller.tls.truststore.path                       |                                                                          | Path to controller TLS truststore                                                        |
| controller.tls.truststore.password                   |                                                                          | truststore password                                                                      |
| controller.tls.client.auth                           | false                                                                    | toggle for requiring TLS client auth                                                     |
| controller.http.server.thread.pool.corePoolSize      | 2 * cores                                                                | Config for the thread-pool used by pinot-controller's http-server.                       |
| controller.http.server.thread.pool.maxPoolSize       | 2 * cores                                                                | Config for the thread-pool used by pinot-controller's http-server.                       |

## Periodic Tasks Configuration

Refer to [Periodic tasks](../basics/components/controller.md#controller-periodic-tasks)
