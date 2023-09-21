# User-Defined Functions (UDFs)

Pinot currently supports two ways for you to implement your own functions:

* Groovy Scripts
* Scalar Functions

### Groovy Scripts

Pinot allows you to run any function using [Apache Groovy](https://groovy-lang.org) scripts. The syntax for executing Groovy script within the query is as follows:

**`GROOVY('result value metadata json', ''groovy script', arg0, arg1, arg2...)`**

This function will execute the groovy script using the arguments provided and return the result that matches the provided result value metadata. \*\*\*\* The function requires the following arguments:

* `Result value metadata json` - json string representing result value metadata. Must contain non-null keys `resultType` and `isSingleValue`.
* `Groovy script to execute`- groovy script string, which uses `arg0`, `arg1`, `arg2` etc to refer to the arguments provided within the script
* `arguments` - pinot columns/other transform functions that are arguments to the groovy script

**Examples**

* Add colA and colB and return a single-value INT\
  `groovy( '{"returnType":"INT","isSingleValue":true}', 'arg0 + arg1', colA, colB)`\\
*   Find the max element in mvColumn array and return a single-value INT

    `groovy('{"returnType":"INT","isSingleValue":true}', 'arg0.toList().max()', mvColumn)`\\
*   Find all elements of the array mvColumn and return as a multi-value LONG column

    `groovy('{"returnType":"LONG","isSingleValue":false}', 'arg0.findIndexValues{ it > 5 }', mvColumn)`\\
*   Multiply length of array mvColumn with colB and return a single-value DOUBLE

    `groovy('{"returnType":"DOUBLE","isSingleValue":true}', 'arg0 * arg1', arraylength(mvColumn), colB)`\\
*   Find all indexes in mvColumnA which have value `foo`, add values at those indexes in mvColumnB

    `groovy( '{"returnType":"DOUBLE","isSingleValue":true}', 'def x = 0; arg0.eachWithIndex{item, idx-> if (item == "foo") {x = x + arg1[idx] }}; return x' , mvColumnA, mvColumnB)`\\
*   Switch case which returns a FLOAT value depending on length of mvCol array

    `groovy('{\"returnType\":\"FLOAT\", \"isSingleValue\":true}', 'def result; switch(arg0.length()) { case 10: result = 1.1; break; case 20: result = 1.2; break; default: result = 1.3;}; return result.floatValue()', mvCol)` \\
*   Any Groovy script which takes no arguments

    `groovy('new Date().format( "yyyyMMdd" )', '{"returnType":"STRING","isSingleValue":true}')`

:warning: Note that Groovy script doesn't accept Built-In ScalarFunction that's specific to Pinot queries. See the section below for more information.

:warning: **Enabling Groovy**

Allowing execuatable Groovy in queries can be a security vulnerability. Use caution and be aware of the security risks if you decide to allow groovy. If you would like to enable Groovy in Pinot queries, you can set the following broker config.

`pinot.broker.disable.query.groovy=false`

If not set, Groovy in queries is disabled by default.

The above configuration applies across the entire Pinot cluster. If you want a table level override to enable/disable Groovy queries, the following property can be set in the query table config.

```json
{
  "tableName": "myTable",
  "tableType": "OFFLINE",
 
  "query" : {
    "disableGroovy": false
  }
}
```

### Scalar Functions

Since the 0.5.0 release, Pinot supports custom functions that return a single output for multiple inputs. Examples of scalar functions can be found in [StringFunctions](supported-transformations.md#string-functions) and [DateTimeFunctions](supported-transformations.md#datetime-functions)

Pinot automatically identifies and registers all the functions that have the `@ScalarFunction` annotation.

Only Java methods are supported.

#### Adding user defined scalar functions

You can add new scalar functions as follows:

* Create a new java project. Make sure you keep the package name as `org.apache.pinot.scalar.XXXX`
* In your java project include the dependency

{% tabs %}
{% tab title="Maven" %}
```
<dependency>
  <groupId>org.apache.pinot</groupId>
  <artifactId>pinot-common</artifactId>
  <version>0.5.0</version>
 </dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```
include 'org.apache.pinot:pinot-common:0.5.0'
```
{% endtab %}
{% endtabs %}

* Annotate your methods with `@ScalarFunction` annotation. Make sure the method is `static` and returns only a single value output. The input and output can have one of the following types -
  * Integer
  * Long
  * Double
  * String

```
//Example Scalar function

@ScalarFunction
static String mySubStr(String input, Integer beginIndex) {
  return input.substring(beginIndex);
}
```

* Place the compiled JAR in the `/plugins` directory in pinot. You will need to restart all Pinot instances if they are already running.
* Now, you can use the function in a query as follows:

```
SELECT mysubstr(playerName, 4) 
FROM baseballStats
```

:warning: Note that the function name in SQL is the same as the function name in Java. The SQL function name is case-insensitive as well.
