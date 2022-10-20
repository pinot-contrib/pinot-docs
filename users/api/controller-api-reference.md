---
description: All user APIs available in Pinot
---

# Controller API Reference

The full up-to-date list of APIs can be viewed on Swagger.

## Cluster

### GET /cluster/configs

List all the cluster configs. These are fetched from Zookeeper from the CONFIGS/CLUSTER/\<clusterName> znode.

**Request**

```
curl -X GET "http://localhost:9000/cluster/configs" -H "accept: application/json"
```

**Response**&#x20;

```
{
  "allowParticipantAutoJoin": "true",
  "enable.case.insensitive": "false",
  "pinot.broker.enable.query.limit.override": "false",
  "default.hyperloglog.log2m": "8"
}
```

### POST /cluster/configs

Post new configs to cluster. These will get stored in the same znode as above i.e. CONFIGS/CLUSTER/\<clusterName>. These properties are appended to the existing properties if keys are new, else they will be updated if key already exists.&#x20;

**Request**

```
curl -X POST "http://localhost:9000/cluster/configs" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d "{ \"pinot.helix.instance.state.maxStateTransitions\" : \"20\", \"custom.cluster.prop\": \"foo\"}"
```

**Response**&#x20;

```
{
  "status": "Updated cluster config."
}
```

### DELETE /cluster/configs

Delete a cluster config.&#x20;

**Request**

```
curl -X DELETE "http://localhost:9000/cluster/configs/custom.cluster.prop" 
```

**Response**&#x20;

```
{
  "status": "Deleted cluster config: custom.cluster.prop"
}
```

### GET /cluster/info

Gets cluster related info, such as cluster name

**Request**

```
curl -X GET "http://localhost:9000/cluster/info" -H "accept: application/json"
```

**Response**&#x20;

```
{
  "clusterName": "QuickStartCluster"
}
```

## Health

### GET /health

Check controller health. Status are OK or WebApplicationException with ServiceUnavailable and message

**Request**

```
curl -X GET "http://localhost:9000/health" -H "accept: text/plain"
```

**Response**

```
OK
```

## Leader

### GET /leader/tables&#x20;

Gets the leader resource map, which shows the tables that are mapped to each leader.

**Request**

```
curl -X GET "http://localhost:9000/leader/tables" -H "accept: application/json"
```

**Response**

{% code overflow="wrap" %}
```
{
  "leadControllerEntryMap": {
    "leadControllerResource_0": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_1": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_2": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_3": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_4": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_5": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_6": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_7": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "baseballStats_OFFLINE"
      ]
    },
    "leadControllerResource_8": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "dimBaseballTeams_OFFLINE",
        "starbucksStores_OFFLINE"
      ]
    },
    "leadControllerResource_9": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "billing_OFFLINE"
      ]
    },
    "leadControllerResource_10": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_11": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_12": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_13": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "githubComplexTypeEvents_OFFLINE"
      ]
    },
    "leadControllerResource_14": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_15": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "githubEvents_OFFLINE"
      ]
    },
    "leadControllerResource_16": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_17": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_18": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_19": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "airlineStats_OFFLINE"
      ]
    },
    "leadControllerResource_20": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_21": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_22": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    },
    "leadControllerResource_23": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": []
    }
  },
  "leadControllerResourceEnabled": true
}
```
{% endcode %}

### GET /leader/tables/\<tableName>

Gets the leaders for the specific table

**Request**

```
curl -X GET "http://localhost:9000/leader/tables/baseballStats" -H "accept: application/json"
```

**Response**

```
{
  "leadControllerEntryMap": {
    "leadControllerResource_7": {
      "leadControllerId": "Controller_192.168.1.24_9000",
      "tableNames": [
        "baseballStats"
      ]
    }
  },
  "leadControllerResourceEnabled": true
}
```

## Table

### GET /debug/tables/\<tableName>

Debug information for the table, which includes metadata and error status about segments, ingestion, servers and brokers of the table

**Request**

```
curl -X GET "http://localhost:9000/debug/tables/baseballStats?type=OFFLINE&verbosity=0" -H "accept: application/json"
```

**Response**

```
[
  {
    "tableName": "baseballStats_OFFLINE",
    "numSegments": 1,
    "numServers": 1,
    "numBrokers": 1,
    "segmentDebugInfos": [],
    "serverDebugInfos": [],
    "brokerDebugInfos": [],
    "tableSize": {
      "reportedSize": "3 MB",
      "estimatedSize": "3 MB"
    },
    "ingestionStatus": {
      "ingestionState": "HEALTHY",
      "errorMessage": ""
    }
  }
]
```

