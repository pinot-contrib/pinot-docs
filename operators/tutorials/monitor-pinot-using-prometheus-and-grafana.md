# Monitor Pinot using Prometheus and Grafana

Here we will introduce how to monitor Pinot with Prometheus and Grafana in Kubernetes environment.

## Prerequisite

* Kubernetes v1.16.5
* HelmCharts v3.1.2

## Deploy Pinot

### Install Pinot helm repo

```
## Adding Pinot helm repo
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/kubernetes/helm
## Extract all the configurable values of Pinot Helm into a config.
helm inspect values pinot/pinot > /tmp/pinot-values.yaml
```

### Configure Pinot Helm to enable Prometheus JMX Exporter

1\. Configure jvmOpts:

Add [JMX Prometheus Java Agent](https://github.com/prometheus/jmx\_exporter) to `controller.jvmOpts` / `broker.jvmOpts`/ `server.jvmOpts` . Note that Pinot Docker image already packages `jmx_prometheus_javaagent.jar`.

Below config will expose pinot metrics to port 8008 for Prometheus to scrape.

```
controller:
  ...
  jvmOpts: "-javaagent:/opt/pinot/etc/jmx_prometheus_javaagent/jmx_prometheus_javaagent.jar=8008:/opt/pinot/etc/jmx_prometheus_javaagent/configs/pinot.yml -Xms256M -Xmx1G"
```

You can port forward port 8008 to local and access metrics though: [http://localhost:8008/metrics](http://localhost:8008/metrics)

![Sample output of JMX metrics](<../../.gitbook/assets/image (21).png>)

2\. Configure service annotations:

Add Prometheus related annotations to enable Prometheus to scrape metrics.

* `controller.service.annotations`
* `broker.service.annotations`
* `server.service.annotations`
* `controller.podAnnotations`
* `broker.podAnnotations`
* `server.podAnnotations`

```
controller:
  ...
  service:
    annotations:
      "prometheus.io/scrape": "true"
      "prometheus.io/port": "8008"
  ...
  podAnnotations:
    "prometheus.io/scrape": "true"
    "prometheus.io/port": "8008"
```

### Deploy Pinot Helm

```
kubectl create ns pinot
helm install pinot pinot/pinot -n pinot --values /tmp/pinot-values.yaml
```

## Deploy Prometheus

Once Pinot is deployed and running, we can start deploy Prometheus.

Similar to Pinot Helm, we will have Prometheus Helm and its config yaml file:

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm inspect values prometheus-community/prometheus > /tmp/prometheus-values.yaml
```

Configure Prometheus

Remember to check the configs:

* server.persistentVolume: data storage location/size limit/storage class
* server.retention: how long to keep the data (default is 15d)

Deploy Prometheus

```
kubectl create ns prometheus
helm install prometheus prometheus-community/prometheus -n prometheus --values /tmp/prometheus-values.yaml
```

Access Prometheus

Port forward Prometheus service to local and open the page on `localhost:30080`

```
kubectl port-forward service/prometheus-server 30080:80 -n prometheus
```

Then we can query metrics Prometheus scrapped:

![](<../../.gitbook/assets/image (23).png>)

## Deploy Grafana

Similar to Pinot Helm, we will have Grafana Helm and it's config yaml file:

```
helm repo add grafana https://grafana.github.io/helm-charts
helm inspect values grafana/grafana > /tmp/grafana-values.yaml
```

* Configure Grafana
* Deploy Grafana

```
kubectl create ns grafana
helm install grafana grafana/grafana -n grafana --values /tmp/grafana-values.yaml
```

* Get Password to access Grafana

```
kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

* Access Grafana dashboard

You can access it locally through port forwarding:

```
kubectl port-forward service/grafana 20080:80 -n grafana
```

Once open the dashboard, you can login with credential:

`admin`/`[ PASSWORD GET FROM PREVIOUS STEP]`

![Grafana Dashboard](<../../.gitbook/assets/image (47) (1).png>)

* Add data source

![](<../../.gitbook/assets/image (35).png>)

Click on Prometheus and set HTTP URL to : `http://prometheus-server.prometheus.svc.cluster.local`

![Prometheus data source config](<../../.gitbook/assets/image (20).png>)

* Configure Pinot Dashboard

Once data source is added, we can import a Pinot Dashboard:

![Grafana Import Button](<../../.gitbook/assets/image (48).png>)

A sample Pinot dashboard JSON is:

{% file src="../../.gitbook/assets/Pinot-1601334866100.json" %}
sample-pinot-dashboard
{% endfile %}

Now you can upload this file and select Prometheus as data source to finish the import

![Grafana Import Page](<../../.gitbook/assets/image (15).png>)

Then you can explore and make your own Pinot dashboard!

![](<../../.gitbook/assets/image (12).png>)

![](<../../.gitbook/assets/image (14).png>)

![](<../../.gitbook/assets/image (28).png>)

![](<../../.gitbook/assets/image (55).png>)

![](<../../.gitbook/assets/image (16).png>)
