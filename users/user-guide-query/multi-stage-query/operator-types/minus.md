---
description: Describes the minus relation operator in the multi-stage query engine.
---

# Minus

The minus operator is used to subtract the result of one query from another query. This operator is used to find the difference between two sets of rows, usually by using the SQL `EXCEPT` operator.

{% hint style="warning" %}
Although it is accepted by the parser, the `ALL` modifier is currently ignored. Therefore `EXCEPT` and `EXCEPT ALL` are equivalent. This issue has been reported in [#13127](https://github.com/apache/pinot/issues/13127)
{% endhint %}

## Implementation details

The minus operator is a semi-blocking operator that first consumes the right input relation in a blocking fashion and then consumes the left input relation in a streaming fashion.

The current implementation consumes the whole right input relation first and stores the rows in a set. Then it consumes the left input relation one block at a time. Each time a block of rows is read from the left input relation, the operator checks if the rows are in the set of rows from the right input relation. All unique rows that are not in the set are added to a new partial result block. Once the whole left input block is analyzed, the operator emits the partial result block.

This process is repeated until all rows from the left input relation are processed.

### Blocking nature

The minus operator is a semi-blocking operator that first consumes the right input relation in a blocking fashion and then consumes the left input relation in a streaming fashion.

In pseudo-code, the algorithm looks like this:

```
HashSet<Row> rightRows = new HashSet<>();
Block rightBlock = rightInput.nextBlock();
while (rightBlock is not EOS) {
    rightRows.addAll(rightBlock.getRows());
    rightBlock = rightInput.nextBlock();
}
Block leftBlock = leftInput.nextBlock();
while (leftBlock is not EOS) {
    Block partialResultBlock = new Block();
    for (Row row : leftBlock.getRows()) {
        if (rightRows.add(row)) {
            partialResultBlock.add(row);
        }
    }
    emit partialResultBlock;
    leftBlock = leftInput.nextBlock();
}
emit EOS
```

## Hints

None

## Stats

### executionTimeMs

Type: Long

The summation of time spent by all threads executing the operator. This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows

Type: Long

The number of groups emitted by the operator.

## Explain attributes

The minus operator is represented in the explain plan as a `LogicalMinus` explain node.

### all

Type: Boolean

This attribute is used to indicate if the operator should return all the rows or only the distinct rows.

{% hint style="warning" %}
Although it is accepted in SQL, the `all` attribute is not currently used in the minus operator. The returned rows are always distinct. This issue has been reported in [#13127](https://github.com/apache/pinot/issues/13127)
{% endhint %}

## Tips and tricks

### Memory pressure

The minus operator ends up having to store all unique rows from both input relations in memory. This can lead to memory pressure if the input relations are large and have a high number of unique rows.

### The order of input relations matter

Although the minus operator ends up adding all unique rows from both input relations to a set, the order of input relations matters. While the right input relation is consumed in a blocking fashion, the left input relation is consumed in a streaming fashion. Therefore the latency of the whole query could be improved if the left input relation is producing values in streaming fashion.

{% hint style="info" %}
In case one of the inputs is blocking and the other is not, it is recommended to use the blocking relation as the right input relation.
{% endhint %}
