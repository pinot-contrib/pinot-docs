---
description: Current Apache Pinot release version and how to pin versions in examples.
---

# Pinot version reference

## Outcome

Know which Pinot version to use and how to pin versions in examples.

{% hint style="warning" %}
All code samples in the **Start Here** guide use `PINOT_VERSION=1.4.0`. If you are using a different version, set the variable accordingly before running any commands.
{% endhint %}

This page is the single source of truth for version information across the Start Here guide and the wider documentation. When following tutorials or code samples, make sure the version you use matches your installed release.

## Current stable release

<table>
  <thead>
    <tr>
      <th>Artifact</th>
      <th>Version</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Apache Pinot binary</td>
      <td>**1.4.0**</td>
    </tr>
    <tr>
      <td>Docker image</td>
      <td>`apachepinot/pinot:1.4.0`</td>
    </tr>
    <tr>
      <td>Maven / Gradle clients</td>
      <td>`1.4.0`</td>
    </tr>
  </tbody>
</table>

## Using PINOT\_VERSION in examples

Most code samples in these docs set a `PINOT_VERSION` environment variable near the top of each snippet. Always verify that the value matches your installed version:

```bash
export PINOT_VERSION=1.4.0

# Then use ${PINOT_VERSION} in commands:

docker pull apachepinot/pinot:${PINOT_VERSION}
```

Once the variable is set, every command in the tutorial that references `${PINOT_VERSION}` will use the correct value automatically.

{% hint style="info" %}
Start Here pages never use the `latest` Docker tag. Always pin to a specific version for reproducibility. The `latest` tag can change without notice and may introduce breaking changes during a tutorial.
{% endhint %}

## Compatibility notes

<table>
  <thead>
    <tr>
      <th>Requirement</th>
      <th>Detail</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Recommended JDK</td>
      <td>**JDK 11** or **JDK 21**</td>
    </tr>
    <tr>
      <td>JDK 17</td>
      <td>Should work but is not officially supported</td>
    </tr>
    <tr>
      <td>Pinot 1.0+ minimum</td>
      <td>JDK 11 or higher required</td>
    </tr>
    <tr>
      <td>JDK 8 support</td>
      <td>Pinot **0.12.1** is the last version that supports JDK 8</td>
    </tr>
  </tbody>
</table>

If you are running JDK 8 and cannot upgrade, use Pinot 0.12.1. For all new deployments, JDK 11 or 21 is recommended.

## Release links

{% hint style="info" %}
You can find all published releases on the [Release notes](../../basics/releases/) page, and all Docker tags on [Docker Hub](https://hub.docker.com/r/apachepinot/pinot/tags).
{% endhint %}

## Older versions

Older Pinot binaries are archived at [https://archive.apache.org/dist/pinot/](https://archive.apache.org/dist/pinot/).
