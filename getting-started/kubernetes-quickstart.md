---
description: Pinot Quickstart in Kubernetes
---

# Running Pinot in Kubernetes

## 1. Prerequisite

This QuickStart assumes the existence of Kubernetes Cluster. Please follow below links to setup your Kubernetes cluster in local or major cloud vendors.

* [Enable Kubernetes on Docker-Desktop](https://docs.docker.com/docker-for-mac/kubernetes/)
* [Install Minikube for local setup](https://kubernetes.io/docs/tasks/tools/install-minikube/)
* [Setup a Kubernetes Cluster using Amazon Elastic Kubernetes Service \(Amazon EKS\)](quickstart/aws-quickstart.md)
* [Setup a Kubernetes Cluster using Google Kubernetes Engine\(GKE\)](quickstart/gcp-quickstart.md)
* [Setup a Kubernetes Cluster using Azure Kubernetes Service \(AKS\)](quickstart/azure-quickstart.md)

## 2. Setup a Pinot cluster for demo

### 2.1 Update helm dependency

```text
helm dependency update
```

### 2.2 Start Pinot with Helm

* For Helm v2.12.1

If cluster is just initialized, ensure helm is initialized by running:

```text
helm init --service-account tiller
```

Then deploy pinot cluster by:

```text
helm install --namespace "pinot-quickstart" --name "pinot" .
```

* For Helm v3.0.0

```text
kubectl create ns pinot-quickstart
helm install -n pinot-quickstart pinot .
```

### **2.3 Troubleshooting \(For helm v2.12.1\)**

* Error: Please run below command if encountering issue:

```text
Error: could not find tiller".
```

* Resolution:

```text
kubectl -n kube-system delete deployment tiller-deploy
kubectl -n kube-system delete service/tiller-deploy
helm init --service-account tiller
```

* Error: Please run below command if encountering permission issue:

`Error: release pinot failed: namespaces "pinot-quickstart" is forbidden: User "system:serviceaccount:kube-system:default" cannot get resource "namespaces" in API group "" in the namespace "pinot-quickstart"`

* Resolution:

```text
kubectl apply -f helm-rbac.yaml
```

### **2.4 Check deployment status**

```text
kubectl get all -n pinot-quickstart
```

## 3 Load data into Pinot through Kafka 

### **3.1 Bring up a Kafka Cluster for realtime data ingestion**

* For helm v2.12.1

```text
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install --namespace "pinot-quickstart"  --name kafka incubator/kafka
```

* For helm v3.0.0

```text
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install -n pinot-quickstart kafka incubator/kafka --set replicas=1
```

### 3.2 Check Kafka deployment status

```text
kubectl get all -n pinot-quickstart |grep kafka
```

Ensure Kafka deployment is ready before executing the scripts in next steps.

```text
pod/kafka-0                                          1/1     Running     0          2m
pod/kafka-zookeeper-0                                       1/1     Running     0          10m
pod/kafka-zookeeper-1                                       1/1     Running     0          9m
pod/kafka-zookeeper-2                                       1/1     Running     0          8m
```



### **3.3 Create Kafka topics**

Below scripts will create two Kafka topics for data ingestion:

```text
kubectl -n pinot-quickstart exec kafka-0 -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic flights-realtime --create --partitions 1 --replication-factor 1
kubectl -n pinot-quickstart exec kafka-0 -- kafka-topics --zookeeper kafka-zookeeper:2181 --topic flights-realtime-avro --create --partitions 1 --replication-factor 1
```

### **3.4 Load data into Kafka and Create Pinot Schema/Tables**

Below script will deploy 3 batch jobs

* Ingest 19492 Json messages to Kafka topic `flights-realtime`  at a speed of 1 msg/sec
* Ingest 19492 Avro messages to Kafka topic `flights-realtime-avro`  at a speed of 1 msg/sec
* Upload Pinot schema `airlineStats`
* Create Pinot Table `airlineStats` to ingest data from Json encoded Kafka topic `flights-realtime`
* Create Pinot Table `airlineStatsAvro`  to ingest data from Avro encoded Kafka topic `flights-realtime-avro`

```text
kubectl apply -f pinot-realtime-quickstart.yml
```

## 4 How to query pinot data

### 4.1 Pinot Query Console

Please use below script to do local port-forwarding and open Pinot query console on your web browser.

```text
./query-pinot-data.sh
```

## 5 Use Superset to query Pinot

### 5.1 Bring up Superset

```text
kubectl apply -f superset.yaml
```

### 5.2 \(First time\) Set up Admin account

```text
kubectl exec -it pod/superset-0 -n pinot-quickstart -- bash -c 'export FLASK_APP=superset:app && flask fab create-admin'
```

### 5.3 \(First time\) Init Superset

```text
kubectl exec -it pod/superset-0 -n pinot-quickstart -- bash -c 'superset db upgrade'
kubectl exec -it pod/superset-0 -n pinot-quickstart -- bash -c 'superset init'
```

### 5.4 Load Demo Data source

```text
kubectl exec -it pod/superset-0 -n pinot-quickstart -- bash -c 'superset import_datasources -p /etc/superset/pinot_example_datasource.yaml'
kubectl exec -it pod/superset-0 -n pinot-quickstart -- bash -c 'superset import_dashboards -p /etc/superset/pinot_example_dashboard.json'
```

### 5.5 Access Superset UI

You can run below command to navigate superset in your browser with the previous admin credential.

```text
./open-superset-ui.sh
```

You can open the imported dashboard by click `Dashboards` banner then click on `AirlineStats`.

## 6 Access Pinot Using Presto

### 6.1 Deploy Presto with Pinot Plugin

You can run below command to deploy a customized Presto with Pinot plugin.

```text
kubectl apply -f presto-coordinator.yaml
```

### 6.2 Query Presto using Presto CLI

Once Presto is deployed, you could run below command.

```text
./pinot-presto-cli.sh
```

### 6.3 Sample queries to execute

* List all catalogs

```text
presto:default> show catalogs;
```

```text
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

```text
presto:default> show tables;
```

```text
    Table
--------------
 airlinestats
(1 row)

Query 20191112_050907_00004_xkm4g, FINISHED, 1 node
Splits: 19 total, 19 done (100.00%)
0:01 [1 rows, 29B] [1 rows/s, 41B/s]
```

* Show schema

```text
presto:default> DESCRIBE pinot.dontcare.airlinestats;
```

```text
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

```text
presto:default> select count(*) as cnt from pinot.dontcare.airlinestats limit 10;
```

```text
 cnt
------
 9745
(1 row)

Query 20191112_051114_00006_xkm4g, FINISHED, 1 node
Splits: 17 total, 17 done (100.00%)
0:00 [1 rows, 8B] [2 rows/s, 19B/s]
```

## 7 How to clean up Pinot deployment

```text
kubectl delete ns pinot-quickstart
```

