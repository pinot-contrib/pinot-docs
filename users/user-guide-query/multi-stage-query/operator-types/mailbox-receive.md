---
description: Describes the mailbox receive operator in the multi-stage query engine.
---

# Mailbox receive

The mailbox receive operator is the operator that receives the data from the mailbox send operator. This is not an actual relational operator but a Pinot extension used to receive data from other stages.

## Implementation details

Stages in the multi-stage query engine are executed in parallel by different workers. Workers send data to each other using mailboxes. The number of mailboxes depends on the send operator parallelism, the receive operator parallelism and the distribution being used. At worst, there is one mailbox per worker pair, so if the upstream send operator has a parallelism of S and the receive operator has a parallelism of R, there will be S \* R mailboxes.

By default, these mailboxes are GRPC channels, but when both workers are in the same server, they can use shared memory and therefore a more efficient on heap mailbox is used.

The mailbox receive operator pulls data from these mailboxes and sends it to the downstream operator.

### Blocking nature

The mailbox receive operator is a streaming operator. It emits the blocks of rows as soon as they are received from the upstream operator.

It is important to notice that the mailbox receive operator tries to be fair when reading from multiple workers.

## Hints

None

## Stats

### executionTimeMs

Type: Long

The summation of time spent by all threads executing the operator. This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows

Type: Long

The number of groups emitted by the operator. This operator should always emit as many rows as its upstream operator.

### fanIn

Type: Long

How many workers are sending data to this operator.

### inMemoryMessages

Type: Long

How many messages have been received in heap format by this mailbox. Receiving in heap messages is more efficient than receiving them in raw format, as the messages do not need to be serialized and deserialized and no network transfer is needed.

### rawMessages

Type: Long

How many messages have been received in raw format and therefore serialized by this mailbox. Receiving in heap messages is more efficient than receiving them in raw format, as the messages do not need to be serialized and deserialized and no network transfer is needed.

### deserializedBytes

Type: Long

How many bytes have been deserialized by this mailbox. A high number here indicates that the mailbox is receiving a lot of data from other servers, which is expensive in terms of CPU, memory and network.

### deserializeTimeMs

Type: Long

How long it took to deserialize the raw messages sent to this mailbox. This time is not wall time, but the sum of the time spent by all threads deserializing messages.

{% hint style="info" %}
Take into account that this time does not include the impact on the network or the GC.
{% endhint %}

### downstreamWaitMs

Type: Long

How much time this operator has been blocked waiting while offering data to be consumed by the downstream operator. A high number here indicates that the downstream operator is slow and may be a bottleneck. For example, usually the receive operator that is the left input of a join operator has a high value here, as the join needs to consume all the messages from the right input before it can start consuming the left input.

### upstreamWaitMs

Type: Long

How much time this operator has been blocked waiting for more data to be sent by the upstream (send) operator. A high number here indicates that the upstream operator is slow and may be a bottleneck. For example, blocking operators like aggregations, sorts, joins or window functions require all the data to be received before they can start emitting a result, so having them as upstream operators of a mailbox receive operator can lead to high values here.

## Explain attributes

Given that the mailbox receive operator is a meta-operator, it is not actually shown in the explain plan. Instead, a single `PinotLogicalExchange` or `PinotLogicalSortExchange` is shown in the explain plan. This exchange explain node is the logical representation of a pair of send and receive operators.

See the [mailbox send operator](mailbox-send.md#explain-attributes) to understand the attributes of the exchange explain node.

## Tips and tricks

None
