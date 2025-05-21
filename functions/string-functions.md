# String Functions

[**UPPER**](../functions-1/upper.md)(col)\
convert string to upper case

[**LOWER**](../functions-1/lower.md)(col)\
convert string to lower case

[**REVERSE**](../functions-1/reverse.md)(col)\
reverse the string

[**SUBSTR**](../functions-1/substr.md)(col, startIndex, endIndex)\
Gets substring of the input string from start to endIndex. Index begins at 0. Set endIndex to -1 to calculate till end of the string

[**CONCAT(col1, col2, seperator)**](../functions-1/concat.md)\
Concatenate two input strings using the seperator

[**TRIM(col)**](../functions-1/trim.md)\
trim spaces from both side of the string

[**LTRIM(col)**](../functions-1/ltrim.md)\
trim spaces from left side of the string

[**RTRIM(col)**](../functions-1/rtrim.md)\
trim spaces from right side of the string

[**LENGTH(col)**](../functions-1/length.md)\
calculate length of the string

[**STRPOS(col, find, N)**](../functions-1/strpos.md)\
Find Nth instance of `find` string in input. Returns 0 if input string is empty. Returns -1 if the Nth instance is not found or input string is null.

[**STARTSWITH(col, prefix)**](../functions-1/startswith.md)\
returns `true` if columns starts with prefix string.

[**REPLACE(col, find, substitute)**](../functions-1/replace.md)\
replace all instances of `find` with `replace` in input

[**RPAD(col, size, pad)**](../functions-1/rpad.md)\
string padded from the right side with `pad` to reach final `size`

[**LPAD(col, size, pad)**](../functions-1/lpad.md)\
string padded from the left side with `pad` to reach final `size`

[**CODEPOINT(col)**](../functions-1/codepoint.md)\
the Unicode codepoint of the first character of the string

[**CHR(codepoint)**](../functions-1/chr.md)\
the character corresponding to the Unicode codepoint

[**regexpExtract(value, regexp)**](../functions-1/regexpextract.md)\
Extracts values that match the provided regular expression

[**regexpReplace(input, matchRegexp, replaceRegexp, matchStartPos, occurrence, flag)**\
](../functions-1/regexpreplace.md)Find and replace a string or regexp pattern with a target string or regexp pattern

[**remove(input, search)**](../functions-1/remove.md)\
removes all instances of search from string

[**urlEncoding(string)**](../functions-1/url.md)\
url-encode a string with UTF-8 format

[**urlDecoding(string)**](../functions-1/url.md)\
decode a url to plaintext string

[**fromBase64(string)**](../functions-1/base64.md)\
decode a Base64-encoded string to bytes represented as a hex string

[**toUtf8(string)**](../functions-1/utf8.md)\
decode a UTF8-encoded string to bytes represented as a hex string

[**isSubnetOf(ipPrefix, ipAddress)**](../functions-1/issubnetof.md)\
checks if ipAddress is in the subnet of the ipPrefix

