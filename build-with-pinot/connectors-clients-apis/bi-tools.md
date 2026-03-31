---
description: Connect Superset, Tableau, and Metabase to Pinot for dashboards and ad hoc exploration.
---

# BI tools

Use BI tools when the main goal is dashboards, self-service exploration, or visual analysis. These integrations usually sit on top of JDBC or a Pinot-specific connector, so this page helps you pick the right tool before you dive into the detailed setup guide.

## What belongs here

| Tool | Connection style | Best for | Notes |
| --- | --- | --- | --- |
| Superset | Native Pinot connector | Dashboards and SQL exploration | The current guide covers Docker and Kubernetes setup paths and a prebuilt Pinot connector image. |
| Tableau | JDBC | Enterprise BI and drag-and-drop analysis | The current guide builds the JDBC artifacts from source and copies the required jars into Tableau's driver directory. |
| Metabase | Community Pinot driver | Lightweight dashboards and exploration | The current quickstart is marked preview and uses Pinot 1.3.0, Metabase v0.55.7, and driver v1.1.0 in the source doc. |

## How to choose

Choose Superset when you want an open-source dashboarding tool with a Pinot-aware connector. Choose Tableau when your organization already standardizes on JDBC-based BI access. Choose Metabase when you want a simpler self-service experience and can accept a preview-quality connector.

The Tableau and Metabase detail docs both include version-pinned quickstart examples. Keep those examples aligned with the source docs when you refresh them so the build instructions remain reproducible.

## Detailed docs

* [Superset](superset.md)
* [Tableau](tableau.md)
* [Metabase](metabase.md)

## What this page covered

This page covered the three BI and visualization integrations that most often sit on top of Pinot JDBC or a Pinot-specific connector.

## Next step

Pick the tool your team already uses and follow the linked setup guide, then validate the Pinot connection with a small query or sample dashboard.

## Related pages

* [Client libraries](client-libraries.md)
* [REST / gRPC APIs](rest-grpc-apis.md)
* [Query engines](query-engines.md)
