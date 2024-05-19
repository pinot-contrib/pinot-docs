---
description:  This page describes configuring the JSON index for Apache Pinot.
---

# JSON index

The JSON index can be applied to JSON string columns to accelerate value lookups and filtering for the column.

## When to use JSON index

Use the JSON string can be used to represent array, map, and nested fields without forcing a fixed schema. While JSON strings are flexible, filtering on JSON string columns is expensive, so consider the use case.

Suppose we have some JSON records similar to the following sample record stored in the `person` column:

```json
{
  "name": "adam",
  "age": 30,
  "country": "us",
  "addresses":
  [
    {
      "number" : 112,
      "street" : "main st",
      "country" : "us"
    },
    {
      "number" : 2,
      "street" : "second st",
      "country" : "us"
    },
    {
      "number" : 3,
      "street" : "third st",
      "country" : "ca"
    }
  ]
}
```

Without an index, to look up the key and filter records based on the value, Pinot must scan and reconstruct the JSON object from the JSON string for every record, look up the key and then compare the value.

For example, in order to find all persons whose name is "adam", the query will look like:

```sql
SELECT * 
FROM mytable 
WHERE JSON_EXTRACT_SCALAR(person, '$.name', 'STRING') = 'adam'
```

The JSON index is designed to accelerate the filtering on JSON string columns without scanning and reconstructing all the JSON objects.

## Enable and configure a JSON index

To enable the JSON index, you can configure the following options in the table configuration:

| Config Key                  | Description                                                                                                                                                                                                                            | Type         | Default                                              |
| --------------------------- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------ | ---------------------------------------------------- |
| **maxLevels**               | Max levels to flatten the json object (array is also counted as one level)                                                                                                                                                             | int          | -1 (unlimited)                                       |
| **excludeArray**            | Whether to exclude array when flattening the object                                                                                                                                                                                    | boolean      | false (include array)                                |
| **disableCrossArrayUnnest** | Whether to not unnest multiple arrays (unique combination of all elements)                                                                                                                                                             | boolean      | false (calculate unique combination of all elements) |
| **includePaths**            | Only include the given paths, e.g. "_$.a.b_", "_$.a.c\[\*]_" (mutual exclusive with **excludePaths**). Paths under the included paths will be included, e.g. "_$.a.b.c_" will be included when "_$.a.b_" is configured to be included. | Set\<String> | null (include all paths)                             |
| **excludePaths**            | Exclude the given paths, e.g. "_$.a.b_", "_$.a.c\[\*]_" (mutual exclusive with **includePaths**). Paths under the excluded paths will also be excluded, e.g. "_$.a.b.c_" will be excluded when "_$.a.b_" is configured to be excluded. | Set\<String> | null (include all paths)                             |
| **excludeFields**           | Exclude the given fields, e.g. "_b_", "_c_", even if it is under the included paths.                                                                                                                                                   | Set\<String> | null (include all fields)                            |

### Recommended way to configure

The recommended way to configure a JSON index is in the `fieldConfigList.indexes` object, within the `json` key.

{% code title="json index defined in tableConfig" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "person",
      "indexes": {
        "json": {
          "maxLevels": 2,
          "excludeArray": false,
          "disableCrossArrayUnnest": true,
          "includePaths": null,
          "excludePaths": null,
          "excludeFields": null
        }
      }
    }
  ],
  ...
}
```
{% endcode %}

All options are optional, so the following is a valid configuration that use the default parameter values:

{% code title="json index defined in tableConfig" %}
```javascript
{
  "fieldConfigList": [
    {
      "name": "person",
      "indexes": {
        "json": {}
      }
    }
  ],
  ...
}
```
{% endcode %}

### Deprecated ways to configure JSON indexes

There are two older ways to configure the indexes that can be configured in the `tableIndexConfig` section inside table 
config.

The first one uses the same JSON explained above, but it is defined inside `tableIndexConfig.jsonIndexConfigs.<column name>`:

{% code title="older way to configure json indexes in table config" %}
```json
{
  "tableIndexConfig": {
    "jsonIndexConfigs": {
      "person": {
        "maxLevels": 2,
        "excludeArray": false,
        "disableCrossArrayUnnest": true,
        "includePaths": null,
        "excludePaths": null,
        "excludeFields": null
      },
      ...
    },
    ...
  }
}
```
{% endcode %}

Like in the previous case, all parameters are optional, so the following is also valid:

{% code title="json index with default config" %}
```json
{
  "tableIndexConfig": {
    "jsonIndexConfigs": {
      "person": {},
      ...
    },
    ...
  }
}
```
{% endcode %}

The last option does not support to configure any parameter.
In order to use this option, add the name of the column in `tableIndexConfig.jsonIndexColumns` like in this example:

{% code title="json index with default config" %}
```javascript
{
  "tableIndexConfig": {        
    "jsonIndexColumns": [
      "person",
      ...
    ],
    ...
  }
}
```
{% endcode %}

#### Example:

With the following JSON document:

```json
{
  "name": "adam",
  "age": 20,
  "addresses": [
    {
      "country": "us",
      "street": "main st",
      "number": 1
    },
    {
      "country": "ca",
      "street": "second st",
      "number": 2
    }
  ],
  "skills": [
    "english",
    "programming"
  ]
}
```

Using the default setting, we will flatten the document into the following records:

```json
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1,
  "skills[1]": "programming"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "addresses[1].number": 2,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "addresses[1].number": 2,
  "skills[1]": "programming"
}
```

With **maxLevels** set to 1:

```json
{
  "name": "adam",
  "age": 20
}
```

With **maxLevels** set to 2:

```json
{
  "name": "adam",
  "age": 20,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "skills[1]": "programming"
}
```

With **excludeArray** set to true:

```json
{
  "name": "adam",
  "age": 20
}
```

With **disableCrossArrayUnnest** set to true:

```json
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1
},
{
  "name": "adam",
  "age": 20,
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "addresses[0].number": 1
},
{
  "name": "adam",
  "age": 20,
  "skills[0]": "english"
},
{
  "name": "adam",
  "age": 20,
  "skills[1]": "programming"
}
```

With **includePaths** set to \["$.name", "$.addresses\[\*].country"]:

```json
{
  "name": "adam",
  "addresses[0].country": "us"
},
{
  "name": "adam",
  "addresses[1].country": "ca"
}
```

With **excludePaths** set to \["$.age", "$.addresses\[\*].number"]:

```json
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].street": "main st",
  "skills[1]": "programming"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].street": "second st",
  "skills[1]": "programming"
}
```

With **excludeFields** set to \["age", "street"]:

```json
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].number": 1,
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[0].country": "us",
  "addresses[0].number": 1,
  "skills[1]": "programming"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].number": 2,
  "skills[0]": "english"
},
{
  "name": "adam",
  "addresses[1].country": "ca",
  "addresses[1].number": 2,
  "skills[1]": "programming"
}
```


Note that the JSON index can only be applied to `STRING/JSON` columns whose values are JSON strings.

{% hint style="info" %}
To reduce unnecessary storage overhead when using a JSON index, we recommend that you add the indexed column to the `noDictionaryColumns` columns list.

For instructions on that configuration property, see the [Raw value forward index](forward-index.md#raw-value-forward-index) documentation.
{% endhint %}

## How to use the JSON index

The JSON index can be used via the `JSON_MATCH` predicate: `JSON_MATCH(<column>, '<filterExpression>')`. For example, to find every entry with the name "adam":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.name"=''adam''')
```

Note that the quotes within the filter expression need to be escaped.

## Supported filter expressions

### Simple key lookup

Find all persons whose name is "adam":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.name"=''adam''')
```

### Chained key lookup

Find all persons who have an address (one of the addresses) with number 112:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].number"=112')
```

Find all persons who have at least one address that is not in the US:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[*].country" != ''us''')
```

### Regex based lookup

Find all persons who have an address (one of the addresses) where the street contains the term 'st':

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, 'REGEXP_LIKE("$.addresses[*].street", ''.*st.*'')')
```

### Range lookup

Find all persons whose age is greater than 18:

```sql
SELECT ...
FROM mytable
WHERE JSON_MATCH(person, '"$.age" > 18')
```


### Nested filter expression

Find all persons whose name is "adam" and also have an address (one of the addresses) with number 112:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.name"=''adam'' AND "$.addresses[*].number"=112')
```

{% hint style="info" %}
`NOT IN` and `!=` can't be used in nested filter expressions in Pinot versions older than 1.2.0. Note that `IS NULL` cannot be used in nested filter expressions currently.
{% endhint %}

### Array access

Find all persons whose first address has number 112:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[0].number"=112')
```

### Existence check

Find all persons who have a phone field within the JSON:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.phone" IS NOT NULL')
```

Find all persons whose first address does not contain floor field within the JSON:

```sql
SELECT ... 
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[0].floor" IS NULL')
```

## JSON context is maintained

The JSON context is maintained for object elements within an array, meaning the filter won't cross-match different objects in the array.

To find all persons who live on "main st" in "ca":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[*].street"=''main st'' AND "$.addresses[*].country"=''ca''')
```

This query won't match "adam" because none of his addresses matches both the street and the country.

If you don't want JSON context, use multiple separate `JSON_MATCH` predicates. For example, to find all persons who have addresses on "main st" and have addresses in "ca" (matches need not have the same address):

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[*].street"=''main st''') AND JSON_MATCH(person, '"$.addresses[*].country"=''ca''')
```

This query will match "adam" because one of his addresses matches the street and another one matches the country.

The array index is maintained as a separate entry within the element, so in order to query different elements within an array, multiple `JSON_MATCH` predicates are required. For example, to find all persons who have first address on "main st" and second address on "second st":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[0].street"=''main st''') AND JSON_MATCH(person, '"$.addresses[1].street"=''second st''')
```

## Supported JSON values

### Object

See examples above.

### Array

```javascript
["item1", "item2", "item3"]
```

To find the records with array element "item1" in "arrayCol":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(arrayCol, '"$[*]"=''item1''')
```

To find the records with second array element "item2" in "arrayCol":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(arrayCol, '"$[1]"=''item2''')
```

### Value

```javascript
123
1.23
"Hello World"
```

To find the records with value 123 in "valueCol":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(valueCol, '"$"=123')
```

### Null

```javascript
null
```

To find the records with null in "nullableCol":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(nullableCol, '"$" IS NULL')
```

## Limitations

1. The key (left-hand side) of the filter expression must be the leaf level of the JSON object, for example, `"$.addresses[*]"='main st'` won't work.
