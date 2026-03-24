---
description: Continuous JFR runbook for Pinot with dynamic cluster-level on/off control
---

# Continuous Java Flight Recorder (JFR)

This page is the runbook for running **continuous Java Flight Recorder (JFR)** in Pinot.

Pinot supports cluster-level runtime control through `ContinuousJfrStarter`, so operators can turn recording on/off or adjust settings without restarting Pinot processes.

## What is Java Flight Recorder (JFR)?

**Java Flight Recorder (JFR)** is a profiling and diagnostics framework built into the JDK. It records events from the JVM and application (for example CPU, memory, allocation, GC, thread, and lock events) into `.jfr` files with low production overhead.

{% hint style="info" %}
In Java 8, JFR was a commercial feature and older documentation may mention `-XX:+UnlockCommercialFeatures -XX:+FlightRecorder`. Since **Java 11**, JFR is part of OpenJDK and does not require commercial flags.
{% endhint %}

## Official deployment model

Run one long-lived recording in each Pinot JVM process (Controller, Broker, Server, Minion) and control it with `pinot.jfr.*` cluster config.

### Configure with cluster config

| Key | Default | Description |
| --- | --- | --- |
| `pinot.jfr.enabled` | `false` | Enables/disables continuous recording. |
| `pinot.jfr.configuration` | `default` | JFR settings profile (`default`, `profile`, or custom JFR config). |
| `pinot.jfr.name` | `pinot-continuous` | Recording name. |
| `pinot.jfr.dumpOnExit` | `false` | Dumps recording on JVM exit. Set to `true` for on-exit dumps; note that this may trigger repository cleanup even if `preserveRepository=true`. |
| `pinot.jfr.toDisk` | `true` | Stores recording repository on disk. |
| `pinot.jfr.maxSize` | `2GB` | Max recording size when `toDisk=true`; supports human-readable values (for example `512MB`, `2GB`) or raw bytes. |
| `pinot.jfr.maxAge` | `P7D` | Max event age (ISO-8601 duration) when `toDisk=true`. |
| `pinot.jfr.directory` | system temp directory | JFR repository directory path. Applied via the DiagnosticCommand MBean as `repositorypath`. |
| `pinot.jfr.dumpPath` | unset | Default JFR dump directory path. Applied via the DiagnosticCommand MBean as `dumppath`. |
| `pinot.jfr.preserveRepository` | `true` | Preserves the JFR repository directory after JVM exit. By default, JFR deletes the repository on exit; set this to prevent that (useful for post-mortem analysis). Applied via the DiagnosticCommand MBean as `preserve-repository`. |
| `pinot.jfr.repositoryMaxTotalSize` | `20GB` | Maximum total size for all repositories under the configured repository directory. When exceeded, older repositories are removed first. The currently active repository is always retained. |

Example:

```properties
pinot.jfr.enabled=true
pinot.jfr.configuration=default
pinot.jfr.name=pinot-continuous
pinot.jfr.dumpOnExit=false
pinot.jfr.toDisk=true
pinot.jfr.maxSize=2GB
pinot.jfr.maxAge=P7D
pinot.jfr.directory=/var/log/pinot/jfr-repository
pinot.jfr.dumpPath=/var/log/pinot/jfr-dumps
pinot.jfr.preserveRepository=true
pinot.jfr.repositoryMaxTotalSize=20GB
```

Notes:

- `configuration=default` is low-overhead and production-safe.
- Use `configuration=profile` only during active investigations.
- `maxAge` and `maxSize` cap footprint and history.
- Configuration changes are applied dynamically; Pinot restarts the active recording in-process.
- `preserveRepository` is useful for post-mortem analysis of in-flight chunks when the repository directory is shared across processes.
- `repositoryMaxTotalSize` automatically removes older repositories to maintain total size, but the active repository is always kept.

### Behavior of ContinuousJfrStarter

- Starts/stops one recording per Pinot JVM based on `pinot.jfr.enabled`.
- Reacts to `pinot.jfr.*` config updates at runtime.
- Manages JFR repository and dump paths via the DiagnosticCommand MBean (`JFR.configure repositorypath=...` and `JFR.configure dumppath=...`).
- Manages recording lifecycle via the DiagnosticCommand MBean (`JFR.start` and `JFR.stop`).
- If the DiagnosticCommand MBean is unavailable, Pinot logs a warning and skips JFR operations instead of failing startup.
- Automatically manages repository cleanup by removing older repositories when total size exceeds `repositoryMaxTotalSize`, while preserving the active repository.
- Uses standard JFR lifecycle controls (same model as JVM-native JFR), with Pinot cluster config as the control plane.

## Operational checks

List JVMs:

```bash
jcmd -l
```

Inspect recordings:

```bash
jcmd <pid> JFR.check
```

## Incident workflow

Capture a point-in-time dump without restarting the process:

```bash
jcmd <pid> JFR.dump name=pinot-continuous filename=/var/log/pinot/jfr/pinot-incident-$(date +%Y%m%d-%H%M%S).jfr
```

Take additional dumps as needed during the incident timeline.

### Alternative startup via JVM options

If you prefer static startup-only configuration, you can configure JFR in `JAVA_OPTS`:

```bash
-XX:StartFlightRecording=name=pinot-continuous,settings=default,disk=true,maxage=7d,maxsize=2g,dumponexit=false
```

Use this only when dynamic cluster-level toggling is not required.

## Handling large recordings

When a recording is too large to transfer or inspect as one file, split it:

```bash
jfr disassemble --output /tmp/jfr-chunks <file.jfr>
```

Share only relevant chunks for triage.

## Retention and tuning

- Start with `configuration=default`.
- Increase `maxAge` for longer timeline retention.
- Increase `maxSize` for high event-volume workloads.
- Configure `repositoryMaxTotalSize` and `preserveRepository` to manage disk usage and support post-mortem analysis.
- Keep host-level cleanup policies for operator-created dump files.
- Use explicit timestamped names for ad hoc dump files.

## Common pitfalls

- Assuming Pinot automatically rotates JFR dump files.
- Running without disk budget guardrails (`maxAge` and `maxSize`).
- Leaving `configuration=profile` enabled permanently.
- Not configuring `dumpPath` when frequent dumps are needed (requires manual directory management).

## Minimal operator checklist

- [ ] `pinot.jfr.enabled=true` applied in cluster config.
- [ ] `pinot.jfr.*` values validated for footprint (`toDisk`, `maxSize`, `maxAge`, `repositoryMaxTotalSize`).
- [ ] `jcmd <pid> JFR.check` validated post-deploy.
- [ ] Incident dump command tested in non-prod.
- [ ] Retention and cleanup policy applied to operator-created dump files.
- [ ] `preserveRepository=true` set if post-mortem analysis is needed.

## Related

- [Monitoring](monitoring.md) — Metrics, Prometheus, and Grafana.
- [Configuration Reference / Monitoring Metrics](../../configuration-reference/monitoring-metrics.md) — Pinot metrics reference.

## Opening and analyzing JFR files

- `jfr summary <file.jfr>` for high-level stats.
- `jfr view <file.jfr>` for aggregated views.
- `jfr print <file.jfr>` for detailed events (`--json` and `--xml` supported).
- Java Mission Control (JMC) for interactive analysis.
- `jdk.jfr.consumer.RecordingFile` for programmatic analysis.

Quick sanity check:

```bash
jfr summary /var/log/pinot/jfr/pinot-incident-20260310-120000.jfr
```

## External references

- [Package jdk.jfr (Java SE 21)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.jfr/jdk/jfr/package-summary.html) — Overview of the JFR API: defining events, controlling Flight Recorder, and the `jdk.jfr` package.
- [The `jfr` command](https://docs.oracle.com/en/java/javase/21/docs/specs/man/jfr.html) — Command-line tool to view, print, and summarize `.jfr` files (JDK 21+).
- [Using JDK Flight Recorder with Java Mission Control](https://docs.oracle.com/en/java/java-components/jdk-mission-control/9/user-guide/using-jdk-flight-recorder.html) — Recording and inspecting flights with the JMC GUI; includes an overview of JFR and how to analyze recordings.
- [JDK Mission Control (JMC) — Download](https://jdk.java.net/jmc/) — Standalone JMC build for opening and analyzing `.jfr` recordings.
- [RecordingFile (jdk.jfr.consumer)](https://docs.oracle.com/en/java/javase/21/docs/api/jdk.jfr/jdk/jfr/consumer/RecordingFile.html) — API for reading and parsing `.jfr` files programmatically.
