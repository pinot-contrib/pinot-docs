# Hints

Multi-stage query engine behavior can be customized with hints. Hints are provided as a comment, for example `/* hintType(hint1='value1',hint2='value2') */`.

Apache Pinot supports the following hints:

* `aggOptions`, explained in [aggregate operator](operator-types/aggregate.md#hints).
* `windowOptions`, explained in [window operator](operator-types/window.md#hints).
* `joinOptions`, explained in [join operator](operator-types/hash_join.md#hints).
