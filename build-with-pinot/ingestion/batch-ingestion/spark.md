---
description: Batch ingestion of data into Apache Pinot using Apache Spark.
---

# Spark

Pinot supports Apache Spark 3.x as a processor to create and push segment files to the database. Pinot distribution is bundled with the Spark code to process your files and convert and upload them to Pinot.

To set up Spark, do one of the following:

* Use the Spark-Pinot Connector. For more information, see the [ReadMe](https://github.com/apache/pinot/blob/master/pinot-connectors/pinot-spark-3-connector/README.md).
* Follow the instructions below.

You can follow the [local install guide](../../../basics/getting-started/install/local.md#1-download-or-build-apache-pinot) to build Pinot from source. The resulting JAR file can be found in `pinot/target/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`

If you do build Pinot from Source, you should consider opting into using the `build-shaded-jar` jar profile with `-Pbuild-shaded-jar`. While Pinot does not bundle spark into its jar, it does bundle certain hadoop libraries.

Next, you need to change the execution config in the [job spec](.#create-schema-configuration) to the following:

```
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

  # name: execution framework name
  name: 'spark'

  # segmentGenerationJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface.
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentGenerationJobRunner'

  # segmentTarPushJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface.
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentTarPushJobRunner'

  # segmentUriPushJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface.
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentUriPushJobRunner'

  #segmentMetadataPushJobRunnerClassName: class name implements org.apache.pinot.spi.ingestion.batch.runner.IngestionJobRunner interface
  segmentMetadataPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.spark3.SparkSegmentMetadataPushJobRunner'

  # extraConfigs: extra configs for execution framework.
  extraConfigs:

    # stagingDir is used in distributed filesystem to host all the segments then move this directory entirely to output directory.
    stagingDir: your/local/dir/staging
```

Spark job specs can filter input paths with `includeFileNamePattern` and `excludeFileNamePattern`. Both properties accept Java NIO `glob:` and `regex:` patterns; see [File name patterns](../../../reference/configuration-reference/job-specification.md#file-name-patterns) for working examples and path-normalization details.

## Required jars and plugins.dir

`pinot-all-*-jar-with-dependencies.jar` does **not** bundle Spark or Hadoop batch-ingestion plugins. Those live under `plugins-external/` in the binary distribution (see `pinot-assembly.xml`). You must put them on the Spark classpath **and** point `plugins.dir` at directories that contain them.

To run Spark ingestion you need:

* `pinot-all` jar — under `lib/` in the package
* `pinot-batch-ingestion-spark-3` shaded plugin jar — under `plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/`
* Any other plugins your job uses (record readers, file systems) — under `plugins/` (for example `pinot-avro`, `pinot-parquet`, `pinot-s3`)

`plugins.dir` accepts a **semicolon-separated** list of directories. Include both `plugins` and `plugins-external` so record readers and the Spark batch runners load correctly:

```
-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins;${PINOT_DISTRIBUTION_DIR}/plugins-external
```

Put the Spark batch plugin and `pinot-all` on the driver (and executor) classpath with `spark.driver.extraClassPath` / `spark.executor.extraClassPath`:

```
spark.driver.extraClassPath =>
${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/pinot-batch-ingestion-spark-3-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar
```

The complete local-mode `spark-submit` command:

```
export PINOT_VERSION=1.4.0 #set to the Pinot version you have installed
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin

SPARK_BATCH_PLUGIN=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/pinot-batch-ingestion-spark-3-${PINOT_VERSION}-shaded.jar
PINOT_ALL_JAR=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar

spark-submit \
  --class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \
  --master local --deploy-mode client \
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins;${PINOT_DISTRIBUTION_DIR}/plugins-external" \
  --conf "spark.driver.extraClassPath=${SPARK_BATCH_PLUGIN}:${PINOT_ALL_JAR}" \
  --conf "spark.executor.extraClassPath=${SPARK_BATCH_PLUGIN}:${PINOT_ALL_JAR}" \
  local://${PINOT_ALL_JAR} \
  -jobSpecFile /path/to/spark_job_spec.yaml
```

Ensure environment variables `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

**Note**: You should change the `master` to `yarn` and `deploy-mode` to `cluster` for production environments.

{% hint style="info" %}
The `spark-core` dependency is not included in Pinot jars since the 0.10.0 release. If you run into runtime issues, make sure your Spark environment provides the dependency, or [build from source](../../../basics/getting-started/) with the matching Spark profile.
{% endhint %}

### Running on YARN

The example below uses YARN with `client` deploy mode so the Spark driver can read the unpacked Pinot distribution referenced by `plugins.dir`. Before running it:

* Build Pinot from source with option `-DuseProvidedHadoop`
* Keep the unpacked Pinot distribution available on the submit host.
* Copy the ingestion spec YAML to S3, HDFS, or another location accessible through `--files`.
* Add the Spark batch plugin and `pinot-all` through `--jars` so Spark distributes them to executors.
* Point the driver and executor classpaths at the distributed jar names.

For YARN `cluster` deploy mode, the driver runs remotely. You must separately distribute and unpack the `plugins` and `plugins-external` directories, then set `plugins.dir` to paths that exist in the remote driver container.

**Example**

```
spark-submit \
  --class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \
  --master yarn --deploy-mode client \
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins;${PINOT_DISTRIBUTION_DIR}/plugins-external" \
  --conf "spark.driver.extraClassPath=pinot-batch-ingestion-spark-3-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \
  --conf "spark.executor.extraClassPath=pinot-batch-ingestion-spark-3-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \
  --jars "${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/pinot-batch-ingestion-spark-3-${PINOT_VERSION}-shaded.jar,${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \
  --files s3://path/to/spark_job_spec.yaml \
  ${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \
  -jobSpecFile spark_job_spec.yaml
```


### FAQ

Q - **I am getting the following exception - `Class has been compiled by a more recent version of the Java Runtime (class file version 55.0), this version of the Java Runtime only recognizes class file versions up to 52.0`**

Since 0.8.0 release, Pinot binaries are compiled with JDK 11. If you are using Spark along with Hadoop 2.7+, you need to use the Java8 version of Pinot. Currently, you need to [build jdk 8 version from source](../../../basics/getting-started/).

Q - **I am not able to find `pinot-batch-ingestion-spark` jar.**

Since Pinot 0.10.0, the Spark batch plugin is located under `plugins-external/pinot-batch-ingestion/` in the binary distribution (in older versions it lived under `plugins/`). Current Spark 3 builds ship `pinot-batch-ingestion-spark-3-*-shaded.jar`.

Q - **Spark is not able to find the jars** **leading to** **`java.nio.file.NoSuchFileException`**

This means the classpath for spark job has not been configured properly. If you are running spark in a distributed environment such as Yarn or k8s, make sure both `spark.driver.extraClassPath` and `spark.executor.extraClassPath` are set. Also, the jars in `driver.extraClassPath` should be added to `--jars` argument in `spark-submit` so that spark can distribute those jars to all the nodes in your cluster. You also need to take provide appropriate scheme with the file path when running the jar. In this doc, we have used `local://` but it can be different depending on your cluster setup.

Q - **Spark job failing while pushing the segments.**

It can be because of misconfigured `controllerURI` in job spec yaml file. If the controllerURI is correct, make sure it is accessible from all the nodes of your YARN or k8s cluster.

Q - **My data gets overwritten during ingestion.**

Set [segmentPushType](../../../reference/configuration-reference/table.md#segments-config) to `APPEND` in the tableConfig.

If already set to `APPEND`, this is likely due to a missing `timeColumnName` in your table config. If you can't provide a time column, use our[ segment name generation configs](../../../reference/configuration-reference/job-specification.md#segment-name-generator-spec) in ingestion spec. Generally using `inputFile` segment name generator should fix your issue.

Q - **I am getting `java.lang.RuntimeException: java.io.IOException: Failed to create directory: pinot-plugins-dir-0/plugins/*`**

Removing `-Dplugins.dir=...` from `spark.driver.extraJavaOptions` can fix this when the plugin jars are already on the Spark classpath via `extraClassPath` and `--jars`. Prefer pointing `plugins.dir` at real local paths that exist on the driver (`plugins` and `plugins-external` under the distribution).

Q - Getting `Class not found:` exception (for example `SparkSegmentGenerationJobRunner`)

The Spark/Hadoop batch runners are **not** inside `pinot-all`. Confirm that:

1. `extraClassPath` for both driver and executors includes the shaded jar under `plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark-3/`
2. That same jar is listed in `--jars` for cluster mode
3. `plugins.dir` includes `${PINOT_DISTRIBUTION_DIR}/plugins-external` (semicolon-separated with `plugins` if you also need record readers / file-system plugins from `plugins/`)
4. The job spec uses the Spark 3 package: `org.apache.pinot.plugin.ingestion.batch.spark3.*`
