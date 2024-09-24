# FST index

The FST index supports regex queries on text. Decreases on-disk index by 4-6 times.&#x20;

* Only supports regex queries
* Only supported on stored or completed Pinot segments (no consuming segments).
* Only supported on dictionary-encoded columns.
* Works better for prefix queries&#x20;

For more information on the FST construction and code, see [Lucene documentation](https://lucene.apache.org/core/9\_10\_0/core/org/apache/lucene/util/fst/FST.html).

## Enable the FST index

To enable the FST index on a dictionary-encoded column, include the following configuration:

```javascript
"fieldConfigList":[
{
"name":"text_col_1",
"encodingType":"DICTIONARY",
"indexType":"FST"
}
]
```

The FST index generates one FST index file (`.lucene.fst)`. If the inverted index is enabled, this is further able to take advantage of that.

For more information about enabling the FST index, see ways to [enable indexes](./#enabling-indexes).

\
