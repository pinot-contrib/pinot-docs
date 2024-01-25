# GapFill Function For Time-Series Dataset

{% hint style="info" %}
GapFill Function is **only supported with the single-stage query engine (v1)**.&#x20;
{% endhint %}

Many of the datasets are time series in nature, tracking state change of an entity over time. The granularity of recorded data points might be sparse or the events could be missing due to network and other device issues in the IOT environment. But analytics applications which are tracking the state change of these entities over time, might be querying for values at lower granularity than the metric interval.

Here is the sample data set tracking the status of parking lots in parking space.

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:01:00.000 | 1            |
| P2    | 2021-10-01 09:17:00.000 | 1            |
| P1    | 2021-10-01 09:33:00.000 | 0            |
| P1    | 2021-10-01 09:47:00.000 | 1            |
| P3    | 2021-10-01 10:05:00.000 | 1            |
| P2    | 2021-10-01 10:06:00.000 | 0            |
| P2    | 2021-10-01 10:16:00.000 | 1            |
| P2    | 2021-10-01 10:31:00.000 | 0            |
| P3    | 2021-10-01 11:17:00.000 | 0            |
| P1    | 2021-10-01 11:54:00.000 | 0            |

We want to find out the total number of parking lots that are occupied over a period of time which would be a common use case for a company that manages parking spaces.

Let us take 30 minutes' time bucket as an example:

| timeBucket/lotId        | P1  | P2  | P3 |
| ----------------------- | --- | --- | -- |
| 2021-10-01 09:00:00.000 | 1   | 1   |    |
| 2021-10-01 09:30:00.000 | 0,1 |     |    |
| 2021-10-01 10:00:00.000 |     | 0,1 | 1  |
| 2021-10-01 10:30:00.000 |     | 0   |    |
| 2021-10-01 11:00:00.000 |     |     | 0  |
| 2021-10-01 11:30:00.000 | 0   |     |    |

If you look at the above table, you will see a lot of missing data for parking lots inside the time buckets. In order to calculate the number of occupied park lots per time bucket, we need gap fill the missing data.

### The Ways of Gap Filling the Data

There are two ways of gap filling the data: FILL\_PREVIOUS\_VALUE and FILL\_DEFAULT\_VALUE.

FILL\_PREVIOUS\_VALUE means the missing data will be filled with the previous value for the specific entity, in this case, park lot, if the previous value exists. Otherwise, it will be filled with the default value.

FILL\_DEFAULT\_VALUE means that the missing data will be filled with the default value. For numeric column, the defaul value is 0. For Boolean column type, the default value is false. For TimeStamp, it is January 1, 1970, 00:00:00 GMT. For STRING, JSON and BYTES, it is empty String. For Array type of column, it is empty array.

We will leverage the following the query to calculate the total occupied parking lots per time bucket.

### Aggregation/Gapfill/Aggregation

#### Query Syntax

```
SELECT time_col, SUM(status) AS occupied_slots_count
FROM (
    SELECT GAPFILL(time_col,'1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','2021-10-01 09:00:00.000',
                   '2021-10-01 12:00:00.000','30:MINUTES', FILL(status, 'FILL_PREVIOUS_VALUE'),
                    TIMESERIESON(lotId)), lotId, status
    FROM (
        SELECT DATETIMECONVERT(event_time,'1:MILLISECONDS:EPOCH',
               '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','30:MINUTES') AS time_col,
               lotId, lastWithTime(is_occupied, event_time, 'INT') AS status
        FROM parking_data
        WHERE event_time >= 1633078800000 AND  event_time <= 1633089600000
        GROUP BY 1, 2
        ORDER BY 1
        LIMIT 100)
    LIMIT 100)
GROUP BY 1
LIMIT 100
```

#### Workflow

The most nested sql will convert the raw event table to the following table.

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:00:00.000 | 1            |
| P2    | 2021-10-01 09:00:00.000 | 1            |
| P1    | 2021-10-01 09:30:00.000 | 1            |
| P3    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P3    | 2021-10-01 11:00:00.000 | 0            |
| P1    | 2021-10-01 11:30:00.000 | 0            |

The second most nested sql will gap fill the returned data as following:

| timeBucket/lotId        | P1 | P2 | P3 |
| ----------------------- | -- | -- | -- |
| 2021-10-01 09:00:00.000 | 1  | 1  | 0  |
| 2021-10-01 09:30:00.000 | 1  | 1  | 0  |
| 2021-10-01 10:00:00.000 | 1  | 1  | 1  |
| 2021-10-01 10:30:00.000 | 1  | 0  | 1  |
| 2021-10-01 11:00:00.000 | 1  | 0  | 0  |
| 2021-10-01 11:30:00.000 | 0  | 0  | 0  |

The outermost query will aggregate the gapfilled data as follows:

| timeBucket              | totalNumOfOccuppiedSlots |
| ----------------------- | ------------------------ |
| 2021-10-01 09:00:00.000 | 2                        |
| 2021-10-01 09:30:00.000 | 2                        |
| 2021-10-01 10:00:00.000 | 3                        |
| 2021-10-01 10:30:00.000 | 2                        |
| 2021-10-01 11:00:00.000 | 1                        |
| 2021-10-01 11:30:00.000 | 0                        |

There is one assumption we made here that the raw data is sorted by the timestamp. The Gapfill and Post-Gapfill Aggregation will not sort the data.

The above example just shows the use case where the three steps happen:

1. The raw data will be aggregated;
2. The aggregated data will be gapfilled;
3. The gapfilled data will be aggregated.

There are three more scenarios we can support.

### Select/Gapfill

If we want to gapfill the missing data per half an hour time bucket, here is the query:

#### Query Syntax

```
SELECT GAPFILL(DATETIMECONVERT(event_time,'1:MILLISECONDS:EPOCH',
               '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','30:MINUTES'),
               '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','2021-10-01 09:00:00.000',
               '2021-10-01 12:00:00.000','30:MINUTES', FILL(is_occupied, 'FILL_PREVIOUS_VALUE'),
               TIMESERIESON(lotId)) AS time_col, lotId, is_occupied
FROM parking_data
WHERE event_time >= 1633078800000 AND  event_time <= 1633089600000
ORDER BY 1
LIMIT 100
```

#### Workflow

At first the raw data will be transformed as follows:

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:00:00.000 | 1            |
| P2    | 2021-10-01 09:00:00.000 | 1            |
| P1    | 2021-10-01 09:30:00.000 | 0            |
| P1    | 2021-10-01 09:30:00.000 | 1            |
| P3    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:00:00.000 | 0            |
| P2    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P3    | 2021-10-01 11:00:00.000 | 0            |
| P1    | 2021-10-01 11:30:00.000 | 0            |

Then it will be gapfilled as follows:

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:00:00.000 | 1            |
| P2    | 2021-10-01 09:00:00.000 | 1            |
| P3    | 2021-10-01 09:00:00.000 | 0            |
| P1    | 2021-10-01 09:30:00.000 | 0            |
| P1    | 2021-10-01 09:30:00.000 | 1            |
| P2    | 2021-10-01 09:30:00.000 | 1            |
| P3    | 2021-10-01 09:30:00.000 | 0            |
| P1    | 2021-10-01 10:00:00.000 | 1            |
| P3    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:00:00.000 | 0            |
| P2    | 2021-10-01 10:00:00.000 | 1            |
| P1    | 2021-10-01 10:30:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P3    | 2021-10-01 10:30:00.000 | 1            |
| P1    | 2021-10-01 11:00:00.000 | 1            |
| P2    | 2021-10-01 11:00:00.000 | 0            |
| P3    | 2021-10-01 11:00:00.000 | 0            |
| P1    | 2021-10-01 11:30:00.000 | 0            |
| P2    | 2021-10-01 11:30:00.000 | 0            |
| P3    | 2021-10-01 11:30:00.000 | 0            |

#### Aggregate/Gapfill

#### Query Syntax

```
SELECT GAPFILL(time_col,'1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','2021-10-01 09:00:00.000',
               '2021-10-01 12:00:00.000','30:MINUTES', FILL(status, 'FILL_PREVIOUS_VALUE'),
               TIMESERIESON(lotId)), lotId, status
FROM (
    SELECT DATETIMECONVERT(event_time,'1:MILLISECONDS:EPOCH',
           '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','30:MINUTES') AS time_col,
           lotId, lastWithTime(is_occupied, event_time, 'INT') AS status
    FROM parking_data
    WHERE event_time >= 1633078800000 AND  event_time <= 1633089600000
    GROUP BY 1, 2
    ORDER BY 1
    LIMIT 100)
LIMIT 100
```

#### Workflow

The nested sql will convert the raw event table to the following table.

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:00:00.000 | 1            |
| P2    | 2021-10-01 09:00:00.000 | 1            |
| P1    | 2021-10-01 09:30:00.000 | 1            |
| P3    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P3    | 2021-10-01 11:00:00.000 | 0            |
| P1    | 2021-10-01 11:30:00.000 | 0            |

The outer sql will gap fill the returned data as following:

| timeBucket/lotId        | P1 | P2 | P3 |
| ----------------------- | -- | -- | -- |
| 2021-10-01 09:00:00.000 | 1  | 1  | 0  |
| 2021-10-01 09:30:00.000 | 1  | 1  | 0  |
| 2021-10-01 10:00:00.000 | 1  | 1  | 1  |
| 2021-10-01 10:30:00.000 | 1  | 0  | 1  |
| 2021-10-01 11:00:00.000 | 1  | 0  | 0  |
| 2021-10-01 11:30:00.000 | 0  | 0  | 0  |

#### Gapfill/Aggregate

#### Query Syntax

```
SELECT time_col, SUM(is_occupied) AS occupied_slots_count
FROM (
    SELECT GAPFILL(DATETIMECONVERT(event_time,'1:MILLISECONDS:EPOCH',
           '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','30:MINUTES'),
           '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss.SSS','2021-10-01 09:00:00.000',
           '2021-10-01 12:00:00.000','30:MINUTES', FILL(is_occupied, 'FILL_PREVIOUS_VALUE'),
           TIMESERIESON(lotId)) AS time_col, lotId, is_occupied
    FROM parking_data
    WHERE event_time >= 1633078800000 AND  event_time <= 1633089600000
    ORDER BY 1
    LIMIT 100)
GROUP BY 1
LIMIT 100
```

#### Workflow

The raw data will be transformed as following at first:

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:00:00.000 | 1            |
| P2    | 2021-10-01 09:00:00.000 | 1            |
| P1    | 2021-10-01 09:30:00.000 | 0            |
| P1    | 2021-10-01 09:30:00.000 | 1            |
| P3    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:00:00.000 | 0            |
| P2    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P3    | 2021-10-01 11:00:00.000 | 0            |
| P1    | 2021-10-01 11:30:00.000 | 0            |

The transformed data will be gap filled as follows:

| lotId | event\_time             | is\_occupied |
| ----- | ----------------------- | ------------ |
| P1    | 2021-10-01 09:00:00.000 | 1            |
| P2    | 2021-10-01 09:00:00.000 | 1            |
| P3    | 2021-10-01 09:00:00.000 | 0            |
| P1    | 2021-10-01 09:30:00.000 | 0            |
| P1    | 2021-10-01 09:30:00.000 | 1            |
| P2    | 2021-10-01 09:30:00.000 | 1            |
| P3    | 2021-10-01 09:30:00.000 | 0            |
| P1    | 2021-10-01 10:00:00.000 | 1            |
| P3    | 2021-10-01 10:00:00.000 | 1            |
| P2    | 2021-10-01 10:00:00.000 | 0            |
| P2    | 2021-10-01 10:00:00.000 | 1            |
| P1    | 2021-10-01 10:30:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P3    | 2021-10-01 10:30:00.000 | 1            |
| P2    | 2021-10-01 10:30:00.000 | 0            |
| P1    | 2021-10-01 11:00:00.000 | 1            |
| P2    | 2021-10-01 11:00:00.000 | 0            |
| P3    | 2021-10-01 11:00:00.000 | 0            |
| P1    | 2021-10-01 11:30:00.000 | 0            |
| P2    | 2021-10-01 11:30:00.000 | 0            |
| P3    | 2021-10-01 11:30:00.000 | 0            |

The aggregation will generate the following table:

| timeBucket              | totalNumOfOccuppiedSlots |
| ----------------------- | ------------------------ |
| 2021-10-01 09:00:00.000 | 2                        |
| 2021-10-01 09:30:00.000 | 2                        |
| 2021-10-01 10:00:00.000 | 3                        |
| 2021-10-01 10:30:00.000 | 2                        |
| 2021-10-01 11:00:00.000 | 1                        |
| 2021-10-01 11:30:00.000 | 0                        |
