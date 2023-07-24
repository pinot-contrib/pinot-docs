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
* **Bcrypt Encryption Algorithm** is utilized to encrypt passwords and store them in the Helix ProperStore


ZkBasicAuthAccessControl also utilizes HTTP basic authentication. Enabling ZkBasicAuthAccessControl only requires adjusting the methods and procedures for user management.
Both components can be protected via auth and even be configured independently. This makes it is possible to separate accounts for administrative functions such as table creation from accounts that are read the contents of tables in production.


### Tokens and User Credentials

Zk Basic auth still supports legacy tokens, which are commonly provided to service accounts, similar to BasicAuthAccessControl.

This is best demonstrated by example of introducing ACLs with a simple admin + user setup. In order to enable zk authentication on a cluster without interrupting operations, we'll go these steps in sequence:

**1. Default "admin" account when you start controller/broker**
```
username: admin
password: admin
```

**2. Create user in the UI**

The user roles in Pinot have been classified into "user" and "admin." Only the admin role has access to the user console page in the Pinot controller. Admin accounts are authorized to create Controller/Broker/Server users through the user console page.

![](<../../.gitbook/assets/zk-basic-auth-access-control.png>)
**2. Distribute service tokens to pinot's components**

the same as BasicAuthControlAccess

**3. Enable ACL enforcement on the controller**

```
controller.admin.access.control.factory.class=org.apache.pinot.controller.api.access.ZkBasicAuthAccessControlFactory
```

After a controller restart, any access to controller APIs requires authentication information. Whether from internal components, external users, or the Web UI.

**4. Enable ACL enforcement on the Broker**

```
# the factory class property is different for the broker
pinot.broker.access.control.class=org.apache.pinot.broker.broker.ZkBasicAuthAccessControlFactory
```

After restarting the broker, any access to broker APIs requires authentication information as well.

Congratulation! You've successfully enabled authentication on Apache Pinot. Read on to learn more about the details and advanced configuration options.

### Authentication with Web UI and API

the same as BasicAuthControlAccess

### Minion and ingestion jobs

the same as BasicAuthControlAccess