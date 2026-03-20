---
description: This guide shows how to set up HDFS as deep storage for a Pinot segment.
---

# HDFS as Deep Storage

To use HDFS as deep storage you need to include HDFS dependency jars and plugins.

## Server Setup

### Configuration

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

### Executable

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

## Controller Setup

### Configuration

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

### Executable

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

## Broker Setup

### Configuration

```
pinot.set.instance.id.to.hostname=true
pinot.server.grpc.enable=true
```

### Executable

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

## Kerberos Authentication

When using HDFS with Kerberos security enabled, Pinot provides two ways to authenticate:

### 1. Automatic Authentication (Recommended)

By configuring the `storage.factory` Kerberos properties shown above, Pinot will automatically handle Kerberos authentication using the specified keytab and principal. This eliminates the need for manual `kinit` commands and ensures continuous authentication even after ticket expiration.

#### Why These Properties Are Required

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

#### Understanding the Two Sets of Kerberos Properties

You may notice two sets of Kerberos properties in the configuration:

1. **`storage.factory` properties (NEW - Recommended):**
   - `pinot.controller.storage.factory.hdfs.hadoop.kerberos.principal`
   - `pinot.controller.storage.factory.hdfs.hadoop.kerberos.keytab`
   - `pinot.server.storage.factory.hdfs.hadoop.kerberos.principal`
   - `pinot.server.storage.factory.hdfs.hadoop.kerberos.keytab`
   
   **Purpose:** These properties configure Kerberos authentication for the HadoopPinotFS storage factory, which handles:
   - Controller's deep storage operations (reading/writing to `controller.data.dir`)
   - Server's deep storage operations
   - General HDFS filesystem operations through the storage factory
   
   **Why needed:** The storage factory is initialized at startup and used throughout the component's lifecycle for HDFS access. Without these properties, any HDFS operation through the storage factory would fail with authentication errors.

2. **`segment.fetcher` properties (Legacy - For backward compatibility):**
   - `pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.principle` (note: typo "principle" instead of "principal" maintained for compatibility)
   - `pinot.controller.segment.fetcher.hdfs.hadoop.kerberos.keytab`
   - `pinot.server.segment.fetcher.hdfs.hadoop.kerberos.principle`
   - `pinot.server.segment.fetcher.hdfs.hadoop.kerberos.keytab`
   
   **Purpose:** These configure Kerberos for the segment fetcher component specifically
   
   **Why both are needed:** While there is some functional overlap, having both ensures:
   - Complete coverage of all HDFS access patterns
   - Backward compatibility with existing deployments
   - Segment fetcher operations work independently of storage factory

#### Benefits of Automatic Authentication

**No Manual Intervention:**
- Eliminates the need to run `kinit` commands manually
- Reduces operational overhead and human error
- Enables fully automated deployments

**Automatic Ticket Renewal:**
- Kerberos tickets typically expire after 24 hours (configurable)
- Manual `kinit` requires re-authentication before expiration
- With keytab-based authentication, Pinot automatically renews tickets internally
- Prevents service disruptions due to expired tickets

**Production Reliability:**
- Manual authentication is unsuitable for production as it requires:
  - Someone to monitor ticket expiration times
  - Manual intervention during off-hours if tickets expire
  - Service restarts or re-authentication during critical operations
- Automatic authentication runs 24/7 without human intervention

**Security Best Practices:**
- Keytab files provide secure, long-term credentials
- No need to store passwords in scripts or configuration
- Keytabs can be managed through enterprise key management systems
- Follows Hadoop's recommended security practices

### 2. Manual Authentication (Legacy)

Alternatively, you can manually authenticate using `kinit` before starting Pinot components:

```bash
kinit -kt <your kerberos keytab> <your kerberos principal>
```

**Limitations of Manual Authentication:**
- **Ticket Expiration:** Kerberos tickets typically expire after 24 hours, requiring re-authentication
- **Service Interruption:** If tickets expire while Pinot is running, HDFS operations will fail until re-authentication
- **Operational Burden:** Requires monitoring and manual intervention, especially problematic for 24/7 production systems
- **Automation Challenges:** Difficult to integrate into automated deployment pipelines
- **Not Recommended:** This approach is only suitable for development/testing environments

**Note:** Manual authentication is not recommended for production environments. Always use the `storage.factory` Kerberos properties for production deployments.

## Troubleshooting

### HDFS FileSystem Issues

If you receive an error that says `No FileSystem for scheme"hdfs"`, the problem is likely to be a class loading issue.

To fix, try adding the following property to `core-site.xml`:

```fs.hdfs.impl org.apache.hadoop.hdfs.DistributedFileSystem```

And then export `/opt/pinot/lib/hadoop-common-<release-version>.jar` in the classpath.

### Kerberos Authentication Issues

#### Error: "Failed to authenticate with Kerberos"

**Possible Causes:**
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

**Cause:** This typically occurs when:
- The `storage.factory` Kerberos properties are not set
- The keytab file path is incorrect or the file doesn't exist
- The Kerberos configuration (`krb5.conf`) is not properly configured

**Solution:**
1. Verify all `storage.factory` Kerberos properties are correctly set in the configuration
2. Ensure the keytab file exists and has correct permissions
3. Check that `/etc/krb5.conf` (or `$JAVA_HOME/jre/lib/security/krb5.conf`) is properly configured with your Kerberos realm settings

#### Error: "Unable to obtain Kerberos password" or "Clock skew too great"

**Cause:** Time synchronization issue between Pinot server and Kerberos KDC

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

**Cause:** This typically indicates that:
- Manual `kinit` was used instead of `storage.factory` properties
- Kerberos tickets have expired (default 24 hours)

**Solution:**
1. Configure `storage.factory` Kerberos properties to enable automatic ticket renewal
2. Remove any manual `kinit` from startup scripts
3. Restart Pinot components to apply the configuration

#### Verifying Kerberos Configuration

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

#### Best Practices

1. **Use absolute paths** for keytab files in configuration
2. **Secure keytab files** with appropriate permissions (400 or 600)
3. **Use service principals** (e.g., `pinot/hostname@REALM`) rather than user principals for production
4. **Monitor Kerberos ticket expiration** in logs to ensure automatic renewal is working
5. **Keep keytab files backed up** in secure locations
6. **Test configuration** in a non-production environment first
