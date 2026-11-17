# Hands-On Lab Catalogue – VJCLAB

This catalogue is the execution backlog. Run one lab at a time. For the current three-node lab, prefer read-only checks before writes and use a disposable keyspace for experiments. Any destructive, high-load or disruptive lab must be planned separately.

## Foundation labs
- LAB-001: Map VM CPU/RAM/disk/network with hostname, hostname -I, uptime, lscpu, free -h, lsblk, df -hT, ip addr and ip route.
- LAB-002: Navigate Linux files; practice ls, find, grep, awk, sed, sort, uniq, cut, head, tail, less and journalctl.
- LAB-003: Explain ownership, mode bits, umask, sudo, ACLs and service accounts using temporary files.
- LAB-004: Inspect processes, signals, sockets and systemd units; distinguish process state from service-unit state.
- LAB-005: Build a TCP port map; use ss, curl, nc where installed, firewall-cmd --list-all and service listener checks.
- LAB-006: Inspect SELinux mode, labels, denials and booleans; correct a test denial without disabling SELinux.

## Cassandra foundation and architecture
- LAB-010: Verify Cassandra version, Java version, install paths and service account on all three nodes.
- LAB-011: Inspect cassandra.yaml and cassandra-rackdc.properties; explain every configured cluster identity/network/storage field.
- LAB-012: Validate 3-node status, schema agreement, datacenter/rack placement, host IDs and token distribution.
- LAB-013: Trace a synthetic INSERT from Python/CQL coordinator to replicas and persistence stages.
- LAB-014: Compare consistency requirements for RF=3 and explain availability when one replica is down.
- LAB-015: Inspect gossip, endpoint states, failure detector and nodetool diagnostics.
- LAB-016: Explain commit log, memtable, flush, SSTable, bloom filter, cache and compaction using safe read-only output.

## CQL and modelling
- LAB-020: Describe keyspace/table and record schema in a version-controlled CQL file.
- LAB-021: Design queries first, identify partition and clustering keys, and test allowed query patterns.
- LAB-022: Estimate partition size and identify risks of a date-only partition at growing volume.
- LAB-023: Create a separate account-history table for a synthetic query pattern.
- LAB-024: Test TTL, timestamp/upsert semantics and deletion/tombstones only in a disposable keyspace.
- LAB-025: Explore batches, LWT, collections and indexes; document where each is and is not appropriate.
- LAB-026: Use tracing and paging and compare query plans/latency with representative synthetic rows.

## Python application
- LAB-030: Create/review requirements, virtual environment, module imports and structured logging.
- LAB-031: Verify contact points, local DC, driver metadata and clean session/cluster shutdown.
- LAB-032: Use prepared statements and typed Decimal/date/UUID parameters.
- LAB-033: Add explicit consistency, timeouts and safe exception reporting.
- LAB-034: Add bounded concurrency, backpressure and retry limits.
- LAB-035: Implement an idempotency key and prove retry does not create a duplicate business effect.
- LAB-036: Emit application metrics and correlate one load run with Cassandra and host metrics.

## Monitoring and operations
- LAB-040: Check Node Exporter and JMX Exporter endpoints from the permitted source.
- LAB-041: Validate Prometheus configuration with promtool and inspect /targets and lastError.
- LAB-042: Query up, scrape duration, JVM heap/GC and host CPU/memory/disk/network.
- LAB-043: Validate Grafana datasource and import/export a dashboard JSON.
- LAB-044: Extend custom Cassandra textfile metrics with parser tests, atomic publication, stale-data detection and failure metrics.
- LAB-045: Create and test a systemd timer only after service script validation; observe at least two runs.
- LAB-046: Write a daily health-check report and escalation criteria.

## Failure, repair and topology
- LAB-050: Run a planned single-node outage exercise with pre-checks, bounded workload and operator approval.
- LAB-051: Inspect hints on each node; distinguish current pending hints from proof of replay.
- LAB-052: Run repair preview and interpret scope; execute actual repair only with explicit approval and a maintenance plan.
- LAB-053: Test failed node restart/rejoin in a disposable cluster.
- LAB-054: Rehearse bootstrap, replace, decommission and removenode in disposable clusters.
- LAB-055: Test network partition and recovery in isolated environment; record quorum outcomes.

## Backup, restore and PITR
- LAB-060: Create per-node snapshots and explain hard links and per-node snapshot timestamps.
- LAB-061: Validate snapshot manifest/schema/components and disk headroom.
- LAB-062: Copy to separate storage and compare SHA-256 manifest; include LAB3 copy validation.
- LAB-063: Run SSTableLoader restore into isolated target and validate partition/key samples.
- LAB-064: Define backup encryption, retention, immutable/offsite storage and restore evidence.
- LAB-065: Harden Commit Log archiver with no-clobber publication, lock/race tests, checksums and failure handling using dummy files.
- LAB-066: Validate Cassandra 4.1.12 archive/restore callback and retry contract.
- LAB-067: PITR recovery drill on disposable cluster; measure RPO/RTO and validate target timestamp.
- LAB-068: Write complete restore runbook and rollback/abort criteria.

## Performance and capacity
- LAB-070: Establish baseline with warm-up, repeated test runs and constant workload conditions.
- LAB-071: Capture per-operation latency histograms, success/failure/timeouts and TPS.
- LAB-072: Diagnose high read latency using proxyhistograms, tablestats, tracing and partition distribution.
- LAB-073: Diagnose high write latency using mutation stage, commit-log sync, disk/network and driver metrics.
- LAB-074: Diagnose tombstones, large partitions and hot partitions in a test dataset.
- LAB-075: Diagnose pending compactions, pending flushes, disk I/O saturation and compaction headroom.
- LAB-076: Correlate GC pauses, heap/off-heap, CPU steal, memory pressure and latency.
- LAB-077: Calculate capacity including raw data, RF, compression, compaction temporary space, repair and restore reserve.
- LAB-078: Conduct controlled before/after tuning and document trade-offs; do not tune from one metric snapshot.

## Security and automation
- LAB-080: Create a least-privilege Cassandra role in an isolated keyspace and verify grants.
- LAB-081: Review authentication, authorization, TLS and certificate lifecycle using a separate secure test environment.
- LAB-082: Audit SSH/firewall/JMX/network exposure and rotate sample lab credentials.
- LAB-083: Build robust shell scripts with strict mode, quoting, traps, idempotency and negative tests.
- LAB-084: Build Python DBA health checks and reports.
- LAB-085: Create Ansible inventory/playbook with check mode and idempotent handlers.
- LAB-086: Create Terraform plan for a disposable environment; protect state and secrets.
- LAB-087: Add CI checks: shellcheck, shfmt, Python lint/unit tests, YAML validation and secret scanning.

## Upgrade, cloud, multi-DC and expert
- LAB-090: Build version compatibility matrix and rolling-upgrade precheck list.
- LAB-091: Rehearse rolling upgrade on disposable cluster; validate schema, data, driver and rollback boundaries.
- LAB-092: Design two-DC NetworkTopologyStrategy and consistency-level matrix.
- LAB-093: Simulate WAN latency/DC isolation in an isolated environment.
- LAB-094: Model a Cassandra-on-Kubernetes design including storage, anti-affinity, disruption budgets and probes.
- LAB-095: Design cloud deployment with private networking, IAM, storage throughput, backup and monitoring.
- LAB-096: Run incident simulation: high latency, node down, backup failure or disk pressure; act as incident commander.
- LAB-097: Produce SLO/SLI dashboard, error budget policy and postmortem.
- LAB-098: Complete capstone architecture, test evidence, DR drill, security review and operational handover.

## Lab evidence template
For every LAB ID, record: date/time, objective, environment, pre-checks, exact commands, output, analysis, error/RCA, change, validation, performance impact, cleanup/rollback and evidence link. Use the completion matrix to update status only after evidence exists.
