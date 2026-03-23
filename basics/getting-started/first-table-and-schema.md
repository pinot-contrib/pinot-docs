---
description: Create your first Pinot schema and table, ready for data ingestion.
---

# First table and schema

## Outcome

By the end of this page you will have a Pinot schema and an offline table called `transcript` registered in your cluster, ready to receive data.

## Prerequisites

* A running Pinot cluster. See the install guides for [Local](install/local.md) or [Docker](install/docker.md).
* For Docker users: the cluster must be on the `pinot-demo` network.
* Confirm your Pinot version. See the [Version reference](pinot-versions.md) page and set the `PINOT_VERSION` environment variable:

```bash
export PINOT_VERSION=<your-pinot-version>
```

## Steps

### 1. Understand schemas

A Pinot schema defines every column in your table and assigns each one a column type. There are three column types:

| Column type | Description |
| --- | --- |
| Dimension | Used in filters and GROUP BY clauses for slicing and dicing data. |
| Metric | Used in aggregations; represents quantitative measurements. |
| DateTime | Represents the timestamp associated with each row. |

Every table must have a schema before it can accept data. The schema tells Pinot how to interpret, index, and store each field.

### 2. Create the data directory

```bash
mkdir -p /tmp/pinot-quick-start/rawdata
```

### 3. Save the sample CSV data

Create the file `/tmp/pinot-quick-start/rawdata/transcript.csv` with the following contents:

{% code title="/tmp/pinot-quick-start/rawdata/transcript.csv" %}
```
studentID,firstName,lastName,gender,subject,score,timestampInEpoch
200,Lucy,Smith,Female,Maths,3.8,1570863600000
200,Lucy,Smith,Female,English,3.5,1571036400000
201,Bob,King,Male,Maths,3.2,1571900400000
202,Nick,Young,Male,Physics,3.6,1572418800000
```
{% endcode %}

In this dataset, `studentID`, `firstName`, `lastName`, `gender`, and `subject` are dimensions, `score` is a metric, and `timestampInEpoch` is the datetime column.

### 4. Save the schema

Create the file `/tmp/pinot-quick-start/transcript-schema.json`:

{% code title="/tmp/pinot-quick-start/transcript-schema.json" %}
```json
{
  "schemaName": "transcript",
  "dimensionFieldSpecs": [
    { "name": "studentID", "dataType": "INT" },
    { "name": "firstName", "dataType": "STRING" },
    { "name": "lastName", "dataType": "STRING" },
    { "name": "gender", "dataType": "STRING" },
    { "name": "subject", "dataType": "STRING" }
  ],
  "metricFieldSpecs": [
    { "name": "score", "dataType": "FLOAT" }
  ],
  "dateTimeFieldSpecs": [{
    "name": "timestampInEpoch",
    "dataType": "LONG",
    "format": "1:MILLISECONDS:EPOCH",
    "granularity": "1:MILLISECONDS"
  }]
}
```
{% endcode %}

### 5. Understand table configs

A table config tells Pinot how to manage the table at runtime -- which columns to index, how many replicas to keep, which tenants to assign, and whether the table is OFFLINE (batch) or REALTIME (streaming). You pair one table config with one schema.

### 6. Save the offline table config

Create the file `/tmp/pinot-quick-start/transcript-table-offline.json`:

{% code title="/tmp/pinot-quick-start/transcript-table-offline.json" %}
```json
{
  "tableName": "transcript",
  "segmentsConfig": {
    "timeColumnName": "timestampInEpoch",
    "timeType": "MILLISECONDS",
    "replication": "1",
    "schemaName": "transcript"
  },
  "tableIndexConfig": {
    "invertedIndexColumns": [],
    "loadMode": "MMAP"
  },
  "tenants": {
    "broker": "DefaultTenant",
    "server": "DefaultTenant"
  },
  "tableType": "OFFLINE",
  "metadata": {}
}
```
{% endcode %}

### 7. Upload the schema and table config

{% tabs %}
{% tab title="Local" %}
```bash
bin/pinot-admin.sh AddTable \
  -tableConfigFile /tmp/pinot-quick-start/transcript-table-offline.json \
  -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
  -exec
```
{% endtab %}

{% tab title="Docker" %}
```bash
docker run --rm -ti \
    --network=pinot-demo \
    -v /tmp/pinot-quick-start:/tmp/pinot-quick-start \
    --name pinot-table-creation \
    apachepinot/pinot:${PINOT_VERSION} AddTable \
    -schemaFile /tmp/pinot-quick-start/transcript-schema.json \
    -tableConfigFile /tmp/pinot-quick-start/transcript-table-offline.json \
    -controllerHost pinot-controller \
    -controllerPort 9000 \
    -exec
```

{% hint style="info" %}
Replace `pinot-controller` with the actual container name of your Pinot controller if you used a different name during setup.
{% endhint %}
{% endtab %}
{% endtabs %}

## Verify

1. Open the Pinot Data Explorer at [http://localhost:9000](http://localhost:9000).
2. Navigate to the **Tables** tab.
3. Confirm you see `transcript_OFFLINE` listed.

If the table appears, the schema and table config were registered successfully.

## Next step

You now have an empty table. Continue to [First batch ingest](first-batch-ingest.md) to import the CSV data into your `transcript` table.
