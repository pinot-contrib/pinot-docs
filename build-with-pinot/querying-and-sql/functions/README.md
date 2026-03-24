---
description: Browse Pinot function families and jump to the right execution-engine guidance.
---

# Functions

Use this section as the entry point for Pinot SQL functions. The goal here is navigation: pick the function family, understand whether it is query-safe in the single-stage engine, and jump to the detailed page when you need full syntax or examples.

Most core function families work in both engines. Window functions require the multi-stage engine, and the engine column in the function index is the quickest way to confirm the supported execution model for a specific function.

## Browse by family

| Family | Typical use | Engine signal | Detailed docs |
| --- | --- | --- | --- |
| Aggregation | Metrics, distinct counts, sketches, percentiles | Both, with a few window-oriented helpers | [Aggregation Functions](../../../functions/aggregation/README.md) |
| Array | Multi-value and array manipulation | Both | [Array Functions](../../../functions/array/README.md) |
| Binary | Hashing and encoding | Both | [Binary Functions](../../../functions/binary/README.md) |
| DateTime | Bucketing, truncation, epoch conversion | Both | [DateTime Functions](../../../functions/datetime/README.md) |
| Funnel | Funnel analytics | Both | [Funnel Functions](../../../functions/funnel/README.md) |
| Geospatial | Spatial predicates and geometry conversion | Both | [GeoSpatial Functions](../../../functions/geospatial/README.md) |
| Hash | Hash-based distribution and routing helpers | Both | [Hash Functions](../../../functions/hash/README.md) |
| IP Address | Network and subnet checks | Both | [IP Address Functions](../../../functions/ip-address/README.md) |
| JSON | Path extraction, formatting, and typed JSON access | Both, with query-safe typed variants | [JSON Functions](../../../functions/json/README.md) |
| Math | Arithmetic and numeric shaping | Both | [Math Functions](../../../functions/math/README.md) |
| Miscellaneous | Utility predicates and helpers | Both | [Miscellaneous Functions](../../../functions/misc/README.md) |
| Null handling | Null-aware query behavior | Both, when null support is enabled | [Null Handling Functions](../../../functions/null-handling/README.md) |
| Sketch | Approximate analytics helpers | Both | [Sketch Functions](../../../functions/sketch/README.md) |
| Statistical | Variance and covariance functions | Both | [Statistical Functions](../../../functions/statistical/README.md) |
| String | Case, slicing, tokenizing, regex, and formatting | Both | [String Functions](../../../functions/string/README.md) |
| Trigonometric | Sine, cosine, and related math | Both | [Trigonometric Functions](../../../functions/trigonometric/README.md) |
| Type conversion | Cast-like and conversion helpers | Both | [Type Conversion Functions](../../../functions/type-conversion/README.md) |
| UDFs | Custom extension points | Varies by implementation | [User-Defined Functions](../../../functions/udf/README.md) |
| Vector / similarity | Embeddings and similarity search helpers | Both, where supported | [Vector / Similarity Functions](../../../functions/vector/README.md) |
| Window | Ranking, framing, and rolling calculations | Multi-stage only | [Window Functions](../../../functions/window/README.md) |

## Ingestion-time transformations

If you are shaping records before they land in Pinot, use the curated transformation guide instead of starting from the raw function catalog.

{% content-ref url="transformations.md" %}
[Transformations](transformations.md)
{% endcontent-ref %}

The transformation guide pulls together the functions most often used in schema updates, ingestion configs, and query projections, including typed JSON access, string shaping, date/time conversion, and multi-value helpers.

## Engine choice

If you are deciding whether a query belongs on the single-stage engine or the multi-stage engine, use the decision guide first and then return here for the function family that matters.

{% content-ref url="../sse-vs-mse.md" %}
[SSE vs MSE](../sse-vs-mse.md)
{% endcontent-ref %}

## What this page covered

- The major Pinot function families and the engine signal for each family.
- Where to go for ingestion-time transformation guidance.
- Which engine decision guide to use before choosing a function-heavy query shape.

## Next step

- Open the function family page for the syntax and examples you need, then confirm the engine constraints before writing the query.

## Related pages

- [SSE vs MSE](../sse-vs-mse.md)
- [Transformations](transformations.md)
- [Function Index](../../../users/user-guide-query/function-index.md)
