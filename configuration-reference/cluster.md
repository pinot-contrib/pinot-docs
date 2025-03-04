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
| pinot.multistage.engine.tls.enabled      | false   | Whether to enable TLS on brokers and servers for the multi-stage query engine. If set to true, TLS will be used for gRPC connections between brokers and servers (query plan dispatch from brokers to servers and final query result from servers to brokers) as well as servers and servers (data shuffle / exchange during execution of multi-stage queries).                                                                   |

## Cluster Configs APIs

## List All Cluster Configs

<mark style="color:blue;">`GET`</mark> `http://<controller>:<port>/cluster/configs`

**Description**

\- Lists all the configurations set at the cluster level

{% tabs %}
{% tab title="200 " %}
```
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```
{% endtab %}
{% endtabs %}

## Update Cluster Configs

<mark style="color:green;">`POST`</mark> `http://<controller>:<port>/cluster/configs`

Add new or update existing cluster configs.

#### Request Body

| Name | Type   | Description                                                                                                                                 |
| ---- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
|      | string | <p>JSON body contains the configs map for new/updated configs. E.g.</p><p><strong><code>{"queryConsoleOnlyView":"true"}</code></strong></p> |

{% tabs %}
{% tab title="200 " %}
```
{
  "status": "Updated cluster config."
}
```
{% endtab %}
{% endtabs %}

Example:

![](../.gitbook/assets/swagger-cluster-config%20\(1\)%20\(1\).png)
