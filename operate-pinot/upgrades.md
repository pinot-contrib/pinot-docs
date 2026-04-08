# Upgrades

This section covers how to upgrade an Apache Pinot cluster safely, including the recommended rolling upgrade strategy, cross-release compatibility testing, and a per-release summary of behavior changes that operators must review before upgrading.

## Purpose

Pinot clusters run multiple independent components (controller, broker, server, minion) that can temporarily be at different versions during a rolling upgrade. A disciplined upgrade process ensures correctness of queries, ingestion, and segment management throughout the transition -- and allows a clean rollback if problems arise.

## When to use

Consult these guides when you are:

* Upgrading Pinot to a new minor or patch release.
* Planning a rollback strategy before applying an upgrade.
* Running the compatibility test suite to validate an upgrade in staging before production.
* Reviewing what changed between your current version and the target version.

## Upgrade strategy overview

### Recommended component order

Upgrade components in this order to minimize disruption. If you need to roll back, reverse the order.

1. **Pinot Controller** (and Helix Controller, if separate) -- Manages metadata and segment assignment; upgrading first ensures the newest controller handles segment operations during the rollout.
2. **Broker** -- Routes queries; a rolling restart briefly shifts traffic to remaining brokers.
3. **Server** -- Serves data; PodDisruptionBudgets ensure availability during rollout.
4. **Minion** -- Runs background tasks with no live query traffic; upgrading last avoids interference with the critical-path components above.

### Rolling upgrade mechanics

Pinot uses Kubernetes StatefulSets with `RollingUpdate` strategy by default, which restarts pods one at a time. Key points:

* **Never upgrade all components simultaneously.** Stagger the rollouts so you can observe the effect of each component upgrade before proceeding.
* **Validate between steps.** After each component finishes its rollout, verify health endpoints, run smoke-test queries, and check ingestion lag before moving to the next component.
* **Back up ZooKeeper** before starting. Table configs, schemas, and segment metadata live in ZooKeeper. A backup lets you recover if the upgrade corrupts metadata.

### Helm-based upgrades

If you deploy with Helm, the upgrade workflow is:

```bash
# 1. Update the image tag in your values file
#    image.tag: "1.1.0"

# 2. Dry-run to review changes
helm upgrade pinot pinot/pinot -n pinot-quickstart -f values.yaml --dry-run --debug

# 3. Apply the upgrade
helm upgrade pinot pinot/pinot -n pinot-quickstart -f values.yaml

# 4. Monitor rollout
kubectl rollout status statefulset/pinot-controller -n pinot-quickstart
kubectl rollout status statefulset/pinot-broker -n pinot-quickstart
kubectl rollout status statefulset/pinot-server -n pinot-quickstart
```

To roll back if issues arise:

```bash
helm rollback pinot -n pinot-quickstart
```

For the full Helm upgrade procedure including pre-upgrade checklist, see the [Helm Chart Values Reference -- Upgrade Procedures](kubernetes/helm-chart-reference.md#upgrade-procedures).

### Compatibility testing

Pinot (since 0.8.0) ships a compatibility test suite that simulates a full upgrade and rollback cycle. It starts a cluster at your current version, upgrades each component one at a time, runs your queries and data operations between each step, then rolls back in reverse order.

Use this to catch incompatibilities before they reach production -- especially if you are skipping multiple releases or use non-default configurations.

For full instructions on running `checkoutAndBuild.sh` and `compCheck.sh`, see:

* [Upgrading Pinot with confidence](upgrading-pinot-cluster.md)

## Upgrade notes by release

Before every upgrade, review the upgrade notes for your target release. These document:

* **Behavior changes** -- New defaults, changed semantics, stricter validation.
* **Deprecations** -- Config fields or APIs being phased out.
* **Migration hazards** -- Changes that require operator action (schema enforcement, load mode changes, new resource controls).
* **New opt-in features** -- Capabilities that are safe to ignore but worth knowing about.

For the per-release breakdown, see:

* [Upgrade Notes](upgrade-notes.md)

## Prerequisites

* Access to the Pinot controller `/version` API to determine your current version.
* A staging or dev cluster to test the upgrade before production.
* A ZooKeeper backup (table configs, schemas, segment metadata).
* All tables in a healthy state with no ongoing rebalances.

## Validate

After upgrading, confirm the cluster is healthy:

1. **Health endpoints** -- All controller, broker, and server pods return 200 on `/health`.
2. **Query correctness** -- Run a representative set of queries and compare results to pre-upgrade baselines.
3. **Ingestion** -- Verify that real-time tables are consuming from streams and consuming segment lag is within bounds.
4. **Segment management** -- Confirm that no segments are in ERROR state and that scheduled tasks (merge/rollup, retention) are running.
