---
description: >-
  Steps for setting up a Pinot cluster and a realtime table which consumes from
  the Github events stream.
---

# Github Events Stream

## Pull Request Merged Events Stream

In this recipe, we will

1. Set up a Pinot cluster, in the steps

   a. Start zookeeper

   b. Start controller

   c. Start broker

   d. Start server

2. Set up a Kafka cluster
3. Create a topic - pullRequestMergedEvents
4. Create a realtime table - pullRequestMergedEvents and a schema
5. Start a task which reads from Github events API and publishes events about merged pull requests to the topic.
6. Query the realtime data

{% hint style="info" %}
**Prerequisites**

Getting Pinot - [Build](../running-pinot-locally.md#build)

Generate a [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) on Github.
{% endhint %}

We will use the `pinot-admin.sh` script in `apache-pinot-incubating-0.3.0-bin` directory from the Pinot source

### Short Version

For a single command to setup all the above steps

```text
bin/pinot-admin.sh GithubEventsQuickStart \
  -personalAccessToken <personal_access_token>
```

### Long Version

{% hint style="info" %}
If you already have a cluster running, scroll down to [Create topic](github-events-stream.md#create-topic)
{% endhint %}

#### Start Zookeeper

```
$ bin/pinot-admin.sh StartZookeeper \
  -zkPort 2191 
```

#### Start Controller

```
$ bin/pinot-admin.sh StartController \
  -zkAddress localhost:2191 \
  -clusterName PinotCluster \
  -controllerPort 9000 
```

#### Start Broker

```
$ bin/pinot-admin.sh StartBroker \
  -zkAddress localhost:2191 \
  -clusterName PinotCluster \
  -brokerPort 7000
```

#### Start Server

```
$ bin/pinot-admin.sh StartServer \
  -zkAddress localhost:2191 \
  -clusterName PinotCluster \
  -serverPort 8000
```

#### Start Kafka

```
$ bin/pinot-admin.sh  StartKafka \
  -zkAddress=localhost:2191/kafka \
  -port 19092
```

#### Create topic

Download [Apache Kafka](https://kafka.apache.org/downloads) release

```
$ bin/kafka-topics.sh \
  --create \
  --bootstrap-server localhost:19092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic pullRequestMergedEvents
```

#### Add table and schema

Schema can be found at  `/examples/stream/githubevents/` in the release, and is also pasted below:

```bash
{
  "schemaName": "pullRequestMergedEvents",
  "dimensionFieldSpecs": [
    {
      "name": "title",
      "dataType": "STRING",
      "defaultNullValue": ""
    },
    {
      "name": "labels",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "userId",
      "dataType": "STRING",
      "defaultNullValue": ""
    },
    {
      "name": "userType",
      "dataType": "STRING",
      "defaultNullValue": ""
    },
    {
      "name": "authorAssociation",
      "dataType": "STRING",
      "defaultNullValue": ""
    },
    {
      "name": "mergedBy",
      "dataType": "STRING",
      "defaultNullValue": ""
    },
    {
      "name": "assignees",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "authors",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "committers",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "requestedReviewers",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "requestedTeams",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "reviewers",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "commenters",
      "dataType": "STRING",
      "singleValueField": false,
      "defaultNullValue": ""
    },
    {
      "name": "repo",
      "dataType": "STRING",
      "defaultNullValue": ""
    },
    {
      "name": "organization",
      "dataType": "STRING",
      "defaultNullValue": ""
    }
  ],
  "metricFieldSpecs": [
    {
      "name": "count",
      "dataType": "LONG",
      "defaultNullValue": 1
    },
    {
      "name": "numComments",
      "dataType": "LONG"
    },
    {
      "name": "numReviewComments",
      "dataType": "LONG"
    },
    {
      "name": "numCommits",
      "dataType": "LONG"
    },
    {
      "name": "numLinesAdded",
      "dataType": "LONG"
    },
    {
      "name": "numLinesDeleted",
      "dataType": "LONG"
    },
    {
      "name": "numFilesChanged",
      "dataType": "LONG"
    },
    {
      "name": "numAuthors",
      "dataType": "LONG"
    },
    {
      "name": "numCommitters",
      "dataType": "LONG"
    },
    {
      "name": "numReviewers",
      "dataType": "LONG"
    },
    {
      "name": "numCommenters",
      "dataType": "LONG"
    },
    {
      "name": "createdTimeMillis",
      "dataType": "LONG"
    },
    {
      "name": "elapsedTimeMillis",
      "dataType": "LONG"
    }
  ],
  "timeFieldSpec": {
    "incomingGranularitySpec": {
      "timeType": "MILLISECONDS",
      "timeFormat": "EPOCH",
      "dataType": "LONG",
      "name": "mergedTimeMillis"
    }
  }
}

```

Table config can be found at `/examples/stream/githubevents/` in the release, and is also pasted below.

{% hint style="info" %}
Note

If you're setting this up on a pre-configured cluster, set the properties `stream.kafka.zk.broker.url` and `stream.kafka.broker.list` correctly, depending on the configuration of your Kafka cluster.  
{% endhint %}

```bash
{
  "tableName": "pullRequestMergedEvents",
  "tableType": "REALTIME",
  "segmentsConfig": {
    "timeColumnName": "mergedTimeMillis",
    "timeType": "MILLISECONDS",
    "retentionTimeUnit": "DAYS",
    "retentionTimeValue": "60",
    "schemaName": "pullRequestMergedEvents",
    "replication": "1",
    "replicasPerPartition": "1"
  },
  "tenants": {},
  "tableIndexConfig": {
    "loadMode": "MMAP",
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "simple",
      "stream.kafka.topic.name": "pullRequestMergedEvents",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.zk.broker.url": "localhost:2191/kafka",
      "stream.kafka.broker.list": "localhost:19092",
      "realtime.segment.flush.threshold.time": "12h",
      "realtime.segment.flush.threshold.size": "100000",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```

Add table using the command

```
$ bin/pinot-admin.sh AddTable \
  -tableConfigFile <path_to_configs>/examples/stream/githubEvents/pullRequestMergedEvents_realtime_table_config.json \
  -schemaFile <path_to_configs>/examples/stream/githubEvents/pullRequestMergedEvents_schema.json -exec
```

#### Publish events

Start the streaming job using the command

```text
$ bin/pinot-admin.sh StreamGithubEvents \
  -topic pullRequestMergedEvents \
  -personalAccessToken <personal_access_token> \
  -schemaFile <path_to_configs>/examples/stream/githubEvents/pullRequestMergedEvents_schema.json
```

### Kubernetes cluster

If you already have a Kubernetes cluster with Pinot and Kafka \(see [Running Pinot in Kubernetes](../kubernetes-quickstart.md)\), first create the topic and then setup the table and streaming using

```text
$ cd kubernetes/helm
$ kubectl apply -f pinot-github-realtime-events.yml
```

### Query

Head over to the [Query Console](http://localhost:9000/query) to checkout the data.

![](../../.gitbook/assets/screen-shot-2020-03-26-at-6.27.43-pm.png)

### 



