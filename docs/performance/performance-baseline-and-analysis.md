# Performance Baseline, Bottleneck Review and Test Methodology

## Scope and limitations

All figures in this document come from small VMware lab runs using three Cassandra 4.1.12 nodes with approximately 3–3.5 GiB RAM each. They are historical observations, not repeatable capacity guarantees, production SLAs or proof that one configuration is faster than another. Test conditions, workload code and measurement boundaries differed between runs.

## Recorded application benchmark observations

| Test record | Consistency / cluster state | Rows requested | Successful / failed | Workload duration | Reported TPS | Average latency | P50 | P95 | P99 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Early generator test | Consistency not documented | 1,000 | Not separately reported | 6.063 s | 164.94 | 6.063 ms elapsed/row* | Not measured | Not measured | Not measured |
| Instrumented benchmark | Historical run, consistency not specified in that record | 1,000 | 1,000 / 0 | 16.722 s inserts; 17.063 s total | 59.8 | 16.311 ms | 9.133 ms | 47.644 ms | 104.218 ms |
| Later baseline A | LOCAL_ONE | 1,000 | 1,000 / 0 | 42.494 s | 23.53 | 41.719 ms | 23.552 ms | 136.155 ms | 231.408 ms |
| Later baseline B | LOCAL_QUORUM | 1,000 | 1,000 / 0 | 40.609 s | 24.63 | 39.831 ms | 15.039 ms | 159.968 ms | 399.826 ms |
| Controlled outage workload, 16 Nov 2026 | LOCAL_QUORUM, LAB2 stopped; LAB1 and LAB3 available | 1,000 | 1,000 / 0 | 7.393 s | 135.27 | 7.062 ms | 5.985 ms | 12.318 ms | 21.048 ms |

* The early 6.063 ms number is total elapsed time divided by 1,000 rows. It includes generator/setup/shutdown overhead and is not a clean per-request latency measurement.

### How to interpret the benchmark history

- The early 164.94 TPS run is not directly comparable with the later 59.8 TPS or 23–25 TPS measurements. The instrumentation and measurement boundaries changed.
- LOCAL_ONE and LOCAL_QUORUM runs had different percentile behaviour. The LOCAL_QUORUM average was slightly lower in that particular run, while its P99 was higher. This single-run result does not establish that LOCAL_QUORUM is faster.
- The node-outage run reported higher throughput and lower latency than the later baseline runs. This must not be interpreted as an outage improving Cassandra performance. The runs were not controlled or repeated under identical CPU, memory, cache, client, data-volume and background-task conditions.
- All recorded application runs shown above had 1,000 successful inserts and zero failures where success/failure counters were captured.

## Table-level Cassandra metrics captured through nodetool

One custom-metrics snapshot recorded the following average table metrics:

| Node | Read latency | Write latency |
|---|---:|---:|
| LAB1 (192.168.62.134) | 7.722 ms | 0.338 ms |
| LAB2 (192.168.62.135) | 19.821 ms | 0.208 ms |
| LAB3 (192.168.62.136) | 5.127 ms | 0.306 ms |

The read sample counts were small. LAB2's higher observed read average was not sufficient evidence to declare a performance incident or assign a root cause. No corrective performance change was made based on this snapshot.

**Important metric distinction:** `nodetool tablestats` read/write latency values are table-level averages. They are not the Python application's request-level P50/P95/P99 percentiles.

## Monitoring scrape performance

- The JMX Exporter endpoint response was approximately 1.2 MB and took several seconds in the recorded observation.
- The recorded Prometheus JMX scrape interval was 30 seconds and timeout was 20 seconds.
- This is an observability payload/scrape-cost consideration. The retained evidence does not show a confirmed scrape timeout incident or prove it caused a database workload slowdown.
- The custom Cassandra metrics were collected centrally from LAB1 using SSH to the other nodes. The metrics file was manually generated successfully; a scheduled timer was proposed but not verified as deployed.

## Capacity and resource constraints

- VJC9LAB1 had approximately 3.5 GiB RAM; LAB2 and LAB3 approximately 3 GiB each.
- At one pre-repair check on LAB1: available memory was approximately 1.2 GiB and swap use approximately 6 MiB. Root filesystem showed 51 GiB available at that check.
- During restore, SSTableLoader warned that only about 50.963 GiB was free across data volumes. Streaming nevertheless completed at 100%; the warning was a capacity observation, not a reported loader failure.
- Repair can consume CPU, memory, disk I/O and network bandwidth. The actual repair was run sequentially with one job thread.
- Do not run multiple heavy database workloads, repairs, restores or compactions concurrently on these small VMs.

## Performance troubleshooting already performed

### Workload instrumentation improvement
The transaction insert code was expanded to report requested/successful/failed counts, connection/preparation time, workload time, TPS, average latency and P50/P95/P99 latency. This corrected a weakness in the early benchmark, where elapsed time divided by rows was incorrectly easy to interpret as request latency.

### Cassandra health/queue inspection
During the failure-recovery exercise:
- `nodetool tpstats` showed Active 0 and Pending 0 for the listed pools, including MutationStage, ReadStage, CompactionExecutor, Repair-Task and AntiEntropyStage.
- Dropped-message counters shown were zero.
- `nodetool compactionstats` showed 0 pending tasks before/after the repair check.
- `nodetool gcstats`, `proxyhistograms`, `tablestats` and JVM/host metrics form part of the DBA diagnostic toolkit, but not every one was captured for each benchmark run.

These checks are useful snapshots, not a complete proof that no latency bottleneck existed during every application test.

## Recommended repeatable benchmark protocol – pending

A future comparison should hold these variables constant:

1. Same Cassandra version, three-node state, schema, RF, JVM settings and data volume.
2. Same Python application build, Python driver version, prepared query and synthetic payload distribution.
3. Fixed consistency level for each comparison; run LOCAL_ONE and LOCAL_QUORUM as separate experiments.
4. Fixed concurrency and request count; record client host and background tasks.
5. Warm-up period followed by multiple measured rounds.
6. Separate connection/preparation time from insert execution time.
7. Record attempted, successful and failed operations; include exceptions and timeout counts.
8. Measure per-operation latency and report average, P50, P95 and P99.
9. Capture Cassandra `nodetool tpstats`, `compactionstats`, `gcstats`, `proxyhistograms`, table stats, OS CPU/memory/disk/network and application metrics during the same time window.
10. Repeat at least three measured rounds and report median and range, not only the best run.

## Future performance RCA checklist

When high read or write latency is observed, do not tune JVM or Cassandra immediately. Establish the impact and compare:
- Application-side latency percentiles and client timeouts.
- Read/write rates, consistency level, concurrency and partition-key distribution.
- `nodetool proxyhistograms`, `tpstats`, `tablestats`, `compactionstats` and dropped-message indicators.
- JVM heap, GC pause/time, CPU saturation, memory pressure and disk latency/utilization.
- Tombstone scans, large partitions, hot partitions, query shape and paging.
- Network RTT, packet drops and cross-node streaming/repair activity.

A performance RCA is complete only after a specific cause is supported by measurements and a controlled before/after test.
