# Realtime

## Tuning Realtime Performance

See the section on [Ingesting Realtime Data](../../../basics/data-import/pinot-stream-ingestion/) before reading this section.

Pinot servers ingest rows into a consuming segment that resides in volatile memory. Therefore, pinot servers hosting consuming segments tend to be memory bound. They may also have long garbage collection cycles when the segment is completed and memory is released.

### Controlling memory allocation

You can configure pinot servers to use off-heap memory for dictionary and forward indices of consuming segments by setting the value of `pinot.server.instance.realtime.alloc.offheap` to `true`. With this configuration in place, the server allocates off-heap memory by memory-mapping files. These files are never flushed to stable storage by Pinot \(the Operating System may do so depending on demand for memory on the host\). The files are discarded when the consuming segment is turned into a completed segment.

By default the files are created under the directory where the table’s segments are stored in local disk attached to the consuming server. You can set a specific directory for consuming segments with the configuration `pinot.server.consumerDir`. Given that there is no control over flushing of pages from the memory mapped for consuming segments, you may want to set the directory to point to a memory-based file system, eliminating wasteful disk I/O.

If memory-mapping is not desirable, you can set `pinot.server.instance.realtime.alloc.offheap.direct` to `true`. In this case, pinot allocates direct [ByteBuffer](https://docs.oracle.com/javase/7/docs/api/java/nio/ByteBuffer.html) objects for consuming segments. Using direct allocation can potentially result in address space fragmentation.

Note

We still use heap memory to store inverted indices for consuming segments.

### Controlling number of rows in consuming segment

The number of rows in a consuming segment needs to be balanced. Having too many rows can result in memory pressure. On the other hand, having too few rows results in having too many small segments. Having too many segments can be detrimental to query performance, and also increase pressure on the Helix.

The recommended way to do this is to use the `realtime.segment.flush.desired.size` setting as described in [StreamConfigs Section](../../../configuration-reference/table.md#realtime-table-config). You can run the administrative tool `pinot-admin.sh RealtimeProvisioningHelper` that will help you to come up with an optimal setting for the segment size.

### Moving completed segments to different hosts

This feature is available only if the consumption type is `LowLevel`.

The structure of the consuming segments and the completed segments are very different. The memory, CPU, I/O and GC characteristics could be very different while processing queries on these segments. Therefore it may be useful to move the completed segments onto different set of hosts in some use cases.

You can host completed segments on a different set of hosts using the `tagOverrideConfig` as described in [Table Config](../../../configuration-reference/table.md). Pinot will automatically move them once the consuming segments are completed.

### Controlling segment build vs segment download on Realtime servers

This feature is available only if the consumption type is `LowLevel`.

When a realtime segment completes, a winner server is chosen as a committer amongst all replicas by the controller. That committer builds the segment and uploads to the controller. The non-committer servers are asked to catchup to the winning offset. If the non-committer servers are able to catch up, they are asked to build the segment and replace the in-memory segment. If they are unable to catchup, they are asked to download the segment from the controller.

Building a segment can cause excessive garbage and may result in GC pauses on the server. Long GC pauses can affect query processing. In order to avoid this, we have a configuration that allows you to control whether

It might become desirable to force the non-committer servers to download the segment from the controller, instead of building it again. The `completionConfig` as described in [Table Config](../../../configuration-reference/table.md) can be used to configure this.

### Fine tuning the segment commit protocol

This feature is available only if the consumption type is `LowLevel`.

Once a committer is asked to commit the segment, it builds a segment, and issues an HTTP POST to the controller, with the segment. The controller than commits the segment in Zookeeper and starts the next consuming segment.

It is possible to conifigure the servers to do a _split_ commit, in which the committer performs the following steps:

> * Build the segment
> * Start a transaction with the lead controller to commit the segment \(CommitStart phase\)
> * Post the completed segment to any of the controllers \(and the controller posts it to segment store\)
> * End the transaction with the lead controller \(CommentEnd phase\). Optionally, this step can be done _with_ the segment metadata.

This method of committing can be useful if the network bandwidth on the lead controller is limiting segment uploads.In order to accomplish this, you will need to set the following configurations:

* On the controller, set `pinot.controller.enable.split.commit` to `true` \(default is `false`\).
* On the server, set `pinot.server.enable.split.commit` to `true` \(default is `false`\).
* On the server, set `pinot.server.enable.commitend.metadata` to `true` \(default is false\).

### RealtimeProvisioningHelper

This tool can help decide the optimum segment size and number of hosts for your table. You will need one sample Pinot segment from your table before you run this command. If you have an offline segment, you can use that. Alternatively, you can provision a test version of your table with some minimum number of hosts that can consume the stream, let it create a few segments with large enough number of rows \(say, 500k  to 1M rows\), and use one of those  segments to run the command. You can drop the test version table, and re-provision it once the command outputs some parameters to set.

#### Version 0.4.0 and older

The arguments for this command are as follows \(some of these have default values, so try the -help argument first\):

* `tableConfigFile`: This is the path to the table config file
* `numPartitions`: Number of partitions in your stream
* `numHosts`: This is a list of the number of hosts for which you need to compute the actual parameters. For example,  if you are planning to deploy between 4 and 8 hosts, you may specify 4,6,8. In this case, the parameters will be computed for each configuration -- that of 4 hosts, 6 hosts, and 8 hosts. You can then decide which of these configurations to use.
* `numHours` : This is a list of maximum number of hours you want your consuming segments to be in consuming state. After these many hours the segment will move to completed state, even if other criteria \(like segment size or number of rows\) are not met yet. This value must be smaller than the retention of your stream. If you specify too small a value, then you run the risk of creating too many segments, this resulting in sub-optimal query performance. If you specify this value to be too big, then you may run the risk of having too large segments, running out of "hot" memory \(consuming segments are in read-write memory\). Specify a few different \(comma-separated\) values, and the command computes the segment size for each of these.
* `retentionHours` : Number of hours of most recent data that needs to be in memory. The realtime segments need to be in memory only until the offline segments are available for use in a hybrid table \(for a realtime only table, specify the table retention time in hours\). For example, if the offline tables are pushed daily, you can specify 72, and if it is pushed hourly, you can specify 24. 
* `maxUsableHostMemory`: This is the total memory available in each host for hosting "retentionHours" worth of segments of this table. Remember to leave some for query processing \(or other tables,  if you have them in the same hosts\)
* `sampleCompletedSegmentDir`: The path of the directory in which the sample segment is present.
* `periodSampleSegmentConsumed`: The time taken for the sample segment to be consumed. If it is an offline segment, then you will need to compute this value by dividing the number of rows in the offline segment by the average ingestion rate of any one partition in your stream \(we assume here that the partitions are more or less uniform\).

Once you run the command, it produces an out like below:

```text
Memory used per host

numHosts --> 8        |10       |12       |14       |
numHours
 4 --------> 31.94GB  |26.61GB  |21.29GB  |18.63GB  |
 6 --------> 31.81GB  |26.51GB  |21.2GB   |18.55GB  |
 8 --------> 31.68GB  |26.4GB   |21.12GB  |18.48GB  |
10 --------> 34.94GB  |29.12GB  |23.29GB  |20.38GB  |
12 --------> 31.42GB  |26.19GB  |20.95GB  |18.33GB  |

Optimal segment size

numHosts --> 8        |10       |12       |14       |
numHours
 4 --------> 144.68MB |144.68MB |144.68MB |144.68MB |
 6 --------> 217.02MB |217.02MB |217.02MB |217.02MB |
 8 --------> 289.36MB |289.36MB |289.36MB |289.36MB |
10 --------> 361.7MB  |361.7MB  |361.7MB  |361.7MB  |
12 --------> 434.04MB |434.04MB |434.04MB |434.04MB |

Consuming memory

numHosts --> 8        |10       |12       |14       |
numHours
 4 --------> 3.11GB   |2.59GB   |2.07GB   |1.82GB   |
 6 --------> 3.83GB   |3.19GB   |2.55GB   |2.24GB   |
 8 --------> 4.55GB   |3.79GB   |3.03GB   |2.66GB   |
10 --------> 5.27GB   |4.39GB   |3.51GB   |3.08GB   |
12 --------> 5.99GB   |4.99GB   |3.99GB   |3.5GB    |
```

Now, depending on how much memory you want to allocate for this table, and how many hosts you want to provision, you can select the number of hours to consume, and the optimal segment size, and enter that into the streamsConfig section of the table configuration.

#### Version 0.5.0 and later

This command has been improved to display the number of pages mapped, as well as take in the push frequency as an argument if the realtime table being provisioned is a part of a hybrid table. The arguments are as follows:

* `tableConfigFile`: This is the path to the table config file
* `numPartitions`: Number of partitions in your stream
* `numHosts`: This is a list of the number of hosts for which you need to compute the actual parameters. For example,  if you are planning to deploy between 4 and 8 hosts, you may specify 4,6,8. In this case, the parameters will be computed for each configuration -- that of 4 hosts, 6 hosts, and 8 hosts. You can then decide which of these configurations to use.
* `numHours` : This is a list of maximum number of hours you want your consuming segments to be in consuming state. After these many hours the segment will move to completed state, even if other criteria \(like segment size or number of rows\) are not met yet. This value must be smaller than the retention of your stream. If you specify too small a value, then you run the risk of creating too many segments, this resulting in sub-optimal query performance. If you specify this value to be too big, then you may run the risk of having too large segments, running out of "hot" memory \(consuming segments are in read-write memory\). Specify a few different \(comma-separated\) values, and the command computes the segment size for each of these.
* `sampleCompletedSegmentDir`: The path of the directory in which the sample segment is present.
* `pushFrequency` : This is optional. If this is a hybrid table, then enter the frequency with which offline segments are pushed \(one of "hourly", "daily", "weekly" or "monthly"\). This argument is ignored if `retentionHours` is specified.
* `maxUsableHostMemory`: This is the total memory available in each host for hosting `retentionHours` worth of data \(_i.e._ "hot" data\) of this table. Remember to leave some for query processing \(or other tables,  if you have them in the same hosts\). If your latency needs to be very low, this value should not exceed the physical memory available to store pinot segments of this table, on each host in your cluster. On the other hand, if you are trying to lower cost and can take higher latencies, consider specifying a bigger value here. Pinot will leave the rest to the Operating System to page memory back in as necessary.
* `retentionHours` : This argument should specify how many hours of data will typically be queried on your table. It is assumed that these are the most recent hours.   If `pushFrequency` is specified, then it is assumed that the older data will be served by the offline table, and the value is derived automatically. For example, if `pushFrequency` is `daily`, this value defaults to `72`. If `hourly`, then `24`. If `weekly`, then `8d`. If `monthly`, then `32d`. If neither `pushFrequency` nor `retentionHours` is specified, then this value is assumed to be the retention time of the realtime table \(e.g. if the table is retained for 6 months, then it is assumed that most queries will retrieve all six months of data\). As an example, if you have a realtime only table with a 21 day retention, and expect that 90% of your queries will be for the most recent 3 days, you can specify a `retentionHours` value of 72. This will help you configure a system that performs much better for most of your queries while taking a performance hit for those that occasionally query older data. 
* `ingestionRate` : Specify the average number of rows ingested per second per partition of your stream.

One you run the command, it produces an output as below:

```text
============================================================
RealtimeProvisioningHelperCommand -tableConfigFile /Users/ssubrama/tmp/samza/realtimeTableConfig.json -numPartitions 16 -pushFrequency null -numHosts 8,6,10 -numHours 6,12,18,24 -sampleCompletedSegmentDir /Users/ssubrama/tmp/samza/TestSamzaAnalyticsFeatures_1593411480000_1593500340000_0/ -ingestionRate 100 -maxUsableHostMemory 10G -retentionHours 72

Note:

* Table retention and push frequency ignored for determining retentionHours
* See https://docs.pinot.apache.org/operators/operating-pinot/tuning/realtime

Memory used per host (Active/Mapped)

numHosts --> 6               |8               |10              |
numHours
 6 --------> 5.05G/19.49G    |3.37G/12.99G    |3.37G/12.99G    |
12 --------> 5.89G/20.33G    |3.93G/13.55G    |3.93G/13.55G    |
18 --------> 6.73G/21.49G    |4.48G/14.33G    |4.48G/14.33G    |
24 --------> 7.56G/22G       |5.04G/14.66G    |5.04G/14.66G    |

Optimal segment size

numHosts --> 6               |8               |10              |
numHours
 6 --------> 111.98M         |111.98M         |111.98M         |
12 --------> 223.96M         |223.96M         |223.96M         |
18 --------> 335.94M         |335.94M         |335.94M         |
24 --------> 447.92M         |447.92M         |447.92M         |

Consuming memory

numHosts --> 6               |8               |10              |
numHours
 6 --------> 1.45G           |987.17M         |987.17M         |
12 --------> 2.61G           |1.74G           |1.74G           |
18 --------> 3.77G           |2.52G           |2.52G           |
24 --------> 4.94G           |3.29G           |3.29G           |

Number of segments queried per host

numHosts --> 6               |8               |10              |
numHours
 6 --------> 12              |12              |12              |
12 --------> 6               |6               |6               |
18 --------> 4               |4               |4               |
24 --------> 3               |3               |3               |
```

The idea here is to choose an optimal segment size so that :

1. The number of segments searched for your queries are minimized
2. The segment size is neither too large not too small \(where "large" and "small" are as per the range for your table\).
3. Overall memory is optimized for your table, considering the other tables in the host, the query traffic, etc.

You can pick the appropriate value for segment size and number of hours in the table config, and set the number of rows to zero. Note that you don't have to pick values exactly as given in each of these combinations \(they are calculated guesses anyway\). Feel free to choose some values in between or out of range as you feel fit, and adjust them after your table is in production \(no restarts required, things will slowly adjust themselves to the new configuration\). The example given below chooses from the output.

**Case 1: Optimize for performance, high QPS**

From the above output you may decide that 6 hours is an optimal consumption time given the number of active segments looked at for a query, and you can afford about 4G of active memory per host. You can choose either 8 or 10 hosts, you choose 10. In this case, the optimal segment size will be 111.98M. You can then enter your realtime table config as below:

```javascript
"realtime.segment.flush.threshold.size": "0"
"realtime.segment.flush.threshold.time": "6h"
"realtime.segment.flush.desired.size": "112M"
```

**Case 2: Optimize for cost, low QPS**

You may decide from the output that you want to make do with 6 hosts. You have only 2G of memory per host for active segments but you are willing to map 8G of active memory on that, with plenty of paging for each query. Since QPS is low, you may have plenty of CPU per query so huge segments may not be a problem. Choose 12 or 24h or consumption and pick an appropriate segment size. You may then configure something like:

```javascript
"realtime.segment.flush.threshold.size": "0"
"realtime.segment.flush.threshold.time": "24h"
"realtime.segment.flush.desired.size": "450M"
```



