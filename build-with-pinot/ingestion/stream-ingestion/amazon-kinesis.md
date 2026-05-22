---
description: >-
  This guide shows you how to ingest a stream of records from an Amazon Kinesis
  topic into a Pinot table.
---

# Ingest streaming data from Amazon Kinesis

To ingest events from an Amazon Kinesis stream into Pinot, set the following configs into your table config:

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
      "stream.kinesis.fetch.timeout.millis": "30000",
      "stream.kinesis.decoder.class.name": "org.apache.pinot.plugin.inputformat.json.JSONMessageDecoder",
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

| Property                     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| streamType                   | This should be set to "kinesis"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| stream.kinesis.topic.name    | Kinesis stream name                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| region                       | Kinesis region e.g. us-west-1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| accessKey                    | Kinesis access key                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| secretKey                    | Kinesis secret key                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| shardIteratorType            | AWS shard iterator type Pinot uses when it opens a shard iterator. Pinot passes this value through to the Kinesis client. **Default:** `LATEST`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| maxRecordsToFetch | Specifies the maximum number of records to retrieve in a single `getRecords` API call to Kinesis. This parameter controls the batch size for data retrieval. Can be set between 1 and 10,000 (Kinesis API limit by AWS) Larger values reduce the number of API calls needed but may increase latency and memory usage per batch. Default value is set to max 10000. Only lower this when you have memory constraints |
| requests\_per\_second\_limit | Controls the maximum Kinesis read requests per second Pinot will attempt per shard. Pinot applies this budget to both `getRecords` and `getShardIterator` reads, accepts fractional values such as `0.25`, and defaults to `1.0`. Start by dividing Kinesis's 5 `getRecords` requests-per-second shard limit across Pinot replicas, Pinot tables, and any non-Pinot consumers that share the shard. |

When Kinesis still returns `ProvisionedThroughputExceededException`, Pinot backs off and retries until the fetch timeout instead of immediately returning an empty batch. This makes fractional `requests_per_second_limit` values practical when several consumers need to share the same shard budget.

Kinesis supports authentication using the [DefaultCredentialsProviderChain](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/DefaultAWSCredentialsProviderChain.html). The credential provider looks for the credentials in the following order:

* Environment Variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (RECOMMENDED since they are recognized by all the AWS SDKs and CLI except for .NET), or `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` (only recognized by Java SDK)
* Java System Properties - `aws.accessKeyId` and `aws.secretKey`
* Web Identity Token credentials from the environment or container
* Credential profiles file at the default location `(~/.aws/credentials)` shared by all AWS SDKs and the AWS CLI
* Credentials delivered through the Amazon EC2 container service if `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` environment variable is set and security manager has permission to access the variable,
* Instance profile credentials delivered through the Amazon EC2 metadata service

{% hint style="info" %}
You must provide all `read` `access level` permissions for Pinot to work with an AWS Kinesis data stream. See the [AWS documentation](amazon-kinesis.md) for details.
{% endhint %}

Although you can also specify the `accessKey` and `secretKey` in the properties above, we don't recommend this insecure method. We recommend using it only for non-production proof-of-concept (POC) setups. You can also specify other AWS fields such as AWS\_SESSION\_TOKEN as environment variables and config and it will work.

### Resharding

In Kinesis, whenever you reshard a stream, it is done via split or merge operations on shards. If you split a shard, the shard closes and creates 2 new children shards. So if you started with shard0, and then split it, it would result in shard1 and shard2. Similarly, if you merge 2 shards, both those will close and create a child shard. So in the same example, if you merge shards 1 and 2, you'll end up with shard3 as the active shard, while shard0, shard1, shard2 will remain closed forever.

Please check out this recipe for more details: [https://dev.startree.ai/docs/pinot/recipes/github-events-stream-kinesis#resharding-kinesis-stream](https://dev.startree.ai/docs/pinot/recipes/github-events-stream-kinesis#resharding-kinesis-stream)

In Pinot, resharding of any stream is detected by periodic task RealtimeValidationManager: [docs](../../../reference/configuration-reference/controller.md#realtimesegmentvalidationmanager). This runs hourly. If you rehsard, your new shards will not get detected unless:

1. We finish ingesting from parent shards completely
2. And after 1, the RealtimeValidationManager runs

You will see a period where the ideal state will show all segments ONLINE, as parents have naturally completed ingesting, and we're waiting for RealtimeValidationManager to kickstart the ingestion from children.

If you need the ingestion to happen sooner, you can manually invoke the RealtimeValidationManager: [docs](../../../basics/components/cluster/controller.md#running-the-periodic-task-manually)

### Limitations

1. `ShardID` is of the format "**shardId-000000000001**". We use the numeric part as `partitionId`. Our `partitionId` variable is integer. If shardIds grow beyond `Integer.MAX\_VALUE`, we will overflow into the partitionId space.
2. Segment size based thresholds for segment completion will not work. It assumes that partition "0" always exists. However, once the shard 0 is split/merged, we will no longer have partition 0.
