# Creating Pinot Segments

#### Realtime segment generation

To consume in realtime, we simply need to create a table with the same name as the schema and point to the Kafka topic to consume from, using a table definition such as this one:

```text
{
  "tableName": "flights",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "7",
    "segmentPushFrequency": "daily",
    "segmentPushType": "APPEND",
    "replication": "1",
    "timeColumnName": "daysSinceEpoch",
    "timeType": "DAYS",
    "segmentAssignmentStrategy": "BalanceNumSegmentAssignmentStrategy"
  },
  "tableIndexConfig": {
    "invertedIndexColumns": [
      "flightNumber",
      "tags",
      "daysSinceEpoch"
    ],
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "highLevel",
      "stream.kafka.topic.name": "flights-realtime",
      "stream.kafka.decoder.class.name": "org.apache.pinot.core.realtime.impl.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.zk.broker.url": "localhost:2181",
      "stream.kafka.hlc.zk.connect.string": "localhost:2181"
    }
  },
  "tenants": {
    "broker": "brokerTenant",
    "server": "serverTenant"
  },
  "metadata": {
  }
}
```

First, we’ll start a local instance of Kafka and start streaming data into it:Untitled

```text
bin/pinot-admin.sh StartKafka &
bin/pinot-admin.sh StreamAvroIntoKafka -avroFile flights-2014.avro -kafkaTopic flights-realtime &
```

This will stream one event per second from the Avro file to the Kafka topic. Then, we’ll create a realtime table, which will start consuming from the Kafka topic.

```text
bin/pinot-admin.sh AddTable -filePath flights-definition-realtime.json
```

We can then query the table with the following query to see the events stream in:

```text
SELECT COUNT(*) FROM flights
```

Repeating the query multiple times should show the events slowly being streamed into the table.

