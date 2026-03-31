# Helm Chart Values Reference

This page provides a comprehensive reference for the Apache Pinot Helm chart configuration values. Use this guide when deploying or customizing Pinot on Kubernetes.

## Chart Overview

| Field | Value |
| --- | --- |
| Chart Name | `pinot` |
| Chart Version | `1.0.0` |
| App Version | `1.0.0` |
| Source | [github.com/apache/pinot/tree/master/helm](https://github.com/apache/pinot/tree/master/helm) |
| Maintainer | `dev@pinot.apache.org` |

## Prerequisites

* Kubernetes 1.20+
* Helm 3.x
* `kubectl` configured to connect to your cluster
* Persistent volume provisioner support in the cluster (for controller, server, and ZooKeeper data)
* A StorageClass appropriate for your cloud provider:
  * AWS: `gp2` or `gp3`
  * GCP: `pd-ssd` or `standard`
  * Azure: `AzureDisk`
  * Docker Desktop: `hostpath`

{% hint style="warning" %}
Do not use blob-store-backed storage classes (such as AzureFile, GCS FUSE, or S3-based CSI) for Pinot data volumes. Use only block storage (EBS, Persistent Disk, Azure Disk).
{% endhint %}

## Global Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `image.repository` | Pinot container image repository | `apachepinot/pinot` |
| `image.tag` | Pinot container image tag | `latest` |
| `image.pullPolicy` | Image pull policy | `Always` |
| `cluster.name` | Pinot cluster name | `pinot-quickstart` |
| `imagePullSecrets` | Docker registry secret names | `[]` |
| `terminationGracePeriodSeconds` | Grace period for pod termination | `30` |
| `securityContext` | Pod-level security context | `{}` |
| `serviceAccount.create` | Create a service account | `true` |
| `serviceAccount.annotations` | Service account annotations | `{}` |
| `serviceAccount.name` | Service account name (auto-generated if empty) | `""` |
| `additionalMatchLabels` | Extra labels for pod selectors | `{}` |

### Default Probe Settings

These defaults apply to all components unless overridden at the component level.

| Parameter | Description | Default |
| --- | --- | --- |
| `probes.initialDelaySeconds` | Seconds before probes start | `60` |
| `probes.periodSeconds` | Probe interval | `10` |
| `probes.failureThreshold` | Failures before marking unhealthy | `10` |
| `probes.successThreshold` | Successes before marking healthy | `1` |
| `probes.timeoutSeconds` | Probe timeout | `10` |

## Authentication

| Parameter | Description | Default |
| --- | --- | --- |
| `pinotAuth.enabled` | Enable Pinot basic auth | `false` |
| `pinotAuth.controllerFactoryClass` | Controller access control factory | `org.apache.pinot.controller.api.access.BasicAuthAccessControlFactory` |
| `pinotAuth.brokerFactoryClass` | Broker access control factory | `org.apache.pinot.broker.broker.BasicAuthAccessControlFactory` |
| `pinotAuth.configs` | Auth config lines (principals, passwords, permissions) | `[]` |

## Controller

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.name` | Controller component name | `controller` |
| `controller.replicaCount` | Number of controller replicas | `1` |
| `controller.configureControllerPort` | Include `controller.port` in config | `true` |
| `controller.podManagementPolicy` | StatefulSet pod management policy | `Parallel` |
| `controller.startCommand` | Start command for the container | `StartController` |

### Controller Resources and JVM

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.resources.requests.memory` | Memory request | `1.25Gi` |
| `controller.jvmOpts` | JVM options for the controller | `-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...` |
| `controller.log4j2ConfFile` | Log4j2 configuration file path | `/opt/pinot/etc/conf/pinot-controller-log4j2.xml` |
| `controller.pluginsDir` | Plugins directory | `/opt/pinot/plugins` |

### Controller Persistence

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.persistence.enabled` | Enable PVC for controller data | `true` |
| `controller.persistence.accessMode` | PVC access mode | `ReadWriteOnce` |
| `controller.persistence.size` | PVC size | `1G` |
| `controller.persistence.mountPath` | Data mount path | `/var/pinot/controller/data` |
| `controller.persistence.storageClass` | Storage class (empty for default) | `""` |
| `controller.persistence.extraVolumes` | Additional volumes | `[]` |
| `controller.persistence.extraVolumeMounts` | Additional volume mounts | `[]` |

### Controller Data Directory

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.data.dir` | Controller data directory | `/var/pinot/controller/data` |

### Controller VIP

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.vip.enabled` | Enable VIP host | `false` |
| `controller.vip.host` | VIP hostname | `pinot-controller` |
| `controller.vip.port` | VIP port | `9000` |

### Controller Service

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.service.type` | Headless service type | `ClusterIP` |
| `controller.service.clusterIP` | Cluster IP (None for headless) | `None` |
| `controller.service.port` | Service port | `9000` |
| `controller.service.protocol` | Service protocol | `TCP` |
| `controller.service.name` | Service port name | `controller` |
| `controller.service.nodePort` | Node port (if type is NodePort) | `""` |
| `controller.service.annotations` | Service annotations | `{}` |
| `controller.service.extraPorts` | Additional ports to expose | `[]` |

### Controller External Service

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.external.enabled` | Expose controller externally | `true` |
| `controller.external.type` | External service type | `LoadBalancer` |
| `controller.external.port` | External service port | `9000` |
| `controller.external.annotations` | External service annotations | `{}` |

### Controller Ingress

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.ingress.v1.enabled` | Enable v1 Ingress | `false` |
| `controller.ingress.v1.ingressClassName` | Ingress class name | `""` |
| `controller.ingress.v1.annotations` | Ingress annotations | `{}` |
| `controller.ingress.v1.tls` | TLS configuration | `[]` |
| `controller.ingress.v1.path` | Ingress path | `/` |
| `controller.ingress.v1.hosts` | Ingress hostnames | `[]` |

### Controller Probes

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.probes.endpoint` | Health check endpoint | `/health` |
| `controller.probes.livenessEnabled` | Enable liveness probe | `false` |
| `controller.probes.readinessEnabled` | Enable readiness probe | `false` |
| `controller.probes.startupEnabled` | Enable startup probe | `false` |

### Controller Scheduling and Miscellaneous

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.nodeSelector` | Node selector labels | `{}` |
| `controller.tolerations` | Pod tolerations | `[]` |
| `controller.affinity` | Pod affinity rules | `{}` |
| `controller.podAnnotations` | Pod annotations | `{}` |
| `controller.initContainers` | Init containers | `[]` |
| `controller.podSecurityContext` | Pod security context | `{}` |
| `controller.securityContext` | Container security context | `{}` |
| `controller.updateStrategy.type` | StatefulSet update strategy | `RollingUpdate` |
| `controller.automaticReload.enabled` | Auto-roll on ConfigMap change | `false` |
| `controller.envFrom` | ConfigMap/Secret references for env vars | `[]` |
| `controller.extraEnv` | Extra environment variables | `[{name: LOG4J_CONSOLE_LEVEL, value: info}]` |
| `controller.extra.configs` | Extra lines appended to pinot-controller.conf | `pinot.set.instance.id.to.hostname=true` |

### Controller PodDisruptionBudget

| Parameter | Description | Default |
| --- | --- | --- |
| `controller.pdb.enabled` | Enable PDB | `false` |
| `controller.pdb.minAvailable` | Minimum available pods | `""` |
| `controller.pdb.maxUnavailable` | Maximum unavailable pods | `50%` |

## Broker

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.name` | Broker component name | `broker` |
| `broker.replicaCount` | Number of broker replicas | `1` |
| `broker.configureBrokerPort` | Include `pinot.broker.client.queryPort` in config | `true` |
| `broker.podManagementPolicy` | StatefulSet pod management policy | `Parallel` |
| `broker.startCommand` | Start command for the container | `StartBroker` |

### Broker Resources and JVM

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.resources.requests.memory` | Memory request | `1.25Gi` |
| `broker.jvmOpts` | JVM options for the broker | `-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...` |
| `broker.log4j2ConfFile` | Log4j2 configuration file path | `/opt/pinot/etc/conf/pinot-broker-log4j2.xml` |
| `broker.pluginsDir` | Plugins directory | `/opt/pinot/plugins` |
| `broker.routingTable.builderClass` | Routing table builder class | `random` |

### Broker Service

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.service.type` | Headless service type | `ClusterIP` |
| `broker.service.clusterIP` | Cluster IP (None for headless) | `None` |
| `broker.service.port` | Service port | `8099` |
| `broker.service.protocol` | Service protocol | `TCP` |
| `broker.service.name` | Service port name | `broker` |
| `broker.service.nodePort` | Node port (if type is NodePort) | `""` |
| `broker.service.annotations` | Service annotations | `{}` |
| `broker.service.extraPorts` | Additional ports to expose | `[]` |

### Broker External Service

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.external.enabled` | Expose broker externally | `true` |
| `broker.external.type` | External service type | `LoadBalancer` |
| `broker.external.port` | External service port | `8099` |
| `broker.external.annotations` | External service annotations | `{}` |

### Broker Ingress

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.ingress.v1.enabled` | Enable v1 Ingress | `false` |
| `broker.ingress.v1.ingressClassName` | Ingress class name | `""` |
| `broker.ingress.v1.annotations` | Ingress annotations | `{}` |
| `broker.ingress.v1.tls` | TLS configuration | `[]` |
| `broker.ingress.v1.path` | Ingress path | `/` |
| `broker.ingress.v1.hosts` | Ingress hostnames | `[]` |

### Broker Probes

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.probes.endpoint` | Health check endpoint | `/health` |
| `broker.probes.livenessEnabled` | Enable liveness probe | `true` |
| `broker.probes.readinessEnabled` | Enable readiness probe | `true` |
| `broker.probes.startupEnabled` | Enable startup probe | `false` |

### Broker Scheduling and Miscellaneous

| Parameter | Description | Default |
| --- | --- | --- |
| `broker.nodeSelector` | Node selector labels | `{}` |
| `broker.tolerations` | Pod tolerations | `[]` |
| `broker.affinity` | Pod affinity rules | `{}` |
| `broker.podAnnotations` | Pod annotations | `{}` |
| `broker.initContainers` | Init containers | `[]` |
| `broker.podSecurityContext` | Pod security context | `{}` |
| `broker.securityContext` | Container security context | `{}` |
| `broker.updateStrategy.type` | StatefulSet update strategy | `RollingUpdate` |
| `broker.automaticReload.enabled` | Auto-roll on ConfigMap change | `false` |
| `broker.envFrom` | ConfigMap/Secret references for env vars | `[]` |
| `broker.extraEnv` | Extra environment variables | `[{name: LOG4J_CONSOLE_LEVEL, value: info}]` |
| `broker.extra.configs` | Extra lines appended to pinot-broker.conf | `pinot.set.instance.id.to.hostname=true` |
| `broker.pdb.enabled` | Enable PDB | `false` |
| `broker.pdb.maxUnavailable` | Maximum unavailable pods | `50%` |

## Server

| Parameter | Description | Default |
| --- | --- | --- |
| `server.name` | Server component name | `server` |
| `server.replicaCount` | Number of server replicas | `1` |
| `server.configureServerPort` | Include `pinot.server.netty.port` in config | `true` |
| `server.podManagementPolicy` | StatefulSet pod management policy | `Parallel` |
| `server.startCommand` | Start command for the container | `StartServer` |

### Server Resources and JVM

| Parameter | Description | Default |
| --- | --- | --- |
| `server.resources.requests.memory` | Memory request | `1.25Gi` |
| `server.jvmOpts` | JVM options for the server | `-Xms512M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...` |
| `server.log4j2ConfFile` | Log4j2 configuration file path | `/opt/pinot/etc/conf/pinot-server-log4j2.xml` |
| `server.pluginsDir` | Plugins directory | `/opt/pinot/plugins` |

### Server Data Directories

| Parameter | Description | Default |
| --- | --- | --- |
| `server.dataDir` | Index data directory | `/var/pinot/server/data/index` |
| `server.segmentTarDir` | Segment tar directory | `/var/pinot/server/data/segment` |

### Server Persistence

| Parameter | Description | Default |
| --- | --- | --- |
| `server.persistence.enabled` | Enable PVC for server data | `true` |
| `server.persistence.accessMode` | PVC access mode | `ReadWriteOnce` |
| `server.persistence.size` | PVC size | `4G` |
| `server.persistence.mountPath` | Data mount path | `/var/pinot/server/data` |
| `server.persistence.storageClass` | Storage class (empty for default) | `""` |
| `server.persistence.extraVolumes` | Additional volumes | `[]` |
| `server.persistence.extraVolumeMounts` | Additional volume mounts | `[]` |

### Server Service

| Parameter | Description | Default |
| --- | --- | --- |
| `server.service.type` | Service type | `ClusterIP` |
| `server.service.nettyPort` | Netty data port | `8098` |
| `server.service.nettyPortName` | Netty port name | `netty` |
| `server.service.adminPort` | Admin HTTP port | `8097` |
| `server.service.adminExposePort` | Admin exposed port | `80` |
| `server.service.adminPortName` | Admin port name | `admin` |
| `server.service.nodePort` | Node port (if type is NodePort) | `""` |
| `server.service.protocol` | Service protocol | `TCP` |
| `server.service.annotations` | Service annotations | `{}` |
| `server.service.extraPorts` | Additional ports to expose | `[]` |

### Server Probes

| Parameter | Description | Default |
| --- | --- | --- |
| `server.probes.endpoint` | Health check endpoint | `/health` |
| `server.probes.livenessEnabled` | Enable liveness probe | `false` |
| `server.probes.readinessEnabled` | Enable readiness probe | `false` |
| `server.probes.startupEnabled` | Enable startup probe | `false` |
| `server.probes.liveness.endpoint` | Liveness-specific endpoint | `/health/liveness` |
| `server.probes.readiness.endpoint` | Readiness-specific endpoint | `/health/readiness` |

### Server Scheduling and Miscellaneous

| Parameter | Description | Default |
| --- | --- | --- |
| `server.nodeSelector` | Node selector labels | `{}` |
| `server.tolerations` | Pod tolerations | `[]` |
| `server.affinity` | Pod affinity rules | `{}` |
| `server.podAnnotations` | Pod annotations | `{}` |
| `server.initContainers` | Init containers | `[]` |
| `server.podSecurityContext` | Pod security context | `{}` |
| `server.securityContext` | Container security context | `{}` |
| `server.updateStrategy.type` | StatefulSet update strategy | `RollingUpdate` |
| `server.automaticReload.enabled` | Auto-roll on ConfigMap change | `false` |
| `server.envFrom` | ConfigMap/Secret references for env vars | `[]` |
| `server.extraEnv` | Extra environment variables | `[{name: LOG4J_CONSOLE_LEVEL, value: info}]` |
| `server.extra.configs` | Extra lines appended to pinot-server.conf | See values.yaml |
| `server.pdb.enabled` | Enable PDB | `false` |
| `server.pdb.maxUnavailable` | Maximum unavailable pods | `1` |

## Minion (StatefulSet)

| Parameter | Description | Default |
| --- | --- | --- |
| `minion.enabled` | Deploy Minion StatefulSet | `false` |
| `minion.name` | Minion component name | `minion` |
| `minion.replicaCount` | Number of minion replicas | `0` |
| `minion.configureMinionPort` | Include `pinot.minion.port` in config | `true` |
| `minion.podManagementPolicy` | StatefulSet pod management policy | `Parallel` |
| `minion.startCommand` | Start command for the container | `StartMinion` |
| `minion.resources.requests.memory` | Memory request | `1.25Gi` |
| `minion.jvmOpts` | JVM options for minion | `-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...` |
| `minion.dataDir` | Minion data directory | `/var/pinot/minion/data` |
| `minion.persistence.enabled` | Enable PVC for minion data | `true` |
| `minion.persistence.size` | PVC size | `4G` |
| `minion.persistence.storageClass` | Storage class (empty for default) | `""` |
| `minion.service.port` | Service port | `9514` |
| `minion.extra.configs` | Extra lines appended to pinot-minion.conf | `pinot.set.instance.id.to.hostname=true` |
| `minion.pdb.enabled` | Enable PDB | `false` |
| `minion.pdb.maxUnavailable` | Maximum unavailable pods | `1` |

## Minion Stateless (Deployment)

The stateless minion runs as a Kubernetes Deployment instead of a StatefulSet, making it suitable for ephemeral task execution.

| Parameter | Description | Default |
| --- | --- | --- |
| `minionStateless.enabled` | Deploy Minion Stateless Deployment | `true` |
| `minionStateless.name` | Component name | `minion-stateless` |
| `minionStateless.replicaCount` | Number of replicas | `1` |
| `minionStateless.configureMinionStatelessPort` | Include `pinot.minion.port` in config | `true` |
| `minionStateless.startCommand` | Start command | `StartMinion` |
| `minionStateless.resources.requests.memory` | Memory request | `1.25Gi` |
| `minionStateless.jvmOpts` | JVM options | `-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G ...` |
| `minionStateless.persistence.enabled` | Enable PVC | `false` |
| `minionStateless.persistence.size` | PVC size (when enabled) | `4G` |
| `minionStateless.service.port` | Service port | `9514` |
| `minionStateless.extra.configs` | Extra config lines | `pinot.set.instance.id.to.hostname=true` |
| `minionStateless.pdb.enabled` | Enable PDB | `false` |
| `minionStateless.pdb.maxUnavailable` | Maximum unavailable pods | `1` |

## ZooKeeper

As of chart version 1.0.0, the chart includes native Apache ZooKeeper Kubernetes templates, replacing the previous Bitnami dependency. You can either use the built-in ZooKeeper or point to an external ensemble.

{% hint style="warning" %}
**Breaking Changes in v1.0.0**: This release introduces breaking changes from the Bitnami-based ZooKeeper:
- StatefulSet selector labels changed from Bitnami defaults to new labels (`app: pinot, component: zookeeper`)
- Data mount path changed from `/bitnami/zookeeper` to `/data`
- Datalog volume claim template renamed from `data-log` to `datalog`
- Bitnami-specific parameters removed: `image.registry`, `global.security.allowInsecureImages`, `tls.*`, `auth.*`

See the [migration guidance](#zookeeper-migration-guide) section below for upgrade instructions.
{% endhint %}

{% hint style="info" %}
For production deployments, consider using the [ZooKeeper Kubernetes Operator](https://github.com/pravega/zookeeper-operator) instead of the bundled chart.
{% endhint %}

| Parameter | Description | Default |
| --- | --- | --- |
| `zookeeper.enabled` | Install bundled ZooKeeper | `true` |
| `zookeeper.urlOverride` | External ZooKeeper connection string (used when `enabled: false`) | `my-zookeeper:2181/my-pinot` |
| `zookeeper.port` | ZooKeeper client port | `2181` |
| `zookeeper.replicaCount` | Number of ZooKeeper replicas | `1` |
| `zookeeper.resources.requests.memory` | Memory request | `1.25Gi` |
| `zookeeper.heapSize` | Java heap size in MB | `1024` |
| `zookeeper.jvmFlags` | Extra JVM flags | `-Djute.maxbuffer=4000000` |
| `zookeeper.persistence.enabled` | Enable persistent storage | `true` |
| `zookeeper.persistence.storageClass` | Storage class | `""` |
| `zookeeper.persistence.size` | PVC size | `8Gi` |
| `zookeeper.autopurge.purgeInterval` | Purge interval in hours | `1` |
| `zookeeper.autopurge.snapRetainCount` | Snapshots to retain | `5` |
| `zookeeper.image.repository` | ZooKeeper image (Apache official) | `zookeeper` |
| `zookeeper.image.tag` | ZooKeeper image tag | `3.9.3` |
| `zookeeper.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `zookeeper.affinity` | Pod affinity rules | `{}` |

### Using an External ZooKeeper

To connect to an existing ZooKeeper ensemble, disable the built-in one and set the URL override:

```yaml
zookeeper:
  enabled: false
  urlOverride: "zk-0.zk-svc:2181,zk-1.zk-svc:2181,zk-2.zk-svc:2181/pinot"
```

### ZooKeeper Migration Guide

If you are upgrading from chart version 0.3.6 (Bitnami-based) to 1.0.0 (native templates), follow one of these migration strategies:

#### Option 1: Fresh Installation (Recommended for non-production clusters)

Delete the existing ZooKeeper StatefulSet and let the chart recreate it with the new templates:

```bash
helm repo update
helm upgrade pinot pinot/pinot -n pinot-quickstart --set zookeeper.enabled=true
kubectl delete statefulset -n pinot-quickstart pinot-zookeeper
```

#### Option 2: Data Migration (For production clusters with existing data)

{% hint style="warning" %}
**Snapshot/log separation required**: The Bitnami image stores both snapshots and transaction logs together in `/bitnami/zookeeper/data/version-2/`. The new chart uses separate directories: `/data` for snapshots and `/datalog` for transaction logs. The restore procedure below handles this separation automatically. If snapshots and logs are not separated, ZooKeeper will refuse to start with: `Snapshot directory has log files`.
{% endhint %}

{% hint style="info" %}
If your old deployment used `replicaCount > 1`, repeat the backup (step 1) for each pod (e.g. `pinot-zookeeper-1`, `pinot-zookeeper-2`) and restore from the pod that was the ZooKeeper leader.
{% endhint %}

1. **Back up ZooKeeper data** while the old cluster is still running:
```bash
NAMESPACE=pinot-quickstart
RELEASE=pinot
kubectl cp ${NAMESPACE}/${RELEASE}-zookeeper-0:/bitnami/zookeeper/data ./zk-data-backup
```

2. **Scale down Pinot components** (controller, broker, server) to stop accessing ZooKeeper:
```bash
kubectl scale statefulset pinot-controller -n pinot-quickstart --replicas=0
kubectl scale statefulset pinot-broker -n pinot-quickstart --replicas=0
kubectl scale statefulset pinot-server -n pinot-quickstart --replicas=0
```

3. **Delete the old ZooKeeper StatefulSet** (PVC data is preserved):
```bash
kubectl delete statefulset pinot-zookeeper -n pinot-quickstart --cascade=orphan
```

4. **Update and install the new chart**:
```bash
helm repo update
helm upgrade pinot pinot/pinot -n pinot-quickstart -f values.yaml
```

5. **Wait for the new ZooKeeper to be ready**:
```bash
kubectl rollout status statefulset/pinot-zookeeper -n pinot-quickstart
```

6. **Scale down ZooKeeper** so you can safely restore data to the PVCs:
```bash
kubectl scale statefulset/${RELEASE}-zookeeper --replicas=0 -n ${NAMESPACE}
```

7. **Launch a temporary pod** to mount both PVCs and restore data with proper snapshot/log separation:
```bash
cat <<EOF | kubectl apply -n ${NAMESPACE} -f -
apiVersion: v1
kind: Pod
metadata:
  name: zk-data-restore
spec:
  containers:
  - name: restore
    image: busybox
    command: ["sleep", "3600"]
    volumeMounts:
    - name: data
      mountPath: /data
    - name: datalog
      mountPath: /datalog
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data-${RELEASE}-zookeeper-0
  - name: datalog
    persistentVolumeClaim:
      claimName: datalog-${RELEASE}-zookeeper-0
  restartPolicy: Never
EOF
kubectl wait --for=condition=ready pod/zk-data-restore -n ${NAMESPACE} --timeout=10m
```

8. **Copy backup and separate snapshots from transaction logs**:
```bash
kubectl cp ./zk-data-backup/. ${NAMESPACE}/zk-data-restore:/data
kubectl exec -n ${NAMESPACE} zk-data-restore -- \
  sh -c 'mkdir -p /datalog/version-2 && mv /data/version-2/log.* /datalog/version-2/'
```

9. **Clean up the restore pod and scale ZooKeeper back up**:
```bash
kubectl delete pod zk-data-restore -n ${NAMESPACE}
kubectl scale statefulset/${RELEASE}-zookeeper --replicas=1 -n ${NAMESPACE}
kubectl rollout status statefulset/${RELEASE}-zookeeper -n ${NAMESPACE}
```

10. **Verify ZooKeeper is healthy**:
```bash
kubectl exec -n ${NAMESPACE} ${RELEASE}-zookeeper-0 -- \
  bash -c 'echo ruok | nc localhost 2181'
# Expected output: imok
```

11. **Restart Pinot components** and verify cluster state:
```bash
kubectl scale statefulset pinot-controller -n pinot-quickstart --replicas=3
kubectl scale statefulset pinot-broker -n pinot-quickstart --replicas=3
kubectl scale statefulset pinot-server -n pinot-quickstart --replicas=4
kubectl exec -n pinot-quickstart pinot-controller-0 -- \
  curl -s http://localhost:9000/instances
```

#### Option 3: Use External ZooKeeper

If you have an existing external ZooKeeper ensemble that you want to continue using, disable the bundled ZooKeeper:

```yaml
zookeeper:
  enabled: false
  urlOverride: "your-zk-ensemble:2181/pinot"
```

### Breaking Changes Summary

| Aspect | Bitnami (v0.3.6) | Native (v1.0.0) |
| --- | --- | --- |
| Image | `bitnamilegacy/zookeeper:3.9.3-debian-12-r22` | `zookeeper:3.9.3` |
| StatefulSet Selectors | `app.kubernetes.io/name: zookeeper` | `app: pinot, component: zookeeper` |
| Data Mount Path | `/bitnami/zookeeper` | `/data` |
| Datalog VCT | `data-log` | `datalog` |
| Removed Parameters | `image.registry`, `global.security.*`, `tls.*`, `auth.*` | N/A |

## Deep Store Configuration

By default, the controller local filesystem is used as the deep store. For production, configure an external deep store using `controller.extra.configs` and `server.extra.configs`.

### Amazon S3

```yaml
controller:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      controller.task.scheduler.enabled=true
      pinot.controller.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
      pinot.controller.storage.factory.s3.region=us-east-1
      pinot.controller.segment.fetcher.protocols=file,http,s3
      pinot.controller.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher

server:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      pinot.server.instance.realtime.alloc.offheap=true
      pinot.server.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
      pinot.server.storage.factory.s3.region=us-east-1
      pinot.server.segment.fetcher.protocols=file,http,s3
      pinot.server.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

{% hint style="info" %}
For AWS authentication, attach an IAM role to the Kubernetes service account via IRSA or use `serviceAccount.annotations` to bind the role.
{% endhint %}

### Google Cloud Storage (GCS)

```yaml
controller:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      controller.task.scheduler.enabled=true
      pinot.controller.storage.factory.class.gs=org.apache.pinot.plugin.filesystem.GcsPinotFS
      pinot.controller.storage.factory.gs.projectId=my-gcp-project
      pinot.controller.segment.fetcher.protocols=file,http,gs
      pinot.controller.segment.fetcher.gs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher

server:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      pinot.server.instance.realtime.alloc.offheap=true
      pinot.server.storage.factory.class.gs=org.apache.pinot.plugin.filesystem.GcsPinotFS
      pinot.server.storage.factory.gs.projectId=my-gcp-project
      pinot.server.segment.fetcher.protocols=file,http,gs
      pinot.server.segment.fetcher.gs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

### Azure Data Lake Storage (ADLS)

```yaml
controller:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      controller.task.scheduler.enabled=true
      pinot.controller.storage.factory.class.adl=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
      pinot.controller.storage.factory.adl.accountName=mystorageaccount
      pinot.controller.storage.factory.adl.accessKey=myaccesskey
      pinot.controller.storage.factory.adl.fileSystemName=pinot-deepstore
      pinot.controller.segment.fetcher.protocols=file,http,adl
      pinot.controller.segment.fetcher.adl.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher

server:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      pinot.server.instance.realtime.alloc.offheap=true
      pinot.server.storage.factory.class.adl=org.apache.pinot.plugin.filesystem.ADLSGen2PinotFS
      pinot.server.storage.factory.adl.accountName=mystorageaccount
      pinot.server.storage.factory.adl.accessKey=myaccesskey
      pinot.server.storage.factory.adl.fileSystemName=pinot-deepstore
      pinot.server.segment.fetcher.protocols=file,http,adl
      pinot.server.segment.fetcher.adl.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

### HDFS

```yaml
controller:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      controller.task.scheduler.enabled=true
      pinot.controller.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
      pinot.controller.storage.factory.hdfs.hadoop.conf.path=/opt/pinot/etc/hadoop/conf
      pinot.controller.segment.fetcher.protocols=file,http,hdfs
      pinot.controller.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher

server:
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      pinot.server.instance.realtime.alloc.offheap=true
      pinot.server.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
      pinot.server.storage.factory.hdfs.hadoop.conf.path=/opt/pinot/etc/hadoop/conf
      pinot.server.segment.fetcher.protocols=file,http,hdfs
      pinot.server.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

## Security Configuration

### TLS/SSL

To enable TLS on Pinot components, disable the default plaintext ports and configure HTTPS through extra configs. You will also need to mount TLS certificates using `extraVolumes` and `extraVolumeMounts`.

```yaml
controller:
  configureControllerPort: false
  persistence:
    extraVolumes:
      - name: tls-certs
        secret:
          secretName: pinot-tls
    extraVolumeMounts:
      - name: tls-certs
        mountPath: /opt/pinot/tls
        readOnly: true
  extra:
    configs: |-
      pinot.set.instance.id.to.hostname=true
      controller.access.protocols=https
      controller.access.protocols.https.port=9443
      pinot.controller.tls.keystore.path=/opt/pinot/tls/keystore.jks
      pinot.controller.tls.keystore.password=changeit
      pinot.controller.tls.truststore.path=/opt/pinot/tls/truststore.jks
      pinot.controller.tls.truststore.password=changeit
```

### Basic Auth

Enable built-in basic authentication using the `pinotAuth` section:

```yaml
pinotAuth:
  enabled: true
  configs:
    - access.control.principals=admin,user
    - access.control.principals.admin.password=verysecret
    - access.control.principals.user.password=secret
    - access.control.principals.user.tables=baseballStats
    - access.control.principals.user.permissions=READ
```

## Monitoring

### Prometheus Metrics Export

Pinot exposes JMX metrics that can be scraped by Prometheus. Use pod annotations to enable auto-discovery:

```yaml
controller:
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "9000"
    prometheus.io/path: "/metrics"

broker:
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8099"
    prometheus.io/path: "/metrics"

server:
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8097"
    prometheus.io/path: "/metrics"
```

For dedicated Prometheus monitoring setup with Grafana dashboards, see [Monitor Pinot using Prometheus and Grafana](../monitor-pinot-using-prometheus-and-grafana.md).

## Common Customization Examples

### Production-Ready Overrides

Below is a values override file suitable as a starting point for production deployments:

```yaml
image:
  tag: "1.0.0"        # Pin to a specific release
  pullPolicy: IfNotPresent

controller:
  replicaCount: 3
  resources:
    requests:
      cpu: 1
      memory: 2Gi
    limits:
      cpu: 2
      memory: 4Gi
  jvmOpts: "-XX:ActiveProcessorCount=2 -Xms1G -Xmx3G -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
  persistence:
    size: 10G
    storageClass: "gp2"   # Adjust for your cloud
  pdb:
    enabled: true
    maxUnavailable: 1

broker:
  replicaCount: 3
  resources:
    requests:
      cpu: 2
      memory: 4Gi
    limits:
      cpu: 4
      memory: 8Gi
  jvmOpts: "-XX:ActiveProcessorCount=4 -Xms2G -Xmx6G -XX:+UseG1GC -XX:MaxGCPauseMillis=200"
  probes:
    livenessEnabled: true
    readinessEnabled: true
  pdb:
    enabled: true
    maxUnavailable: 1

server:
  replicaCount: 4
  resources:
    requests:
      cpu: 4
      memory: 16Gi
    limits:
      cpu: 8
      memory: 32Gi
  jvmOpts: "-Xms8G -Xmx24G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:MaxDirectMemorySize=8G"
  persistence:
    size: 100G
    storageClass: "gp2"
  probes:
    livenessEnabled: true
    readinessEnabled: true
    startupEnabled: true
  pdb:
    enabled: true
    maxUnavailable: 1

zookeeper:
  replicaCount: 3
  persistence:
    size: 20Gi
    storageClass: "gp2"
```

{% hint style="info" %}
Set resource `requests` and `limits` to the same values to ensure pods get a Guaranteed QoS class. This prevents OOM kills during traffic spikes.
{% endhint %}

### Specifying Values with Helm

You can pass individual values on the command line:

```bash
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot-prod \
    --set server.replicaCount=4 \
    --set server.persistence.size=100G
```

Or use a custom values file:

```bash
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    -f production-values.yaml
```

## Upgrade Procedures

Follow these steps for a safe Helm-based upgrade of a running Pinot cluster.

### Pre-Upgrade Checklist

1. Review the [Pinot release notes](../../basics/releases) for breaking changes.
2. Back up your ZooKeeper data (table configs, schemas, segment metadata).
3. Ensure all tables are in a healthy state with no ongoing rebalances.
4. Test the upgrade in a staging environment first.

### Rolling Upgrade Steps

1. Update the image tag in your values file:

```yaml
image:
  tag: "1.1.0"   # Target version
```

2. Run a dry-run to review changes:

```bash
helm upgrade pinot pinot/pinot -n pinot-quickstart -f values.yaml --dry-run --debug
```

3. Apply the upgrade:

```bash
helm upgrade pinot pinot/pinot -n pinot-quickstart -f values.yaml
```

4. Monitor the rollout progress:

```bash
kubectl rollout status statefulset/pinot-controller -n pinot-quickstart
kubectl rollout status statefulset/pinot-broker -n pinot-quickstart
kubectl rollout status statefulset/pinot-server -n pinot-quickstart
```

### Recommended Upgrade Order

Upgrade components in this order to minimize disruption:

1. **Minion** -- has no live query traffic.
2. **Controller** -- manages metadata; upgrading first ensures the newest controller manages segment assignment.
3. **Broker** -- routes queries; rolling restart briefly shifts traffic to remaining brokers.
4. **Server** -- serves data; PDB ensures availability during rollout.

{% hint style="warning" %}
Avoid upgrading all components simultaneously. Use `updateStrategy.type: RollingUpdate` (the default) so pods restart one at a time.
{% endhint %}

### Rollback

If issues arise, roll back to the previous release:

```bash
helm rollback pinot -n pinot-quickstart
```

For additional guidance on production operations, see [Running Pinot in Production](../running-pinot-in-production.md) and [Kubernetes Deployment](deployment-pinot-on-kubernetes.md).
