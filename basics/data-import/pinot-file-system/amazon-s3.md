# Amazon S3

You can enable [Amazon S3](https://aws.amazon.com/s3/) Filesystem backend by including the plugin `pinot-s3` .

```text
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-s3
```

You can also configure the S3 filesystem using the following options -

* `region` - The AWS Data centre region in which the bucket is located
* `accessKey` - \(Optional\) AWS access key required for authentication. This should only be used for testing purposes as we don't store these keys in secret.
* `secretKey` - \(Optional\) AWS secret key required for authentication. This should only be used for testing purposes as we don't store these keys in secret.
* `disableAcl` - If this is set to `false`, bucket owner is granted full access to the objects created by pinot. Default value is `true`. 

Each of these properties should be prefixed by `pinot.[node].storage.factory.s3.` where `node` is either `controller` or `server` depending on the config

e.g.

```text
pinot.controller.storage.factory.s3.region=ap-southeast-1
```

S3 Filesystem supports authentication using the [DefaultCredentialsProviderChain](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/DefaultAWSCredentialsProviderChain.html). The credential provider looks for the credentials in the following order -

* Environment Variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` \(RECOMMENDED since they are recognized by all the AWS SDKs and CLI except for .NET\), or `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` \(only recognized by Java SDK\)
* Java System Properties - `aws.accessKeyId` and `aws.secretKey`
* Web Identity Token credentials from the environment or container
* Credential profiles file at the default location `(~/.aws/credentials)` shared by all AWS SDKs and the AWS CLI
* Credentials delivered through the Amazon EC2 container service if `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` environment variable is set and security manager has permission to access the variable,
* Instance profile credentials delivered through the Amazon EC2 metadata service

You can also specify the accessKey and secretKey using the properties. However, this method is not secure and should be used only for POC setups.

### Examples

#### Job spec

```yaml
executionFrameworkSpec:
    name: 'standalone'
    segmentGenerationJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentGenerationJobRunner'
    segmentTarPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentTarPushJobRunner'
    segmentUriPushJobRunnerClassName: 'org.apache.pinot.plugin.ingestion.batch.standalone.SegmentUriPushJobRunner'
jobType: SegmentCreationAndTarPush
inputDirURI: 's3://pinot-bucket/pinot-ingestion/batch-input/'
outputDirURI: 's3://pinot-bucket/pinot-ingestion/batch-output/'
overwriteOutput: true
pinotFSSpecs:
    - scheme: s3
      className: org.apache.pinot.plugin.filesystem.S3PinotFS
      configs:
        region: 'ap-southeast-1'
recordReaderSpec:
    dataFormat: 'csv'
    className: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReader'
    configClassName: 'org.apache.pinot.plugin.inputformat.csv.CSVRecordReaderConfig'
tableSpec:
    tableName: 'students'
pinotClusterSpecs:
    - controllerURI: 'http://localhost:9000'
```

#### Controller config

```text
controller.data.dir=s3://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.controller.storage.factory.s3.region=ap-southeast-1
pinot.controller.segment.fetcher.protocols=file,http,s3
pinot.controller.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### Server config

```text
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.server.storage.factory.s3.region=ap-southeast-1
pinot.server.segment.fetcher.protocols=file,http,s3
pinot.server.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

#### 

#### 

