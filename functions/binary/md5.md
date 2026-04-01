---
description: This section contains reference documentation for the MD5 function.
---

# MD5

Return MD5 digest of binary column(`bytes` type) as hex string

## Signature

> MD5(bytesCol)

## Usage Examples

These examples are based on the [Real time Quick Start](../../basics/getting-started/quick-start.md#realtime).

```sql
select event_id, location, MD5(location) AS hash
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
      <td>92a8b787e81672261aad8afcf9de3aee</td>
    </tr>
  </tbody>
</table>

{% hint style="info" %}
The row returned will be different if you run this example as the data is ingested in real-time.
{% endhint %}
