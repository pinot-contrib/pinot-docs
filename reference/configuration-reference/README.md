---
description: Dense reference for Pinot configuration surfaces.
---

# Configuration Reference

This section reorganizes the configuration surface into the core objects operators reach for most often: cluster, schema, table, ingestion, job specs, metrics, dynamic environment handling, and plugin settings. Cluster and schema configuration are flattened directly into this section, and the pages here are the primary reference entry points, while some legacy material still remains in the older `configuration-reference/` tree.

## Reference Map

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Use it for</th>
      <th>Reference page</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cluster</td>
      <td>Cluster-wide knobs, query protection, and broker behavior</td>
      <td>[Cluster](cluster.md)</td>
    </tr>
    <tr>
      <td>Schema</td>
      <td>Column definitions, null handling, data types, and MAP field support</td>
      <td>[Schema](schema.md)</td>
    </tr>
    <tr>
      <td>Table</td>
      <td>Offline, real-time, hybrid, routing, query, and indexing config</td>
      <td>[Table](table.md)</td>
    </tr>
    <tr>
      <td>Ingestion</td>
      <td>Stream and batch ingestion settings embedded in table config</td>
      <td>[Ingestion](ingestion.md)</td>
    </tr>
    <tr>
      <td>Job spec</td>
      <td>Offline ingestion job configuration and templating</td>
      <td>[Ingestion Job Spec](job-specification.md)</td>
    </tr>
    <tr>
      <td>Monitoring metrics</td>
      <td>Server, broker, and controller metric configuration</td>
      <td>[Monitoring Metrics](monitoring-metrics.md)</td>
    </tr>
    <tr>
      <td>Dynamic environment</td>
      <td>Environment-variable substitution in config payloads</td>
      <td>[Dynamic Environment](dynamic-environment.md)</td>
    </tr>
    <tr>
      <td>Plugin reference</td>
      <td>Plugin-family configuration and version guidance</td>
      <td>[Plugin Configuration Reference](plugin-reference.md)</td>
    </tr>
  </tbody>
</table>

## What this page covers

- The dense configuration surfaces that belong in reference.
- The flat reference pages for the most commonly used Pinot config topics.
- How to get from this landing page to the detailed config docs.

## Next step

Open the specific config page for the object you are changing, then cross-check any linked table or schema behavior before editing a table config.

## Related pages

- [Table](table.md)
- [Schema](schema.md)
- [Ingestion](ingestion.md)
- [Plugin Configuration Reference](plugin-reference.md)
- [Legacy Plugin Configuration Landing](../../configuration-reference/plugin-reference/README.md)
