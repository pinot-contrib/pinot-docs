---
description: >-
  Create and edit a table configuration in the Pinot UI or with the API.
---

# Create and update an Apache Pinot table configuration

In Apache Pinot, create a table by creating a JSON file, generally referred to as your _table config_. Update, add, or delete parameters as needed, and then reload the file.

## Create a Pinot table configuration

Before you create a Pinot table configuration, you must first have a running Pinot cluster with broker and server tenants. 

1. Create a plaintext file locally using settings from [the available properties](https://docs.pinot.apache.org/configuration-reference/table) for your use case.

1. Use the Pinot API to upload your table config file:
  `POST @fileName.json URL:9000/tables`


<Callout>
    You may find it useful to download [an example from the Pinot GitHub](https://github.com/apache/pinot/tree/master/pinot-tools/src/main/resources/examples) and then modify it. An example from among these is included at the end of this page in [Example Pinot table config file](#example-pinot-table-config-file).
</Callout>

## Update a Pinot table configuration

To modify your Pinot table configuration, use the Pinot UI or the API.

<Callout type="tip">
    Any time you make a change to your table config, you may need to do one or more of the following, depending on the change.
</Callout>

Simple changes only require updating and saving your modified table configuration file. These include:

* Changing the data or segment retention time

* Changing the realtime [consumption rate limiter](https://docs.pinot.apache.org/basics/data-import/pinot-stream-ingestion#throttle-stream-consumption) settings

To update existing data and segments, after you update and save the changes to the table config file, do the following as applicable:

**When you add or modify indexes or the table schema**, perform a [segment reload](https://docs.pinot.apache.org/basics/data-import/segment-reload). To [reload](https://docs.pinot.apache.org/basics/getting-started/frequent-questions/operations-faq#whats-the-difference-between-reset-refresh-and-reload) all segments:
* In the Pinot UI, from the table page, click **Reload All Segments**.
* Using the Pinot API, send `POST /segments/{tableName}/reload`.

**When you re-partition data**, perform a segment [refresh](https://docs.pinot.apache.org/basics/getting-started/frequent-questions/operations-faq#whats-the-difference-between-reset-refresh-and-reload). To refresh, replace an existing segment with a new one by uploading a segment reusing the existing filename.
* Using the Pinot API, send `POST /segments?tableName={yourTableName}`.
* Automate this action by including `SegmentRefreshTask` in your table configuration to make Pinot refresh segments if they are not consistent with the table configuration. See the [SegmentRefreshTask](../getting-started/table-config-file-usage.md) documentation for limitations to using this.

**When you change the transform function used to populate a derived field** or **increase the number of partitions in an upsert-enabled table**, perform a table re-bootstrap. One way to do this is to delete and recreate the table:
* Using the Pinot API, first send `DELETE /tables/{tableName}` followed by `POST /tables` with the new table configuration.

**When you change the stream topic** or **change the Kafka cluster** containing the Kafka topic you want to consume from, perform a real-time ingestion pause and resume. To pause and resume real-time ingestion:
* Using the Pinot API, first send `POST /tables/{tableName}/pauseConsumption` followed by `POST /tables/{tableName}/resumeConsumption`.

### Update a Pinot table in the UI

To update a table configuration in the Pinot UI, do the following:

1. In the **Cluster Manager** click the **Tenant Name** of the tenant that hosts the table you want to modify.

1. Click the **Table Name** in the list of tables in the tenant.

1. Click the **Edit Table** button. This creates a pop-up window containing the table configuration. Edit the contents in this window. Click **Save** when you are done.


### Update a Pinot table using the API

To update a table configuration using the Pinot API, do the following:

1. Get the current table configuration with `GET /tables/{tableName}`.

1. Modify the file locally.

1. Upload the edited file with `PUT /table/{tableName} fileName.json`.


## Example Pinot table configuration file

This example comes from the [Apache Pinot Quickstart Examples](https://docs.pinot.apache.org/basics/getting-started/quick-start). This table configuration defines a table called **airlineStats_OFFLINE**, which you can interact with by running the example.

```json
{
  "OFFLINE": {
    "tableName": "airlineStats_OFFLINE",
    "tableType": "OFFLINE",
    "segmentsConfig": {
      "timeType": "DAYS",
      "replication": "1",
      "segmentAssignmentStrategy": "BalanceNumSegmentAssignmentStrategy",
      "timeColumnName": "DaysSinceEpoch",
      "segmentPushType": "APPEND",
      "minimizeDataMovement": false
    },
    "tenants": {
      "broker": "DefaultTenant",
      "server": "DefaultTenant"
    },
    "tableIndexConfig": {
      "rangeIndexVersion": 2,
      "autoGeneratedInvertedIndex": false,
      "createInvertedIndexDuringSegmentGeneration": false,
      "loadMode": "MMAP",
      "enableDefaultStarTree": false,
      "starTreeIndexConfigs": [
        {
          "dimensionsSplitOrder": [
            "AirlineID",
            "Origin",
            "Dest"
          ],
          "skipStarNodeCreationForDimensions": [],
          "functionColumnPairs": [
            "COUNT__*",
            "MAX__ArrDelay"
          ],
          "maxLeafRecords": 10
        },
        {
          "dimensionsSplitOrder": [
            "Carrier",
            "CancellationCode",
            "Origin",
            "Dest"
          ],
          "skipStarNodeCreationForDimensions": [],
          "functionColumnPairs": [
            "MAX__CarrierDelay",
            "AVG__CarrierDelay"
          ],
          "maxLeafRecords": 10
        }
      ],
      "enableDynamicStarTreeCreation": true,
      "aggregateMetrics": false,
      "nullHandlingEnabled": false,
      "optimizeDictionary": false,
      "optimizeDictionaryForMetrics": false,
      "noDictionarySizeRatioThreshold": 0
    },
    "metadata": {
      "customConfigs": {}
    },
    "fieldConfigList": [
      {
        "name": "ts",
        "encodingType": "DICTIONARY",
        "indexType": "TIMESTAMP",
        "indexTypes": [
          "TIMESTAMP"
        ],
        "timestampConfig": {
          "granularities": [
            "DAY",
            "WEEK",
            "MONTH"
          ]
        }
      }
    ],
    "ingestionConfig": {
      "transformConfigs": [
        {
          "columnName": "ts",
          "transformFunction": "fromEpochDays(DaysSinceEpoch)"
        },
        {
          "columnName": "tsRaw",
          "transformFunction": "fromEpochDays(DaysSinceEpoch)"
        }
      ],
      "continueOnError": false,
      "rowTimeValueCheck": false,
      "segmentTimeValueCheck": true
    },
    "tierConfigs": [
      {
        "name": "hotTier",
        "segmentSelectorType": "time",
        "segmentAge": "3130d",
        "storageType": "pinot_server",
        "serverTag": "DefaultTenant_OFFLINE"
      },
      {
        "name": "coldTier",
        "segmentSelectorType": "time",
        "segmentAge": "3140d",
        "storageType": "pinot_server",
        "serverTag": "DefaultTenant_OFFLINE"
      }
    ],
    "isDimTable": false
  }
}
```