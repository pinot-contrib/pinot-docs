---
description: Deep dive into the multi-stage engine (MSE) internals, execution model, and troubleshooting.
---

# Multi-stage query

For an overview of when to use the multi-stage engine (MSE) versus the single-stage engine (SSE), see [Query Engines (SSE vs MSE)](../../../build-with-pinot/querying-and-sql/sse-vs-mse.md). This section provides a deep dive into MSE internals. Most of the concepts explained here are related to the engine's execution model and are not required for writing queries. However, understanding them can help you take advantage of MSE's capabilities and troubleshoot issues.

## Mailbox channel keep-alive

In versions containing [Apache Pinot #19383](https://github.com/apache/pinot/pull/19383), MSE mailbox data channels use gRPC keep-alive by default. This helps detect a peer that stops responding without closing its socket, such as an unreachable host or an obsolete pod address. Dropping the dead transport allows reconnection instead of repeatedly sending queries to a silently broken cached connection. Queries can still fail or time out during detection; keep-alive does not retry failed queries.

These startup settings apply to mailbox services on brokers and servers. They are separate from the broker dispatch-channel settings under `pinot.query.multistage.dispatch.channel.*` and the user-facing gRPC query service.

| Property | Default | Description |
| --- | --- | --- |
| `pinot.query.runner.channel.keep.alive.time.ms` | `300000` | Client ping interval in milliseconds. A non-positive value disables keep-alive. gRPC clamps positive intervals below 10000 ms to 10000 ms. |
| `pinot.query.runner.channel.keep.alive.timeout.ms` | `30000` | Time in milliseconds to wait for a ping acknowledgment before declaring the transport dead. Must be positive when keep-alive is enabled. |
| `pinot.query.runner.channel.keep.alive.without.calls` | `false` | Whether clients ping connections without active RPCs. Enable only after every receiving peer permits these pings. |
| `pinot.query.runner.mailbox.server.permit.keep.alive.time.ms` | `300000` | Minimum ping interval in milliseconds accepted by a mailbox server. A non-positive value retains the gRPC server default; it does not disable enforcement. |
| `pinot.query.runner.mailbox.server.permit.keep.alive.without.calls` | `false` | Whether the mailbox server accepts pings without active RPCs. |

With the defaults, pings are deferred while no RPC is active. A later query may therefore encounter the dead connection and fail during recovery. Permitting and enabling pings without calls allows detection between queries, but does not guarantee that queries cannot encounter a new failure.

### Safely tuning detection

Keep the defaults during a mixed-version rollout: older mailbox servers enforce a five-minute minimum and reject pings without calls. Wait until **every broker and server** supports these settings before tuning them. For each channel, the client interval must be at least the receiving server's permitted interval.

1. First lower the receiving permits on all brokers and servers, for example `pinot.query.runner.mailbox.server.permit.keep.alive.time.ms=15000`. If idle pings are planned, also set `pinot.query.runner.mailbox.server.permit.keep.alive.without.calls=true`. Complete the rolling restart before changing clients. Verify `permitKeepAliveTimeMs` and `permitKeepAliveWithoutCalls` in the `Starting GrpcMailboxServer` startup log.
2. Then lower `pinot.query.runner.channel.keep.alive.time.ms`, for example to `30000`, while retaining the default 30000 ms timeout. Roll the brokers and servers and verify `channel keepAlive[timeMs=30000, timeoutMs=30000, ...]` in the `Initialized MailboxService` log. Interval plus timeout gives an approximate 60-second detection window when pings are active, not a guaranteed recovery deadline.
3. Optionally set `pinot.query.runner.channel.keep.alive.without.calls=true` and roll again, once all peers permit it.

Leave room between the server permit and client interval for scheduling jitter. Short timeouts can mistake a long garbage-collection pause for a failed peer and terminate healthy in-flight queries. Prefer lowering the interval before reducing the timeout.

`too_many_pings` or `GOAWAY(ENHANCE_YOUR_CALM)` indicates rejected pings: check every peer's permitted interval and idle-ping policy, and restore compatible client settings. `UNAVAILABLE: Keepalive failed` against a healthy peer can indicate an overly short timeout.
