# Spark

Pinot supports Apache spark as a processor to create and push segment files to the database. Pinot distribution is bundled with the Spark code to process your files and convert and upload them to Pinot.

You can follow the [wiki](../../getting-started/running-pinot-locally.md#build-from-source-or-download-the-distribution) to build pinot distribution from source. The resulting JAR file can be found in `pinot/target/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`

Next, you need to change the execution config in the [job spec](./#create-schema-configuration) to the following -

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

You can check out the sample job spec here.

To run Spark ingestion, you need the following jars in your classpath

* `pinot-batch-ingestion-spark` plugin jar - available in `plugins-external` directory in the package
* `pinot-all` jar - available in `lib` directory in the package

These jars can be specified using `spark.driver.extraClassPath`   or any other option.&#x20;

```
spark.driver.extraClassPath =>
pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar
```

For loading any other plugins that you want to use,  you can use -

```
spark.driver.extraJavaOptions =>
-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins
```



The complete spark-submit command should look as follows

```
export PINOT_VERSION=0.10.0
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin

spark-submit //
--class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand //
--master local --deploy-mode client //
--conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins" //
--conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark/pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" //
-conf "spark.executor.extraClassPath=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark/pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" //
local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar -jobSpecFile /path/to/spark_job_spec.yaml
```

Please ensure environment variables `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

**Note**: You should change the `master` to `yarn` and `deploy-mode` to `cluster` for production environments

{% hint style="info" %}
We have stopped including `spark-core` dependency in our jars post 0.10.0 release. Users can try 0.11.0-SNAPSHOT and later versions of `pinot-batch-ingestion-spark` in case of any runtime issues. You can either [build from source ](../../getting-started/)or [download latest master build jars](https://repo.startreedata.io/artifactory/external-snapshots/org/apache/pinot/).
{% endhint %}

{% hint style="info" %}
For Pinot version prior to 0.10.0, the spark plugin is located in `${PINOT_DISTRIBUTION_DIR}/plugins/pinot-batch-ingestion/pinot-batch-ingestion-spark/pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar`
{% endhint %}
