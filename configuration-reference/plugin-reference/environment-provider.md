---
description: >-
  Configure cloud environment providers for automatic Pinot instance configuration.
---

# Environment Provider Plugins

Environment Provider plugins allow Pinot to discover cloud-specific instance metadata at startup. This metadata is used to configure failure domains, availability zones, and other cloud-specific settings that improve data placement and fault tolerance.

## Available Implementations

<table>
  <thead>
    <tr>
      <th>Plugin</th>
      <th>Class Name</th>
      <th>Cloud Provider</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Azure**</td>
      <td>`org.apache.pinot.plugin.provider.AzureEnvironmentProvider`</td>
      <td>Microsoft Azure</td>
    </tr>
  </tbody>
</table>

## Azure Environment Provider

The Azure Environment Provider queries the [Azure Instance Metadata Service (IMDS)](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service) to retrieve the platform fault domain for the current VM. This information is used by Pinot's Helix-based cluster management to distribute instances across Azure failure domains for improved fault tolerance.

### Configuration

<table>
  <thead>
    <tr>
      <th>Property</th>
      <th>Type</th>
      <th>Required</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>`maxRetry`</td>
      <td>Integer</td>
      <td>Yes</td>
      <td>Maximum number of HTTP retries (must be > 0)</td>
    </tr>
    <tr>
      <td>`imdsEndpoint`</td>
      <td>String</td>
      <td>Yes</td>
      <td>Azure IMDS endpoint URL</td>
    </tr>
    <tr>
      <td>`connectionTimeoutMillis`</td>
      <td>Integer</td>
      <td>Yes</td>
      <td>HTTP connection timeout in milliseconds</td>
    </tr>
    <tr>
      <td>`requestTimeoutMillis`</td>
      <td>Integer</td>
      <td>Yes</td>
      <td>HTTP request/response timeout in milliseconds</td>
    </tr>
  </tbody>
</table>

### Example Configuration

```properties
pinot.server.environment.provider.className=org.apache.pinot.plugin.provider.AzureEnvironmentProvider
pinot.server.environment.provider.maxRetry=3
pinot.server.environment.provider.imdsEndpoint=http://169.254.169.254/metadata/instance?api-version=2020-09-01
pinot.server.environment.provider.connectionTimeoutMillis=5000
pinot.server.environment.provider.requestTimeoutMillis=5000
```

### How It Works

1. At startup, the provider sends an HTTP GET request to the Azure IMDS endpoint
2. The IMDS response contains VM metadata including the `compute.platformFaultDomain` field
3. The failure domain value is returned and used by Helix to configure the instance
4. This enables Pinot to distribute replicas across fault domains, improving availability during Azure infrastructure failures

{% hint style="info" %}
The Azure IMDS endpoint (`169.254.169.254`) is only accessible from within an Azure VM. This plugin should only be enabled when running Pinot on Azure infrastructure.
{% endhint %}

## Writing a Custom Environment Provider

To create a custom environment provider, implement the `PinotEnvironmentProvider` interface:

```java
public interface PinotEnvironmentProvider {
    void init(PinotConfiguration pinotConfiguration);
    String getFailureDomain();
}
```

See the [Plugin Architecture](../../developers/plugin-architecture/README.md) docs for general guidance on building Pinot plugins.
