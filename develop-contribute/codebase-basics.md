# Codebase Basics

This section helps you get the Apache Pinot source code onto your machine, understand how the repository is organized, manage Maven dependencies correctly, and build Docker images from source.

## What you will learn

<table>
  <thead>
    <tr>
      <th>Topic</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Code Setup](../developers/developers-and-contributors/code-setup.md)</td>
      <td>Fork and clone the Pinot repository, install Maven, configure your IDE, and run a local QuickStart from source.</td>
    </tr>
    <tr>
      <td>[Code Modules and Organization](../developers/developers-and-contributors/code-modules-and-organization.md)</td>
      <td>Understand every top-level Maven module -- SPI, core services, plugins, connectors, testing, and deployment artifacts.</td>
    </tr>
    <tr>
      <td>[Dependency Management](../developers/developers-and-contributors/dependency-management.md)</td>
      <td>Follow the project's guidelines for adding, updating, and shading external dependencies in both core modules and plugins.</td>
    </tr>
    <tr>
      <td>[Build Docker Images](../tutorials/operations/build-docker-images.md)</td>
      <td>Build Pinot and Pinot-Superset Docker images from any branch or fork, including ARM64 builds.</td>
    </tr>
  </tbody>
</table>

## Recommended reading order

1. **Code Setup** -- start here to get a working local build.
2. **Code Modules and Organization** -- learn where to find (and place) code.
3. **Dependency Management** -- review the rules before adding any new library.
4. **Build Docker Images** -- package your changes into container images for testing or deployment.

## Prerequisites

* Git installed and configured with SSH keys for GitHub.
* JDK 21 (JDK 17 is also supported with additional VM options).
* Apache Maven 3.6 or later.
* Docker (required only for building container images).

## Next step

Once you are comfortable navigating the codebase, learn how to extend Pinot with custom plugins:

* [Extending Pinot](../developers/developers-and-contributors/extending-pinot/README.md)
