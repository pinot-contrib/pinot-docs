---
description: Choose batch ingestion when Pinot should load prebuilt data from files, warehouses, or distributed processing jobs.
---

# Batch Ingestion

Batch ingestion builds Pinot segments outside the cluster and pushes them into Pinot after the data is already shaped. Use it when the data changes in larger chunks, when you need deterministic backfills, or when the pipeline already produces files or segment artifacts.

The most important design choice is not the framework, but the output contract: what the schema looks like, what the table expects, and where the segments land.

## Common batch paths

Spark-based ingestion.

Hadoop-style distributed ingestion.

Backfill jobs for historical ranges. Pinot ships `LaunchBackfillIngestionJob` for the case where the backfilled input may have fewer files than the original ingestion — see [Backfill Data](batch-ingestion/backfill-data.md).

Dimension tables and other specialized offline loads.

## What to decide early

Decide on the file format, the deep-storage target, and the segment push workflow before you optimize the job itself. Most batch ingestion problems come from mismatched assumptions at those boundaries.

## Select input files

Use `includeFileNamePattern` and `excludeFileNamePattern` in the ingestion job spec to filter input paths. Both accept Java NIO `PathMatcher` patterns with either the `glob:` or `regex:` prefix:

```yaml
includeFileNamePattern: 'glob:**/*.avro'
excludeFileNamePattern: 'regex:.*[.]tmp'
```

The pattern must match the whole normalized path, not only the file name. See [File name patterns](../../reference/configuration-reference/job-specification.md#file-name-patterns) for Java regex syntax, job-spec template escaping, and URI normalization details.

## Learn more

The original step-by-step batch docs live in [Import Data](README.md) and [Data Ingestion Overview](README.md).

## What this page covered

This page covered when to choose batch ingestion and the main design decisions that shape it.

## Next step

Read [Stream Ingestion](stream-ingestion.md) if the source system is a live event stream.

## Related pages

- [Ingestion](README.md)
- [Stream Ingestion](stream-ingestion.md)
- [Formats and Filesystems](formats-filesystems.md)
- [Original Batch Docs](batch-ingestion/README.md)
