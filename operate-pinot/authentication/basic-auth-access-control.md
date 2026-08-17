---
description: Set up BasicAuthAccessControl for access to controller and broker
---

# Basic auth access control

## Set up tokens and user credentials

The configuration of HTTP Basic Auth in Apache Pinot distinguishes between **Tokens,** which are typically provided to service accounts, and **User Credentials**, which can be used by a human to log onto the web UI or issue SQL queries. While we distinguish these two concepts in the configuration of HTTP Basic Auth, they are fully-convertible formats holding the same authentication information. This distinction allows us to support future token-based authentication methods not reliant on username and password pairs. Currently, Tokens are merely base64-encoded username & password tuples, similar to those you can find in HTTP Authorization header values ([RFC 7617](https://tools.ietf.org/html/rfc7617)).

This is best demonstrated by example of introducing ACLs with a simple admin user setup. In order to enable authentication on a cluster without interrupting operations, we'll go these steps in sequence:

{% hint style="warning" %} In order to keep secret tokens safe in production when using Kubernetes please use [Dynamic Environment Configuration](../../reference/configuration-reference/dynamic-environment.md) {% endhint %}


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

For simplicity, we'll reuse the admin credentials as service tokens. In a production environment, you'll keep them separate.

{% tabs %}
{% tab title="Controller" %}
```
# Enable the controller to fetch segments by providing the credentials as a token
pinot.controller.segment.fetcher.auth.token=Basic YWRtaW46dmVyeXNlY3JldA

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

{% hint style="info" %}
Do not surround the token value with quotes – a common mistake.
{% endhint %}

**3. Enable ACL enforcement on the controller**

```
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.BasicAuthAccessControlFactory
```

After a controller restart, access to controller APIs requires authentication information (from internal components, external users, or the Web UI).

**4. Create users and enable ACL enforcement on the broker**

```
# the factory class property is different for the broker
pinot.broker.access.control.class=org.apache.pinot.broker.broker.BasicAuthAccessControlFactory

pinot.broker.access.control.principals=admin,user
pinot.broker.access.control.principals.admin.password=verysecret
pinot.broker.access.control.principals.user.password=secret

# No need to set READ permissions here since broker requests are read-only
```

After restarting the broker, any access to broker APIs requires authentication information as well.

Congratulations! You've successfully enabled authentication on Apache Pinot. Read on to learn more about the details and advanced configuration options.

#### Authentication with Web UI and API

Apache Pinot's Basic Auth follows the established standards for HTTP Basic Auth. Credentials are provided via an HTTP Authorization header. The pinot-controller web ui dynamically adapts to your auth configuration and will display a login prompt when basic auth is enabled. Restricted users are still shown all available ui functions, but their operations will fail with an error message if ACLs prohibit access.

The controller Swagger UI also exposes that same `Authorization` header through the standard `Authorize` dialog. Enter `Basic <token>` there once per session instead of editing each request by hand. If your deployment uses bearer tokens on the same header, the same dialog also accepts `Bearer <token>`. This only changes how Swagger documents and collects the header; Pinot's runtime authentication behavior is unchanged.

If you're using pinot's CLI clients you can provide your credentials either via dedicated username and password arguments, or as pre-serialized token for the HTTP Authorization header. Note, that while most of Apache Pinot's CLI commands support auth, not all of them have been back-fitted yet. If you encounter any such case, you can access the REST API directly, e.g. via curl.

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

#### Controller authentication and authorization

Pinot-controller has supported custom access control implementations for quite some time. We expanded the scope of this support in 0.8.0+ and added a default implementation for HTTP Basic Auth. Furthermore, the controller's web UI added support for user login workflows and graceful handling of authentication and authorization messages.

Controller Auth can be enabled via configuration in the controller properties. The configuration options allow the specification of usernames and passwords as well as optional ACL restrictions on a per-table and per-access-type (_CREATE_, _READ_, _UPDATE_, _DELETE_) basis.

The example below creates two users, _admin_ with password _verysecret_ and _user_ with password _secret_. _admin_ has full access, whereas _user_ is restricted to READ operations and, additionally, to tables named _myusertable_, _baseballStats_, and _stuff_, and to tables not named _excludedTable_ in all cases where the API calls are table-specific.

```
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.BasicAuthAccessControlFactory

controller.admin.access.control.principals=admin,user
controller.admin.access.control.principals.admin.password=verysecret
controller.admin.access.control.principals.user.password=secret
controller.admin.access.control.principals.user.tables=myusertable,baseballStats,stuff
controller.admin.access.control.principals.user.excludeTables=excludedTable
controller.admin.access.control.principals.user.permissions=READ
```

This configuration will automatically allow other pinot components to access pinot-controller with the shared _admin_ service token set up earlier.

{% hint style="info" %}
If `*.principals.<user>.tables`is not configured, all tables are accessible to \<user>.
{% endhint %}

Controller Basic Auth enforces `CREATE`, `READ`, `UPDATE`, and `DELETE` permissions for both table-specific and cluster-level endpoints. A principal with an explicit permission list is denied operations outside that list. Omitting the permission list, or configuring an empty list, preserves the legacy wildcard behavior.

Invalid credentials return HTTP `401`. Valid credentials without the required permission or table access return HTTP `403`. Table allow lists apply only when the endpoint targets a table; cluster-level endpoints use the CRUD permission declared by the endpoint.

{% hint style="warning" %}
Before rolling out cluster-permission enforcement to controllers, grant the server identity used by `pinot.server.segment.uploader.auth.token` cluster-level `CREATE` permission. Segment completion callbacks mutate controller state. If you use an action-aware custom policy, also grant that identity `COMMIT_SEGMENT`. Update the identity before upgrading controllers to prevent real-time segment commits from failing authorization.
{% endhint %}

Log-download endpoints require `READ`. The deprecated `/auth/verify` endpoint remains an exception: invalid credentials produce its legacy boolean `false` response instead of an HTTP `401`.

#### Broker authentication and authorization

Pinot-Broker, similar to pinot-controller above, has supported access control for a while now and we added a default implementation for HTTP Basic Auth. Since pinot-broker does not provide a web UI by itself, authentication is only relevant for SQL queries hitting the broker's REST API.

Broker Auth can be enabled via configuration in the broker properties, similar to the controller. The configuration options allow specification of usernames and passwords as well as optional ACL restrictions on a per-table table basis (access type is always READ). Note, that it is possible to configure a different set of users, credentials, and permissions for broker access. However, **if you want a user to be able to access data via the query console on the controller web UI,** that user must (a) share the **same username and password** on both controller and broker, and (b) have **READ permissions and table-level access**.

The example below again creates two users, _admin_ with password _verysecret_ and _user_ with password _secret_. _admin_ has full access, whereas _user_ is restricted to tables named _baseballStats_ and _otherstuff_ and to tables not named _otherExcludedTable_ .

```
# the factory class property is different for the broker
pinot.broker.access.control.class=org.apache.pinot.broker.broker.BasicAuthAccessControlFactory

pinot.broker.access.control.principals=admin,user
pinot.broker.access.control.principals.admin.password=verysecret
pinot.broker.access.control.principals.user.password=secret
pinot.broker.access.control.principals.user.tables=baseballStats,otherstuff
controller.admin.access.control.principals.user.excludeTables=otherExcludedTable
```

{% hint style="info" %}
If `*.principals.<user>.tables`is not configured, all tables are accessible to \<user>.
{% endhint %}

#### Server admin API authentication and authorization

The server admin listener can enforce its configured `AccessControlFactory` across administrative routes. Health and readiness GET endpoints (`/health`, `/health/liveness`, and `/health/readiness`) remain public. Segment and valid-document bitmap downloads continue to use table-level authorization. All other built-in and custom admin routes, including `/api/`, `/help/`, and `/swaggerui-dist/`, require administrative authorization.

Static Basic Auth requires an explicit `admin` permission. A principal that only has table `read` access cannot call administrative routes.

```properties
pinot.server.admin.access.control.factory.class=org.apache.pinot.server.access.BasicAuthAccessFactory
pinot.server.admin.access.control.principals=serverAdmin,segmentReader
pinot.server.admin.access.control.principals.serverAdmin.password=<admin-password>
pinot.server.admin.access.control.principals.serverAdmin.permissions=admin
pinot.server.admin.access.control.principals.segmentReader.password=<reader-password>
pinot.server.admin.access.control.principals.segmentReader.permissions=read
pinot.server.admin.access.control.principals.segmentReader.tables=<allowed-tables>
```

For ZooKeeper-managed Basic Auth, the authenticated user must have role `ADMIN` and component `SERVER`. When no server access-control factory is configured, `AllowAllAccessFactory` preserves the default unauthenticated behavior.

Controllers and brokers call privileged server operations, so configure their outbound service credentials before enabling server enforcement:

```properties
# controller.conf
controller.server.admin.auth.token=<base64-admin-token>

# broker.conf
pinot.broker.server.admin.auth.token=<base64-admin-token>
```

The default static provider sends these values as `Authorization: Basic <token>`. For a rolling migration, first add dedicated server admin principals, then deploy and configure controller and broker credentials, and only then enable the server access-control factory. Custom server `AccessControl` implementations must override `authorizeAdminAccess`; its compatibility default denies administrative access. Minion does not consume this server admin credential, so affected minion-to-server paths require a trusted network or an identity-injecting proxy or service mesh.

#### Minion and ingestion jobs

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
