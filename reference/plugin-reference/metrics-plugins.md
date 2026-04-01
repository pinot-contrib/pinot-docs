---
description: Metrics plugin reference.
---

# Metrics Plugins

Pinot's metrics plugins select which JMX backend publishes internal metrics. The important distinction is not the metric name but the implementation that emits it.

## Built-in Backends

<table>
  <thead>
    <tr>
      <th>Plugin</th>
      <th>Role</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Yammer</td>
      <td>Default metrics backend in many Pinot deployments</td>
    </tr>
    <tr>
      <td>Dropwizard</td>
      <td>Alternate JMX metrics backend</td>
    </tr>
    <tr>
      <td>Compound</td>
      <td>Fan-out backend that publishes to multiple registries</td>
    </tr>
  </tbody>
</table>

## What this page covered

- The built-in metric backends.
- Why plugin selection matters for observability.
- Where to look when you need to wire metrics into Pinot.

## Next step

Check the component you are configuring, then verify the plugin name and any required registry settings before restarting the service.

## Related pages

- [Plugin Reference](README.md)
- [Monitoring Metrics](../configuration-reference/monitoring-metrics.md)
- [Configuration Reference](../configuration-reference/README.md)
