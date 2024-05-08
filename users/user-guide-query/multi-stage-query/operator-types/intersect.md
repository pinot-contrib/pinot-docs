---
description: >-
  Describes the intersect relation operator in the multi-stage query engine.
---

# Intersect relational operator

The intersect operator is a relational operator that combines two relations and returns the common rows between 
them. 
The operator is used to find the intersection of two or more relations.

## Implementation details
The current implementation consumes the whole right input relation first and stores the rows in a set.
Then it consumes the left input relation one block at a time.
Each time a block of rows is read from the left input relation, the operator checks if the rows are in the set of rows
from the right input relation.
All unique rows that are in the set are added to a new partial result block.
Once the whole left input block is analyzed, the operator emits the partial result block.

This process is repeated until all rows from the left input relation are processed.

In pseudo-code, the algorithm looks like this:

### Blocking nature
The intersect operator is a semi-blocking operator that first consumes the right input relation in a blocking fashion
and then consumes the left input relation in a streaming fashion.

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
        if (rightRows.remove(row)) {
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

The summation of time spent by all threads executing the operator.
This means that the wall time spent in the operation may be smaller that this value if the parallelism is larger than 1.

### emittedRows
Type: Long

The number of groups emitted by the operator.

## Explain attributes

## Tips and tricks

### The order of input relations matter
The intersect operator has a memory footprint that is proportional to the number of unique rows in the right input 
relation.
It also consumes the right input relation in a blocking fashion while the left input relation is consumed in a
streaming fashion.

This means that:
- In case any of the input relations is significantly larger than the other, it is recommended to use the
  smaller relation as the right input relation.
- In case one of the input is blocking and the other is not, it is recommended to use the blocking relation as the right
  input relation.

This two hints can be contradictory, so it is up to the user to decide which one to follow based on the specific
query pattern.
Remember that you can use the stage stats to check the number of rows emitted by each of the inputs and adjust the order
of the inputs accordingly.
