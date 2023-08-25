---
description: Upload a table segment in Apache Pinot.
---

# Upload a table segment from an external source

This procedure uploads one or more table segments that have been in storage outside of Apache Pinot. This means that the data source is not configured in your [table configuration](../../configuration-reference/table.md).

You have two options. Use the Pinot Admin script if your data is on a local host or use the {nameHere} API for that or when data is on an external host, such as Amazon S3.

## Use the Pinot Admin script to upload segments

To compress and upload segment files to your Pinot server, use:

```bash
pinot-admin.sh UploadSegment -controllerHost localhost -controllerPort 9000 -segmentDir /path/to/local/dir -tableName myTable
```

All the options should be prefixed with `-` (hyphen)

| Option         | Description                               |
| -------------- | ----------------------------------------- |
| controllerHost | hostname or ip of the controller          |
| controllerPort | port of the controller                    |
| segmentDir     | local directory containing segment files  |
| tableName      | name of the table to push the segments in |

## Use the Pinot Controller API to upload segments






To reload all segments from a table, use:

```
POST /segments/{tableName}/reload
```

To reload a specific segment from a table, use:

```
POST /segments/{tableName}/{segmentName}/reload
```

Either API call will return a JSON response like this one for a successful operation:

```json
{
    "status": "200"
}
```