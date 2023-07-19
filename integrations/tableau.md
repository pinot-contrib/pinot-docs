---
description: This section details how to connect to Pinot from Tableau using JDBC
---

# Tableau

Tableau is a popular data visualization tool for enterprise business intelligence. In this section we'll cover the details on how to use Pinot's JDBC client to connect and query real-time or offline tables from [Tableau Desktop](https://www.tableau.com/products/desktop).

### Building the Pinot JDBC client from source

As a part of the Pinot open source distribution, we provide a JDBC client that must be built from source code and is not yet available as a binary. We plan to expand support for the JDBC client as a binary in the near future. In this section, we'll walk through building the Pinot project from source and locating the binaries required to connect to Pinot from Tableau Desktop.

#### Clone Pinot from GitHub

The first step is to clone Apache Pinot from GitHub, which will pull down the most recent Pinot snapshot from the git repository. From your terminal, clone the official Apache Pinot repository to your local disk.

```
$ git clone https://github.com/apache/pinot.git
```

#### Build Pinot using Maven

After you clone the Pinot source using git, you will need to build the project using Apache Maven.

{% hint style="info" %}
To build the Java binaries of Apache Pinot, you must have JDK 11+ installed and the latest version of Apache Maven.
{% endhint %}

Now, from your terminal, change directories to the top-level folder containing the cloned Apache Pinot source code. Now, run the following command to build Pinot from source.

```
$ mvn clean install -DskipTests -Pbin-dist
```

If you have the correct prerequisites installed, the build will complete successfully in 5-10 minutes, depending on your machine's resources. When the build is complete, Maven will have installed the necessary binaries on your local machine.

#### Locating your local Maven repository

Your local machine has a Maven repository, called `m2`, which contains a cache of Java binaries, either built from source or cloned from a hosted Maven repository. To locate this directory, run the following command in your terminal, which will locate the `m2` repository on your machine.

```
mvn help:evaluate -Dexpression=settings.localRepository
```

After running this command, you should see something similar to the following output.

```
[INFO] Scanning for projects...
[INFO] 
[INFO] ------------------< org.apache.maven:standalone-pom >-------------------
[INFO] Building Maven Stub Project (No POM) 1
[INFO] --------------------------------[ pom ]---------------------------------
[INFO] 
[INFO] --- maven-help-plugin:3.2.0:evaluate (default-cli) @ standalone-pom ---
[INFO] No artifact parameter specified, using 'org.apache.maven:standalone-pom:pom:1' as project.
[INFO] 
/Users/user/.m2/repository
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  1.698 s
[INFO] Finished at: 2021-11-09T12:50:48-05:00
[INFO] ------------------------------------------------------------------------
```

On line 10 of the above output, you will see an example folder location of the local Maven repository for a macOS user. The folder location we'll use for this guide will be `/Users/user/.m2/repository`.

{% hint style="info" %}
The folder location for your Maven repository will be different for Windows users, but the binaries and folder structure of the `m2` repository are the same on both operating systems.
{% endhint %}

### Install Pinot JDBC for Tableau Desktop

There are three binaries that are required by Tableau to be able to connect to Pinot. Each of these binaries are located inside the `m2` repository on the machine that you used to build Pinot from source. After completing the previous step, you will need to locate those binaries using the folder location of your `m2` repository, such as `/Users/user/.m2/repository` for this example.

The directory we need to copy the binaries to will depend on your operating system. Your Tableau Desktop installation will create a `Drivers` directory, which will vary depending on whether you are using macOS or Windows. The folder locations for each operating system are listed below.

**macOS:** `~/Library/Tableau/Drivers`

**Windows:** `C:\Program Files\Tableau\Drivers`

#### Installing Pinot for Tableau Desktop on macOS

In the previous section, we located the `Driver` directory for your Tableau Desktop installation on macOS. Now, let's now copy the three Pinot binaries from their respective `m2` repository locations to Tableau's `Drivers` directory. The output from the command below will identify and save the most recent Pinot snapshot version that you've installed from Maven to an environment variable.

```
PINOT_VERSION=$(ls -td ~/.m2/repository/org/apache/pinot/pinot/*/ | head -1 | grep -o "\d*.\d*\.\d*-SNAPSHOT") 
```

To check to make sure that Pinot was correctly installed on your machine using Maven, run the following command.

```
echo $PINOT_VERSION
```

The output of the command should be something like the following: `#.#.#-SNAPSHOT`. If that's the case, then you can run the following commands in the same terminal window to install the Pinot binaries to Tableau Desktop.

```
cd ~/Library/Tableau/Drivers
cp ~/.m2/repository/com/ning/async-http-client/1.9.21/async-http-client-1.9.21.jar .
cp ~/.m2/repository/org/apache/pinot/pinot-jdbc-shaded/$PINOT_VERSION/pinot-jdbc-shaded-$PINOT_VERSION.jar .
```

You will also need to download [calcite-core](https://mvnrepository.com/artifact/org.apache.calcite/calcite-core/1.34.0) and copy that into the `~/Library/Tableau/Drivers` directory as well.&#x20;

Now, verify that the binaries are present in your `Drivers` directory.

```
ls ~/Library/Tableau/Drivers
...
async-http-client-1.9.21.jar         calcite-core-1.34.0.jar 
pinot-jdbc-shaded-0.13.0-SNAPSHOT.jar
```

If the output from the command on the first line of the previous snippet matches the JAR files listed here, then you've successfully installed the Pinot connector for Tableau Desktop.

#### Installing Pinot for Tableau Desktop on Windows

This section is coming soon. Refer to the previous section and substitute the Windows directories using the same process.

### Connecting to Pinot from Tableau Desktop

Now that you've installed the Pinot JDBC connector binaries to your Tableau Desktop installation, you can begin to use Pinot as a data source. On your machine, make sure you restart Tableau so that it can locate and use the Pinot JDBC connector files that we copied to the `Drivers` directory in the previous steps.

Once Tableau Desktop has restarted, you can now create a new JDBC connection to Pinot using the following steps.

1. Create a new Tableau Book using the `File > New` menu option
2. In the new Book, use the `Data > New Data Source` menu option
3. Locate the `Other Databases (JDBC)` option in the resulting window
4. Add your Pinot JDBC connection URL (`jdbc:pinot://localhost:9000`)
5. Choose `SQL92` as your dialect
6. Click `Sign In`

The result of the previous steps should result in a successful connection to Pinot. If the connection fails, make sure that you note the resulting error message. If the connection to Pinot could not be established, it is likely that you do not have network access to either the Pinot controller or broker from your machine. For Tableau to be able to query Pinot, you'll need to make sure that both the controller (by default `localhost:9000`) and the broker (by default `localhost:8000`) can be accessed from your machine.

For any other error messages or connection issues, contact us on our community Slack and report your issue on the `Troubleshooting` channel.
