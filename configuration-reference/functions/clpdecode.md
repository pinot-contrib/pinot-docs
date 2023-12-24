---
description: This section contains reference documentation for the CLPDECODE function.
---

# CLPDECODE

Reconstructs (decodes) the value of a CLP-encoded field from its component columns.

The [CLPLogMessageDecoder](../../basics/data-import/clp.md) can encode fields into a set of three columns:

* `<field>_logtype`
* `<field>_dictionaryVars`
* `<field>_encodedVars`

where `<field>` is the field's name before encoding. We refer to such a set of columns as a column group.

## Signatures

> CLPDECODE(colGroupName)
> 
> CLPDECODE(colGroupName, defaultValue)
> 
> CLPDECODE(colGroupName_logtype, colGroupName_dictionaryVars, colGroupName_encodedVars)
> 
> CLPDECODE(colGroupName_logtype, colGroupName_dictionaryVars, colGroupName_encodedVars, defaultValue)

* The syntax lets you specify the name of a column group or all columns within the column group.
  * To use the syntax where you only specify the column group's name, you need to enable an additional query-rewriter as described [below](#enable-the-column-group-syntax).   
* `defaultValue` is optional and used when a column group can't be decoded for some reason (e.g., it's null).

## Usage Examples

Consider a record that contains a "message" field with the following value:

> INFO Task task_12 assigned to container: [ContainerID:container_15], operation took 0.335 seconds. 8 tasks remaining.

[CLPLogMessageDecoder](../../basics/data-import/clp.md) encodes this information into 3 columns:

| message_logtype                                                                                              | message_dictionaryVars      | message_encodedVars     |
|--------------------------------------------------------------------------------------------------------------|-----------------------------|-------------------------|
| INFO Task \x12 assigned to container: [ContainerID:\x12], operation took \x13 seconds. \x11 tasks remaining. | ["task_12", "container_15"] | [0x190000000000014f, 8] |

Then we can use `CLPDECODE` as follows:

```sql
SELECT CLPDECODE(message) AS message
FROM myTable
```

| message                                                                                                               |
|-----------------------------------------------------------------------------------------------------------------------|
| INFO Task task_12 assigned to container: [ContainerID:container_15], operation took 0.335 seconds. 8 tasks remaining. |

# Enable the column-group syntax

To use the `CLPDECODE` syntax that only specifies the column group name, you must configure the Pinot broker with an additional query rewriter as follows:

```properties
pinot.broker.query.rewriter.class.names=org.apache.pinot.sql.parsers.rewriter.CompileTimeFunctionsInvoker,org.apache.pinot.sql.parsers.rewriter.SelectionsRewriter,org.apache.pinot.sql.parsers.rewriter.PredicateComparisonRewriter,org.apache.pinot.sql.parsers.rewriter.CLPDecodeRewriter,org.apache.pinot.sql.parsers.rewriter.AliasApplier,org.apache.pinot.sql.parsers.rewriter.OrdinalsUpdater,org.apache.pinot.sql.parsers.rewriter.NonAggregationGroupByToDistinctQueryRewriter
```

This adds the `CLPDecodeRewriter` to the default set of query rewriters. Note that the `CLPDecodeRewriter` is placed before the `AliasApplier` so that any aliasing of CLP-encoded fields happens only after the `CLPDECODE` rewrite.
