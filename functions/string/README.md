# String Functions

[**UPPER**](../functions/string/upper.md)(col)\
convert string to upper case

[**LOWER**](../functions/string/lower.md)(col)\
convert string to lower case

[**INITCAP**](../functions/string/initcap.md)(col)\
convert the first letter of each word to uppercase and the rest to lowercase

[**REVERSE**](../functions/string/reverse.md)(col)\
reverse the string

[**SUBSTR**](../functions/string/substr.md)(col, startIndex, endIndex)\
Gets substring of the input string from start to endIndex. Index begins at 0. Set endIndex to -1 to calculate till end of the string

**SUBSTRING(col, beginIndex)** / **SUBSTRING(col, beginIndex, length)**\
Returns the substring of the input string starting at a 1-based `beginIndex`. When `length` is provided, returns a substring of that length.

Usage: `SUBSTRING(col, beginIndex)` or `SUBSTRING(col, beginIndex, length)`\
Example: `SELECT SUBSTRING('hello', 2) FROM myTable` returns `'ello'`\
Example: `SELECT SUBSTRING('hello', 2, 3) FROM myTable` returns `'ell'`

[**CONCAT(col1, col2, seperator)**](../functions/string/concat.md)\
Concatenate two input strings using the seperator

[**TRIM(col)**](../functions/string/trim.md)\
trim spaces from both side of the string

**TRIM(end, characters, value)**\
Standard SQL trim function. Trims the specified `characters` from the specified end of the string. `end` can be `BOTH`, `LEADING`, or `TRAILING`.

Usage: `TRIM('BOTH', 'xy', col)`\
Example: `SELECT TRIM('LEADING', ' ', '  hello  ') FROM myTable` returns `'hello  '`

[**LTRIM(col)**](../functions/string/ltrim.md)\
trim spaces from left side of the string

[**RTRIM(col)**](../functions/string/rtrim.md)\
trim spaces from right side of the string

[**LENGTH(col)**](../functions/string/length.md)\
calculate length of the string

[**levenshtein_distance(string1, string2)**](../functions/string/levenshtein_distance.md)\
Returns the Levenshtein edit distance between two strings

**hammingDistance(string1, string2)**\
Returns the Hamming distance between two strings of equal length. Returns -1 if the strings have different lengths.

Usage: `hammingDistance(col1, col2)`\
Example: `SELECT hammingDistance('karolin', 'kathrin') FROM myTable` returns `3`

[**STRPOS(col, find, N)**](../functions/string/strpos.md)\
Find Nth instance of `find` string in input. Returns 0 if input string is empty. Returns -1 if the Nth instance is not found or input string is null.

**strrpos(col, find)** / **strrpos(col, find, N)**\
Returns the index of the last occurrence of `find` in the input string. When `N` is provided, returns the Nth occurrence counting from the end of the string.

Usage: `strrpos(col, find)` or `strrpos(col, find, N)`\
Example: `SELECT strrpos('hello world hello', 'hello') FROM myTable`

**contains(col, substring)**\
Returns `true` if the input string contains the specified substring, `false` otherwise.

Usage: `contains(col, substring)`\
Example: `SELECT contains(playerName, 'john') FROM myTable`

[**STARTSWITH(col, prefix)**](../functions/string/startswith.md)\
returns `true` if columns starts with prefix string.

**endsWith(col, suffix)**\
Returns `true` if the input string ends with the specified suffix, `false` otherwise.

Usage: `endsWith(col, suffix)`\
Example: `SELECT endsWith(playerName, 'son') FROM myTable`

**strcmp(string1, string2)**\
Compares two strings lexicographically. Returns `0` if equal, a value less than `0` if the first string is lexicographically less than the second, and a value greater than `0` if the first string is lexicographically greater.

Usage: `strcmp(col1, col2)`\
Example: `SELECT strcmp(name1, name2) FROM myTable`

[**REPLACE(col, find, substitute)**](../functions/string/replace.md)\
replace all instances of `find` with `replace` in input

[**RPAD(col, size, pad)**](../functions/string/rpad.md)\
string padded from the right side with `pad` to reach final `size`

[**LPAD(col, size, pad)**](../functions/string/lpad.md)\
string padded from the left side with `pad` to reach final `size`

**leftSubStr(col, length)** / **left(col, length)**\
Returns the leftmost `length` characters from the input string.

Usage: `leftSubStr(col, length)` or `left(col, length)`\
Example: `SELECT leftSubStr('hello', 3) FROM myTable` returns `'hel'`

**rightSubStr(col, length)** / **right(col, length)**\
Returns the rightmost `length` characters from the input string.

Usage: `rightSubStr(col, length)` or `right(col, length)`\
Example: `SELECT rightSubStr('hello', 3) FROM myTable` returns `'llo'`

**repeat(col, times)** / **repeat(col, separator, times)**\
Concatenates the input string to itself the specified number of times. When a `separator` is provided, it is placed between each repetition.

Usage: `repeat(col, times)` or `repeat(col, separator, times)`\
Example: `SELECT repeat('ab', 3) FROM myTable` returns `'ababab'`\
Example: `SELECT repeat('ab', ',', 3) FROM myTable` returns `'ab,ab,ab'`

**split(col, delimiter)** / **split(col, delimiter, limit)**\
Splits the input string by the specified delimiter and returns an array of strings. Also available as `stringToArray`. When `limit` is provided, limits the number of resulting parts.

Usage: `split(col, delimiter)` or `split(col, delimiter, limit)`\
Example: `SELECT split('a,b,c', ',') FROM myTable` returns `['a', 'b', 'c']`

**splitPart(col, delimiter, index)** / **splitPart(col, delimiter, limit, index)**\
Splits the input string by the specified delimiter and returns the element at the given index. The index is 0-based and supports negative values to index from the end. Returns `"null"` if the index is out of bounds.

Usage: `splitPart(col, delimiter, index)` or `splitPart(col, delimiter, limit, index)`\
Example: `SELECT splitPart('a,b,c', ',', 1) FROM myTable` returns `'b'`\
Example: `SELECT splitPart('a,b,c', ',', -1) FROM myTable` returns `'c'`

**normalize(col)** / **normalize(col, form)**\
Normalizes a Unicode string. Without a form argument, uses NFC normalization. The optional `form` parameter can be `NFC`, `NFD`, `NFKC`, or `NFKD`.

Usage: `normalize(col)` or `normalize(col, 'NFC')`\
Example: `SELECT normalize(textCol) FROM myTable`

[**CODEPOINT(col)**](../functions/string/codepoint.md)\
the Unicode codepoint of the first character of the string

[**CHR(codepoint)**](../functions/string/chr.md)\
the character corresponding to the Unicode codepoint

**fromBytes(bytes, charsetName)**\
Converts a byte array to a string using the specified character set encoding.

Usage: `fromBytes(col, 'UTF-8')`\
Example: `SELECT fromBytes(byteCol, 'UTF-8') FROM myTable`

**toBytes(col, charsetName)**\
Converts a string to a byte array using the specified character set encoding.

Usage: `toBytes(col, 'UTF-8')`\
Example: `SELECT toBytes(stringCol, 'UTF-8') FROM myTable`

**fromUtf8(bytes)**\
Converts a UTF-8 encoded byte array to a string.

Usage: `fromUtf8(col)`\
Example: `SELECT fromUtf8(byteCol) FROM myTable`

**fromAscii(bytes)**\
Converts an ASCII encoded byte array to a string.

Usage: `fromAscii(col)`\
Example: `SELECT fromAscii(byteCol) FROM myTable`

**toAscii(col)**\
Converts a string to an ASCII encoded byte array.

Usage: `toAscii(col)`\
Example: `SELECT toAscii(stringCol) FROM myTable`

**toBase64(bytes)**\
Encodes binary data (byte array) to a Base64 encoded string.

Usage: `toBase64(col)`\
Example: `SELECT toBase64(byteCol) FROM myTable`

[**regexpExtract(value, regexp)**](../functions/string/regexpextract.md)\
Extracts values that match the provided regular expression

[**regexpReplace(input, matchRegexp, replaceRegexp, matchStartPos, occurrence, flag)**\
](../functions/string/regexpreplace.md)Find and replace a string or regexp pattern with a target string or regexp pattern

[**remove(input, search)**](../functions/string/remove.md)\
removes all instances of search from string

**toUUIDBytes(uuidString)**\
Converts a UUID string to a 16-byte array representation. Returns null if the input is not a valid UUID.

Usage: `toUUIDBytes(col)`\
Example: `SELECT toUUIDBytes('550e8400-e29b-41d4-a716-446655440000') FROM myTable`

**fromUUIDBytes(bytes)**\
Converts a 16-byte array to a UUID string representation.

Usage: `fromUUIDBytes(col)`\
Example: `SELECT fromUUIDBytes(uuidByteCol) FROM myTable`

**isJson(col)**\
Returns `true` if the input string is valid JSON, `false` otherwise.

Usage: `isJson(col)`\
Example: `SELECT isJson('{"key":"value"}') FROM myTable` returns `true`

[**urlEncoding(string)**](../functions/string/url.md)\
url-encode a string with UTF-8 format

[**urlDecoding(string)**](../functions/string/url.md)\
decode a url to plaintext string

[**fromBase64(string)**](../functions/binary/base64.md)\
decode a Base64-encoded string to bytes represented as a hex string

[**toUtf8(string)**](../functions/binary/utf8.md)\
decode a UTF8-encoded string to bytes represented as a hex string

[**isSubnetOf(ipPrefix, ipAddress)**](../functions/misc/issubnetof.md)\
checks if ipAddress is in the subnet of the ipPrefix

[**Add Prefix, Suffix & Ngram UDFs**](../functions/string/add-prefix-suffix-ngram-udfs.md)\
provides prefix, suffix and ngram functionality for string manipulation
