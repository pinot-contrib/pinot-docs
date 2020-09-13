# Monitor Pinot using Prometheus and Grafana

Here we will introduce how to monitor Pinot with Prometheus and Grafana in Kubernetes environment.

## Prerequisite

* Kubernetes v1.16.5
* HelmCharts v3.1.2

## Deploy Pinot

### Install Pinot helm repo

```text
## Adding Pinot helm repo
helm repo add pinot https://raw.githubusercontent.com/apache/incubator-pinot/master/kubernetes/helm
## Extract all the configurable values of Pinot Helm into a config.
helm inspect values pinot/pinot > /tmp/pinot-values.yaml
```

### Configure Pinot Helm to enable Prometheus JMX Exporter

1. Configure jvmOpts:

Add [JMX Prometheus Java Agent](https://github.com/prometheus/jmx_exporter) to `controller.jvmOpts` / `broker.jvmOpts`/ `server.jvmOpts` . Note that Pinot image already packages `jmx_prometheus_javaagent-0.12.0.jar`.

Below config will expose pinot metrics to port 8008 for Prometheus to scrape.

```text
controller:
  ...
  jvmOpts: "-javaagent:/opt/pinot/etc/jmx_prometheus_javaagent/jmx_prometheus_javaagent-0.12.0.jar=8008:/opt/pinot/etc/jmx_prometheus_javaagent/configs/pinot.yml -Xms256M -Xmx1G"
```

You can port forward port 8008 to local and access metrics though: [http://localhost:8008/metrics](http://localhost:8008/metrics)

2. Configure service annotations:

Add prometheus related annotations to enable prometheus to scrape metrics.  

* `controller.service.annotations` 
* `broker.service.annotations`
* `server.service.annotations`
* `controller.podAnnotations` 
* `broker.podAnnotations`
* `server.podAnnotations`

```text
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

```text
kubectl create ns pinot
helm install pinot pinot/pinot -n pinot --values /tmp/pinot-values.yaml
```

## Deploy Prometheus

Once Pinot is deployed and running, we can start deploy Prometheus.

Similar to Pinot Helm, we will have Prometheus Helm and it's config yaml file:

```text
helm inspect values stable/prometheus > /tmp/prometheus-values.yaml
```

Configure Prometheus

Please remember to check the configs: 

* server.persistentVolume: data storage location/size limit/storage class
* server.retention: how long to keep the data \(default is 15d\)

Deploy Prometheus

```text
kubectl create ns prometheus
helm install prometheus stable/prometheus -n prometheus --values /tmp/prometheus-values.yaml
```

Access Prometheus

Port forward Prometheus service to local and open the page on `localhost:30080`

```text
kubectl port-forward service/prometheus-server 30080:80 -n prometheus
```

Then we can query metrics Prometheus scrapped:

![](../../.gitbook/assets/image%20%2842%29.png)

## Deploy Grafana

Similar to Pinot Helm, we will have Grafana Helm and it's config yaml file:

```text
helm inspect values stable/grafana > /tmp/grafana-values.yaml
```

* Configure Grafana



* Deploy Grafana

```text
kubectl create ns grafana
helm install grafana stable/grafana -n grafana --values /tmp/grafana-values.yaml
```

* Get Password to access Grafana

```text
kubectl get secret --namespace grafana grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

* Access Grafana dashboard 

You can access it locally through port forwarding:

```text
kubectl port-forward service/grafana 20080:80 -n grafana
```

 Once open the dashboard, you can login with credential: 

`admin`/`[ PASSWORD GET FROM PREVIOUS STEP]` 

![Grafana Dashboard](../../.gitbook/assets/image%20%2847%29.png)

* Add data source

![](../../.gitbook/assets/image%20%2844%29.png)

Click on Prometheus and set HTTP URL to : `http://prometheus-server.prometheus.svc.cluster.local`

![Prometheus data source config](../../.gitbook/assets/image%20%2848%29.png)

* Configure Pinot Dashboard

Once data source is added, we can import a Pinot Dashboard:

![Grafana Import Button](../../.gitbook/assets/image%20%2845%29.png)

A sample Pinot dashboard JSON is:

{% file src="../../.gitbook/assets/pinot-1599691007230.json" caption="sample-pinot-dashboard" %}

Now you can upload this file and select Prometheus as data source to finish the import

![Grafana Import Page](../../.gitbook/assets/image%20%2846%29.png)

Then you can explore and make your own Pinot dashboard!

![Pinot Dashboard](../../.gitbook/assets/image%20%2843%29.png)







