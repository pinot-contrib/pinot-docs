---
description: This page describes how to write your own stream ingestion plugin for Pinot.
---

# Stream Ingestion Plugin

You can write custom stream ingestion plugins to add support for your own streaming platforms such as Pravega, Kinesis etc.

Stream Ingestion Plugins can be of two types -

* High Level - Consume data without control over the partitions
* Low Level - Consume data from each partition with offset management

### Requirements to support Stream Level \(High Level\) consumers

The stream should provide the following guarantees:

* Exactly once delivery \(unless restarting from a checkpoint\) for each consumer of the stream.
* \(Optionally\) support mechanism to split events \(in some arbitrary fashion\) so that each event in the stream is delivered exactly to one host out of set of hosts.
* Provide ways to save a checkpoint for the data consumed so far. If the stream is partitioned, then this checkpoint is a vector of checkpoints for events consumed from individual partitions.
* The checkpoints should be recorded only when Pinot makes a call to do so.
* The consumer should be able to start consumption from one of:
  * latest available data
  * earliest available data
  * last saved checkpoint

### Requirements to support Partition Level \(Low Level\) consumers

While consuming rows at a partition level, the stream should support the following properties:

* Stream should provide a mechanism to get the current number of partitions.
* Each event in a partition should have a unique offset that is not more than 64 bits long.
* Refer to a partition as a number not exceeding 32 bits long.
* Stream should provide the following mechanisms to get an offset for a given partition of the stream:
  * get the offset of the oldest event available \(assuming events are aged out periodically\) in the partition.
  * get the offset of the most recent event published in the partition
  * \(optionally\) get the offset of an event that was published at a specified time
* Stream should provide a mechanism to consume a set of events from a partition starting from a specified offset.
* Pinot assumes that the offsets of incoming events are monotonically increasing; _i.e._, if Pinot consumes an event at offset `o1`, then the offset `o2` of the following event should be such that `o2 > o1`.

In addition, we have an operational requirement that the number of partitions should not be reduced over time.

### Stream plug-in implementation

In order to add a new type of stream \(say, Foo\) implement the following classes:

1. FooConsumerFactory extends [StreamConsumerFactory](https://github.com/apache/incubator-pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/stream/StreamConsumerFactory.java)
2. FooPartitionLevelConsumer implements [PartitionLevelConsumer](https://github.com/apache/incubator-pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/stream/PartitionLevelConsumer.java)
3. FooStreamLevelConsumer implements [StreamLevelConsumer](https://github.com/apache/incubator-pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/stream/StreamLevelConsumer.java)
4. FooMetadataProvider implements [StreamMetadataProvider](https://github.com/apache/incubator-pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/stream/StreamMetadataProvider.java)
5. FooMessageDecoder implements [StreamMessageDecoder](https://github.com/apache/incubator-pinot/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/stream/StreamMessageDecoder.java)

Depending on stream level or partition level, your implementation needs to include StreamLevelConsumer or PartitionLevelConsumer.

The properties for the stream implementation are to be set in the table configuration, inside `streamConfigs` section.

Use the `streamType` property to define the stream type. For example, for the implementation of stream `foo`, set the property `"streamType" : "foo"`.

The rest of the configuration properties for your stream should be set with the prefix `"stream.foo"`. Be sure to use the same suffix for: \(see examples below\):

* topic
* consumer type
* stream consumer factory
* offset
* decoder class name
* decoder properties
* connection timeout
* fetch timeout

All values should be strings. For example:

```text
"streamType" : "foo",
"stream.foo.topic.name" : "SomeTopic",
"stream.foo.consumer.type": "LowLevel",
"stream.foo.consumer.factory.class.name": "fully.qualified.pkg.ConsumerFactoryClassName",
"stream.foo.consumer.prop.auto.offset.reset": "largest",
"stream.foo.decoder.class.name" : "fully.qualified.pkg.DecoderClassName",
"stream.foo.decoder.prop.a.decoder.property" : "decoderPropValue",
"stream.foo.connection.timeout.millis" : "10000", // default 30_000
"stream.foo.fetch.timeout.millis" : "10000" // default 5_000
```

You can have additional properties that are specific to your stream. For example:

```text
"stream.foo.some.buffer.size" : "24g"
```

In addition to these properties, you can define thresholds for the consuming segments:

* rows threshold
* time threshold

The properties for the thresholds are as follows:

```text
"realtime.segment.flush.threshold.size" : "100000"
"realtime.segment.flush.threshold.time" : "6h"
```

An example of this implementation can be found in the [KafkaConsumerFactory](https://github.com/apache/incubator-pinot/blob/master/pinot-plugins/pinot-stream-ingestion/pinot-kafka-2.0/src/main/java/org/apache/pinot/plugin/stream/kafka20/KafkaConsumerFactory.java), which is an implementation for the kafka stream.

### 

