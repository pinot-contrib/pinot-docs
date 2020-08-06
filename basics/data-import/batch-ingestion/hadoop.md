# Hadoop

Pinot supports[ Apache Hadoop](https://hadoop.apache.org/) as a processor to create and push segment files to the database. Pinot distribution is bundled with the Spark code to process your files and convert and upload them to Pinot.

You can follow the \[wiki\] to build pinot distribution from source. The resulting JAR file can be found in `incubator-pinot/target/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar`

Next, you need to change the execution config in the job spec to the following -

```text
# executionFrameworkSpec: Defines ingestion jobs to be running.
executionFrameworkSpec:

	# name: execution framework name
  name: 'hadoop'

  # segmentGenerationJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentGenerationJobRunner interface.
  segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentGenerationJobRunner'

  # segmentTarPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentTarPushJobRunner interface.
  segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentTarPushJobRunner'

  # segmentUriPushJobRunnerClassName: class name implements org.apache.pinot.spi.batch.ingestion.runner.SegmentUriPushJobRunner interface.
  segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.hadoop.HadoopSegmentUriPushJobRunner'
  
	# extraConfigs: extra configs for execution framework.
  extraConfigs:

    # stagingDir is used in distributed filesystem to host all the segments then move this directory entirely to output directory.
    stagingDir: your/local/dir/staging 
```

You can check out the sample job spec here.

Finally execute the hadoop job using the command -

```text
export PINOT_VERSION=0.5.0-SNAPSHOT
export PINOT_DISTRIBUTION_DIR=${PINOT_ROOT_DIR}/pinot-distribution/target/apache-pinot-incubating-${PINOT_VERSION}-bin/apache-pinot-incubating-${PINOT_VERSION}-bin
export HADOOP_CLIENT_OPTS="-Dplugins.dir=${PINOT_DISTRIBUTION_DIR}/plugins -Dlog4j2.configurationFile=${PINOT_DISTRIBUTION_DIR}/conf/pinot-ingestion-job-log4j2.xml"

hadoop jar  \\
        ${PINOT_DISTRIBUTION_DIR}/lib/pinot-all-${PINOT_VERSION}-jar-with-dependencies.jar \\
        org.apache.pinot.tools.admin.command.LaunchDataIngestionJobCommand \\
        -jobSpecFile ${PINOT_DISTRIBUTION_DIR}/examples/batch/airlineStats/hadoopIngestionJobSpec.yaml
```

Please ensure environment variables `PINOT_ROOT_DIR` and `PINOT_VERSION` are set properly.

