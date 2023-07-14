# Server Startup Status Checkers

## Overview

When operating Pinot in a production environment, it's not always desirable to have servers immediately available for querying when they have started up. This is especially so for real-time servers that may have to re-consume some amount of data before they are "caught up". Pinot offers several strategies for determining when a server is up, healthy, and available for querying.

### Health Checks

Pinot servers have several endpoints for determining the health of the servers.

`GET /health/liveness` answers "is this server up." This only ensures that the server was able to start, and you can connect to it.

`GET /health/readiness` answers "is this server up and ready to server data." The checkers below determine if the "readiness" aspect returns `OK`.

`GET /health` performs the same check as the readiness endpoint.

## No Consuming Status Check (Default Behavior)

It's possible to operate Pinot with no checkers at all by disabling the following configurations, but this is not recommended. Instead, the defaults here are the following:

```
# this is the default, 10 minutes.
pinot.server.startup.timeoutMs=600000
# this is the default. you do not have to specify this.
pinot.server.startup.enableServiceStatusCheck=true
```

Pinot will wait up to 10 minutes for all server startup operations to complete. This will wait for the server's Ideal State to match its External State before marking the server as healthy. This could be mean downloading segments, building indices, and creating consumption streams. It is recommended to start with the default time and add more time as needed.

Waiting for Ideal State to match External State is not configurable. If `enableServiceStatusCheck=true`, this will always be one of the checks.

## Static Consumption Wait

The most basic startup check is the static one. It is configured by the following:

```
# this is the default, 10 minutes.
pinot.server.startup.timeoutMs=600000
# this is the default. you do not have to specify this.
pinot.server.startup.enableServiceStatusCheck=true
# the default is 0, and the server will not wait
pinot.server.starter.realtimeConsumptionCatchupWaitMs=60000
```

In the above example, a Pinot server will wait 60 seconds for all consuming segments before becoming healthy and available for serving queries. This gives the servers 1 minute to consume data un-throttled before being marked as healthy. Overall, the server will still only wait 10 minutes for all startup actions to complete. So make sure `realtimeConsumptionCatchupWaitMs` < `timeoutMs`.

## Offset Based Segment Checker

The first option to determine fresher real-time data is the offset based status checker. This checker will determine the end offset of each consuming segment at the time of Pinot startup. It will then consume to that offset before marking the segment as healthy. Once all segments are healthy, this checker will return healthy.

```
# this is the default, 10 minutes.
pinot.server.startup.timeoutMs=600000
# this is the default. you do not have to specify this.
pinot.server.startup.enableServiceStatusCheck=true
# the default is 0, and the server will not wait
pinot.server.starter.realtimeConsumptionCatchupWaitMs=60000
# this is disabled by default.
pinot.server.starter.enableRealtimeOffsetBasedConsumptionStatusChecker=true
```

There are some caveats to note here:

* `realtimeConsumptionCatchupWaitMs` must still be set. This checker will only wait as long as the value for `realtimeConsumptionCatchupWaitMs`.
* This checker will not ever recompute end offsets after it starts. With high real-time volume, you will still be behind. This means if your server takes 8 minutes to startup and have this checker become healthy, you will be 8 minutes behind and rapidly consuming data once the server starts serving queries.

## Freshness Based Segment Checker&#x20;

The strictest checker Pinot offers is the freshness based one. This works similarly to the offset checker but with an extra condition. The actual events in that stream must meet a minimum freshness before the server is marked as healthy. This checker provides the best freshness guarantees for real-time data at the expense of longer startup time.

```
# this is the default, 10 minutes.
pinot.server.startup.timeoutMs=600000
# this is the default. you do not have to specify this.
pinot.server.startup.enableServiceStatusCheck=true
# the default is 0, and the server will not wait
pinot.server.starter.realtimeConsumptionCatchupWaitMs=60000
# this is disabled by default.
pinot.server.starter.enableRealtimeOffsetBasedConsumptionStatusChecker=true
# the default is 10000. Values <=0 are not allowed.
pinot.server.starter.realtimeConsumptionCatchupWaitMs=10000
```

In the example above, the Pinot server will wait up to 1 minute for all consuming streams to have data within 10 seconds of the current system time. This is reevaluated for each pass of the checker, so this checker gives the best guarantee of having fresh data when before a server starts. This checker also checks the current offset a segment is at compared to the max offset of the stream, and it will mark the segment as healthy when those are equal. This is useful when you have a low volume stream where there may never be data fresher than `realtimeConsumptionCatchupWaitMs`.

There are still some caveats that apply here:

* `realtimeConsumptionCatchupWaitMs` must still be set. This checker will only wait as long as the value for `realtimeConsumptionCatchupWaitMs`.
* your events must implement `getMetadataAtIndex` to pass the event timestamp correctly. The current kafka, kinesis, and pulsar implementations already do this using the event ingestion time. But if your data takes multiple hops, it will only count the freshness from the last hop.
