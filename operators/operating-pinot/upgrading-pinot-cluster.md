# Upgrading Pinot with confidence

Pinot has unit and integration tests that verify that the system can work well as long as all components are in the same version. Further, each PR goes through reviews in which Pinot committers can decide whether a PR may break compatibility, and if so, how it can be avoided. Even with all this, it is useful to be able to test an upgrade before actually subjecting a live installation to upgrades.

Pinot has multiple components that run independently of each other. Therefore upgrading a mission-critical pinot cluster will result in scenarios where one component is running an old version and the other a new version of Pinot. It can also happen that this state \(of multiple versions\) is in place for days together. Or, we may need to revert the upgrade process \(usually done in reverse order\) -- possibly due to reasons outside of Pinot.

Pinot is highly configurable, so it is possible that there are few installations that use the same combination of configuration options as any one site does. Therefore, it may be that a defect or incompatibility exists with that particular combination of configurations, and went undetected in reviews.

In practice, installations upgrade their deployments to newer versions periodically, or when an urgent bug-fix is needed, or when a new release is published. It is also possible that an installation has not upgraded Pinot for a long time. Either way, it is usually the case that installations will pull in a lot more new/modified software than the feature or bug fix they need. 

In a mission-critical pinot installation, the administrators require that during \(and certainly after\) the upgrade, correctness of normal operations \(segment pushes, ingestion from streams, queries, monitoring, etc.\) is not compromised..

For the reasons stated above, it is useful to have a way to test an upgrade before applying to the production cluster. Further, it is useful to be able to customize the tests to run using the unique table/schema/configurations/queries combination that an installation is using. If an installation has not upgraded pinot for a long time, it is useful to know what parts may be incompatible during the upgrade process, and schedule downtime if required.

As of release 0.8.0, Pinot has a compatibility tester that you can run before upgrading your installation with a new release. You can specify your own configuration for the pinot components, your table configurations and schema, your queries with your sample data, and run the compatibility suite \(you can build one based on the sample test suite provided\).

We recommend that you upgrade Pinot components in the following order \(if you need to roll back a release, do it in the reverse order\).

1. Controller
2. Broker
3. Server
4. Minion

The test suite runs through an upgrade sequence of upgrading each component one at a time \(Controller, Broker, and Server in that order\), and then reverting the new versions back to old version \(Server, Broker and Controller, in that order\). In between each upgrade or downgrade \(referred to as a "phase"\), a set of test operations \(as specified in the test suite\) is executed. The operations are specified in a declarative way in yaml files. At present the following operations are supported:

* Create a table with a specific table config and schema
* Create a segment from an input file and add it to a table
* Run the queries specified in a file and verify the results as specified in a file
* Create a Kafka topic with specified number of partitions
* Ingest rows into the Kafka topic \(so that server can consume them\)
* Delete a table
* Delete a segment from a table

One or more of the above set of test operations can be done during each phase in the rollout or roll-back sequence. The test suite does the following steps in sequence

1. Set up a cluster with old version of controller, broker and server
2. Stop old controller, start new controller
3. Stop old broker and start new broker
4. Stop old server and start new server
5. Stop new server and start old server
6. Stop new broker and start old broker
7. Stop new controller and start old controller

Tests can be run in each phase, \(i.e. between any two steps outlined above, or, after the last step\). You can create a test suite by writing yaml files for each phase. You may decide to skip any phase by _not_ providing a yaml file for that phase.

The idea here is as follows:

* Any persisted files \(such as table configs, schemas, data segments, etc.\) are readable during and after upgrade.
* Any persisted files while in the new release are readable after a rollback \(in case that is required\).
* Protocols between the components evolve in a backward compatible manner.

Minion upgrades is currently not supported in the test framework. Also, testing compatibility of the controller APIs is not supported at this time. We welcome contributions in these areas.

See the [yaml files](https://github.com/apache/incubator-pinot/tree/master/compatibility-verifier/sample-test-suite) provided along with the source code for examples on how to specify operations for each roll forward/backward stage of the upgrade process.

## Running the compatibility test suite

You can use command line tools to verify compatibility against a previous release of Pinot \(the tools support a `--help` option\). Here are the steps to follow:

### Determine the revision of Pinot you are currently running

This can be a commit hash, or a release tag \(such as `release-0.7.1`\). You can obtain the commit hash from the controller URI `/version`.

### Determine the version of pinot that you wish to upgrade to

This can be a tag or a commit hash.

### Clone the current master

Clone the current source code from Pinot and go to the appropriate directory. This will get you the latest compatibility tester.

```text
git clone https://github.com/apache/incubator-pinot.git
cd compatibility-verifier
```

### Check out and build the two releases

Checkout and build the sources of the two releases you want to verify. Make sure your working directory \(-w argument\) has enough space to hold two build trees, logs, etc.

```text
./checkoutAndBuild.sh -o $OLD_COMMIT -n $NEW_COMMIT -w /tmp/wd
```

### Run compatibility regression suite

```text
./compCheck.sh -w /tmp/wd -t $TEST_SUITE_DIR
```

The command will exit with a status of 0 if all tests pass, 1 otherwise.

NOTE:

* You can run the `compCheck.sh` command multiple times against the same build, you just need to make sure to provide a new working directory name each time.
* You can specify a `-k` option to the `compCheck.sh` command to keep the cluster \(Kafka, Pinot components\) running. You can then attempt the operation \(e.g. a query\) that failed. 

## Query and Data files

So we can use the same data files and queries, upload them as new set of rows \(both in Realtime and Offline tables\), we encourage you to modify your table schema by adding an integer column called `generationNumber`. Each time data is uploaded, the values written as `__GENERATION_NUMBER__` in your input data files \(or in the query files\) are substituted with a new integer value.

This allows the test suite to upload the same data as different segments, and verify that the current data as well as the previously uploaded ones are all working correctly in terms of responding to queries. The test driver automatically tests all previous generation numbers as well.

See the [input file](https://github.com/apache/incubator-pinot/blob/master/compatibility-verifier/sample-test-suite/config/data/RealtimeFeatureTest1-data-00.csv) and [query file](https://github.com/apache/incubator-pinot/blob/master/compatibility-verifier/sample-test-suite/config/queries/feature-test-2-sql-realtime.queries) in sample test suite for use of this feature. 

Consider an input line in the data file like the following:

```text
123456,__GENERATION_NUMBER__,"s1-0",s2-0,1,2,m1-0-0;m1-0-1,m2-0-0;m2-0-1,3;4,6;7,Java C++ Python,01a0bc,k1;k2;k3;k4;k5,1;1;2;2;2,"{""k1"":1,""k2"":1,""k3"":2,""k4"":2,""k5"":2}",10,11,12.1,13.1
```

When this input line is processed to generate a segment or push data into Kafka, the string `__GENERATION_NUMBER__` will be replaced with an integer \(each yaml file is one generation, starting with 0\).

Similarly, consider a query like the following:

```text
SELECT longDimSV1, intDimMV1, count(*) FROM FeatureTest2 WHERE generationNumber = __GENERATION_NUMBER__ AND (stringDimSV1 != 's1-6' AND longDimSV1 BETWEEN 10 AND 1000 OR (intDimMV1 < 42 AND stringDimMV2 IN ('m2-0-0', 'm2-2-0') AND intDimMV2 NOT IN (6,72))) GROUP BY longDimSV1, intDimMV1 ORDER BY longDimSV1, intDimMV1 LIMIT 20
```

Before issuing this query, the tests will substitute the string `__GENERATION_NUMBER__` with the actual generation number like above.

Use of generation number is optional \(the test suite will try to substitute the string `__GENERATION_NUMBER__` , but not find it if your input files do not have the string in them\). Another way is to ensure that the set of queries you provide for each phase also includes results from the previous phases. That will make sure that all previously loaded data are also considered in the results when the queries are issued.

## Result files

The first time you set up your result files, it is important that you look over the results carefully and make sure that they are correct.

In some cases, Pinot may provide different results each time you execute a query. For example, consider the query:

```text
SELECT foo FROM T1 WHERE x = 7 GROUP BY bar LIMIT 5
```

Since `ORDER BY` is not specified, if there are more than 5 results, there is no guarantee that Pinot will return the same five rows every time. In such a case, you can include all possible values of `foo` where `x = 7` matches, and indicate that in your result file by specifying `isSuperset: true`. An example of this feature is shown below:

```text
{"isSuperset":true, "resultTable":{"dataSchema":{"columnNames":["foo"],"columnDataTypes":["LONG"]},"rows":[[11],[41],[-9223372036854775808],[32],[42],[48]]},"exceptions":[],"numServersQueried":1,"numServersResponded":1,"numSegmentsQueried":2,"numSegmentsProcessed":2,"numSegmentsMatched":2,"numConsumingSegmentsQueried":1,"numDocsScanned":13,"numEntriesScannedInFilter":120,"numEntriesScannedPostFilter":26,"numGroupsLimitReached":false,"totalDocs":66,"timeUsedMs":3,"offlineThreadCpuTimeNs":0,"realtimeThreadCpuTimeNs":352435,"segmentStatistics":[],"traceInfo":{},"minConsumingFreshnessTimeMs":1621918872017}
```

See the sample test suite for an example of how to use this in the result file.

## Sample test suite

The sample test suite provided does the following between each stage of the upgrade:

* Add a segment to an offline table
* Run queries against new segments, and all old segments added thus far.
* Add more rows to Kafka, ensuring that at least one segment is completed and at

  least some rows are left uncommitted, so that we can test correct re-consumption of those

  rows after rollout/rollback.

* Run queries against the data ingested so far.

The table configurations schemas, data and queries have been chosen in such a way as to cover the major features that Pinot supports.

As a good practice, we suggest that you build your own test suite that has the tables, schemas, queries, and system configurations used in your installation of Pinot, so that you can verify compatibility for the features/configurations that your cluster uses.

