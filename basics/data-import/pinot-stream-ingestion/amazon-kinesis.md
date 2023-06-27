---
description: >-
  This guide shows you how to ingest a stream of records from an Amazon Kinesis
  topic into a Pinot table.
---

# Import from Amazon Kinesis

To ingest events from an Amazon Kinesis stream into Pinot, set the following configs into the table config:

```json
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
      "realtime.segment.flush.threshold.rows": "1000000",
      "realtime.segment.flush.threshold.time": "6h"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

where the Kinesis specific properties are:

| Property                  | Description                                                                                                                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| streamType                | This should be set to "kinesis"                                                                                                                                                                     |
| stream.kinesis.topic.name | Kinesis stream name                                                                                                                                                                                 |
| region                    | Kinesis region e.g. us-west-1                                                                                                                                                                       |
| accessKey                 | Kinesis access key                                                                                                                                                                                  |
| secretKey                 | Kinesis secret key                                                                                                                                                                                  |
| shardIteratorType         | Set to LATEST to consume only new records, TRIM\_HORIZON for earliest sequence number_,_ AT_\__SEQUENCE\_NUMBER and AFTER\_SEQUENCE\_NUMBER to start consumptions from a particular sequence number |
| maxRecordsToFetch         | ... Default is 20.                                                                                                                                                                                  |

Kinesis supports authentication using the [DefaultCredentialsProviderChain](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/DefaultAWSCredentialsProviderChain.html). The credential provider looks for the credentials in the following order -

* Environment Variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (RECOMMENDED since they are recognized by all the AWS SDKs and CLI except for .NET), or `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` (only recognized by Java SDK)
* Java System Properties - `aws.accessKeyId` and `aws.secretKey`
* Web Identity Token credentials from the environment or container
* Credential profiles file at the default location `(~/.aws/credentials)` shared by all AWS SDKs and the AWS CLI
* Credentials delivered through the Amazon EC2 container service if `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` environment variable is set and security manager has permission to access the variable,
* Instance profile credentials delivered through the Amazon EC2 metadata service

Although you can also specify the `accessKey` and `secretKey` in the properties above, we don't recommend this unsecure method. We recommend using it only for non-production proof-of-concept (POC) setups. You can also specify other AWS fields such as AWS\_SESSION\_TOKEN as environment variables and config and it will work.

#### Limitations

1. `ShardID` is of the format "**shardId-000000000001**". We use the numeric part as `partitionId`. Our `partitionId` variable is integer. If shardIds grow beyond `Integer.MAX\_VALUE`, we will overflow into the partitionId space.
2. Segment size based thresholds for segment completion will not work. It assumes that partition "0" always exists. However, once the shard 0 is split/merged, we will no longer have partition 0.
