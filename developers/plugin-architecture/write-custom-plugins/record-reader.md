# Input Format Plugin

Pinot [supports multiple input formats](../../../basics/data-import/pinot-input-formats.md) out of the box for batch ingestion. For real-time ingestion, currently only JSON is supported. However, due to pluggable architecture of pinot you can easily use any format by implementing standard interfaces.

## Batch Record Reader Plugin

All the Batch Input formats supported by Pinot utilise [RecordReader](https://github.com/apache/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/data/readers/RecordReader.java) to deserialize the data.\
You can also implement the RecordReader and [RecordExtractor](https://github.com/apache/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/data/readers/RecordExtractor.java) interface to add support for your own file formats.

To index the file into Pinot segment, simply implement the interface and plug it into the index engine - [SegmentCreationDriverImpl](https://github.com/apache/blob/master/pinot-core/src/main/java/org/apache/pinot/core/segment/creator/impl/SegmentIndexCreationDriverImpl.java). We use a 2-passes algorithm to index the file into Pinot segment, hence the _rewind()_ method is required for the record reader.

### Generic Row

[GenericRow](https://github.com/apache/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/data/readers/GenericRow.java) is the record abstraction which the index engine can read and index with. It is a map from column name (String) to column value (Object). For multi-valued column, the value should be an object array (Object\[]).

### Contracts for Record Reader

There are several contracts for record readers that developers should follow when implementing their own record readers:

* The output GenericRow should follow the table schema provided, in the sense that:
  * All the columns in the schema should be preserved (if column does not exist in the original record, put default value instead)
  * Columns not in the schema should not be included
  * Values for the column should follow the field spec from the schema (data type, single-valued/multi-valued)
* For the time column (refer to [TimeFieldSpec](https://github.com/apache/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/data/TimeFieldSpec.java)), record reader should be able to read both incoming and outgoing time (we allow _incoming time - time value from the original data_ to _outgoing time - time value stored in Pinot_ conversion during index creation).
  * If incoming and outgoing time column name are the same, use incoming time field spec
  * If incoming and outgoing time column name are different, put both of them as time field spec
  * We keep both incoming and outgoing time column to handle cases where the input file contains time values that are already converted

## Stream Decoder Plugin

Pinot uses decoders to parse data available in real-time streams. Decoders are responsible for converting binary data in the streams to a GenericRow object.

You can write your own decoder by implementing the [StreamMessageDecoder](https://github.com/apache/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/stream/StreamMessageDecoder.java) interface. You can also use the [RecordExtractor](https://github.com/apache/blob/master/pinot-spi/src/main/java/org/apache/pinot/spi/data/readers/RecordExtractor.java) from the batch input formats to extract fields to GenericRow from the parsed object.
