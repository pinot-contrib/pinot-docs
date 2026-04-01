---
description: Deep dive into the multi-stage engine (MSE) internals, execution model, and troubleshooting.
---

# Multi-stage query

For an overview of when to use the multi-stage engine (MSE) versus the single-stage engine (SSE), see [Query Engines (SSE vs MSE)](../../../build-with-pinot/querying-and-sql/sse-vs-mse.md). This section provides a deep dive into MSE internals. Most of the concepts explained here are related to the engine's execution model and are not required for writing queries. However, understanding them can help you take advantage of MSE's capabilities and troubleshoot issues.
