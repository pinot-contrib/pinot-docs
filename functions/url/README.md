# URL Functions

This document describes the URL utility functions available as scalar functions. These functions allow you to extract, transform, and manipulate various components of a URL such as the protocol, domain, port, path, query parameters, and more.&#x20;

### urlProtocol

**Description**: Extracts the protocol (scheme) from the URL.

**Syntax**:

```
urlProtocol(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The protocol (e.g., "http", "https") or null if the URL is invalid.

**Example**:

```
SELECT urlProtocol('https://example.com/path');
// Returns: "https"
```

### urlDomain

**Description**: Extracts the domain from the URL.

**Syntax**:

```
urlDomain(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The full domain (e.g., "www.example.com") or null if the URL is invalid.

**Example**:

```
SELECT urlDomain('https://www.example.com/path');
// Returns: "www.example.com"
```

### urlDomainWithoutWWW

**Description**: Extracts the domain from the URL while removing a leading "www." if present.

**Syntax**:

```
urlDomainWithoutWWW(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The domain without the "www." prefix (e.g., "example.com") or null if invalid.

**Example**:

```
SELECT urlDomainWithoutWWW('https://www.example.com/path');
// Returns: "example.com"
```

### urlTopLevelDomain

**Description**: Extracts the top-level domain (TLD) from the URL.

**Syntax**:

```
urlTopLevelDomain(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The top-level domain (e.g., "com", "org") or null if invalid.

**Example**:

```
SELECT urlTopLevelDomain('https://example.com/path');
// Returns: "com"
```

### urlFirstSignificantSubdomain

**Description**: Extracts the first significant subdomain from the URL based on standard TLD rules.

**Syntax**:

```
urlFirstSignificantSubdomain(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The first significant subdomain (for example, for "blog.example.com", returns "example") or null if invalid.

**Example**:

```
SELECT urlFirstSignificantSubdomain('https://blog.example.com');
// Returns: "example"
```

_Note: The logic considers common TLDs such as “com”, “net”, “org”, and “co”._

### cutToFirstSignificantSubdomain

**Description**: Truncates the URL’s domain to include only the first significant subdomain and the top-level domain.

**Syntax**:

```
cutToFirstSignificantSubdomain(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

A truncated domain such as "example.com" (or a deeper hierarchy for non-standard TLDs) or null if invalid.

**Example**:

```
SELECT cutToFirstSignificantSubdomain('https://blog.example.com');
// Returns: "example.com"
```

### cutToFirstSignificantSubdomainWithWWW

**Description**: Similar to cutToFirstSignificantSubdomain but preserves a leading "www." if it is part of the URL.

**Syntax**:

```
cutToFirstSignificantSubdomainWithWWW(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The truncated domain with "www." preserved (if applicable) or null if invalid.

**Example**:

```
SELECT cutToFirstSignificantSubdomainWithWWW('https://www.blog.example.com');
// Returns: "www.example.com"
```

### urlPort

**Description**: Extracts the port number from the URL.

**Syntax**:

```
urlPort(url: String) → int
```

**Parameters**:

• url: URL string.

**Returns**:

The port number, or -1 if no port is specified or if the URL is invalid.

**Example**:

```
SELECT urlPort('https://example.com:8080/path');
// Returns: 8080
```

### urlPath

**Description**: Extracts the path component from the URL (excluding the query string).

**Syntax**:

```
urlPath(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The URL path (e.g., "/path/to/resource") or null if invalid.

**Example**:

```
SELECT urlPath('https://example.com/path?query=1');
// Returns: "/path"
```

### urlPathWithQuery

**Description**: Extracts the path component from the URL. (Note that this function uses the raw path as returned by the URI parser.)

**Syntax**:

```
urlPathWithQuery(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The URL path (which may include query encoding details) or null if invalid.

**Example**:

```
SELECT urlPathWithQuery('https://example.com/path?query=1');
// Returns: "/path"
```

### urlQueryString

**Description**: Extracts the query string from the URL without the leading ? and excluding the fragment.

**Syntax**:

```
urlQueryString(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The query string (e.g., "key=value\&key2=value2"), or null if absent or invalid.

**Example**:

```
SELECT urlQueryString('https://example.com/path?key=value#section');
// Returns: "key=value"
```

### urlFragment

**Description**: Extracts the fragment identifier from the URL (without the # symbol).

**Syntax**:

```
urlFragment(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The fragment (e.g., "section") or null if invalid or not present.

**Example**:

```
SELECT urlFragment('https://example.com/path#section');
// Returns: "section"
```

### urlQueryStringAndFragment

**Description**: Combines the query string and fragment identifier from the URL into a single string.

**Syntax**:

```
urlQueryStringAndFragment(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

A concatenated string such as "key=value#section", or null if neither component is present.

**Example**:

```
SELECT urlQueryStringAndFragment('https://example.com/path?key=value#section');
// Returns: "key=value#section"
```

### extractURLParameter

**Description**: Extracts the value of a specific query parameter from the URL. If multiple parameters with the same name exist, the first occurrence is returned.

**Syntax**:

```
extractURLParameter(url: String, name: String) → String
```

**Parameters**:

• url: URL string.

• name: Name of the parameter to extract.

**Returns**:

The value of the parameter, or an empty string if not found or if the URL is invalid.

**Example**:

```
SELECT extractURLParameter('https://example.com/path?page=1&lr=213', 'page');
// Returns: "1"
```

### extractURLParameters

**Description**: Extracts all query parameters from the URL as an array of name=value pairs.

**Syntax**:

```
extractURLParameters(url: String) → String[]
```

**Parameters**:

• url: URL string.

**Returns**:

An array of query parameters (e.g., \["page=1", "lr=213"]), or an empty array if no parameters exist.

**Example**:

```
SELECT extractURLParameters('https://example.com/path?page=1&lr=213');
// Returns: ["page=1", "lr=213"]
```

### extractURLParameterNames

**Description**: Extracts the names of all query parameters present in the URL.

**Syntax**:

```
extractURLParameterNames(url: String) → String[]
```

**Parameters**:

• url: URL string.

**Returns**:

An array of parameter names (e.g., \["page", "lr"]), or an empty array if no query parameters exist.

**Example**:

```
SELECT extractURLParameterNames('https://example.com/path?page=1&lr=213');
// Returns: ["page", "lr"]
```

### urlHierarchy

**Description**: Generates a hierarchy of URLs truncated at each level of the path. The base URL (scheme and host) is always included.

**Syntax**:

```
urlHierarchy(url: String) → String[]
```

**Parameters**:

• url: URL string.

**Returns**:

An array of URLs representing the hierarchical levels. For example, given the URL "https://example.com/a/b/c", it returns:

```
[
  "https://example.com",
  "https://example.com/a",
  "https://example.com/a/b",
  "https://example.com/a/b/c"
]
```

**Example**:

```
SELECT urlHierarchy('https://example.com/a/b/c');
// Returns: ["https://example.com", "https://example.com/a", "https://example.com/a/b", "https://example.com/a/b/c"]
```

### urlPathHierarchy

**Description**: Generates a hierarchy of the path segments from the URL. The protocol and host are excluded, and the root ("/") is not included.

**Syntax**:

```
urlPathHierarchy(url: String) → String[]
```

**Parameters**:

• url: URL string.

**Returns**:

An array of hierarchical path segments. For example, for the URL "https://example.com/browse/CONV-6788", it returns:

```
["/browse", "/browse/CONV-6788"]
```

**Example**:

```
SELECT urlPathHierarchy('https://example.com/browse/CONV-6788');
// Returns: ["/browse", "/browse/CONV-6788"]
```

### urlEncode

**Description**: Encodes a URL string into a URL-safe format. Spaces are replaced with +.

**Syntax**:

```
urlEncode(url: String) → String
```

**Parameters**:

• url: URL string to encode.

**Returns**:

The URL-encoded string or null if the input is invalid.

**Example**:

```
SELECT urlEncode('https://example.com/path with space');
// Returns: "https%3A%2F%2Fexample.com%2Fpath+with+space"
```

### urlDecode

**Description**: Decodes a URL-encoded string.

**Syntax**:

```
urlDecode(url: String) → String
```

**Parameters**:

• url: URL-encoded string.

**Returns**:

The decoded URL string or null if the input is invalid.

**Example**:

```
SELECT urlDecode('https%3A%2F%2Fexample.com%2Fpath+with+space');
// Returns: "https://example.com/path with space"
```

### urlEncodeFormComponent

**Description**: Encodes a string as a URL form component following RFC-1866 standards. Spaces are encoded as +.

**Syntax**:

```
urlEncodeFormComponent(url: String) → String
```

**Parameters**:

• url: String to encode.

**Returns**:

The encoded string or null if the input is invalid.

**Example**:

```
SELECT urlEncodeFormComponent('Hello World!');
// Returns: "Hello+World%21"
```

### urlDecodeFormComponent

**Description**: Decodes a URL form component encoded per RFC-1866 (decodes + to a space).

**Syntax**:

```
urlDecodeFormComponent(url: String) → String
```

**Parameters**:

• url: URL-encoded string.

**Returns**:

The decoded string or null if the input is invalid.

**Example**:

```
SELECT urlDecodeFormComponent('Hello+World%21');
// Returns: "Hello World!"
```

### urlNetloc

**Description**: Extracts the network locality from the URL. This includes user information (if any), the host, and the port.

**Syntax**:

```
urlNetloc(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

A string in the format username:password@host:port (if user info is present) or null if the URL is invalid.

**Example**:

```
SELECT urlNetloc('https://user:pass@example.com:8080/path');
// Returns: "user:pass@example.com:8080"
```

### cutWWW

**Description**: Removes the leading "www." from the URL’s domain.

**Syntax**:

```
cutWWW(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The URL with the "www." prefix removed from the domain. If an error occurs, the original URL is returned.

**Example**:

```
SELECT cutWWW('https://www.example.com/path');
// Returns: "https://example.com/path"
```

### cutQueryString

**Description**: Removes the query string (including the ?) from the URL.

**Syntax**:

```
cutQueryString(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The URL without the query string. If an error occurs, the original URL is returned.

**Example**:

```
SELECT cutQueryString('https://example.com/path?key=value');
// Returns: "https://example.com/path"
```

### cutFragment

**Description**: Removes the fragment identifier (including the #) from the URL.

**Syntax**:

```
cutFragment(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The URL without the fragment. If an error occurs, the original URL is returned.

**Example**:

```
SELECT cutFragment('https://example.com/path#section');
// Returns: "https://example.com/path"
```

### cutQueryStringAndFragment

**Description**: Removes both the query string and the fragment identifier from the URL.

**Syntax**:

```
cutQueryStringAndFragment(url: String) → String
```

**Parameters**:

• url: URL string.

**Returns**:

The URL stripped of both the query string and fragment. If an error occurs, the original URL is returned.

**Example**:

```
SELECT cutQueryStringAndFragment('https://example.com/path?key=value#section');
// Returns: "https://example.com/path"
```

### cutURLParameter

**Description**: Removes a specific query parameter from the URL.

**Syntax**:

```
cutURLParameter(url: String, name: String) → String
```

**Parameters**:

• url: URL string.

• name: The query parameter name to remove.

**Returns**:

The URL with the specified query parameter removed. If an error occurs, the original URL is returned.

**Example**:

```
SELECT cutURLParameter('https://example.com/path?key=value&remove=this', 'remove');
// Returns: "https://example.com/path?key=value"
```

### cutURLParameters

**Description**: Removes multiple query parameters from the URL.

**Syntax**:

```
cutURLParameters(url: String, names: String[]) → String
```

**Parameters**:

• url: URL string.

• names: An array of query parameter names to remove.

**Returns**:

The URL with the specified query parameters removed.

**Example**:

```
SELECT cutURLParameters('https://example.com/path?key=value&remove=this&other=param', ARRAY['remove', 'other']);
// Returns: "https://example.com/path?key=value"
```
