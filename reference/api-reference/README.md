---
description: API reference for Pinot query and controller endpoints.
---

# Pinot API Reference

This section reorganizes the Pinot API surface into broker query APIs, query response formatting, controller admin APIs, controller API examples, and broker gRPC. The goal is to keep the overview light while still documenting the endpoint-level behavior operators and client authors need.

## Reference Map

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Use it for</th>
      <th>Source page</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Broker query API</td>
      <td>SQL query submission, broker cursors, and response-store lifecycle</td>
      <td>[Broker Query API](query-api.md)</td>
    </tr>
    <tr>
      <td>Query response format</td>
      <td>Response fields and cursor payload structure</td>
      <td>[Query Response Format](query-response-format.md)</td>
    </tr>
    <tr>
      <td>Controller admin API</td>
      <td>Swagger UI walkthrough for cluster and table administration</td>
      <td>[Controller Admin API](controller-admin-api.md)</td>
    </tr>
    <tr>
      <td>Controller API examples</td>
      <td>Endpoint families and representative admin requests</td>
      <td>[Controller API Examples](controller-api.md)</td>
    </tr>
    <tr>
      <td>Broker gRPC</td>
      <td>gRPC query transport and client configuration</td>
      <td>[Broker gRPC API](broker-grpc-api.md)</td>
    </tr>
  </tbody>
</table>

## What this page covered

- The main Pinot API surfaces and their intended use.
- Which pages in this subtree contain endpoint-level detail.
- Where to go for query, controller, and gRPC reference material.

## Next step

Pick the API family you need, then cross-check the request and response examples against the component you are targeting.

## Related pages

- [Broker Query API](query-api.md)
- [Query Response Format](query-response-format.md)
- [Controller Admin API](controller-admin-api.md)
- [Controller API Examples](controller-api.md)
- [Broker gRPC API](broker-grpc-api.md)
