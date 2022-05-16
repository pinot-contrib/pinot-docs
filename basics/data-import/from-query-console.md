# From Query Console

## Insert a file into Pinot from Query Console

{% hint style="info" %}
This feature is supported after the 0.11.0 release. Reference PR: [https://github.com/apache/pinot/pull/8557](https://github.com/apache/pinot/pull/8557)
{% endhint %}

### How it works

1. Parse the query with the table name and directory URI along with a list of options for the ingestion job.
2. Call controller minion task execution API endpoint to schedule the task on minion
3. Response has the schema of table name and task job id.

### Usage Syntax

> INSERT INTO \[database.]table FROM FILE dataDirURI OPTION ( k=v ) \[, OPTION (k=v)]\*

### Example

```
INSERT INTO "baseballStats"
FROM FILE 's3://my-bucket/public_data_set/baseballStats/rawdata/'
OPTION(taskName=myTask-s3)
OPTION(input.fs.className=org.apache.pinot.plugin.filesystem.S3PinotFS)
OPTION(input.fs.prop.accessKey=my-key)
OPTION(input.fs.prop.secretKey=my-secret)
OPTION(input.fs.prop.region=us-west-2)
```

Screenshot

![](<../../.gitbook/assets/image (13).png>)

## Insert Rows into Pinot

&#x20;We are actively developing this feature...

The details will be revealed soon.
