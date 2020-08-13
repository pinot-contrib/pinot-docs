---
description: Integrate with Superset
---

# Superset

Start running [Superset Image](https://hub.docker.com/repository/docker/apachepinot/pinot-superset) with pre-built Superset Pinot connector.

{% tabs %}
{% tab title="Docker" %}
1. Run below command to start a standalone Superset deployment

```text
docker run \
  --network pinot-demo \
  --name=superset \
  -p 8088:8088 \
  -d apachepinot/pinot-superset:latest
```

2.1. \(First time\) Setup Admin account by running below command and follow instructions to set password.

```text
docker exec \
    -it superset \
    bash -c 'export FLASK_APP=superset && flask fab create-admin'
```

Output:

![Superset Admin Command line Output](../.gitbook/assets/image%20%288%29.png)

2.2. \(First time\) DB upgrade and Initialize Superset

```text
docker exec \
    -t superset \
    bash -c 'superset db upgrade && superset init'
```

1. Import Pre-defined Pinot Datasources and Dashboard

```text
docker exec \
    -t superset \
    bash -c 'superset import_datasources -p /etc/examples/pinot/pinot_example_datasource_quickstart.yaml && \
             superset import_dashboards -p /etc/examples/pinot/pinot_example_dashboard.json'
```

1. Go to SuperSet UI: [http://localhost:8088/](http://localhost:8088/) to play around with dashboard.
{% endtab %}
{% endtabs %}

