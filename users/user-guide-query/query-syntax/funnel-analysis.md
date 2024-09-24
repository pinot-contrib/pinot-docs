# Funnel Analysis

Apache Pinot supports a few funnel functions:

## FunnelMaxStep

`FunnelMaxStep` evaluates user interactions within a specified time window to determine the furthest step reached in a predefined sequence of actions. By analyzing event timestamps and conditions set for each step, it identifies the maximum progression point for each user, ensuring that the sequence follows the configured order or other specific rules like strict timestamp increases or event uniqueness. This function is instrumental in funnel analysis, helping businesses and analysts understand user behavior, measure conversion rates, and identify potential drop-offs in critical user journeys.

{% content-ref url="../../../configuration-reference/functions/funnelmaxstep-1.md" %}
[funnelmaxstep-1.md](../../../configuration-reference/functions/funnelmaxstep-1.md)
{% endcontent-ref %}



## FunnelMatchStep

Similar to `FunnelMaxStep` , this function returns an array which reflects the matching status for the steps.

{% content-ref url="../../../configuration-reference/functions/funnelmaxstep-2.md" %}
[funnelmaxstep-2.md](../../../configuration-reference/functions/funnelmaxstep-2.md)
{% endcontent-ref %}





## FunnelCompleteCount

This function evaluates all funnel events and returns how many times the user has completed the full steps.

{% content-ref url="../../../configuration-reference/functions/funnelmaxstep.md" %}
[funnelmaxstep.md](../../../configuration-reference/functions/funnelmaxstep.md)
{% endcontent-ref %}





