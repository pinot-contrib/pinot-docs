# Querying JSON data

To see how JSON data can be queried, assume that we have the following table:

```text
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

We also assume that "jsoncolumn" has a [Json Index](https://docs.pinot.apache.org/basics/indexing/json-index) on it. Note that the last two rows in the table have different structure than the rest of the rows. In keeping with JSON specification, a JSON column can contain any valid JSON data and doesn't need to adhere to a predefined schema. To pull out the entire JSON document for each row, we can run the query below:

```text
SELECT id, jsoncolumn 
  FROM myTable
```

| id | jsoncolumn |
| ----------- | ----------- |
|"101" |"{"name":{"first":"daffy","last":"duck"},"score":101,"data":["a","b","c","d"]}"|
|102"| "{"name":{"first":"donald","last":"duck"},"score":102,"data":["a","b","e","f"]}|
|"103"|"{"name":{"first":"mickey","last":"mouse"},"score":103,"data":["a","b","g","h"]}|
|"104"|"{"name":{"first":"minnie","last":"mouse"},"score":104,"data":["a","b","i","j"]}"|
|"105"|"{"name":{"first":"goofy","last":"dwag"},"score":104,"data":["a","b","i","j"]}"|
|"106"|"{"person":{"name":"daffy duck","companies":[{"name":"n1","title":"t1"},{"name":"n2","title":"t2"}]}}"|
|"107"|"{"person":{"name":"scrooge mcduck","companies":[{"name":"n1","title":"t1"},{"name":"n2","title":"t2"}]}}"|

To drill down and pull out specific keys within the JSON column, we simply append the JsonPath expression of those keys to the end of the column name.


```text
SELECT id,
       json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
       json_extract_scalar(jsoncolumn, '$.name.first', 'STRING', 'null') first_name
       json_extract_scalar(jsoncolumn, '$.data[1]', 'STRING', 'null') value
  FROM myTable
```

|id|last_name|first_name|value|
| ----------- | ----------- | ----------- | ----------- |
|101|duck|daffy|b|
|102|duck|donald|b|
|103|mouse|mickey|b|
|104|mouse|minnie|b|
|105|dwag|goofy|b|
|106|null|null|null|
|107|null|null|null|

Note that the third column \(value\) is null for rows with id 106 and 107. This is because these rows have JSON 
documents that don't have a key with JsonPath $.data\[1\]. We can filter out these rows.

```text
SELECT id,
       json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
       json_extract_scalar(jsoncolumn, '$.name.first', 'STRING', 'null') first_name,
       json_extract_scalar(jsoncolumn, '$.data[1]', 'STRING', 'null') value
  FROM myTable
 WHERE JSON_MATCH(jsoncolumn, '"$.data[1]" IS NOT NULL')
```

|id|last_name|first_name|value|
| ----------- | ----------- | ----------- | ----------- |
|101|duck|daffy|b|
|102|duck|donald|b|
|103|mouse|mickey|b|
|104|mouse|minnie|b|
|105|dwag|goofy|b|

Certain last names \(duck and mouse for example\) repeat in the data above. We can get a count of each last name by 
running a GROUP BY query on a JsonPath expression.

```text
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         count(*)
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.data[1]" IS NOT NULL')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
ORDER BY 2 DESC
```
|jsoncolumn.name.last|count(*)|
| ----------- | ----------- |
|"mouse"|"2"|
|"duck"|"2"|
|"dwag"|"1"|


Also there is numerical information \(jsconcolumn.$.id\) embeded within the JSON document. We can extract those 
numerical values from JSON data into SQL and sum them up using the query below.

```text
  SELECT json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null') last_name,
         sum(json_extract_scalar(jsoncolumn, '$.id', 'INT', 0)) total
    FROM myTable
   WHERE JSON_MATCH(jsoncolumn, '"$.name.last" IS NOT NULL')
GROUP BY json_extract_scalar(jsoncolumn, '$.name.last', 'STRING', 'null')
```
|jsoncolumn.name.last|sum(jsoncolumn.score)|
| ----------- | ----------- |
|"mouse"|"207"|
|"dwag"|"104"|
|"duck"|"203"|

