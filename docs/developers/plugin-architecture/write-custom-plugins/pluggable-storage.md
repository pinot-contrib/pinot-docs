# Filesystem Plugin

Pinot enables its users to write a PinotFS abstraction layer to store data in a data layer of their choice for real-time and offline segments.

Some examples of storage backends(other than local storage) currently supported are:

* [HadoopFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html)
* [Azure Data Lake](https://azure.microsoft.com/en-us/solutions/data-lake/)

If the above two filesystems do not meet your needs, you can extend the current [PinotFS](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/filesystem/PinotFS.java) to customize for your needs.

## New Storage Type implementation

In order to add a new type of storage backend such as Amazon S3 we need to implement the [PinotFS](https://github.com/apache/pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/filesystem/PinotFS.java) class. The interface expects common method related to accessing the file system such as `mkdir`, `list` etc.

Once the the class is ready, you can compile it and put it in the `/plugins` directory of pinot.

## Using plugin in real-time table

You can set the configuration in real time or batch tables by using base scheme of URI (scheme://host:port/path) as suffix.\
e.g. for the path `hdfs://user/yarn/path/to/dir` , the base scheme is `hdfs` and all the config keys should have `hdfs` in them such `pinot.controller.storage.factory.hdfs`

The example here uses the existing `org.apache.pinot.filesystem.HadoopPinotFS` to store real-time segments in a HDFS filesytem. In the Pinot controller config, add the following new configs:

```
"controller.data.dir": "SET_TO_YOUR_HDFS_ROOT_DIR"
"controller.local.temp.dir": "SET_TO_A_LOCAL_FILESYSTEM_DIR"
"pinot.controller.storage.factory.class.hdfs": "org.apache.pinot.filesystem.HadoopPinotFS"
"pinot.controller.storage.factory.hdfs.hadoop.conf.path": "SET_TO_YOUR_HDFS_CONFIG_DIR"
"pinot.controller.storage.factory.hdfs.hadoop.kerberos.principle": "SET_IF_YOU_USE_KERBEROS"
"pinot.controller.storage.factory.hdfs.hadoop.kerberos.keytab": "SET_IF_YOU_USE_KERBEROS"
"controller.enable.split.commit": "true"
```

In the Pinot controller config, add the following new configs:

```
"pinot.server.instance.enable.split.commit": "true"
```

## Configurations for Offline Tables

These properties for the stream implementation are to be set in your controller and server configurations.

In your controller and server configs, set the FS class you would like to support. `pinot.controller.storage.factory.class.${YOUR_URI_SCHEME}` to the full path of the FS class you would like to include

You also need to configure `pinot.controller.local.temp.dir` for the local dir on the controller machine.

For filesystem specific configs, you can pass in the following with either the pinot.controller prefix or the pinot.server prefix.

All the following configs need to be prefixed with storage.factory.

e.g. AzurePinotFS requires the following configs according to your environment:

`adl.accountId`, `adl.authEndpoint,` `adl.clientId`, `adl.clientSecret`

Sample Controller Config

```
"pinot.controller.storage.factory.class.adl": "org.apache.pinot.filesystem.AzurePinotFS"
"pinot.controller.storage.factory.adl.accountId": "xxxx"
"pinot.controller.storage.factory.adl.authEndpoint": "xxxx"
"pinot.controller.storage.factory.adl.clientId": "xxxx"
"pinot.controller.segment.fetcher.protocols": "adl"
```

Sample Server Config

```
"pinot.server.storage.factory.class.adl": "org.apache.pinot.filesystem.AzurePinotFS"
"pinot.server.storage.factory.adl.accountId": "xxxx"
"pinot.server.storage.factory.adl.authEndpoint": "xxxx"
"pinot.server.storage.factory.adl.clientId": "xxxx"
"pinot.server.segment.fetcher.protocols": "adl"
```

You can find the parameters in your account as follows: [https://stackoverflow.com/questions/56349040/what-is-clientid-authtokenendpoint-clientkey-for-accessing-azure-data-lake](https://stackoverflow.com/questions/56349040/what-is-clientid-authtokenendpoint-clientkey-for-accessing-azure-data-lake)

Also make sure to set the following config with the value `adl`

```
"segment.fetcher.protocols" : "adl"
```

To see how to upload segments to different storage systems, check [Batch Segment Fetcher Plugin](write-your-batch.md).
