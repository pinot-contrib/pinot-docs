# Amazon Kinesis

{% hint style="warning" %}
This is not tested in production. You may hit some snags while trying to use this.
{% endhint %}

To ingest events from an Amazon Kinesis stream into Pinot, set the following configs into the table config

```text
{
  "tableName": "kinesisTable",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "timestamp",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kinesis",
      "stream.kinesis.topic.name": "<your kinesis stream name>",
      "region": "<your region>",
      "accessKey": "<your access key>",
      "secretKey": "<your secret key>",
      "shardIteratorType": "AFTER_SEQUENCE_NUMBER",
      "stream.kinesis.consumer.type": "lowlevel",
      "stream.kinesis.fetch.timeout.millis": "30000",
      "stream.kinesis.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kinesis.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kinesis.KinesisConsumerFactory",
      "realtime.segment.flush.threshold.size": "1000000",
      "realtime.segment.flush.threshold.time": "6h"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}

```

where the Kinesis specific properties are:

| Property | Description |
| :--- | :--- |
| streamType | This should be set to "kinesis" |
| stream.kinesis.topic.name | Kinesis stream name |
| region | Kinesis region e.g. us-west-1 |
| accessKey | Kinesis access key |
| secretKey | Kinesis secret key |
| shardIteratorType | Set to "LATEST" for largest offset \(default\), "AFTER\__SEQUENCE_\_NUMBER" for earliest offset |
| maxRecordsToFetch | ... Default is 20. |

#### Limitations

1. ShardID is of the format "**shardId-000000000001**". We use the numeric part as partitionId. Our partitionId variable is integer. If shardIds grow beyond Integer.MAX\_VALUE, we will overflow
2. Segment size based thresholds for segment completion will not work. It assumes that partition "0" always exists. However, once the shard 0 is split/merged, we will no longer have partition 0.



