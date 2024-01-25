---
description: An overview of the single-stage query engine.
---

# Single-stage query engine (v1)

The Pinot single-stage query engine (v1) uses a scatter-gather query engine model, shown in the following diagram. In certain cases, for example, if you need to query using JOINs on large data sets, the [multi-stage query engine (v2)](multi-stage-engine.md) may be a more performant option.

<figure><img src="../.gitbook/assets/Multi-Stage-Pinot-Query-Engine-v1 (2).png" alt=""><figcaption><p>Single-stage query engine (v1)</p></figcaption></figure>
