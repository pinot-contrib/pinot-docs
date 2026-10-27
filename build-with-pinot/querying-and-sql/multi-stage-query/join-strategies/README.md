# Join strategies

## Distribution-hint validation

The planner rejects distribution pairs that can lose or duplicate join results. A `BROADCAST` side, or a `LOCAL` scan of a table hinted `is_replicated='true'`, supplies the whole side to each worker. Except for the single-worker FULL-join case below, both sides cannot be whole.

When one side is whole:

- `INNER` permits either side to be whole.
- `LEFT`, `ANTI`, `ASOF`, `LEFT_ASOF` and `LEFT_MARK` require the right side to be whole.
- `RIGHT` requires the left side to be whole.
- `SEMI` requires the right side to be whole, except that a whole left side with the right side hashed on equi-join keys is also valid.
- `FULL` with equi-join keys cannot use a whole side; hash both sides on the join keys instead.

When neither side is whole, equi-join keys are required and both distributions must match and must not be `RANDOM`. `LOCAL`/`LOCAL` is accepted on the user's guarantee that the inputs are co-partitioned; the planner cannot verify that guarantee.

A `FULL` join without equi-join keys runs on one worker and requires each side to use `RANDOM` or `BROADCAST`. Other joins without equi-join keys need a whole side, subject to the join-type rules above. Previously accepted unsafe hints can now fail planning; remove or correct the hints instead of relying on their earlier results.

In order to execute a join, all the rows of the tables to be joined need to be in the same place. In classical databases like Postgres this is not a problem, as there is usually a single server (or all servers have all the data). But in distributed databases like Pinot, where rows of the tables are distributed across servers, data needs to be shuffled between servers (at least in the general case). This data shuffle is expensive and can be a bottleneck for the query performance.

The most simple way to execute the join would be to move all data into a single server, as shown in the diagram below.

![](<../../../../.gitbook/assets/image (15).png>)

*Dotted arrows mean shuffle while solid arrows mean in-server transfer*

This approach may work for small tables, but it would not scale for large tables that do not fit into a single server. Pinot assumes this is going to be the common case, so it never uses this technique. It is shown here only to help understand the shuffling problem.

What Pinot does is to create _virtual partitions_ at query time. These virtual partitions are created in such a way that Pinot can guarantee that rows that need to be joined are sent to the same server but at the same time it tries to minimize the amount of data that needs to be shuffled between servers.

There are several strategies Pinot can use to reduce data shuffle. Some of them are so effective that they can be used to execute the join without any data shuffle at all, but they are only applicable in some cases.

The strategies, in order of effectiveness, are:

1. [Lookup joins](lookup-join-strategy.md)
2. [Colocated joins](colocated-join-strategy.md)
3. [Query time partition join](query-time-partition-join-strategy.md)
4. [Random + broadcast join](random-+-broadcast-join-strategy.md)

These techniques are explained in more detail in the their own pages. More join strategies will be added in the future. They are listed in the GitHub issue [#14518](https://github.com/apache/pinot/issues/14518).
