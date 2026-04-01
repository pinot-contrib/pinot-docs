---
description: Browse Pinot function families and jump to the right execution-engine guidance.
---

# Functions

Use this section as the entry point for Pinot SQL functions. The goal here is navigation: pick the function family, understand whether it is query-safe in the single-stage engine, and jump to the detailed page when you need full syntax or examples.

Most core function families work in both engines. Window functions require the multi-stage engine, and the engine column in the function index is the quickest way to confirm the supported execution model for a specific function.

## Browse by family

<table>
  <thead>
    <tr>
      <th>Family</th>
      <th>Typical use</th>
      <th>Engine signal</th>
      <th>Detailed docs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Aggregation</td>
      <td>Metrics, distinct counts, sketches, percentiles</td>
      <td>Both, with a few window-oriented helpers</td>
      <td>[Aggregation Functions](aggregation/README.md)</td>
    </tr>
    <tr>
      <td>Array</td>
      <td>Multi-value and array manipulation</td>
      <td>Both</td>
      <td>[Array Functions](array/README.md)</td>
    </tr>
    <tr>
      <td>Binary</td>
      <td>Hashing and encoding</td>
      <td>Both</td>
      <td>[Binary Functions](binary/README.md)</td>
    </tr>
    <tr>
      <td>DateTime</td>
      <td>Bucketing, truncation, epoch conversion</td>
      <td>Both</td>
      <td>[DateTime Functions](datetime/README.md)</td>
    </tr>
    <tr>
      <td>Funnel</td>
      <td>Funnel analytics</td>
      <td>Both</td>
      <td>[Funnel Functions](funnel/README.md)</td>
    </tr>
    <tr>
      <td>Geospatial</td>
      <td>Spatial predicates and geometry conversion</td>
      <td>Both</td>
      <td>[GeoSpatial Functions](geospatial/README.md)</td>
    </tr>
    <tr>
      <td>Hash</td>
      <td>Hash-based distribution and routing helpers</td>
      <td>Both</td>
      <td>[Hash Functions](hash/README.md)</td>
    </tr>
    <tr>
      <td>IP Address</td>
      <td>Network and subnet checks</td>
      <td>Both</td>
      <td>[IP Address Functions](ip-address/README.md)</td>
    </tr>
    <tr>
      <td>JSON</td>
      <td>Path extraction, formatting, and typed JSON access</td>
      <td>Both, with query-safe typed variants</td>
      <td>[JSON Functions](json/README.md)</td>
    </tr>
    <tr>
      <td>Math</td>
      <td>Arithmetic and numeric shaping</td>
      <td>Both</td>
      <td>[Math Functions](math/README.md)</td>
    </tr>
    <tr>
      <td>Miscellaneous</td>
      <td>Utility predicates and helpers</td>
      <td>Both</td>
      <td>[Miscellaneous Functions](misc/README.md)</td>
    </tr>
    <tr>
      <td>Null handling</td>
      <td>Null-aware query behavior</td>
      <td>Both, when null support is enabled</td>
      <td>[Null Handling Functions](null-handling/README.md)</td>
    </tr>
    <tr>
      <td>Sketch</td>
      <td>Approximate analytics helpers</td>
      <td>Both</td>
      <td>[Sketch Functions](sketch/README.md)</td>
    </tr>
    <tr>
      <td>Statistical</td>
      <td>Variance and covariance functions</td>
      <td>Both</td>
      <td>[Statistical Functions](statistical/README.md)</td>
    </tr>
    <tr>
      <td>String</td>
      <td>Case, slicing, tokenizing, regex, and formatting</td>
      <td>Both</td>
      <td>[String Functions](string/README.md)</td>
    </tr>
    <tr>
      <td>Trigonometric</td>
      <td>Sine, cosine, and related math</td>
      <td>Both</td>
      <td>[Trigonometric Functions](trigonometric/README.md)</td>
    </tr>
    <tr>
      <td>Type conversion</td>
      <td>Cast-like and conversion helpers</td>
      <td>Both</td>
      <td>[Type Conversion Functions](type-conversion/README.md)</td>
    </tr>
    <tr>
      <td>UDFs</td>
      <td>Custom extension points</td>
      <td>Varies by implementation</td>
      <td>[User-Defined Functions](udf/README.md)</td>
    </tr>
    <tr>
      <td>Vector / similarity</td>
      <td>Embeddings and similarity search helpers</td>
      <td>Both, where supported</td>
      <td>[Vector / Similarity Functions](vector/README.md)</td>
    </tr>
    <tr>
      <td>Window</td>
      <td>Ranking, framing, and rolling calculations</td>
      <td>Multi-stage only</td>
      <td>[Window Functions](window/README.md)</td>
    </tr>
  </tbody>
</table>

## Ingestion-time transformations

If you are shaping records before they land in Pinot, use the curated transformation guide instead of starting from the raw function catalog.

{% content-ref url="transformations.md" %}
[Transformations](transformations.md)
{% endcontent-ref %}

The transformation guide pulls together the functions most often used in schema updates, ingestion configs, and query projections, including typed JSON access, string shaping, date/time conversion, and multi-value helpers.

## Engine choice

If you are deciding whether a query belongs on the single-stage engine or the multi-stage engine, use the decision guide first and then return here for the function family that matters.

{% content-ref url="../build-with-pinot/querying-and-sql/sse-vs-mse.md" %}
[SSE vs MSE](../build-with-pinot/querying-and-sql/sse-vs-mse.md)
{% endcontent-ref %}

## What this page covered

- The major Pinot function families and the engine signal for each family.
- Where to go for ingestion-time transformation guidance.
- Which engine decision guide to use before choosing a function-heavy query shape.

## Next step

- Open the function family page for the syntax and examples you need, then confirm the engine constraints before writing the query.

## Related pages

- [SSE vs MSE](../build-with-pinot/querying-and-sql/sse-vs-mse.md)
- [Transformations](transformations.md)
- [Function Index](../build-with-pinot/querying-and-sql/function-index.md)
