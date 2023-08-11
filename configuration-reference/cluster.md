# Cluster

## Cluster Configs Definition

These are the properties that be set at the cluster level.

| Property                                 | Default | Description                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| allowParticipantAutoJoin                 | true    | This is a Helix Property that allows any Pinot Server/Broker/Controller to automatically join the cluster. This is true by default. Operators can set this to false for more control. If you set this to false, you will have to explicitly invoke `/Instance/addInstance` API. This property is checked when a Pinot node starts and has no effect once the node is connected to the cluster.                                    |
| enable.case.insensitive                  | true    | By default, Pinot queries are case insensitive. Table name, column name, etc are case insensitive. This is because the schema is still optional for batch tables. If you have a schema, you can set this to false and pinot will accept any case for table names and columns. This property is applicable to the broker and is read only when the broker starts. Changing this property will require restarting the broker.       |
| pinot.broker.enable.query.limit.override | false   | This allows operators to protect the Pinot cluster against bad queries with large limits. By setting this to true, if Pinot broker override query limit when it is larger than broker config:`pinot.broker.query.response.limit (Default is 2147483647).`E.g. If set`pinot.broker.query.response.limit=1000` in Broker conf, then query`SELECT * FROM myTable LIMIT 25000`will be override to `SELECT * FROM myTable LIMIT 1000`. |
| default.hyperloglog.log2m                | 8       | This is a special config to override for hyperloglog that is used for approximate distinct count. Default value is 8.                                                                                                                                                                                                                                                                                                             |
| queryConsoleOnlyView                     | false   | Only show query console for controller web UI, this is useful when you don't want to expose cluster or ZK UI to Users.                                                                                                                                                                                                                                                                                                            |
| hideQueryConsoleTab                      | false   | Hide query console tab from controller web UI, this is useful when you don't want to expose query console UI to Users.                                                                                                                                                                                                                                                                                                            |

## Cluster Configs APIs

![](<../.gitbook/assets/Screen Shot 2020-07-01 at 10.29.33 PM.png>)

{% swagger baseUrl="http://<controller>:<port>/cluster/configs" path="" method="get" summary="List All Cluster Configs" %}
{% swagger-description %}
**Description**

\- Lists all the configurations set at the cluster level
{% endswagger-description %}

{% swagger-response status="200" description="" %}
```
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```
{% endswagger-response %}
{% endswagger %}

{% swagger baseUrl="http://<controller>:<port>/cluster/configs" path="" method="post" summary="Update Cluster Configs" %}
{% swagger-description %}
Add new or update existing cluster configs.
{% endswagger-description %}

{% swagger-parameter in="body" name="" type="string" required="false" %}
JSON body contains the configs map for new/updated configs. E.g.

**`{"queryConsoleOnlyView":"true"}`**
{% endswagger-parameter %}

{% swagger-response status="200" description="" %}
```
{
  "status": "Updated cluster config."
}
```
{% endswagger-response %}
{% endswagger %}

Example:

![](<../.gitbook/assets/image (9) (2).png>)
