# Rebalance Brokers

Rebalance operation is used to recompute assignment of brokers or servers in the cluster. This is not a single command, but more of a series of steps that need to be taken.

In case of brokers, rebalance operation is used to recalculate the broker assignment to the tables. This is typically done after capacity changes.

### Capacity changes

These are typically done when downsizing/uplifting a cluster, or replacing nodes of a cluster.

#### Tenants and tags

Every broker added to the Pinot cluster, has tags associated with it. A group of brokers with the same tag forms a Broker Tenant. By default, a broker in the cluster gets added to the `DefaultTenant` i.e. gets tagged as `DefaultTenant_BROKER`. Below is an example of how this tag looks in the znode, as seen in ZooInspector.

![Broker tag](<../../../.gitbook/assets/Screen Shot 2020-09-15 at 11.24.58 AM.png>)

A Pinot table config has a tenants section, to define the tenant to be used by the table. More details about this in the [Tenants](../../../basics/components/cluster/tenant.md) section.

```
 {   
    "tableName": "myTable_OFFLINE",
    "tenants" : {
      "broker":"DefaultTenant",
      "server":"DefaultTenant"
    }
  }
```

Using the tenant defined above, a mapping is created, from table name to brokers and stored in the `IDEALSTATES/brokerResource`. This mapping can be used by external services that need to pick a broker for querying.&#x20;

![brokerResource IDEALSTATE](<../../../.gitbook/assets/Screen Shot 2020-09-15 at 11.26.12 AM.png>)

#### Updating tags

If you want to scale up brokers, add new brokers to the cluster, and then tag them based on the tenant used by the table. If you're using `DefaultTenant`, no tagging needs to be done, as every broker node by default joins with tag `DefaultTenant_BROKER`.&#x20;

If you want to scale down brokers, untag the brokers you wish to remove.

To update the tags on the broker, use the following API:

`PUT /instances/{instanceName}/updateTags?tags=<comma separated tags>`

![updateTags API](<../../../.gitbook/assets/Screen Shot 2020-09-15 at 11.31.47 AM.png>)

Example for tagging the broker as per your custom tenant:

`PUT /instances/Broker_10.20.151.8_8000/updateTags?tags=customTenant_BROKER`

Example for untagging a broker:

`PUT /instances/Broker_10.20.151.8_8000/updateTags?tags=untagged_BROKER`

### Rebuild broker resource

After making any capacity changes to the broker, the brokerResource needs to be rebuilt. This can be done with the below API:

`POST /tables/{tableNameWithType}/rebuildBrokerResourceFromHelixTags`

![rebuildBrokerResource API](<../../../.gitbook/assets/Screen Shot 2020-09-15 at 11.35.29 AM.png>)

### Drop nodes

This is when you untagged and now want to remove the node from the cluster.&#x20;

First, shutdown the broker. Then, use API below to remove the node from the cluster.

`DELETE /instances/{instanceName}`

![](<../../../.gitbook/assets/Screen Shot 2020-09-15 at 11.38.37 AM.png>)

### Troubleshooting

If you encounter the below message when dropping, it means the broker process hasn't been shut down.&#x20;

```
Failed to drop instance Broker_10.1.10.51_8000 - 
    Instance Broker_10.1.10.51_8000 is still live
```

If you encounter below message, it means the broker has not been removed from the ideal state. Check the untagging and rebuild steps went through successfully.

```
Failed to drop instance Broker_172.17.0.2_8099 - 
    Instance Broker_172.17.0.2_8099 exists in ideal state for brokerResource
```
