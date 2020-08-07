# Cluster

These are the properties that be set at the cluster level. 

| Property | Default | Description |
| :--- | :--- | :--- |
| allowParticipantAutoJoin |  | This is a Helix Property that allows any Pinot Server/Broker/Controller to automatically join the cluster. This is true by default. Operators can set this to false for more control. If you set this to false, you will have to explicitly invoke `/Instance/addInstance`  API. This property is checked when a Pinot node starts and has no effect once the node is connected to the cluster. |
| enable.case.insensitive |  | By default, Pinot queries are case sensitive. Table name, column name, etc must be case sensitive. This is because the schema is still optional for batch tables. If you have a schema, you can set this to true and pinot will accept any case for table names and columns. This property is applicable to the broker and is read only when the broker starts. Changing this property will required broker to be restarted. |
| pinot.broker.enable.query.limit.override |  | This allows operators to protect the Pinot cluster against bad queries with large limits. By setting this to true, if Pinot broker override query limit when it is larger than broker config:`pinot.broker.query.response.limit (Default is 2147483647).`E.g. If set`pinot.broker.query.response.limit=1000` in Broker conf, then query`SELECT * FROM myTable LIMIT 25000`will be override to `SELECT * FROM myTable LIMIT 1000`. |
| default.hyperloglog.log2m |  | This is a special config to override for hyperloglog that is used for approximate distinct count. Default value is 8. |



### Retrieve current config

You can retrieve all of the cluster properties using the following controller API - 

{% api-method method="get" host="http://<controller>:<port>/cluster/configs\'" path="" %}
{% api-method-summary %}
List Cluster Config
{% endapi-method-summary %}

{% api-method-description %}
**Description** - Lists all the configurations set at the cluster level
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

![](../.gitbook/assets/screen-shot-2020-07-01-at-10.29.33-pm.png)



