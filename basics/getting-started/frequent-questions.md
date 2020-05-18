---
description: >-
  This page has a collection of frequently asked questions with answers from the
  community.
---

# Frequent questions

{% hint style="info" %}
This is a list of frequent questions most often asked in our troubleshooting channel on Slack. Please feel free to contribute your questions and answers here and make a pull request.
{% endhint %}

### Do replica groups work for real-time? <a id="docs-internal-guid-3eddb872-7fff-0e2a-b4e3-b1b43454add3"></a>

Yes, replica groups work implicitly for realtime. There is no config needed. All you have to do is ensure the number of servers is a multiple of numReplicas. The partitions get uniformly sprayed across the servers, creating replica groups.  
  
For example, consider we have 6 partitions, 2 replicas, and 4 servers.

|  | r1 | r2 |
| :--- | :--- | :--- |
| p1 | S0 | S1 |
| p2 | S2 | S3 |
| p3 | S0 | S1 |
| p4 | S2 | S3 |
| p5 | S0 | S1 |
| p6 | S2 | S3 |

As you can see, the set \(S0, S2\) contains r1 of every partition, and \(s1, S3\) contains r2 of every partition. The query will only be routed to one of the sets, and not span every server.

