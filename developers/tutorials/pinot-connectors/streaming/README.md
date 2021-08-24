# Streaming

## Pluggable Streams

Note

This section is a pre-read if you are planning to develop plug-ins for streams other than Kafka. Pinot supports Kafka out of the box.

Prior to commit [ba9f2d](https://github.com/apache/pinot/commit/ba9f2ddfc0faa42fadc2cc48df1d77fec6b174fb), Pinot was only able to support consuming from [Kafka](https://kafka.apache.org/documentation/) stream.

Pinot now enables its users to write plug-ins to consume from pub-sub streams other than Kafka. \(Please refer to [Issue \#2583](https://github.com/apache/pinot/issues/2583)\)

Some of the streams for which plug-ins can be added are:

* [Amazon kinesis](https://docs.aws.amazon.com/streams/latest/dev/building-enhanced-consumers-kcl.html)
* [Azure Event Hubs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-java-get-started-receive-eph)
* [LogDevice](https://code.fb.com/core-data/logdevice-a-distributed-data-store-for-logs/)
* [Pravega](http://pravega.io/docs/latest/javadoc/)
* [Pulsar](https://pulsar.apache.org/docs/en/client-libraries-java/)

You may encounter some limitations either in Pinot or in the stream system while developing plug-ins. Please feel free to get in touch with us when you start writing a stream plug-in, and we can help you out. We are open to receiving PRs in order to improve these abstractions if they do not work for a certain stream implementation.

Refer to [Consuming and Indexing rows in Realtime](https://cwiki.apache.org/confluence/display/PINOT/Consuming+and+Indexing+rows+in+Realtime) for details on how Pinot consumes streaming data.

