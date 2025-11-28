# Dynamic Environment

To load environment variables into the configuration you can use the `dynamic.env.config` property key to list all the property names that will need templating at run time. Pinot will lookup the in the environment for the variable specified as value and insert the contents in the configuration.

{% hint style="info" %}
\`dynamic.env.config\` is a property that refers to the configuration it's defined in. If you have multiple configuration files make sure to define it in each one of them listing the all the properties that need templating in that specific file.
{% endhint %}

## Example:

Following an example where we first load some variables in the ENV and then we specify in the config what needs to be templated and with which variable.

```shell
export PINOT_CONTROLLER_HOST=host
export PINOT_SERVER_PROPERTY=property
export ANOTHER_VARIABLE=random
```

#### Config from CLI or Config Path

```properties
dynamic.env.config=pinot.controller.host,pinot.server.property,other.var
pinot.controller.host=PINOT_CONTROLLER_HOST
pinot.server.property=PINOT_SERVER_PROPERTY
other.var=ANOTHER_VARIABLE
```

#### Final result (in memory)

```properties
dynamic.env.config=pinot.controller.host,pinot.server.property,other.var
pinot.controller.host=host
pinot.server.property=property
other.var=random
```
