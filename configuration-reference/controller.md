# Controller

Most of the properties in Pinot are set in Zookeeper via  Helix. However, there are many properties that can be passed as part of the controller.conf at startup time.

```text
bin/pinot-admin.sh StartController -configFileName /path/to/controller.conf
```

Controller.conf can have the following properties. All properties are defined in this class.

{% embed url="https://github.com/apache/incubator-pinot/blob/master/pinot-controller/src/main/java/org/apache/pinot/controller/ControllerConf.java" %}

TBD

| Property | Description |
| :--- | :--- |
|  |  |

