---
description: API reference for Pinot query and controller endpoints.
---

# Pinot API Reference

This section reorganizes the Pinot API surface into broker query APIs, query response formatting, controller admin APIs, controller API examples, and broker gRPC. The goal is to keep the overview light while still documenting the endpoint-level behavior operators and client authors need.

## Reference Map

| Area | Use it for | Source page |
| --- | --- | --- |
| Broker query API | SQL query submission, broker cursors, and response-store lifecycle | [Broker Query API](query-api.md) |
| Query response format | Response fields and cursor payload structure | [Query Response Format](query-response-format.md) |
| Controller admin API | Swagger UI walkthrough for cluster and table administration | [Controller Admin API](controller-admin-api.md) |
| Controller API examples | Endpoint families and representative admin requests | [Controller API Examples](controller-api.md) |
| Broker gRPC | gRPC query transport and client configuration | [Broker gRPC API](broker-grpc-api.md) |

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
