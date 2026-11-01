---
description: Apache Pinot 1.5.0 artifacts, Java requirements, and source version.
---

# Pinot version reference

This documentation snapshot describes Apache Pinot **1.5.0**.

| Artifact | Version |
| --- | --- |
| Apache Pinot binary | **1.5.0** |
| Docker image | `apachepinot/pinot:1.5.0` |
| Maven / Gradle artifacts | `1.5.0` |
| Source tag | [`release-1.5.0`](https://github.com/apache/pinot/tree/release-1.5.0) |

Use `PINOT_VERSION=1.5.0` when following examples in this snapshot. Download
older release distributions from the [Apache archive](https://archive.apache.org/dist/pinot/apache-pinot-1.5.0/).

## Java and Scala requirements

Pinot 1.5.0 requires **JDK 11 or later**. Its default build targets Java 11
bytecode and uses **Scala 2.12.20**; an optional Scala 2.13 profile is also
available. These values are defined in the
[1.5.0 source POM](https://github.com/apache/pinot/blob/release-1.5.0/pom.xml).
JDK 8 is not supported by Pinot 1.5.0.

## Release notes

Read the [1.5.0 release notes](../releases/1.5.0.md) before upgrading. The
release source commit is `30fdfeea3a533d61d4eaf4c8050f5f4c07493de4`.
