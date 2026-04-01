---
description: This section contains reference documentation for the SHA function.
---

# sha

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

<table>
  <thead>
    <tr>
      <th>event\_id</th>
      <th>location</th>
      <th>hash</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>282776561</td>
      <td>80406178a3d70a3d714041d5c28f5c28f6</td>
      <td>b914583284ac29d2bd3c9d097245b031d99d687d</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
The row returned will be different if you run this example as the data is ingested in real-time.
{% endhint %}
