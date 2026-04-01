---
description: >-
  This guide shows you how to configure HDFS for use with Pinot, including data
  import and deep storage.
---

# Hadoop DFS

Enable the [Hadoop distributed file system (HDFS)](https://hadoop.apache.org/) using the `pinot-hdfs` plugin. In the controller or server, add the config:

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-hdfs
```

{% hint style="info" %}
By default Pinot loads all the plugins, so you can just drop this plugin there. Also, if you specify `-Dplugins.include`, you need to put all the plugins you want to use, e.g. `pinot-json`, `pinot-avro` , `pinot-kafka-3.0...`
{% endhint %}

HDFS implementation provides the following options:

* `hadoop.conf.path`: Absolute path of the directory containing Hadoop XML configuration files, such as **hdfs-site.xml, core-site.xml** .
* `hadoop.write.checksum`: Create checksum while pushing an object. Default is `false`
* `hadoop.kerberos.principle`
* `hadoop.kerberos.keytab`

Each of these properties should be prefixed by `pinot.[node].storage.factory.class.hdfs.` where `node` is either `controller` or `server` depending on the config

The `kerberos` configs should be used only if your Hadoop installation is secured with Kerberos. Refer to the [Hadoop in secure mode documentation](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SecureMode.html) for information on how to secure Hadoop using Kerberos.

You must provide proper Hadoop dependencies jars from your Hadoop installation to your Pinot startup scripts.

```
export HADOOP_HOME=/local/hadoop/
export HADOOP_VERSION=2.7.1
export HADOOP_GUAVA_VERSION=11.0.2
export HADOOP_GSON_VERSION=2.2.4
export CLASSPATH_PREFIX="${HADOOP_HOME}/share/hadoop/hdfs/hadoop-hdfs-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-annotations-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-auth-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/hadoop-common-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/guava-${HADOOP_GUAVA_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/gson-${HADOOP_GSON_VERSION}.jar"
```

## Push HDFS segment to Pinot Controller

To push HDFS segment files to Pinot controller, send the HDFS path of your newly created segment files to the Pinot Controller. The controller will download the files.

This curl example requests tells the controller to download segment files to the proper table:

```
curl -X POST -H "UPLOAD_TYPE:URI" -H "DOWNLOAD_URI:hdfs://nameservice1/hadoop/path/to/segment/file.
```

## Examples

### Job spec

Standalone Job:

```yaml
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: 'hdfs:///path/to/input/directory/'
outputDirURI: 'hdfs:///path/to/output/directory/'
includeFileNamePath: 'glob:**/*.csv'
overwriteOutput: true
pinotFSSpecs:
    - scheme: hdfs
      className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
      configs:
        hadoop.conf.path: 'path/to/conf/directory/'
recordReaderSpec:
    dataFormat: 'csv'
    className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
    configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
    tableName: 'students'
pinotClusterSpecs:
    - controllerURI: 'http://localhost:9000'
```

Hadoop Job:

```yaml
executionFrameworkSpec:
    name: 'hadoop'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentUriPushJobRunner'
    extraConfigs:
      stagingDir: 'hdfs:///path/to/staging/directory/'
jobType: SegmentCreationAndTarPush
inputDirURI: 'hdfs:///path/to/input/directory/'
outputDirURI: 'hdfs:///path/to/output/directory/'
includeFileNamePath: 'glob:**/*.csv'
overwriteOutput: true
pinotFSSpecs:
    - scheme: hdfs
      className: org.apache.pinot.plugin.filesystem.HadoopPinotFS
      configs:
        hadoop.conf.path: '/etc/hadoop/conf/'
recordReaderSpec:
    dataFormat: 'csv'
    className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
    configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
    tableName: 'students'
pinotClusterSpecs:
    - controllerURI: 'http://localhost:9000'
```

### Controller config

```
controller.data.dir=hdfs://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.controller.storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory/
pinot.controller.segment.fetcher.protocols=file,http,hdfs
pinot.controller.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
```

### Server config

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.server.storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory/
pinot.server.segment.fetcher.protocols=file,http,hdfs
pinot.server.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
pinot.server.segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
pinot.server.segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
```

### Minion config

```
storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
storage.factory.hdfs.hadoop.conf.path=path/to/conf/directory
segment.fetcher.protocols=file,http,hdfs
segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
```

## HDFS as deep storage

To use HDFS as deep storage, configure each Pinot component with the HDFS plugin and the appropriate storage factory and segment fetcher properties. The sections below provide complete configuration and startup examples for each component.

### Server setup

#### Configuration

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.server.storage.factory.hdfs.hadoop.conf.path=/path/to/hadoop/conf/directory/
# For server, instructing the HadoopPinotFS plugin to use the specified keytab and principal when accessing HDFS paths
pinot.server.storage.factory.hdfs.hadoop.kerberos.principle=<hdfs-principle>
pinot.server.storage.factory.hdfs.hadoop.kerberos.keytab=<hdfs-keytab>
pinot.server.segment.fetcher.protocols=file,http,hdfs
pinot.server.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
pinot.server.segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
pinot.server.segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
pinot.set.instance.id.to.hostname=true
pinot.server.instance.dataDir=/path/in/local/filesystem/for/pinot/data/server/index
pinot.server.instance.segmentTarDir=/path/in/local/filesystem/for/pinot/data/server/segment
pinot.server.grpc.enable=true
pinot.server.grpc.port=8090
```

#### Executable

```
export HADOOP_HOME=/path/to/hadoop/home
export HADOOP_VERSION=2.7.1
export HADOOP_GUAVA_VERSION=11.0.2
export HADOOP_GSON_VERSION=2.2.4
export GC_LOG_LOCATION=/path/to/gc/log/file
export PINOT_VERSION=0.10.0
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin/
export SERVER_CONF_DIR=/path/to/pinot/conf/dir/
export ZOOKEEPER_ADDRESS=localhost:2181


export CLASSPATH_PREFIX="${HADOOP_HOME}/share/hadoop/hdfs/hadoop-hdfs-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-annotations-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-auth-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/hadoop-common-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/guava-${HADOOP_GUAVA_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/gson-${HADOOP_GSON_VERSION}.jar"
export JAVA_OPTS="-Xms4G -Xmx16G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:${GC_LOG_LOCATION}/gc-pinot-server.log"
${PINOT_DISTRIBUTION_DIR}/bin/start-server.sh  -zkAddress ${ZOOKEEPER_ADDRESS} -configFileName ${SERVER_CONF_DIR}/server.conf
```

### Controller setup

#### Configuration

```
controller.data.dir=hdfs://path/in/hdfs/for/controller/segment
controller.local.temp.dir=/tmp/pinot/
controller.zk.str=<ZOOKEEPER_HOST:ZOOKEEPER_PORT>
controller.enable.split.commit=true
controller.access.protocols.http.port=9000
controller.helix.cluster.name=PinotCluster
pinot.controller.storage.factory.class.hdfs=org.apache.pinot.plugin.filesystem.HadoopPinotFS
pinot.controller.storage.factory.hdfs.hadoop.conf.path=/path/to/hadoop/conf/directory/
# For controller, instructing the HadoopPinotFS plugin to use the specified keytab and principal when accessing the HDFS path defined in controller.data.dir
pinot.controller.storage.factory.hdfs.hadoop.kerberos.principle=<hdfs-principle>
pinot.controller.storage.factory.hdfs.hadoop.kerberos.keytab=<hdfs-keytab>
pinot.controller.segment.fetcher.protocols=file,http,hdfs
pinot.controller.segment.fetcher.hdfs.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.principle=<your kerberos principal>
pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.keytab=<your kerberos keytab>
controller.vip.port=9000
controller.port=9000
pinot.set.instance.id.to.hostname=true
pinot.server.grpc.enable=true
```

#### Executable

```
export HADOOP_HOME=/path/to/hadoop/home
export HADOOP_VERSION=2.7.1
export HADOOP_GUAVA_VERSION=11.0.2
export HADOOP_GSON_VERSION=2.2.4
export GC_LOG_LOCATION=/path/to/gc/log/file
export PINOT_VERSION=0.10.0
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin/
export SERVER_CONF_DIR=/path/to/pinot/conf/dir/
export ZOOKEEPER_ADDRESS=localhost:2181


export CLASSPATH_PREFIX="${HADOOP_HOME}/share/hadoop/hdfs/hadoop-hdfs-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-annotations-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-auth-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/hadoop-common-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/guava-${HADOOP_GUAVA_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/gson-${HADOOP_GSON_VERSION}.jar"
export JAVA_OPTS="-Xms8G -Xmx12G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:${GC_LOG_LOCATION}/gc-pinot-controller.log"
${PINOT_DISTRIBUTION_DIR}/bin/start-controller.sh -configFileName ${SERVER_CONF_DIR}/controller.conf
```

### Broker setup

#### Configuration

```
pinot.set.instance.id.to.hostname=true
pinot.server.grpc.enable=true
```

#### Executable

```
export HADOOP_HOME=/path/to/hadoop/home
export HADOOP_VERSION=2.7.1
export HADOOP_GUAVA_VERSION=11.0.2
export HADOOP_GSON_VERSION=2.2.4
export GC_LOG_LOCATION=/path/to/gc/log/file
export PINOT_VERSION=0.10.0
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin/
export SERVER_CONF_DIR=/path/to/pinot/conf/dir/
export ZOOKEEPER_ADDRESS=localhost:2181


export CLASSPATH_PREFIX="${HADOOP_HOME}/share/hadoop/hdfs/hadoop-hdfs-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-annotations-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/hadoop-auth-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/hadoop-common-${HADOOP_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/guava-${HADOOP_GUAVA_VERSION}.jar:${HADOOP_HOME}/share/hadoop/common/lib/gson-${HADOOP_GSON_VERSION}.jar"
export JAVA_OPTS="-Xms4G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:${GC_LOG_LOCATION}/gc-pinot-broker.log"
${PINOT_DISTRIBUTION_DIR}/bin/start-broker.sh -zkAddress ${ZOOKEEPER_ADDRESS} -configFileName  ${SERVER_CONF_DIR}/broker.conf
```

## Kerberos authentication

When using HDFS with Kerberos security enabled, Pinot provides two ways to authenticate:

### 1. Automatic authentication (recommended)

By configuring the `storage.factory` Kerberos properties shown above, Pinot will automatically handle Kerberos authentication using the specified keytab and principal. This eliminates the need for manual `kinit` commands and ensures continuous authentication even after ticket expiration.

#### Why these properties are required

The `storage.factory` Kerberos properties serve a critical purpose in Pinot's HDFS integration:

**For Controller:**
- The controller uses `controller.data.dir` to store segment metadata and other data in HDFS
- When `controller.data.dir` points to an HDFS path (e.g., `hdfs://namenode:8020/pinot/data`), the HadoopPinotFS plugin needs Kerberos credentials to access it
- Without `storage.factory` Kerberos properties, the controller would fail to read/write to HDFS, causing segment upload and metadata operations to fail
- These properties enable the HadoopPinotFS plugin to programmatically authenticate using the keytab file

**For Server:**
- The server uses HadoopPinotFS for various HDFS operations including segment downloads and deep storage access
- When servers need to access segments stored in HDFS deep storage, they require valid Kerberos credentials
- The `storage.factory` properties provide persistent authentication that survives across server restarts and ticket expirations

#### Understanding the two sets of Kerberos properties

You may notice two sets of Kerberos properties in the configuration:

1. **`storage.factory` properties (recommended):**
   - `pinot.controller.storage.factory.hdfs.hadoop.kerberos.principal`
   - `pinot.controller.storage.factory.hdfs.hadoop.kerberos.keytab`
   - `pinot.server.storage.factory.hdfs.hadoop.kerberos.principal`
   - `pinot.server.storage.factory.hdfs.hadoop.kerberos.keytab`

   **Purpose:** These properties configure Kerberos authentication for the HadoopPinotFS storage factory, which handles controller and server deep storage operations and general HDFS filesystem operations through the storage factory.

   **Why needed:** The storage factory is initialized at startup and used throughout the component's lifecycle for HDFS access. Without these properties, any HDFS operation through the storage factory would fail with authentication errors.

2. **`segment.fetcher` properties (legacy, for backward compatibility):**
   - `pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.principle` (note: typo "principle" instead of "principal" maintained for compatibility)
   - `pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.keytab`
   - `pinot.server.segment.fetcher.hdfs.hadoop.kerberos.principle`
   - `pinot.server.segment.fetcher.hdfs.hadoop.kerberos.keytab`

   **Purpose:** These configure Kerberos for the segment fetcher component specifically.

   **Why both are needed:** While there is some functional overlap, having both ensures complete coverage of all HDFS access patterns, backward compatibility with existing deployments, and independent operation of the segment fetcher.

#### Benefits of automatic authentication

- Eliminates the need to run `kinit` commands manually, reducing operational overhead and human error
- Kerberos tickets typically expire after 24 hours (configurable); with keytab-based authentication, Pinot automatically renews tickets internally, preventing service disruptions
- Keytab files provide secure, long-term credentials without storing passwords in scripts or configuration

### 2. Manual authentication (legacy)

Alternatively, you can manually authenticate using `kinit` before starting Pinot components:

```bash
kinit -kt <your kerberos keytab> <your kerberos principal>
```

**Limitations of manual authentication:**

- **Ticket expiration:** Kerberos tickets typically expire after 24 hours, requiring re-authentication
- **Service interruption:** If tickets expire while Pinot is running, HDFS operations will fail until re-authentication
- **Operational burden:** Requires monitoring and manual intervention, especially problematic for 24/7 production systems
- **Automation challenges:** Difficult to integrate into automated deployment pipelines

{% hint style="warning" %}
Manual authentication is not recommended for production environments. Always use the `storage.factory` Kerberos properties for production deployments.
{% endhint %}

## Troubleshooting

### HDFS FileSystem issues

If you receive an error that says `No FileSystem for scheme"hdfs"`, the problem is likely to be a class loading issue.

To fix, try adding the following property to `core-site.xml`:

```fs.hdfs.impl org.apache.hadoop.hdfs.DistributedFileSystem```

And then export `/opt/pinot/lib/hadoop-common-<release-version>.jar` in the classpath.

### Kerberos authentication issues

#### Error: "Failed to authenticate with Kerberos"

**Possible causes:**
1. **Incorrect keytab path:** Ensure the keytab file path is absolute and accessible by the Pinot process
2. **Wrong principal name:** Verify the principal name matches the one in the keytab file
3. **Keytab file permissions:** The keytab file must be readable by the user running Pinot (typically `chmod 400` or `chmod 600`)

**Solution:**
```bash
# Verify keytab contains the correct principal
klist -kt /path/to/your.keytab

# Test authentication manually
kinit -kt /path/to/your.keytab your-principal@YOUR.REALM

# Check if authentication succeeded
klist
```

#### Error: "GSSException: No valid credentials provided"

**Cause:** This typically occurs when the `storage.factory` Kerberos properties are not set, the keytab file path is incorrect or the file doesn't exist, or the Kerberos configuration (`krb5.conf`) is not properly configured.

**Solution:**
1. Verify all `storage.factory` Kerberos properties are correctly set in the configuration
2. Ensure the keytab file exists and has correct permissions
3. Check that `/etc/krb5.conf` (or `$JAVA_HOME/jre/lib/security/krb5.conf`) is properly configured with your Kerberos realm settings

#### Error: "Unable to obtain Kerberos password" or "Clock skew too great"

**Cause:** Time synchronization issue between Pinot server and Kerberos KDC.

**Solution:**
```bash
# Check time synchronization
date
# Ensure NTP is running and synchronized
sudo systemctl status ntpd
# Or for chrony
sudo systemctl status chronyd
```

Kerberos requires clock synchronization within 5 minutes (default) between client and KDC.

#### Error: "HDFS operation fails after running for several hours"

**Cause:** This typically indicates that manual `kinit` was used instead of `storage.factory` properties, and Kerberos tickets have expired (default 24 hours).

**Solution:**
1. Configure `storage.factory` Kerberos properties to enable automatic ticket renewal
2. Remove any manual `kinit` from startup scripts
3. Restart Pinot components to apply the configuration

#### Verifying Kerberos configuration

To verify your Kerberos setup is working correctly:

```bash
# 1. Test keytab authentication
kinit -kt /path/to/your.keytab your-principal@YOUR.REALM

# 2. Verify you can list HDFS directories
hdfs dfs -ls /

# 3. Check Pinot logs for authentication messages
tail -f /path/to/pinot/logs/pinot-controller.log | grep -i kerberos
tail -f /path/to/pinot/logs/pinot-server.log | grep -i kerberos

# 4. Look for successful authentication messages like:
# "Login successful for user <principal> using keytab file <keytab-path>"
```

#### Best practices

1. **Use absolute paths** for keytab files in configuration
2. **Secure keytab files** with appropriate permissions (400 or 600)
3. **Use service principals** (e.g., `pinot/hostname@REALM`) rather than user principals for production
4. **Monitor Kerberos ticket expiration** in logs to ensure automatic renewal is working
5. **Keep keytab files backed up** in secure locations
6. **Test configuration** in a non-production environment first
