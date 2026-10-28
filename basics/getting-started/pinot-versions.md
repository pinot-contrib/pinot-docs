---
description: Current Apache Pinot release version and how to pin versions in examples.
---

# Pinot version reference

## Outcome

Know which Pinot version to use and how to pin versions in examples.

{% hint style="warning" %}
All code samples in the **Start Here** guide use `PINOT_VERSION=1.6.0`. If you are using a different version, set the variable accordingly before running any commands.
{% endhint %}

This page is the single source of truth for version information across the Start Here guide and the wider documentation. When following tutorials or code samples, make sure the version you use matches your installed release.

## Current stable release

| Artifact | Version |
| --- | --- |
| Apache Pinot binary | **1.6.0** |
| Docker image | `apachepinot/pinot:1.6.0` |
| Maven / Gradle clients | `1.6.0` |

## Using PINOT\_VERSION in examples

Most code samples in these docs set a `PINOT_VERSION` environment variable near the top of each snippet. Always verify that the value matches your installed version:

```bash
export PINOT_VERSION=1.6.0

# Then use ${PINOT_VERSION} in commands:
docker pull apachepinot/pinot:${PINOT_VERSION}
```

Once the variable is set, every command in the tutorial that references `${PINOT_VERSION}` will use the correct value automatically.

{% hint style="info" %}
Start Here pages never use the `latest` Docker tag. Always pin to a specific version for reproducibility. The `latest` tag can change without notice and may introduce breaking changes during a tutorial.
{% endhint %}

## Compatibility notes

| Requirement | Detail |
| --- | --- |
| **Pinot 1.6.0+ services** | **JDK 25+** for build and runtime |
| **Client libraries** | JDK 11+ (Java/JDBC clients and explicitly pinned SPI/common artifacts remain compatible with Java 11) |
| Pinot 1.0–1.5.x minimum | JDK 11 or higher required; follow the build/runtime guidance for that release |
| JDK 8 support | Pinot **0.12.1** is the last version that supports JDK 8 |

**Starting with Pinot 1.6.0:** services require **JDK 25 or later** for building and runtime. Java/JDBC clients and the explicitly pinned SPI/common artifacts continue to target Java 11 bytecode for backward compatibility with external JVM consumers. See the [1.6.0 upgrade notes](../../reference/releases/1.6.0.md#upgrade-notes-and-removals) before upgrading.

## Release links

{% hint style="info" %}
You can find all published releases on the [Release notes](../../reference/releases/) page, and all Docker tags on [Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).
{% endhint %}

## Older versions

Older Pinot binaries are archived at [https://archive.apache.org/dist/pinot/](https://archive.apache.org/dist/pinot/).
