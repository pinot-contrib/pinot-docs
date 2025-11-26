# FunnelCompleteCount

The `FunnelCompleteCount` function in Pinot is designed to track user progress through a predefined series of steps or stages in a funnel, such as user interactions on a website from page views to purchases. This function is particularly useful for analyzing how many times users progress through the whole conversion processes within a specified time window.

## **Syntax**

```sql
FunnelCompleteCount(
    timestampExpression, 
    windowSize, 
    numberSteps, stepExpression
    [, stepExpression[, stepExpression, ...]]
    [, mode [, mode, ... ]]
)
```

## Return

This function returns how many times the funnel has been went through.

## Arguments

1. **`timestampExpression`**:
   * **Type**: Expression in `TIMESTAMP` or `LONG`
   * **Description**: This is an expression that evaluates to the timestamp of each event. It's used to determine the order of events for a particular user or session. The timestamp is crucial for evaluating whether subsequent actions fall within the specified window.
2. **`windowSize`**:
   * **Type**: `LONG`
   * **Description**: Specifies the size of the time window in which the sequence of funnel steps must occur. The window is defined in milliseconds. This parameter sets the maximum allowed time between the first and the last step in the funnel for them to be considered as part of the same user journey.
3. **`numberSteps`**:
   * **Type**: `Integer`
   * **Description**: Defines the total number of distinct steps in the funnel. This count should match the number of `stepExpression` parameters provided.
4. **`stepExpression`**:
   * **Type**: `Boolean Expression`
   * **Description**: These are expressions that define each step in the funnel. Typically, these are conditions that evaluate whether a specific event type or action has occurred. Multiple step expressions are separated by commas, with each expression corresponding to a step in the funnel sequence.
5. **`mode`** (optional):
   * **Type**: String
   * **Description**: Defines additional modes or options that alter how the funnel analysis is calculated. Common modes might include settings to handle overlapping events, reset the window upon each step, or other custom behaviors specific to the needs of the funnel analysis. If unspecified, the default behavior as defined by Pinot is used.



## **Optional Mode Supported**

### STRICT\_DEDUPLICATION

The `STRICT_DEDUPLICATION` mode ensures that repeating occurrences of the same event condition within a funnel sequence disrupt further processing of the funnel for that user session. This mode is crucial when it's important to identify and measure unique, non-repeated actions in a sequence, ensuring each step of the funnel represents a distinct action.

#### Practical Impact

* **Event Sequence Interruption**: When an event that satisfies a current step condition occurs repeatedly without progression to the next step, `strict_deduplication` interrupts and essentially ends the analysis of the funnel for that sequence. This prevents the funnel from incorrectly advancing if the same action is merely repeated instead of moving through the intended steps.
* **Enhanced Accuracy in Funnel Progression**: This mode is useful for scenarios where the continuity and progression of distinct steps are critical for accurate conversion analysis. It avoids the misinterpretation of user engagement where repeated similar actions might otherwise suggest a false progression through the funnel.

#### Example

For instance, if a funnel is designed to track user progression from a homepage visit, to a search, to adding an item to a cart, and then to checkout, the `strict_deduplication` mode would stop processing the funnel sequence if the user performs multiple searches without proceeding to add an item to the cart. This ensures that only a linear, non-repetitive progression through these steps is considered as valid funnel movement.

This mode helps maintain the integrity of each step in the user's journey, ensuring that the data reflects true user behavior without overcounting repetitive actions that do not lead to actual progression.



### STRICT\_ORDER

The `strict_order` mode enforces a stringent sequence order for events within a funnel. This mode ensures that the progression through the steps follows the exact specified order without any intervening events that are not part of the defined sequence.

#### Behavior of `strict_order`

* **Sequence Adherence**: The `strict_order` mode requires that the events occur in the exact order specified without any other types of events intervening. If an event occurs that is not the next expected step in the defined sequence, the analysis of the funnel for that user session is halted.
* **Early Termination**: In the presence of an out-of-sequence event, the analysis stops, and the maximum event level is determined as the last correct step in the sequence before the interruption. For instance, in a specified sequence of A -> B -> C, if the sequence is A -> B -> D, then the funnel analysis terminates after B because D is not the expected next step (C).

#### Practical Impact

* **Enhanced Precision in Path Analysis**: This mode is particularly valuable when the precise order of actions is critical for the analysis, such as in strict process flows where each step must be followed in a specific order to be considered successful.
* **Avoids Misinterpretation**: It prevents the misinterpretation of funnel progress where intervening or unordered events could suggest a misleading path through the funnel.

#### Example

Consider a scenario where a funnel is set up to track user progression through the following steps: logging in (A), searching for products (B), adding a product to the cart (C), and completing a purchase (D). Using the `strict_order` mode, if the sequence goes A -> B -> E -> C, the analysis will terminate after B because E (an unexpected event like viewing account details) intervenes before C, the expected next step. Therefore, the maximum step reached is reported as 2, representing the successful completion of steps A and B only.

This mode is crucial for scenarios requiring strict compliance to process steps, ensuring that only users who follow the exact intended sequence are counted in the funnel analysis.

### STRICT\_INCREASE

The `strict_increase`  is designed to ensure that the sequence of events being analyzed has strictly increasing timestamps. This mode is crucial for accurately tracking and analyzing user behavior in scenarios where the chronological order of events directly impacts the interpretation of user actions within a funnel.

#### Behavior of `strict_increase`

* **Timestamp Order**: This mode requires that each subsequent event in the funnel must have a timestamp greater than the previous event. It ensures that the user's actions are not only in the correct sequence but also follow a temporal progression without any backtracking or simultaneous actions.
* **Analysis Integrity**: If any event in the sequence does not adhere to the strictly increasing order by timestamp, the analysis for that sequence either stops at that point or ignores the out-of-order event, depending on how critical the temporal sequence is to the funnel's logic.

#### Practical Impact

* **Temporal Validation**: This mode is particularly useful in scenarios where the timing of events is crucial, such as in sessions where actions must follow one another in real-time to be considered valid. It validates the sequence not just by the type of event, but also by ensuring that these events are progressively happening over time.
* **Avoiding Data Errors**: It helps in avoiding potential data errors or anomalies where timestamps might not have been recorded correctly, or events may appear out of order due to system errors or delays in logging events.

#### Example

Consider a funnel designed to analyze a user's journey from visiting a website to making a purchase, defined by the following steps: page visit (A), item addition (B), checkout initiation (C), and payment completion (D). Using the `strict_increase` mode, the funnel will only consider sequences where each action occurs later than the previous. If a user's sequence is A (t1) -> B (t2) -> A (t3) -> C (t4) with t3 being less than or equal to t2, then the analysis will ignore the second occurrence of A or terminate, depending on the specific implementation and requirements of the analysis.

This mode helps ensure that the funnel analysis reflects true, linear progress through the intended actions, with each step occurring in a timely, sequential manner.

### KEEP\_ALL

The `KEEP_ALL` mode is designed to ensure that all events in the data set are considered in the analysis, even if they do not match any of the specified step conditions in the funnel sequence. This mode is particularly useful for comprehensive data analysis where the context of non-matching events may still provide valuable insights about user behavior or system performance.

#### Behavior of `KEEP_ALL`

* **Inclusive Analysis**: In the `KEEP_ALL` mode, the funnel function includes every event within the specified time window in the analysis, regardless of whether these events correspond to the predefined steps in the funnel. This allows for a more holistic view of the user's actions during the session.
* **Context Retention**: By including all events, this mode helps retain the full context of a user's session, capturing activities that may not be directly related to the funnel but could influence or explain the user's behavior and decisions at other points.

#### Practical Impact

* **Enhanced Insight**: This mode is invaluable for scenarios where understanding the entirety of user interactions is crucial, such as in complex user journeys where additional actions between the main funnel steps might influence the outcomes or indicate other patterns of interest.
* **Data Completeness**: It prevents data loss from filtering out non-matching events, which can be important when analyzing sessions for comprehensive patterns, troubleshooting issues, or performing detailed user journey analysis.

#### Example

Consider a scenario where a funnel is set up to track user progress through steps like logging in, searching for a product, and making a purchase. With `KEEP_ALL` mode enabled, if a user performs additional actions such as updating profile information or viewing terms and conditions, these events are also included in the analysis. This comprehensive inclusion allows analysts to see a fuller picture of what the user did during their session, not just the actions that directly relate to the funnel. This can reveal if other activities are detracting from the main conversion goals, or if they are part of a broader user engagement that doesn't neatly fit into the primary funnel steps.

This mode helps to ensure that no potential insights are lost by excluding events, making it a powerful option for detailed analysis and understanding of user interactions beyond the strict confines of the predefined funnel steps.

## Examples

### Data Set

<table><thead><tr><th>event_name</th><th width="287">ts</th><th>user_id</th></tr></thead><tbody><tr><td>screen_viewed</td><td>1718112402</td><td>1</td></tr><tr><td>screen_clicked</td><td>1718112403</td><td>1</td></tr><tr><td>purchased</td><td>1718112404</td><td>1</td></tr><tr><td>screen_viewed</td><td>1718112405</td><td>1</td></tr><tr><td>screen_clicked</td><td>1718112406</td><td>1</td></tr><tr><td>purchased</td><td>1718112407</td><td>1</td></tr><tr><td>screen_viewed</td><td>1718112405</td><td>2</td></tr><tr><td>screen_clicked</td><td>1718112406</td><td>2</td></tr><tr><td>purchased</td><td>1718112407</td><td>2</td></tr><tr><td>screen_viewed</td><td>1718112404</td><td>3</td></tr><tr><td>screen_clicked</td><td>1718112405</td><td>3</td></tr><tr><td>cart_viewed</td><td>1718112406</td><td>3</td></tr><tr><td>purchased</td><td>1718112407</td><td>3</td></tr><tr><td>screen_viewed</td><td>1717939609</td><td>4</td></tr><tr><td>screen_clicked</td><td>1718112405</td><td>4</td></tr><tr><td>purchased</td><td>1718112405</td><td>4</td></tr></tbody></table>

### Queries

#### Query funnels

```sql
SELECT user_id,
  funnelCompleteCount(
    ts,
    '1000000',
    4,
    event_name = 'screen_viewed',
    event_name = 'screen_clicked',
    event_name = 'cart_viewed',
    event_name = 'purchased'
  ) as rounds
FROM clickstreamFunnel
GROUP BY user_id
ORDER BY user_id
```

**Response**

<table data-header-hidden><thead><tr><th width="530"></th><th></th></tr></thead><tbody><tr><td>user_id</td><td>rounds</td></tr><tr><td>1</td><td>0</td></tr><tr><td>2</td><td>0</td></tr><tr><td>3</td><td>1</td></tr><tr><td>4</td><td>0</td></tr></tbody></table>



#### Query with strict\_order

```sql
SELECT user_id,
  funnelCompleteCount(
    ts,
    '1000000',
    3,
    event_name = 'screen_viewed',
    event_name = 'screen_clicked',
    event_name = 'purchased',
    'strict_order'
  ) as rounds
FROM clickstreamFunnel
GROUP BY user_id
ORDER BY user_id
```

**Response**

| user\_id | rounds |
| -------- | ------ |
| 1        | 2      |
| 2        | 1      |
| 3        | 1      |
| 4        | 0      |

#### Query with strict\_order and keep\_all

```sql
SELECT user_id,
  funnelCompleteCount(
    ts,
    '100000',
    3,
    event_name = 'screen_viewed',
    event_name = 'screen_clicked',
    event_name = 'purchased',
    'strict_order',
    'keep_all'
  ) as rounds
FROM clickstreamFunnel
GROUP BY user_id
ORDER BY user_id
```

**Response**

| user\_id | rounds |
| -------- | ------ |
| 1        | 2      |
| 2        | 1      |
| 3        | 0      |
| 4        | 0      |

#### Query with longer window

```sql
SELECT user_id,
  funnelMaxStep(
    ts,
    '1000000',
    3,
    event_name = 'screen_viewed',
    event_name = 'screen_clicked',
    event_name = 'purchased',
    'strict_order'
  ) as rounds
FROM clickstreamFunnel
GROUP BY user_id
ORDER BY user_id
```

**Response**

<table data-header-hidden><thead><tr><th width="530"></th><th></th></tr></thead><tbody><tr><td>user_id</td><td>rounds</td></tr><tr><td>1</td><td>2</td></tr><tr><td>2</td><td>1</td></tr><tr><td>3</td><td>1</td></tr><tr><td>4</td><td>1</td></tr></tbody></table>

