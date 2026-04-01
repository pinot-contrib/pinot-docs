---
description: Index of design documents and how to propose new ones
---

# Design Documents

Design documents capture the motivation, technical approach, and trade-offs behind significant changes to Apache Pinot. They serve as a permanent record so that contributors and operators can understand why a feature works the way it does.

## Purpose

* **Alignment** -- A design doc lets the community review the approach before code is written, reducing rework.
* **Onboarding** -- New contributors can read design docs to understand the reasoning behind major subsystems.
* **Auditability** -- Design docs provide a historical record of architectural decisions.

## When to write a design document

Write a design doc when your change involves any of the following:

* A new major feature or subsystem (for example, a new index type, a new query engine phase, or a new ingestion path)
* A significant change to an existing subsystem that alters its behavior or data format
* A cross-component change that affects multiple Pinot services (controller, broker, server, minion)
* A public API change that affects backward compatibility

Bug fixes, small enhancements, and documentation changes typically do not need a design doc.

## How to propose a design document

1. **Open a GitHub issue** describing the problem and proposed solution at a high level. Label it with `design-doc` or `PEP` (Pinot Enhancement Proposal).
2. **Write the design doc** in a Google Doc (or equivalent) and share it with the Pinot dev mailing list (`dev@pinot.apache.org`). Include:
   * Problem statement and motivation
   * Proposed design with diagrams where helpful
   * API or configuration changes
   * Alternatives considered
   * Rollout and backward-compatibility plan
3. **Collect feedback** from reviewers on the doc and the GitHub issue.
4. **Update this page** by adding a row to the index table below once the design is accepted.
5. **Implement** the feature following the [Contribution Guidelines](../developers-and-contributors/contribution-guidelines.md).

## Design document index

### In-repo design docs

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Segment Writer API](segment-writer-api.md)</td>
      <td>API for programmatically building Pinot segments without a full batch ingestion job</td>
    </tr>
  </tbody>
</table>

### 2025

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Authors</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[NGram Filtering Index](https://docs.google.com/document/d/1FG1adOh9YGuePnX43maR2m3I5TpnEmQ6sU4fGtuCnh0/)</td>
      <td>Ting Chen, Qiaochu Liu</td>
      <td>Aug 2025</td>
    </tr>
  </tbody>
</table>

### 2024

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Authors</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Reuse common expressions in a query](https://docs.google.com/document/d/1HQhbpU8x4mcdt0mTEptOiu2cABNwrVUQXTh_nNB2pH8)</td>
      <td>Gonzalo Ortiz</td>
      <td>Sep 2024</td>
    </tr>
  </tbody>
</table>

### 2022

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Authors</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Peer downloading for offline segments](https://docs.google.com/document/d/1HtU8NsYz84NiAKGh16Yv8WKxyhdXHx-KNsINcWZ7MEI/edit?usp=sharing)</td>
      <td>Xuanyi Li</td>
      <td>Nov 2022</td>
    </tr>
    <tr>
      <td>[Segment format without forward index](https://docs.google.com/document/d/1MNLLhYCg5e-UFBQ6wTBODd41sDsbjevwRfwoGuNowWw/edit#heading=h.jwlk6va28akf)</td>
      <td>Sonam Mandal</td>
      <td>Oct 2022</td>
    </tr>
    <tr>
      <td>[Runtime query killing](https://docs.google.com/document/d/1Z9DYAfKznHQI9Wn8BjTWZYTcNRVGiPP0B8aEP3w_1jQ/edit#heading=h.o3jia8j0k10u)</td>
      <td>Jia Guo</td>
      <td>Oct 2022</td>
    </tr>
    <tr>
      <td>[Forward Index Handler in Segment Reload](https://docs.google.com/document/d/1Gai0DHBnyR4joG_8AcoR-27_exEBTpVfTFU04HyPdd8/edit#heading=h.liwwtls82n1z)</td>
      <td>Vivek Iyer</td>
      <td>Sep 2022</td>
    </tr>
    <tr>
      <td>[Support multiple data directories for Pinot server](https://docs.google.com/document/d/1B_8k2XGMrxfFAo_g-MEjEPGj84Xy8YW4-yUiZ2BQkuE/edit#heading=h.2ic29gs71g43)</td>
      <td>Xiaobing Li</td>
      <td>Aug 2022</td>
    </tr>
    <tr>
      <td>[Reload status API](https://docs.google.com/document/d/1Eqn2FDDIhCr8G2JFlifs5FjT0LsVPfpPTpdJIJvorwI/edit?usp=sharing)</td>
      <td>Saurabh Dubey</td>
      <td>Aug 2022</td>
    </tr>
    <tr>
      <td>[Deduplication during real-time ingestion](https://docs.google.com/document/d/17sOSRQ1slff30z7jDc0ec5qKwv0xSfPkDjpMOY07POQ/edit?usp=sharing)</td>
      <td>Saurabh Dubey</td>
      <td>June 2022</td>
    </tr>
    <tr>
      <td>[Adaptive Server Selection](https://docs.google.com/document/d/1w8YVpKIj0S62NvwDpf1HgruwxJYJ6ODuKQLjGXupH8w/edit#heading=h.u87pirlgxhmf)</td>
      <td>Vivek Iyer</td>
      <td>June 2022</td>
    </tr>
    <tr>
      <td>[MV column compression evaluation](https://docs.google.com/document/d/1BWtNKvxL1Uaydni_BJCgWN8i9_WeSdgL3Ksh4IpY_K0/edit)</td>
      <td>Sonam Mandal</td>
      <td>June 2022</td>
    </tr>
    <tr>
      <td>[Minimize Data Movement for Instance Assignment](https://docs.google.com/document/d/1_Fn-yNjt9Ih0SQiIqIhCEvE9BvYugvAhB4tgWH-VoWE/edit)</td>
      <td>Jialiang Li</td>
      <td>June 2022</td>
    </tr>
    <tr>
      <td>[Server Failure Detector](https://docs.google.com/document/d/1X32OMT6lC4pCveQVzK6OvRlaW0kE9HZ2vn_EHzesM1w/edit?usp=sharing)</td>
      <td>Jackie Jiang</td>
      <td>Apr 2022</td>
    </tr>
    <tr>
      <td>[Generalized Pre-Aggregation](https://docs.google.com/document/d/17nMXwmDa7-eopzSaQ4XhbfnbF7myQMzDshanSPXLK0s/edit?usp=sharing)</td>
      <td>Evan Noon</td>
      <td>Mar 2022</td>
    </tr>
    <tr>
      <td>[Multi-stage Query Engine](https://docs.google.com/document/d/10-vL_bUrI-Pi2oYudWyUlQl9Kf0cLrW-Z8hGczkCPik/edit?usp=sharing)</td>
      <td>Rong Rong</td>
      <td>Feb 2022</td>
    </tr>
    <tr>
      <td>[Pause/Resume Stream](https://docs.google.com/document/d/1uuXuif0SfMTnH3ykfuzXXNjh-LyszjilodD_mdlilZg/edit)</td>
      <td>Sajjad Moradi, Subbu Subramaniam</td>
      <td>Feb 2022</td>
    </tr>
    <tr>
      <td>[Fault Domain Awareness](https://docs.google.com/document/d/1KmJ1DsYXVdzrojj_JYBHRJ2gRMQ5y-o63YqPs7ei7nI/edit)</td>
      <td>Jia Guo, Sidd</td>
      <td>Feb 2022</td>
    </tr>
    <tr>
      <td>[Pinot Flink Connector](https://docs.google.com/document/d/1GVoFHOHSDPs1MEDKEmKguKwWMqM1lwQKj2e64RAKDf8/edit#heading=h.uvocz0dwkepo)</td>
      <td>Yupeng Fu</td>
      <td>Jan 2022</td>
    </tr>
    <tr>
      <td>[Pluggable Indexes](https://docs.google.com/document/d/1Slu7klgQn_3RcEJWUuHq9AF0v5ZDA9M2Y0dy8iqrtLQ/edit)</td>
      <td>Richard Startin</td>
      <td>Jan 2022</td>
    </tr>
    <tr>
      <td>[Petabyte-Scale Log Storage and Search in Pinot with CLP](https://docs.google.com/document/d/1nHZb37re4mUwEA258x3a2pgX13EWLWMJ0uLEDk1dUyU/edit#heading=h.j0al1jpfd8eb)</td>
      <td>Ting Chen</td>
      <td>Dec 2022</td>
    </tr>
  </tbody>
</table>

### 2021

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Authors</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Improve raw variable length forward index format](https://docs.google.com/document/d/1Y7MyQGmDD2fI7brOOFQtToxd8ML837qRuc3IlNYFvCw/edit)</td>
      <td>Richard Startin</td>
      <td>Nov 2021</td>
    </tr>
    <tr>
      <td>[Consistent Push and Rollback](https://docs.google.com/document/d/1PUy4wSUPFyEWEW3a88Mipdug3cPj4EpV__lx-BVUTYk/edit?usp=sharing)</td>
      <td>Seunghyun Lee, Jialiang Li</td>
      <td>Nov 2021</td>
    </tr>
    <tr>
      <td>[Aggregation Filter](https://docs.google.com/document/d/1qJzG1CmyVZpLN6rdI8V0zUWEaIjQ86hDL9XwrcPKcTs/edit?usp=sharing)</td>
      <td>Atri Sharma</td>
      <td>Oct 2021</td>
    </tr>
    <tr>
      <td>[Range encoded bit-sliced indexes](https://docs.google.com/document/d/1se2OgqXJiD7r7S7U6SUmTIAApO66QIrAYosxvXHEXlw/edit)</td>
      <td>Richard Startin</td>
      <td>Sep 2021</td>
    </tr>
    <tr>
      <td>[Time Series Aggregate Functions](https://docs.google.com/document/d/1D5tyd-gFIe5QjL8XYLQmL5_traw-jtKkzeF96G3naes/edit?usp=sharing)</td>
      <td>Lakshmanan Velusamy, Weixiang Sun</td>
      <td>Sep 2021</td>
    </tr>
    <tr>
      <td>[Native Text Indices](https://docs.google.com/document/d/1PMhoRy6WF46C4d4mw0LVe9b8Vjqes6vsXZkmxXzMYzw/edit?usp=sharing)</td>
      <td>Atri Sharma</td>
      <td>Sep 2021</td>
    </tr>
    <tr>
      <td>[Geospatial Support](https://docs.google.com/document/d/1Mkm5RHS_tof-vIUt5-UNeOgRYSBAN6M_pN-hedV6Q0g/edit?usp=sharing)</td>
      <td>Yupeng Fu</td>
      <td>May 2021</td>
    </tr>
    <tr>
      <td>[Segment Writer API](https://docs.google.com/document/d/1f_JlegCkH_Zysm80maLnv7iqgWtD9uPiBLkeLmMUoNg/edit)</td>
      <td>Neha Pawar</td>
      <td>Feb 2021</td>
    </tr>
    <tr>
      <td>[Partial Upsert](https://docs.google.com/document/d/1qrTD7x23FlPrAUVIFbWs6GSBtTsztWhWgis-xr1lGMs/edit?usp=sharing)</td>
      <td>Qiaochu Liu</td>
      <td>Feb 2021</td>
    </tr>
  </tbody>
</table>

### 2020

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Authors</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Kinesis Integration in Pinot](https://docs.google.com/document/d/1hFbzumQAGALAi8XZMOsVlwVHN-s2t37MA5QUfduL4Yk/edit?usp=sharing)</td>
      <td>Neha Pawar</td>
      <td>Dec 2020</td>
    </tr>
    <tr>
      <td>[JSON Indexing](https://docs.google.com/document/d/1ZBkZUjlkTH7pA1dN_hLAUXhuP1pIo4WmtM5YXktUifg/edit?usp=sharing)</td>
      <td>Kishore Gopalakrishna</td>
      <td>Oct 2020</td>
    </tr>
    <tr>
      <td>[Lookup Join](https://docs.google.com/document/d/1InWmxbRqwcqIakzvoEWHLxtX4XR9H5L01256EbAUHV8/edit?usp=sharing)</td>
      <td>Dharak Kharod</td>
      <td>Oct 2020</td>
    </tr>
    <tr>
      <td>[Strict Replica-Group Routing](https://docs.google.com/document/d/1B5SghG0x5JHfZrKMBjiv_m3Dd969hfyWgc1joKZpJIU/edit?usp=sharing)</td>
      <td>Jackie Jiang</td>
      <td>Oct 2020</td>
    </tr>
    <tr>
      <td>[Cluster Manager UI](https://docs.google.com/document/d/1E6OWyt-NvOpbBsOH1qwi5v8DcNSgT4PTLJ21TKYIsoI/edit#heading=h.8xhj1hrxrxl)</td>
      <td>Neha Pawar</td>
      <td>Sep 2020</td>
    </tr>
    <tr>
      <td>[Pinot Upsert Revisited](https://docs.google.com/document/d/1qljEMndPMxbbKtjlVn9mn2toz7Qrk0TGQsHLfI--7h8/edit#heading=h.lsfmyoyyxtgt)</td>
      <td>Yupeng Fu</td>
      <td>Sep 2020</td>
    </tr>
    <tr>
      <td>[Use IdSet for Id Filtering](https://docs.google.com/document/d/1s6DZ9eTPqH7vaKQlPjKiWb_OBC3hkkEGICIzcd5gozc/edit?usp=sharing)</td>
      <td>Jackie Jiang</td>
      <td>Sep 2020</td>
    </tr>
    <tr>
      <td>[Pinot managed offline flows](https://docs.google.com/document/d/1-e_9aHQB4HXS38ONtofdxNvMsGmAoYfSnc2LP88MbIc/edit#heading=h.60ws8it8iwvp)</td>
      <td>Neha</td>
      <td>Aug 2020</td>
    </tr>
    <tr>
      <td>[Server Health Checker](https://docs.google.com/document/d/1PP_RaDuS7KGeF9RnAcRFJRCA8aCVxxVLTJn-c3hg9qQ/edit)</td>
      <td>Chinmay</td>
      <td>Aug 2020</td>
    </tr>
    <tr>
      <td>[HAVING and Post-Aggregation Support](https://docs.google.com/document/d/1Dg1KXpxIdl75Tsg2YFCYVeE8sMAIj64ZWoxDcj1cHwo/edit?usp=sharing)</td>
      <td>Jackie Jiang</td>
      <td>July 2020</td>
    </tr>
    <tr>
      <td>[Segment Merge and Rollup (Updated)](https://docs.google.com/document/d/1-AKCfXNXdoNjFIvJ87wjWwFM_38gS0NCwFrIYjYsqp8/edit)</td>
      <td>Seunghyun</td>
      <td>June 2020</td>
    </tr>
    <tr>
      <td>[Filtering during ingestion](https://docs.google.com/document/d/1Cahnas3nh0XErETH0KHLaecN6xCnRVYWNKO3rDn7qcI/edit)</td>
      <td>Neha</td>
      <td>June 2020</td>
    </tr>
    <tr>
      <td>[Segment Preprocessing Hadoop Job](https://docs.google.com/document/d/1BnjjVj3OLuo-vmOt0WjqEFbUC9AZgCDuDxCtLEFPM34/edit?usp=sharing)</td>
      <td>Jialiang Li</td>
      <td>May 2020</td>
    </tr>
    <tr>
      <td>[Flattening during ingestion](https://docs.google.com/document/d/1IYCsYCgGn6YMWTDG4-i61Hxbtnac2dCuhvDKUZIxDYg/edit?usp=sharing)</td>
      <td>Neha</td>
      <td>May 2020</td>
    </tr>
    <tr>
      <td>[Compatibility Regression Testing](https://docs.google.com/document/d/1yNlvnLKDNUuyRWOKYYF01FWW9weYMGoaLRtU-CueciM/edit#heading=h.sbzlx23tnq14)</td>
      <td>Subbu</td>
      <td>May 2020</td>
    </tr>
    <tr>
      <td>[Refactor pinot-core and pinot-common](https://docs.google.com/document/d/1urROfQZuTE8JJmW3IMCeB2i3FYoEyG1TCyPsxvSaNuw/edit?usp=sharing)</td>
      <td>Kishore</td>
      <td>May 2020</td>
    </tr>
    <tr>
      <td>[Range Indexing in Pinot](https://docs.google.com/document/d/1eisu7L-ERLs1OZCASOz3qSpzZfoipplKrYgmBXaFobw/edit?usp=sharing)</td>
      <td>Kishore</td>
      <td>Apr 2020</td>
    </tr>
    <tr>
      <td>[Deprecate TimeFieldSpec, make DateTimeFieldSpec mainstream](https://docs.google.com/document/d/1SU1jCjfsIDSA960fD5YWQbD72p8UdGF0c7CroFNt9Ho/edit#heading=h.qeqkd3x33xzp)</td>
      <td>Neha</td>
      <td>Apr 2020</td>
    </tr>
    <tr>
      <td>[Geospatial support in Pinot](https://docs.google.com/document/d/1Mkm5RHS_tof-vIUt5-UNeOgRYSBAN6M_pN-hedV6Q0g/edit?ts=5ea0b8d4#heading=h.i45os595j1sp)</td>
      <td>Yupeng Fu</td>
      <td>Apr 2020</td>
    </tr>
    <tr>
      <td>[Column transformation during ingestion](https://docs.google.com/document/d/13BywJncHrLAFLm-qy4kfKaPxXfAg9XE5v3_fk9sGVSo/edit?usp=sharing)</td>
      <td>Neha</td>
      <td>Mar 2020</td>
    </tr>
    <tr>
      <td>[Tiered Storage](https://docs.google.com/document/d/1Z4FLg3ezHpqvc6zhy0jR6Wi2OL8wLO_lRC6aLkskFgs/edit?usp=sharing)</td>
      <td>Neha</td>
      <td>Mar 2020</td>
    </tr>
    <tr>
      <td>[Synthetic Data Generator for Pinot](https://cwiki.apache.org/confluence/display/PINOT/Synthetic+Data+Generator+for+Pinot)</td>
      <td>Alex Pucher</td>
      <td>Mar 2020</td>
    </tr>
  </tbody>
</table>

### 2019 and earlier

<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Authors</th>
      <th>Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>[Text Search](https://docs.google.com/document/d/19uLti7wwl7nPlDuy6cUVnLOll2C8u3YtUITbNj0TT5o/edit)</td>
      <td>Siddharth Teotia</td>
      <td>Nov 2019</td>
    </tr>
    <tr>
      <td>[Pinot SQL migration Plan](https://docs.google.com/document/d/1uNIq0cybUtVtdtJ38-4ewFNEQorbg-2KYr-CMSj6H_8/edit#heading=h.ejrg0ci2rzol)</td>
      <td>Xiang Fu</td>
      <td>Nov 2019</td>
    </tr>
    <tr>
      <td>[Segment Admin Rest APIs](https://cwiki.apache.org/confluence/display/PINOT/Segment+Admin+Rest+APIs)</td>
      <td>Jackie Jiang</td>
      <td>Nov 2019</td>
    </tr>
    <tr>
      <td>[Order By in aggregations](https://cwiki.apache.org/confluence/display/PINOT/Order+By)</td>
      <td>Neha</td>
      <td>Oct 2019</td>
    </tr>
    <tr>
      <td>[Pinot Benchmark as a Service](https://cwiki.apache.org/confluence/display/PINOT/Pinot+Benchmark+as+a+Service)</td>
      <td>Jialiang Li</td>
      <td>Sep 2019</td>
    </tr>
    <tr>
      <td>[Controller Separation between Helix and Pinot](https://cwiki.apache.org/confluence/display/PINOT/Controller+Separation+between+Helix+and+Pinot)</td>
      <td>Jialiang Li</td>
      <td>Jun 2019</td>
    </tr>
    <tr>
      <td>[Upsert](https://docs.google.com/document/d/1SFFir7ByxCff-aVYxQeTHpNhPXeP5q7P4g_6O2iNGgU/edit?usp=sharing)</td>
      <td>James</td>
      <td>Jun 2019</td>
    </tr>
    <tr>
      <td>[Pinot Freshness Metric](https://cwiki.apache.org/confluence/display/PINOT/Pinot+Freshness+Metric)</td>
      <td>Sunitha Beeram</td>
      <td>May 2019</td>
    </tr>
    <tr>
      <td>[By passing deep-store requirement for Real-time segment completion](https://cwiki.apache.org/confluence/display/PINOT/By-passing+deep-store+requirement+for+Realtime+segment+completion)</td>
      <td>Ting, Chinmay</td>
      <td>May 2019</td>
    </tr>
    <tr>
      <td>[Project Tuna: Automatic Inverted Index Recommendation](https://cwiki.apache.org/confluence/display/PINOT/Automated+Inverted+Index+Recommendation+for+Pinot)</td>
      <td>Jia Guo</td>
      <td>May 2019</td>
    </tr>
    <tr>
      <td>[Segment Completion Enhancement for deep storage support](https://cwiki.apache.org/confluence/display/PINOT/Segment+Completion+Protocol+enhancements+for+Deep+Store+support)</td>
      <td>Subbu</td>
      <td>Feb 2019</td>
    </tr>
    <tr>
      <td>[Segment Merge and Rollup](https://cwiki.apache.org/confluence/display/PINOT/Segment+Merge+and+Rollup)</td>
      <td>Seunghyun Lee</td>
      <td>2018</td>
    </tr>
    <tr>
      <td>[Pinot-Minion Service](https://docs.google.com/document/d/1kbK88fCexmEsDcFINebqLvZWtKg8CVQN4kmsLm0s9f8/edit?usp=sharing)</td>
      <td>Jackie Jiang</td>
      <td>2017</td>
    </tr>
    <tr>
      <td>[Consuming and indexing rows in real time](https://cwiki.apache.org/confluence/display/PINOT/Consuming+and+Indexing+rows+in+Realtime)</td>
      <td>Subbu</td>
      <td>2017</td>
    </tr>
    <tr>
      <td>[Partition Aware Query Routing](https://cwiki.apache.org/confluence/display/PINOT/Partition+Aware+Query+Routing)</td>
      <td>Subbu</td>
      <td>2017</td>
    </tr>
    <tr>
      <td>[Query Processing](https://cwiki.apache.org/confluence/display/PINOT/Query+Processing)</td>
      <td>Subbu</td>
      <td>2016</td>
    </tr>
    <tr>
      <td>[Expressions and UDFs](https://cwiki.apache.org/confluence/display/PINOT/Expressions+and+UDFs)</td>
      <td>Subbu</td>
      <td>2016</td>
    </tr>
  </tbody>
</table>
