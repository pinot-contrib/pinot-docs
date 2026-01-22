# Random + broadcast join strategy

In order to execute joins, Pinot creates virtual partitions at query time. The more general way to do so is to assign a random partition to each row of the table. Each partition is then assigned to a server, and the join is executed in a distributed manner.

This partition technique can be applied to one of the tables in the join, but not to both. Otherwise, the result wouldn't be correct as some of the pairs of rows would be lost and never joined. Therefore what Pinot does is partition one of the tables and broadcast the other one.

<figure><img src="../../../../.gitbook/assets/image (7) (1).png" alt="" width="563"><figcaption><p>Dotted arrows mean shuffle while solid arrows mean in-server transfer</p></figcaption></figure>

This technique is used by Pinot when no other technique (like semantic virtual partition or colocated joins) can be used. For example, on queries like:

```sql
SELECT A.col1, B.col2
FROM A
JOIN B
ON A.col2 > B.col3 or A.col4 < B.col4
```

As always, Pinot assumes that the right table is the smallest, so that is the one that is broadcasted. When this technique is used, the number of rows that are shuffled can be upper-bounded by `count(A) + count(B) * number of servers` .

\
