---
description: This section contains reference documentation for the url functions.
---

# Url

Returns the url-encoded or url-decoded string of the input string with UTF\_8 encoding, formatting details see [java.net.URLEncoder](https://docs.oracle.com/javase/8/docs/api/java/net/URLEncoder.html)

## Signature

> encodeUrl(string)
>
> decodeUrl(string)

## Usage Examples

```sql
SELECT concat('https://www.google.com/search?q=', encodeUrl('key1=val1 key2=45% key3=#47'),'') AS encoded
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>encoded</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>https://www.google.com/search?q=key1%3Dval1+key2%3D45%25+key3%3D%2347</td>
    </tr>
  </tbody>
</table>

```sql
SELECT decodeUrl('https://www.google.com/search?q=key1%3Dval1+key2%3D45%25+key3%3D%2347') AS decoded
FROM ignoreMe
```

<table>
  <thead>
    <tr>
      <th>decoded</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>https://www.google.com/search?q=key1=val1 key2=45% key3=#47</td>
    </tr>
  </tbody>
</table>
