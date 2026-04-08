---
description: Pause and resume ingestion based on resource utilization.
---

# Pause ingestion based on resource utilization

Pinot can pause real-time ingestion when disk utilization exceeds a configured threshold, and resume it when utilization returns within limits. The same resource-utilization status is also used to skip minion task generation for affected tables.

## How It Works

The periodic task `ResourceUtilizationChecker` fetches disk-usage information from each Pinot server and stores it in the controller-side resource-utilization cache. Pinot then uses that cached status in two places:

* `RealtimeSegmentValidationManager` pauses REALTIME tables when disk utilization is above the configured threshold.
* `PinotTaskManager` skips minion task generation for tables whose servers are above the configured threshold.

When the cached status returns to `PASS`, Pinot clears the resource-utilization pause state and allows ingestion to resume. If the status is `UNDETERMINED` and the table is already paused because of resource utilization, Pinot leaves it paused until fresh disk-usage data is available.

## How disk usage is collected

The controller calls the server endpoint `GET /instance/diskUtilization` on each server instance.

In the current implementation, that endpoint always computes disk usage for the server's `instanceDataDir`. The controller still sends the configured `controller.disk.utilization.path` header, but the server endpoint ignores that header today.

## Configuration

The following controller configurations control this feature:

| Config | Default Value | Description |
| --- | --- | --- |
| controller.enable.resource.utilization.check | false | Master switch for enforcing resource-utilization checks during real-time ingestion validation and minion task generation. |
| controller.enable.all.resource.utilization.checkers | true | Registers all resource-utilization checkers for backward compatibility. |
| controller.enable.disk.utilization.checker | false | Registers the disk-utilization checker when `controller.enable.all.resource.utilization.checkers` is `false`. |
| controller.resource.utilization.checker.frequency | 300 | Checker frequency in seconds. Setting this value to `-1` disables the periodic checker task. |
| controller.resource.utilization.checker.initial.delay | 300 | Initial delay in seconds before the checker runs. If `controller.resource.utilization.checker.collect.usage.at.startup=true`, Pinot forces this value to `0`. |
| controller.resource.utilization.checker.collect.usage.at.startup | false | When enabled, the controller waits for the checker cache to be populated before reporting itself healthy. If the startup collection times out, the controller still becomes healthy (fail-open). |
| controller.disk.utilization.threshold | 0.95 | Disk-usage threshold, expressed as a fraction between 0 and 1. |
| controller.disk.utilization.check.timeoutMs | 30000 | Timeout in milliseconds for collecting disk-usage responses from servers. |
| controller.disk.utilization.path | /home/pinot/data | Compatibility config sent by the controller when requesting disk usage. The current server endpoint ignores this value and always measures `instanceDataDir`. |

## Metrics

The gauge `pinot_controller_resourceUtilizationLimitExceeded_Value` is set to `1` when resource utilization is above the threshold for a table, and reset to `0` when the table is back within limits.

## FAQs

### Is controller restart required after changing any of the configuration properties?

Yes. Update the property to the desired value and restart the controller(s).

### Does ResourceUtilizationChecker run only on the lead controller?

The periodic task `ResourceUtilizationChecker` runs on all controllers. The controller periodic tasks `RealtimeSegmentValidationManager` and `PinotTaskManager` run only on the lead controller.

### How to identify the Pinot servers that are low on disk capacity?

Search the controller logs for the message prefix `Disk utilization for server` to find the relevant instances.

## References

* [Added support to pause and resume ingestion based on resource utilization](https://github.com/apache/pinot/pull/15008)
