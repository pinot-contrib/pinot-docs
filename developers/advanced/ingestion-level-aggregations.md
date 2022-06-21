# Ingestion Aggregations

Many data analytics use-cases only need aggregated data. For example, data used in charts can be aggregated down to one row per time bucket per dimension combination. 

Doing this results in much less storage and better query performance. Configuring this for a table is done via the Aggregation Config in the [table config](../../configuration-reference/table.md).

## Aggregation Config

The aggregation config controls the aggregations that happen during realtime data ingestion. Offline aggregations must be handled separately. 

Below is a description of the config, which is defined in the ingestion config of the table config. 

```json
{
  "tableConfig": {
    "tableName": "...",
    "ingestionConfig": {
      "aggregationConfigs": [{
        "columeName": "aggregatedFieldName",
        "aggregationFunction": "<aggregationFunction>(<originalFieldName>)"
      }]
    }
  }
}
```

## Example Scenario
Here is an example of sales data, where only the daily sales aggregates per product are needed. 

### Example Input Data

```json
{"customerID":205,"product_name": "car","price":"1500.00","timestamp":1571900400000}
{"customerID":206,"product_name": "truck","price":"2200.00","timestamp":1571900400000}
{"customerID":207,"product_name": "car","price":"1300.00","timestamp":1571900400000}
{"customerID":208,"product_name": "truck","price":"700.00","timestamp":1572418800000}
{"customerID":209,"product_name": "car","price":"1100.00","timestamp":1572505200000}
{"customerID":210,"product_name": "car","price":"2100.00","timestamp":1572505200000}
{"customerID":211,"product_name": "truck","price":"800.00","timestamp":1572678000000}
{"customerID":212,"product_name": "car","price":"800.00","timestamp":1572678000000}
{"customerID":213,"product_name": "car","price":"1900.00","timestamp":1572678000000}
{"customerID":214,"product_name": "car","price":"1000.00","timestamp":1572678000000}
```

### Schema
Note that the schema only reflects the final table structure.

```json
{
  "schemaName": "daily_sales_schema",
  "dimensionFieldSpecs": [
    {
      "name": "product_name",
      "dataType": "STRING"
    }
  ],
  "metricSpecs": [
    {
      "name": "sales_count",
      "dataType": "LONG"
    },
    {
      "name": "total_sales",
      "dataType": "DOUBLE"
    }
  ],
  "dateTimeFieldSpecs": [
    {
      "name": "daysSinceEpoch",
      "dataType": "LONG",
      "format": "1:MILLISECONDS:EPOCH",
      "granularity": "1:MILLISECONDS"
    }
  ]
}
```

### Table Config

```json
{
  "tableName": "daily_sales",
  "ingestionConfig": {
    "transformConfigs": [
      {
        "columnName": "daysSinceEpoch",
        "transformFunction": "toEpochDays(timestamp)"
      }
    ],
    "aggregationConfigs": [
      {
        "columnName": "total_sales",
        "aggregationFunction": "SUM(price)"
      },
      {
        "columnName": "sales_count", 
        "aggregationFunction": "COUNT(*)"
      }
    ]
  }
}
```

### Example Final Table

| product_name | sales_count | total_sales | daysSinceEpoch | 
|--------------|-------------|-------------|----------------|
| car          | 2           | 2800.00     | 18193          |
| truck        | 1           | 2200.00     | 18193          |
| truck        | 1           | 700.00      | 18199          |
| car          | 2           | 3300.00     | 18200          |
| truck        | 1           | 800.00      | 18202          |
| car          | 3           | 3700.00     | 18202          |

## Requirements
The following are required for ingestion aggregation to work: 
- [Stream ingestion](../../basics/data-import/pinot-stream-ingestion) type must be lowLevel.
- All metrics must have aggregation configs.
- All metrics must be noDictionaryColumns.

## Allowed Aggregation Functions

| function name | notes | 
| ----------| ------|
| MAX | | 
| MIN| | 
|SUM | |
|COUNT| Specify as `COUNT(*)`| 
| DISTINCTCOUNTHLL| Not available yet, but coming soon| 


## Frequently Asked Questions

### Why not use a Startree? 
Startrees can only be added to realtime segments after the segments has sealed, and creating startrees is CPU-intensive. Ingestion Aggregation works for consuming segments and uses no additional CPU. 

Startrees take additional memory to store, while ingestion aggregation stores less data than the original dataset. 

### When to not use ingestion aggregation? 
If the original rows in non-aggregated form are needed, then ingestion-aggregation cannot be used. 

### I already use the `aggregateMetrics` setting? 
The `aggregateMetrics` works the same as Ingestion Aggregation, but only allows for the SUM function. 

The current changes are backward compatible, so no need to change your table config unless you need a different aggregation function. 

### Does this config work for offline data?

Ingestion Aggregation only works for realtime ingestion. For offline data, the offline process needs to generate the
aggregates separately.

### Why do all metrics need to be aggregated?

If a metric isn't aggregated then it will result in more than one row per unique set of dimensions.



