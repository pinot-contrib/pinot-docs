---
description: >-
  This section contains reference documentation for the FUNNELCOUNT function.
---

# FUNNELCOUNT

Funnel analytics aggregation function. 

Returns array of distinct correlated counts for each funnel step.


## Signature

> **FUNNEL_COUNT (**
>> STEPS ( **predicate1, predicate2** ... ), 
>> 
>> CORRELATED_BY ( **correlation_column** ),
>> 
>> SETTINGS ( **setting1, setting2** ... ) 
>> **)**


| Parameter       | Arguments              | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|-----------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *STEPS*         | `predicates 1...n`     | (required) These are individual predicates representing funnel steps which are applied on rows selected by the `where` clause. Distinct values from the `correlation_column` that satisfy these predicates are counted per step. For example, all filtered rows that match `url = '/checkout'` are unionized into a set. Sets are intersected with the sets resulted from the preceding steps, each step retaining only individuals present in previous steps. Finally, unique counts are returned for each step in the funnel.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| *CORRELATED_BY* | `correlation_column`   | (required) Column to leverage for funnel correlation, distinct values from this column are counted per step during aggregation. Only dictionary-encoded columns are supported.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| *SETTINGS*      | `settings 1...n`       | (optional) Settings to select and configure a funnel counting strategy: <br/><p>`bitmap` (default): This strategy is accurate for _INT_ column, but approximate for other cases where hash codes are used in distinct counting and there may be hash collisions. For accurate distinct counting on all column types, use 'set' instead. See also [DISTINCTCOUNTBITMAP](distinctcountbitmap.md).</p><p>`set`: This strategy uses [fastutil](https://fastutil.di.unimi.it/) hash sets. Use with care, unbounded memory cost. See also [DISTINCTCOUNT](distinctcount.md).</p><p>`theta_sketch`: This strategy leverages [Theta Sketch](https://datasketches.apache.org/docs/Theta/ThetaSketchFramework.html) framework to provide an approximate funnel count with a small memory footprint. See also [DISTINCTCOUNTTHETASKETCH](distinctcountthetasketch.md).</p><p>`nominalEntries`: theta-sketch strategy parameter (defaults to 4096). Can only be used in conjunction with *theta_sketch* setting.</p><p>`partitioned`: This strategy counts funnel steps per segment, then sums up step counts across segments. Correlation column should be configured as partition column for this strategy. See also [SEGMENTPARTITIONEDDISTINCTCOUNT](segmentpartitioneddistinctcount.md).</p><p>`sorted`: This strategy counts funnel steps per segment with zero memory footprint. Correlation column should be configured as sort column for this strategy. Can only be used in conjunction with `partitioned` setting.</p> |

## Usage Examples

Many datasets are time series in nature, tracking events of an entity over time.
An example of such a dataset could be a user analytics activity log from a commerce web application. 

### Example

| user_id | event_time              | url                    |
|---------|-------------------------|------------------------|
| U1      | 2021-10-01 09:01:00.000 | /product/listing       |
| U2      | 2021-10-01 09:17:00.000 | /product/search        |
| U1      | 2021-10-01 09:33:00.000 | /product/details       |
| U1      | 2021-10-01 09:47:00.000 | /cart/add              |
| U3      | 2021-10-01 10:02:00.000 | /product/listing       |
| U3      | 2021-10-01 10:05:00.000 | /product/search        |
| U2      | 2021-10-01 10:06:00.000 | /product/search        |
| U2      | 2021-10-01 10:15:00.000 | /checkout/start        |
| U2      | 2021-10-01 10:16:00.000 | /cart/add              |
| U3      | 2021-10-01 11:17:00.000 | /product/details       |
| U2      | 2021-10-01 11:18:00.000 | /checkout/confirmation |
| U3      | 2021-10-01 11:21:00.000 | /cart/add              |
| U1      | 2021-10-01 11:33:00.000 | /cart/add              |
| U1      | 2021-10-01 11:46:00.000 | /checkout/start        |
| U1      | 2021-10-01 11:54:00.000 | /checkout/confirmation | 

#### Funnel
We want to analyse the following checkout funnel: 
* */cart/add*
* */checkout/start*
* */checkout/confirmation*

#### Counts
We want to answer the following questions about the above funnel:
* How many users entered the top of the funnel? 
* How many of these users proceeded to the second step? 
* How many users reached the bottom of the funnel after completing all steps? 

#### Query
```sql
select 
  FUNNEL_COUNT(
    STEPS(
      url = '/cart/add', 
      url = '/checkout/start', 
      url = '/checkout/confirmation'),
    CORRELATED_BY(user_id)
  ) AS counts
from user_log 
```

| counts  |
|---------|
| 3, 2, 2 |

> **Notes**
> 
> Notice that although *U1* user added to cart twice, it still counted as one conversion in the first step, as we report on unique counts rather than total events.
> Also notice that although *U2* events were logged out of order, we still counted the user as converted.
> 

> **Equivalence**
> 
> The above query is equivalent to the below presto SQL query:
> ```sql
> select 
>    ARRAY[
>      count_if(steps[1]),
>      count_if(steps[1] and steps[2]),
>      count_if(steps[1] and steps[2] and steps[3])
>    ] as counts
>  from (
>    select 
>      ARRAY[
>        bool_or(url = '/cart/add'),
>        bool_or(url = '/checkout/start'),
>        bool_or(url = '/checkout/confirmation')
>      ] as steps
>    from user_log
>    group by user_id
>  )
> ```

#### Settings
For a large dataset we could use for example a *theta_sketch* strategy, or furthermore, partition the data by user_id and leverage a *partitioned* strategy.
It is also important to filter in the *where* clause so to aggregate only necessary rows.
```sql
select 
  FUNNEL_COUNT(
    STEPS(
      url = '/cart/add', 
      url = '/checkout/start', 
      url = '/checkout/confirmation'),
    CORRELATED_BY(user_id),
    SETTINGS('theta_sketch', 'nominalEntries=4096')
  ) AS counts
from user_log 
where url in ('/cart/add', '/checkout/start', '/checkout/confirmation')
```

| counts  |
|---------|
| 3, 2, 2 |

### Another Example
We now want to learn how many users checkout after a text search; as opposed to other entry points such as browsing a product category listing. 
We want to then analyse the following funnel:
* */product/search*
* */cart/add*
* */checkout/start*
* */checkout/confirmation*

#### Query
```sql
select 
  FUNNEL_COUNT(
    STEPS(
      url = '/product/search',
      url = '/cart/add', 
      url = '/checkout/start', 
      url = '/checkout/confirmation'),
    CORRELATED_BY(user_id)
  ) AS counts
from user_log 
```

| counts     |
|------------|
| 2, 2, 1, 1 |

> **Notes**
>
> Notice that *U1* is not counted in this funnel, as the user did not perform any product search.
> Both *U2* and *U3* entered the top of the funnel and performed the second step, but only *U2* converted to the bottom of the funnel.
