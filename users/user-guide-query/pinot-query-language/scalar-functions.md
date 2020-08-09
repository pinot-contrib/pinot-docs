# Scalar Functions

Since 0.5.0 release, Pinot supports custom functions which returns a single output for multiple inputs. Some examples of scalar functions can be found in [StringFunctions](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/function/StringFunctions.java) and [DateTimeFunctions](https://github.com/apache/incubator-pinot/blob/master/pinot-common/src/main/java/org/apache/pinot/common/function/DateTimeFunctions.java) 

Pinot automatically identifies and registers all the functions with annotation `@ScalarFunction` 

Currently only Java methods are supported.

### Adding scalar functions

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



