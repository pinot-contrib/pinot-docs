# Pluggable Storage

Pinot enables its users to write a PinotFS abstraction layer to store data in a data layer of their choice for realtime and offline segments.

Some examples of storage backends\(other than local storage\) currently supported are:

* [HadoopFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html)
* [Azure Data Lake](https://azure.microsoft.com/en-us/solutions/data-lake/)

If the above two filesystems do not meet your needs, you can extend the current [PinotFS](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/filesystem/PinotFS.java) to customize for your needs.

### New Storage Type implementation

In order to add a new type of storage backend \(say, Amazon s3\) implement the following class:

S3FS extends [PinotFS](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/filesystem/PinotFS.java)

### Configurations for Realtime Tables

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

Note: currently there is a bug in the controller \(issue &lt;https://github.com/apache/incubator-pinot/issues/3847&gt;\), for now you can cherrypick the PR [https://github.com/apache/incubator-pinot/pull/3849](https://github.com/apache/incubator-pinot/pull/3849) to fix the issue as tested already. The PR is under review now.

### Configurations for Offline Tables

These properties for the stream implementation are to be set in your controller and server configurations.

In your controller and server configs, please set the FS class you would like to support. pinot.controller.storage.factory.class.${YOUR\_URI\_SCHEME} to the full path of the FS class you would like to include

You also need to configure pinot.controller.local.temp.dir for the local dir on the controller machine.

For filesystem specific configs, you can pass in the following with either the pinot.controller prefix or the pinot.server prefix.

All the following configs need to be prefixed with storage.factory.

AzurePinotFS requires the following configs according to your environment:

adl.accountId, adl.authEndpoint, adl.clientId, adl.clientSecret

Sample Controller Config

```text
"pinot.controller.storage.factory.class.adl": "org.apache.pinot.filesystem.AzurePinotFS"
"pinot.controller.storage.factory.adl.accountId": "xxxx"
"pinot.controller.storage.factory.adl.authEndpoint": "xxxx"
"pinot.controller.storage.factory.adl.clientId": "xxxx"
"pinot.controller.storage.factory.adl.clientId": "xxxx"
"pinot.controller.segment.fetcher.protocols": "adl"
```

Sample Server Config

```text
"pinot.server.storage.factory.class.adl": "org.apache.pinot.filesystem.AzurePinotFS"
"pinot.server.storage.factory.adl.accountId": "xxxx"
"pinot.server.storage.factory.adl.authEndpoint": "xxxx"
"pinot.server.storage.factory.adl.clientId": "xxxx"
"pinot.server.storage.factory.adl.clientId": "xxxx"
"pinot.server.segment.fetcher.protocols": "adl"
```

You can find the parameters in your account as follows: [https://stackoverflow.com/questions/56349040/what-is-clientid-authtokenendpoint-clientkey-for-accessing-azure-data-lake](https://stackoverflow.com/questions/56349040/what-is-clientid-authtokenendpoint-clientkey-for-accessing-azure-data-lake)

Please also make sure to set the following config with the value “adl”

```text
"segment.fetcher.protocols" : "adl"
```

To see how to upload segments to different storage systems, check `../segment_fetcher.rst`.

HadoopPinotFS requires the following configs according to your environment:

hadoop.kerberos.principle, hadoop.kerberos.keytab, hadoop.conf.path

Please make sure to also set the following config with the value “hdfs”

```text
"segment.fetcher.protocols" : "hdfs"
```

