---
description: Connect federated SQL engines to Pinot for cross-source analytics.
---

# Query engines

Use federated query engines when Pinot is one source in a broader SQL stack and you want to join or compare it with other systems. These integrations are the right fit when a data platform already standardizes on Trino for interactive analytics.

## What belongs here

<table>
  <thead>
    <tr>
      <th>Engine</th>
      <th>Best for</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Trino</td>
      <td>Interactive federated SQL across multiple data sources</td>
      <td>The current guide covers Kubernetes deployment, Pinot catalog configuration, and CLI-based validation.</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
**Presto support removed**: The Pinot Presto connector, Docker images, and Helm chart have been removed as of [apache/pinot#17947](https://github.com/apache/pinot/pull/17947). Trino (the Presto successor) is the recommended query engine for federated SQL over Pinot.
{% endhint %}

## Detailed docs

* [Trino](../../integrations/trino.md)
* [Query engines on Kubernetes](../../basics/getting-started/kubernetes/query-engines.md)

## What this page covered

This page covered the federated SQL engine most commonly used to query Pinot alongside other systems.

## Next step

Use the linked Trino guide, then verify the catalog configuration with a small query before rolling it into production.

## Related pages

* [BI tools](bi-tools.md)
* [REST / gRPC APIs](rest-grpc-apis.md)
* [Querying Pinot](../querying-and-sql/querying-pinot.md)
