---
description: Integrate with Superset
---

# Superset

## Start Superset with Docker Image

Start running [Superset Image](https://hub.docker.com/repository/docker/apachepinot/pinot-superset) with pre-built Superset Pinot connector.

{% tabs %}
{% tab title="Docker" %}
1. Run below command to start a standalone Superset deployment

```text
docker run \
  --network pinot-demo \
  --name=superset \
  -p 8088:8080 \
  -d apachepinot/pinot-superset:latest
```

2.1. \(First time\) Setup Admin account by running below command and follow instructions to set password.

```text
docker exec -it superset superset fab create-admin \
               --username admin \
               --firstname Superset \
               --lastname Admin \
               --email admin@superset.com \
               --password admin
```

2.2. \(First time\) DB upgrade and Initialize Superset 

```text
docker exec -it superset superset db upgrade
docker exec -it superset superset init
```

3. Import Pre-defined Pinot Datasources and Dashboard

```text
docker exec \
    -t superset \
    bash -c 'superset import_datasources -p /etc/examples/pinot/pinot_example_datasource_quickstart.yaml && \
             superset import_dashboards -p /etc/examples/pinot/pinot_example_dashboard.json'
```

4. Go to SuperSet UI: [http://localhost:8088/](http://localhost:8088/) to play around with dashboard.
{% endtab %}
{% endtabs %}

## Advanced Setup

### Adding Pinot database

In order to add Pinot cluster as a database, a SQLAlchemy URI is required.

The format of URI is:

`pinot://<pinot-broker-host>:<pinot-broker-port><pinot-broker-path>?controller=<pinot-controller-host>:<pinot-controller-port>`

E.g.

> `pinot://pinot-broker:9000/query/sql?controller=http://pinot-controller:9000/`

Below is an example for the QuickStart cluster, you can click `TEST CONNECTION` button to check if Pinot cluster is successfully connected.

![Add Pinot cluster as a new Database](../.gitbook/assets/image%20%2834%29.png)

