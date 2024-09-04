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

Plugins using the old structure are encourage to shaded commonly used dependencies such as `guava`, `jackson`&#x20; to prevent class collisions with Pinot.
