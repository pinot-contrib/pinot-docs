---
description: >-
  This section contains reference documentation for the FREQUENTLONGSSKETCH
  function.
---

# FrequentLongsSketch

`FREQUENTLONGSSKETCH` is an estimation data-sketch function which can be used to estimate the frequency of an item. It is based on [Apache Datasketches library](https://datasketches.apache.org/docs/Frequency/FrequentItemsOverview.html) and returns a serialized sketch object which can be merged with other sketches.

## Signature

> FREQUENTLONGSSKETCH(column, maxMapSize=256) -> Base64 encoded sketch object

* `column` (required): Name of the column to aggregate on. Needs to be a type which can be cast into 'LONG'.
* `maxMapSize`: This value specifies the maximum physical length of the internal hash map. The maxMapSize must be a power of 2 and the default value is 256.

## Usage Example

```sql
select FREQUENTLONGSSKETCH(AirlineID, 16) from airlineStats
```

| frequentlongssketch(AirlineID) |
| ------------------------------ |
| BAEKCAUAAAAOAAAAAA...          |

Which can be used, for example in Java as:

```java
byte[] byteArr = Base64.getDecoder().decode(encodedSketch);
LongsSketch sketch = LongsSketch.getInstance(Memory.wrap(byteArr));

LongsSketch.Row[] items = sketch.getFrequentItems(ErrorType.NO_FALSE_NEGATIVES);
for (int i = 0; i < items.length; i++) {
  LongsSketch.Row item = items[i];
  System.out.printf("Airline: %d, Frequency: %d %n", item.getItem(), item.getEstimate());
}
```

For more examples on the sketch API, refer to the Datasketches [documentation](https://datasketches.apache.org/docs/Frequency/FrequentItemsJavaExample.html).
