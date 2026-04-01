# JSON Functions

## **Transform Functions** [](#transform-functions)

CommentShare feedback on the editorThese functions can only be used in Pinot SQL queries.CommentShare feedback on the editor

| Function                                                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ​[**JSONEXTRACTSCALAR(jsonField, 'jsonPath', 'resultsType', [defaultValue])**](jsonextractscalar.md) Evaluates the `'jsonPath'` on `jsonField`, returns the result as the type `'resultsType'`, use optional `defaultValue`for null or parsing error. |
| ​[**JSONEXTRACTKEY(jsonField, 'jsonPath', ['paramString'])**](jsonextractkey.md) Extracts all matched JSON field keys based on `'jsonPath'` into a `STRING_ARRAY.` |
| ​[**JSONEXTRACTINDEX(jsonField, 'jsonPath', index, 'resultsType', [defaultValue])**](jsonextractindex.md) Extracts the indexed value from an array matched by `'jsonPath'` and returns it as the requested scalar type. |
| ​[**EXTRACT(dateTimeField FROM dateTimeExpression)**](../../functions/datetime/extract.md) Extracts the field from the DATETIME expression of the format `'YYYY-MM-DD HH:MM:SS'`. Currently, this transformation function supports `YEAR`, `MONTH`, `DAY`, `HOUR`, `MINUTE`, and `SECOND` fields. |

## **Scalar Functions** [](#scalar-functions)

CommentShare feedback on the editorThese functions can be used for column transformation in table ingestion configs.CommentShare feedback on the editor

| Function                                                                                                 | Usage                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ​[**TOJSONMAPSTR**(map) ](../../functions/json/tojsonmapstr.md)​                                            | Convert map to JSON String                                                                                                                                                                                                                                                                                                                                                                                                      |
| ​[**JSONFORMAT**(object)](../../functions/json/jsonformat.md)                                               | Convert object to JSON String                                                                                                                                                                                                                                                                                                                                                                                                   |
| ​[**JSONPATH(jsonField, 'jsonPath')**](../../functions/json/jsonpath.md)                                    | Extracts the object value from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. **Cannot be used in query because data type is not specified.**                                                                                                                                                                                                                                              |
| ​[**JSONPATHLONG**(jsonField, 'jsonPath', \[defaultValue\])](../../functions/json/jsonpathlong.md)          | Extracts the **Long** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error.                                                                                                                                                                                                                                                                                                       |
| ​[**JSONPATHDOUBLE**(jsonField, 'jsonPath', \[defaultValue\])](../../functions/json/jsonpathdouble.md)      | Extracts the **Double** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error.                                                                                                                                                                                                                                                                                                     |
| ​[**JSONPATHSTRING(jsonField, 'jsonPath', \[defaultValue\])**](../../functions/json/jsonpathstring.md)      | Extracts the **String** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error.                                                                                                                                                                                                                                                                                                     |
| ​[**JSONPATHARRAY**(jsonField, 'jsonPath')](../../functions/json/jsonpatharray.md)                          | Extracts an array from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. **Cannot be used in query because data type is not specified.**                                                                                                                                                                                                                                                      |
| ​[**JSONPATHARRAYDEFAULTEMPTY**(jsonField, 'jsonPath')](../../functions/json/jsonpatharraydefaultempty.md)  | Extracts an array from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. Returns empty array for null or parsing error. **Cannot be used in query because data type is not specified.**                                                                                                                                                                                                       |
| ​[**JSONPATHEXISTS**(jsonField, 'jsonPath')](../../functions/json/jsonpathexists.md)                    | Check if path exists in JSON object                                                                                                                                                                                                                                                                                                                                                                                             |
| **c**(keyValueArray, \[keyColumnName], \[valueColumnName]) | Extract an array of key-value maps to a map. Default `keyColumnName` is `key` and default `valueColumnName` is `value` . E.g. **JsonKeyValueArrayToMap(input, 'key', 'value'):** Input: `[{"key": "k1", "value": "v1"}, {"key": "k2", "value": "v2"}, {"key": "k3", "value": "v3"}]` Output: `{"k1": "v1", "k2": "v2", "k3": "v3"}` |
| **JsonStringToArray**(jsonString)                                                                        | Convert a JSON String to Java List                                                                                                                                                                                                                                                                                                                                                                                              |
| **JsonStringToMap**(jsonString)                                                                          | Convert a JSON String to Java Map                                                                                                                                                                                                                                                                                                                                                                                               |
| **JsonStringToListOrMap**(jsonString)                                                                    | Convert a JSON String to either Java List or Map                                                                                                                                                                                                                                                                                                                                                                                |

## Additional Reference Pages

| Function | Function |
| --- | --- |
| [JSONPATHLONG](jsonpathlong.md) | [JSONPATHDOUBLE](jsonpathdouble.md) |
| [JSONPATHSTRING](jsonpathstring.md) |  |

## More Examples

To see how JSON data can be queried, assume that we have the following table:

```
Table myTable:
  id        INTEGER
  jsoncolumn    JSON 

Table data:
101,{"name":{"first":"daffy"\,"last":"duck"}\,"score":101\,"data":["a"\,"b"\,"c"\,"d"]}
102,{"name":{"first":"donald"\,"last":"duck"}\,"score":102\,"data":["a"\,"b"\,"e"\,"f"]}
103,{"name":{"first":"mickey"\,"last":"mouse"}\,"score":103\,"data":["a"\,"b"\,"g"\,"h"]}
104,{"name":{"first":"minnie"\,"last":"mouse"}\,"score":104\,"data":["a"\,"b"\,"i"\,"j"]}
105,{"name":{"first":"goofy"\,"last":"dwag"}\,"score":104\,"data":["a"\,"b"\,"i"\,"j"]}
106,{"person":{"name":"daffy duck"\,"companies":[{"name":"n1"\,"title":"t1"}\,{"name":"n2"\,"title":"t2"}]}}
107,{"person":{"name":"scrooge mcduck"\,"companies":[{"name":"n1"\,"title":"t1"}\,{"name":"n2"\,"title":"t2"}]}}
```

We also assume that "jsoncolumn" has a [Json Index](../../build-with-pinot/indexing/json-index.md) on it. Note that the last two rows in the table have different structure than the rest of the rows. In keeping with JSON specification, a JSON column can contain any valid JSON data and doesn't need to adhere to a predefined schema. To pull out the entire JSON document for each row, we can run the query below:

```
SELECT id, jsoncolumn 
  FROM myTable
```

| id    | jsoncolumn                                                                                                   |
| ----- | ------------------------------------------------------------------------------------------------------------ |
| "101" | "{"name":{"first":"daffy","last":"duck"},"score":101,"data":\["a","b","c","d"]}"                             |
| 102"  | "{"name":{"first":"donald","last":"duck"},"score":102,"data":\["a","b","e","f"]}                             |
| "103" | "{"name":{"first":"mickey","last":"mouse"},"score":103,"data":\["a","b","g","h"]}                            |
| "104" | "{"name":{"first":"minnie","last":"mouse"},"score":104,"data":\["a","b","i","j"]}"                           |
| "105" | "{"name":{"first":"goofy","last":"dwag"},"score":104,"data":\["a","b","i","j"]}"                             |
| "106" | "{"person":{"name":"daffy duck","companies":\[{"name":"n1","title":"t1"},{"name":"n2","title":"t2"}]\}}"     |
| "107" | "{"person":{"name":"scrooge mcduck","companies":\[{"name":"n1","title":"t1"},{"name":"n2","title":"t2"}]\}}" |

To drill down and pull out specific keys within the JSON column, we simply append the JsonPath expression of those keys to the end of the column name.

```
SELECT id,
       json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
       json_extract_scalar(jsoncolumn, '$.name.first', 'STRING', 'null') first_name
       json_extract_scalar(jsoncolumn, '$.data[1]', 'STRING', 'null') value
  FROM myTable
```

| id  | last\_name | first\_name | value |
| --- | ---------- | ----------- | ----- |
| 101 | duck       | daffy       | b     |
| 102 | duck       | donald      | b     |
| 103 | mouse      | mickey      | b     |
| 104 | mouse      | minnie      | b     |
| 105 | dwag       | goofy       | b     |
| 106 | null       | null        | null  |
| 107 | null       | null        | null  |

Note that the third column (value) is null for rows with id 106 and 107. This is because these rows have JSON documents that don't have a key with JsonPath $.data\[1]. We can filter out these rows.

```
SELECT id,
       json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
       json_extract_scalar(jsoncolumn, '$.name.first', 'STRING', 'null') first_name,
       json_extract_scalar(jsoncolumn, '$.data[1]', 'STRING', 'null') value
  FROM myTable
 WHERE JSON_MATCH(jsoncolumn, '"$.data[1]" IS NOT NULL')
```

| id  | last\_name | first\_name | value |
| --- | ---------- | ----------- | ----- |
| 101 | duck       | daffy       | b     |
| 102 | duck       | donald      | b     |
| 103 | mouse      | mickey      | b     |
| 104 | mouse      | minnie      | b     |
| 105 | dwag       | goofy       | b     |

Certain last names (duck and mouse for example) repeat in the data above. We can get a count of each last name by running a GROUP BY query on a JsonPath expression.

```
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         count(*)
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.data[1]" IS NOT NULL')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
ORDER BY 2 DESC
```

| jsoncolumn.name.last | count(\*) |
| -------------------- | --------- |
| "mouse"              | "2"       |
| "duck"               | "2"       |
| "dwag"               | "1"       |

Also there is numerical information (jsconcolumn.$.id) embeded within the JSON document. We can extract those numerical values from JSON data into SQL and sum them up using the query below.

```
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         sum(json_extract_scalar(jsoncolumn, '$.id', 'INT', 0)) total
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.name.last" IS NOT NULL')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
```

| jsoncolumn.name.last | sum(jsoncolumn.score) |
| -------------------- | --------------------- |
| "mouse"              | "207"                 |
| "dwag"               | "104"                 |
| "duck"               | "203"                 |

### JSON\_MATCH and JSON\_EXTRACT\_SCALAR

Note that the `JSON_MATCH` function utilizes `JsonIndex` and can only be used if a `JsonIndex` is already present on the JSON column. As shown in the examples above, the second argument of `JSON_MATCH` operator takes a predicate. This predicate is evaluated against the `JsonIndex` and supports `=`, `!=`, `IS NULL`,  `IS NOT NULL`, IN and relational operators, such as `>`, `<`, `>=`,  `<=` and `BETWEEN`.&#x20;

`JSON_MATCH` function also provides the ability to use wildcard `*` JsonPath expressions even though it doesn't support full JsonPath expressions.

```
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         json_extract_scalar(jsoncolumn, '$.id', 'INT', 0) total
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.data[*]" = ''f''')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
```

| last\_name | total |
| ---------- | ----- |
| "duck"     | "102" |

While, JSON\_MATCH supports `IS NULL` and `IS NOT NULL` operators, these operators should only be applied to leaf-level path elements, i.e the predicate `JSON_MATCH(jsoncolumn, '"$.data[*]" IS NOT NULL')` is not valid since `"$.data[*]"` does not address a "leaf" element of the path; however, `"$.data[0]" IS NOT NULL')` is valid since `"$.data[0]"` unambigously identifies a leaf element of the path.

`JSON_EXTRACT_SCALAR` does not utilize JsonIndex and therefore performs slower than `JSON_MATCH` which utilizes JsonIndex. However, `JSON_EXTRACT_SCALAR` supports a wider range for of JsonPath expressions and operators. To make the best use of fast index access (`JSON_MATCH`) along with JsonPath expressions (`JSON_EXTRACT_SCALAR`) you can combine the use of these two functions in WHERE clause.

### JSON\_MATCH syntax

The second argument of the `JSON_MATCH` function is a boolean expression in string form. This section shows how to correctly write the second argument of JSON\_MATCH. Let's assume we want to search a JSON array array `data` for values `k` and `j`. This can be done by the following predicate:

```
data[0] IN ('k', 'j')
```

To convert this predicate into string form for use in JSON\_MATCH, we first turn the left side of the predicate into an identifier by enclosing it in double quotes:

```
"data[0]" IN ('k', 'j')
```

Next, the literals in the predicate also need to be enclosed by '. Any existing ' need to be escaped as well. This gives us:

```
"data[0]" IN (''k'', ''j'')
```

Finally, we need to create a string out of the entire expression above by enclosing it in ':

```
'"data[0]" IN (''k'', ''j'')'
```

Now we have the string representation of the original predicate and this can be used in JSON\_MATCH function:

```
   WHERE JSON_MATCH(jsoncolumn, '"data[0]" IN (''k'', ''j'')')
```

For more JSON\_MATCH examples, please see&#x20;

{% content-ref url="../../build-with-pinot/indexing/json-index.md" %}
[json-index.md](../../build-with-pinot/indexing/json-index.md)
{% endcontent-ref %}
