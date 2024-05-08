---
description: >-
  Describes the mailbox send operator in the multi-stage query engine.
---

# Mailbox send operator

## Implementation details

### Blocking nature

## Hints
None

## Stats
### executionTimeMs
Type: Long

The summation of time spent by all threads executing the operator.
This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows
Type: Long

The number of groups emitted by the operator.
This operator should always emit as many rows as its upstream operator.

## Explain attributes

### stage
Type: number

The stage id of the operator. The root stage has id 0 and this number is incremented by 1 for each stage.
Current implementation iterates over the stages in pre-order traversal, although this is not guaranteed.

This stat is useful to understand extract stages from queries, as explained in 
[understanding stages](../understanding-stages.md).

### parallelism
Type: Int

Number of threads executing the stage.
Although this stat is only reported in the send mailbox operator, it is the same for all operators in the stage.

### fanOut
Type: Int

The number of workers this operation is sending data to.
A large fan out may indicate that the operation is sending data to many workers, which may be a bottleneck that may be
improved using partitioning.

### inMemoryMessages
Type: Int

How many messages have been sent in heap format by this mailbox.
Sending in heap messages is more efficient than sending in raw format, as the messages do not need to be serialized
and deserialized and no network transfer is needed.

### rawMessages
Type: Int

How many messages have been sent in raw format and therefore serialized by this mailbox.
Sending in heap messages is more efficient than sending in raw format, as the messages do not need to be serialized
and deserialized and no network transfer is needed.

### serializedBytes
Type: Long

How many bytes have been serialized by this mailbox.
A high number here indicates that the mailbox is sending a lot of data to other servers, which is expensive in terms
of CPU, memory and network.

### serializationTimeMs
Type: Long

How long it took to serialize the raw messages sent by this mailbox. 
This time is not wall time, but the sum of the time spent by all threads serializing messages.

{% hint style="info" %}
Take into account that this time does not include the impact on the network or the GC.
{% endhint %}

## Tips and tricks