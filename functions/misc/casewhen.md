---
description: This section contains reference documentation for the caseWhen function.
---

# caseWhen

Returns values depending on boolean expressions. This function can only be used in an [ingestion transformation function](../../developers/advanced/ingestion-level-transformations.md).

## Signature

> caseWhen(booleanExpr1, valueIfExpr1True, booleanExpr2, valueIfExpr2True) caseWhen(booleanExpr1, valueIfExpr1True, booleanExpr2, valueIfExpr2True, ... ,valueIfFalse)

<table>
  <thead>
    <tr>
      <th>Arguments</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`booleanExpr1`</td>
      <td>A boolean expression</td>
    </tr>
    <tr>
      <td>`valueIfExpr1True`, `valueIfExpr2True`</td>
      <td>A value to return.</td>
    </tr>
  </tbody>
</table>

## Usage Examples

The usage examples are based on extracting fields from the following JSON documents:

```json
{
  "latitude": 1.0
}
```

<table>
  <thead>
    <tr>
      <th>Expression</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`CASEWHEN(latitude > 0, 'North', 'South')`</td>
      <td>`North`</td>
    </tr>
    <tr>
      <td>`CASEWHEN(latitude > 0, 1, 0)`</td>
      <td>`1`</td>
    </tr>
  </tbody>
</table>

This function can be used in the [table config](../../configuration-reference/table.md) to add `northernHemisphere` column:

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
