# Live Banking Transaction Application – VJCLAB

A hands-on database engineering project demonstrating a multi-node Apache Cassandra platform, Python banking transaction workload, database operations, recovery, backup/restore, monitoring and automation.

> **Lab status:** This is a learning and validation environment, not a production banking service. All performance figures are small-lab observations, not production capacity claims or SLAs.

## Project study material

- [Live Banking Project Complete Study Book v2 (PDF)](Live_Banking_Project_Complete_Study_Book_v2.pdf)
- [Project history from earliest retained evidence to current state](docs/project-history/project-from-start-to-current.md)
- [Runbooks and documentation index](docs/README.md)
- [Daily activity history](daily-activity/README.md)

## Technology stack

- Apache Cassandra 4.1.12, three-node cluster, one datacenter (dc1)
- CentOS Stream 9 and OpenJDK 11
- Python 3.9.25 and Cassandra Python driver 3.29.3
- Prometheus, Node Exporter, Cassandra JMX Exporter and Grafana
- Shell automation, nodetool, cqlsh, sstableloader

## Lab topology

| Node | Address | Role |
|---|---|---|
| VJC9LAB1 | 192.168.62.134 | Cassandra node 1, Python application, Prometheus and Grafana |
| VJC9LAB2 | 192.168.62.135 | Cassandra node 2 |
| VJC9LAB3 | 192.168.62.136 | Cassandra node 3 |

Cassandra cluster configuration observed: cluster VJCLAB, datacenter dc1, rack rack1, GossipingPropertyFileSnitch, Murmur3Partitioner and 16 tokens per node. Keyspace banking_stream uses NetworkTopologyStrategy with RF=3 in dc1.

## Project lifecycle coverage

1. Linux VM readiness, networking, SSH administration and firewall controls.
2. Cassandra cluster operations, CQL connectivity, schema and health checks.
3. Python banking transaction generation, prepared inserts and latency reporting.
4. Host/JVM/Cassandra observability with Prometheus and Grafana.
5. Custom Cassandra table-level metrics and dashboard panels.
6. Controlled node outage, recovery, repair preview and incremental repair.
7. Snapshots, staged backup copies, checksums and SSTableLoader restore.
8. Snapshot automation and Commit Log archival/PITR preparation.

## Key validated outcomes

- Three Cassandra nodes were observed in UN state in the latest recorded cluster check on 17 November 2026.
- A controlled node-outage workload on 16 November inserted 1,000 transactions successfully using LOCAL_QUORUM while one node was stopped. This is one lab exercise, not an HA guarantee.
- Repair preview reported the previewed data in sync; a sequential incremental repair completed successfully for the specified keyspace/table.
- Snapshot creation and metadata verification completed on all three nodes. Checksum comparisons were confirmed for LAB1 and LAB2 staged copies; LAB3 checksum comparison remains unconfirmed.
- SSTableLoader restored data into a separate target table. The selected 2026-11-15 partition returned 3,000 rows in both source and restore; five sample rows were inspected.
- Prometheus previously showed seven scrape targets UP. Custom Cassandra table metrics were manually generated and scraped. A one-minute systemd timer was proposed but not verified as installed/active.
- Commit Log archive script v2.0 was deployed on all nodes and exercised with dummy files only.

## Current project status – 17 November 2026

**In progress:** Validate Cassandra 4.1.12 archive callback and failure/retry semantics; harden the archive script's no-overwrite behaviour; test all dummy-file branches; design and validate PITR recovery.

**Not enabled:** Live archive_command and restore settings remain empty on all nodes. No real Commit Log segment has been archived. No archiving-related Cassandra configuration change or restart has been performed.

**Other pending evidence:** LAB3 snapshot checksum comparison, independent off-host backup, backup retention, broader restore equivalence checks, automated custom-metrics timer, and some Grafana panels.

## Repository policy

Never commit passwords, tokens, private SSH keys, .env files, real customer/banking data, raw Commit Logs, SSTables, snapshots or backup directories. Only publish sanitised examples, scripts, synthetic data and documentation. Keep confidential employer/customer details out of the repository.

See docs/README.md and daily-activity/README.md.
