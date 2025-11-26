---
description: Pinot quick start in Kubernetes
---

# Running in Kubernetes

Get started running Pinot in Kubernetes.

{% hint style="info" %}
<mark style="color:red;">Note:</mark> The examples in this guide are sample configurations to be used as reference. For production setup, you may want to customize it to your needs.
{% endhint %}

## Prerequisites

### Kubernetes

This guide assumes that you already have a running Kubernetes cluster.

If you haven't yet set up a Kubernetes cluster, see the links below for instructions:

* [Enable Kubernetes on Docker-Desktop](https://docs.docker.com/docker-for-mac/kubernetes/)
* [Install Minikube for local setup](https://kubernetes.io/docs/tasks/tools/install-minikube/)
  * Make sure to run with enough resources: `minikube start --vm=true --cpus=4 --memory=8g --disk-size=50g`
* [Set up a Kubernetes Cluster using Amazon Elastic Kubernetes Service (Amazon EKS)](public-cloud-examples/aws-quickstart.md)
* [Set up a Kubernetes Cluster using Google Kubernetes Engine (GKE)](public-cloud-examples/gcp-quickstart.md)
* [Set up a Kubernetes Cluster using Azure Kubernetes Service (AKS)](public-cloud-examples/azure-quickstart.md)

### Pinot

Make sure that you've downloaded Apache Pinot. The scripts for the setup in this guide can be found in our[ open source project on GitHub](https://github.com/apache/pinot).

{% tabs %}
{% tab title="Git clone project source" %}
```bash
# checkout pinot
git clone https://github.com/apache/pinot.git
cd pinot/helm/pinot
```
{% endtab %}
{% endtabs %}

## Set up a Pinot cluster in Kubernetes

### Start Pinot with Helm

{% tabs %}
{% tab title="Run Helm with pre-installed package" %}
The Pinot repository has pre-packaged Helm charts for Pinot and Presto. The Helm repository index file is [here](https://github.com/apache/pinot/blob/master/helm/index.yaml).

```bash
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/helm
kubectl create ns pinot-quickstart
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot \
    --set server.replicaCount=2
```

**Note**: Specify **StorageClass** based on your cloud vendor. Don't mount a blob store (such as AzureFile, GoogleCloudStorage, or S3) as the data serving file system. Use only Amazon EBS/GCP Persistent Disk/Azure Disk-style disks.

* For AWS: "**gp2**"
* For GCP: "**pd-ssd**" or "**standard**"
* For Azure: "**AzureDisk**"
* For Docker-Desktop: "**hostpath**"
{% endtab %}

{% tab title="Run Helm script within Git repo" %}
**1.1.1 Update Helm dependency**

```bash
helm dependency update
```

**1.1.2 Start Pinot with Helm**

```bash
kubectl create ns pinot-quickstart
helm install -n pinot-quickstart pinot ./pinot
```
{% endtab %}
{% endtabs %}

### **Check Pinot deployment status**

```
kubectl get all -n pinot-quickstart
```

## Load data into Pinot using Kafka

### **Bring up a Kafka cluster for real-time data ingestion**

```bash
helm repo add kafka https://charts.bitnami.com/bitnami
helm install -n pinot-quickstart kafka kafka/kafka --set replicas=1,zookeeper.image.tag=latest,listeners.client.protocol=PLAINTEXT
```

### Check Kafka deployment status

Ensure the Kafka deployment is ready before executing the scripts in the following steps. Run the following command:

```bash
kubectl get all -n pinot-quickstart | grep kafka
```

Below is an example output showing the deployment is ready:

```
pod/kafka-controller-0                   1/1     Running     0          2m
pod/kafka-controller-1                   1/1     Running     0          2m
pod/kafka-controller-2                   1/1     Running     0          2m
```

### **Create Kafka topics**

Run the scripts below to create two Kafka topics for data ingestion:

```bash
kubectl -n pinot-quickstart exec kafka-controller-0 -- kafka-topics.sh --bootstrap-server kafka:9092 --topic flights-realtime --create --partitions 1 --replication-factor 1
kubectl -n pinot-quickstart exec kafka-controller-0 -- kafka-topics.sh --bootstrap-server kafka:9092 --topic flights-realtime-avro --create --partitions 1 --replication-factor 1
```

### **Load data into Kafka and create Pinot schema/tables**

The script below does the following:

* Ingests 19492 JSON messages to Kafka topic `flights-realtime` at a speed of 1 msg/sec
* Ingests 19492 Avro messages to Kafka topic `flights-realtime-avro` at a speed of 1 msg/sec
* Uploads Pinot schema `airlineStats`
* Creates Pinot table `airlineStats` to ingest data from JSON encoded Kafka topic `flights-realtime`
* Creates Pinot table `airlineStatsAvro` to ingest data from Avro encoded Kafka topic `flights-realtime-avro`

```bash
kubectl apply -f pinot/helm/pinot/pinot-realtime-quickstart.yml
```

## Query with the Pinot Data Explorer

### Pinot Data Explorer

The following script (located at `./pinot/helm/pinot`) performs local port forwarding, and opens the Pinot query console in your default web browser.

```bash
./query-pinot-data.sh
```

## Query Pinot with Superset

### Bring up Superset using Helm

1. Install the SuperSet Helm repository:

```bash
helm repo add superset https://apache.github.io/superset
```

2. Get the Helm values configuration file:

```bash
helm inspect values superset/superset > /tmp/superset-values.yaml
```

3. For Superset to install Pinot dependencies, edit `/tmp/superset-values.yaml` file to add a`pinotdb` pip dependency into `bootstrapScript` field.
4. You can also build your own image with this dependency or use the image `apachepinot/pinot-superset:latest` instead.

![](../../.gitbook/assets/kubernetes-build-image.png)

5. Replace the default admin credentials inside the `init` section with a meaningful user profile and stronger password.
6. Install Superset using Helm:

```bash
kubectl create ns superset
helm upgrade --install --values /tmp/superset-values.yaml superset superset/superset -n superset
```

7. Ensure your cluster is up by running:

```bash
kubectl get all -n superset
```

### Access the Superset UI

1. Run the below command to port forward Superset to your `localhost:18088`.

```bash
kubectl port-forward service/superset 18088:8088 -n superset
```

2. Navigate to Superset in your browser with the admin credentials you set in the previous section.
3. Create a new database connection with the following URI: `pinot+http://pinot-broker.pinot-quickstart:8099/query?controller=http://pinot-controller.pinot-quickstart:9000/`
4. Once the database is added, you can add more data sets and explore the dashboard options.

## Access Pinot with Trino

### Deploy Trino

1. Deploy Trino with the Pinot plugin installed:

```bash
helm repo add trino https://trinodb.github.io/charts/
```

2. See the charts in the Trino Helm chart repository:

```bash
helm search repo trino
```

3. In order to connect Trino to Pinot, you'll need to add the Pinot catalog, which requires extra configurations. Run the below command to get all the configurable values.

```bash
helm inspect values trino/trino > /tmp/trino-values.yaml
```

4. To add the Pinot catalog, edit the `additionalCatalogs` section by adding:

```
additionalCatalogs:
  pinot: |
    connector.name=pinot
    pinot.controller-urls=pinot-controller.pinot-quickstart:9000
```

{% hint style="info" %}
Pinot is deployed at namespace `pinot-quickstart`, so the controller serviceURL is `pinot-controller.pinot-quickstart:9000`
{% endhint %}

5. After modifying the `/tmp/trino-values.yaml` file, deploy Trino with:

```bash
kubectl create ns trino-quickstart
helm install my-trino trino/trino --version 0.2.0 -n trino-quickstart --values /tmp/trino-values.yaml
```

6. Once you've deployed Trino, check the deployment status:

```bash
kubectl get pods -n trino-quickstart
```

![](../../.gitbook/assets/trino-deployment-status.png)

### Query Pinot with the Trino CLI

Once Trino is deployed, run the below command to get a runnable Trino CLI.

1. Download the Trino CLI:

```bash
curl -L https://repo1.maven.org/maven2/io/trino/trino-cli/363/trino-cli-363-executable.jar -o /tmp/trino && chmod +x /tmp/trino
```

2. Port forward Trino service to your local if it's not already exposed:

```bash
echo "Visit http://127.0.0.1:18080 to use your application"
kubectl port-forward service/my-trino 18080:8080 -n trino-quickstart
```

3. Use the Trino console client to connect to the Trino service:

```bash
/tmp/trino --server localhost:18080 --catalog pinot --schema default
```

4. Query Pinot data using the Trino CLI, like in the sample queries below.

### Sample queries to execute

#### List all catalogs

```
trino:default> show catalogs;
```

```
  Catalog
---------
 pinot
 system
 tpcds
 tpch
(4 rows)

Query 20211025_010256_00002_mxcvx, FINISHED, 2 nodes
Splits: 36 total, 36 done (100.00%)
0.70 [0 rows, 0B] [0 rows/s, 0B/s]
```

#### List all tables

```
trino:default> show tables;
```

```
    Table
--------------
 airlinestats
(1 row)

Query 20211025_010326_00003_mxcvx, FINISHED, 3 nodes
Splits: 36 total, 36 done (100.00%)
0.28 [1 rows, 29B] [3 rows/s, 104B/s]
```

#### Show schema

```
trino:default> DESCRIBE airlinestats;
```

```
        Column        |      Type      | Extra | Comment
----------------------+----------------+-------+---------
 flightnum            | integer        |       |
 origin               | varchar        |       |
 quarter              | integer        |       |
 lateaircraftdelay    | integer        |       |
 divactualelapsedtime | integer        |       |
 divwheelsons         | array(integer) |       |
 divwheelsoffs        | array(integer) |       |
......

Query 20211025_010414_00006_mxcvx, FINISHED, 3 nodes
Splits: 36 total, 36 done (100.00%)
0.37 [79 rows, 5.96KB] [212 rows/s, 16KB/s]
```

#### Count total documents

```
trino:default> select count(*) as cnt from airlinestats limit 10;
```

```
 cnt
------
 9746
(1 row)

Query 20211025_015607_00009_mxcvx, FINISHED, 2 nodes
Splits: 17 total, 17 done (100.00%)
0.24 [1 rows, 9B] [4 rows/s, 38B/s]
```

## Access Pinot with Presto

### Deploy Presto with the Pinot plugin

1. First, deploy Presto with default configurations:

{% tabs %}
{% tab title="Helm" %}
```
helm install presto pinot/presto -n pinot-quickstart
```
{% endtab %}

{% tab title="K8s Scripts" %}
```
kubectl apply -f presto-coordinator.yaml
```
{% endtab %}
{% endtabs %}

2. To customize your deployment, run the below command to get all the configurable values.

```
helm inspect values pinot/presto > /tmp/presto-values.yaml
```

3. After modifying the `/tmp/presto-values.yaml` file, deploy Presto:

```
helm install presto pinot/presto -n pinot-quickstart --values /tmp/presto-values.yaml
```

4. Once you've deployed the Presto instance, check the deployment status:

```
kubectl get pods -n pinot-quickstart
```

![Sample Output of K8s Deployment Status](https://lh3.googleusercontent.com/t4LnQL4xalac-ObeF37LvtrroHzfgr84lYv3av\_MI1NWIcUG1Kuc9uDmJHdYbyJiEfLuBdvT3451VS49lGO\_i167m82EM2ZfWk84Zvj-Hib8hHLI8mZt20akpdEh3BLV1Q4ETaL\_)

### Query Presto using the Presto CLI

Once Presto is deployed, you can run the below command from [here](https://github.com/apache/pinot/blob/master/kubernetes/helm/presto/pinot-presto-cli.sh), or follow the steps below.

```bash
./pinot-presto-cli.sh
```

1. Download the Presto CLI:

```bash
curl -L https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.246/presto-cli-0.246-executable.jar -o /tmp/presto-cli && chmod +x /tmp/presto-cli
```

2. Port forward `presto-coordinator` port 8080 to `localhost` port 18080:

```bash
kubectl port-forward service/presto-coordinator 18080:8080 -n pinot-quickstart> /dev/null &
```

3. Start the Presto CLI with the Pinot catalog:

```bash
/tmp/presto-cli --server localhost:18080 --catalog pinot --schema default
```

4. Query Pinot data with the Presto CLI, like in the sample queries below.

### Sample queries to execute

#### List all catalogs

```
presto:default> show catalogs;
```

```
 Catalog
---------
 pinot
 system
(2 rows)

Query 20191112_050827_00003_xkm4g, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0:01 [0 rows, 0B] [0 rows/s, 0B/s]
```

#### List all tables

```
presto:default> show tables;
```

```
    Table
--------------
 airlinestats
(1 row)

Query 20191112_050907_00004_xkm4g, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0:01 [1 rows, 29B] [1 rows/s, 41B/s]
```

#### Show schema

```
presto:default> DESCRIBE pinot.dontcare.airlinestats;
```

```
        Column        |  Type   | Extra | Comment
----------------------+---------+-------+---------
 flightnum            | integer |       |
 origin               | varchar |       |
 quarter              | integer |       |
 lateaircraftdelay    | integer |       |
 divactualelapsedtime | integer |       |
......

Query 20191112_051021_00005_xkm4g, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0:02 [80 rows, 6.06KB] [35 rows/s, 2.66KB/s]
```

#### Count total documents

```
presto:default> select count(*) as cnt from pinot.dontcare.airlinestats limit 10;
```

```
 cnt
------
 9745
(1 row)

Query 20191112_051114_00006_xkm4g, FINISHED, 1 node
Splits: 17 total, 17 done (100.00%)
0:00 [1 rows, 8B] [2 rows/s, 19B/s]
```

## Delete a Pinot cluster in Kubernetes

To delete your Pinot cluster in Kubernetes, run the following command:

```bash
kubectl delete ns pinot-quickstart
```
