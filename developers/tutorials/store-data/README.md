# Store Data

## Pinot Persistent Layers

By default, Pinot does not come with a storage layer, so all the data sent, won't be stored in case of system crash. In order to persistently store the generated segments, you will need a storage layer.

Pinot enables its users to write a PinotFS abstraction layer to store data in a data layer of their choice for realtime and offline segments.

Some examples of storage backends\(other than local storage\) currently supported are:

* [HadoopFS](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/FileSystemShell.html)
* [Azure Data Lake](https://azure.microsoft.com/en-us/solutions/data-lake/)

If the above two filesystems do not meet your needs, you can extend the current [PinotFS](https://github.com/apache/pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/filesystem/PinotFS.java) to customize for your needs.

### New Storage Type implementation

In order to add a new type of storage backend \(say, Amazon s3\) implement the following class:

S3FS extends [PinotFS](https://github.com/apache/pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/filesystem/PinotFS.java)

