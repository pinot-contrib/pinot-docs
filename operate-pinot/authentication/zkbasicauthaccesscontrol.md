---
description: Set up ZkBasicAuthAccessControl for access to controller and broker
---

# ZkBasicAuthAccessControl

{% hint style="info" %}
<mark style="color:red;">Note:</mark> Be sure to keep your password safe, as encrypted passwords cannot be decrypted.
{% endhint %}

Apache Pinot 0.10.0+ includes built-in support for Enhanced HTTP Basic Auth using ZooKeeper. Although it is disabled by default for simplified setup, authentication and authorization can be easily added to any environment through configuration. ACLs (Access Control Lists) can be set for both API and table levels. This upgrade can be seamlessly performed in any environment without requiring replication, ensuring zero downtime.

The latest ZK Basic Auth offers the following features:

* **User Console** offers a more convenient method for changing user authentication settings
* **Hot Deployment** is supported when updating authentication information
* **Bcrypt Encryption Algorithm** is used to encrypt passwords and store them in the Helix ProperStore

ZkBasicAuthAccessControl also uses HTTP basic authentication. Enabling ZkBasicAuthAccessControl only requires adjusting the methods and procedures for user management. Both components can be protected via auth and can be configured independently. This makes it possible to separate accounts for administrative functions such as table creation from accounts that are read the contents of tables in production.

### Set up tokens and user credentials

Zk Basic auth still supports legacy tokens, which are commonly provided to service accounts, similar to BasicAuthAccessControl.

Follow these steps to set up ZooKeeper-backed Basic Auth with an initial administrator and separate user accounts.

**1. Configure the initial administrator and start the controller**

```properties
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.ZkBasicAuthAccessControlFactory
access.control.init.username=admin
access.control.init.password=<set-a-strong-password>
```

On first startup with an empty ZooKeeper user store, the controller requires a nonblank `access.control.init.password` and uses it to create administrator entries for the controller, broker, and server. Set the password through your deployment's secret management, and replace the placeholder before starting. `access.control.init.username` is optional and defaults to `admin`.

These settings only apply to initialization. If the user store already contains users, changing the bootstrap settings does not update those accounts. Use the user console or user-management API to rotate credentials.

**2. Create user in the UI**

The user roles in Pinot have been classified into "user" and "admin." Only the admin role has access to the user console page in the Pinot controller. Admin accounts are authorized to create Controller/Broker/Server users through the user console page.

**3. Distribute service tokens to pinot's components**

the same as BasicAuthControlAccess

**4. Verify ACL enforcement on the controller**

With the factory configured in step 1, internal components, external users, and the Web UI must authenticate to access controller APIs.

The controller applies each user's CRUD permissions to cluster-level endpoints as well as table-specific endpoints. An explicit permission list is restrictive; an empty permission list retains legacy wildcard access. Invalid credentials return HTTP `401`, while an authenticated user without the required permission receives HTTP `403`. Before upgrading controllers, follow the [segment-uploader rolling upgrade requirement](basic-auth-access-control.md#controller-authentication-and-authorization).

**5. Enable ACL enforcement on the Broker**

```
# the factory class property is different for the broker
pinot.broker.access.control.class=org.apache.pinot.broker.broker.ZkBasicAuthAccessControlFactory
```

After restarting the broker, any access to broker APIs requires authentication information as well.

Congratulations! You've successfully enabled authentication on Apache Pinot. Read on to learn more about the details and advanced configuration options.

### Authentication with Web UI and API

See [Authentication with Web UI and API](basic-auth-access-control.md#authentication-with-web-ui-and-api).

### Minion and ingestion jobs

See [Minion and ingestion jobs](basic-auth-access-control.md#minion-and-ingestion-jobs).
