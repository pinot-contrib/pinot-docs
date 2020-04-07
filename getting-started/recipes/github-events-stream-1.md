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

## Steps

{% tabs %}
{% tab title="Docker" %}
Setting up the Pinot cluster

Follow the instructions from the Docker tab in Advanced Pinot Setup
{% endtab %}

{% tab title="Launcher scripts" %}

{% endtab %}
{% endtabs %}

