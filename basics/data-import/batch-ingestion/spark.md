---
description: Batch ingestion of data into Apache Pinot using Apache Spark.
---

# Spark

Pinot supports Apache Spark (2.x and 3.x) as a processor to create and push segment files to the database. Pinot distribution is bundled with the Spark code to process your files and convert and upload them to Pinot.

To set up Spark, do one of the following:

* Use the Spark-Pinot Connector. For more information, see the [ReadMe](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-spark-3-connector/README.md).
* Follow the instructions below.

You can follow the [wiki](../../getting-started/running-pinot-locally.md#build-from-source-or-download-the-distribution) to build Pinot from source. The resulting JAR file can be found in `pinot/target/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`

If you do build Pinot from Source, you should consider opting into using the `build-shaded-jar` jar profile with `-Pbuild-shaded-jar`. While Pinot does not bundle spark into its jar, it does bundle certain hadoop libraries.

Next, you need to change the execution config in the [job spec](./#create-schema-configuration) to the following:

```
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  # name: execution framework name
  name: 'spark'

  # segmentGenerationJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface.
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentGenerationJobRunner'

  # segmentTarPushJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface.
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentTarPushJobRunner'

  # segmentUriPushJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface.
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentUriPushJobRunner'

  #segmentMetadataPushJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark.SparkSegmentMetadataPushJobRunner'

  # extraConfigs: extra configs for execution framework.
  extraConfigs:

    # stagingDir is used in distributed filesystem to host all the segments then move this directory entirely to output directory.
    stagingDir: your/local/dir/staging
```

To run Spark ingestion, you need the following jars in your classpath

* `pinot-batch-ingestion-spark` plugin jar - available in `plugins-external` directory in the package
* `pinot-all` jar - available in `lib` directory in the package

These jars can be specified using `spark.driver.extraClassPath` or any other option.

```
spark.driver.extraClassPath =>
pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar
```

For loading any other plugins that you want to use, use:

```
spark.driver.extraJavaOptions =>
-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins
```

The complete spark-submit command should look like this:

```
export PINOT_VERSION=0.10.0
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin

spark-submit //
--class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand //
--master local --deploy-mode client //
--conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins" //
--conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-2.4/pinot-batch-ingestion-spark-2.4-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" //
-conf "spark.executor.extraClassPath=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-2.4/pinot-batch-ingestion-spark-2.4-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" //
local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar -jobSpecFile /path/to/spark_job_spec.yaml
```

Ensure environment variables `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

**Note**: You should change the `master` to `yarn` and `deploy-mode` to `cluster` for production environments.

{% hint style="info" %}
We have stopped including `spark-core` dependency in our jars post 0.10.0 release. Users can try 0.11.0-SNAPSHOT and later versions of `pinot-batch-ingestion-spark` in case of any runtime issues. You can either [build from source ](../../getting-started/)or download latest master build jars.
{% endhint %}

### Running in Cluster Mode on YARN

If you want to run the spark job in cluster mode on YARN/EMR cluster, the following needs to be done -

* Build Pinot from source with option `-DuseProvidedHadoop`
* Copy Pinot binaries to S3, HDFS or any other distributed storage that is accessible from all nodes.
* Copy Ingestion spec YAML file to S3, HDFS or any other distributed storage. Mention this path as part of `--files` argument in the command
* Add `--jars` options that contain the s3/hdfs paths to all the required plugin and pinot-all jar
* Point `classPath` to spark working directory.  Generally, just specifying the jar names without any paths works. Same should be done for main jar as well as the spec YAML file

**Example**

```
spark-submit //
--class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand //
--master yarn --deploy-mode cluster //
--conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins" //
--conf "spark.driver.extraClassPath=pinot-batch-ingestion-spark-2.4/pinot-batch-ingestion-spark-2.4-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" //
--conf "spark.executor.extraClassPath=pinot-batch-ingestion-spark-2.4/pinot-batch-ingestion-spark-2.4-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" //
--jars "${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-2.4/pinot-batch-ingestion-spark-2.4-${PINOT_VERSION}-shaded.jar,${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar"
--files s3://path/to/spark_job_spec.yaml
local://pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar -jobSpecFile spark_job_spec.yaml
```

{% hint style="success" %}
For Spark 3.x, replace `pinot-batch-ingestion-spark-2.4` with `pinot-batch-ingestion-spark-3.2` in all places in the commands. \
\
Also, ensure the classpath in ingestion spec is changed from `org.apache.pinot.plugin.ingestion.batch.spark.`\
to \
`org.apache.pinot.plugin.ingestion.batch.spark3.`
{% endhint %}

### FAQ

Q - **I am getting the following exception - `Class has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0`**

Since 0.8.0 release, Pinot binaries are compiled with JDK 11. If you are using Spark along with Hadoop 2.7+, you need to use the Java8 version of Pinot. Currently, you need to [build jdk 8 version from source](../../getting-started/).



Q - **I am not able to find `pinot-batch-ingestion-spark` jar.**

For Pinot version prior to 0.10.0, the spark plugin is located in `plugin` dir of binary distribution. For 0.10.0 and later, it is located in `pinot-external` dir.



Q - **Spark is not able to find the jars** **leading to**  **`java.nio.file.NoSuchFileException`**

This means the classpath for spark job has not been configured properly. If you are running spark in a distributed environment such as Yarn or k8s, make sure both `spark.driver.classpath` and `spark.executor.classpath` are set. Also, the jars in `driver.classpath` should be added to `--jars` argument in `spark-submit` so that spark can distribute those jars to all the nodes in your cluster. You also need to take provide appropriate scheme with the file path when running the jar. In this doc, we have used `local:\\` but it can be different depending on your cluster setup.



Q - **Spark job failing while pushing the segments.**

It can be because of misconfigured `controllerURI` in job spec yaml file. If the controllerURI is correct, make sure it is accessible from all the nodes of your YARN or k8s cluster.



Q - **My data gets overwritten during ingestion.**

Set [segmentPushType](../../../configuration-reference/table.md#segments-config) to `APPEND` in the tableConfig.

If already set to `APPEND`, this is likely due to a missing `timeColumnName` in your table config. If you can't provide a time column, use our[ segment name generation configs](../../../configuration-reference/job-specification.md#segment-name-generator-spec) in ingestion spec. Generally using `inputFile` segment name generator should fix your issue.



Q - **I am getting `java.lang.RuntimeException: java.io.IOException: Failed to create directory: pinot-plugins-dir-0/plugins/*`**

Removing `-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins` from `spark.driver.extraJavaOptions`  should fix this. As long as plugins are mentioned in classpath and `jars` argument it should not be an issue.



Q - Getting `Class not found:` exception

Check if `extraClassPath` arguments contain all the plugin jars for both driver and executors. Also, all the plugin jars are mentioned in the `--jars` argument. If both of these are correct, check if the `extraClassPath` contains local filesystem classpaths and not s3 or hdfs or any other distributed file system classpaths.

