---
description: Pinot Client for Golang
---

# Golang

Pinot provides [a native Go client](https://github.com/startreedata/pinot-client-go) to query the database directly from Go application.&#x20;

### Install

1. Follow this [Pinot quickstart](https://apache-pinot.gitbook.io/apache-pinot-cookbook/getting-started/running-pinot-locally) link to install and start Pinot locally.

```
bin/quick-start-batch.sh
```

2. Check out the [client library GitHub repository](https://github.com/startreedata/pinot-client-go/tree/master).

```
git clone git@github.com:startreedata/pinot-client-go.git
cd pinot-client-go
```

3. Build and run the example application to query from the [Pinot batch quickstart](https://docs.pinot.apache.org/basics/getting-started/running-pinot-locally).

```
go build ./examples/batch-quickstart
./batch-quickstart
```

### Use the Golang client

#### Create a Pinot connection

Initialize the Pinot client using one of the methods below.

#### Zookeeper Path

```
pinotClient := pinot.NewFromZookeeper([]string{"localhost:2123"}, "", "QuickStartCluster")
```

#### List of broker addresses

```
pinotClient := pinot.NewFromBrokerList([]string{"localhost:8000"})
```

#### ClientConfig

The Go client repository contains an [example](https://github.com/startreedata/pinot-client-go/blob/master/examples/pinot-client-withconfig/main.go) script.

Note: You need not configure `“content-type”` as a header in `ExtraHTTPHeader`.

```
pinotClient := pinot.NewWithConfig(&pinot.ClientConfig{
	ZkConfig: &pinot.ZookeeperConfig{
		ZookeeperPath:     zkPath,
		PathPrefix:        strings.Join([]string{zkPathPrefix, pinotCluster}, "/"),
		SessionTimeoutSec: defaultZkSessionTimeoutSec,
	},
    ExtraHTTPHeader: map[string]string{
        "extra-header": "value",
    },
})
```

#### ClientConfig with HTTP client

If you require a specialized HTTP client, you have the option to create your own HTTP client and utilize the `NewWithConfigAndClient` function to establish a Pinot client that can accommodate a custom HTTP client.

The Go client repository contains an [example](https://github.com/startreedata/pinot-client-go/blob/master/examples/pinot-client-with-config-and-http-client/main.go) script.

### Query Pinot

The Go client repository contains an [example](https://github.com/startreedata/pinot-client-go/blob/master/examples/batch-quickstart/main.go) script.&#x20;

Code snippet:

```
pinotClient, err := pinot.NewFromZookeeper([]string{"localhost:2123"}, "", "QuickStartCluster")
if err != nil {
    log.Error(err)
}
brokerResp, err := pinotClient.ExecuteSQL("baseballStats", "select count(*) as cnt, sum(homeRuns) as sum_homeRuns from baseballStats group by teamID limit 10")
if err != nil {
    log.Error(err)
}
log.Infof("Query Stats: response time - %d ms, scanned docs - %d, total docs - %d", brokerResp.TimeUsedMs, brokerResp.NumDocsScanned, brokerResp.TotalDocs)
```

### Response format

The query response has the following format:

```
type BrokerResponse struct {
	AggregationResults          []*AggregationResult `json:"aggregationResults,omitempty"`
	SelectionResults            *SelectionResults    `json:"SelectionResults,omitempty"`
	ResultTable                 *ResultTable         `json:"resultTable,omitempty"`
	Exceptions                  []Exception          `json:"exceptions"`
	TraceInfo                   map[string]string    `json:"traceInfo,omitempty"`
	NumServersQueried           int                  `json:"numServersQueried"`
	NumServersResponded         int                  `json:"numServersResponded"`
	NumSegmentsQueried          int                  `json:"numSegmentsQueried"`
	NumSegmentsProcessed        int                  `json:"numSegmentsProcessed"`
	NumSegmentsMatched          int                  `json:"numSegmentsMatched"`
	NumConsumingSegmentsQueried int                  `json:"numConsumingSegmentsQueried"`
	NumDocsScanned              int64                `json:"numDocsScanned"`
	NumEntriesScannedInFilter   int64                `json:"numEntriesScannedInFilter"`
	NumEntriesScannedPostFilter int64                `json:"numEntriesScannedPostFilter"`
	NumGroupsLimitReached       bool                 `json:"numGroupsLimitReached"`
	TotalDocs                   int64                `json:"totalDocs"`
	TimeUsedMs                  int                  `json:"timeUsedMs"`
	MinConsumingFreshnessTimeMs int64                `json:"minConsumingFreshnessTimeMs"`
}
```

Note that `AggregationResults` and `SelectionResults` are holders for Pinot query language (PQL) queries.

Meanwhile, `ResultTable` is the holder for SQL queries. `ResultTable` is defined as:

```
// ResultTable is a ResultTable
type ResultTable struct {
	DataSchema RespSchema      `json:"dataSchema"`
	Rows       [][]interface{} `json:"rows"`
}
```

`RespSchema` is defined as:

```
// RespSchema is response schema
type RespSchema struct {
	ColumnDataTypes []string `json:"columnDataTypes"`
	ColumnNames     []string `json:"columnNames"`
}
```

There are multiple functions defined for `ResultTable`, such as the following:

```
func (r ResultTable) GetRowCount() int
func (r ResultTable) GetColumnCount() int
func (r ResultTable) GetColumnName(columnIndex int) string
func (r ResultTable) GetColumnDataType(columnIndex int) string
func (r ResultTable) Get(rowIndex int, columnIndex int) interface{}
func (r ResultTable) GetString(rowIndex int, columnIndex int) string
func (r ResultTable) GetInt(rowIndex int, columnIndex int) int
func (r ResultTable) GetLong(rowIndex int, columnIndex int) int64
func (r ResultTable) GetFloat(rowIndex int, columnIndex int) float32
func (r ResultTable) GetDouble(rowIndex int, columnIndex int) float64
```

See an example of a function in use [here](https://github.com/fx19880617/pinot-client-go/blob/master/examples/batch-quickstart/main.go#L58) and below:

```
// Print Response Schema
for c := 0; c < brokerResp.ResultTable.GetColumnCount(); c++ {
  fmt.Printf("%s(%s)\t", brokerResp.ResultTable.GetColumnName(c), brokerResp.ResultTable.GetColumnDataType(c))
}
fmt.Println()

// Print Row Table
for r := 0; r < brokerResp.ResultTable.GetRowCount(); r++ {
  for c := 0; c < brokerResp.ResultTable.GetColumnCount(); c++ {
    fmt.Printf("%v\t", brokerResp.ResultTable.Get(r, c))
  }
  fmt.Println()
}
```
