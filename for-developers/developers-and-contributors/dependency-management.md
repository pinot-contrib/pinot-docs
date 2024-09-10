# Dependency Management

## Executive Summary

This document outlines guidelines for managing external dependencies in the Apache Pinot Project. By enforcing these guidelines, we can ensure that contributors continually apply dependency management best practices in a consistent and centralized manner across the code base. These practices lead to a more predictable dependency graph and allows third-party builds dependent on OSS to repeatably override dependencies as needed for compliance or other reasons. See [OSS issue](https://github.com/apache/pinot/issues/12676) for more details on the motivation.

## Dependency Management Guidelines

When adding new dependencies or updating the version of an existing dependency, follow these guidelines.

For standard (non plugin) Pinot subprojects:

1. Define all versions inside of the top-level Pinot POM’s _dependencyManagement_ section.
2. Use properties to define dependency versions and refer to the property when declaring your dependency in the Pinot POM. This allows the version to be easily overridden using Maven’s [Versions plugin](https://www.mojohaus.org/versions/versions-maven-plugin/examples/update-properties.html).
3. Include the dependency inside the dependencies section of the subproject but do not define a version.
4. If a BOM version of a dependency exists, favor the BOM so that any transitive dependencies in the dependency group are also pinned at the same version. For example, prefer `com.fasterxml.jackson:jackson-bom` over `com.fasterxml.jackson.core:jackson-annotations` to enforce that all transitive dependencies for the Jackson libraries are at the same version.

For Pinot plugin subprojects:

1. If the required dependency (and version) is present in the Pinot POM, do not shade the dependency and reference it without a version in the subproject’s _dependencies_ section.
2. If the dependency is not present in the Pinot POM, or is present at a different version, use the maven-shade-plugin to relocate the library, so you can avoid class loading conflicts due to duplicate classes from Pinot POM or other plugins. In such cases, you can also define the dependency inside the subproject’s POM to pin its version. It is the plugin’s responsibility to ensure that no Pinot methods are called that reference conflicting libraries, and thus avoid failing with a `MethodNotFoundException` at runtime. For example, a plugin may be able to call `JsonUtils.objectToString` but not `JsonUtils.objectToJsonNode` when shading Jackson libraries.

## Examples

### Managing shared dependencies in Pinot POM

```
  <properties>
    <jackson.version>2.12.7</jackson.version>
    <snakeyaml.version>2.2</snakeyaml.version>
    ... 
  </properties>

  <dependencyManagement>
    <dependencies>
      <!-- prefer boms to pin multiple artifacts at the same version -->
      <dependency>
        <groupId>com.fasterxml.jackson</groupId>
        <artifactId>jackson-bom</artifactId>
        <version>${jackson.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
      <dependency>
        <groupId>org.yaml</groupId>
        <artifactId>snakeyaml</artifactId>
        <version>${snakeyaml.version}</version>
      </dependency>
      ...
  </dependencyManagement>
```

### Referencing a shared dependency from a subproject

```
  <dependencies>
    <!-- do not include a version with the dependency here
         as the version should be defined in the Pinot POM -->
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-annotations</artifactId>
    </dependency>
    ...
  </dependencies>
```

### Shading a dependency in a plugin subproject

```
  <!-- pin versions required by plugin -->
  <dependencyManagement>
    <dependencies>
      <dependency>
        <groupId>software.amazon.awssdk</groupId>
        <artifactId>bom</artifactId>
        <version>${aws.sdk.version}</version>
        <type>pom</type>
        <scope>import</scope>
      </dependency>
    </dependencies>
  </dependencyManagement>

  ...
  <!-- include required dependencies -->
  <dependencies>
    <dependency>
      <groupId>software.amazon.awssdk</groupId>
      <artifactId>sdk-core</artifactId>
    </dependency>
    <dependency>
      <groupId>software.amazon.awssdk</groupId>
      <artifactId>kinesis</artifactId>
    </dependency>
    <dependency>
      <groupId>com.fasterxml.jackson.core</groupId>
      <artifactId>jackson-core</artifactId>
    </dependency>
    ...
  </dependencies>
  ...

<!-- maven-shade-plugin configuration to relocate conflicting libraries -->
<relocations>
    <relocation>
      <pattern>software.amazon</pattern>
      <shadedPattern>${shade.prefix}.software.amazon</shadedPattern>
     </relocation>
    <relocation>
      <pattern>com.fasterxml.jackson</pattern>
      <shadedPattern>${shade.prefix}.com.fasterxml.jackson</shadedPattern>
     </relocation>
</relocations>
```
