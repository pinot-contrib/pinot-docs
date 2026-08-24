# Funnel Analysis Functions

Apache Pinot supports a few funnel functions:

## Null handling

When [advanced null handling](../../build-with-pinot/querying-and-sql/null-value-support.md#advanced-null-handling-support) is enabled, funnel functions ignore rows whose timestamp is null. `FUNNELCOUNT` also ignores a row when any `CORRELATE_BY` column is null. Null step predicates are treated as not matched, while null optional extra fields do not discard an otherwise matched event.

With advanced null handling disabled, Pinot continues to read each column's configured default null value.

## FunnelMaxStep

`FunnelMaxStep` evaluates user interactions within a specified time window to determine the furthest step reached in a predefined sequence of actions. By analyzing event timestamps and conditions set for each step, it identifies the maximum progression point for each user, ensuring that the sequence follows the configured order or other specific rules like strict timestamp increases or event uniqueness. This function is instrumental in funnel analysis, helping businesses and analysts understand user behavior, measure conversion rates, and identify potential drop-offs in critical user journeys.

{% content-ref url="funnelmaxstep-1.md" %}
[funnelmaxstep-1.md](funnelmaxstep-1.md)
{% endcontent-ref %}



## FunnelMatchStep

Similar to `FunnelMaxStep` , this function returns an array which reflects the matching status for the steps.

{% content-ref url="funnelmaxstep-2.md" %}
[funnelmaxstep-2.md](funnelmaxstep-2.md)
{% endcontent-ref %}





## FunnelCompleteCount

This function evaluates all funnel events and returns how many times the user has completed the full steps.

{% content-ref url="funnelcompletecount.md" %}
[funnelcompletecount.md](funnelcompletecount.md)
{% endcontent-ref %}

## FunnelCount

This function evaluates funnel steps and returns the distinct correlated counts for each step.

{% content-ref url="funnelcount.md" %}
[funnelcount.md](funnelcount.md)
{% endcontent-ref %}

## Additional Reference Pages

- [funnelmaxstep.md](funnelmaxstep.md)
- [FUNNELSTEPDURATIONSTATS](../aggregation/funnelstepdurationstats.md)
- [FUNNELEVENTSFUNCTIONEVAL](../aggregation/funneleventsfunctioneval.md)
