---
description: Decouple the controller from the data path for real-time Pinot tables.
---

# Decoupling Controller from the Data Path

## Ingestion bottleneck on the Pinot Controller

In case of RealTime Pinot tables, whenever a Pinot server finishes consuming a segment, it goes through a segment completion protocol sequence. The default approach is to upload this segment to the lead Pinot controller which in turn will persist it in the segment store (eg: NFS, S3 or HDFS). As a result, since all the real-time segments flow through the controller, it can become a bottleneck and slow down the overall ingestion rate. To overcome this limitation, we've added a new stream-level configuration which allows bypassing the controller in the segment completion protocol.&#x20;

### Stream Config

Add the following stream-level config to allow the server to upload the completed segment to the deep store directly.&#x20;

```
realtime.segment.serverUploadToDeepStore = true
```

When this is enabled, the Pinot servers will attempt to upload the completed segment to the segment store directly, thus by-passing the controller. Once this is finished, it will update the controller with the corresponding segment metadata.&#x20;

{% hint style="info" %}
`pinot.server.segment.store.uri` is optional by default. However, this config is required so that the server knows where the deep store is. Hence, before enabling `realtime.segment.serverUploadToDeepStore` on the table, make sure that the `pinot.server.segment.store.uri` is configured on the servers.
{% endhint %}

## Overview of Peer Download policy

Peer download policy is introduced to allow failure recovery, incase of a failure to upload the completed segment to the deep store. If the segment store is unavailable for whatever reason, the corresponding segments can still be downloaded directly from the Pinot servers. Hence, the policy  is called `peer download`.

**Note:** This is available in the latest master (not in 0.5.0 release)

## How to enable Peer Download for Segments

This scheme only works for real-time tables using the Low Level Consumer (LLC) mode. The changes needed are as follows:

### Controller Config

Add the following things to the Controller Config

```
controller.allow.hlc.tables=false
controller.enable.split.commit=true
```

### Server Config

Add the following things to the server config

```
pinot.server.instance.segment.store.uri=<URI of segment store>
pinot.server.instance.enable.split.commit=true
pinot.server.storage.factory.class.(scheme)=<the corresponding Pinot FS impl>
```

Here URI of segment store should point to the desired _**full**_ path in the corresponding segment store with both filesystem scheme and path (eg: `file://dir` or `hdfs://path` or `s3://path`)

Replace the last field (i.e., _scheme_) of _pinot.server.storage.factory.class.(scheme)_ with the corresponding scheme (e.g., _hdfs, s3_ or _gcs_) of the segment store URI configured above. Then put the PinotFS subclass for the scheme as the config value.

### Table config

Add the following things to the real-time [segments config](https://docs.pinot.apache.org/configuration-reference/table#segmentsconfig):

```
    "segmentsConfig": {
      ...
      "peerSegmentDownloadScheme": "http"
    }
```

In this case, the `peerSegmentDownloadScheme` can be either `http` or `https`.

### Config for failure case handling

Enabling peer download may incur LLC segments failed to be uploaded to segment store in some failure cases, e.g. segment store is unavailable during segment completion. Add the following controller config to enable the upload retry by a controller periodic job asynchronously.

```
controller.realtime.segment.deepStoreUploadRetryEnabled=true
```
