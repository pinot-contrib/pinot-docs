---
description: Measure forward-index and dictionary compression coverage for a Pinot table.
---

# Compression stats

Compression stats let you inspect how much serialized column-value data Pinot stores in forward indexes and
dictionaries after compression. The feature is off by default and surfaces through the existing controller table size
and metadata APIs.

## Enable collection

Set `tableIndexConfig.compressionStatsEnabled` to `true` in the table config:

```json
{
  "tableIndexConfig": {
    "compressionStatsEnabled": true
  }
}
```

Pinot records stats only for segments built, or forward indexes rewritten, while the flag is enabled. Existing segments
are not backfilled.

## Query the stats

Use the controller APIs documented in [Controller API Examples](../../reference/api-reference/controller-api.md):

* `GET /tables/{tableName}/size` returns a `compressionStats` summary for each covered offline or realtime sub-table.
  Add `includeColumnCompressionStats=true` to include `columnCompressionStats`.
* `GET /tables/{tableName}/metadata?type=OFFLINE` returns the offline table's aggregate `compressionStats` summary.
  Add `columns=...` to scope the metadata response and `includeColumnCompressionStats=true` to include per-column
  entries.

The table-level summary reports:

| Field | Meaning |
| --- | --- |
| `uncompressedValueSizePerReplicaInBytes` | Tracked serialized value bytes for one logical copy of the covered segments |
| `forwardIndexAndDictionaryStorageSizePerReplicaInBytes` | Forward-index and dictionary bytes on disk for the same logical copy |
| `compressionRatio` | `uncompressedValueSizePerReplicaInBytes / forwardIndexAndDictionaryStorageSizePerReplicaInBytes` |
| `segmentsWithCompleteStats` | Number of logical segments that contributed complete stats |
| `totalSegments` | Total logical segments in the sub-table |
| `partialCoverage` | `true` when one or more logical segments could not contribute stats |

Per-column entries break out the column name, observed index types, aggregate sizes, ratio, and
`encodingBreakdown`. Raw forward indexes report the chunk compression type; dictionary-encoded columns report combined
forward-index and dictionary bytes.

## Coverage caveats

Only eligible forward-index columns contribute to the ratio. Columns without a forward index, and older segments that
do not have persisted value-size metadata, are excluded from the summary and from per-column coverage.

In verbose `GET /tables/{tableName}/size` responses, Pinot selects one complete replica for each logical segment when
it attaches segment-level compression fields under `segments.<segment>.serverInfo.<server>`. Other replicas still
report disk size, but not segment-level compression details.

`GET /tables/{tableName}/metadata` currently supports offline tables only. During rolling upgrades or mixed old/new
segment populations, `partialCoverage` stays `true` until Pinot can read stats for every covered logical segment.

## Controller gauges

When compression stats are available for a table, the lead controller emits these gauges:

| Gauge | Unit |
| --- | --- |
| `tableCompressionStatsRatioPercent` | Percent |
| `tableCompressionStatsUncompressedValueSizePerReplica` | Bytes |
| `tableCompressionStatsForwardIndexAndDictionaryStorageSizePerReplica` | Bytes |

These gauges are removed when collection is disabled or when no covered segment remains.
