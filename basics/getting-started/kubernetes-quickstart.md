---
description: Pinot quick start in Kubernetes
---

# Running in Kubernetes

## 1. Prerequisites

{% hint style="info" %}
This quickstart assumes that you already have a running Kubernetes cluster. Please follow the links below to set up a Kubernetes cluster.

* [Enable Kubernetes on Docker-Desktop](https://docs.docker.com/docker-for-mac/kubernetes/)
* [Install Minikube for local setup](https://kubernetes.io/docs/tasks/tools/install-minikube/) (make sure to run with enough resources e.g. `minikube start --vm=true --cpus=4 --memory=8g --disk-size=50g)`
* [Setup a Kubernetes Cluster using Amazon Elastic Kubernetes Service (Amazon EKS)](public-cloud-examples/aws-quickstart.md)
* [Setup a Kubernetes Cluster using Google Kubernetes Engine (GKE)](public-cloud-examples/gcp-quickstart.md)
* [Setup a Kubernetes Cluster using Azure Kubernetes Service (AKS)](public-cloud-examples/azure-quickstart.md)
{% endhint %}

## 2. Setting up a Pinot cluster in Kubernetes

Before continuing, please make sure that you've downloaded Apache Pinot. The scripts for the setup in this guide can be found in our open source project on GitHub.

The scripts can be found in the Pinot source at `./pinot/kubernetes/helm`

{% tabs %}
{% tab title="Git clone project source" %}
```bash
# checkout pinot
git clone https://github.com/apache/pinot.git
cd pinot/kubernetes/helm
```
{% endtab %}
{% endtabs %}

### 2.1 Start Pinot with Helm

{% tabs %}
{% tab title="Run Helm with Pre-installed Package" %}
Pinot repo has pre-packaged HelmCharts for Pinot and Presto. Helm Repo index file is [here](https://github.com/apache/pinot/blob/master/kubernetes/helm/index.yaml).

```
helm repo add pinot https://raw.githubusercontent.com/apache/pinot/master/kubernetes/helm
kubectl create ns pinot-quickstart
helm install pinot pinot/pinot \
    -n pinot-quickstart \
    --set cluster.name=pinot \
    --set server.replicaCount=2
```

**NOTE**: Please specify **StorageClass** based on your cloud vendor. For Pinot Server, please don't mount blob store like AzureFile/GoogleCloudStorage/S3 as the data serving file system.

Only use Amazon EBS/GCP Persistent Disk/Azure Disk style disks.

* For AWS: "**gp2**"
* For GCP: "**pd-ssd**" or "**standard**"
* For Azure: "**AzureDisk**"
* For Docker-Desktop: "**hostpath**"
{% endtab %}

{% tab title="Run Helm Script within Git Repo" %}
#### 2.1.1 Update helm dependency

```
helm dependency update
```

#### 2.1.2 Start Pinot with Helm

* For Helm **v2.12.1**

If your Kubernetes cluster is recently provisioned, ensure Helm is initialized by running:

```
helm init --service-account tiller
```

Then deploy a new HA Pinot cluster using the following command:

```
helm install --namespace "pinot-quickstart" --name "pinot" pinot
```

* For Helm **v3.0.0**

```
kubectl create ns pinot-quickstart
helm install -n pinot-quickstart pinot pinot
```

#### **2.1.3 Troubleshooting (For helm v2.12.1)**

* Error: Please run the below command if encountering the following issue:

```
Error: could not find tiller.
```

* Resolution:

```
kubectl -n kube-system delete deployment tiller-deploy
kubectl -n kube-system delete service/tiller-deploy
helm init --service-account tiller
```

* Error: Please run the command below if encountering a permission issue:

`Error: release pinot failed: namespaces "pinot-quickstart" is forbidden: User "system:serviceaccount:kube-system:default" cannot get resource "namespaces" in API group "" in the namespace "pinot-quickstart"`

* Resolution:

```
kubectl apply -f helm-rbac.yaml
```
{% endtab %}
{% endtabs %}

### **2.2 Check Pinot deployment status**

```
kubectl get all -n pinot-quickstart
```

## 3. Load data into Pinot using Kafka

### **3.1 Bring up a Kafka cluster for real-time data ingestion**

{% tabs %}
{% tab title="For Helm v3.0.0" %}
```
helm repo add incubator https://charts.helm.sh/incubator
helm install -n pinot-quickstart kafka incubator/kafka --set replicas=1,zookeeper.image.tag=latest
```
{% endtab %}

{% tab title="For Helm v2.12.1" %}
```
helm repo add incubator https://charts.helm.sh/incubator
helm install --namespace "pinot-quickstart"  --name kafka incubator/kafka --set zookeeper.image.tag=latest 
```
{% endtab %}
{% endtabs %}

### 3.2 Check Kafka deployment status

```
kubectl get all -n pinot-quickstart | grep kafka
```

Ensure the Kafka deployment is ready before executing the scripts in the following next steps.

```
pod/kafka-0                                                 1/1     Running     0          2m
pod/kafka-zookeeper-0                                       1/1     Running     0          10m
pod/kafka-zookeeper-1                                       1/1     Running     0          9m
pod/kafka-zookeeper-2                                       1/1     Running     0          8m
```

### **3.3 Create Kafka topics**

The scripts below will create two Kafka topics for data ingestion:

```
kubectl -n pinot-quickstart exec kafka-0 -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic flights-realtime --create --partitions 1 --replication-factor 1
kubectl -n pinot-quickstart exec kafka-0 -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic flights-realtime-avro --create --partitions 1 --replication-factor 1
```

### **3.4 Load data into Kafka and create Pinot schema/tables**

The script below will deploy 3 batch jobs.

* Ingest 19492 JSON messages to Kafka topic `flights-realtime` at a speed of 1 msg/sec
* Ingest 19492 Avro messages to Kafka topic `flights-realtime-avro` at a speed of 1 msg/sec
* Upload Pinot schema `airlineStats`
* Create Pinot table `airlineStats` to ingest data from JSON encoded Kafka topic `flights-realtime`
* Create Pinot table `airlineStatsAvro` to ingest data from Avro encoded Kafka topic `flights-realtime-avro`

```
kubectl apply -f pinot/pinot-realtime-quickstart.yml
```

## 4. Query using Pinot Data Explorer

### 4.1 Pinot Data Explorer

Please use the script below to perform local port-forwarding, which will also open Pinot query console in your default web browser.

This script can be found in the Pinot source at `./pinot/kubernetes/helm/pinot`

```
./query-pinot-data.sh
```

## 5. Using Superset to query Pinot

### 5.1 Bring up Superset using helm

Install SuperSet Helm Repo

```
helm repo add superset https://apache.github.io/superset
```

Get Helm values config file:

```
helm inspect values superset/superset > /tmp/superset-values.yaml
```

Edit `/tmp/superset-values.yaml` file and add `pinotdb` pip dependency into `bootstrapScript` field, so Superset will install pinot dependencies during bootstrap time.

You can also build your own image with this dependency or just use image: `apachepinot/pinot-superset:latest` instead.

![](<../../.gitbook/assets/image (31).png>)

Also remember to change the admin credential inside the `init` section with meaningful user profile and stronger password.

![](<../../.gitbook/assets/image (8).png>)

Install Superset using helm

```
kubectl create ns superset
helm upgrade --install --values /tmp/superset-values.yaml superset superset/superset -n superset
```

Ensure your cluster is up by running:

```
kubectl get all -n superset
```

### 5.2 Access Superset UI

You can run the below command to port forward superset to your `localhost:18088`. Then you can navigate superset in your browser with the previous set admin credential.

```
kubectl port-forward service/superset 18088:8088 -n superset
```

Create Pinot Database using URI:

`pinot+http://pinot-broker.pinot-quickstart:8099/query?controller=http://pinot-controller.pinot-quickstart:9000/`

![](<../../.gitbook/assets/image (42).png>)

Once the database is added, you can add more data sets and explore the dashboarding.

## 6. Access Pinot using Trino

### 6.1 Deploy Trino

You can run the command below to deploy Trino with the Pinot plugin installed.

```
helm repo add trino https://trinodb.github.io/charts/
```

The above command adds Trino HelmChart repo. You can then run the below command to see the charts.

```
helm search repo trino
```

In order to connect Trino to Pinot, we need to add Pinot catalog, which requires extra configurations. You can run the below command to get all the configurable values.

```
helm inspect values trino/trino > /tmp/trino-values.yaml
```

To add Pinot catalog, you can edit the `additionalCatalogs` section by adding:

```
additionalCatalogs:
  pinot: |
    connector.name=pinot
    pinot.controller-urls=pinot-controller.pinot-quickstart:9000
```

{% hint style="info" %}
Pinot is deployed at namespace `pinot-quickstart`, so the controller serviceURL is `pinot-controller.pinot-quickstart:9000`
{% endhint %}

After modifying the `/tmp/trino-values.yaml` file, you can deploy Trino with:

```
kubectl create ns trino-quickstart
helm install my-trino trino/trino --version 0.2.0 -n trino-quickstart --values /tmp/trino-values.yaml
```

Once you deployed the Trino, You can check Trino deployment status by:

```
kubectl get pods -n trino-quickstart
```

![](<../../.gitbook/assets/image (60).png>)

### 6.2 Query Trino using Trino CLI

Once Trino is deployed, you can run the below command to get a runnable Trino CLI.

#### **6.2.1 Download Trino CLI**

```
curl -L https://repo1.maven.org/maven2/io/trino/trino-cli/363/trino-cli-363-executable.jar -o /tmp/trino && chmod +x /tmp/trino
```

**6.2.2 Port forward Trino service to your local if it's not already exposed**

```
echo "Visit http://127.0.0.1:18080 to use your application"
kubectl port-forward service/my-trino 18080:8080 -n trino-quickstart
```

**6.2.3 Use Trino console client to connect to Trino service**

```
/tmp/trino --server localhost:18080 --catalog pinot --schema default
```

**6.2.4 Query Pinot data using Trino CLI**

![](<../../.gitbook/assets/image (6).png>)

### 6.3 Sample queries to execute

* List all catalogs

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

* List All tables

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

* Show schema

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

* Count total documents

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

## 7. Access Pinot using Presto

### 7.1 Deploy Presto using Pinot plugin

You can run the command below to deploy a customized Presto with the Pinot plugin installed.

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

The above command deploys Presto with default configs. For customizing your deployment, you can run the below command to get all the configurable values.

```
helm inspect values pinot/presto > /tmp/presto-values.yaml
```

After modifying the `/tmp/presto-values.yaml` file, you can deploy Presto with:

```
helm install presto pinot/presto -n pinot-quickstart --values /tmp/presto-values.yaml
```

Once you deployed the Presto, You can check Presto deployment status by:

```
kubectl get pods -n pinot-quickstart
```

![Sample Output of K8s Deployment Status](https://lh3.googleusercontent.com/t4LnQL4xalac-ObeF37LvtrroHzfgr84lYv3av\_MI1NWIcUG1Kuc9uDmJHdYbyJiEfLuBdvT3451VS49lGO\_i167m82EM2ZfWk84Zvj-Hib8hHLI8mZt20akpdEh3BLV1Q4ETaL\_)

### 7.2 Query Presto using Presto CLI

Once Presto is deployed, you can run the below command from [here](https://github.com/apache/pinot/blob/master/kubernetes/helm/presto/pinot-presto-cli.sh), or just follow steps 6.2.1 to 6.2.3.

```
./pinot-presto-cli.sh
```

#### **6.2.1 Download Presto CLI**

```
curl -L https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.246/presto-cli-0.246-executable.jar -o /tmp/presto-cli && chmod +x /tmp/presto-cli
```

**6.2.2 Port forward presto-coordinator port 8080 to localhost port 18080**

```
kubectl port-forward service/presto-coordinator 18080:8080 -n pinot-quickstart> /dev/null &
```

#### **6.2.3 Start Presto CLI with pinot catalog to query it then query it**

```
/tmp/presto-cli --server localhost:18080 --catalog pinot --schema default
```

6.2.4 Query Pinot data using Presto CLI

![](https://lh3.googleusercontent.com/e5h4FIpvLjSiLi9J2WeABD8CAhtxj-vjyzjgj4pgmtkY-0o3uVr-qNHlOrFV3RGTu8ah4VFtLw5vqAABTATvTjLF5g2E6VnpDKRweAp\_akfD7EeabgXVr2ObbUMIsDZ9pibO1a9j)

### 7.3 Sample queries to execute

* List all catalogs

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

* List All tables

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

* Show schema

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

* Count total documents

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

## 8. Deleting the Pinot cluster in Kubernetes

```
kubectl delete ns pinot-quickstart
```

<mark style="color:red;">Note:</mark> These are sample configs to be used as reference. For production setup, you may want to customize it to your needs.
