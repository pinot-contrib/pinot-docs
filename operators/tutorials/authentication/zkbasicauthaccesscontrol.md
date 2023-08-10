---
description: Set up ZkBasicAuthAccessControl for access to controller and broker
---

# ZkBasicAuthAccessControl

{% hint style="info" %}
<mark style="color:red;">Note:</mark> Please be sure to keep your password safe, as encrypted passwords cannot be decrypted.
{% endhint %}

Apache Pinot 0.10.0+ includes built-in support for Enhanced HTTP Basic Auth using ZooKeeper. Although it is disabled by default for simplified setup, authentication and authorization can be easily added to any environment through configuration. ACLs (Access Control Lists) can be set for both API and table levels. This upgrade can be seamlessly performed in any environment without requiring replication, ensuring zero downtime.

The latest ZK Basic Auth offers the following features:

* **User Console** offers a more convenient method for changing user authentication settings
* **Hot Deployment** is supported when updating authentication information
* **Bcrypt Encryption Algorithm** is used to encrypt passwords and store them in the Helix ProperStore

ZkBasicAuthAccessControl also uses HTTP basic authentication. Enabling ZkBasicAuthAccessControl only requires adjusting the methods and procedures for user management. Both components can be protected via auth and can be configured independently. This makes it possible to separate accounts for administrative functions such as table creation from accounts that are read the contents of tables in production.

### Set up tokens and user credentials

Zk Basic auth still supports legacy tokens, which are commonly provided to service accounts, similar to BasicAuthAccessControl.

This is best demonstrated by example of introducing ACLs with a simple admin + user setup. To enable zk authentication on a cluster without interrupting operations, we'll go these steps in sequence:

**1. Default "admin" account when you start controller/broker**

```
username: admin
password: admin
```

**2. Create user in the UI**

The user roles in Pinot have been classified into "user" and "admin." Only the admin role has access to the user console page in the Pinot controller. Admin accounts are authorized to create Controller/Broker/Server users through the user console page.

**3. Distribute service tokens to pinot's components**

the same as BasicAuthControlAccess

**4. Enable ACL enforcement on the controller**

```
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.ZkBasicAuthAccessControlFactory
```

After a controller restart, any access to controller APIs requires authentication information. Whether from internal components, external users, or the Web UI.

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
