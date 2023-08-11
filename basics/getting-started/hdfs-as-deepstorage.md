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
