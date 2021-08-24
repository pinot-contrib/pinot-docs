# Streaming Tables

### Configurations for Streaming Tables

The example here uses the existing org.apache.pinot.filesystem.HadoopPinotFS to store realtime segments in a HDFS filesytem. In the Pinot controller config, add the following new configs:

```text
"controller.data.dir": "SET_TO_YOUR_HDFS_ROOT_DIR"
"controller.local.temp.dir": "SET_TO_A_LOCAL_FILESYSTEM_DIR"
"pinot.controller.storage.factory.class.hdfs": "org.apache.pinot.filesystem.HadoopPinotFS"
"pinot.controller.storage.factory.hdfs.hadoop.conf.path": "SET_TO_YOUR_HDFS_CONFIG_DIR"
"pinot.controller.storage.factory.hdfs.hadoop.kerberos.principle": "SET_IF_YOU_USE_KERBEROS"
"pinot.controller.storage.factory.hdfs.hadoop.kerberos.keytab": "SET_IF_YOU_USE_KERBEROS"
"controller.enable.split.commit": "true"
```

In the Pinot controller config, add the following new configs:

```text
"pinot.server.instance.enable.split.commit": "true"
```

Note: currently there is a bug in the controller \(issue &lt;https://github.com/apache/pinot/issues/3847&gt;\), for now you can cherrypick the PR [https://github.com/apache/pinot/pull/3849](https://github.com/apache/pinot/pull/3849) to fix the issue as tested already. The PR is under review now.

