# Null Value Support

### Need for special NULL value handling

By default, Pinot transforms null values coming from the data source to a default value determined by the type of the corresponding column (or as specified in the schema). Eg: for INT column, the default will be 0 and for STRING column, the default is `"null"`. This transformation is necessary to ensure all the indices can be built correctly during segment creation. However, we're now unable to keep track of the null values in the Pinot table and hence cannot support queries such as:

```sql
select count(*) from my_table where column IS NOT NULL
```

There is a workaround by matching with default values in the filter predicate. However, this is error prone since oftentimes it's difficult to distinguish valid values from the default null values. Therefore, we added first class NULL value support in Pinot for overcoming this limitation. As of today, the latest version supports **NULL filter predicates** only. Generic support for NULL handling in query execution is in progress (eg: within aggregation functions such as `count` or `sum`).

### High Level Architecture

To turn on `NULL` handling, simply enable the boolean flag in the table index config called as `nullHandlingEnabled` (see [tableIndexConfig section](https://docs.pinot.apache.org/configuration-reference/table#tableindexconfig-1)). Note - this will cause Pinot to use additional memory and disk space per segment. The details are as follows:

#### **Ingestion Phase**

During data ingestion (either real-time/offline) each`GenericRow` object derived from the original data source record keeps track of all the column names containing null values. This is done as part of the `NullValueTransformer`. For each such column, the segment creation logic updates a NULL value vector (implemented by a roaring bitmap) with the corresponding document ID. Effectively, at the end of the segment creation process we get a per column NULL value vector which can give us the set of document IDs containing null values for that column. This per column vector is then exposed through the `DataSource` interface for use in query execution.

#### Query Phase

During Query execution, if the query includes a `IS NULL` or `IS NOT NULL` predicate as shown above, we fetch the NULL value vector for the corresponding column within `FilterPlanNode` and retrieve the corresponding bitmap which represents all document IDs containing NULL values for that column. This bitmap is then used to create a `BitmapBasedFilterOperator`which does the actual filtering operation.

### &#x20;
