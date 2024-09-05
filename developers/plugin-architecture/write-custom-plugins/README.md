# Write Custom Plugins

Pinot allows user to easily create and use new plugins to support custom needs. The developer needs to implement a few standard interfaces specific to the type of plugins in Java.

Once the code is ready, you can put the complete JAR file in pinot `/plugins` directory. All the classes in plugins directory are loaded at pinot's startup.

As of Apache Pinot 1.3.0 there's an additional support for a new structure:

     /plugins
        /my-custom-plugin
           /classes/...
           /com-2.3.1.jar
           /foo-1.2.1.jar
           /bar-3.1.1.jar
           /pinot-plugin.properties

This way there's no need to shade classes anymore, because Pinot will ensure isolation and proper ordered loading of these classes. 
Pinot will only expose the classes in pinot-spi.
The `classes`-directory will contain custom compiled Java-code of the plugin.
Next to these `classes` are all the runtime required dependencies, but without the pinot-jars.
The `pinot-plugin.properties` is currently a placeholder to recognize this new structure. In the future this file will be used to store metadata for the plugin.

Currently the following keys are supported:
<dl>
  <dt>parent.realmId</dt>
  <dd>Specify the id of the parent realm. The parentRealm is the final classloader to look for classes. If not defined, then there's no parent realm</dd>
  <dt>importFrom.[realmId]</dt>
  <dd>Comma separated list of packaged that the plugin imports from another realm. When looking for a class, these imports are verified first. The following is used by all plugins and cannot be replaced: <code>importFrom.pinot=org.apache.pinot.spi</code>
</dd>
</dl>

Users of [Apache Maven](http://maven.apache.org) can use the pinot assembly descriptor to generate this new structure. 
This can be done by added the following to the `pom.xml`. 

      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-assembly-plugin</artifactId>
        <version>3.7.1</version>
        <dependencies>
          <dependency>
            <groupId>org.apache.pinot</groupId>
            <artifactId>assembly-descriptor</artifactId>
            <version>1.3.0</version> <!-- should match pinot version -->
          </dependency>
        </dependencies>
        <executions>
          <execution>
            <id>make-assembly</id>
            <phase>package</phase>
            <goals>
              <goal>single</goal>
            </goals>
            <configuration>
              <descriptorRefs>
                <descriptorRef>pinot-plugin</descriptorRef>
              </descriptorRefs>
            </configuration>
          </execution>
        </executions>
      </plugin>

Alternative you can use the old structure where your plugin is packaged in a single shaded jar or uberjar:

     /plugins
        /my-custom-plugin
           /my-custom-plugin-1.0.0-shaded.jar

Plugins using this structure will be able to use all classes provided by Pinot, so dependencies that are not provided by Pinot (the ones you don't import as <scope>provided</scope>) must be _shaded_.
Plugins using the old structure are encourage to _relocate_ (i.e. rename the original package name) commonly used dependencies such as `guava`, `jackson`&#x20;  using a plugin specific prefix to prevent class collisions with Pinot.
