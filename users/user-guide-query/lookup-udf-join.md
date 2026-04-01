---
description: >-
  For more information about using JOINs with the multi-stage query engine, see
  JOINs.
---

# Lookup UDF Join

{% hint style="info" %}
Lookup UDF Join is **only supported with the single-stage query engine (v1)**. Lookup joins can be executed using [query hints](multi-stage-query/join-strategies/lookup-join-strategy.md) in the multi-stage query engine. For more information about using JOINs with the multi-stage query engine, see [JOINs](joins.md).
{% endhint %}

Lookup UDF is used to get dimension data via primary key from a dimension table allowing a decoration join functionality. Lookup UDF can only be used with [a dimension table](../../manage-data/data-import/batch-ingestion/dim-table.md) in Pinot.

## Syntax

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

* `dimTable` Name of the dim table to perform the lookup on.
* `dimColToLookUp` The column name of the dim table to be retrieved to decorate our result.
* `dimJoinKey` The column name on which we want to perform the lookup i.e. the join column name for dim table.
* `factJoinKey` The column name on which we want to perform the lookup against e.g. the join column name for fact table

Noted that:

1. all the dim-table-related expressions are expressed as literal strings, this is the LOOKUP UDF syntax limitation: we cannot express column identifier which doesn't exist in the query's main table, which is the `factTable` table.
2. the syntax definition of `[ '''dimJoinKey''', factJoinKey ]*` indicates that if there are multiple dim partition columns, there should be multiple join key pair expressed.

## Examples

Here are some of the examples

### Single-partition-key-column Example

Consider the table `baseballStats`

<table>
  <thead>
    <tr>
      <th>Column</th>
      <th>Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>playerID</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>yearID</td>
      <td>INT</td>
    </tr>
    <tr>
      <td>teamID</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>league</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>playerName</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>playerStint</td>
      <td>INT</td>
    </tr>
    <tr>
      <td>numberOfGames</td>
      <td>INT</td>
    </tr>
    <tr>
      <td>numberOfGamesAsBatter</td>
      <td>INT</td>
    </tr>
    <tr>
      <td>AtBatting</td>
      <td>INT</td>
    </tr>
    <tr>
      <td>runs</td>
      <td>INT</td>
    </tr>
  </tbody>
</table>

and dim table `dimBaseballTeams`

<table>
  <thead>
    <tr>
      <th>Column</th>
      <th>Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>teamID</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>teamName</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>teamAddress</td>
      <td>STRING</td>
    </tr>
  </tbody>
</table>

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

<table>
  <thead>
    <tr>
      <th>teamID</th>
      <th>nameFromLocal</th>
      <th>nameFromLookup</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>ANA</td>
      <td>Anaheim Angels</td>
      <td>Anaheim Angels</td>
    </tr>
    <tr>
      <td>ARI</td>
      <td>Arizona Diamondbacks</td>
      <td>Arizona Diamondbacks</td>
    </tr>
    <tr>
      <td>ATL</td>
      <td>Atlanta Braves</td>
      <td>Atlanta Braves</td>
    </tr>
    <tr>
      <td>BAL</td>
      <td>Baltimore Orioles (original- 1901–1902 current- since 1954)</td>
      <td>Baltimore Orioles (original- 1901–1902 current- since 1954)</td>
    </tr>
  </tbody>
</table>

### Complex-partition-key-columns Example

Consider a single dimension table with schema:

BILLING SCHEMA

<table>
  <thead>
    <tr>
      <th>Column</th>
      <th>Type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>customerId</td>
      <td>INT</td>
    </tr>
    <tr>
      <td>creditHistory</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>firstName</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>lastName</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>isCarOwner</td>
      <td>BOOLEAN</td>
    </tr>
    <tr>
      <td>city</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>maritalStatus</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>buildingType</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>missedPayment</td>
      <td>STRING</td>
    </tr>
    <tr>
      <td>billingMonth</td>
      <td>STRING</td>
    </tr>
  </tbody>
</table>

#### Self LOOKUP example

```
select 
  customerId,
  missedPayment, 
  LOOKUP('billing', 'city', 'customerId', customerId, 'creditHistory', creditHistory) AS lookedupCity 
from billing
```

<table>
  <thead>
    <tr>
      <th>customerId</th>
      <th>missedPayment</th>
      <th>lookedupCity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>341</td>
      <td>Paid</td>
      <td>Palo Alto</td>
    </tr>
    <tr>
      <td>374</td>
      <td>Paid</td>
      <td>Mountain View</td>
    </tr>
    <tr>
      <td>398</td>
      <td>Paid</td>
      <td>Palo Alto</td>
    </tr>
    <tr>
      <td>427</td>
      <td>Paid</td>
      <td>Cupertino</td>
    </tr>
    <tr>
      <td>435</td>
      <td>Paid</td>
      <td>Cupertino</td>
    </tr>
  </tbody>
</table>

## Usage FAQ

* The data return type of the UDF will be that of the `dimColToLookUp` column type.
* when multiple primary key columns are used for the dimension table (e.g. composite primary key), ensure that the order of keys appearing in the lookup() UDF is the same as the order defined in the `primaryKeyColumns` from the dimension table schema.
