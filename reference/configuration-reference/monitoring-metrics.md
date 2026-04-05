---
description: Monitoring-metric configuration reference.
---

# Monitoring Metrics Reference

This page keeps the monitoring overview and the metric inventory together so the reference stays on a single page.

Pinot provides metrics out of the box so that you can monitor every aspect of performance and robustness of the Pinot cluster. Most of the metrics are available either at table level or instance level. There are three main categories of metrics:

* **Gauge** - A single value at any point in time
* **Meter** - Rates of the metric per unit of time
* **Timer** - Record durations and can be used to fetch average duration per unit of time, percentile values, minimum or maximum values, etc.

### Pinot Server

| Metric Name | Description | Metric type |
| --- | --- | --- |
| LLC-PARTITION-CONSUMING | This gives a binary value based on whether low-level consumption is healthy (1) or unhealthy (0). It's important to ensure at least a single replica of each partition is consuming. |  |
| HIGHEST-STREAM-OFFSET-CONSUMED | The highest offset which has been consumed so far |  |
| DOCUMENT_COUNT | total number of records in table |  |
| SEGMENT_COUNT | total number of segments in table |  |
| UPSERT_PRIMARY_KEYS_COUNT | total unique primary keys in table |  |
| LAST_REALTIME_SEGMENT_CREATION_DURATION_SECONDS | time in seconds it took for latest real-time segment to get created |  |
| LAST_REALTIME_SEGMENT_CREATION_WAIT_TIME_SECONDS | time in seconds it took for segment creation to start (generally due to waiting for a lock to get acquired) |  |
| LAST_REALTIME_SEGMENT_INITIAL_CONSUMPTION_DURATION_SECONDS | time in seconds spent consuming records for latest segment |  |
| LAST_REALTIME_SEGMENT_CATCHUP_DURATION_SECONDS | time in seconds spent on catching up to the latest offset in metadata. This can happen when multiple servers are consuming from same partition. |  |
| LAST_REALTIME_SEGMENT_COMPLETION_DURATION_SECONDS | time in seconds between when we stopped consuming records and when the segment gets committed |  |
| REALTIME_OFFHEAP_MEMORY_USED | off heap memory in bytes current used by real-time segments |  |
| REALTIME_SEGMENT_NUM_PARTITIONS | Number of partitions for a table |  |
| LLC_SIMULTANEOUS_SEGMENT_BUILDS | Number of segments being built currently |  |
| REALTIME_INGESTION_DELAY_MS | Per partition metric that measures the delay in milliseconds from the time an event was produced to the stream that feeds Pinot until the event was consumed by Pinot. Partitions that are not actively consuming due to lack of events will report 0 delay. Partitions that are stuck or falling behind will report their last measured delay aged by the time since the sample was taken: this enables the user to monitor partitions that have events queued but where Pinot is falling behind in consumption. This metric assumes event timestamps is UTC time zone, if timestamps are using other timezones, the delay shown will be offset. |  |
| ROWS_WITH_ERRORS | number of rows that either didn't get transformed or didn't get indexed. |  |
| REALTIME_ROWS_CONSUMED | total number of records consumed from input |  |
| INVALID_REALTIME_ROWS_DROPPED | number of records that were filtered based on FilterConfig specified in table config |  |
| REALTIME_CONSUMPTION_EXCEPTIONS | number of rows that were not consumed because of some exception. It doesn't track exceptions during transformation and indexing. |  |
| RELOAD_FAILURES | Number of failures occurred while reloading segments |  |
| REFRESH_FAILURES | Number of failures occurred while refreshing segments |  |
| UNTAR_FAILURES | Number of failures occurred while uncompressing segments |  |
| SEGMENT_DOWNLOAD_FAILURES | Number of failures occurred while downloading segments from deep store to local |  |
| DELETED_SEGMENT_COUNT | Number of segments deleted either because of retention policies, explicit delete request etc. |  |
| QUERIES | Number of queries executed |  |
| QUERY_EXECUTION_EXCEPTIONS | Number of exceptions encountered during query execution |  |
| NUM-MISSING-SEGMENTS | Number of missing segments that the broker queried for (expected to be on the server) but the server didn't have. This can be due to retention or stale routing table |  |
| NO_TABLE_ACCESS | number of query requests for which table access was denied either due to table not being present or access control restrictions. |  |
| HELIX_ZOOKEEPER_RECONNECTS | Number of times Server instance re-connected to zookeeper. |  |
| NETTY_CONNECTION_BYTES_RECEIVED | total bytes received by the server |  |
| NETTY_CONNECTION_BYTES_SENT | total bytes sent by the server |  |
| NETTY_CONNECTION_RESPONSES_SENT | total responses sent by the server |  |
| FRESHNESS_LAG_MS | time period between when the data was last updated in the table and the current time |  |
| NETTY_CONNECTION_SEND_RESPONSE_LATENCY | time spent in sending response to brokers after the results are available |  |
| NETTY_TOTAL_MAX_DIRECT_MEMORY | Maximum direct memory available to the server's Netty query service |  |
| NETTY_TOTAL_USED_DIRECT_MEMORY | Current direct memory allocated by the server's Netty query service |  |
| GRPC_TOTAL_MAX_DIRECT_MEMORY | Maximum direct memory available to the shaded Netty runtime used by the server gRPC query service and MSE mailbox traffic |  |
| GRPC_TOTAL_USED_DIRECT_MEMORY | Current direct memory allocated by the shaded Netty runtime used by the server gRPC query service and MSE mailbox traffic |  |
| EXECUTION_THREAD_CPU_TIME_NS | time spent by all threads processing query and results (doesn't includes time spent in system activities) |  |
| SYSTEM_ACTIVITIES_CPU_TIME_NS | time spent in nanoseconds processing query on the servers (only counts system acitivities such as GC, OS paging etc.) |  |
| RESPONSE_SER_CPU_TIME_NS | time spent in nanoseconds serializing query response on servers |  |
| TOTAL_CPU_TIME_NS | total time spent in nanoseconds processing query on the servers |  |
| END_TO_END_REALTIME_INGESTION_DELAY_MS | When supported by the underlying stream, this metric provides the ingestion delay in milliseconds from the time an event was ingested by the first stream in your ingestion pipeline to the time the event was ingested by Pinot. The metric is not emitted when the underlying stream does not support this feature. The metric relies on this metric being in UTC time zone. If your time stamp is in another time zone, your metric will be offset accordingly. |  |

#### Tracking time spent in various phases of Query execution in milliseconds

| Metric Name | Description |  |
| --- | --- | --- |
| REQUEST_DESERIALIZATION | Time spent in deserializing query request |  |
| SEGMENT_PRUNING | Time spent in Segment Pruning |  |
| BUILD_QUERY_PLAN | Time spent in building query plan |  |
| QUERY_PLAN_EXECUTION | Time spent in executing query plan |  |
| QUERY_PROCESSING | Total Time spent in processing the query request from receiving the parsed query to getting data. Doesn't include ser-de time. |  |
| SCHEDULER_WAIT | Time spent in the scheduler queue waiting for the query to be executed |  |
| RESPONSE_SERIALIZATION | Time spent in serializing query response |  |
| TOTAL_QUERY_TIME | Total time to take from receiving the query to returning the responde. |  |

### Pinot Broker

| Metric Name | Description | Metric Type |
| --- | --- | --- |
| UNHEALTHY_SERVERS | Number of unhealthy servers detected |  |
| QUERY_QUOTA_CAPACITY_UTILIZATION_RATE | percentage of configured rate limit being used on each broker |  |
| MAX_BURST_QPS |  |  |
| QUERY_RATE_LIMIT_DISABLED | 1 if rate limit is enabled on broker, 0 otherwise |  |
| REQUEST_SIZE | Query String length on each broker |  |
| RESIZE_TIME_MS | time spent in resizing results for the output. either because of LIMIT or maximum allowed group by keys or any other criteria |  |
| QUERIES | The rate which an individual broker is receiving queries. Units are in QPS |  |
| REQUEST_COMPILATION_EXCEPTIONS | Number of queries which failed during compilation |  |
| RESOURCE_MISSING_EXCEPTIONS | Number of queries for which table doesn't exists |  |
| QUERY_VALIDATION_EXCEPTIONS | Number of invalid queries |  |
| UNKNOWN_COLUMN_EXCEPTIONS | Number of queries with unknown columns |  |
| NO_SERVER_FOUND_EXCEPTIONS | Number of queries for which no server was found to contain its data |  |
| REQUEST_TIMEOUT_BEFORE_SCATTERED_EXCEPTIONS | Number of times query timed out before even being sent to the servers |  |
| REQUEST_CHANNEL_LOCK_TIMEOUT_EXCEPTIONS | number of times query failes while trying to acquire lock to server connections |  |
| REQUEST_SEND_EXCEPTIONS | Number of queries failed while sending to server |  |
| RESPONSE_FETCH_EXCEPTIONS | Number of queries failed while handling response from servers |  |
| DATA_TABLE_DESERIALIZATION_EXCEPTIONS | Number of queries failed while deserializing response data from servers |  |
| RESPONSE_MERGE_EXCEPTIONS | Number of queries that failed while merging responses from multiple servers. This can be due to schema inconsitency or any other issues |  |
| BROKER_RESPONSES_WITH_PROCESSING_EXCEPTIONS | Number of queries where atleast one exception occured |  |
| BROKER_RESPONSES_WITH_PARTIAL_SERVERS_RESPONDED | Number of queries with incomplete results due to missing responses from servers |  |
| BROKER_RESPONSES_WITH_NUM_GROUPS_LIMIT_REACHED | Number of queries where total number of groups exceeded configured limit (default limit - 100K) |  |
| DOCUMENTS_SCANNED | Total number of documents read from segments in each query |  |
| ENTRIES_SCANNED_IN_FILTER |  |  |
| ENTRIES_SCANNED_POST_FILTER |  |  |
| NUM_RESIZES | Number of result resizes for queries |  |
| REQUEST_DROPPED_DUE_TO_ACCESS_ERROR | Number of queries dropped due to invalid access permissions on table |  |
| GROUP_BY_SIZE | Number of rows in group by queries |  |
| TOTAL_SERVER_RESPONSE_SIZE | Total number of bytes received from servers for queries |  |
| QUERY_QUOTA_EXCEEDED | Number of queries failed due to query rate limit being breached |  |
| NO_SERVING_HOST_FOR_SEGMENT | Number of segments per query for which no servers are available |  |
| SERVER_MISSING_FOR_ROUTING | Number of servers that could not be added to routing table for query |  |
| NETTY_CONNECTION_REQUESTS_SENT | total number of requests sent to servers |  |
| NETTY_CONNECTION_BYTES_SENT | total bytes sent to servers |  |
| NETTY_CONNECTION_BYTES_RECEIVED | total bytes received from servers |  |
| PROACTIVE_CLUSTER_CHANGE_CHECK | Number of requests raised to zookeeper to check the cluster state such as IDEAL STATES, EXTERNAL VIEW etc. |  |
| HELIX_ZOOKEEPER_RECONNECTS | Number of times broker instance re-connected to zookeeper. |  |
| CLUSTER_CHANGE_QUEUE_TIME | Time spent in milliseconds in queue for cluster change requests |  |
| FRESHNESS_LAG_MS | time period between when the data was last updated in the table and the current time |  |
| NETTY_CONNECTION_SEND_REQUEST_LATENCY | latency of sending the request from broker to server |  |
| OFFLINE_THREAD_CPU_TIME_NS | aggregated thread cpu time in nanoseconds for query processing from offline servers |  |
| REALTIME_THREAD_CPU_TIME_NS | aggregated thread cpu time in nanoseconds for query processing from real-time servers |  |
| OFFLINE_SYSTEM_ACTIVITIES_CPU_TIME_NS | aggregated system activities cpu time in nanoseconds for query processing from offline servers (e.g. GC, OS paging etc.) |  |
| REALTIME_SYSTEM_ACTIVITIES_CPU_TIME_NS | aggregated system activities cpu time in nanoseconds for query processing from real-time servers (e.g. GC, OS paging etc.) |  |
| OFFLINE_RESPONSE_SER_CPU_TIME_NS | aggregated response serialization cpu time in nanoseconds for query processing from offline servers |  |
| REALTIME_RESPONSE_SER_CPU_TIME_NS | aggregated response serialization cpu time in nanoseconds for query processing from real-time servers |  |
| OFFLINE_TOTAL_CPU_TIME_NS | aggregated total cpu time(thread + system activities + response serialization) in nanoseconds for query processing from offline servers |  |
| REALTIME_TOTAL_CPU_TIME_NS | time(thread + system activities + response serialization) in nanoseconds for query processing from real-time servers |  |
| GRPC_TOTAL_MAX_DIRECT_MEMORY | Maximum direct memory available to the shaded Netty runtime used by broker gRPC services and MSE mailbox traffic |  |
| GRPC_TOTAL_USED_DIRECT_MEMORY | Current direct memory allocated by the shaded Netty runtime used by broker gRPC services and MSE mailbox traffic |  |

#### Tracking time spent in various phases of Query execution in milliseconds

| Metric Name | Description | Metric Type |
| --- | --- | --- |
| REQUEST_COMPILATION | Time spent in compiling SQL query |  |
| QUERY_EXECUTION | Total Time spent in query executiong |  |
| QUERY_ROUTING | Time spent in creating a routing table for segments |  |
| SCATTER_GATHER | Time spent in sending and collecting responses from servers. |  |
| REDUCE | Time spent in combining query results from multiple servers |  |
| AUTHORIZATION | Time spent checking table access after query compilation |  |

### Pinot Controller

| Metric Name | Description | Metric Type |
| --- | --- | --- |
| PERCENT_SEGMENTS_AVAILABLE | Percentage of complete online replicas in external view as compared to replicas in ideal state |  |
| NUMBER_OF_REPLICAS | Total number of replicas available for table |  |
| SEGMENTS_IN_ERROR_STATE | Number of segments in an `ERROR` state for a given table. |  |
| TABLE_STORAGE_QUOTA_UTILIZATION | Shows how much of the table's storage quota is currently being used, metric will a percentage of a the entire quota. |  |
| LAST_PUSH_TIME_DELAY_HOURS | The time in hours since the last time an offline segment has been pushed to the controller. |  |
| HEALTHCHECK_OK_CALLS | Number of health check requests for which controller was healthy |  |
| HEALTHCHECK_BAD_CALLS | Number of health check requests for which controller was unhealthy |  |
| CONTROLLER_INSTANCE_POST_ERROR | Errors occurred while updating state for an instance (server and broker) |  |
| CONTROLLER_SEGMENT_UPLOAD_ERROR | Errors occurred while sending uploading segment request |  |
| CONTROLLER_SCHEMA_UPLOAD_ERROR | Errors occurred while uploading schema |  |
| CONTROLLER_TABLE_SCHEMA_UPDATE_ERROR | Errors occurred while updating schema |  |
| CONTROLLER_TABLE_ADD_ERROR | Errors occurred while adding table config |  |
| CONTROLLER_TABLE_UPDATE_ERROR | Errors occurred while updating table config |  |
| CONTROLLER_TABLE_TENANT_UPDATE_ERROR | Errors occurred while updating a Tenant |  |
| CONTROLLER_TABLE_TENANT_CREATE_ERROR | Errors occurred while creating a Tenant |  |
| CONTROLLER_TABLE_TENANT_DELETE_ERROR | Errors while deleting a Tenant |  |
| CONTROLLER_REALTIME_TABLE_SEGMENT_ASSIGNMENT_ERROR | Errors occurred while assigning a real-time segment to a server instance |  |
| CONTROLLER_LEADERSHIP_CHANGE_WITHOUT_CALLBACK | Number of times a controller loses/gains leadership without a callback from Helix |  |
| CONTROLLER_PERIODIC_TASK_RUN | Number of Periodic tasks running currently |  |
| CONTROLLER_PERIODIC_TASK_ERROR | Number of Periodic tasks that failed due to error |  |
| NUMBER_TIMES_SCHEDULE_TASKS_CALLED | Minion tasks schedule request sent to controller |  |
| NUMBER_TASKS_SUBMITTED | Number of minion tasks submitted to the controller. |  |
| NUMBER_SEGMENT_UPLOAD_TIMEOUT_EXCEEDED | Number of segments uploads failed due to timeout. Segments are re-uploaded in this case by controller itself. |  |
| CRON_SCHEDULER_JOB_TRIGGERED | Number of minion tasks triggered that use cron |  |
| NUMBER_ADHOC_TASKS_SUBMITTED | Number of minion ad hoc tasks submitted |  |
| LLC_STATE_MACHINE_ABORTS | Number of times a real-time segment commit operation was aborted |  |
| LLC_ZOOKEEPER_FETCH_FAILURES | Number of Zookeeper metadata fetch requests failed |  |
| LLC_ZOOKEEPER_UPDATE_FAILURES | Number of Zookeeper metadata update requests failed |  |
| LLC_STREAM_DATA_LOSS | Indicates data loss for table either due to offsets available to consume from topic larger than the last stored offset in pinot or segment lost in CONSUMING state |  |
| HELIX_ZOOKEEPER_RECONNECTS | Number of times broker instance re-connected to zookeeper. |  |
| CRON_SCHEDULER_JOB_EXECUTION_TIME_MS | Time spent in scheduling cron jobs |  |
| IDEAL_STATE_UPDATE_FAILURE | Indicates failed to update ideal state of table |  |
| IDEAL_STATE_UPDATE_RETRY | Number of retries update ideal state of table |  |
| IDEAL_STATE_UPDATE_TIME_MS | Time spent in updating ideal state for table |  |
| DEEP_STORE_READ_BYTES_IN_PROGRESS | Bytes being read from deep store |  |
| DEEP_STORE_READ_OPS_IN_PROGRESS | Active deep store read count |  |
| DEEP_STORE_WRITE_BYTES_IN_PROGRESS | Bytes being written to deep store |  |
| DEEP_STORE_WRITE_OPS_IN_PROGRESS | Active deep store write count |  |
| DEEP_STORE_READ_BYTES_COMPLETED | Total Bytes read from deep store |  |
| DEEP_STORE_WRITE_BYTES_COMPLETED | Total Bytes written to deep store |  |
| DEEP_STORE_SEGMENT_READ_TIME_MS | Time taken to read the segment from deep store |  |
| DEEP_STORE_SEGMENT_WRITE_TIME_MS | Time taken to write the segment to deep store |  |

### Pinot Minion

| Metric Name | Description | Metric Type |
| --- | --- | --- |
| NUMBER_OF_TASKS | Number of tasks currently running |  |
| NUMBER_TASKS_EXECUTED | Number of tasks triggered in Minion |  |
| NUMBER_TASKS_COMPLETED | Number of tasks completed successfully |  |
| NUMBER_TASKS_CANCELLED | Number of tasks that were cancelled |  |
| NUMBER_TASKS_FAILED | Number of tasks that failed |  |
| NUMBER_TASKS_FATAL_FAILED | Number of tasks that failed with unretryable exceptions |  |
| TASK_QUEUEING | Time spent by tasks in queue |  |
| TASK_EXECUTION | Time spent by tasks in execution |  |
