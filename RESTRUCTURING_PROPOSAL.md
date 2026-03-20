# Apache Pinot Documentation Restructuring Proposal

> **Status:** Proposal  
> **Date:** 2026-03-20  
> **Related PRs:** #511 (SUMMARY.md restructure), #513 (missing feature docs)

## Executive Summary

This document proposes a phased restructuring of the Apache Pinot documentation based on an analysis of the current docs, a cross-check against the `apache/pinot` source code, and a review of documentation patterns used by comparable database projects (ClickHouse, CockroachDB, Apache Druid, StarRocks, DuckDB).

The goal is to make Pinot documentation easier to navigate, reduce content fragmentation, and close documentation gaps for features that exist in source code but lack user-facing docs.

---

## 1. Problems Identified

### 1.1 Navigation & Information Architecture

| Problem | Details |
|---------|---------|
| **Getting Started is buried** | Currently nested under `Basics`, requiring 2 clicks to reach. Every comparable database puts this at the top level. |
| **Audience-based splits are confusing** | `For Users`, `For Developers`, `For Operators` creates artificial boundaries. Users looking for ingestion docs must check both `Manage Data` AND `Developers > Advanced`. |
| **Indexing hidden under "Basics"** | Indexing is an advanced, differentiating feature for Pinot. Druid, ClickHouse, and StarRocks all give equivalent features top-level visibility. |
| **Security docs scattered** | Authentication is in `Operators > Tutorials > Authentication`, TLS is in `Operators > Tutorials`, and access control is in `Operators > Deployment`. Three different locations for related content. |
| **Monitoring docs fragmented** | Core monitoring is in `Operators > Deployment`, Prometheus/Grafana tutorial is in `Operators > Tutorials`. Should be one section. |
| **Release notes buried under Basics** | Release notes are under `Basics > Release Notes`. Every comparable database has release info at the top level or in a dedicated section. |
| **Ingestion docs split across sections** | Overview in `Developers > Advanced`, implementation in `Manage Data`, transformations in `Developers > Advanced`. |

### 1.2 Documentation Gaps (Cross-Checked Against Source Code)

| Feature | Source Code Location | Doc Status |
|---------|---------------------|------------|
| **Kafka 4.0 connector** | `pinot-plugins/pinot-stream-ingestion/pinot-kafka-4.0/` | **Not documented** (Fixed in PR #513) |
| **Segment pruning strategies** | `pinot-broker/.../routing/segmentpruner/` | No dedicated docs (Fixed in PR #513) |
| **M3QL timeseries language** | `pinot-plugins/pinot-timeseries-lang/pinot-timeseries-m3ql/` | Partial — plugin dev guide exists but no M3QL syntax reference |
| **Flink streaming connector** | `pinot-connectors/pinot-flink-connector/` | Only batch ingestion documented; streaming use case missing |
| **Deprecated kafka20 references** | `kafka20` plugin removed from source | 12 references in docs (Fixed in PR #513) |

### 1.3 Content Quality Issues

| Issue | Details |
|-------|---------|
| **`functions-1/` directory naming** | 186 function reference files in a directory named `functions-1` (likely a GitBook naming collision). Should be renamed to `function-reference/`. |
| **Duplicate function directories** | Both `functions/` (19 files, category overviews) and `functions-1/` (186 files, individual functions) exist. Confusing structure. |
| **Inconsistent casing** | Mix of title case and sentence case in SUMMARY.md entries |
| **Statistical functions misplaced** | `VAR_POP`, `VAR_SAMP`, `STDDEV_POP`, `STDDEV_SAMP` are in `Configuration Reference > Plugin Reference` instead of `Functions` |
| **Outdated Docker images** | Kafka docs reference `wurstmeister/kafka:latest` which is unmaintained |

---

## 2. Proposed Structure

The new structure follows **task-based organization** (what users want to DO) rather than audience-based organization (who the user IS). This pattern is used by ClickHouse, CockroachDB, DuckDB, and StarRocks.

```
Getting Started              ← First thing users see (promoted from Basics)
  ├── Running Pinot locally
  ├── Running in Docker
  ├── Quick Start Examples
  ├── Running in Kubernetes
  ├── Running on Public Clouds
  ├── FAQs
  └── Recipes

Architecture & Concepts      ← Renamed from "Basics" (which was misleading)
  ├── Concepts / Storage Model
  ├── Components (Cluster, Table, Schema, Segment...)
  ├── Single-Stage Query Engine (v1)
  └── Multi-Stage Query Engine (v2)

Data Ingestion               ← Consolidated from "Manage Data" + "Developers > Advanced"
  ├── Overview
  ├── Batch Ingestion (Spark, Flink, Hadoop)
  ├── Stream Ingestion (Kafka, Kinesis, Pulsar)
  ├── Kafka Connector Versions   ← NEW
  ├── Upsert and Dedup
  ├── Supported Data Formats
  ├── File Systems
  ├── Ingestion Transformations  ← Moved from Developers > Advanced
  └── Ingestion Aggregations     ← Moved from Developers > Advanced

Querying Data                ← Extracted from "For Users > Query"
  ├── Query Syntax
  ├── Multi-Stage Query Engine
  ├── Time Series Queries
  ├── Query Options / Quotas / Cancellation / Cursors
  └── Null Value Support        ← Moved from Developers > Advanced

Indexing                     ← Promoted from "Basics > Indexing"
  ├── All index types (Bloom, Dictionary, Forward, FST, Geospatial,
  │   Inverted, JSON, Native Text, Range, Star-Tree, Text, Timestamp, Vector)

APIs & Clients               ← Extracted from "For Users"
  ├── Broker Query API / gRPC API
  ├── Controller Admin API
  └── Client Libraries (JDBC, Java, Python, Go)

Operations                   ← Reorganized from flat "For Operators"
  ├── Deployment (Cluster, Table, Ingestion setup)
  ├── Segment Management (Assignment, Rebalance, Tiered Storage)
  ├── Security (Auth + TLS consolidated)
  ├── Monitoring (Core + Prometheus/Grafana consolidated)
  ├── Performance Tuning (Tuning + OOM + Throttling + Segment Pruning)
  ├── Segment Pruning           ← NEW
  ├── Kubernetes Deployment
  └── Upgrading / Logs / CLI

Configuration Reference      ← Cleaned up
  ├── Cluster / ZK / Controller / Broker / Server / Table / Schema
  ├── Ingestion / Job Spec / Monitoring Metrics
  └── Plugin Reference (statistical functions moved to Functions)

Functions                    ← Statistical functions moved here
  ├── Category overviews (Aggregation, Transformation, Array, etc.)
  ├── Statistical Functions     ← Moved from Config Reference
  ├── Window Functions
  └── Function List (A-Z reference)

Integrations                 ← Unchanged
Development                  ← Renamed from "For Developers"
Tutorials                    ← Consolidated from scattered tutorials
Reference / Troubleshooting
Release Notes                ← Promoted to top-level
Resources / Community
Contributing
```

---

## 3. Implementation Plan

### Phase 1: Navigation Restructure (PR #511)
**Effort:** Low | **Impact:** High | **Risk:** Low

- Restructure `SUMMARY.md` only
- No file moves — all existing file paths preserved
- Validates that the new navigation makes sense before doing heavier work

### Phase 2: Missing Feature Documentation (PR #513)
**Effort:** Medium | **Impact:** High | **Risk:** Low

- Add Kafka 4.0 connector documentation
- Add segment pruning guide
- Fix deprecated kafka20 references

### Phase 3: Directory Cleanup (Future PR)
**Effort:** Medium | **Impact:** Medium | **Risk:** Medium

- Rename `functions-1/` → `function-reference/`
- Move statistical function pages from `configuration-reference/plugin-reference/` to `functions/`
- Update all internal cross-references
- Update `.gitbook.yaml` redirects

### Phase 4: Content Gap Closure (Future PRs)
**Effort:** High | **Impact:** High | **Risk:** Low

Suggested priorities:
1. M3QL timeseries language syntax reference
2. Flink streaming connector documentation
3. Updated Docker examples (replace unmaintained `wurstmeister/kafka`)
4. Production deployment best practices guide (similar to CockroachDB's)
5. Migration guide from other OLAP systems (similar to ClickHouse's)
6. "When to use Pinot" use cases page (similar to Druid's)

### Phase 5: Platform Migration Consideration (Future)
**Effort:** Very High | **Impact:** High | **Risk:** High

All comparable databases have moved away from GitBook:
- ClickHouse → Docusaurus
- Druid → Docusaurus
- StarRocks → Docusaurus
- DuckDB → Custom
- CockroachDB → Custom

Benefits of migration: versioned docs, better search, custom components, API reference auto-generation, community contribution workflow via GitHub PRs.

---

## 4. Benchmarking Summary

### What Top Database Docs Do Well

| Pattern | Used By | Applicable to Pinot |
|---------|---------|-------------------|
| Task-based nav (not audience-based) | ClickHouse, DuckDB, StarRocks | Yes — PR #511 |
| Getting Started as first section | All 5 databases | Yes — PR #511 |
| Dedicated Security section | CockroachDB, ClickHouse | Yes — PR #511 |
| Integration/Client libs prominent | DuckDB, ClickHouse | Yes — PR #511 |
| "When to use" / Use Cases page | Druid, StarRocks | Recommended |
| Migration guides from competitors | ClickHouse (from Snowflake, BigQuery, etc.) | Recommended |
| Versioned documentation | CockroachDB, StarRocks, DuckDB | Requires platform change |
| AI search assistant | StarRocks | Nice-to-have |
| Live demo / playground | DuckDB | Nice-to-have |

---

## 5. Validation

All proposed changes were validated by:
1. **Source code cross-check** — Cloned `apache/pinot` and verified feature existence, class names, configuration properties
2. **Link validation** — All SUMMARY.md entries reference existing files
3. **Completeness check** — Every page in the original SUMMARY.md appears in the restructured version
4. **Competitive analysis** — Reviewed 5 comparable database documentation sites
