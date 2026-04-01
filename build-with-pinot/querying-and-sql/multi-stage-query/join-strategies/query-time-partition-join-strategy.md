# Query time partition join strategy

Although in the general case both tables cannot be partitioned without breaking the join semantics, there are some cases where it is possible. For example, if the join condition is an equality between two columns like `ON A.col2 = B.col3`, it is possible to assign a partition function to each table that guarantees that `partition(A.col2) <> partition(B.col3) => A.col2 <> B.col3`. The most common case is to use a hash function as a partition function. The corollary of this property is that rows that end up in different servers after shuffling did not need to be joined.

![](../../../../.gitbook/assets/image (13).png)

*Dotted arrows mean shuffle while solid arrows mean in-server transfer*

This technique is used by Pinot whenever it can infer it is possible, like when the join condition is an equality between two columns or a conjunction of equalities, for example:

```sql
SELECT A.col1, B.col2 
FROM A
JOIN B
ON A.col2 = B.col3 AND Ab.col5 = B.col2
```

When this technique is used, the number of rows that are shuffled is `count(A) + count(B)`.
