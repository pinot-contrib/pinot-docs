# Spark

Pinot supports Apache spark as a processor to create and push segment files to the database. Pinot distribution is bundled with the Spark code to process your files and convert and upload them to Pinot.

You can follow the [wiki](../../getting-started/running-pinot-locally.md#build-from-source-or-download-the-distribution) to build pinot distribution from source. The resulting JAR file can be found in `pinot/target/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`

Next, you need to change the execution config in the [job spec](./#create-schema-configuration) to the following -

```text
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

Now, add the pinot jar to spark's classpath using following options -

```text
spark.driver.extraJavaOptions =>
-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins

OR

spark.driver.extraClassPath =>
pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar
```

Please ensure environment variables `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

Finally execute the spark job using the command -

```text
export PINOT_VERSION=0.8.0
export PINOT_DISTRIBUTION_DIR=${PINOT_ROOT_DIR}/pinot-distribution/target/apache-pinot-${PINOT_VERSION}-bin/apache-pinot-${PINOT_VERSION}-bin

cd ${PINOT_DISTRIBUTION_DIR}

${SPARK_HOME}/bin/spark-submit \\
  --class org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \\
  --master "local[2]" \\
  --deploy-mode client \\
  --conf "spark.driver.extraJavaOptions=-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml" \\
  --conf "spark.driver.extraClassPath=${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar" \\
  local://${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \\
  -jobSpecFile ${PINOT_DISTRIBUTION_DIR}/examples/batch/airlineStats/sparkIngestionJobSpec.yaml
```

**Note**: You should change the `master` to `yarn` and `deploy-mode` to `cluster` for production.

