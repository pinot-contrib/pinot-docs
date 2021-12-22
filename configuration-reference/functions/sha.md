---
description: This section contains reference documentation for the SHA function.
---

# SHA

Return SHA-1 digest of binary column(`bytes` type) as hex string

## Signature

> SHA(bytesCol)

## Usage Examples

These examples are based on the [Real time Quick Start](../../basics/getting-started/quick-start.md#realtime).


```sql
select event_id, location, SHA(location) AS hash
from meetupRsvp 
limit 1
```

| event_id|	location	| hash |
| ------------- | ------------- | ------------- |
|282776561 |	80406178a3d70a3d714041d5c28f5c28f6	| b914583284ac29d2bd3c9d097245b031d99d687d|


{% hint style="info" %}
The row returned will be different if you run this example as the data is ingested in real-time. 
{% endhint %}
