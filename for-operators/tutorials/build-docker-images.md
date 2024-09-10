# Build Docker Images

## Overview

The scripts to build Pinot related docker images is located at [here](https://github.com/apache/pinot/tree/master/docker/images).

You can access those scripts by running below command to checkout Pinot repo:

```
git clone git@github.com:apache/pinot.git pinot
cd pinot/docker/images
```

You can find current supported 3 images in this directory:

* **Pinot**: Pinot all-in-one distribution image
* **Pinot-Presto**: Presto image with Presto-Pinot Connector built-in.
* **Pinot-Superset**: Superset image with Pinot connector built-in.

## Pinot

This is a docker image of [Apache Pinot](https://github.com/apache/pinot).

## How to build a docker image

There is a docker build script which will build a given Git repo/branch and tag the image.

Usage:

```
./docker-build.sh [Docker Tag] [Git Branch] [Pinot Git URL] [Kafka Version] [Java Version] [JDK Version] [OpenJDK Image ]
```

This script will check out Pinot Repo `[Pinot Git URL]` on branch `[Git Branch]` and build the docker image for that.

The docker image is tagged as `[Docker Tag]`.

`Docker Tag`: Name and tag your docker image. Default is `pinot:latest`.

`Git Branch`: The Pinot branch to build. Default is `master`.

`Pinot Git URL`: The Pinot Git Repo to build, users can set it to their own fork. Note that the URL is `https://` based, not `git://`. Default is the Apache Repo: `https://github.com/apache/pinot.git`.

`Kafka Version`: The Kafka Version to build pinot with. Default is `2.0`

`Java Version`: The Java Build and Runtime image version. Default is `11`

`JDK Version`: The JDK parameter to build pinot, set as part of maven build option: `-Djdk.version=${JDK_VERSION}`. Default is `11`

`OpenJDK Image`: Base image to use for Pinot build and runtime. Default is `openjdk`.

* Example of building and tagging a snapshot on your own fork:

```
./docker-build.sh pinot_fork:snapshot-5.2 snapshot-5.2 https://github.com/your_own_fork/pinot.git
```

* Example of building a release version:

```
./docker-build.sh pinot:release-0.1.0 release-0.1.0 https://github.com/apache/pinot.git
```

### Build image with arm64 base image

For users on Mac M1 chips, they need to build the images with arm64 base image, e.g. `arm64v8/openjdk`

* Example of building an arm64 image:

```
./docker-build.sh pinot:latest master https://github.com/apache/pinot.git 2.0 11 11 arm64v8/openjdk
```

or just run the docker build script directly

```
docker build -t pinot:latest --no-cache --network=host --build-arg PINOT_GIT_URL=https://github.com/apache/pinot.git --build-arg PINOT_BRANCH=master --build-arg JDK_VERSION=11 --build-arg OPENJDK_IMAGE=arm64v8/openjdk -f Dockerfile .
```

Note that if you are not on arm64 machine, you can still build the image by turning on the experimental feature of docker, and add `--platform linux/arm64` into the `docker build ...` script, e.g.

```
docker build -t pinot:latest --platform linux/arm64 --no-cache --network=host --build-arg PINOT_GIT_URL=https://github.com/apache/pinot.git --build-arg PINOT_BRANCH=master --build-arg JDK_VERSION=11 --build-arg OPENJDK_IMAGE=arm64v8/openjdk -f Dockerfile .
```

## How to publish a docker image

Script `docker-push.sh` publishes a given docker image to your docker registry.

In order to push to your own repo, the image needs to be explicitly tagged with the repo name.

* Example of publishing a image to [apachepinot/pinot](https://cloud.docker.com/u/apachepinot/repository/docker/apachepinot/pinot) dockerHub repo.

```
./docker-push.sh apachepinot/pinot:latest
```

* Tag a built image, then push.

```
docker tag pinot:release-0.1.0 apachepinot/pinot:release-0.1.0
docker push apachepinot/pinot:release-0.1.0
```

Script `docker-build-and-push.sh` builds and publishes this docker image to your docker registry after build.

* Example of building and publishing a image to [apachepinot/pinot](https://cloud.docker.com/u/apachepinot/repository/docker/apachepinot/pinot) dockerHub repo.

```
./docker-build-and-push.sh apachepinot/pinot:latest master https://github.com/apache/pinot.git
```

### Kubernetes Examples

Refer to [Kubernetes Quickstart](../../basics/getting-started/kubernetes-quickstart.md) for deployment examples.

## Pinot Presto

Docker image for [Presto](https://github.com/prestodb/presto) with Pinot integration.

This docker build project is specialized for Pinot.

### How to build

Usage:

```
./docker-build.sh [Docker Tag] [Git Branch] [Presto Git URL]
```

This script will check out Presto Repo `[Presto Git URL]` on branch `[Git Branch]` and build the docker image for that.

The docker image is tagged as `[Docker Tag]`.

`Docker Tag`: Name and tag your docker image. Default is `pinot-presto:latest`.

`Git Branch`: The Presto branch to build. Default is `master`.

`Presto Git URL`: The Presto Git Repo to build, users can set it to their own fork. Note that the URL is `https://` based, not `git://`. Default is the Apache Repo: `https://github.com/prestodb/presto.git`.

### How to push

```
docker push apachepinot/pinot-presto:latest
```

### Configuration

Follow the [instructions](https://prestodb.io/docs/current/installation/deployment.html) provided by Presto for writing your own configuration files under `etc` directory.

### Volumes

The image defines two data volumes: one for mounting configuration into the container, and one for data.

The configuration volume is located alternatively at `/home/presto/etc`, which contains all the configuration and plugins.

The data volume is located at `/home/presto/data`.

### Kubernetes Examples

Refer to [`presto-coordinator.yaml`](https://github.com/apache/pinot/blob/master/kubernetes/examples/helm/prest-coordinator.yaml) as k8s deployment example.

## Pinot Superset

Docker image for [Superset](https://github.com/ApacheInfra/superset) with Pinot integration.

This docker build project is based on Project [docker-superset](https://github.com/amancevice/docker-superset) and specialized for Pinot.

### How to build

Modify file `Makefile` to change `image` and `superset_version` accordingly.

Below command will build docker image and tag it as `superset_version` and `latest`.

```
make latest
```

You can also build directly with `docker build` command by setting arguments:

```
docker build \
    --build-arg NODE_VERSION=latest \
    --build-arg PYTHON_VERSION=3.6 \
    --build-arg SUPERSET_VERSION=0.34.1 \
    --tag apachepinot/pinot-superset:0.34.1 \
    --target build .
```

### How to push

```
make push
```

### Configuration

Follow the [instructions](https://superset.apache.org/installation.html#configuration) provided by Apache Superset for writing your own `superset_config.py`.

Place this file in a local directory and mount this directory to `/etc/superset` inside the container. This location is included in the image's `PYTHONPATH`. Mounting this file to a different location is possible, but it will need to be in the `PYTHONPATH`.

### Volumes

The image defines two data volumes: one for mounting configuration into the container, and one for data (logs, SQLite DBs, \&c).

The configuration volume is located alternatively at `/etc/superset` or `/home/superset`; either is acceptable. Both of these directories are included in the `PYTHONPATH` of the image. Mount any configuration (specifically the `superset_config.py` file) here to have it read by the app on startup.

The data volume is located at `/var/lib/superset` and it is where you would mount your SQLite file (if you are using that as your backend), or a volume to collect any logs that are routed there. This location is used as the value of the `SUPERSET_HOME` environmental variable.

### Kubernetes Examples

Refer to [`superset.yaml`](https://github.com/apache/pinot/blob/master/kubernetes/examples/helm/superset.yaml) as k8s deployment example.
