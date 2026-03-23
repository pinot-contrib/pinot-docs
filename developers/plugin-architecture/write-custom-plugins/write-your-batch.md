# Batch Segment Fetcher Plugin

You can also implement your own segment fetchers for other file systems and load into Pinot system with an external jar.

All you need to do is to implement a class that extends the interface of [SegmentFetcher](https://github.com/apache/pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/segment/fetcher/SegmentFetcher.java) and provide config to Pinot Controller and Server as follows:

```
pinot.controller.segment.fetcher.`<protocol>`.class =`<class path to your implementation>
```

or

```
pinot.server.segment.fetcher.`<protocol>`.class =`<class path to your implementation>
```

You can also provide other configs to your fetcher under config-root `pinot.server.segment.fetcher.<protocol>`

## Related pages

* [Write Custom Plugins](./) -- how to package and deploy plugins
* [Filesystem Plugin](pluggable-storage.md) -- write a custom PinotFS storage backend
* [Segment Fetchers](../../developers-and-contributors/extending-pinot/segment-fetchers.md) -- HDFS fetcher configuration and custom fetcher implementation
