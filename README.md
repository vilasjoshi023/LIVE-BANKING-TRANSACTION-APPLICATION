# Live Banking Transaction Application – VJCLAB

A hands-on database engineering project demonstrating a multi-node Apache Cassandra platform, Python banking transaction workload, operational recovery, backup/restore, and observability.

> **Lab environment:** Three CentOS Stream 9 VMware VMs. This is a learning and validation environment, not a production banking service. All results are lab observations and must not be represented as production SLAs or capacity guarantees.

## Technology stack

- Apache Cassandra 4.1.12, three nodes, one datacenter (`dc1`)
- Python 3.9 and Cassandra Python driver 3.29.3
- Linux / CentOS Stream 9
- Prometheus, Node Exporter, JMX Exporter and Grafana
- Shell automation, nodetool, cqlsh, SSTableLoader

## Lab topology

| Node | Address | Role |
|---|---|---|
| VJC9LAB1 | 192.168.62.134 | Cassandra node 1, Python application, Prometheus, Grafana |
| VJC9LAB2 | 192.168.62.135 | Cassandra node 2 |
| VJC9LAB3 | 192.168.62.136 | Cassandra node 3 |

Cassandra configuration observed in the lab: cluster `VJCLAB`, datacenter `dc1`, rack `rack1`, GossipingPropertyFileSnitch, Murmur3Partitioner and 16 tokens per node. The `banking_stream` keyspace uses NetworkTopologyStrategy with RF=3.

## Repository layout

```text
.
├── README.md
├── docs/
│   ├── architecture/
│   ├── cluster-operations/
│   ├── failure-recovery/
│   ├── backup-restore/
│   ├── commitlog-pitr/
│   └── monitoring/
├── daily-activity/
│   ├── README.md
│   ├── activity-template.md
│   ├── 2026-11-16.md
│   └── 2026-11-17.md
├── application/
│   ├── src/
│   ├── config/
│   └── requirements.txt
├── scripts/
│   ├── backup/
│   ├── monitoring/
│   └── operations/
└── monitoring/
    ├── prometheus/
    └── grafana/
```

The layout is a target structure; folders and files will be added as their implementations are safely migrated. An empty directory is not evidence that its implementation is complete.

## Work completed and validated

- Built and verified a three-node Cassandra 4.1.12 cluster; observed all three nodes in UN state during the latest recorded check on 17 November 2026.
- Created the `banking_stream` keyspace and `bank_transactions` table.
- Built a Python transaction insertion workload using prepared statements and LOCAL_QUORUM.
- Ran a controlled node outage exercise: 1,000 inserts succeeded while one node was down; this is a single lab test, not a performance guarantee.
- Performed repair preview and an incremental repair for the specified keyspace/table scope.
- Set up Prometheus scraping for Prometheus, Node Exporter and Cassandra JMX Exporter; built a Grafana DBA monitoring dashboard.
- Created Cassandra snapshots on all three nodes, copied snapshot files to a staging location and performed checksum comparisons for the confirmed node copies.
- Restored SSTables into a separate restore keyspace using SSTableLoader; the tested date partition count was 3,000 in source and restored table.
- Automated snapshot creation across all three nodes and verified snapshot metadata; the automation does not yet provide off-host backup, retention or full restore orchestration.
- Developed and deployed Commit Log archive script v2.0 to all three nodes and validated it with dummy files only.

## Current status – 17 November 2026

**In progress:** Review Cassandra 4.1.12 Commit Log archive callback behaviour, harden the archive script's no-overwrite behaviour, and design/test the PITR recovery workflow.

**Not yet enabled:** The live `archive_command` and restore settings remain empty on all three nodes. No real Commit Log segment has been archived. No Cassandra configuration change or restart has been made for archiving.

## Safety and publication policy

Never commit passwords, tokens, private SSH keys, `.env` files, real customer data, banking credentials, raw Commit Logs, SSTables, snapshots or database backup files. Publish sanitised examples, scripts, command output with secrets removed, and documentation only. Do not include internal employer/customer information.

See [Daily Activity](daily-activity/README.md) for chronological engineering notes.
