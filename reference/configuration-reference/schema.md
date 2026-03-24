---
description: Schema configuration reference.
---

# Schema Configuration

This page points to the schema reference for column definitions, null-handling behavior, and complex types. The full schema examples and field-spec tables remain in the existing schema page.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Schema name | Must match the table name without the OFFLINE or REALTIME suffix | [Schema](../../configuration-reference/schema.md) |
| Dimension, metric, and datetime specs | Define the logical shape of the data | [Schema](../../configuration-reference/schema.md) |
| Null handling | Controls schema-level null semantics for column-based null storage | [Schema](../../configuration-reference/schema.md) |
| Complex fields | Documents MAP support and child field specs | [Schema](../../configuration-reference/schema.md) |

## What this page covered

- The schema concerns that matter for configuration work.
- Where to find the canonical field-spec tables and examples.
- The relationship between schema shape and table configuration.

## Next step

Review the schema page before you touch table config so the field names, types, and null behavior stay aligned.

## Related pages

- [Configuration Reference](README.md)
- [Table](../../configuration-reference/table.md)
- [First Table + Schema](../../basics/getting-started/first-table-and-schema.md)
- [Table Overview](../../basics/components/table/README.md)
