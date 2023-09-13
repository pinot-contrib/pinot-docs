---
description: Batch ingestion of backfill data into Apache Pinot.
---

# Backfill Data

## Introduction

Pinot batch ingestion involves two parts: routine ingestion job(hourly/daily) and backfill. Here are some examples to show how routine batch ingestion works in Pinot offline table:

* [Batch Ingestion Overview](https://docs.pinot.apache.org/basics/data-import/batch-ingestion)
* [Batch Ingestion in Practice](https://docs.pinot.apache.org/users/tutorials/batch-data-ingestion-in-practice)

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
