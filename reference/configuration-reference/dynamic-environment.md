---
description: Environment-variable substitution reference for Pinot configs.
---

# Dynamic Environment Reference

This page points to the configuration reference for environment-variable substitution. The existing page remains the canonical source for placeholder syntax and component-availability caveats.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Placeholder syntax | Lets operators templatize config values | [Dynamic Environment](../../configuration-reference/dynamic-environment.md) |
| Component scope | Explains where environment variables must exist | [Dynamic Environment](../../configuration-reference/dynamic-environment.md) |

## What this page covered

- The config substitution surface for deployment-specific values.
- The safety caveat around component-wide environment availability.
- The source page for the complete placeholder rules.

## Next step

Use `${NAME}` or `${NAME:DEFAULT}` only when the same value is safe to resolve across the Pinot components that need it.

## Related pages

- [Configuration Reference](README.md)
- [Table](../../configuration-reference/table.md)
- [Job Spec](../../configuration-reference/job-specification.md)
