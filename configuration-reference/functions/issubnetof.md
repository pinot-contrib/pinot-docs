---
description: This section contains reference documentation for the isSubnetOf function.
---

# isSubnetOf

Takes 2 arguments of type STRING. The first argument is an `ipPrefix`, and the second argument is a single `ipAddress`. This function handles both IPv4 and IPv6 arguments.

Returns a boolean value checking if `ipAddress` is in the subnet of `ipPrefix`

## Signatures

`isSubnetOf(ipPrefix, ipAddress) -> boolean`

## Usage Examples

See the following sample queries where `isSubnetOf` is used in different parts of the query.

<pre class="language-sql"><code class="lang-sql">SELECT isSubnetOf('192.168.0.1/24', '192.168.0.225') 
<strong>AS result
</strong><strong>FROM myTable;
</strong><strong>---> returns true
</strong><strong>
</strong>SELECT isSubnetOf('1.2.3.128/26', '1.2.5.1') 
AS result
FROM myTable;
---> returns false</code></pre>

```sql
SELECT isSubnetOf('2001:4800:7825:103::/64', '2001:4800:7825:103::2050')
AS result
FROM myTable;
---> returns true

SELECT isSubnetOf('7890:db8:113::8a2e:370:7334/127', '7890:db8:113::8a2e:370:7336') 
AS result
FROM myTable;
---> returns false
```

<pre class="language-sql"><code class="lang-sql"><strong>SELECT count(*) 
</strong><strong>FROM myTable 
</strong><strong>WHERE isSubnetOf('192.168.0.1/24', ipAddressCol);
</strong><strong>
</strong>SELECT count(*) 
FROM myTable 
WHERE isSubnetOf('192.168.0.1/24', ipAddressCol) 
OR isSubnetOf(ipPrefixCol, '7890:db8:113::8a2e:370:7336');</code></pre>

<pre class="language-sql"><code class="lang-sql">SELECT 
<strong>    CASE 
</strong>        WHEN isSubnetOf('105.25.245.115/27', srcIPAddress) THEN 'case1' 
        WHEN isSubnetOf('105.25.245.115/27', dstIPAddress) THEN 'case2'
        ELSE 'case3' 
    END AS differentFlow
FROM myTable;</code></pre>
