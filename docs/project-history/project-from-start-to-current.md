# VJCLAB Project – From Initial Lab Setup to Current State

## Purpose and scope

This file is the chronological engineering record for the Live Banking Transaction Application. It consolidates the infrastructure, database, Python ingestion, monitoring, troubleshooting, performance, resilience, backup/restore and Commit Log preparation work recorded to date.

**Evidence policy:** Exact dates are used only where retained project notes identify them. Earlier milestones without reliable day-level timestamps are kept in an undated sequence. A symptom in a generic troubleshooting table is not represented as a resolved incident unless a root cause and corrective result were recorded.

## 1. Initial lab architecture and scope

The project was built as a three-node VMware lab using CentOS Stream 9, with a small memory allocation on each VM.

| VM | Address | Main responsibilities |
|---|---|---|
| VJC9LAB1 | 192.168.62.134 | Cassandra node 1, Python workload, Prometheus, Grafana, central metrics collection |
| VJC9LAB2 | 192.168.62.135 | Cassandra node 2 |
| VJC9LAB3 | 192.168.62.136 | Cassandra node 3 |

The lab includes Cassandra internode communication (7000), CQL/native transport (9042), local JMX management (7199), JMX Exporter (9404), Node Exporter (9100), Prometheus (9090) and Grafana (3000). Cassandra JMX 7199 was kept local-only; metrics ports were restricted to the required lab sources.

The objective is DBA learning with synthetic transactions. The project is not a completed production payments platform: there is no claim of customer-facing API, Kafka integration, settlement processing, production HA/SLA, or full banking correctness controls.

## 2. Linux and Cassandra foundation

- Prepared three CentOS Stream 9 VMs with 2 vCPU each and approximately 3–3.5 GiB RAM.
- Established administrative SSH from LAB1 to LAB2/LAB3 using a root-owned private key with restrictive permissions.
- Installed/operated Apache Cassandra 4.1.12 and OpenJDK 11 across all three nodes.
- Configured cluster VJCLAB, datacenter dc1, rack rack1, GossipingPropertyFileSnitch, Murmur3Partitioner and 16 tokens per node.
- Used Cassandra health and diagnostic commands including `nodetool status`, `describecluster`, `getendpoints`, `info`, `tpstats`, `compactionstats` and `tablestats`.
- Latest recorded cluster verification on 17 November 2026 showed all three nodes UN.

## 3. Banking keyspace, schema and Python workload

- Created `banking_stream` using NetworkTopologyStrategy with RF=3 in dc1.
- Created `banking_stream.bank_transactions` with transaction date and transaction UUID as the primary key and account, amount, currency, type, status, description and created timestamp attributes.
- Built the Python application under `/opt/banking-app`, using Python 3.9.25, a virtual environment, Cassandra driver 3.29.3, Faker, python-dotenv and colorama.
- Configured all three Cassandra contact points, port 9042, local DC dc1 and keyspace banking_stream.
- Implemented a driver connection layer using DCAwareRoundRobinPolicy and a transaction insert module using prepared statements. Later benchmark runs explicitly used LOCAL_QUORUM.
- Expanded the workload report to count successes/failures and report TPS, average latency and P50/P95/P99.

## 4. Host, Cassandra/JVM and application observability

- Installed Node Exporter 1.12.1 on all three VMs.
- Installed JMX Exporter 1.7.0 as a Java agent in the Cassandra JVM; it exposes metrics on port 9404 and starts/stops with Cassandra.
- Installed Prometheus 3.15.1 on LAB1, using 15-second global scrape/evaluation intervals; Cassandra JMX targets used a recorded 30-second interval and 20-second timeout. Retention was recorded as seven days.
- Installed Grafana 10.2.6 on LAB1 and configured the Prometheus datasource.
- The last earlier monitoring baseline before the lab shutdown recorded seven of seven targets UP: one Prometheus, three Node Exporters and three JMX Exporters.
- Later added custom table-level metrics based on `nodetool tablestats banking_stream`, collected centrally from LAB1 through Node Exporter's textfile collector.
- Read/write latency, read/write count and pending-flush Grafana panels were confirmed. SSTable count, dropped mutations and collection-status panels were not confirmed.
- The custom metrics script was manually executed; its one-minute systemd timer was proposed but not confirmed as installed/active.

## 5. Project start/stop operations

- Created project startup and shutdown scripts under `/usr/local/bin` on LAB1.
- The startup workflow starts/checks exporters, starts Cassandra sequentially, waits for native transport, verifies three UN nodes, then starts Prometheus and Grafana.
- The stop script's remote verification loop had a nested SSH quoting error. Cassandra drain/stop commands were executed manually on all nodes and monitoring services were stopped.
- During shutdown, systemd showed a Cassandra unit as failed with exit code 143 after a successful drain. The interpretation recorded was a SIGTERM-style exit; the correct operational action is to verify the Cassandra JVM and port 9042, not to assume the service is still running or blindly reset its state.
- The original corrected stop script deployment was not confirmed. A reference replacement was documented for review.

## 6. Error and RCA chronology

Confirmed problems and evidence-backed root causes are documented in [Issue Register – Errors, RCA and Corrective Actions](../troubleshooting/incident-rca-register.md). Highlights:

- Node Exporter and Prometheus were bound to node-specific addresses, so localhost checks failed; diagnostics of the listening socket led to use of the actual address.
- TCP/9100 was blocked by firewalld despite ping success; source-restricted rich rules were added and metrics retrieval was verified.
- Grafana's connection to Prometheus was blocked by SELinux; the persistent `grafana_can_tcp_connect_prometheus_port` boolean resolved datasource queries.
- Running the Python file directly led to `ModuleNotFoundError: src`; running it as a module from the project root resolved the import context.
- The first custom metrics script had an output redirection bug and over-broad SSTable-count parser; the temporary-file redirection, anchored parser and NaN handling corrected it.
- Shutdown verification failed because of nested SSH quoting; service stop was performed manually while the script issue remained under review.
- Snapshot transfer from LAB3 to LAB2 could not authenticate because LAB3 did not possess the needed private key; LAB1 was used as a relay without weakening key permissions.
- SSTable validation initially hard-coded LAB1's generation prefix; checking for any TOC component corrected the false missing-file report.
- The detailed RCA record also distinguishes a benign curl broken-pipe message and open Commit Log script design findings from actual runtime incidents.

## 7. Performance and workload measurements

The project has multiple 1,000-row observations. They are not directly comparable because workload version, instrumentation, run conditions and measurement boundaries changed.

| Run | Mode/condition | Observed throughput | Average | P50 | P95 | P99 |
|---|---|---:|---:|---:|---:|---:|
| Early generator run | consistency not retained | 164.94 TPS | 6.063 ms elapsed per row* | – | – | – |
| Instrumented run | historical record | 59.8 TPS | 16.311 ms | 9.133 ms | 47.644 ms | 104.218 ms |
| Baseline A | LOCAL_ONE | 23.53 TPS | 41.719 ms | 23.552 ms | 136.155 ms | 231.408 ms |
| Baseline B | LOCAL_QUORUM | 24.63 TPS | 39.831 ms | 15.039 ms | 159.968 ms | 399.826 ms |
| Node outage exercise, 16 Nov | LOCAL_QUORUM, LAB2 down | 135.27 TPS | 7.062 ms | 5.985 ms | 12.318 ms | 21.048 ms |

*The early 6.063 ms is elapsed duration divided by row count, not measured per-request latency.

The outage benchmark's higher throughput must not be interpreted as proof that taking a node down makes Cassandra faster; the runs were not controlled. The performance assessment and repeatable test protocol are documented in [Performance Baseline and Analysis](../performance/performance-baseline-and-analysis.md).

A custom table-stats snapshot showed LAB2's average read latency higher than the other nodes (19.821 ms versus 7.722 ms and 5.127 ms), but sample counts were small and no performance RCA was justified. JMX Exporter returned approximately 1.2 MB and took several seconds to scrape; that is a monitoring payload consideration, not a confirmed database slowdown.

## 8. Dated progress snapshot – 31 October 2026

The retained early project guide states that progress was captured through 31 October 2026. It records 12,100 synthetic rows for the transaction-date partition 2026-10-30; the partition date is not assumed to be the date of setup or ingestion.

- Established the three CentOS Stream 9 VM layout and Cassandra 4.1.12 cluster configuration.
- Created banking_stream and bank_transactions; a 12,100-row synthetic partition for 2026-10-30 was recorded.
- Built the Python app structure, environment configuration, driver connection module, transaction generator and prepared synchronous insert path.
- Recorded an early 1,000-row workload at 6.063 seconds (about 164.94 inserts/second). The elapsed-time-per-row number was not a clean per-request latency measurement.
- Added Node Exporter, the Cassandra JVM JMX Exporter agent, Prometheus and Grafana. The last captured pre-shutdown state showed seven Prometheus targets UP.
- Resolved Grafana-to-Prometheus SELinux network permission using the persistent grafana_can_tcp_connect_prometheus_port boolean.
- Recorded cqlsh failure through 127.0.0.1 while the private node IP worked; the original rpc_address/listener evidence was not retained.
- Recorded shutdown-script nested SSH quoting trouble and Cassandra service exit status 143 after drain; Cassandra was stopped manually and process/port verification was part of the safe-shutdown guidance.

See [31 October activity snapshot](../../daily-activity/2026-10-31.md).

- Stopped LAB2 for a controlled node outage while LAB1/LAB3 remained available.
- Inserted 1,000 transactions through Python using LOCAL_QUORUM: 1,000 successful, 0 failed.
- Restarted LAB2 and later verified all three nodes UN.
- Inspected pending hints on LAB1 only; LAB1 reported no pending hints. This does not establish hint status on the other nodes.
- Ran repair preview for the specified table; preview reported the previewed data in sync.
- Ran sequential incremental repair with one job for the specified keyspace/table; parent command and session reported success.
- Created same-tag snapshots separately on all three nodes, staged copies on LAB2, and compared checksums for LAB1 and LAB2 copies (10 files each). LAB3 checksum comparison remained unconfirmed.
- Restored SSTables into a separately created compatible target table with SSTableLoader. The selected 2026-11-15 partition count was 3,000 in both source and restore; five sample rows were inspected.
- Created and ran snapshot automation for all three nodes; all node snapshot metadata checks passed. This script does not yet implement off-host copy, retention or restore orchestration.

See [16 November daily activity](../../daily-activity/2026-11-16.md).

## 10. Dated activity – 17 November 2026

- Confirmed Cassandra 4.1.12 on all three nodes.
- Reviewed Commit Log configuration on all nodes; archive and restore parameters remained empty; precision was MICROSECONDS.
- Prepared node-specific archive directories, deployed Commit Log archive script v2.0 to all nodes and verified identical script SHA-256.
- Tested dummy files on all three nodes. No real Commit Log segment was archived.
- Identified a no-overwrite race in v2.0 during code review. Live archive configuration remains disabled.
- PITR and archive callback semantics remain under review.

See [17 November daily activity](../../daily-activity/2026-11-17.md).

## 10. Current status and next steps

### Completed and evidenced
- Three-node Cassandra cluster and banking schema.
- Python synthetic transaction insertion workload and reporting.
- Host/JVM/Cassandra monitoring foundation and custom metric script (manual execution).
- Controlled node outage, specified-scope incremental repair.
- Snapshot creation, partial checksum validation, isolated SSTableLoader restore.
- Snapshot metadata automation.
- Commit Log archive script v2.0 deployed and dummy-file tested.

### Pending, deferred or incompletely validated
- Upload the actual sanitised Python source and requirements file from LAB1.
- Upload verified start/stop/backup/metrics scripts; do not recreate originals from memory and claim they are byte-for-byte copies.
- Add sanitised Prometheus configuration and Grafana dashboard export.
- Confirm whether the custom-metrics timer was ever installed and validate scheduled cycles.
- Confirm LAB3 source/copy checksum comparison.
- Establish independent storage and retention for backups.
- Perform broader data restore validation and measured RPO/RTO testing.
- Harden Commit Log archive script against races and test all branches with dummy files.
- Validate Cassandra 4.1.12 archiving and failure/retry semantics.
- Design and test PITR before any configuration activation.
- Do not touch the deferred VJC9LAB3 `viasroot` cleanup unless expressly requested.

## 11. Daily record policy

Use one `daily-activity/YYYY-MM-DD.md` file for each actual work session. Record the real date, the exact action performed, observed output, RCA and correction if there was an error, performance measurements, validation and next work. If there was no new activity or no evidence, do not invent a log entry or result.
