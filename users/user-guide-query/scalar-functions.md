# User-Defined Functions \(UDFs\)

Pinot currently supports two ways of for user to implement their own functions 

* Groovy Scripts
* Scalar Functions

### Groovy Scripts

Pinot allows you the run any function other than those supported out of the box using [Apache Groovy](https://groovy-lang.org/) scripts. The syntax for executing groovy script within the query is as follows -

**`GROOVY('result value metadata json', ''groovy script', arg0, arg1, arg2...)`**

This function will execute the groovy script using the arguments provided and return the result which matches the provided result value metadata. ****The function requires the following arguments - 

`Result value metadata json` - json string representing result value metadata. Must contain non-null keys `resultType` and `isSingleValue`. 

`Groovy script to execute`- groovy script string, which uses `arg0`,  `arg1`, `arg2` etc to refer to the arguments provided within the script

`arguments` - pinot columns/other transform functions which are arguments to the groovy script

**Examples**

* Add colA and colB and return a single-value INT `groovy('{"returnType":"INT","isSingleValue":true}', 'arg0 + arg1', colA, colB)` 
* Find the max element in mvColumn array and return a single-value INT

  `groovy('{"returnType":"INT","isSingleValue":true}', 'arg0.toList().max()', mvColumn)`  

* Find all elements of the array mvColumn and return as a multi-value LONG column

  `groovy('{"returnType":"LONG","isSingleValue":false}', 'arg0.findIndexValues{ it > 5 }', mvColumn)`  

* Multiply length of array mvColumn with colB and return a single-value DOUBLE

  `groovy('{"returnType":"DOUBLE","isSingleValue":true}', 'arg0 * arg1', arraylength(mvColumn), colB)`  

* Find all indexes in mvColumnA which have value `foo`, add values at those indexes in mvColumnB

  `groovy( '{"returnType":"DOUBLE","isSingleValue":true}', 'def x = 0; arg0.eachWithIndex{item, idx-> if (item == "foo") {x = x + arg1[idx] }}; return x' , mvColumnA, mvColumnB)`  

* Switch case which returns a FLOAT value depending on length of mvCol array 

  `groovy('{\"returnType\":\"FLOAT\", \"isSingleValue\":true}', 'def result; switch(arg0.length()) { case 10: result = 1.1; break; case 20: result = 1.2; break; default: result = 1.3;}; return result.floatValue()', mvCol)`   

* Any Groovy script which takes no arguments

  `groovy('new Date().format( "yyyyMMdd" )', '{"returnType":"STRING","isSingleValue":true}')`



### Scalar Functions

Since 0.5.0 release, Pinot supports custom functions which returns a single output for multiple inputs. Some examples of scalar functions can be found in [StringFunctions](supported-transformations.md#string-functions) and [DateTimeFunctions ](supported-transformations.md#datetime-functions)

Pinot automatically identifies and registers all the functions with annotation `@ScalarFunction` 

Currently only Java methods are supported.

#### Adding user defined scalar functions

You can add new scalar functions as follows - 

* Create a new java project. Make sure you keep the package name as `org.apache.pinot.scalar.XXXX`
* In your java project include the dependency

{% tabs %}
{% tab title="Maven" %}
```text
<dependency>
  <groupId>org.apache.pinot</groupId>
  <artifactId>pinot-common</artifactId>
  <version>0.5.0</version>
 </dependency>
```
{% endtab %}

{% tab title="Gradle" %}
```text
include 'org.apache.pinot:pinot-common:0.5.0'
```
{% endtab %}
{% endtabs %}

* Annotate your methods with `@ScalarFunction` annotation. Make sure the method is `static` and returns only a single value output. The input and output can have one of the following types - 
  * Integer
  * Long
  * Double
  * String

```text
//Example Scalar function

@ScalarFunction
static String mySubStr(String input, Integer beginIndex) {
  return input.substring(beginIndex);
}
```

* Place the compiled JAR in `/plugins` directory in pinot. You will need to restart all pinot instances if they are already running.
* Now, you can use the function in query as follows. Note that function name in SQL is same as function name in Java. The SQL function name is case-insensitive as well.

```text
SELECT mysubstr(playerName, 4) FROM baseballStats
```



