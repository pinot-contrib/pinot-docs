# JSON Index

JSON index can be applied to JSON string columns to accelerate the value lookup and filtering for the column.

## When to use JSON index

JSON string can be used to represent the array, map, nested field without forcing a fixed schema. It is very flexible, but the flexibility comes with a cost - filtering on JSON string columns is very expensive.

Suppose we have some JSON records similar to the following sample record stored in the `person` column:

```javascript
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

Without an index, in order to look up a key and filter records based on the value, we need to scan and reconstruct the JSON object from the JSON string for every record, look up the key and then compare the value.

For example, in order to find all persons whose name is "adam", the query will look like:

```sql
SELECT * 
FROM mytable 
WHERE JSON_EXTRACT_SCALAR(person, '$.name', 'STRING') = 'adam'
```

JSON index is designed to accelerate the filtering on JSON string columns without scanning and reconstructing all the JSON objects.

## Configure JSON index

To enable the JSON index, set the following config in the table config:

### Config since release `0.12.0`:

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

| Config Key                  | Desciprtion                                                                                                                                                                                                                            | Type         | Default                                              |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ---------------------------------------------------- |
| **maxLevels**               | Max levels to flatten the json object (array is also counted as one level)                                                                                                                                                             | int          | -1 (unlimited)                                       |
| **excludeArray**            | Whether to exclude array when flattening the object                                                                                                                                                                                    | boolean      | false (include array)                                |
| **disableCrossArrayUnnest** | Whether to not unnest multiple arrays (unique combination of all elements)                                                                                                                                                             | boolean      | false (calculate unique combination of all elements) |
| **includePaths**            | Only include the given paths, e.g. "_$.a.b_", "_$.a.c\[\*]_" (mutual exclusive with **excludePaths**). Paths under the included paths will be included, e.g. "_$.a.b.c_" will be included when "_$.a.b_" is configured to be included. | Set\<String> | null (include all paths)                             |
| **excludePaths**            | Exclude the given paths, e.g. "_$.a.b_", "_$.a.c\[\*]_" (mutual exclusive with **includePaths**). Paths under the excluded paths will also be excluded, e.g. "_$.a.b.c_" will be excluded when "_$.a.b_" is configured to be excluded. | Set\<String> | null (include all paths)                             |
| **excludeFields**           | Exclude the given fields, e.g. "_b_", "_c_", even if it is under the included paths.                                                                                                                                                   | Set\<String> | null (include all fields)                            |

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

With the default setting, we will flatten the document into the following records:

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
  "age": 20son
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

### Legacy config before release `0.12.0`:

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

The legacy config has the same behavior as the default settings in the new config.



Note that JSON index can only be applied to `STRING/JSON` columns whose values are JSON strings.

When you're using a JSON index, we would recommend that you add the indexed column to the `noDictionaryColumns` columns list to reduce unnecessary storage overhead. For instructions on that config property, see the [Raw value forward index](forward-index.md#raw-value-forward-index) documentation.

## How to use JSON index

JSON index can be used via the `JSON_MATCH` predicate: `JSON_MATCH(<column>, '<filterExpression>')`. For example, to find all persons whose name is "adam", the query will look like:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.name"=''adam''')
```

Note that the quotes within the filter expression need to be escaped.

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for `filterExpression`: `'name=''adam'''`
{% endhint %}

## Supported filter expressions

### Simple key lookup

Find all persons whose name is "adam":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.name"=''adam''')
```

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for filterExpression: `'name=''adam'''`
{% endhint %}

### Chained key lookup

Find all persons who have an address (one of the addresses) with number 112:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[*].number"=112')
```

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for filterExpression: `'addresses.number=112'`
{% endhint %}

### Nested filter expression

Find all persons whose name is "adam" and also have an address (one of the addresses) with number 112:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.name"=''adam'' AND "$.addresses[*].number"=112')
```

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for filterExpression: `'name=''adam'' AND addresses.number=112'`
{% endhint %}

### Array access

Find all persons whose first address has number 112:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[0].number"=112')
```

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for filterExpression: `'"addresses[0].number"=112'`
{% endhint %}

### Existence check

Find all persons who have a phone field within the JSON:

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.phone" IS NOT NULL')
```

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for filterExpression: `'phone IS NOT NULL'`
{% endhint %}

Find all persons whose first address does not contain floor field within the JSON:

```sql
SELECT ... 
FROM mytable
WHERE JSON_MATCH(person, '"$.addresses[0].floor" IS NULL')
```

{% hint style="info" %}
In release `0.7.1`, we use the old syntax for filterExpression: `'"addresses[0].floor" IS NULL'`
{% endhint %}

## JSON context is maintained

The JSON context is maintained for object elements within an array, i.e. the filter won't cross-match different objects in the array.

To find all persons who live on "main st" in "ca":

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[*].street"=''main st'' AND "$.addresses[*].country"=''ca''')
```

This query won't match "adam" because none of his addresses matches both the street and the country.

If JSON context is not desired, use multiple separate `JSON_MATCH` predicates. E.g. to find all persons who have addresses on "main st" and have addressed in "ca" (doesn't have to be the same address):

```sql
SELECT ... 
FROM mytable 
WHERE JSON_MATCH(person, '"$.addresses[*].street"=''main st''') AND JSON_MATCH(person, '"$.addresses[*].country"=''ca''')
```

This query will match "adam" because one of his addresses matches the street and another one matches the country.

Note that the array index is maintained as a separate entry within the element, so in order to query different elements within an array, multiple `JSON_MATCH` predicates are required. E.g. to find all persons who have first address on "main st" and second address on "second st":

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

{% hint style="warning" %}
In release `0.7.1`, json string must be object (cannot be `null`, value or array); multi-dimensional array is not supported.
{% endhint %}

## Limitations

1. The key (left-hand side) of the filter expression must be the leaf level of the JSON object, e.g. `"$.addresses[*]"='main st'` won't work.
