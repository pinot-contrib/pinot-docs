---
description: Dense reference for Pinot plugin families.
---

# Plugin Families Reference

This section is the reference map for Pinot's built-in plugin families. The detailed family pages live here so the configuration tree can stay dense and the authoring guides can stay elsewhere.

## Plugin Families

<table>
  <thead>
    <tr>
      <th>Family</th>
      <th>Use it for</th>
      <th>Page</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Stream ingestion connectors</td>
      <td>Kafka, Kinesis, and Pulsar consumer factories</td>
      <td>[Stream Ingestion Connectors](stream-ingestion-connectors.md)</td>
    </tr>
    <tr>
      <td>Stream connector version matrix</td>
      <td>Compatibility between broker, connector, and Kafka major versions</td>
      <td>[Stream Connector Version Matrix](stream-connector-matrix.md)</td>
    </tr>
    <tr>
      <td>Metrics plugins</td>
      <td>JMX metric backends and registry fan-out</td>
      <td>[Metrics Plugins](metrics-plugins.md)</td>
    </tr>
    <tr>
      <td>Environment provider</td>
      <td>Cloud metadata discovery for instance placement</td>
      <td>[Environment Provider](environment-provider.md)</td>
    </tr>
  </tbody>
</table>

## What this page covered

- The plugin families that belong in the configuration reference.
- The detailed pages that live under this subtree.
- The areas where version compatibility matters most.

## Next step

Open the plugin-family page for the integration you are changing, then verify supported versions before changing deployment settings.

## Related pages

- [Configuration Reference](../configuration-reference/README.md)
- [Stream Ingestion Connectors](stream-ingestion-connectors.md)
- [Metrics Plugins](metrics-plugins.md)
