# IP Address Functions

Pinot provides functions for working with IP addresses and subnets. These functions support both IPv4 and IPv6 addresses and use CIDR notation for subnet prefixes (e.g., `192.168.0.0/16`, `2001:db8::/32`).

## isSubnetOf

```sql
isSubnetOf(ipPrefix, ipAddress)
```

Returns `true` if the given IP address belongs to the specified subnet prefix. The first argument must be a CIDR prefix (e.g., `'192.168.1.0/24'`) and the second must be a plain IP address without a prefix.

```sql
SELECT isSubnetOf('192.168.1.0/24', clientIp) AS is_internal
FROM accessLog
WHERE isSubnetOf('10.0.0.0/8', clientIp)
-- Filters rows where clientIp is in the 10.0.0.0/8 private range
```

## ipPrefix

```sql
ipPrefix(ipAddress, prefixBits)
```

Returns the CIDR prefix for the given IP address and prefix length in bits. The IP address must not already contain a prefix. The prefix length must be between 0 and 32 for IPv4, or 0 and 128 for IPv6.

```sql
SELECT ipPrefix(clientIp, 24) AS subnet
FROM accessLog
LIMIT 5
-- For clientIp='192.168.1.100', returns '192.168.1.0/24'
```

## ipSubnetMin

```sql
ipSubnetMin(ipPrefix)
```

Returns the lowest (first) IP address in the given subnet.

```sql
SELECT ipSubnetMin('192.168.1.0/24') AS range_start
FROM myTable
LIMIT 1
-- Returns '192.168.1.0'
```

## ipSubnetMax

```sql
ipSubnetMax(ipPrefix)
```

Returns the highest (last) IP address in the given subnet.

```sql
SELECT ipSubnetMax('192.168.1.0/24') AS range_end
FROM myTable
LIMIT 1
-- Returns '192.168.1.255'
```
