---
description: Schedule queries to prioritize them.
---

# Query Scheduling

Pinot supports various different query scheduling mechanisms to allow for more control around which queries have priority when executing on the server instances.&#x20;

Currently, there are the following options that can be configured using the `pinot.query.scheduler.name` configuration:

* First Come First Serve (`fcfs`) (Default)
* Bounded First Come First Serve (`bounded_fcfs`)
* Token Bucket (`tokenbucket`)

### First Come First Serve

This is the default scheduling mechanism, which simply allows all queries to execute in a first come, first serve mechanism. For most deployments, this is likely sufficient, but high QPS deployments that have skewed query workloads may struggle under this scheduling mechanism.

### Bounded Schedulers

Bounded query schedulers operate under a context of a single table, and additionally respect the following configurations:

* `pinot.query.scheduler.threads_per_query_pct` (default 20%) will allow individual threads to take up to this percentage of the threads allocated to a table resource group
* `pinot.query.scheduler.table_threads_soft_limit_pct` (default 30%) indicates that once this percentage of the available threads are taken up by this resource group, the scheduler should prefer other resource groups but still allow queries in this group
* `pinot.query.scheduler.table_threads_hard_limit_pct` (default 45%) indicates that once this percentage of the available threads are taken up, the scheduler should not schedule any more queries for this resource group

#### Bounded First Come First Serve

Similarly to the "first come first serve" scheduling mechanism, this option will bound the resource utilization by ensuring that only a certain number of queries are running concurrently (set using the `pinot.query.scheduler.query_runner_threads` configuration).

#### Token Bucket Scheduler

This query scheduling mechanism will periodically grant tokens to each scheduler group, and will select the group to run with the highest number of tokens assigned to it. This can be configured using the following configurations:

* `pinot.query.scheduler.tokens_per_ms` will indicate how many tokens to generate per second for each group. The default value for this is the number of threads avaialble to run queries (which will essentially attempt to schedule more queries than is possible to run)
* `pinot.query.scheduler.token_lifetime_ms` indicates the lifetime of every allocated token

This scheduler applies a linear decay for groups that have recently been scheduled to avoid starvation and allow groups with light workloads to be scheduled.
