---
description: Describes the mailbox send operator in the multi-stage query engine.
---

# Mailbox send

The mailbox send operator is the operator that sends data to the mailbox receive operator. This is not an actual relational operator but a Pinot extension used to send data to other stages.

These operators are always the root of the intermediate and leaf stages.

## Implementation details

Stages in the multi-stage query engine are executed in parallel by different workers. Workers send data to each other using mailboxes. The number of mailboxes depends on the send operator parallelism, the receive operator parallelism and the distribution being used. At worst, there is one mailbox per worker pair, so if the upstream send operator has a parallelism of S and the receive operator has a parallelism of R, there will be S \* R mailboxes.

By default, these mailboxes are GRPC channels, but when both workers are in the same server, they can use shared memory and therefore a more efficient on heap mailbox is used.

The mailbox send operator wraps these mailboxes, offering single logical mailbox to the stage. How to distribute data to different workers of the downstream stage is determined by the distribution of the operator. The supported distributions are `hash`, `random` and `broadcast`.

* `hash` means there are multiple instances of the stream, and each instance contains records whose keys hash to a particular hash value. Instances are disjoint; a given record appears on exactly one stream. The list of numbers in the bracket indicates the columns used to calculate the hash. These numbers are 0-based column indexes on the virtual row projected by the upstream.
* `random` means there are multiple instances of the stream, and each instance contains randomly chosen records. Instances are disjoint; a given record appears on exactly one stream.
* `broadcast` means there are multiple instances of the stream, and all records appear in each instance. This is the most expensive distribution, as it requires sending all the data to all the workers.

### Blocking nature

The mailbox send operator is a streaming operator. It emits the blocks of rows as soon as they are received from the upstream operator.

## Hints

None

## Stats

### executionTimeMs

Type: Long

The summation of time spent by all threads executing the operator. This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows

Type: Long

The number of groups emitted by the operator. This operator should always emit as many rows as its upstream operator.

### stage

Type: number

The stage id of the operator. The root stage has id 0 and this number is incremented by 1 for each stage. Current implementation iterates over the stages in pre-order traversal, although this is not guaranteed.

This stat is useful to understand extract stages from queries, as explained in [understanding stages](../understanding-stages.md).

### parallelism

Type: Int

Number of threads executing the stage. Although this stat is only reported in the send mailbox operator, it is the same for all operators in the stage.

### fanOut

Type: Int

The number of workers this operation is sending data to. A large fan out may indicate that the operation is sending data to many workers, which may be a bottleneck that may be improved using partitioning.

### inMemoryMessages

Type: Int

How many messages have been sent in heap format by this mailbox. Sending in heap messages is more efficient than sending in raw format, as the messages do not need to be serialized and deserialized and no network transfer is needed.

### rawMessages

Type: Int

How many messages have been sent in raw format and therefore serialized by this mailbox. Sending in heap messages is more efficient than sending in raw format, as the messages do not need to be serialized and deserialized and no network transfer is needed.

### serializedBytes

Type: Long

How many bytes have been serialized by this mailbox. A high number here indicates that the mailbox is sending a lot of data to other servers, which is expensive in terms of CPU, memory and network.

### serializationTimeMs

Type: Long

How long it took to serialize the raw messages sent by this mailbox. This time is not wall time, but the sum of the time spent by all threads serializing messages.

{% hint style="info" %}
Take into account that this time does not include the impact on the network or the GC.
{% endhint %}

## Explain attributes

Given that the mailbox send operator is a meta-operator, it is not actually shown in the explain plan. Instead, a single `PinotLogicalExchange` or `PinotLogicalSortExchange` is shown in the explain plan. This exchange explain node is the logical representation of a pair of send and receive operators.

### distribution

Type: Expression

Example: `distribution=[hash[0]]`, `distribution=[random]` or `distribution=[broadcast]`

The distribution used by the mailbox receive operator. Values supported by Pinot are `hash`, `random` and `broadcast`, as explained in the [implementation details](mailbox-send.md#implementation-details).

While `broadcast` and `random` distributions don't have any parameters, the `hash` distribution includes a list of numbers in brackets. That list represents the columns used to calculate the hash and are the 0-based column indexes on the virtual row projected by the upstream operator.

For example, in following explain plan:

```
PinotLogicalExchange(distribution=[hash[0, 1]])
    LogicalProject(groupUUID=[$3], userUUID=[$4])
      LogicalTableScan(table=[[default, userGroups]])
```

Indicates that the data is distributed by the first and second columns of the projected row, which are `groupUUID` and `userUUID` respectively.

## Tips and tricks

None
