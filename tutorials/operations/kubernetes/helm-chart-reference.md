# Helm Chart Values Reference

This page provides a comprehensive reference for the Apache Pinot Helm chart configuration values. Use this guide when deploying or customizing Pinot on Kubernetes.

## Chart Overview

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Chart Name</td>
      <td>`pinot`</td>
    </tr>
    <tr>
      <td>Chart Version</td>
      <td>`1.0.0`</td>
    </tr>
    <tr>
      <td>App Version</td>
      <td>`1.0.0`</td>
    </tr>
    <tr>
      <td>Source</td>
      <td>[github.com/apache/pinot/tree/master/helm](https://github.com/apache/pinot/tree/master/helm)</td>
    </tr>
    <tr>
      <td>Maintainer</td>
      <td>`dev@pinot.apache.org`</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`image.repository`</td>
      <td>Pinot container image repository</td>
      <td>`apachepinot/pinot`</td>
    </tr>
    <tr>
      <td>`image.tag`</td>
      <td>Pinot container image tag</td>
      <td>`latest`</td>
    </tr>
    <tr>
      <td>`image.pullPolicy`</td>
      <td>Image pull policy</td>
      <td>`Always`</td>
    </tr>
    <tr>
      <td>`cluster.name`</td>
      <td>Pinot cluster name</td>
      <td>`pinot-quickstart`</td>
    </tr>
    <tr>
      <td>`imagePullSecrets`</td>
      <td>Docker registry secret names</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`terminationGracePeriodSeconds`</td>
      <td>Grace period for pod termination</td>
      <td>`30`</td>
    </tr>
    <tr>
      <td>`securityContext`</td>
      <td>Pod-level security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`serviceAccount.create`</td>
      <td>Create a service account</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`serviceAccount.annotations`</td>
      <td>Service account annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`serviceAccount.name`</td>
      <td>Service account name (auto-generated if empty)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`additionalMatchLabels`</td>
      <td>Extra labels for pod selectors</td>
      <td>`{}`</td>
    </tr>
  </tbody>
</table>

### Default Probe Settings

These defaults apply to all components unless overridden at the component level.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`probes.initialDelaySeconds`</td>
      <td>Seconds before probes start</td>
      <td>`60`</td>
    </tr>
    <tr>
      <td>`probes.periodSeconds`</td>
      <td>Probe interval</td>
      <td>`10`</td>
    </tr>
    <tr>
      <td>`probes.failureThreshold`</td>
      <td>Failures before marking unhealthy</td>
      <td>`10`</td>
    </tr>
    <tr>
      <td>`probes.successThreshold`</td>
      <td>Successes before marking healthy</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`probes.timeoutSeconds`</td>
      <td>Probe timeout</td>
      <td>`10`</td>
    </tr>
  </tbody>
</table>

## Authentication

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`pinotAuth.enabled`</td>
      <td>Enable Pinot basic auth</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`pinotAuth.controllerFactoryClass`</td>
      <td>Controller access control factory</td>
      <td>`org.apache.pinot.controller.api.access.BasicAuthAccessControlFactory`</td>
    </tr>
    <tr>
      <td>`pinotAuth.brokerFactoryClass`</td>
      <td>Broker access control factory</td>
      <td>`org.apache.pinot.broker.broker.BasicAuthAccessControlFactory`</td>
    </tr>
    <tr>
      <td>`pinotAuth.configs`</td>
      <td>Auth config lines (principals, passwords, permissions)</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

## Controller

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.name`</td>
      <td>Controller component name</td>
      <td>`controller`</td>
    </tr>
    <tr>
      <td>`controller.replicaCount`</td>
      <td>Number of controller replicas</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`controller.configureControllerPort`</td>
      <td>Include `controller.port` in config</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`controller.podManagementPolicy`</td>
      <td>StatefulSet pod management policy</td>
      <td>`Parallel`</td>
    </tr>
    <tr>
      <td>`controller.startCommand`</td>
      <td>Start command for the container</td>
      <td>`StartController`</td>
    </tr>
  </tbody>
</table>

### Controller Resources and JVM

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.resources.requests.memory`</td>
      <td>Memory request</td>
      <td>`1.25Gi`</td>
    </tr>
    <tr>
      <td>`controller.jvmOpts`</td>
      <td>JVM options for the controller</td>
      <td>`-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...`</td>
    </tr>
    <tr>
      <td>`controller.log4j2ConfFile`</td>
      <td>Log4j2 configuration file path</td>
      <td>`/opt/pinot/etc/conf/pinot-controller-log4j2.xml`</td>
    </tr>
    <tr>
      <td>`controller.pluginsDir`</td>
      <td>Plugins directory</td>
      <td>`/opt/pinot/plugins`</td>
    </tr>
  </tbody>
</table>

### Controller Persistence

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.persistence.enabled`</td>
      <td>Enable PVC for controller data</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`controller.persistence.accessMode`</td>
      <td>PVC access mode</td>
      <td>`ReadWriteOnce`</td>
    </tr>
    <tr>
      <td>`controller.persistence.size`</td>
      <td>PVC size</td>
      <td>`1G`</td>
    </tr>
    <tr>
      <td>`controller.persistence.mountPath`</td>
      <td>Data mount path</td>
      <td>`/var/pinot/controller/data`</td>
    </tr>
    <tr>
      <td>`controller.persistence.storageClass`</td>
      <td>Storage class (empty for default)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`controller.persistence.extraVolumes`</td>
      <td>Additional volumes</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`controller.persistence.extraVolumeMounts`</td>
      <td>Additional volume mounts</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Controller Data Directory

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.data.dir`</td>
      <td>Controller data directory</td>
      <td>`/var/pinot/controller/data`</td>
    </tr>
  </tbody>
</table>

### Controller VIP

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.vip.enabled`</td>
      <td>Enable VIP host</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`controller.vip.host`</td>
      <td>VIP hostname</td>
      <td>`pinot-controller`</td>
    </tr>
    <tr>
      <td>`controller.vip.port`</td>
      <td>VIP port</td>
      <td>`9000`</td>
    </tr>
  </tbody>
</table>

### Controller Service

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.service.type`</td>
      <td>Headless service type</td>
      <td>`ClusterIP`</td>
    </tr>
    <tr>
      <td>`controller.service.clusterIP`</td>
      <td>Cluster IP (None for headless)</td>
      <td>`None`</td>
    </tr>
    <tr>
      <td>`controller.service.port`</td>
      <td>Service port</td>
      <td>`9000`</td>
    </tr>
    <tr>
      <td>`controller.service.protocol`</td>
      <td>Service protocol</td>
      <td>`TCP`</td>
    </tr>
    <tr>
      <td>`controller.service.name`</td>
      <td>Service port name</td>
      <td>`controller`</td>
    </tr>
    <tr>
      <td>`controller.service.nodePort`</td>
      <td>Node port (if type is NodePort)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`controller.service.annotations`</td>
      <td>Service annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.service.extraPorts`</td>
      <td>Additional ports to expose</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Controller External Service

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.external.enabled`</td>
      <td>Expose controller externally</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`controller.external.type`</td>
      <td>External service type</td>
      <td>`LoadBalancer`</td>
    </tr>
    <tr>
      <td>`controller.external.port`</td>
      <td>External service port</td>
      <td>`9000`</td>
    </tr>
    <tr>
      <td>`controller.external.annotations`</td>
      <td>External service annotations</td>
      <td>`{}`</td>
    </tr>
  </tbody>
</table>

### Controller Ingress

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.ingress.v1.enabled`</td>
      <td>Enable v1 Ingress</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`controller.ingress.v1.ingressClassName`</td>
      <td>Ingress class name</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`controller.ingress.v1.annotations`</td>
      <td>Ingress annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.ingress.v1.tls`</td>
      <td>TLS configuration</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`controller.ingress.v1.path`</td>
      <td>Ingress path</td>
      <td>`/`</td>
    </tr>
    <tr>
      <td>`controller.ingress.v1.hosts`</td>
      <td>Ingress hostnames</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Controller Probes

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.probes.endpoint`</td>
      <td>Health check endpoint</td>
      <td>`/health`</td>
    </tr>
    <tr>
      <td>`controller.probes.livenessEnabled`</td>
      <td>Enable liveness probe</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`controller.probes.readinessEnabled`</td>
      <td>Enable readiness probe</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`controller.probes.startupEnabled`</td>
      <td>Enable startup probe</td>
      <td>`false`</td>
    </tr>
  </tbody>
</table>

### Controller Scheduling and Miscellaneous

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.nodeSelector`</td>
      <td>Node selector labels</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.tolerations`</td>
      <td>Pod tolerations</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`controller.affinity`</td>
      <td>Pod affinity rules</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.podAnnotations`</td>
      <td>Pod annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.initContainers`</td>
      <td>Init containers</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`controller.podSecurityContext`</td>
      <td>Pod security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.securityContext`</td>
      <td>Container security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`controller.updateStrategy.type`</td>
      <td>StatefulSet update strategy</td>
      <td>`RollingUpdate`</td>
    </tr>
    <tr>
      <td>`controller.automaticReload.enabled`</td>
      <td>Auto-roll on ConfigMap change</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`controller.envFrom`</td>
      <td>ConfigMap/Secret references for env vars</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`controller.extraEnv`</td>
      <td>Extra environment variables</td>
      <td>`[{name: LOG4J_CONSOLE_LEVEL, value: info}]`</td>
    </tr>
    <tr>
      <td>`controller.extra.configs`</td>
      <td>Extra lines appended to pinot-controller.conf</td>
      <td>`pinot.set.instance.id.to.hostname=true`</td>
    </tr>
  </tbody>
</table>

### Controller PodDisruptionBudget

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`controller.pdb.enabled`</td>
      <td>Enable PDB</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`controller.pdb.minAvailable`</td>
      <td>Minimum available pods</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`controller.pdb.maxUnavailable`</td>
      <td>Maximum unavailable pods</td>
      <td>`50%`</td>
    </tr>
  </tbody>
</table>

## Broker

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.name`</td>
      <td>Broker component name</td>
      <td>`broker`</td>
    </tr>
    <tr>
      <td>`broker.replicaCount`</td>
      <td>Number of broker replicas</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`broker.configureBrokerPort`</td>
      <td>Include `pinot.broker.client.queryPort` in config</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`broker.podManagementPolicy`</td>
      <td>StatefulSet pod management policy</td>
      <td>`Parallel`</td>
    </tr>
    <tr>
      <td>`broker.startCommand`</td>
      <td>Start command for the container</td>
      <td>`StartBroker`</td>
    </tr>
  </tbody>
</table>

### Broker Resources and JVM

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.resources.requests.memory`</td>
      <td>Memory request</td>
      <td>`1.25Gi`</td>
    </tr>
    <tr>
      <td>`broker.jvmOpts`</td>
      <td>JVM options for the broker</td>
      <td>`-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...`</td>
    </tr>
    <tr>
      <td>`broker.log4j2ConfFile`</td>
      <td>Log4j2 configuration file path</td>
      <td>`/opt/pinot/etc/conf/pinot-broker-log4j2.xml`</td>
    </tr>
    <tr>
      <td>`broker.pluginsDir`</td>
      <td>Plugins directory</td>
      <td>`/opt/pinot/plugins`</td>
    </tr>
    <tr>
      <td>`broker.routingTable.builderClass`</td>
      <td>Routing table builder class</td>
      <td>`random`</td>
    </tr>
  </tbody>
</table>

### Broker Service

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.service.type`</td>
      <td>Headless service type</td>
      <td>`ClusterIP`</td>
    </tr>
    <tr>
      <td>`broker.service.clusterIP`</td>
      <td>Cluster IP (None for headless)</td>
      <td>`None`</td>
    </tr>
    <tr>
      <td>`broker.service.port`</td>
      <td>Service port</td>
      <td>`8099`</td>
    </tr>
    <tr>
      <td>`broker.service.protocol`</td>
      <td>Service protocol</td>
      <td>`TCP`</td>
    </tr>
    <tr>
      <td>`broker.service.name`</td>
      <td>Service port name</td>
      <td>`broker`</td>
    </tr>
    <tr>
      <td>`broker.service.nodePort`</td>
      <td>Node port (if type is NodePort)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`broker.service.annotations`</td>
      <td>Service annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.service.extraPorts`</td>
      <td>Additional ports to expose</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Broker External Service

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.external.enabled`</td>
      <td>Expose broker externally</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`broker.external.type`</td>
      <td>External service type</td>
      <td>`LoadBalancer`</td>
    </tr>
    <tr>
      <td>`broker.external.port`</td>
      <td>External service port</td>
      <td>`8099`</td>
    </tr>
    <tr>
      <td>`broker.external.annotations`</td>
      <td>External service annotations</td>
      <td>`{}`</td>
    </tr>
  </tbody>
</table>

### Broker Ingress

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.ingress.v1.enabled`</td>
      <td>Enable v1 Ingress</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`broker.ingress.v1.ingressClassName`</td>
      <td>Ingress class name</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`broker.ingress.v1.annotations`</td>
      <td>Ingress annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.ingress.v1.tls`</td>
      <td>TLS configuration</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`broker.ingress.v1.path`</td>
      <td>Ingress path</td>
      <td>`/`</td>
    </tr>
    <tr>
      <td>`broker.ingress.v1.hosts`</td>
      <td>Ingress hostnames</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Broker Probes

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.probes.endpoint`</td>
      <td>Health check endpoint</td>
      <td>`/health`</td>
    </tr>
    <tr>
      <td>`broker.probes.livenessEnabled`</td>
      <td>Enable liveness probe</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`broker.probes.readinessEnabled`</td>
      <td>Enable readiness probe</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`broker.probes.startupEnabled`</td>
      <td>Enable startup probe</td>
      <td>`false`</td>
    </tr>
  </tbody>
</table>

### Broker Scheduling and Miscellaneous

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`broker.nodeSelector`</td>
      <td>Node selector labels</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.tolerations`</td>
      <td>Pod tolerations</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`broker.affinity`</td>
      <td>Pod affinity rules</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.podAnnotations`</td>
      <td>Pod annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.initContainers`</td>
      <td>Init containers</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`broker.podSecurityContext`</td>
      <td>Pod security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.securityContext`</td>
      <td>Container security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`broker.updateStrategy.type`</td>
      <td>StatefulSet update strategy</td>
      <td>`RollingUpdate`</td>
    </tr>
    <tr>
      <td>`broker.automaticReload.enabled`</td>
      <td>Auto-roll on ConfigMap change</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`broker.envFrom`</td>
      <td>ConfigMap/Secret references for env vars</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`broker.extraEnv`</td>
      <td>Extra environment variables</td>
      <td>`[{name: LOG4J_CONSOLE_LEVEL, value: info}]`</td>
    </tr>
    <tr>
      <td>`broker.extra.configs`</td>
      <td>Extra lines appended to pinot-broker.conf</td>
      <td>`pinot.set.instance.id.to.hostname=true`</td>
    </tr>
    <tr>
      <td>`broker.pdb.enabled`</td>
      <td>Enable PDB</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`broker.pdb.maxUnavailable`</td>
      <td>Maximum unavailable pods</td>
      <td>`50%`</td>
    </tr>
  </tbody>
</table>

## Server

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.name`</td>
      <td>Server component name</td>
      <td>`server`</td>
    </tr>
    <tr>
      <td>`server.replicaCount`</td>
      <td>Number of server replicas</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`server.configureServerPort`</td>
      <td>Include `pinot.server.netty.port` in config</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`server.podManagementPolicy`</td>
      <td>StatefulSet pod management policy</td>
      <td>`Parallel`</td>
    </tr>
    <tr>
      <td>`server.startCommand`</td>
      <td>Start command for the container</td>
      <td>`StartServer`</td>
    </tr>
  </tbody>
</table>

### Server Resources and JVM

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.resources.requests.memory`</td>
      <td>Memory request</td>
      <td>`1.25Gi`</td>
    </tr>
    <tr>
      <td>`server.jvmOpts`</td>
      <td>JVM options for the server</td>
      <td>`-Xms512M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...`</td>
    </tr>
    <tr>
      <td>`server.log4j2ConfFile`</td>
      <td>Log4j2 configuration file path</td>
      <td>`/opt/pinot/etc/conf/pinot-server-log4j2.xml`</td>
    </tr>
    <tr>
      <td>`server.pluginsDir`</td>
      <td>Plugins directory</td>
      <td>`/opt/pinot/plugins`</td>
    </tr>
  </tbody>
</table>

### Server Data Directories

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.dataDir`</td>
      <td>Index data directory</td>
      <td>`/var/pinot/server/data/index`</td>
    </tr>
    <tr>
      <td>`server.segmentTarDir`</td>
      <td>Segment tar directory</td>
      <td>`/var/pinot/server/data/segment`</td>
    </tr>
  </tbody>
</table>

### Server Persistence

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.persistence.enabled`</td>
      <td>Enable PVC for server data</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`server.persistence.accessMode`</td>
      <td>PVC access mode</td>
      <td>`ReadWriteOnce`</td>
    </tr>
    <tr>
      <td>`server.persistence.size`</td>
      <td>PVC size</td>
      <td>`4G`</td>
    </tr>
    <tr>
      <td>`server.persistence.mountPath`</td>
      <td>Data mount path</td>
      <td>`/var/pinot/server/data`</td>
    </tr>
    <tr>
      <td>`server.persistence.storageClass`</td>
      <td>Storage class (empty for default)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`server.persistence.extraVolumes`</td>
      <td>Additional volumes</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`server.persistence.extraVolumeMounts`</td>
      <td>Additional volume mounts</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Server Service

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.service.type`</td>
      <td>Service type</td>
      <td>`ClusterIP`</td>
    </tr>
    <tr>
      <td>`server.service.nettyPort`</td>
      <td>Netty data port</td>
      <td>`8098`</td>
    </tr>
    <tr>
      <td>`server.service.nettyPortName`</td>
      <td>Netty port name</td>
      <td>`netty`</td>
    </tr>
    <tr>
      <td>`server.service.adminPort`</td>
      <td>Admin HTTP port</td>
      <td>`8097`</td>
    </tr>
    <tr>
      <td>`server.service.adminExposePort`</td>
      <td>Admin exposed port</td>
      <td>`80`</td>
    </tr>
    <tr>
      <td>`server.service.adminPortName`</td>
      <td>Admin port name</td>
      <td>`admin`</td>
    </tr>
    <tr>
      <td>`server.service.nodePort`</td>
      <td>Node port (if type is NodePort)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`server.service.protocol`</td>
      <td>Service protocol</td>
      <td>`TCP`</td>
    </tr>
    <tr>
      <td>`server.service.annotations`</td>
      <td>Service annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`server.service.extraPorts`</td>
      <td>Additional ports to expose</td>
      <td>`[]`</td>
    </tr>
  </tbody>
</table>

### Server Probes

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.probes.endpoint`</td>
      <td>Health check endpoint</td>
      <td>`/health`</td>
    </tr>
    <tr>
      <td>`server.probes.livenessEnabled`</td>
      <td>Enable liveness probe</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`server.probes.readinessEnabled`</td>
      <td>Enable readiness probe</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`server.probes.startupEnabled`</td>
      <td>Enable startup probe</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`server.probes.liveness.endpoint`</td>
      <td>Liveness-specific endpoint</td>
      <td>`/health/liveness`</td>
    </tr>
    <tr>
      <td>`server.probes.readiness.endpoint`</td>
      <td>Readiness-specific endpoint</td>
      <td>`/health/readiness`</td>
    </tr>
  </tbody>
</table>

### Server Scheduling and Miscellaneous

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`server.nodeSelector`</td>
      <td>Node selector labels</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`server.tolerations`</td>
      <td>Pod tolerations</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`server.affinity`</td>
      <td>Pod affinity rules</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`server.podAnnotations`</td>
      <td>Pod annotations</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`server.initContainers`</td>
      <td>Init containers</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`server.podSecurityContext`</td>
      <td>Pod security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`server.securityContext`</td>
      <td>Container security context</td>
      <td>`{}`</td>
    </tr>
    <tr>
      <td>`server.updateStrategy.type`</td>
      <td>StatefulSet update strategy</td>
      <td>`RollingUpdate`</td>
    </tr>
    <tr>
      <td>`server.automaticReload.enabled`</td>
      <td>Auto-roll on ConfigMap change</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`server.envFrom`</td>
      <td>ConfigMap/Secret references for env vars</td>
      <td>`[]`</td>
    </tr>
    <tr>
      <td>`server.extraEnv`</td>
      <td>Extra environment variables</td>
      <td>`[{name: LOG4J_CONSOLE_LEVEL, value: info}]`</td>
    </tr>
    <tr>
      <td>`server.extra.configs`</td>
      <td>Extra lines appended to pinot-server.conf</td>
      <td>See values.yaml</td>
    </tr>
    <tr>
      <td>`server.pdb.enabled`</td>
      <td>Enable PDB</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`server.pdb.maxUnavailable`</td>
      <td>Maximum unavailable pods</td>
      <td>`1`</td>
    </tr>
  </tbody>
</table>

## Minion (StatefulSet)

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`minion.enabled`</td>
      <td>Deploy Minion StatefulSet</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`minion.name`</td>
      <td>Minion component name</td>
      <td>`minion`</td>
    </tr>
    <tr>
      <td>`minion.replicaCount`</td>
      <td>Number of minion replicas</td>
      <td>`0`</td>
    </tr>
    <tr>
      <td>`minion.configureMinionPort`</td>
      <td>Include `pinot.minion.port` in config</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`minion.podManagementPolicy`</td>
      <td>StatefulSet pod management policy</td>
      <td>`Parallel`</td>
    </tr>
    <tr>
      <td>`minion.startCommand`</td>
      <td>Start command for the container</td>
      <td>`StartMinion`</td>
    </tr>
    <tr>
      <td>`minion.resources.requests.memory`</td>
      <td>Memory request</td>
      <td>`1.25Gi`</td>
    </tr>
    <tr>
      <td>`minion.jvmOpts`</td>
      <td>JVM options for minion</td>
      <td>`-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 ...`</td>
    </tr>
    <tr>
      <td>`minion.dataDir`</td>
      <td>Minion data directory</td>
      <td>`/var/pinot/minion/data`</td>
    </tr>
    <tr>
      <td>`minion.persistence.enabled`</td>
      <td>Enable PVC for minion data</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`minion.persistence.size`</td>
      <td>PVC size</td>
      <td>`4G`</td>
    </tr>
    <tr>
      <td>`minion.persistence.storageClass`</td>
      <td>Storage class (empty for default)</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`minion.service.port`</td>
      <td>Service port</td>
      <td>`9514`</td>
    </tr>
    <tr>
      <td>`minion.extra.configs`</td>
      <td>Extra lines appended to pinot-minion.conf</td>
      <td>`pinot.set.instance.id.to.hostname=true`</td>
    </tr>
    <tr>
      <td>`minion.pdb.enabled`</td>
      <td>Enable PDB</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`minion.pdb.maxUnavailable`</td>
      <td>Maximum unavailable pods</td>
      <td>`1`</td>
    </tr>
  </tbody>
</table>

## Minion Stateless (Deployment)

The stateless minion runs as a Kubernetes Deployment instead of a StatefulSet, making it suitable for ephemeral task execution.

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`minionStateless.enabled`</td>
      <td>Deploy Minion Stateless Deployment</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`minionStateless.name`</td>
      <td>Component name</td>
      <td>`minion-stateless`</td>
    </tr>
    <tr>
      <td>`minionStateless.replicaCount`</td>
      <td>Number of replicas</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`minionStateless.configureMinionStatelessPort`</td>
      <td>Include `pinot.minion.port` in config</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`minionStateless.startCommand`</td>
      <td>Start command</td>
      <td>`StartMinion`</td>
    </tr>
    <tr>
      <td>`minionStateless.resources.requests.memory`</td>
      <td>Memory request</td>
      <td>`1.25Gi`</td>
    </tr>
    <tr>
      <td>`minionStateless.jvmOpts`</td>
      <td>JVM options</td>
      <td>`-XX:ActiveProcessorCount=2 -Xms256M -Xmx1G ...`</td>
    </tr>
    <tr>
      <td>`minionStateless.persistence.enabled`</td>
      <td>Enable PVC</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`minionStateless.persistence.size`</td>
      <td>PVC size (when enabled)</td>
      <td>`4G`</td>
    </tr>
    <tr>
      <td>`minionStateless.service.port`</td>
      <td>Service port</td>
      <td>`9514`</td>
    </tr>
    <tr>
      <td>`minionStateless.extra.configs`</td>
      <td>Extra config lines</td>
      <td>`pinot.set.instance.id.to.hostname=true`</td>
    </tr>
    <tr>
      <td>`minionStateless.pdb.enabled`</td>
      <td>Enable PDB</td>
      <td>`false`</td>
    </tr>
    <tr>
      <td>`minionStateless.pdb.maxUnavailable`</td>
      <td>Maximum unavailable pods</td>
      <td>`1`</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Parameter</th>
      <th>Description</th>
      <th>Default</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`zookeeper.enabled`</td>
      <td>Install bundled ZooKeeper</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`zookeeper.urlOverride`</td>
      <td>External ZooKeeper connection string (used when `enabled: false`)</td>
      <td>`my-zookeeper:2181/my-pinot`</td>
    </tr>
    <tr>
      <td>`zookeeper.port`</td>
      <td>ZooKeeper client port</td>
      <td>`2181`</td>
    </tr>
    <tr>
      <td>`zookeeper.replicaCount`</td>
      <td>Number of ZooKeeper replicas</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`zookeeper.resources.requests.memory`</td>
      <td>Memory request</td>
      <td>`1.25Gi`</td>
    </tr>
    <tr>
      <td>`zookeeper.heapSize`</td>
      <td>Java heap size in MB</td>
      <td>`1024`</td>
    </tr>
    <tr>
      <td>`zookeeper.jvmFlags`</td>
      <td>Extra JVM flags</td>
      <td>`-Djute.maxbuffer=4000000`</td>
    </tr>
    <tr>
      <td>`zookeeper.persistence.enabled`</td>
      <td>Enable persistent storage</td>
      <td>`true`</td>
    </tr>
    <tr>
      <td>`zookeeper.persistence.storageClass`</td>
      <td>Storage class</td>
      <td>`""`</td>
    </tr>
    <tr>
      <td>`zookeeper.persistence.size`</td>
      <td>PVC size</td>
      <td>`8Gi`</td>
    </tr>
    <tr>
      <td>`zookeeper.autopurge.purgeInterval`</td>
      <td>Purge interval in hours</td>
      <td>`1`</td>
    </tr>
    <tr>
      <td>`zookeeper.autopurge.snapRetainCount`</td>
      <td>Snapshots to retain</td>
      <td>`5`</td>
    </tr>
    <tr>
      <td>`zookeeper.image.repository`</td>
      <td>ZooKeeper image (Apache official)</td>
      <td>`zookeeper`</td>
    </tr>
    <tr>
      <td>`zookeeper.image.tag`</td>
      <td>ZooKeeper image tag</td>
      <td>`3.9.3`</td>
    </tr>
    <tr>
      <td>`zookeeper.image.pullPolicy`</td>
      <td>Image pull policy</td>
      <td>`IfNotPresent`</td>
    </tr>
    <tr>
      <td>`zookeeper.affinity`</td>
      <td>Pod affinity rules</td>
      <td>`{}`</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>Aspect</th>
      <th>Bitnami (v0.3.6)</th>
      <th>Native (v1.0.0)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Image</td>
      <td>`bitnamilegacy/zookeeper:3.9.3-debian-12-r22`</td>
      <td>`zookeeper:3.9.3`</td>
    </tr>
    <tr>
      <td>StatefulSet Selectors</td>
      <td>`app.kubernetes.io/name: zookeeper`</td>
      <td>`app: pinot, component: zookeeper`</td>
    </tr>
    <tr>
      <td>Data Mount Path</td>
      <td>`/bitnami/zookeeper`</td>
      <td>`/data`</td>
    </tr>
    <tr>
      <td>Datalog VCT</td>
      <td>`data-log`</td>
      <td>`datalog`</td>
    </tr>
    <tr>
      <td>Removed Parameters</td>
      <td>`image.registry`, `global.security.*`, `tls.*`, `auth.*`</td>
      <td>N/A</td>
    </tr>
  </tbody>
</table>

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

1. Review the [Pinot release notes](../../../basics/releases/) for breaking changes.
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
