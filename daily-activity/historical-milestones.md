# Earlier Engineering Milestones – Consolidated Historical Record

> **Date handling:** The available project notes do not preserve the exact calendar date for each of the activities below. This file consolidates verified project history without assigning invented dates. The dated daily logs remain separate.

## 1. Lab infrastructure and Cassandra cluster

- Prepared three CentOS Stream 9 VMware lab nodes:
  - VJC9LAB1 – 192.168.62.134 – 2 vCPU, approximately 3.5 GiB RAM.
  - VJC9LAB2 – 192.168.62.135 – 2 vCPU, approximately 3.0 GiB RAM.
  - VJC9LAB3 – 192.168.62.136 – 2 vCPU, approximately 3.0 GiB RAM.
- Installed and operated Apache Cassandra 4.1.12 with OpenJDK 11.
- Established cluster name `VJCLAB`, datacenter `dc1`, rack `rack1`, GossipingPropertyFileSnitch, Murmur3Partitioner and 16 tokens per node.
- Configured SSH administration from LAB1 to LAB2 and LAB3. Remote Cassandra administration runs under the `cassandra` operating-system account.
- Established operational checks using `nodetool status`, `nodetool describecluster`, `nodetool getendpoints`, `nodetool info` and `nodetool tpstats`.
- Observed all three nodes in UN state in the latest cluster check recorded on 17 November 2026.

## 2. Banking data model

Created keyspace `banking_stream` with NetworkTopologyStrategy and RF=3 for datacenter `dc1`.

Created table `banking_stream.bank_transactions` with transaction date and transaction UUID as the composite primary key, plus account, type, amount, currency, status, description and creation timestamp attributes.

The schema and sample data are a learning workload. Do not upload real customer transactions or personally identifiable data.

## 3. Python transaction workload

- Set up the project under `/opt/banking-app` with a Python virtual environment.
- Installed Python 3.9.25, `cassandra-driver==3.29.3`, Faker, python-dotenv and colorama.
- Configured contact points for all three Cassandra nodes, native port 9042, local DC `dc1`, and keyspace `banking_stream`.
- Implemented a Python Cassandra connection layer using DCAwareRoundRobinPolicy and LOCAL_QUORUM for the transaction workload.
- Implemented prepared-statement inserts and benchmark reporting: success/failure counts, workload duration, TPS, average latency, P50, P95 and P99.
- Correct module invocation used: `python -m src.transaction_insert` from `/opt/banking-app`. Direct invocation as `python src/transaction_insert.py` can fail because of the package import path.

### Recorded benchmark observations

These separate lab runs were not controlled experiments and must not be compared as if only one variable changed.

| Run context | Consistency / condition | Inserts | Observed throughput | Average latency |
|---|---|---:|---:|---:|
| Earlier baseline | LOCAL_ONE | 1,000 | 23.53 TPS | 41.719 ms |
| Earlier baseline | LOCAL_QUORUM | 1,000 | 24.63 TPS | 39.831 ms |
| Controlled node outage, 16 Nov 2026 | LOCAL_QUORUM, one node down | 1,000 | 135.27 TPS | 7.062 ms |

The outage run also recorded P50 5.985 ms, P95 12.318 ms and P99 21.048 ms. These are workload-specific observations from a small lab, not a capacity forecast or production SLA.

## 4. Monitoring and observability

- Installed and configured Prometheus and Grafana on LAB1.
- Configured Node Exporter on all three Cassandra nodes and JMX Exporter on the Cassandra nodes.
- Configured Prometheus scrape targets for Prometheus, Node Exporter and Cassandra JMX Exporter; all seven targets were previously observed UP.
- Created Grafana dashboard `Banking Application - DBA Monitoring`.
- Dashboard panels included host CPU, memory, disk and network; JVM heap and GC indicators; Cassandra read/write latency and counts; and pending flushes.
- Developed `/usr/local/bin/cassandra_prometheus_metrics.sh` to collect additional Cassandra metrics into the Node Exporter textfile collector on LAB1.
- Custom metric names included `cassandra_dba_read_count`, `cassandra_dba_read_latency_ms`, `cassandra_dba_write_count`, `cassandra_dba_write_latency_ms`, `cassandra_dba_pending_flushes`, `cassandra_dba_sstable_count`, `cassandra_dba_dropped_mutations` and `cassandra_dba_collection_success`.
- Manual metric script execution was confirmed. A systemd timer was proposed but was not confirmed as installed and active in the project notes.

## 5. Operations and automation

- Built a project startup workflow on LAB1 to start and check Node Exporter, Cassandra, Prometheus and Grafana, then validate Cassandra cluster status.
- Maintained separate stop/start scripts for lab operations.
- Developed `/usr/local/bin/cassandra_backup.sh` for sequential snapshot creation and metadata verification on all three nodes. Its confirmed scope is snapshot creation and metadata verification, not full off-host backup orchestration.
- Developed Commit Log archive script v2.0; the dated 17 November activity record contains the detailed deployment and dummy-file test evidence.

## 6. Related dated activity logs

- [16 November 2026 – Failure recovery, repair, backup and restore](2026-11-16.md)
- [17 November 2026 – Commit Log archiving preparation](2026-11-17.md)

## 7. Remaining work identified in the historical notes

- Migrate sanitised application source code and operational scripts into this repository.
- Add sanitised Prometheus and Grafana configuration exports.
- Confirm whether the custom-metrics systemd timer was installed; do not assume it is active.
- Complete off-host backup design, retention policy, node3 checksum comparison and broader restore validation.
- Complete Commit Log archive script hardening and PITR workflow before enabling archiving.
