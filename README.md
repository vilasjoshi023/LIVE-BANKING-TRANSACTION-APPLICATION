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

## Historical project status – 17 November 2026

**In progress:** Validate Cassandra 4.1.12 archive callback and failure/retry semantics; harden the archive script's no-overwrite behaviour; test all dummy-file branches; design and validate PITR recovery.

**Not enabled:** Live archive_command and restore settings remain empty on all nodes. No real Commit Log segment has been archived. No archiving-related Cassandra configuration change or restart has been performed.

**Other pending evidence:** LAB3 snapshot checksum comparison, independent off-host backup, backup retention, broader restore equivalence checks, automated custom-metrics timer, and some Grafana panels.

## Repository policy

Never commit passwords, tokens, private SSH keys, .env files, real customer/banking data, raw Commit Logs, SSTables, snapshots or backup directories. Only publish sanitised examples, scripts, synthetic data and documentation. Keep confidential employer/customer details out of the repository.

See docs/README.md and daily-activity/README.md.


## Current project status – 25 November 2026

**Cassandra security audit:** A first-pass security audit was completed across all three nodes. The current configuration has AllowAllAuthenticator, AllowAllAuthorizer, client TLS disabled, internode encryption set to none, and Cassandra audit logging disabled. Anonymous CQL access to the banking keyspace and system_auth role metadata was demonstrated. Sensitive password-hash material was exposed during the lab test; the raw value is not stored in this repository and must be treated as sensitive pending credential rotation.

**system_auth metadata:** The keyspace replication strategy was changed from SimpleStrategy RF=3 to NetworkTopologyStrategy dc1=3. Schema agreement and three live nodes were verified afterward. A pre-authentication system_auth snapshot named pre_auth_security_20261125 was created and verified on all three nodes.

**Administrative exposure:** Cassandra JMX 7199 was observed bound to localhost. SSH listens on IPv4/IPv6 wildcard addresses, password authentication is enabled, and the public firewalld zone permits the SSH service. Cockpit socket was inactive. JMX Exporter listens on 0.0.0.0:9404; host firewall rules show LAB1 source allowlists for LAB2/LAB3 exporter endpoints. Full reachability validation remains pending.

**Application integration readiness:** Cassandra client dependencies were identified in cassandra_connection.py, transaction_insert.py, transaction_concurrent_test.py and slow_query_lab.py. The central connection factory has not yet been reviewed for credential integration. No Cassandra authentication or authorization rollout has been performed.

**Slow-query automation:** The banking-slow-query.timer unit is now verified enabled and active on LAB1. Multiple successful timer-triggered executions and repeated metric updates still need to be verified. Grafana/Prometheus deployment of the prepared dashboard and alert templates remains pending.

**Next actions:** Review the Python connection factory; inventory all Cassandra clients; design dedicated DBA, application and read-only roles; plan credential rotation and staged authentication/authorization rollout; then plan client/internode TLS, audit logging and SSH/monitoring endpoint hardening.

No Cassandra authenticator/authorizer change, TLS change, audit-logging change, SSH hardening, firewall modification or Cassandra restart was performed during the security-audit activity. The system_auth replication-strategy update is the only Cassandra configuration metadata change recorded for that activity.


## Current project status – 26 November 2026

**Cassandra security pilot:** PasswordAuthenticator is enabled on VJC9LAB3 only; VJC9LAB1 and VJC9LAB2 remain on AllowAllAuthenticator. The dba_admin, banking_app and banking_readonly roles exist on LAB3. Separate dba_admin, banking_app and banking_readonly login tests succeeded; both application roles completed a bounded SELECT. All nodes still use AllowAllAuthorizer, so role permission boundaries are not yet enforced. LAB3 authorization rollout is pending the node clientstats review.

**Application integration:** The shared Python connection factory supports optional PlainTextAuthProvider authentication. Syntax validation and a connection test passed with the current anonymous configuration; LOCAL_QUORUM was preserved. The application .env file is mode 0600. No real application credentials were added to the file or repository.

**Latest maintenance checkpoint:** The slow-query timer and service were both verified inactive. nodetool status showed all three Cassandra nodes UN. LAB3 nodetool clientstats output remains outstanding. No CassandraAuthorizer, TLS, audit logging, SSH hardening or firewall changes have been applied.

**Reference library:** Searchable transcriptions and page guide for four user-supplied Cassandra PDF references are indexed in [docs/reference-library](docs/reference-library/README.md). The original PDF binary attachments are not committed; the repository contains Markdown text transcriptions for the text-readable PDFs and a page-by-page visual guide for the image-only infographic PDF.

See [the detailed security activity](daily-activity/2026-11-25-cassandra-security-audit.md) and [26 November checkpoint](daily-activity/2026-11-26.md).


## Apache Cassandra DBA Master Program – project learning path

The project's structured Cassandra learning path follows the uploaded **Apache Cassandra DBA Master Program** 18-section curriculum. It is adapted to the existing VJCLAB three-node Cassandra 4.1.12 environment and the Live Banking synthetic workload.

- [VJCLAB learning roadmap](docs/learning-roadmap/apache-cassandra-dba-master-program-vjclab.md)
- [18 topic-wise learning pages](docs/learning-roadmap/topics/README.md)
- [Source syllabus transcription](docs/reference-library/apache-cassandra-dba-master-program-source-syllabus.md)
- [Cassandra reference library](docs/reference-library/README.md)

Current continuation point: finish the Section 10 security/access-control pilot safely (LAB3 authentication is working; authorization enforcement and remaining-node rollout are pending). Then progress through multi-node operations, daily DBA work, repair/maintenance, backup/restore, PITR, monitoring and performance, followed by the remaining fundamentals and isolated upgrade/modernization topics. Cassandra 5.x-only SAI and 4.x-to-5.x upgrade work will not be applied to the 4.1.12 cluster.

The original Master Program PDF and the four earlier Cassandra PDFs are included in the updated local upload bundle, but their PDF binaries are not yet committed to the repository. See [source PDF upload instructions](docs/reference-library/source-pdfs/README.md).
