# Config Validator SPI

## Overview

Pinot provides Service Provider Interface (SPI) for validating table and instance configurations before they are persisted. This allows you to implement custom validation logic that runs during configuration creation and updates.

There are two validator interfaces:

1. **TableConfigValidator** - validates table configuration changes
2. **InstanceConfigValidator** - validates instance configuration changes

Both validators follow the same registration and invocation pattern with short-circuit semantics: the first validator to reject a configuration stops further validation and immediately raises an exception.

## TableConfigValidator

### Interface Definition

```java
package org.apache.pinot.spi.config.table;

public interface TableConfigValidator {
  /**
   * Validates a table configuration.
   *
   * @param tableConfig the table configuration to validate
   * @param schema the table schema (nullable)
   * @throws ConfigValidationException if validation fails
   */
  void validate(TableConfig tableConfig, @Nullable Schema schema) 
      throws ConfigValidationException;
}
```

### Registration

Register your validator using:

```java
TableConfigValidatorRegistry.register(new MyTableConfigValidator());
```

### Invocation

Validators are invoked before table configuration is persisted during:
- Table creation
- Table update
- Preflight validation through `POST /tableConfigs/validate`
- Preflight validation through `POST /tables/validate`

Multiple validators can be registered and are invoked in registration order. The first validator that throws `ConfigValidationException` will reject the operation and short-circuit remaining validators.

Both preflight endpoints run registered validators without persisting the table config. Use either endpoint to catch custom validation failures before submitting the corresponding create or update request.

## InstanceConfigValidator

### Interface Definition

```java
package org.apache.pinot.spi.config.instance;

public interface InstanceConfigValidator {
  /**
   * Validates an instance configuration.
   *
   * @param instance the instance configuration to validate
   * @throws ConfigValidationException if validation fails
   */
  void validate(Instance instance) throws ConfigValidationException;
}
```

### Registration

Register your validator using:

```java
InstanceConfigValidatorRegistry.register(new MyInstanceConfigValidator());
```

### Invocation

Validators are invoked before instance configuration is persisted during:
- Instance addition
- Instance update
- Instance tag updates

Similar to table validators, multiple instance validators can be registered with the same short-circuit semantics.

## ConfigValidationException

When validation fails, throw `ConfigValidationException`:

```java
package org.apache.pinot.spi.exception;

public class ConfigValidationException extends RuntimeException {
  public ConfigValidationException(String message) {
    super(message);
  }

  public ConfigValidationException(String message, Throwable cause) {
    super(message, cause);
  }
}
```

This exception is mapped to HTTP 400 (Bad Request) at the REST API boundary, providing immediate feedback to clients attempting invalid configurations.

## Important Requirements

### Thread Safety

**Validator implementations must be thread-safe.** Validators may be invoked concurrently from multiple threads, so ensure your implementation properly handles concurrent access to shared state.

### Best Practices

1. **Fail Fast** - Validate early and provide clear error messages
2. **Stateless** - Keep validators stateless when possible
3. **No Side Effects** - Validators should only validate, not modify configurations
4. **Clear Messages** - Include actionable information in error messages

## Example: Table Name Prefix Validator

Here's an example validator that enforces table names follow a specific naming convention:

```java
import org.apache.pinot.spi.config.table.TableConfig;
import org.apache.pinot.spi.config.table.TableConfigValidator;
import org.apache.pinot.spi.exception.ConfigValidationException;
import org.apache.pinot.spi.data.Schema;
import javax.annotation.Nullable;

public class TableNamePrefixValidator implements TableConfigValidator {
  private final String requiredPrefix;

  public TableNamePrefixValidator(String requiredPrefix) {
    this.requiredPrefix = requiredPrefix;
  }

  @Override
  public void validate(TableConfig tableConfig, @Nullable Schema schema) 
      throws ConfigValidationException {
    String tableName = tableConfig.getTableName();
    
    if (!tableName.startsWith(requiredPrefix)) {
      throw new ConfigValidationException(
          String.format(
              "Table name '%s' must start with prefix '%s'",
              tableName,
              requiredPrefix
          )
      );
    }
  }
}
```

To register this validator:

```java
TableConfigValidatorRegistry.register(
    new TableNamePrefixValidator("prod_")
);
```

Now any attempt to create or update a table without the `prod_` prefix will be rejected with a clear error message.

## Example: Instance Tag Validator

Here's an example validator for instance configurations:

```java
import org.apache.pinot.spi.config.instance.Instance;
import org.apache.pinot.spi.config.instance.InstanceConfigValidator;
import org.apache.pinot.spi.exception.ConfigValidationException;

public class InstanceTagValidator implements InstanceConfigValidator {
  private static final String REQUIRED_TAG = "monitoring_enabled";

  @Override
  public void validate(Instance instance) throws ConfigValidationException {
    if (!instance.getTags().contains(REQUIRED_TAG)) {
      throw new ConfigValidationException(
          String.format(
              "Instance '%s' must have the '%s' tag",
              instance.getInstanceId(),
              REQUIRED_TAG
          )
      );
    }
  }
}
```

Register it:

```java
InstanceConfigValidatorRegistry.register(new InstanceTagValidator());
```

## Integration Points

The validators are invoked at the following REST endpoints:

**Table Configuration:**
- `POST /tables` (table creation)
- `PUT /tables/{tableName}` (table update)

**Instance Configuration:**
- `POST /instances` (instance addition)
- `PUT /instances/{instanceId}` (instance update)
- `PUT /instances/{instanceId}/tags` (tag updates)

Validation failures return HTTP 400 with the exception message in the response body.

## See Also

- [Plugin Architecture Overview](README.md)
- [Pinot Configuration Reference](../../../reference/configuration-reference/)
