# Amazon EKS (Kafka)

## If you need to connect non-EKS AWS jobs (Lambdas/EC2) to a Kafka running inside an AWS EKS&#x20;

General steps: update Kafka's `advertised.listeners` and make sure Kafka is accessible (e.g. allow inputs on Security Groups).

You will probably face the following problems.

{% hint style="warning" %}
&#x20;If you want to connect to Kafka outside of EKS, you will need to change `advertised.listeners`.  When a client connects to a single Kafka bootstrap server (like other brokers), a bootstrap server sends a list of addresses for all brokers to the client.  If you want to connect to a EKS Kafka, these default values will not be correct.  This [post](https://rmoff.net/2018/08/02/kafka-listeners-explained/) provides an excellent explanation of the field.
{% endhint %}

{% hint style="info" %}
If you use Helm to deploy Kafka to AWS EKS, review the [chart's README](https://github.com/helm/charts/tree/master/incubator/kafka).  It describes multiple setups for communicating into EKS.
{% endhint %}

{% hint style="warning" %}
Running `helm upgrade` on the Kafka chart does not always update the pods.  The exact reason is unknown.  It's probably an issue with the chart's implementation.  You should run `kubectl describe pod` and other commands to see the current status of the pods.  During initial development, you can run `helm uninstall` and then `helm install`to force the values to update.&#x20;
{% endhint %}
