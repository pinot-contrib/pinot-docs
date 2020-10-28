---
description: 'Upsert support in Apache Pinot.'
---

# Upsert Support

Pinot provides native support of upsert during the real-time table's ingestion. There are scenarios that the records need modifications such as correcting a ride fare and updating a delivery status. 

To enable upsert on a Pinot table, there are a couple of configurations to make on the Pinot table as well as on the input stream.

## Define the primary key in the schema

To update a record, a primary key is needed to uniquely identify the record. To define a primary key, add the field `primaryKeyColumns` to the schema definition. For example, the schema definition of `UpsertMeetupRSVP` in the quick start example has this definition.

{% code title="upsert_meetupRsvp_schema.json" %}
```javascript
{
	"primaryKeyColumns": ["event_id"]
}
```
{% endcode %}

Note this field expects a list of columns, as the primary key can be composite.

## Partition the input stream by the primary key

A key requirement for the upsert Pinot table is to partition the input stream by the primary key. For Kafka messages, this means the producer shall set the key in the [`send`](https://kafka.apache.org/20/javadoc/index.html?org/apache/kafka/clients/producer/KafkaProducer.html) API. If the original stream is not partitioned, then a streaming processing job (e.g. Flink) is needd to shuffle and repartition into an output stream for Pinot's ingestion.

## Enable upsert in the table configurations

There are a few configurations needed in the table configurations to enable upsert.

### Upsert mode

For append-only tables, the upsert mode defaults to `NONE`. To enable the upsert, set the `mode` to `FULL` for the full update. In future, Pinot plans to add the partial update support. For example:

{% code title="upsert mode" %}
```javascript
{
	"upsertConfig": {
    "mode": "FULL"
  }
}
```

### Use replicaGroup for routing



{% endcode %}

{% code title="upsert_meetupRsvp_realtime_table_config.json" %}
```javascript
{
}
```
{% endcode %}
