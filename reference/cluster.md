---
description: An overview of the single-stage query engine.
---

# Single-stage query engine (v1)

The Pinot single-stage query engine (v1) uses a scatter-gather query engine model, shown in the following diagram. In certain cases, for example, if you need to query using JOINs on large data sets, the [multi-stage query engine (v2)](https://app.gitbook.com/o/-LtRX9NwSr7Ga7zA4piL/s/-LtH6nl58DdnZnelPdTc-887967055/\~/changes/1760/reference/cluster-1) may be a more performant option.&#x20;

<figure><img src="../.gitbook/assets/Multi-Stage-Pinot-Query-Engine-v1 (2).png" alt=""><figcaption></figcaption></figure>
