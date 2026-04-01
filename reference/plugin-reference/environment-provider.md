---
description: >-
  Configure cloud environment providers for automatic Pinot instance configuration.
---

# Environment Provider Plugins

Environment Provider plugins allow Pinot to discover cloud-specific instance metadata at startup. This metadata is used to configure failure domains, availability zones, and other cloud-specific settings that improve data placement and fault tolerance.

## Available Implementations

| Plugin | Class Name | Cloud Provider |
|--------|-----------|---------------|
| **Azure** | `org.apache.pinot.plugin.provider.AzureEnvironmentProvider` | Microsoft Azure |

## Azure Environment Provider

The Azure Environment Provider queries the [Azure Instance Metadata Service (IMDS)](https://learn.microsoft.com/en-us/azure/virtual-machines/instance-metadata-service) to retrieve the platform fault domain for the current VM. This information is used by Pinot's Helix-based cluster management to distribute instances across Azure failure domains for improved fault tolerance.

### Configuration

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `maxRetry` | Integer | Yes | Maximum number of HTTP retries (must be > 0) |
| `imdsEndpoint` | String | Yes | Azure IMDS endpoint URL |
| `connectionTimeoutMillis` | Integer | Yes | HTTP connection timeout in milliseconds |
| `requestTimeoutMillis` | Integer | Yes | HTTP request/response timeout in milliseconds |

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
