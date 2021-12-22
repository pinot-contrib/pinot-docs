---
description: >-
  Steps for setting up a Pinot cluster and a realtime table which consumes from
  the GitHub events stream.
---

# GitHub Events Stream

## Pull Request Merged Events Stream

In this recipe, we will

1. Set up a Pinot cluster, in the steps

   a. Start zookeeper

   b. Start controller

   c. Start broker

   d. Start server

2. Set up a Kafka cluster
3. Create a Kafka topic - pullRequestMergedEvents
4. Create a realtime table - pullRequestMergedEvents and a schema
5. Start a task which reads from [GitHub events API ](https://developer.github.com/v3/activity/events/)and publishes events about merged pull requests to the topic.
6. Query the realtime data

## Steps

### Using Docker images or Launcher Scripts

{% tabs %}
{% tab title="Docker" %}
### Pull docker image

Get the latest Docker image.

```text
export PINOT_VERSION=latest
export PINOT_IMAGE=apachepinot/pinot:${PINOT_VERSION}
docker pull ${PINOT_IMAGE}
```

## Long Version

### Set up the Pinot cluster

Follow the instructions in [Advanced Pinot Setup](https://docs.pinot.apache.org/getting-started/advanced-pinot-setup#start-pinot-components-using-docker) to setup the Pinot cluster with the components:

1. Zookeeper
2. Controller
3. Broker
4. Server
5. Kafka

### Create a Kafka topic

Create a Kafka topic called `pullRequestMergedEvents` for the demo.

```bash
docker exec \
  -t kafka \
  /opt/kafka/bin/kafka-topics.sh \
  --zookeeper pinot-zookeeper:2181/kafka \
  --partitions=1 --replication-factor=1 \
  --create --topic pullRequestMergedEvents
```

### Add Pinot table and schema

The schema is present at `examples/stream/githubEvents/pullRequestMergedEvents_schema.json` and is also pasted below

{% code title="pullRequestMergedEvents\_schema.json" %}
```javascript
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
{% endcode %}

The table config is present at `examples/stream/githubEvents/docker/pullRequestMergedEvents_realtime_table_config.json` and is also pasted below.

{% hint style="info" %}
**Note**  
If you're setting this up on a pre-configured cluster, set the properties `stream.kafka.zk.broker.url` and `stream.kafka.broker.list` correctly, depending on the configuration of your Kafka cluster. 
{% endhint %}

{% code title="pullRequestMergedEvents\_realtime\_table\_config.json" %}
```javascript
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
    "invertedIndexColumns": [
      "organization",
      "repo"
    ],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "simple",
      "stream.kafka.topic.name": "pullRequestMergedEvents",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.zk.broker.url": "pinot-zookeeper:2181/kafka",
      "stream.kafka.broker.list": "kafka:9092",
      "realtime.segment.flush.threshold.time": "12h",
      "realtime.segment.flush.threshold.rows": "100000",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}
```
{% endcode %}

Add the table and schema using the following command

```bash
$ docker run \
    --network=pinot-demo \
    --name pinot-streaming-table-creation \
    ${PINOT_IMAGE} AddTable \
    -schemaFile examples/stream/githubEvents/pullRequestMergedEvents_schema.json \
    -tableConfigFile examples/stream/githubEvents/docker/pullRequestMergedEvents_realtime_table_config.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
Executing command: AddTable -tableConfigFile examples/stream/githubEvents/docker/pullRequestMergedEvents_realtime_table_config.json -schemaFile examples/stream/githubEvents/pullRequestMergedEvents_schema.json -controllerHost pinot-controller -controllerPort 9000 -exec
Sending request: http://pinot-controller:9000/schemas to controller: 20c241022a96, version: Unknown
{"status":"Table pullRequestMergedEvents_REALTIME succesfully added"}
```

### Publish events

Start streaming GitHub events into the Kafka topic

{% hint style="info" %}
**Prerequisites**

Generate a [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) on GitHub.
{% endhint %}

```bash
$ docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-github-events-into-kafka \
    -d ${PINOT_IMAGE} StreamGitHubEvents \
    -schemaFile examples/stream/githubEvents/pullRequestMergedEvents_schema.json \
    -topic pullRequestMergedEvents \
    -personalAccessToken <your_github_personal_access_token> \
    -kafkaBrokerList kafka:9092
```

## Short Version

For a single command to setup all the above steps, use the following command. Make sure to stop any previous running Pinot services.

```bash
$ docker run --rm -ti \
    --network=pinot-demo \
    --name pinot-github-events-quick-start \
     ${PINOT_IMAGE} GitHubEventsQuickStart \
    -personalAccessToken <your_github_personal_access_token> 
```
{% endtab %}

{% tab title="Launcher scripts" %}
### Get Pinot

Follow instructions in [Build from source](https://docs.pinot.apache.org/getting-started/running-pinot-locally#build-from-source-or-download-the-distribution) to get the latest Pinot code

## Long Version

### Set up the Pinot cluster

Follow the instructions in [Advanced Pinot Setup](https://docs.pinot.apache.org/getting-started/advanced-pinot-setup#start-pinot-components-via-launcher-scripts) to setup the Pinot cluster with the components:

1. Zookeeper
2. Controller
3. Broker
4. Server
5. Kafka

### Create a Kafka topic

Download [Apache Kafka](https://kafka.apache.org/downloads) release. 

Create a Kafka topic called `pullRequestMergedEvents` for the demo.

```
$ bin/kafka-topics.sh \
  --create \
  --bootstrap-server localhost:19092 \
  --replication-factor 1 \
  --partitions 1 \
  --topic pullRequestMergedEvents
```

### Add Pinot table and schema

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
**Note**

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
    "invertedIndexColumns": [
      "organization",
      "repo"
    ],
    "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.consumer.type": "simple",
      "stream.kafka.topic.name": "pullRequestMergedEvents",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.zk.broker.url": "localhost:2191/kafka",
      "stream.kafka.broker.list": "localhost:19092",
      "realtime.segment.flush.threshold.time": "12h",
      "realtime.segment.flush.threshold.rows": "100000",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest"
    }
  },
  "metadata": {
    "customConfigs": {}
  }
}


```

Add the table and schema using the command

```
$ bin/pinot-admin.sh AddTable \
  -tableConfigFile $PATH_TO_CONFIGS/examples/stream/githubEvents/pullRequestMergedEvents_realtime_table_config.json \
  -schemaFile $PATH_TO_CONFIGS/examples/stream/githubEvents/pullRequestMergedEvents_schema.json \
  -exec
```

### Publish events

Start streaming GitHub events into the Kafka topic

{% hint style="info" %}
**Prerequisites**

Generate a [personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) on GitHub.
{% endhint %}

```text
$ bin/pinot-admin.sh StreamGitHubEvents \
  -topic pullRequestMergedEvents \
  -personalAccessToken <your_github_personal_access_token> \
  -kafkaBrokerList localhost:19092 \
  -schemaFile $PATH_TO_CONFIGS/examples/stream/githubEvents/pullRequestMergedEvents_schema.json
```

## Short Version

For a single command to setup all the above steps

```bash
$ bin/pinot-admin.sh GitHubEventsQuickStart \
  -personalAccessToken <your_github_personal_access_token>
```
{% endtab %}
{% endtabs %}

### Kubernetes cluster

If you already have a Kubernetes cluster with Pinot and Kafka \(see [Running Pinot in Kubernetes](../basics/getting-started/kubernetes-quickstart.md)\), first create the topic and then setup the table and streaming using

```text
$ cd kubernetes/helm
$ kubectl apply -f pinot-github-realtime-events.yml
```

## Query

Head over to the [Query Console](http://localhost:9000/query) to checkout the data!

![](../.gitbook/assets/screen-shot-2020-03-26-at-6.27.43-pm.png)

### Visualizing on SuperSet

You can use SuperSet to visualize this data. Some of the interesting insights we captures were

#### Most Active organizations during the lockdown

![](../.gitbook/assets/screen-shot-2020-04-08-at-9.28.57-am.png)

Repositories by number of commits in the Apache organization

![](../.gitbook/assets/screen-shot-2020-04-08-at-9.29.12-am.png)

To integrate with SuperSet you can check out the [SuperSet Integrations](../integrations/superset.md) page.







