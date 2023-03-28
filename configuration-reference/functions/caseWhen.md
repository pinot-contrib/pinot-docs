---
description: This section contains reference documentation for the caseWhen function.
---

# caseWhen

Returns values depending on boolean expressions.
This function can only be used in an [ingestion transformation function](../../developers/advanced/ingestion-level-transformations.md).

## Signature

> JSONPATH(jsonField, 'jsonPath')
> caseWhen(booleanExpr1, valueIfTrue, valueIfFalse)
> caseWhen(booleanExpr1, valueIfExpr1True, booleanExpr2, valueIfExpr2True)
> caseWhen(booleanExpr1, valueIfExpr1True, booleanExpr2, valueIfExpr2True, ... ,valueIfFalse)

| Arguments    | Description                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------ |
| `booleanExpr1`  | A boolean expression                                              |
| `valueIfExpr1True`, `valueIfExpr2True` | A value to return. |

{% hint style="warning" %}
**`'jsonPath'`**\` is a literal. Pinot uses single quotes to distinguish them from **identifiers.** \
****\
****You can use the [Jayway JsonPath Evaluator Tool](https://jsonpath.herokuapp.com/) to test JSON expressions before you import any data.
{% endhint %}

## Usage Examples

The usage examples are based on extracting fields from the following JSON documents:

```json
{
  "latitude": 1.0
}
```

| Expression                 | Value    |
| -------------------------- | -------- |
| `CASEWHEN(latitude > 0, 'North', 'South')` | `North` |
| `CASEWHEN(latitude > 0, 1, 0)` | `1` |

This function can be used in the [table config](../table.md) to add `northernHemisphere` column:

```json
{
   "tableConfig":{
      "ingestionConfig":{
         "transformConfigs":[
            {
               "columnName":"northernHemisphereStr",
               "transformFunction":"CASEWHEN(latitude > 0, 'North', 'South')"
            }
         ]
      }
   }
}
```
