---
description: Pause and Un-pause Ingestion based on Resource Utilization
---

# Pause ingestion based on resource utilization

A new capability has been added to Pinot to pause and un-pause ingestion based on resource utilization. This feature is designed to help users manage their Pinot clusters more effectively by pausing ingestion when resource utilization exceeds a specified threshold. Ingestion is un-paused when resource utilization falls below the threshold.

## How It Works

The periodic task `ResourceUtilizationChecker` runs periodically and computes the disk usage info of the Pinot server instances. The periodic task `RealTimeSegmentValidationManager` utilizes the disk usage info captured by the `ResourceUtilizationChecker` task and pauses consumption on REALTIME tables if disk utilization is above the threshold. The `RealTimeSegmentValidationManager` task would un-pause ingestion when disk utilization falls below the threshold. The periodic task `PinotTaskManager` utilizes the disk usage info and prevents minion based task generation if disk utilization is above threshold. The `PinotTaskManager` task would allow minion based task generation when disk utilization falls below the threshold.

## Configuration

The following configurations are available to control this feature:

| Config | Default Value | Description |
| --- | --- | --- |
| controller.resource.utilization.checker.frequency | 300 | Value is in seconds. The disk utilization is computed for all Pinot servers in this frequency. Setting the value to -1 would disable the disk usage computation. |
| controller.disk.utilization.path | /home/pinot/data | Disk utilization is calculated for this path. |
| controller.disk.utilization.threshold | 0.95 | Value should be between 0 and 1. |
| controller.enable.resource.utilization.check | false | The feature is off by default. |

## Metrics

The metric `pinot_controller_resourceUtilizationLimitExceeded_Value` would be set to `1` when disk utilization is above the threshold. The metric would be set to `0` when disk utilization is below the threshold.

## FAQs

### Is controller restart required after changing any of the configuration properties?

Yes, update the property to the desired value and restart the controller(s).

### Does ResourceUtilizationChecker run only on the lead controller?

The periodic task `ResourceUtilizationChecker` runs on all controllers. The controller periodic tasks `RealtimeSegmentValidationManager` and `PinotTaskManager` runs only on the lead controller.

### How to identify the Pinot servers that are low on disk capacity?

Grep for the keyword `Disk utilization for server` on any Pinot controller log to find the relevant servers.

## References

* [Added support to pause and resume ingestion based on resource utilization](https://github.com/apache/pinot/pull/15008)
