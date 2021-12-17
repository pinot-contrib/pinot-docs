---
description: This section contains reference documentation for the mode function.
---

# mode

Get the most frequent value in a group. 
When multiple modes are present it gives the minimum of all the modes. 
This behavior can be overridden to get the maximum or the average mode.

## Signature

> MODE(colName, [reducerType])

## Usage Examples

These examples are based on the [Batch Quick Start](../../basics/getting-started/quick-start.md#batch).

```sql
select mode(yearID) AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001

```

| value   | 
| ------------- |
| 2008 | 

```sql
select mode(yearID, 'AVG') AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001

```

| value   | 
| ------------- |
| 2010 | 

```sql
select mode(yearID, 'MIN') AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001

```

| value   | 
| ------------- |
| 2008 | 


```sql
select mode(yearID, 'MAX') AS value
from baseballStats 
WHERE AtBatting != 0 AND yearID > 2001

```

| value   | 
| ------------- |
| 2012 |     