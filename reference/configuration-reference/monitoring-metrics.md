---
description: Monitoring-metric configuration reference.
---

# Monitoring Metrics Reference

This page points to the metric configuration reference for broker, server, and controller observability. The canonical metric names, defaults, and plugin interactions stay in the original metrics page.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Metric families | Broker, server, controller, and JVM metrics | [Monitoring Metrics](../../configuration-reference/monitoring-metrics.md) |
| Plugin wiring | How metric implementations are selected | [Plugin Reference](../../configuration-reference/plugin-reference/metrics-plugins.md) |

## What this page covered

- The observability-related config surface in Pinot.
- The relationship between metrics config and the plugin system.
- The source page that contains the full metric property list.

## Next step

Start from the metric family you care about, then confirm the plugin implementation and component-level defaults before changing the config.

## Related pages

- [Configuration Reference](README.md)
- [Plugin Families Reference](../plugin-reference/README.md)
- [Release Notes](../release-notes/README.md)
