---
description: Pinot controller admin UI reference.
---

# Controller Admin API

The controller admin UI at `http://<controller-host>:<port>/help` is the quickest way to inspect and exercise Pinot's administrative endpoints. Use it for schema, table, and segment operations when you want the interactive Swagger surface instead of raw curl examples.

## What It Covers

<table>
  <thead>
    <tr>
      <th>Area</th>
      <th>Typical task</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tables</td>
      <td>List, inspect, delete, and update table configs</td>
    </tr>
    <tr>
      <td>Schemas</td>
      <td>List, inspect, create, and delete schemas</td>
    </tr>
    <tr>
      <td>Segments</td>
      <td>List, inspect, upload, and reload segments</td>
    </tr>
  </tbody>
</table>

## Operational Reminder

Controller APIs are for administrative tasks. Use the broker query API for querying Pinot, even if the controller UI also exposes a query console.

## What this page covered

- The controller Swagger UI entry point.
- Which administrative tasks belong in the controller UI.
- Why the broker query API still owns SQL execution.

## Next step

Use the Swagger UI to confirm the endpoint shape, then jump to the controller API examples page when you need exact curl payloads.

## Related pages

- [API Reference](README.md)
- [Controller API Examples](controller-api.md)
- [Broker Query API](query-api.md)
- [Query Response Format](query-response-format.md)
