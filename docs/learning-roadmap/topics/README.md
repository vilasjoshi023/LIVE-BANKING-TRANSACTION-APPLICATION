# Apache Cassandra DBA Master Program – topic-wise tracker

This directory contains one page per section in the uploaded six-page *Apache Cassandra DBA Master Program*. Topic names are taken from the source syllabus. Practical exercises, evidence requirements and VJCLAB status notes are project-specific adaptations.

## Topic index

| Section | Topic | Learning page |
|---:|---|---|
| 1 | NoSQL Fundamentals & Apache Cassandra Overview | [Open topic 01](section-01-nosql-fundamentals.md) |
| 2 | Installation & Environment Setup | [Open topic 02](section-02-installation-environment-setup.md) |
| 3 | Cassandra Architecture | [Open topic 03](section-03-cassandra-architecture.md) |
| 4 | Cassandra Internals (Read & Write Path) | [Open topic 04](section-04-cassandra-internals-read-write-path.md) |
| 5 | Data Modeling – Fundamentals | [Open topic 05](section-05-data-modeling-fundamentals.md) |
| 6 | Data Modeling – Advanced | [Open topic 06](section-06-advanced-data-modeling.md) |
| 7 | Cassandra Query Language (CQL) – Basics | [Open topic 07](section-07-cql-basics.md) |
| 8 | Cassandra Query Language (CQL) – Advanced & Best Practices | [Open topic 08](section-08-cql-advanced-best-practices.md) |
| 9 | Indexing & Query Optimization | [Open topic 09](section-09-indexing-query-optimization.md) |
| 10 | Security and Access Control | [Open topic 10](section-10-security-access-control.md) |
| 11 | Multi-Node Cluster Setup and Operations | [Open topic 11](section-11-multi-node-cluster-operations.md) |
| 12 | Daily DBA Operations (Nodetool) | [Open topic 12](section-12-daily-dba-operations-nodetool.md) |
| 13 | Repair & Maintenance | [Open topic 13](section-13-repair-maintenance.md) |
| 14 | Backup & Restore | [Open topic 14](section-14-backup-restore.md) |
| 15 | Point-in-Time Recovery (PITR) | [Open topic 15](section-15-point-in-time-recovery.md) |
| 16 | Monitoring & Observability | [Open topic 16](section-16-monitoring-observability.md) |
| 17 | Performance Tuning & Troubleshooting | [Open topic 17](section-17-performance-tuning-troubleshooting.md) |
| 18 | Upgrade, Migration & Modern Deployments | [Open topic 18](section-18-upgrade-migration-modern-deployments.md) |

## Progress rules

- **Not started:** no practical evidence recorded.
- **In progress:** work is currently being performed or evidence is incomplete.
- **Lab completed:** the planned bounded exercise has been executed and outputs captured.
- **Validated:** expected results, operational impact and any negative tests have been checked and documented.

A successful command alone does not establish production readiness. Planned topics must not be marked complete until the evidence checklist is satisfied.

## Current training position

The immediate active module is **Section 10 – Security and Access Control**. The LAB3 PasswordAuthenticator pilot and dba_admin, banking_app and banking_readonly login tests have succeeded. CassandraAuthorizer remains disabled on all nodes, so permission enforcement is pending. LAB3 nodetool clientstats output is still required before the authorization pilot proceeds.

After Section 10, continue through Sections 11–17 in the project roadmap, while revising Sections 1–9 systematically. Section 18 is a separate modernization track. Refer to the [VJCLAB master learning roadmap](../apache-cassandra-dba-master-program-vjclab.md) for the sequence, environment baseline and version boundaries.
