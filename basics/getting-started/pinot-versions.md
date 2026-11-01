---
description: Apache Pinot 1.5.1 artifacts, Java requirements, and source version.
---

# Pinot version reference

This documentation snapshot describes Apache Pinot **1.5.1**.

| Artifact | Version |
| --- | --- |
| Apache Pinot binary | **1.5.1** |
| Docker image | `apachepinot/pinot:1.5.1` |
| Maven / Gradle artifacts | `1.5.1` |
| Source tag | [`release-1.5.1`](https://github.com/apache/pinot/tree/release-1.5.1) |

Use `PINOT_VERSION=1.5.1` when following examples in this snapshot. Download
older release distributions from the [Apache archive](https://archive.apache.org/dist/pinot/apache-pinot-1.5.1/).

## Java and Scala requirements

Pinot 1.5.1 requires **JDK 11 or later**. Its default build targets Java 11
bytecode and uses **Scala 2.12.20**; an optional Scala 2.13 profile is also
available. These values are defined in the
[1.5.1 source POM](https://github.com/apache/pinot/blob/release-1.5.1/pom.xml).
JDK 8 is not supported by Pinot 1.5.1.

## Release notes

Read the [1.5.1 release notes](../releases/1.5.1.md) before upgrading. The
release source commit is `020ff0d0538b2079d4cf4cb2676a191c87c95d4d`.
