# JSON Functions

## **Transform Functions** <a href="#transform-functions" id="transform-functions"></a>

CommentShare feedback on the editorThese functions can only be used in Pinot SQL queries.CommentShare feedback on the editor

<table>
  <thead>
    <tr>
      <th>Function</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><p>​<a href="../../functions/json/jsonextractscalar.md"><strong>JSONEXTRACTSCALAR(jsonField, 'jsonPath', 'resultsType', [defaultValue])</strong></a> </p><p>Evaluates the <code>'jsonPath'</code> on <code>jsonField</code>, returns the result as the type <code>'resultsType'</code>, use optional <code>defaultValue</code>for null or parsing error.</p></td>
    </tr>
    <tr>
      <td><p>​<a href="../../functions/json/jsonextractkey.md"><strong>JSONEXTRACTKEY(jsonField, 'jsonPath', ['paramString'])</strong></a> </p><p>Extracts all matched JSON field keys based on <code>'jsonPath'</code> into a <code>STRING_ARRAY.</code></p></td>
    </tr>
    <tr>
      <td><p>​<a href="../../functions/json/jsonextractindex.md"><strong>JSONEXTRACTINDEX(jsonField, 'jsonPath', index, 'resultsType', [defaultValue])</strong></a> </p><p>Extracts the indexed value from an array matched by <code>'jsonPath'</code> and returns it as the requested scalar type.</p></td>
    </tr>
    <tr>
      <td><p>​<a href="../../functions/datetime/extract.md"><strong>EXTRACT(dateTimeField FROM dateTimeExpression)</strong></a> </p><p>Extracts the field from the DATETIME expression of the format <code>'YYYY-MM-DD HH:MM:SS'</code>. Currently, this transformation function supports <code>YEAR</code>, <code>MONTH</code>, <code>DAY</code>, <code>HOUR</code>, <code>MINUTE</code>, and <code>SECOND</code> fields.</p></td>
    </tr>
  </tbody>
</table>

## **Scalar Functions** <a href="#scalar-functions" id="scalar-functions"></a>

CommentShare feedback on the editorThese functions can be used for column transformation in table ingestion configs.CommentShare feedback on the editor

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>​[**TOJSONMAPSTR**(map) ](../../functions/json/tojsonmapstr.md)​</td>
      <td>Convert map to JSON String</td>
    </tr>
    <tr>
      <td>​[**JSONFORMAT**(object)](../../functions/json/jsonformat.md)</td>
      <td>Convert object to JSON String</td>
    </tr>
    <tr>
      <td>​[**JSONPATH(jsonField, 'jsonPath')**](../../functions/json/jsonpath.md)</td>
      <td>Extracts the object value from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. **Cannot be used in query because data type is not specified.**</td>
    </tr>
    <tr>
      <td>​[**JSONPATHLONG**(jsonField, 'jsonPath', \[defaultValue\])](../../functions/json/jsonpathlong.md)</td>
      <td>Extracts the **Long** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error.</td>
    </tr>
    <tr>
      <td>​[**JSONPATHDOUBLE**(jsonField, 'jsonPath', \[defaultValue\])](../../functions/json/jsonpathdouble.md)</td>
      <td>Extracts the **Double** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error.</td>
    </tr>
    <tr>
      <td>​[**JSONPATHSTRING(jsonField, 'jsonPath', \[defaultValue\])**](../../functions/json/jsonpathstring.md)</td>
      <td>Extracts the **String** value from `jsonField` based on `'jsonPath'`, use optional `defaultValue`for null or parsing error.</td>
    </tr>
    <tr>
      <td>​[**JSONPATHARRAY**(jsonField, 'jsonPath')](../../functions/json/jsonpatharray.md)</td>
      <td>Extracts an array from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. **Cannot be used in query because data type is not specified.**</td>
    </tr>
    <tr>
      <td>​[**JSONPATHARRAYDEFAULTEMPTY**(jsonField, 'jsonPath')](../../functions/json/jsonpatharraydefaultempty.md)</td>
      <td>Extracts an array from `jsonField` based on `'jsonPath'`, the result type is inferred based on JSON value. Returns empty array for null or parsing error. **Cannot be used in query because data type is not specified.**</td>
    </tr>
    <tr>
      <td>​[**JSONPATHEXISTS**(jsonField, 'jsonPath')](../../functions/json/jsonpathexists.md)</td>
      <td>Check if path exists in JSON object</td>
    </tr>
    <tr>
      <td>**c**(keyValueArray, \[keyColumnName], \[valueColumnName])</td>
      <td><p>Extract an array of key-value maps to a map. Default <code>keyColumnName</code> is <code>key</code> and default <code>valueColumnName</code> is <code>value</code> . E.g. <strong>JsonKeyValueArrayToMap(input, 'key', 'value'):</strong><br>Input: <code>[{"key": "k1", "value": "v1"}, {"key": "k2", "value": "v2"}, {"key": "k3", "value": "v3"}]</code><br>Output: <code>{"k1": "v1", "k2": "v2", "k3": "v3"}</code></p></td>
    </tr>
    <tr>
      <td>**JsonStringToArray**(jsonString)</td>
      <td>Convert a JSON String to Java List</td>
    </tr>
    <tr>
      <td>**JsonStringToMap**(jsonString)</td>
      <td>Convert a JSON String to Java Map</td>
    </tr>
    <tr>
      <td>**JsonStringToListOrMap**(jsonString)</td>
      <td>Convert a JSON String to either Java List or Map</td>
    </tr>
  </tbody>
</table>

## Additional Reference Pages

<table>
  <thead>
    <tr>
      <th>Function</th>
      <th>Function</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[JSONPATHLONG](jsonpathlong.md)</td>
      <td>[JSONPATHDOUBLE](jsonpathdouble.md)</td>
    </tr>
    <tr>
      <td>[JSONPATHSTRING](jsonpathstring.md)</td>
      <td></td>
    </tr>
  </tbody>
</table>

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

We also assume that "jsoncolumn" has a [Json Index](../../basics/indexing/json-index.md) on it. Note that the last two rows in the table have different structure than the rest of the rows. In keeping with JSON specification, a JSON column can contain any valid JSON data and doesn't need to adhere to a predefined schema. To pull out the entire JSON document for each row, we can run the query below:

```
SELECT id, jsoncolumn 
  FROM myTable
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>jsoncolumn</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"101"</td>
      <td>"{"name":{"first":"daffy","last":"duck"},"score":101,"data":\["a","b","c","d"]}"</td>
    </tr>
    <tr>
      <td>102"</td>
      <td>"{"name":{"first":"donald","last":"duck"},"score":102,"data":\["a","b","e","f"]}</td>
    </tr>
    <tr>
      <td>"103"</td>
      <td>"{"name":{"first":"mickey","last":"mouse"},"score":103,"data":\["a","b","g","h"]}</td>
    </tr>
    <tr>
      <td>"104"</td>
      <td>"{"name":{"first":"minnie","last":"mouse"},"score":104,"data":\["a","b","i","j"]}"</td>
    </tr>
    <tr>
      <td>"105"</td>
      <td>"{"name":{"first":"goofy","last":"dwag"},"score":104,"data":\["a","b","i","j"]}"</td>
    </tr>
    <tr>
      <td>"106"</td>
      <td>"{"person":{"name":"daffy duck","companies":\[{"name":"n1","title":"t1"},{"name":"n2","title":"t2"}]\}}"</td>
    </tr>
    <tr>
      <td>"107"</td>
      <td>"{"person":{"name":"scrooge mcduck","companies":\[{"name":"n1","title":"t1"},{"name":"n2","title":"t2"}]\}}"</td>
    </tr>
  </tbody>
</table>

To drill down and pull out specific keys within the JSON column, we simply append the JsonPath expression of those keys to the end of the column name.

```
SELECT id,
       json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
       json_extract_scalar(jsoncolumn, '$.name.first', 'STRING', 'null') first_name
       json_extract_scalar(jsoncolumn, '$.data[1]', 'STRING', 'null') value
  FROM myTable
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>last\_name</th>
      <th>first\_name</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>101</td>
      <td>duck</td>
      <td>daffy</td>
      <td>b</td>
    </tr>
    <tr>
      <td>102</td>
      <td>duck</td>
      <td>donald</td>
      <td>b</td>
    </tr>
    <tr>
      <td>103</td>
      <td>mouse</td>
      <td>mickey</td>
      <td>b</td>
    </tr>
    <tr>
      <td>104</td>
      <td>mouse</td>
      <td>minnie</td>
      <td>b</td>
    </tr>
    <tr>
      <td>105</td>
      <td>dwag</td>
      <td>goofy</td>
      <td>b</td>
    </tr>
    <tr>
      <td>106</td>
      <td>null</td>
      <td>null</td>
      <td>null</td>
    </tr>
    <tr>
      <td>107</td>
      <td>null</td>
      <td>null</td>
      <td>null</td>
    </tr>
  </tbody>
</table>

Note that the third column (value) is null for rows with id 106 and 107. This is because these rows have JSON documents that don't have a key with JsonPath $.data\[1]. We can filter out these rows.

```
SELECT id,
       json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
       json_extract_scalar(jsoncolumn, '$.name.first', 'STRING', 'null') first_name,
       json_extract_scalar(jsoncolumn, '$.data[1]', 'STRING', 'null') value
  FROM myTable
 WHERE JSON_MATCH(jsoncolumn, '"$.data[1]" IS NOT NULL')
```

<table>
  <thead>
    <tr>
      <th>id</th>
      <th>last\_name</th>
      <th>first\_name</th>
      <th>value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>101</td>
      <td>duck</td>
      <td>daffy</td>
      <td>b</td>
    </tr>
    <tr>
      <td>102</td>
      <td>duck</td>
      <td>donald</td>
      <td>b</td>
    </tr>
    <tr>
      <td>103</td>
      <td>mouse</td>
      <td>mickey</td>
      <td>b</td>
    </tr>
    <tr>
      <td>104</td>
      <td>mouse</td>
      <td>minnie</td>
      <td>b</td>
    </tr>
    <tr>
      <td>105</td>
      <td>dwag</td>
      <td>goofy</td>
      <td>b</td>
    </tr>
  </tbody>
</table>

Certain last names (duck and mouse for example) repeat in the data above. We can get a count of each last name by running a GROUP BY query on a JsonPath expression.

```
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         count(*)
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.data[1]" IS NOT NULL')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
ORDER BY 2 DESC
```

<table>
  <thead>
    <tr>
      <th>jsoncolumn.name.last</th>
      <th>count(\*)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"mouse"</td>
      <td>"2"</td>
    </tr>
    <tr>
      <td>"duck"</td>
      <td>"2"</td>
    </tr>
    <tr>
      <td>"dwag"</td>
      <td>"1"</td>
    </tr>
  </tbody>
</table>

Also there is numerical information (jsconcolumn.$.id) embeded within the JSON document. We can extract those numerical values from JSON data into SQL and sum them up using the query below.

```
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         sum(json_extract_scalar(jsoncolumn, '$.id', 'INT', 0)) total
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.name.last" IS NOT NULL')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
```

<table>
  <thead>
    <tr>
      <th>jsoncolumn.name.last</th>
      <th>sum(jsoncolumn.score)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"mouse"</td>
      <td>"207"</td>
    </tr>
    <tr>
      <td>"dwag"</td>
      <td>"104"</td>
    </tr>
    <tr>
      <td>"duck"</td>
      <td>"203"</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>last\_name</th>
      <th>total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>"duck"</td>
      <td>"102"</td>
    </tr>
  </tbody>
</table>

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

{% content-ref url="../../basics/indexing/json-index.md" %}
[json-index.md](../../basics/indexing/json-index.md)
{% endcontent-ref %}
