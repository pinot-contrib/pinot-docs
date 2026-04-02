---
description: Load streaming data into Pinot on Kubernetes using Kafka
---

# Stream ingestion (Kubernetes)

This guide walks you through loading streaming data into a Pinot cluster running in Kubernetes. Make sure you have completed [Running in Kubernetes](../kubernetes/) first.

## Load data into Pinot using Kafka

### **Bring up a Kafka cluster for real-time data ingestion**

{% hint style="info" %}
The Bitnami Kafka Helm chart deploys Kafka in **KRaft mode** (with a built-in controller quorum) by default, so a separate ZooKeeper deployment is not required for Kafka.
{% endhint %}

```bash
helm repo add kafka https://charts.bitnami.com/bitnami
helm install -n pinot-quickstart kafka kafka/kafka \
    --set replicas=1 \
    --set listeners.client.protocol=PLAINTEXT
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
