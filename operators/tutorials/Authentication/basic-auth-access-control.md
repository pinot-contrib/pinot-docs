---
description: Set up BasicAuthAccessControl for access to controller and broker
---

# BasicAuthAccessControl

# Tokens and User Credentials

The configuration of HTTP Basic Auth in Apache Pinot distinguishes between **Tokens,** which are typically provided to service accounts, and **User Credentials**, which can be used by a human to log onto the web UI or issue SQL queries. While we distinguish these two concepts in the configuration of HTTP Basic Auth, they are fully-convertible formats holding the same authentication information. This distinction allows us to support future token-based authentication methods not reliant on username and password pairs. Currently, Tokens are merely base64-encoded username & password tuples, similar to those you can find in HTTP Authorization header values ([RFC 7617](https://tools.ietf.org/html/rfc7617))

This is best demonstrated by example of introducing ACLs with a simple admin + user setup. In order to enable authentication on a cluster without interrupting operations, we'll go these steps in sequence:

**1. Create "admin" and "user" in the controller properties**

```
# Create users "admin" and "user". Keep in mind we're not enforcing any ACLs yet.
controller.admin.access.control.principals=admin,user

# Set the user's password to "secret" and allow "READ" only
controller.admin.access.control.principals.user.password=secret
controller.admin.access.control.principals.user.permissions=READ

# Set the admin's password to "verysecret"
controller.admin.access.control.principals.admin.password=verysecret

```

**2. Distribute service tokens to pinot's components**

For simplicity, we'll reuse the admin credentials as service tokens. In a production environment you'll keep them separate.

{% tabs %}
{% tab title="Controller" %}
```
# Enable the controller to fetch segments by providing the credentials as a token
controller.segment.fetcher.auth.token=Basic YWRtaW46dmVyeXNlY3JldA

# "Basic " + base64encode("admin:verysecret")
```
{% endtab %}

{% tab title="Broker" %}
```
# no tokens required
```
{% endtab %}

{% tab title="Minion" %}
```
segment.fetcher.auth.token=Basic YWRtaW46dmVyeXNlY3JldA
task.auth.token=Basic YWRtaW46dmVyeXNlY3JldA

```
{% endtab %}

{% tab title="Server" %}
```
pinot.server.segment.fetcher.auth.token=Basic YWRtaW46dmVyeXNlY3JldA
pinot.server.segment.uploader.auth.token=Basic YWRtaW46dmVyeXNlY3JldA
pinot.server.instance.auth.token=Basic YWRtaW46dmVyeXNlY3JldA
```
{% endtab %}
{% endtabs %}

Restart the affected components for the configuration changes to take effect.

**3. Enable ACL enforcement on the controller**

```
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.BasicAuthAccessControlFactory
```

After a controller restart, any access to controller APIs requires authentication information. Whether from internal components, external users, or the Web UI.

**4. Create users and enable ACL enforcement on the Broker**

```
# the factory class property is different for the broker
pinot.broker.access.control.class=org.apache.pinot.broker.broker.BasicAuthAccessControlFactory

pinot.broker.access.control.principals=admin,user
pinot.broker.access.control.principals.admin.password=verysecret
pinot.broker.access.control.principals.user.password=secret

# No need to set READ permissions here since broker requests are read-only
```

After restarting the broker, any access to broker APIs requires authentication information as well.

Congratulation! You've successfully enabled authentication on Apache Pinot. Read on to learn more about the details and advanced configuration options.

### Authentication with Web UI and API

Apache Pinot's Basic Auth follows the established standards for HTTP Basic Auth. Credentials are provided via an HTTP Authorization header. The pinot-controller web ui dynamically adapts to your auth configuration and will display a login prompt when basic auth is enabled. Restricted users are still shown all available ui functions, but their operations will fail with an error message if ACLs prohibit access.

If you're using pinot's CLI clients you can provide your credentials either via dedicated username and password arguments, or as pre-serialized token for the HTTP Authorization header. Note, that while most of Apache Pinot's CLI commands support auth, not all of them have been back-fitted yet. If you encounter any such case, you can access the REST API directly, e.g. via curl.

![](<../../.gitbook/assets/Screen Shot 2021-05-25 at 3.35.05 PM.png>)

{% tabs %}
{% tab title="CLI Arguments" %}
```
$ bin/pinot-admin.sh PostQuery \
  -user user -password secret \
  -brokerPort 8000 -query 'SELECT * FROM baseballStats'
```
{% endtab %}

{% tab title="CLI Token" %}
```
$ bin/pinot-admin.sh PostQuery \
  -authToken "Basic dXNlcjpzZWNyZXQ=" \
  -brokerPort 8000 -query 'SELECT * FROM baseballStats'
```
{% endtab %}

{% tab title="HTTP Headers" %}
```
$ curl http://localhost:8000/query/sql \
  -H 'Authorization: Basic dXNlcjpzZWNyZXQ=' \
  -d '{"sql":"SELECT * FROM baseballStats"}'
```
{% endtab %}
{% endtabs %}

### Controller Authentication and Authorization

Pinot-controller has supported custom access control implementations for quite some time. We expanded the scope of this support in 0.8.0+ and added a default implementation for HTTP Basic Auth. Furthermore, the controller's web UI added support for user login workflows and graceful handling of authentication and authorization messages.

Controller Auth can be enabled via configuration in the controller properties. The configuration options allow the specification of usernames and passwords as well as optional ACL restrictions on a per-table and per-access-type (_CREATE_, _READ_, _UPDATE_, _DELETE_) basis.

The example below creates two users, _admin_ with password _verysecret_ and _user_ with password _secret_. _admin_ has full access, whereas _user_ is restricted to READ operations and, additionally, to tables named _myusertable_, _baseballStats_, and _stuff_ in all cases where the API calls are table-specific.

```
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.BasicAuthAccessControlFactory

controller.admin.access.control.principals=admin,user
controller.admin.access.control.principals.admin.password=verysecret
controller.admin.access.control.principals.user.password=secret
controller.admin.access.control.principals.user.tables=myusertable,baseballStats,stuff
controller.admin.access.control.principals.user.permissions=READ
```

This configuration will automatically allow other pinot components to access pinot-controller with the shared _admin_ service token set up earlier.

{% hint style="info" %}
If `*.principals.<user>.tables`is not configured, all tables are accessible to \<user>.
{% endhint %}

### Broker Authentication and Authorization

Pinot-Broker, similar to pinot-controller above, has supported access control for a while now and we added a default implementation for HTTP Basic Auth. Since pinot-broker does not provide a web UI by itself, authentication is only relevant for SQL queries hitting the broker's REST API.

Broker Auth can be enabled via configuration in the broker properties, similar to the controller. The configuration options allow specification of usernames and passwords as well as optional ACL restrictions on a per-table table basis (access type is always READ). Note, that it is possible to configure a different set of users, credentials, and permissions for broker access. However, **if you want a user to be able to access data via the query console on the controller web UI,** that user must (a) share the **same username and password** on both controller and broker, and (b) have **READ permissions and table-level access**.

The example below again creates two users, _admin_ with password _verysecret_ and _user_ with password _secret_. _admin_ has full access, whereas _user_ is restricted to tables named _baseballStats_ and _otherstuff_.

```
# the factory class property is different for the broker
pinot.broker.access.control.class=org.apache.pinot.broker.broker.BasicAuthAccessControlFactory

pinot.broker.access.control.principals=admin,user
pinot.broker.access.control.principals.admin.password=verysecret
pinot.broker.access.control.principals.user.password=secret
pinot.broker.access.control.principals.user.tables=baseballStats,otherstuff
```

{% hint style="info" %}
If `*.principals.<user>.tables`is not configured, all tables are accessible to \<user>.
{% endhint %}

### Minion and ingestion jobs

Similar to any API calls, offline jobs executed via command line or minion require credentials as well if ACLs are enabled on pinot-controller. These credentials can be provided either as part of the job spec itself or using CLI arguments and as values (via **-values**) or properties (via **-propertyFile**) if Groovy templates are defined in the jobSpec.

{% tabs %}
{% tab title="Job Spec YAML" %}
```
authToken: Basic YWRtaW46dmVyeXNlY3JldA
```
{% endtab %}

{% tab title="CLI Arguments" %}
```
$ bin/pinot-admin.sh LaunchDataIngestionJob \
  -user admin -password verysecret \
  -jobSpecFile myJobSpec.yaml
```
{% endtab %}

{% tab title="CLI Token" %}
```
$ bin/pinot-admin.sh LaunchDataIngestionJob \
  -authToken "Basic YWRtaW46dmVyeXNlY3JldA" \
  -jobSpecFile myJobSpec.yaml
```
{% endtab %}

{% tab title="CLI Values" %}
```
# this requires a reference to "${authToken}" in myJobSpec.yaml!
$ bin/pinot-admin.sh LaunchDataIngestionJob \
  -jobSpecFile myJobSpec.yaml \
  -values "authToken=Basic YWRtaW46dmVyeXNlY3JldA"
```
{% endtab %}
{% endtabs %}
