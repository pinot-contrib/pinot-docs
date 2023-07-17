# Lookup UDF Join

Lookup UDF is used to get dimension data via primary key from a dimension table allowing a decoration join functionality. Lookup UDF can only be used with [a dimension table](../../basics/data-import/batch-ingestion/dim-table.md) in Pinot.&#x20;

## Syntax&#x20;

The UDF function syntax is listed as below:

```
lookupUDFSpec:
    LOOKUP
    '('
    '''dimTable'''
    '''dimColToLookup'''
    [ '''dimJoinKey''', factJoinKey ]*
    ')'
```

* `dimTable` Name of the dim table to perform the lookup on.&#x20;
* `dimColToLookUp` The column name of the dim table to be retrieved to decorate our result.
* `dimJoinKey` The column name on which we want to perform the lookup i.e. the join column name for dim table.&#x20;
* `factJoinKey` The column name on which we want to perform the lookup against e.g. the join column name for fact table

Noted that:

1. all the dim-table-related expressions are expressed as literal strings, this is the LOOKUP UDF syntax limitation: we cannot express column identifier which doesn't exist in the query's main table, which is the `factTable` table.
2. the syntax definition of `[ '''dimJoinKey''', factJoinKey ]*` indicates that if there are multiple dim partition columns, there should be multiple join key pair expressed.

## Examples

Here are some of the examples

### Single-partition-key-column Example

Consider the table `baseballStats`&#x20;

| Column                | Type   |
| --------------------- | ------ |
| playerID              | STRING |
| yearID                | INT    |
| teamID                | STRING |
| league                | STRING |
| playerName            | STRING |
| playerStint           | INT    |
| numberOfGames         | INT    |
| numberOfGamesAsBatter | INT    |
| AtBatting             | INT    |
| runs                  | INT    |

and dim table `dimBaseballTeams`

| Column      | Type   |
| ----------- | ------ |
| teamID      | STRING |
| teamName    | STRING |
| teamAddress | STRING |

several acceptable queries are:

#### Dim-Fact LOOKUP example

<pre><code><strong>SELECT 
</strong>  playerName, 
  teamID, 
  LOOKUP('dimBaseballTeams', 'teamName', 'teamID', teamID) AS teamName, 
  LOOKUP('dimBaseballTeams', 'teamAddress', 'teamID', teamID) AS teamAddress
FROM baseballStats 
</code></pre>

<table><thead><tr><th width="141">playerName</th><th width="94.33333333333331">teamID</th><th>teamName</th><th>teamAddress</th></tr></thead><tbody><tr><td>David Allan</td><td>BOS</td><td>Boston Red Caps/Beaneaters (from 1876–1900) or Boston Red Sox (since 1953)</td><td>4 Jersey Street, Boston, MA</td></tr><tr><td>David Allan</td><td>CHA</td><td>null</td><td>null</td></tr><tr><td>David Allan</td><td>SEA</td><td>Seattle Mariners (since 1977) or Seattle Pilots (1969)</td><td>1250 First Avenue South, Seattle, WA</td></tr><tr><td>David Allan</td><td>SEA</td><td>Seattle Mariners (since 1977) or Seattle Pilots (1969)</td><td>1250 First Avenue South, Seattle, WA</td></tr></tbody></table>

#### Self LOOKUP example

```
SELECT 
  teamID, 
  teamName AS nameFromLocal,
  LOOKUP('dimBaseballTeams', 'teamName', 'teamID', teamID) AS nameFromLookup
FROM dimBaseballTeams
```

| teamID | nameFromLocal                                               | nameFromLookup                                              |
| ------ | ----------------------------------------------------------- | ----------------------------------------------------------- |
| ANA    | Anaheim Angels                                              | Anaheim Angels                                              |
| ARI    | Arizona Diamondbacks                                        | Arizona Diamondbacks                                        |
| ATL    | Atlanta Braves                                              | Atlanta Braves                                              |
| BAL    | Baltimore Orioles (original- 1901–1902 current- since 1954) | Baltimore Orioles (original- 1901–1902 current- since 1954) |

### Complex-partition-key-columns Example

Consider a single dimension table with schema:

BILLING SCHEMA

| Column        | Type    |
| ------------- | ------- |
| customerId    | INT     |
| creditHistory | STRING  |
| firstName     | STRING  |
| lastName      | STRING  |
| isCarOwner    | BOOLEAN |
| city          | STRING  |
| maritalStatus | STRING  |
| buildingType  | STRING  |
| missedPayment | STRING  |
| billingMonth  | STRING  |

#### Self LOOKUP example

```
select 
  customerId,
  missedPayment, 
  LOOKUP('billing', 'city', 'customerId', customerId, 'creditHistory', creditHistory) AS lookedupCity 
from billing
```

| customerId | missedPayment | lookedupCity  |
| ---------- | ------------- | ------------- |
| 341        | Paid          | Palo Alto     |
| 374        | Paid          | Mountain View |
| 398        | Paid          | Palo Alto     |
| 427        | Paid          | Cupertino     |
| 435        | Paid          | Cupertino     |



## Usage FAQ

* The data return type of the UDF will be that of the `dimColToLookUp` column type.&#x20;
* when multiple primary key columns are used for the dimension table (e.g. composite primary key), ensure that the order of keys appearing in the lookup() UDF is the same as the order defined in the `primaryKeyColumns` from the dimension table schema.
