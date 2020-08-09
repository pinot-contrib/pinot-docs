---
description: Pinot Client for Golang
---

# Golang

Pinot also provides [a native go client](https://github.com/fx19880617/pinot-client-go) to query database directly from go application. 

### Installation

Please follow this [Pinot Quickstart](https://apache-pinot.gitbook.io/apache-pinot-cookbook/getting-started/running-pinot-locally) link to install and start Pinot batch QuickStart locally.

```text
bin/quick-start-batch.sh
```

Check out Client library Github Repo

```text
git clone git@github.com:fx19880617/pinot-client-go.git
cd pinot-client-go
```

Build and run the example application to query from Pinot Batch Quickstart

```text
go build ./examples/batch-quickstart
./batch-quickstart
```

### Usage

#### Create a Pinot Connection

Pinot client could be initialized through:

#### 1. Zookeeper Path.

```text
pinotClient := pinot.NewFromZookeeper([]string{"localhost:2123"}, "", "QuickStartCluster")
```

#### 2. A list of broker addresses.

```text
pinotClient := pinot.NewFromBrokerList([]string{"localhost:8000"})
```

#### 3. ClientConfig

```text
pinotClient := pinot.NewWithConfig(&pinot.ClientConfig{
	ZkConfig: &pinot.ZookeeperConfig{
		ZookeeperPath:     zkPath,
		PathPrefix:        strings.Join([]string{zkPathPrefix, pinotCluster}, "/"),
		SessionTimeoutSec: defaultZkSessionTimeoutSec,
	},
    ExtraHTTPHeader: map[string]string{
        "extra-header":"value",
    },
})
```

### Query Pinot

Please see this [example](https://github.com/fx19880617/pinot-client-go/blob/master/examples/batch-quickstart/main.go) for your reference.

Code snippet:

```text
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

### Response Format

Query Response is defined as the struct of following:

```text
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

Note that `AggregationResults` and `SelectionResults` are holders for PQL queries.

Meanwhile `ResultTable` is the holder for SQL queries. `ResultTable` is defined as:

```text
// ResultTable is a ResultTable
type ResultTable struct {
	DataSchema RespSchema      `json:"dataSchema"`
	Rows       [][]interface{} `json:"rows"`
}
```

`RespSchema` is defined as:

```text
// RespSchema is response schema
type RespSchema struct {
	ColumnDataTypes []string `json:"columnDataTypes"`
	ColumnNames     []string `json:"columnNames"`
}
```

There are multiple functions defined for `ResultTable`, like:

```text
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

Sample Usage is [here](https://github.com/fx19880617/pinot-client-go/blob/master/examples/batch-quickstart/main.go#L58)

```text
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

