# Write Custom Plugins

Pinot allows user to easily create and use new plugins to support custom needs. The developer needs to implement a few standard interfaces specific to the the type of plugins in Java.

Once the code is ready, you can put the complete JAR file in pinot `/plugins` directory. All the classes in plugins directory are loaded at pinot's startup.\
\
We also encourage users to shaded commonly used dependencies such as `guava`, `jackson`&#x20;
