---
description: Ingestion job specification reference.
---

# Ingestion Job Spec Reference

This page points to the offline ingestion job specification reference, which is the dense configuration surface for segment generation and push workflows. The canonical templating and execution-framework details remain in the original job-spec page.

## Key Areas

| Area | Why it matters | Source |
| --- | --- | --- |
| Templating | Parameterized job specs with runtime overrides | [Ingestion Job Spec](../../configuration-reference/job-specification.md) |
| Execution framework | Standalone, Hadoop, Spark, and push mode selection | [Ingestion Job Spec](../../configuration-reference/job-specification.md) |
| Segment naming | How generated segment names are derived | [Ingestion Job Spec](../../configuration-reference/job-specification.md) |

## What this page covered

- The offline ingestion job-spec surface and its main use cases.
- The source page that contains the full property matrix.
- The relationship between job specs and batch ingestion guides.

## Next step

Use this page as the jump-off point, then validate the job spec against the segment push workflow you are running.

## Related pages

- [Configuration Reference](README.md)
- [Ingestion](../../configuration-reference/ingestion.md)
- [Batch Ingestion](../../manage-data/data-import/batch-ingestion/README.md)
