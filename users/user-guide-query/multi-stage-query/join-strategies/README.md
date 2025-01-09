# Join strategies

In order to execute a join, all the rows of the tables to be joined need to be in the same place. In classical databases like Postgres this is not a problem, as there is usually a single server (or all servers have all the data). But in distributed databases like Pinot, where rows of the tables are distributed across servers, data needs to be shuffled between servers (at least in the general case). This data shuffle is expensive and can be a bottleneck for the query performance.

The most simple way to execute the join would be to move all data into a single server, as shown in the diagram below.

<figure><img src="../../../../.gitbook/assets/image (15).png" alt="" width="563"><figcaption><p>Dotted arrows mean shuffle while strong arrows mean in-server transfer</p></figcaption></figure>

This approach may work for small tables, but it would not scale for large tables that do not fit into a single server. Pinot assumes this is going to be the common case, so it never uses this technique. It is shown here only to help to understand shuffling problem.

What Pinot does is to create _virtual partitions_ at query time. These virtual partitions are created in such a way that Pinot can guarantee that rows that need to be joined are sent to the same server but at the same time it tries to minimize the amount of data that needs to be shuffled between servers.

There are several strategies Pinot can use to reduce data shuffle. Some of them are so effective that they can be used to execute the join without any data shuffle at all, but they are only applicable in some cases.

The strategies in order of effectiveness are:

1. To not shuffle data at all. Pinot supports the following cases:
   1. [Lookup joins](lookup-join-strategy.md)
   2. [Colocated joins](colocated-join-strategy.md)
2. [Query time partition Join](query-time-partition-join-strategy.md)
3. [Random + broadcast](random-+-broadcast-join-strategy.md)

These techniques are explained in more detail in the their own sections. More join strategies will be added in the future. The are listed in the GitHub issue [#14518](https://github.com/apache/pinot/issues/14518).
