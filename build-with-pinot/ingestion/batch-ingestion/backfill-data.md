---
description: Batch ingestion of backfill data into Apache Pinot.
---

# Backfill Data

## Introduction

Pinot batch ingestion involves two parts: routine ingestion job(hourly/daily) and backfill. Here are some examples to show how routine batch ingestion works in Pinot offline table:

* [Batch Ingestion Overview](.)
* [Batch Ingestion in Practice](../../../tutorials/data-ingestion/batch-data-ingestion-in-practice.md)

**High-level description**

1. Organize raw data into buckets (eg: /var/pinot/airlineStats/rawdata/2014/01/01). Each bucket typically contains several files (eg: /var/pinot/airlineStats/rawdata/2014/01/01/airlineStats\_data\_2014-01-01\_0.avro)
2. Run a Pinot batch ingestion job, which points to a specific date folder like ‘/var/pinot/airlineStats/rawdata/2014/01/01’. The segment generation job will convert each such avro file into a Pinot segment for that day and give it a unique name.
3. Run Pinot segment push job to upload those segments with those uniques names via a Controller API

{% hint style="info" %}
**IMPORTANT**: The segment name is the unique identifier used to uniquely identify that segment in Pinot. If the controller gets an upload request for a segment with the same name - it will attempt to replace it with the new one.
{% endhint %}

This newly uploaded data can now be queried in Pinot. However, sometimes users will make changes to the raw data which need to be reflected in Pinot. This process is known as 'Backfill'.

## How to backfill data in Pinot

Pinot supports data modification only at the segment level, which means you must update entire segments for doing backfills. The high level idea is to repeat steps 2 (segment generation) and 3 (segment upload) mentioned above:

* Backfill jobs must run at the same granularity as the daily job. E.g., if you need to backfill data for 2014/01/01, specify that input folder for your backfill job (e.g.: ‘/var/pinot/airlineStats/rawdata/2014/01/01’)
* The backfill job will then generate segments with the same name as the original job (with the new data).
* When uploading those segments to Pinot, the controller will replace the old segments with the new ones (segment names act like primary keys within Pinot) one by one.


### Edge case example

Backfill jobs expect the same number of (or more) data files on the backfill date. So the segment generation job will create the same number of (or more) segments than the original run.

For example, assuming table airlineStats has 2 segments(airlineStats\_2014-01-01\_2014-01-01\_0, airlineStats\_2014-01-01\_2014-01-01\_1) on date 2014/01/01 and the backfill input directory contains only 1 input file. Then the segment generation job will create just one segment: airlineStats\_2014-01-01\_2014-01-01\_0. After the segment push job, only segment airlineStats\_2014-01-01\_2014-01-01\_0 got replaced and stale data in segment airlineStats\_2014-01-01\_2014-01-01\_1 are still there.

**If the raw data is modified in such a way that the original time bucket has fewer input files than the first ingestion run, backfill will fail.**

### Complete backfill with LaunchBackfillIngestionJob

To safely handle the case described above — where the backfill input may have fewer files than the original ingestion — Pinot ships a dedicated CLI command, `LaunchBackfillIngestionJob`. Instead of relying on segment-name collision to replace stale data, it uses Pinot's segment-lineage machinery to atomically replace the existing segments in a date range with the newly generated ones. See [Consistent Data Push and Rollback](../../../operate-pinot/consistent-push-and-rollback.md) for the underlying lineage semantics.

#### How it works

`LaunchBackfillIngestionJob` reuses the same `ingestionJobSpec.yaml` as `LaunchDataIngestionJob` and runs in four steps:

| Step | Description |
|------|-------------|
| 1. Fetch existing segments | Calls the controller's `selectSegments` API to list every OFFLINE-table segment that overlaps `[startDate, endDate)`. These are the segments that will be replaced. |
| 2. Generate new segments | Runs a local `SegmentCreation` pass over the input directory. The segment-name generator is forced to `simple` with a unique `_<currentTimeMs>` postfix, so newly generated segment names never collide with the existing ones (and the lineage replace can therefore reference both sets unambiguously). |
| 3. Create a lineage entry | Calls `startReplaceSegments` with `segmentsFrom = <existing>` and `segmentsTo = <newly generated>`. The old segments continue to serve queries until the lineage entry is finalized. |
| 4. Push and finalize | Uploads the new segments via `SegmentTarPush`, then calls `endReplaceSegments`, which atomically switches brokers onto the new segment set and retires the old one. If the push fails, the lineage entry is rolled back and any partially uploaded segments are cleaned up. |

Because the old segment set is recorded explicitly in step 3 — rather than inferred from name collisions — the failure mode described in [Edge case example](#edge-case-example), where a shrunken backfill input leaves stale segments behind, cannot occur.

`LaunchBackfillIngestionJob` currently supports **OFFLINE tables only**.

#### Running the command

```bash
bin/pinot-admin.sh LaunchBackfillIngestionJob \
    -jobSpecFile /path/to/ingestionJobSpec.yaml \
    -startDate 2014-01-01 \
    -endDate 2014-01-02
```

| Option | Required | Description |
|--------|----------|-------------|
| `-jobSpecFile` | yes | Same job-spec YAML used by `LaunchDataIngestionJob`. |
| `-startDate` | yes | Backfill start date, **inclusive**. Format `yyyy-MM-dd`, parsed as **UTC**. |
| `-endDate` | yes | Backfill end date, **exclusive**. Format `yyyy-MM-dd`, parsed as **UTC**. |
| `-partitionColumn` | no | Column on which segments were partitioned via `BoundedColumnValue`. Used together with `-partitionColumnValue` to scope which segments are replaced. |
| `-partitionColumnValue` | no | Only segments whose `BoundedColumnValue` partition contains this value are eligible for replacement. |

All authentication options inherited from `LaunchDataIngestionJob` (`-authToken`, `-user`, `-password`, `-authProvider`, `-authTokenUrl`) are supported.

{% hint style="info" %}
Because dates are parsed as UTC day boundaries, callers in non-UTC time zones should account for the offset when building `-startDate` / `-endDate`. A "January 1st" backfill local to `America/Los_Angeles`, for example, spans `2014-01-01T08:00Z` to `2014-01-02T08:00Z`, which does not align with the UTC-day boundaries the command uses.
{% endhint %}

#### Filtering by partition column

For tables whose offline segments are partitioned by `BoundedColumnValue`, the backfill can be scoped to a subset of partitions using `-partitionColumn` and `-partitionColumnValue`:

```bash
bin/pinot-admin.sh LaunchBackfillIngestionJob \
    -jobSpecFile /path/to/ingestionJobSpec.yaml \
    -startDate 2014-01-01 \
    -endDate 2014-01-02 \
    -partitionColumn region \
    -partitionColumnValue us-east-1
```

The command computes the partition ID for `us-east-1` using the column's recorded partition function, then keeps only segments whose partition metadata contains that ID. Segments with no `BoundedColumnValue` partition metadata, or those covering more than one partition, are skipped.
