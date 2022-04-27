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

Now, add the pinot plugins to spark's classpath using following options -

```
spark.driver.extraJavaOptions =>
-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins
```

You also need to add `pinot-batch-ingestion-spark` jar along with `pinot-all` to the `spark.driver.extraClassPath`&#x20;

This can be done as\


```
spark.driver.extraClassPath =>
pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar
```

The complete spark-submit command should look as follows

```
export PINOT_VERSION=0.10.0
export PINOT_DISTRIBUTION_DIR=/path/to/apache-pinot-${PINOT_VERSION}-bin

spark-submit //
--class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand //
--master local --deploy-mode client //
--conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" //
--conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/plugins-external/pinot-batch-ingestion/pinot-batch-ingestion-spark/pinot-batch-ingestion-spark-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar:${PINOT_DISTRIBUTION_DIR}/plugins/pinot-file-system/pinot-s3/pinot-s3-${PINOT_VERSION}-shaded.jar:${PINOT_DISTRIBUTION_DIR}/plugins/pinot-input-format/pinot-parquet/pinot-parquet-${PINOT_VERSION}-shaded.jar" //
local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar -jobSpecFile /path/to/spark_job_spec.yaml
```

Please ensure environment variables `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

**Note**: You should change the `master` to `yarn` and `deploy-mode` to `cluster` for production

{% hint style="info" %}
We have stopped including `spark-core` dependency in our jars post 0.10.0 release. Users can try 0.11.0-SNAPSHOT and later versions of `pinot-batch-ingestion-spark` in case of any runtime issues.
{% endhint %}
