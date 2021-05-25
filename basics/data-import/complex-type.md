
---
description: Complex-type handling in Apache Pinot.
---

# Complex-type handling in Apache Pinot

It's common for the ingested data to have complex structure. For example, Avro schema has [records](https://avro.apache.org/docs/current/spec.html#schema_record) and [arrays](https://avro.apache.org/docs/current/spec.html#Arrays), while JSON data has [objects](https://json-schema.org/understanding-json-schema/reference/object.html) and [arrays](https://json-schema.org/understanding-json-schema/reference/array.html).  In Apache Pinot, the model supports primitive data types (including int, long, float, double, string, bytes), as well as limited multi-value types such as an array of primitive types. Such simple data types allow Pinot to build fast indexing structures for good query performance, but it requires some handling on the complex structures. There are in general two options for such handling, convert the complex-type data into JSON string and build JSON index; or use the inbuilt complex-type handling rule in the ingestion config.

In this page, we'll show how to handle this complex-type structure with these two approaches, to process the example data in the following figure, which is a field `group` from the [Meetup events Quickstart example](https://github.com/apache/incubator-pinot/tree/master/pinot-tools/src/main/resources/examples/stream/meetupRsvp). 

![Example JSON data](../../.gitbook/assets/complex-type-example-data.png)


## Handle the complex type with JSON indexing

Apache Pinot provides powerful [JSON index](../indexing/json-index.md) to accelerate the value lookup and filtering for the column. To convert an object `group` with complex type to JSON, you can add the following config to table config. 

{% code title="json\_meetupRsvp\_realtime\_table\_config.json" %}
```javascript
{
  "transformConfigs": [
      {
        "columnName": "group_json",
        "transformFunction": "jsonFormat(\"group\")"
      }
    ],
    ...
    "tableIndexConfig": {
    "loadMode": "MMAP",
    "noDictionaryColumns": [
      "group_json"
    ],
    "jsonIndexColumns": [
      "group_json"
    ]
  },

}
```

Note the config `transformConfigs` transforms the object `group` to a JSON string `group_json`, which is then creates the jSON indexing with config `jsonIndexColumns`. To read the full spec, please check out this [file](https://github.com/apache/incubator-pinot/blob/master/pinot-tools/src/main/resources/examples/stream/meetupRsvp/json_meetupRsvp_realtime_table_config.json).

Additionall, you need to overwrite the `maxLength` of the field `group_json` on the schema, because by default, a string column has a limited length. For example,

{% code title="json\_meetupRsvp\_realtime\_table\_schema.json" %}
```javascript
{
  {
      "name": "group_json",
      "dataType": "STRING",
      "maxLength": 2147483647
    }
    ...
}
```

For the full spec, please check out this [file](https://github.com/apache/incubator-pinot/blob/master/pinot-tools/src/main/resources/examples/stream/meetupRsvp/json_meetupRsvp_schema.json).

With this, you can start to query the nested fields under `group`. For the deatils about the supported JSON function, please check out this [guide]((../indexing/json-index.md)).

## Handle the complex type with ingestion configurations

Though JSON indexing is a handy way to process the complex types, there are some limitations:
 - It’s not performant to group by or order by a JSON field, because `JSON_EXTRACT_SCALAR` is needed to extract the values in the GROUP BY which invokes the function evaluation.
 - For cases that you want to use Pinot's [multi-column functions](https://docs.pinot.apache.org/users/user-guide-query/supported-aggregations#multi-value-column-functions) such as `DISTINCTCOUNTMV`


Alternatively, you can use the complex-type handling in ingestion configurations to flatten and unnest the complex structure and convert them into primitive types. Then you can reduce the complex-type data into a flattened Pinot table, and query it via SQL.

To process this complex-type, you can add the configuration `complexTypeConfig` to the `ingestionConfig`. For example:

{% code title="complexTypeHandling\_meetupRsvp\_realtime\_table\_config.json" %}
```javascript
{
  "ingestionConfig": {    
    "complexTypeConfig": {
      "delimiter": '.',
      "fieldsToUnnest": ["group.group_topics"]
    }
  }
}
```

With the `complexTypeConfig` , all the map objects will be flattened to direct fields. And with `unnestFields` , a record with the nested collection will unnest into multiple records. For instance, the example in the beginning will transform into two rows with this configuration. 

![Flattened/unnested data](../../.gitbook/assets/complex-type-flattened.png)

Note that
 - The nested field `group_id` under `group` is flattened to field `group.group_id`. The default value of the delimiter is `.`, you can choose other delimiter by changing the configuration `delimiter` under `complexTypeConfig`.
 - The nested array `group_topics` under `group` is unnested into the top-level, and convert the output to a collection of two rows. Note the handling of the nested field within `group_topics`, and the eventual top-level field of `group.group_topics.urlkey`. All the collections to unnest shall be included in configuration `fieldsToUnnest`, otherwise the ingestion by default will serialize the collection to JSON string except for the array of primitive values, which will be ingested as multi-value column by default.


You can find the full spec of the table config [here](https://github.com/apache/incubator-pinot/blob/master/pinot-tools/src/main/resources/examples/stream/meetupRsvp/complexTypeHandling_meetupRsvp_realtime_table_config.json) and the table schema [here](https://github.com/apache/incubator-pinot/blob/master/pinot-tools/src/main/resources/examples/stream/meetupRsvp/complexTypeHandling_meetupRsvp_schema.json).

With the flattening/unnesting, you can then query the table with primitive values using the SQL query like:

```sql
select "group.group_topics.urlkey", "group.group_topics.topic_name", "group.group_id" from meetupRsvp limit 10
```

Note `.` is a reserved character in SQL, so you need to quote the flattened column.


