# Kubernetes Deployment

Pinot community has provided Helm based [Kubernetes deployment template](../../basics/getting-started/kubernetes-quickstart.md).

You can deploy it as simple as run a `helm install` command.

However there are a few things to be noted before starting the benchmark/production.

## Container Resources

We recommend to run Pinot with pre-defined resources for the container, and make requests and limits to be the same.&#x20;

This will ensure the container won't be killed if there is a sudden bump of workload.

It will also be simpler to benchmark the system, e.g. get broker qps limit.

Below is an example for values to set in `values.yaml` file. Default resources is not set.

```
resources:
  requests:
    cpu: 1
    memory: 1G
  limits:
    cpu: 1
    memory: 1G
```

## JVM Setting

### Pinot Controller/Broker

JVM setting should be complaint with the container resources for Pinot Controller and Pinot Broker.

```
resources:
  requests:
    cpu: 1
    memory: 1G
  limits:
    cpu: 1
    memory: 1G
```

You can make JVM setting like below to make `-Xmx` the same size as your container.

```
jvmOpts: "-Xms256M -Xmx1G"
```

### Pinot Server

For Pinot Server, heap is majorly used for query processing, metadata management. It uses off-heap memory for data loading/persistence, memory mapped files page caching. So we recommend just keep minimal requirement for JVM, and leave the rest of the container for off-heap data operations.

E.g. Assuming data is 100 GB on disk, the container size is 4 CPU, 10GB Memory.

```
resources:
  requests:
    cpu: 4
    memory: 10G
  limits:
    cpu: 4
    memory: 10G
```

For JVM, limit `-Xmx` to not exceed 50% container memory limit, so that the rest of the container could be leveraged by the off-heap operations.

```
jvmOpts: "-Xms1G -Xmx4G"
```

## Deep storage

Pinot uses remote storage as deep storage to backup segments.

Default deployment creates a mount disk(e.g Amazon EBS) as deep storage in controller.

You can configure your own S3/Azure DataLate/Google Cloud Storage following this [link](../../basics/data-import/pinot-file-system/#enabling-a-file-system).

