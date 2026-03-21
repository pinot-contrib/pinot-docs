# Pinot version reference

This page lists the current Apache Pinot release version used throughout the documentation examples. When following tutorials or code samples, replace the version placeholders with the version you have installed.

## Current stable release

| Artifact | Version |
| --- | --- |
| Apache Pinot binary | **1.4.0** |
| Docker image | `apachepinot/pinot:1.4.0` |
| Maven / Gradle clients | `1.4.0` |

## Using the correct version in examples

Most code samples in these docs set a `PINOT_VERSION` environment variable near the top of each snippet. Always verify that the value matches your installed version:

```bash
# Set this to the version you have installed
export PINOT_VERSION=1.4.0
```

{% hint style="info" %}
You can find all published releases on the [Release notes](../../basics/releases/) page, and all Docker tags on [Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).
{% endhint %}

## Older versions

Older Pinot binaries are archived at [https://archive.apache.org/dist/pinot/](https://archive.apache.org/dist/pinot/).
