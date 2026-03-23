---
description: Run a complete Pinot cluster with sample data in under 10 minutes.
---

# Ten-minute quickstart

## Outcome

By the end of this guide you will have a fully functional Apache Pinot cluster running locally with sample data loaded, ready to query.

## Prerequisites

* [Docker](https://docs.docker.com/get-docker/) installed and running
* Recommended resources: 8 CPUs, 16 GB RAM

## Steps

**1. Set the Pinot version**

```bash
export PINOT_VERSION=1.4.0
```

See the [Version reference](pinot-versions.md) page for the current stable release.

**2. Start Pinot with sample data**

```bash
docker run \
    -p 2123:2123 \
    -p 9000:9000 \
    -p 8000:8000 \
    -p 7050:7050 \
    -p 6000:6000 \
    apachepinot/pinot:${PINOT_VERSION} QuickStart \
    -type batch
```

This single command starts ZooKeeper, Controller, Broker, Server, and Minion, then loads a baseball statistics dataset.

## Verify

1. Open the Pinot Query Console at [http://localhost:9000](http://localhost:9000).
2. Run a sample query:

```sql
SELECT playerName, sum(runs) AS totalRuns
FROM baseballStats
GROUP BY playerName
ORDER BY totalRuns DESC
LIMIT 10
```

You should see results returned within milliseconds.

## Next step

This quickstart bundles everything in a single process for convenience. For a list of all available quickstart types (batch, streaming, hybrid, and more), see [Quick Start Examples](quick-start.md).

Ready for a production-style setup? Continue to [Install / deploy](install/).
