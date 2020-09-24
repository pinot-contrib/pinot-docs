---
description: For Real Time Pinot tables
---

# Decoupling Controller from the Data Path

## Ingestion bottleneck on the Pinot Controller

In case of RealTime Pinot tables, whenever a Pinot server finishes consuming a segment, it goes through a segment completion protocol sequence. The default approach is to upload this segment to the lead Pinot controller which in turn will persist it in the segment store \(eg: NFS, S3 or HDFS\). As a result, since all the realtime segments flow through the controller, it can become a bottleneck and slow down the overall ingestion rate. To overcome this limitation, we've added a new policy which allows bypassing the controller in the segment completion protocol. This is internally named as "Peer Download policy"

## Overview of Peer Download policy

When this is enabled, the Pinot servers will attempt to upload the completed segment to the segment store directly, thus by-passing the controller. Once this is finished, it will update the controller with the corresponding segment metadata. The reason this policy is named `peer download` is because if the segment store is unavailable for whatever reason, the corresponding segments can still be downloaded directly from the Pinot servers.

## How to enable Peer Download for Segments

This scheme only works for real-time tables using the Low Level Consumer \(LLC\) mode. The changes needed are as follows:

### Controller Config

Add the following things to the Controller Config

```text
controller.allow.hlc.tables=false
controller.enable.split.commit=true

```

### Server Config

Add the following things to the server config

```text
pinot.server.instance.segment.store.uri=<URI of segment store>
pinot.server.instance.enable.split.commit=true
pinot.server.instance.enable.commitend.metadata=true
```

Here URI of segment store should point to the desired path in the corresponding segment store \(eg: `file://` or `hdfs://` or `s3://`\)

### Table config

Add the following things to the real-time [segments config](https://docs.pinot.apache.org/configuration-reference/table#segmentsconfig):

```text
    "segmentsConfig": {
      ...
      
      "completionConfig": {
        "completionMode": "DOWNLOAD"
      }
      "peerSegmentDownloadScheme": "http"
    }

```

In this case, the `peerSegmentDownloadScheme` can be either `http` or `https`. 









