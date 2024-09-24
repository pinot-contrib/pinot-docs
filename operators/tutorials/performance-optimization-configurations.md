# Performance Optimization Configurations

#### Query Option to Enable \`AND\` Predicate Reordering

An optional optimization for queries with  long `AND` predicate will be to let execution engine reorder the predicates based on cardinality, so as to do minimum scanning for un-indexed operators. To use it, simply add the following option to the original query&#x20;

```
SET AndScanReordering = 'True'; SELECT FOO from BAR WHERE predicate1 AND predicate2 AND predicate3 AND predicate4 ...
```

This feature cannot guarantee optimization for all use cases, but on average it can help. Try with some before/after comparison.

PR: [https://github.com/apache/pinot/pull/9420](https://github.com/apache/pinot/pull/9420)

#### Enabling Server Side Segment Stream Download-Untar with rate limiter:

Pinot server supports segment download-untar with rate limiter, which reduces the bytes written to disk and optimizes disk bandwidth usage [https://github.com/apache/pinot/pull/8753](https://github.com/apache/pinot/pull/8753). This feature involves the following server level configs

```
pinot.server.instance.segment.stream.download.untar : true
// enable stream download and untar 
pinot.server.instance.segment.stream.download.untar.rate.limit.bytes.per.sec : 100000000
// the max download-untar rate is limited to 100000000 bytes/sec
```

Another useful config is:

```
pinot.server.instance.table.level.max.parallel.segment.downloads : 4
```

This helps to limit the number of max parallel number of segment download per table, at server level

#### Enabling Netty Native TLS:

Apache Pinot supports using native TLS library [https://netty.io/wiki/forked-tomcat-native.html](https://netty.io/wiki/forked-tomcat-native.html) for broker-server transmission, which would potentially boost TLS encryption/decryption performance. This can be enabled by adding the following broker/server config

```
pinot.broker.tls.ssl.provider :  OPENSSL
pinot.server.tls.ssl.provider :  OPENSSL
```

#### Enabling Netty Native Transport:

Apache Pinot supports using native transport library [https://netty.io/wiki/native-transports.html](https://netty.io/wiki/native-transports.html)  for broker-server transmission, which would potentially boost performance under high QPS. This can be enabled using:

<pre><code><strong>pinot.broker.netty.native.transports.enabled : true
</strong>pinot.server.netty.native.transports.enabled : true</code></pre>
