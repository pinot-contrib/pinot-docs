---
description: Continuous JFR runbook for Pinot with dynamic cluster-level on/off control
---

# Continuous Java Flight Recorder (JFR)

This page is the runbook for running **continuous Java Flight Recorder (JFR)** in Pinot.

Pinot supports cluster-level runtime control through `ContinuousJfrStarter`, so operators can turn recording on/off or adjust settings without restarting Pinot processes. The JVM options own the repository, so the data of a crashed JVM can survive a restart.

## What is Java Flight Recorder (JFR)?

**Java Flight Recorder (JFR)** is a profiling and diagnostics framework built into the JDK. It records events from the JVM and application (for example CPU, memory, allocation, GC, thread, and lock events) into `.jfr` files with low production overhead.

{% hint style="info" %}
In Java 8, JFR was a commercial feature and older documentation may mention `-XX:+UnlockCommercialFeatures -XX:+FlightRecorder`. Since **Java 11**, JFR is part of OpenJDK and does not require commercial flags.
{% endhint %}

## Official deployment model

Run one long-lived recording in each Pinot JVM process (Controller, Broker, Server, Minion) and control it with `pinot.jfr.*` cluster config.

The responsibility is split in two:

- **The JVM** owns the options that are global to the process: the repository directory, `preserve-repository`, the dump path and the chunk size. Set them with `-XX:FlightRecorderOptions` in the JVM options.
- **Pinot** owns the options of one recording, from the `pinot.jfr.*` cluster configs. It starts, stops and changes the recording at runtime, without a restart.

### Configure the repository with JVM options

By default, the JVM writes the recording to a repository in the temporary directory, and deletes it when the JVM exits. To keep the data of a JVM that crashed or was killed, put the repository on a persistent disk:

```bash
-XX:FlightRecorderOptions:repository=/var/pinot/jfr,preserve-repository=true,dumppath=/var/pinot/jfr
```

- `repository`: the directory of the repository. The JVM creates one subdirectory for each run, named `<yyyy_MM_dd_HH_mm_ss>_<pid>`.
- `preserve-repository=true`: keeps the repository after the JVM exits.
- `dumppath`: the directory for the emergency dump of a crash (`hs_err_pid<pid>.jfr`) and for the `dumpOnExit` files. Without it, the JVM writes them to its working directory.

Put all the options in one `-XX:FlightRecorderOptions` flag. The JVM does not merge two of these flags: the last one replaces the first one.

{% hint style="warning" %}
The JVM does not delete the run directories of old runs when `preserve-repository=true`. Delete them outside the JVM, for example with a script that runs before the JVM starts. Each run directory holds up to two times `pinot.jfr.maxSize`: the running recording, and the recording that Pinot saves when it stops the recording.
{% endhint %}

### Configure the recording with cluster config

| Key | Default | Description |
| --- | --- | --- |
| `pinot.jfr.enabled` | `false` | Enables or disables continuous recording. |
| `pinot.jfr.instanceRegex` | unset | A regular expression that selects the instances that record. It must match the full instance ID, for example `Server_.*` or `(Broker\|Controller)_.*`. If it is not set, all instances record. If it is not a valid regular expression, each instance logs an error and keeps its current state. |
| `pinot.jfr.configuration` | `default` | JFR settings profile (`default`, `profile`, or the path of a custom `.jfc` file). |
| `pinot.jfr.name` | `pinot-continuous` | Recording name. |
| `pinot.jfr.dumpOnExit` | `false` | Dumps the recording to a file in `dumppath` when the JVM exits. With `preserve-repository=true`, the repository keeps the same data, so this option is usually not necessary. |
| `pinot.jfr.toDisk` | `true` | Stores the recording in the repository on disk. If `false`, the recording stays in memory. |
| `pinot.jfr.maxSize` | `2GB` | Max recording size when `toDisk=true`; supports human-readable values (for example `512MB`, `2GB`) or raw bytes. |
| `pinot.jfr.maxAge` | `P7D` | Max event age (ISO-8601 duration) when `toDisk=true`. |

Example:

```properties
pinot.jfr.enabled=true
pinot.jfr.instanceRegex=Server_.*
pinot.jfr.configuration=default
pinot.jfr.name=pinot-continuous
pinot.jfr.toDisk=true
pinot.jfr.maxSize=2GB
pinot.jfr.maxAge=P7D
```

Notes:

- `configuration=default` is low-overhead and production-safe.
- Use `configuration=profile` only during active investigations.
- `maxAge` and `maxSize` cap footprint and history.
- Configuration changes are applied dynamically. Pinot changes the options of the running recording. Only a change of `toDisk` starts a new recording.

{% hint style="info" %}
Older versions also read `pinot.jfr.directory`, `pinot.jfr.dumpPath`, `pinot.jfr.preserveRepository`, `pinot.jfr.repositoryMaxTotalSize` and `pinot.jfr.maxDumps`. Pinot now ignores these keys and logs a warning for each one. Use the `-XX:FlightRecorderOptions` options above, and delete old run directories outside the JVM.
{% endhint %}

### Behavior of ContinuousJfrStarter

- Each Pinot component (Controller, Broker, Server, Minion) runs its own recording. Components that run in the same JVM, for example in a quickstart, run one recording each, with the same name.
- Reacts to `pinot.jfr.*` config updates at runtime, through the `jdk.jfr` API.
- When Pinot stops a recording (for example `enabled=false`, or `instanceRegex` no longer matches), it first saves the recording to `<name>-<timestamp>.jfr` in the run directory of the repository. Each component keeps only its last saved recording.
- When the component stops while the JVM shuts down, Pinot leaves the recording to the JVM, so that `dumpOnExit` still works.
- If the JVM starts with `-XX:StartFlightRecording`, Pinot ignores the `pinot.jfr.*` cluster configs and logs a warning, because the JVM flags own the recording.

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
- Set `preserve-repository=true` and a persistent `repository` to keep the data of a crashed JVM.
- Delete the run directories of old runs outside the JVM. Keep more than the newest one, because in a crash loop the run that crashed first is not the newest one.
- Keep host-level cleanup policies for operator-created dump files.
- Use explicit timestamped names for ad hoc dump files.

## Read the data of a crashed or killed JVM

- **Crash** (for example `-XX:+CrashOnOutOfMemoryError`): the JVM writes `hs_err_pid<pid>.jfr` to `dumppath`. Read it directly.
- **Kill** (`SIGKILL`, a container OOM kill): there is no dump. The newest chunk of the run directory is not complete, and `jfr` cannot read it. Put the other chunks in a directory, then run `jfr assemble <directory> <file.jfr>`.
- **Stop through the cluster config**: read the `<name>-<timestamp>.jfr` file that Pinot saved in the run directory.

## Common pitfalls

- Assuming Pinot automatically rotates JFR dump files.
- Running without disk budget guardrails (`maxAge` and `maxSize`).
- Leaving `configuration=profile` enabled permanently.
- Setting `-XX:FlightRecorderOptions` twice, for example in two environment variables. The last flag replaces the first one.
- Keeping the repository in the temporary directory, where the data of a crashed JVM does not survive a container restart.

## Minimal operator checklist

- [ ] `-XX:FlightRecorderOptions:repository=...,preserve-repository=true,dumppath=...` set in the JVM options, if post-mortem analysis is needed.
- [ ] A cleanup of old run directories in the repository.
- [ ] `pinot.jfr.enabled=true` applied in cluster config.
- [ ] `pinot.jfr.*` values validated for footprint (`toDisk`, `maxSize`, `maxAge`).
- [ ] `jcmd <pid> JFR.check` validated post-deploy.
- [ ] Incident dump command tested in non-prod.
- [ ] Retention and cleanup policy applied to operator-created dump files.

## Related

- [Monitoring](monitoring.md) — Metrics, Prometheus, and Grafana.
- [Configuration Reference / Monitoring Metrics](../reference/configuration-reference/monitoring-metrics.md) — Pinot metrics reference.

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
