# Data Ingestion Overview

## Ingesting Offline data

Segments for offline tables are constructed outside of Pinot, typically in Hadoop via map-reduce jobs and ingested into Pinot via REST API provided by the Controller. Pinot provides libraries to create Pinot segments out of input files in AVRO, JSON or CSV formats in a hadoop job, and push the constructed segments to the controllers via REST APIs.

When an Offline segment is ingested, the controller looks up the table’s configuration and assigns the segment to the servers that host the table. It may assign multiple servers for each segment depending on the number of replicas configured for that table.

Pinot supports different segment assignment strategies that are optimized for various use cases.

Once segments are assigned, Pinot servers get notified via Helix to “host” the segment. The segments are downloaded from the remote segment store to the local storage, untarred, and memory-mapped.

Once the server has loaded (memory-mapped) the segment, Helix notifies brokers of the availability of these segments. The brokers start to include the new segments for queries. Brokers support different routing strategies depending on the type of table, the segment assignment strategy, and the use case.

Data in offline segments are immutable (Rows cannot be added, deleted, or modified). However, segments may be replaced with modified data.

Starting from `release-0.11.0`, Pinot supports uploading offline segments to real-time tables. This is useful when user wants to bootstrap a real-time table with some initial data, or add some offline data to a real-time table without changing the data stream. Note that this is different from the [hybrid table](../../basics/components/table/#hybrid-table) setup, and no time boundary is maintained between the offline segments and the real-time segments.

## Ingesting Real-time Data

Segments for real-time tables are constructed by Pinot servers with rows ingested from data streams such as Kafka. Rows ingested from streams are made available for query processing as soon as they are ingested, thus enabling applications such as those that need real-time charts on analytics.

In large scale installations, data in streams is typically split across multiple stream partitions. The underlying stream may provide consumer implementations that allow applications to consume data from any subset of partitions, including all partitions (or, just from one partition).

A pinot table can be configured to consume from streams in one of two modes:

> * `LowLevel`: This is the preferred mode of consumption. Pinot creates independent partition-level consumers for each partition. Depending on the the configured number of replicas, multiple consumers may be created for each partition, taking care that no two replicas exist on the same server host. Therefore you need to provision _at least_ as many hosts as the number of replicas configured.
> * `HighLevel`: Pinot creates _one_ stream-level consumer that consumes from all partitions. Each message consumed could be from any of the partitions of the stream. Depending on the configured number of replicas, multiple stream-level consumers are created, taking care that no two replicas exist on the same server host. Therefore you need to provision exactly as many hosts as the number of replicas configured.

Of course, the underlying stream should support either mode of consumption in order for a Pinot table to use that mode. Kafka has support for both of these modes. See [Stream ingestion](../../basics/data-import/pinot-stream-ingestion/) for more information on the support of other data streams in Pinot.

In either mode, Pinot servers store the ingested rows in volatile memory until either one of the following conditions are met:

> 1. A certain number of rows are consumed
> 2. The consumption has gone on for a certain length of time

(See [StreamConfigs Section](../../configuration-reference/table.md#realtime-table-config) on how to set these values, or have pinot compute them for you)

Upon reaching either one of these limits, the servers do the following:

> * Pause consumption
> * Persist the rows consumed so far into non-volatile storage
> * Continue consuming new rows into volatile memory again.

The persisted rows form what we call a _completed_ segment (as opposed to a _consuming_ segment that resides in volatile memory).

In `LowLevel` mode, the completed segments are persisted the into local non-volatile store of pinot server _as well as_ the segment store of the pinot cluster (See [Pinot Architecture Overview](../../basics/architecture.md)). This allows for easy and automated mechanisms for replacing pinot servers, or expanding capacity, etc. Pinot has [special mechanisms](https://cwiki.apache.org/confluence/display/PINOT/Consuming+and+Indexing+rows+in+Realtime#ConsumingandIndexingrowsinRealtime-Segmentcompletionprotocol) that ensure that the completed segment is equivalent across all replicas.

During segment completion, one winner is chosen by the controller from all the replicas as the `committer server`. The `committer server` builds the segment and uploads it to the controller. All the other `non-committer servers` follow one of these two paths:

1. If the in-memory segment is equivalent to the committed segment, the `non-committer` server also builds the segment locally and replaces the in-memory segment
2. If the in-memory segment is non equivalent to the committed segment, the `non-committer` server downloads the segment from the controller.

For more details on this protocol, refer to [this doc](https://cwiki.apache.org/confluence/display/PINOT/Consuming+and+Indexing+rows+in+Realtime#ConsumingandIndexingrowsinRealtime-Segmentcompletionprotocol).

In `HighLevel` mode, the servers persist the consumed rows into local store (and **not** the segment store). Since consumption of rows can be from any partition, it is not possible to guarantee equivalence of segments across replicas.

See [Consuming and Indexing rows in Realtime](https://cwiki.apache.org/confluence/display/PINOT/Consuming+and+Indexing+rows+in+Realtime) for details.
