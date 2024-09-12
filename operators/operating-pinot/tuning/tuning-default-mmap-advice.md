---
description: Adding on behalf of https://github.com/dinoocch
---

# Tuning Default MMAP Advice

{% hint style="info" %}
These details are only relevant for Pinot running on either Linux or potentially Darwin.
{% endhint %}

Pinot uses memory-mapped files to support larger than memory data sizes. In certain cases, additional tuning can help improve latency.

## Important concepts

Under the hood, `mmap()` exposes each file as a large virtual address space backed by a [page cache](https://en.wikipedia.org/wiki/Page\_cache). This page cache uses the free memory in the system to make file io cheaper.

When a memory page is requested, the kernel will first check the page cache (if the page was accessed) and fall back or "fault" to reading the page from disk if it is not present.

When a new page is read into the cache or allocated for active use, an LRU algorithm is used to choose the evicted page which will be used. There are some nuances here and substantial literature if you are interested, for example [this article](https://lwn.net/Articles/851184/).

The kernel additionally provides read-ahead, which reads additional data into the page cache with the expectation that it might be useful soon. This is great for usecases which sequentially access data, but may not be as useful for non-sequential accesses, and can result in evicting useful pages.

## Supported configuration

{% hint style="warning" %}
Currently madvise configuration is only supported for the UnsafePinotBuffer. To get full benefit, you most likely want to configure `pinot.offheap.prioritize.bytebuffer -> false`.
{% endhint %}

Currently the only exposed configuration is `pinot.server.mmap.advice.default` which accepts the following values (corresponding to [posix\_madvise](https://man7.org/linux/man-pages/man3/posix\_madvise.3.html) options)

* `NORMAL` - The default behavior. Readahead is based on the block `read_ahead_kb` config.
* `RANDOM` - Advises random reads, discouraging reading ahead.
* `SEQUENTIAL` - Advises sequential access, suggesting more aggressive read ahead and reclamation of read pages.
* `WILL_NEED` - Advises the pages will all be accessed, and may be equivalent to an async read call for the data.
* `DONT_NEED` - Advises that the application will not need any of the pages, and evicts them from the cache. Most likely you should never set this option.

Note that since this support is currently configured per-instance without granular options, operators will have to choose a value that best suits their general query patterns and hardware.

### Choosing a value

As a loose rule of thumb, readahead is often very valuable for sequential workloads with substantial scanning, slow disks with a relatively high memory to disk ratio, or cases where io performs best when batched into larger requests (for example network attached cloud storage).

On Linux, you can see the configured read\_ahead setting:

{% code title="Implying 128kb readahead on device sda" %}
```
$ cat /sys/block/sda/queue/read_ahead_kb
128
```
{% endcode %}

Additional utilities are available to help understand io and cache performance.

For example [bcc/readahead](https://github.com/iovisor/bcc/blob/master/tools/readahead\_example.txt) provide a summary of when (and if) read ahead pages are used.

Outputs like:

```
[ /usr/share/bcc/tools ]$ sudo ./readahead
Tracing... Hit Ctrl-C to end.
^C
Read-ahead unused pages: 11353563
Histogram of read-ahead used page age (ms):     age (ms)            : count     distribution
         0 -> 1          : 0        |                                        |
         2 -> 3          : 0        |                                        |
         4 -> 7          : 0        |                                        |
         8 -> 15         : 0        |                                        |
        16 -> 31         : 0        |                                        |
        32 -> 63         : 0        |                                        |
        64 -> 127        : 0        |                                        |
       128 -> 255        : 0        |                                        |
       256 -> 511        : 0        |                                        |
       512 -> 1023       : 0        |                                        |
      1024 -> 2047       : 4        |                                        |
      2048 -> 4095       : 0        |                                        |
      4096 -> 8191       : 0        |                                        |
      8192 -> 16383      : 184      |****************************************| 
```

May indicate that readahead is both unused and actually potentially harming performance.

## Related Issues

* [pinot#12166](https://github.com/apache/pinot/issues/12166)
* [pinot#13721](https://github.com/apache/pinot/pull/13721)
