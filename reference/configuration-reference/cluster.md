---
description: Cluster-level configuration reference.
---

# Cluster Configuration

This page is the reference entry point for cluster-level settings: controller-backed configs, broker safeguards, query-engine toggles, and resource-accounting controls. The canonical field-by-field definitions remain in the existing cluster config page.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Cluster configs | Global config values stored in ZK and read by Pinot components | [Cluster](../../configuration-reference/cluster.md) |
| Query safety | Broker query limits, query-console visibility, and MSE enablement | [Cluster](../../configuration-reference/cluster.md) |
| Resource accounting | CPU and memory sampling plus automatic query killing | [Cluster](../../configuration-reference/cluster.md) |

## What this page covered

- The cluster-level settings you are most likely to touch.
- The source page that holds the full property table and REST examples.
- The operational areas affected by cluster config.

## Next step

Use the controller API or cluster config page to verify the exact property name before changing a live cluster.

## Related pages

- [Configuration Reference](README.md)
- [Table](../../configuration-reference/table.md)
- [Query Using Cursors](../../users/user-guide-query/query-using-cursors.md)
