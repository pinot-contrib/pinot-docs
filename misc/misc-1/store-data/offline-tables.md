# Batch Tables

### Configurations for Batch Tables

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

