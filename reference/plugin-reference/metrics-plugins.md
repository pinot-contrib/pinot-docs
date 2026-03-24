---
description: Metrics plugin reference.
---

# Metrics Plugins

Pinot's metrics plugins select which JMX backend publishes internal metrics. The important distinction is not the metric name but the implementation that emits it.

## Built-in Backends

| Plugin | Role |
| --- | --- |
| Yammer | Default metrics backend in many Pinot deployments |
| Dropwizard | Alternate JMX metrics backend |
| Compound | Fan-out backend that publishes to multiple registries |

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
