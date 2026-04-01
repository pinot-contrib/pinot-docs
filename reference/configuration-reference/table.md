---
description: Table configuration reference.
---

# Table Configuration

The detailed table config page stays in the original location. This page is the reference entry point for the pieces operators edit most often: table identity, routing, query controls, ingestion settings, indexing, tenants, and upsert or dedup.

## Key Areas

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Why it matters</th>
      <th>Source</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Table identity</td>
      <td>OFFLINE, REALTIME, and hybrid table structure</td>
      <td>[Table](../../configuration-reference/table.md)</td>
    </tr>
    <tr>
      <td>Routing</td>
      <td>Broker-to-server routing and pruning behavior</td>
      <td>[Table](../../configuration-reference/table.md)</td>
    </tr>
    <tr>
      <td>Query settings</td>
      <td>Query timeout, resource limits, and engine toggles</td>
      <td>[Table](../../configuration-reference/table.md)</td>
    </tr>
    <tr>
      <td>Ingestion</td>
      <td>Batch and streaming ingestion config nested in table config</td>
      <td>[Ingestion](../../configuration-reference/ingestion.md)</td>
    </tr>
    <tr>
      <td>Indexing</td>
      <td>Per-column index configuration and deprecated forms</td>
      <td>[Table](../../configuration-reference/table.md)</td>
    </tr>
    <tr>
      <td>Upsert and dedup</td>
      <td>Real-time correctness controls for mutable streams</td>
      <td>[Table](../../configuration-reference/table.md)</td>
    </tr>
  </tbody>
</table>

## What this page covered

- The table config areas that most directly affect ingestion and query behavior.
- The canonical table-config reference page.
- The relationship between table config and the rest of the reference tree.

## Next step

Check the table config page and the related ingestion or indexing page before editing a production table definition.

## Related pages

- [Configuration Reference](README.md)
- [Schema](schema.md)
- [Ingestion](../../configuration-reference/ingestion.md)
- [Indexing](../../basics/indexing/README.md)
