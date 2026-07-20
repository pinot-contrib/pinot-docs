# Build Docker Images

## Overview

The scripts to build Pinot related docker images is located at [here](https://github.com/apache/pinot/tree/master/docker/images).

You can access those scripts by running below command to checkout Pinot repo:

```
git clone git@github.com:apache/pinot.git pinot
cd pinot/docker/images
```

You can find current supported 2 images in this directory:

* **Pinot**: Pinot all-in-one distribution image
* **Pinot-Superset**: Superset image with Pinot connector built-in.

## Pinot

This is a docker image of [Apache Pinot](https://github.com/apache/pinot).

Official Pinot service images now target **JDK 25**. The published `latest` tag promotes the `25-ms-openjdk` runtime, and `*-21-*` service tags are no longer published. When you build Pinot service images locally with the helper scripts below, pass `25` for the Java/JDK version arguments to match current releases.

### Docker Base Image Updates

As of [PR #18178](https://github.com/apache/pinot/pull/18178), the Pinot Docker images have been overhauled to improve security and eliminate CVE vulnerabilities:

#### Base Image Changes

- **amazoncorretto runtime**: Migrated from `amazoncorretto:*-al2023-jdk` to `debian:bookworm-slim` with Corretto JDK installed via apt. This eliminates all Python-related CVEs present in the Amazon Linux base image.
- **ms-openjdk runtime**: Migrated from `ubuntu:24.10` (non-LTS, EOL) to `ubuntu:24.04 LTS` for long-term support and stability.

#### Security Improvements

- All base images now run `apt-get upgrade -y` at build time to apply OS security patches
- Thrift compiler upgraded from 0.12.0 to 0.22.0 with SHA-512 checksum verification
- Removed `git` from runtime images to reduce attack surface
- Removed `fontconfig` from Corretto images (unnecessary for headless server deployment)
- Changed download tool from `curl` to `wget` to reduce CVE surface
- CVE hardening: amazoncorretto image reduced from 29 HIGH CVEs to 9 total (0 fixable)

#### Migration Notes

If your deployments rely on `git` being available in the Pinot Docker images, you will need to add it separately or use a custom image that includes it.

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

`Kafka Version`: The Kafka Version to build pinot with. Default is `3.0`. Supported values are `3.0` and `4.0`.

`Java Version`: The Java build and runtime image version. Use `25` for current Pinot service releases. The helper script defaults to `21` if omitted.

`JDK Version`: The JDK parameter to build Pinot, set as part of the Maven build option `-Djdk.version=${JDK_VERSION}`. Use `25` for current Pinot service releases. The helper script defaults to `21` if omitted.

`OpenJDK Image`: Base image to use for Pinot build and runtime. Default is `openjdk`.

* Example of building and tagging a snapshot on your own fork:

```
./docker-build.sh pinot_fork:snapshot-5.2 snapshot-5.2 https://github.com/your_own_fork/pinot.git
```

* Example of building a release version:

```
./docker-build.sh pinot:latest latest https://github.com/apache/pinot.git
```

### Build image with arm64 base image

For users on Mac M1 chips, they need to build the images with arm64 base image, e.g. `arm64v8/openjdk`

* Example of building an arm64 image:

```
./docker-build.sh pinot:latest master https://github.com/apache/pinot.git 2.0 25 25 arm64v8/openjdk
```

or just run the docker build script directly

```
docker build -t pinot:latest --no-cache --network=host --build-arg PINOT_GIT_URL=https://github.com/apache/pinot.git --build-arg PINOT_BRANCH=master --build-arg JDK_VERSION=25 --build-arg OPENJDK_IMAGE=arm64v8/openjdk -f Dockerfile .
```

Note that if you are not on arm64 machine, you can still build the image by turning on the experimental feature of docker, and add `--platform linux/arm64` into the `docker build ...` script, e.g.

```
docker build -t pinot:latest --platform linux/arm64 --no-cache --network=host --build-arg PINOT_GIT_URL=https://github.com/apache/pinot.git --build-arg PINOT_BRANCH=master --build-arg JDK_VERSION=25 --build-arg OPENJDK_IMAGE=arm64v8/openjdk -f Dockerfile .
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
docker tag pinot:latest apachepinot/pinot:latest
docker push apachepinot/pinot:latest
```

Script `docker-build-and-push.sh` builds and publishes this docker image to your docker registry after build.

* Example of building and publishing a image to [apachepinot/pinot](https://cloud.docker.com/u/apachepinot/repository/docker/apachepinot/pinot) dockerHub repo.

```
./docker-build-and-push.sh apachepinot/pinot:latest master https://github.com/apache/pinot.git
```

### Kubernetes Examples

Refer to the [Kubernetes install guide](../basics/getting-started/install/kubernetes.md) for deployment examples.

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
