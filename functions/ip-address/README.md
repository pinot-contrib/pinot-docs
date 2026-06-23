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

## isIPv4String

```sql
isIPv4String(ipString)
```

Returns `true` when the input is a valid IPv4 address string without a CIDR prefix.

```sql
SELECT isIPv4String('192.168.1.1') AS valid_v4
-- Returns true
```

## isIPv6String

```sql
isIPv6String(ipString)
```

Returns `true` when the input is a valid IPv6 address string without a CIDR prefix.

```sql
SELECT isIPv6String('2001:db8::1') AS valid_v6
-- Returns true
```

## isPrivateIp / is_private_ip

```sql
isPrivateIp(ipString)
```

Returns `true` when the input is a plain IPv4 or IPv6 address without a CIDR prefix and it falls into one of these ranges:

- RFC 1918 IPv4: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- IPv4 loopback: `127.0.0.0/8`
- IPv4 link-local: `169.254.0.0/16`
- IPv6 loopback: `::1`
- IPv6 link-local: `fe80::/10`
- IPv6 ULA: `fc00::/7`

```sql
SELECT isPrivateIp(clientIp) AS is_private
FROM accessLog
WHERE isPrivateIp(clientIp)
LIMIT 5
-- Returns true for addresses such as '10.0.0.1', '127.0.0.1', 'fe80::1', and 'fd00::1'
```

## ipFamily / ip_family

```sql
ipFamily(ipString)
```

Returns the address family for a plain IP address string: `4` for IPv4 and `6` for IPv6.

```sql
SELECT ipFamily('2001:db8::1') AS ip_version
-- Returns 6
```

## ipv4ToLong

```sql
ipv4ToLong(ipString)
```

Converts an IPv4 address string to its unsigned 32-bit integer representation as a `LONG`.

```sql
SELECT ipv4ToLong('192.168.1.1') AS ip_as_long
-- Returns 3232235777
```

## longToIpv4

```sql
longToIpv4(value)
```

Converts an unsigned 32-bit `LONG` value in the IPv4 range back to dotted-decimal IPv4 text.

```sql
SELECT longToIpv4(3232235777) AS ip_text
-- Returns '192.168.1.1'
```

## ipv6ToBytes

```sql
ipv6ToBytes(ipString)
```

Converts an IPv6 address string to a 16-byte `BYTES` value.

```sql
SELECT ipv6ToBytes('2001:db8::1') AS ip_bytes
FROM myTable
LIMIT 1
```

## bytesToIpv6

```sql
bytesToIpv6(bytes)
```

Converts a 16-byte IPv6 `BYTES` value to canonical IPv6 text.

```sql
SELECT bytesToIpv6(ipv6ToBytes('2001:db8::1')) AS ip_text
-- Returns '2001:db8::1'
```

## ipv4ToIpv6

```sql
ipv4ToIpv6(ipString)
```

Maps an IPv4 address to its IPv4-mapped IPv6 representation.

```sql
SELECT ipv4ToIpv6('192.168.1.1') AS mapped_ip
-- Returns '::ffff:c0a8:101'
```

## ipMaskLen / ip_mask_len

```sql
ipMaskLen(cidr)
```

Returns the prefix length from a CIDR string.

```sql
SELECT ipMaskLen('192.168.1.0/24') AS prefix_len
-- Returns 24
```

## ipNetmask / ip_netmask

```sql
ipNetmask(cidr)
```

Returns the network mask for a CIDR prefix as an IP address string.

```sql
SELECT ipNetmask('192.168.1.0/24') AS netmask
-- Returns '255.255.255.0'
```

## ipHostmask / ip_hostmask

```sql
ipHostmask(cidr)
```

Returns the host mask for a CIDR prefix as an IP address string.

```sql
SELECT ipHostmask('192.168.1.0/24') AS hostmask
-- Returns '0.0.0.255'
```

## ipv4CIDRToRange

```sql
ipv4CIDRToRange(cidr)
```

Returns a two-element `STRING[]` containing the minimum and maximum IPv4 addresses covered by the CIDR range.

```sql
SELECT ipv4CIDRToRange('192.168.1.0/24') AS ip_range
FROM myTable
LIMIT 1
-- Returns ['192.168.1.0', '192.168.1.255']
```
