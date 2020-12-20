# Supported Aggregations

Pinot provides support for aggregations using GROUP BY. You can use the following functions to get the aggregated value.

<table>
  <thead>
    <tr>
      <th style="text-align:left">Function</th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><b>COUNT</b>
      </td>
      <td style="text-align:left">Get the count of rows in a group</td>
      <td style="text-align:left"><code>COUNT(*)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MIN</b>
      </td>
      <td style="text-align:left">Get the minimum value in a group</td>
      <td style="text-align:left"><code>MIN(playerScore)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MAX</b>
      </td>
      <td style="text-align:left">Get the maximum value in a group</td>
      <td style="text-align:left"><code>MAX(playerScore)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>SUM</b>
      </td>
      <td style="text-align:left">Get the sum of values in a group</td>
      <td style="text-align:left"><code>SUM(playerScore)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>AVG</b>
      </td>
      <td style="text-align:left">Get the average of the values in a group</td>
      <td style="text-align:left"><code>AVG(playerScore)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MINMAXRANGE</b>
      </td>
      <td style="text-align:left">Returns the min and max value in a group</td>
      <td style="text-align:left"><code>MINMAXRANGE(playerScore)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>PERCENTILE(column, N)</b>
      </td>
      <td style="text-align:left">Returns the Nth percentile of the group where N is a decimal number between
        0 and 100 inclusive</td>
      <td style="text-align:left"><code>PERCENTILE(playerScore, 50), PERCENTILE(playerScore, 99.9)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>PERCENTILEEST(column, N)</b>
      </td>
      <td style="text-align:left">Returns the Nth percentile of the group using <a href="https://github.com/airlift/airlift/blob/master/stats/src/main/java/io/airlift/stats/QuantileDigest.java">Quantile Digest</a> algorithm</td>
      <td
      style="text-align:left"><code>PERCENTILEEST(playerScore, 50), PERCENTILEEST(playerScore, 99.9)</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>PercentileTDigest(column, N)</b>
      </td>
      <td style="text-align:left">Returns the Nth percentile of the group using <a href="https://raw.githubusercontent.com/tdunning/t-digest/master/docs/t-digest-paper/histo.pdf">T-digest algorithm</a>
      </td>
      <td style="text-align:left"><code>PERCENTILETDIGEST(playerScore, 50), PERCENTILETDIGEST(playerScore, 99.9)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCT</b>
      </td>
      <td style="text-align:left">Returns the distinct row values in a group</td>
      <td style="text-align:left"><code>DISTINCT(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCTCOUNT</b>
      </td>
      <td style="text-align:left">Returns the count of distinct row values in a group</td>
      <td style="text-align:left"><code>DISTINCTCOUNT(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCTCOUNTHLL</b>
      </td>
      <td style="text-align:left">Returns an approximate distinct count using HyperLogLog in a group</td>
      <td
      style="text-align:left"><code>DISTINCTCOUNTHLL(playerName)</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCTCOUNTRAWHLL</b>
      </td>
      <td style="text-align:left">Returns HLL response serialized as string. The serialized HLL can be converted
        back into an HLL and then aggregated with other HLLs. A common use case
        may be to merge HLL responses from different Pinot tables, or to allow
        aggregation after client-side batching.</td>
      <td style="text-align:left">
        <p><code>DISTINCTCOUNTRAWHLL(playerName)</code>
        </p>
        <p>&lt;code&gt;&lt;/code&gt;</p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>FASTHLL (Deprecated)</b>
      </td>
      <td style="text-align:left"><b>WARN</b>: will be deprecated soon. FASTHLL stores serialized HyperLogLog
        in String format, which performs worse than DISTINCTCOUNTHLL, which supports
        serialized HyperLogLog in BYTES (byte array) format</td>
      <td style="text-align:left"><code>FASTHLL(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DistinctCountThetaSketch</b>
      </td>
      <td style="text-align:left">See <a href="how-to-handle-unique-counting.md">Cardinality Estimation</a>
      </td>
      <td style="text-align:left"></td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DistinctCountRawThetaSketch</b>
      </td>
      <td style="text-align:left">See <a href="how-to-handle-unique-counting.md">Cardinality Estimation</a>
      </td>
      <td style="text-align:left"></td>
    </tr>
  </tbody>
</table>

## Multi-value column functions

The following aggregation functions can be used for multi-value columns

<table>
  <thead>
    <tr>
      <th style="text-align:left"><b>Function</b>
      </th>
      <th style="text-align:left">Description</th>
      <th style="text-align:left">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align:left"><b>COUNTMV</b>
      </td>
      <td style="text-align:left">Get the count of rows in a group</td>
      <td style="text-align:left"><code>COUNTMV(playerName)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MINMV</b>
      </td>
      <td style="text-align:left">Get the minimum value in a group</td>
      <td style="text-align:left"><code>MINMV(playerScores)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MAXMV</b>
      </td>
      <td style="text-align:left">Get the maximum value in a group</td>
      <td style="text-align:left"><code>MAXMV(playerScores)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>SUMMV</b>
      </td>
      <td style="text-align:left">Get the sum of values in a group</td>
      <td style="text-align:left"><code>SUMMV(playerScores)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>AVGMV</b>
      </td>
      <td style="text-align:left">Get the avg of values in a group</td>
      <td style="text-align:left"><code>AVGMV(playerScores)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>MINMAXRANGEMV</b>
      </td>
      <td style="text-align:left">Returns the min and max value in a group</td>
      <td style="text-align:left"><code>MINMAXRANGEMV(playerScores)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>PERCENTILEMV(column, N)</b>
      </td>
      <td style="text-align:left">Returns the Nth percentile of the group where N is a decimal number between
        0 and 100 inclusive</td>
      <td style="text-align:left">
        <p><code>PERCENTILEMV(playerScores, 50),</code>
        </p>
        <p><code>PERCENTILEMV(playerScores, 99.9)</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>PERCENTILEESTMV(column, N)</b>
      </td>
      <td style="text-align:left">Returns the Nth percentile of the group using <a href="https://github.com/airlift/airlift/blob/master/stats/src/main/java/io/airlift/stats/QuantileDigest.java">Quantile Digest</a> algorithm</td>
      <td
      style="text-align:left">
        <p><code>PERCENTILEESTMV(playerScores, 50),</code>
        </p>
        <p><code>PERCENTILEESTMV(playerScores, 99.9)</code>
        </p>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>PercentileTDigestMV(column, N)</b>
      </td>
      <td style="text-align:left">Returns the Nth percentile of the group using <a href="https://raw.githubusercontent.com/tdunning/t-digest/master/docs/t-digest-paper/histo.pdf">T-digest algorithm</a>
      </td>
      <td style="text-align:left">
        <p><code>PERCENTILETDIGESTMV(playerScores, 50),</code>
        </p>
        <p><code>PERCENTILETDIGESTMV(playerScores, 99.9),</code>
        </p>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCTCOUNTMV</b>
      </td>
      <td style="text-align:left">Returns the count of distinct row values in a group</td>
      <td style="text-align:left"><code>DISTINCTCOUNTMV(playerNames)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCTCOUNTHLLMV</b>
      </td>
      <td style="text-align:left">Returns an approximate distinct count using HyperLogLog in a group</td>
      <td
      style="text-align:left"><code>DISTINCTCOUNTHLLMV(playerNames)</code>
        </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>DISTINCTCOUNTRAWHLLMV</b>
      </td>
      <td style="text-align:left">Returns HLL response serialized as string. The serialized HLL can be converted
        back into an HLL and then aggregated with other HLLs. A common use case
        may be to merge HLL responses from different Pinot tables, or to allow
        aggregation after client-side batching.</td>
      <td style="text-align:left"><code>DISTINCTCOUNTRAWHLLMV(playerNames)</code>
      </td>
    </tr>
    <tr>
      <td style="text-align:left"><b>FASTHLLMV (Deprecated)</b>
      </td>
      <td style="text-align:left">stores serialized HyperLogLog in String format, which performs worse than
        DISTINCTCOUNTHLL, which supports serialized HyperLogLog in BYTES (byte
        array) format</td>
      <td style="text-align:left"><code>FASTHLLMV(playerNames)</code>
      </td>
    </tr>
  </tbody>
</table>

\`\`

