---
description: >-
  This guide shows you how to import data from files stored in Amazon S3.
---

# Amazon S3

Enable the [Amazon S3](https://aws.amazon.com/s3/) file system backend by including the `pinot-s3` plugin. In the controller or server configuration, add the config:

```
-Dplugins.dir=/opt/pinot/plugins -Dplugins.include=pinot-s3
```

## S3A URI scheme support

Starting in Pinot 1.3.0, the `pinot-s3` plugin supports both the `s3://` and `s3a://` URI schemes. Both schemes use the same underlying AWS SDK v2 client and identical configuration — the only difference is the URI prefix. This allows Pinot to integrate with Hadoop-based ecosystems and tools that standardize on the `s3a://` scheme.

To use the `s3a://` scheme, specify it in your deep store paths and file system configuration:

```
controller.data.dir=s3a://path/to/data/directory/
pinot.controller.storage.factory.class.s3a=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.controller.storage.factory.s3a.region=us-east-1
pinot.controller.segment.fetcher.protocols=file,http,s3a
pinot.controller.segment.fetcher.s3a.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

All configuration properties documented below work identically for both the `s3` and `s3a` schemes.

{% hint style="info" %}
By default Pinot loads all the plugins, so you can just drop this plugin there. Also, if you specify `-Dplugins.include`, you need to put all the plugins you want to use, e.g. `pinot-json`, `pinot-avro` , `pinot-kafka-3.0...`
{% endhint %}

You can configure the S3 file system using the following options:

<table>
  <thead>
    <tr>
      <th>Configuration</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>region</td>
      <td>The AWS Data center region in which the bucket is located</td>
    </tr>
    <tr>
      <td>accessKey</td>
      <td>(Optional) AWS access key required for authentication. This should only be used for testing purposes as we don't store these keys in secret.</td>
    </tr>
    <tr>
      <td>secretKey</td>
      <td>(Optional) AWS secret key required for authentication. This should only be used for testing purposes as we don't store these keys in secret.</td>
    </tr>
    <tr>
      <td><p></p><p>endpoint</p></td>
      <td>(Optional) Override endpoint for s3 client.</td>
    </tr>
    <tr>
      <td><p></p><p>disableAcl</p></td>
      <td>If this is set to`false`, bucket owner is granted full access to the objects created by pinot. Default value is `true`.</td>
    </tr>
    <tr>
      <td>serverSideEncryption</td>
      <td>(Optional) The server-side encryption algorithm used when storing this object in Amazon S3 (Now supports `aws:kms`), set to null to disable SSE.</td>
    </tr>
    <tr>
      <td>ssekmsKeyId</td>
      <td>(Optional, but **required** when `serverSideEncryption=aws:kms`) Specifies the AWS KMS key ID to use for object encryption. All GET and PUT requests for an object protected by AWS KMS will fail if not made via SSL or using SigV4.</td>
    </tr>
    <tr>
      <td>ssekmsEncryptionContext</td>
      <td>(Optional) Specifies the AWS KMS Encryption Context to use for object encryption. The value of this header is a base64-encoded UTF-8 string holding JSON with the encryption context key-value pairs.</td>
    </tr>
    <tr>
      <td>requestChecksumCalculation</td>
      <td>(Optional) Controls whether checksums are calculated for request payloads. Default: `WHEN_SUPPORTED`. Options: `WHEN_SUPPORTED`, `WHEN_REQUIRED`.</td>
    </tr>
    <tr>
      <td>responseChecksumValidation</td>
      <td>(Optional) Controls whether checksums are validated on response payloads. Default: `WHEN_SUPPORTED`. Options: `WHEN_SUPPORTED`, `WHEN_REQUIRED`.</td>
    </tr>
    <tr>
      <td>useLegacyMd5Plugin</td>
      <td>(Optional) When set to `true`, uses the LegacyMd5Plugin to restore pre-2.30.0 MD5 checksum behavior. Default: `false`.</td>
    </tr>
    <tr>
      <td>enableCrossRegionAccess</td>
      <td>(Optional) If you want to copy objects b/w two buckets that lie in different regions. Defaults to `true` if not configured.</td>
    </tr>
  </tbody>
</table>

Each of these properties should be prefixed by `pinot.[node].storage.factory.s3.` where `node` is either `controller` or `server` depending on the config

e.g.

```
pinot.controller.storage.factory.s3.region=ap-southeast-1
```

S3 Filesystem supports authentication using the [DefaultCredentialsProviderChain](https://docs.aws.amazon.com/AWSJavaSDK/latest/javadoc/com/amazonaws/auth/DefaultAWSCredentialsProviderChain.html). The credential provider looks for the credentials in the following order -

* Environment Variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (RECOMMENDED since they are recognized by all the AWS SDKs and CLI except for .NET), or `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` (only recognized by Java SDK)
* Java System Properties - `aws.accessKeyId` and `aws.secretKey`
* Web Identity Token credentials from the environment or container
* Credential profiles file at the default location `(~/.aws/credentials)` shared by all AWS SDKs and the AWS CLI
* Credentials delivered through the Amazon EC2 container service if `AWS_CONTAINER_CREDENTIALS_RELATIVE_URI` environment variable is set and security manager has permission to access the variable,
* Instance profile credentials delivered through the Amazon EC2 metadata service

You can also specify the accessKey and secretKey using the properties. However, this method is not secure and should be used only for POC setups.

## Checksum validation

{% hint style="info" %}
Checksum configuration is available starting in Pinot 1.4.
{% endhint %}

Starting with AWS SDK 2.30.0, the S3 client enables request and response checksum validation by default. Pinot exposes configuration properties to control this behavior.

### Request and response checksums

By default, Pinot sets both `requestChecksumCalculation` and `responseChecksumValidation` to `WHEN_SUPPORTED`, which means the S3 client calculates checksums on uploads and validates them on downloads whenever the API supports it. This provides data integrity verification for segment files stored in your deep store.

If you want to disable automatic checksums and only use them when the S3 API strictly requires it, set both properties to `WHEN_REQUIRED`:

```
pinot.controller.storage.factory.s3.requestChecksumCalculation=WHEN_REQUIRED
pinot.controller.storage.factory.s3.responseChecksumValidation=WHEN_REQUIRED
```

<table>
  <thead>
    <tr>
      <th>Value</th>
      <th>Behavior</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>WHEN_SUPPORTED</td>
      <td>Calculate/validate checksums whenever the API supports it (default)</td>
    </tr>
    <tr>
      <td>WHEN_REQUIRED</td>
      <td>Only calculate/validate checksums when the API requires it</td>
    </tr>
  </tbody>
</table>

### LegacyMd5Plugin for S3-compatible stores

Some S3-compatible object stores (e.g. MinIO, Ceph, or older AWS configurations) require the legacy `Content-MD5` header on requests. After the AWS SDK 2.30.0 upgrade, these stores may return errors like:

```
Missing required content hash for this request: Content-MD5 or x-amz-content-sha256
```

To restore the pre-2.30.0 MD5 checksum behavior, enable the `useLegacyMd5Plugin` option:

```
pinot.controller.storage.factory.s3.useLegacyMd5Plugin=true
```

This adds the LegacyMd5Plugin to the S3 client, which sends the `Content-MD5` header that these stores expect.

{% hint style="warning" %}
Only enable `useLegacyMd5Plugin` if your S3-compatible store requires the legacy MD5 header. For standard AWS S3, the default checksum behavior is recommended.
{% endhint %}

## Examples

### Job spec

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

### Controller config

```
controller.data.dir=s3://path/to/data/directory/
controller.local.temp.dir=/path/to/local/temp/directory
controller.enable.split.commit=true
pinot.controller.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.controller.storage.factory.s3.region=ap-southeast-1
pinot.controller.segment.fetcher.protocols=file,http,s3
pinot.controller.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

### Server config

```
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.server.storage.factory.s3.region=ap-southeast-1
pinot.server.storage.factory.s3.httpclient.maxConnections=50
pinot.server.storage.factory.s3.httpclient.socketTimeout=30s
pinot.server.storage.factory.s3.httpclient.connectionTimeout=2s
pinot.server.storage.factory.s3.httpclient.connectionTimeToLive=0s
pinot.server.storage.factory.s3.httpclient.connectionAcquisitionTimeout=10s
pinot.server.segment.fetcher.protocols=file,http,s3
pinot.server.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```

### Minion config

```
pinot.minion.storage.factory.class.s3=org.apache.pinot.plugin.filesystem.S3PinotFS
pinot.minion.storage.factory.s3.region=ap-southeast-1
pinot.minion.segment.fetcher.protocols=file,http,s3
pinot.minion.segment.fetcher.s3.class=org.apache.pinot.common.utils.fetcher.PinotFSSegmentFetcher
```
