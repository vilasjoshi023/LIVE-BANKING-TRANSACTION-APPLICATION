# Apache Cassandra DBA Master Program – VJCLAB learning roadmap

**Primary curriculum source:** [Apache Cassandra DBA Master Program source syllabus](../reference-library/apache-cassandra-dba-master-program-source-syllabus.md)  
**Original uploaded program:** `Apache Cassandra DBA Master Program.pdf` (6 pages; original PDF binary is not yet committed to this repository).

## Training objective

Use the 18-section Apache Cassandra DBA Master Program as the curriculum for the Live Banking Transaction Application project. Deliver the syllabus through practical work on the existing three-node VJCLAB environment, evidence capture, troubleshooting exercises and DBA interview checkpoints.

This is a guided lab and synthetic banking workload, not a production banking platform. The curriculum follows the uploaded source's scope and sequence. Practical exercises will be adapted to the installed release and existing lab rather than reinstalling or rebuilding components unnecessarily.

## Lab baseline

| Item | Current lab baseline |
|---|---|
| Operating system | CentOS Stream 9 |
| Cassandra | Apache Cassandra 4.1.12 |
| Cluster | VJCLAB |
| Datacenter | dc1 |
| Nodes | VJC9LAB1 .134, VJC9LAB2 .135, VJC9LAB3 .136 |
| Rack labels | rack1 on all nodes |
| Python driver | cassandra-driver 3.29.3 |
| Banking keyspace | banking_stream |
| Consistency level | LOCAL_QUORUM |
| Monitoring | Prometheus, Node Exporter, Cassandra JMX Exporter, Grafana |
| Application | /opt/banking-app |

All example commands, configuration keys and upgrade steps must be checked against Cassandra 4.1.12 and the exact installed package layout before execution.

## How each section will be taught

Every section uses the same delivery loop:

1. **Concept:** explain the topic and why a Cassandra DBA needs it.
2. **Lab:** run a bounded practical exercise in VJCLAB or an isolated test namespace.
3. **Evidence:** capture commands, outputs, metrics and any error messages without secrets.
4. **RCA:** explain symptom, investigation, root cause, remediation and validation.
5. **Interview checkpoint:** answer realistic DBA questions in a clear, production-oriented manner.
6. **Documentation:** update the daily activity log and relevant runbook/reference page.

No destructive node lifecycle, repair, cleanup, decommission, snapshot deletion, upgrade, or security restart exercise will be run without an explicit pre-check, recovery plan and controlled step-by-step validation.

## Topic-wise learning pages

Each of the 18 curriculum sections has its own GitHub page with the source syllabus topics, VJCLAB practical plan, evidence checklist, safety/version controls and interview checkpoints.

- [Open the 18-topic tracker](topics/README.md)

## Curriculum and lab mapping

| Section | Master Program topic | Planned VJCLAB practical work | Tracking |
|---:|---|---|---|
| 1 | NoSQL fundamentals & Cassandra overview | NoSQL types, CAP/PACELC, BASE/ACID, Cassandra vs RDBMS, use cases and architecture comparison | To study systematically |
| 2 | Installation & environment setup | Review installed binary layout, Java, Linux limits, disk/memory, cassandra.yaml, cqlsh and nodetool; use existing installation evidence | Existing lab; review and validate |
| 3 | Cassandra architecture | Peer-to-peer, tokens, vnodes, DC/rack, gossip, coordinator, replication and consistency scenarios | Existing cluster; structured revision |
| 4 | Cassandra internals | Trace write/read paths; commit log, memtable, SSTables, caches, Bloom filters, tombstones and STCS/LCS/UCS | Concepts partly covered; practical drills planned |
| 5 | Data modeling fundamentals | Inspect banking_stream.bank_transactions primary key, partition boundaries, query patterns and partition-size risk | Existing schema; assess |
| 6 | Advanced data modeling | Time-series buckets, bucketing, denormalization and large-partition handling; design account-oriented query tables without unbounded filtering | Planned schema-design lab |
| 7 | CQL basics | DDL/DML/DCL, CRUD, primary-key query rules, TTL and collections | Existing CQL use; structured exercise |
| 8 | Advanced CQL | Good vs bad batches, prepared statements, LWT trade-offs, tracing and consistency per query | Driver and CQL lab planned |
| 9 | Indexing & query optimization | Primary-key access, secondary-index limits, anti-patterns, bounded query review | Slow-query comparison already performed; extend |
| 10 | Security & access control | Authentication/RBAC, roles, grants, TLS, audit logging and security review | In progress; LAB3 authentication pilot |
| 11 | Multi-node setup & operations | Seeds, single vs multi-DC NetworkTopologyStrategy, gossip/RPC, data distribution and safe node lifecycle | Existing 3-node cluster; lifecycle drills pending |
| 12 | Daily DBA operations | status, ring, tablestats, tpstats, toppartitions and node lifecycle health checks | Partly practiced; build repeatable runbook |
| 13 | Repair & maintenance | Incremental repair, cleanup, flush, compaction, Reaper and maintenance windows | Repair/compaction activities partly completed; extend |
| 14 | Backup & restore | Snapshots, incremental backups, CommitLog backup, SSTableLoader and Medusa overview | Snapshot/checksum/restore lab partly completed |
| 15 | Point-in-time recovery | CommitLog archive, recovery point selection, restore, replay and validation | Archive preparation completed; PITR not yet proven |
| 16 | Monitoring & observability | Latency/throughput/compaction metrics, system.log, gc.log, Prometheus, Grafana and alerting | Monitoring platform installed; dashboards/alerts and coverage to validate |
| 17 | Performance tuning & troubleshooting | G1GC/ZGC concepts, heap, disk/I/O, slow queries, GC and production scenarios | Diagnostics and slow-query lab partly completed; scenario drills planned |
| 18 | Upgrade, migration & modern deployments | 4.x→5.x rolling-upgrade planning, SSTable upgrades, dsbulk/sstableloader, K8ssandra and cloud Cassandra | Future isolated upgrade/migration track |

## Important version boundaries

- The working lab is Cassandra **4.1.12**.
- The source syllabus explicitly labels SAI as a Cassandra **5.x** topic. SAI must not be treated as an available 4.1.12 exercise; cover its concept now and execute only in a separate Cassandra 5.x test environment.
- The source includes rolling upgrades from 4.x to 5.x. This is a future migration exercise, not a change to the current learning cluster. First build a tested compatibility matrix, backup and rollback plan in an isolated clone.
- The source includes G1GC / ZGC. Collector availability and suitability depend on the Cassandra release and supported JDK. Verify supported JVM options before changing the live lab.
- K8ssandra and cloud Cassandra are architecture/deployment studies initially; do not install Kubernetes workloads on the current memory-constrained VMs.

## Current project progress – starting checkpoint

The following are already evidenced in the project history and will be treated as prior lab work, not repeated blindly:

- Three-node Cassandra 4.1.12 VJCLAB cluster and banking_stream workload.
- Python transaction workload and shared connection factory.
- LOCAL_QUORUM usage.
- Slow-query workload and Prometheus textfile metrics preparation.
- Cassandra monitoring stack with Prometheus, Node Exporter, JMX Exporter and Grafana.
- Node health, repair preview/incremental repair exercises.
- Snapshot creation, checksum checks and SSTableLoader restore to a separate target.
- CommitLog archive preparation with test/dummy files; live PITR remains unproven.
- Initial security audit and system_auth replication-strategy change to NetworkTopologyStrategy dc1=3.
- Python connection factory updated with optional PlainTextAuthProvider; anonymous-compatible connection test passed; .env mode set to 0600.
- PasswordAuthenticator pilot enabled only on VJC9LAB3.
- dba_admin authenticated successfully on LAB3.
- banking_app and banking_readonly authenticated and completed bounded SELECTs on LAB3.
- CassandraAuthorizer remains AllowAllAuthorizer on all nodes; role-based permission enforcement has not started.
- Latest maintenance checkpoint: slow-query timer and service inactive; all nodes observed UN; LAB3 nodetool clientstats output still outstanding.

## Immediate learning sequence

Resume from the actual current state; do not roll back completed evidence just to follow a textbook order.

1. **Finish Section 10 – Security and Access Control:** obtain LAB3 clientstats; verify no client workload is using the pilot; complete a controlled CassandraAuthorizer pilot, grants and positive/negative privilege tests; then plan the remaining-node rollout and TLS/audit logging as separate changes.
2. **Section 11 – Multi-Node Operations:** topology, NetworkTopologyStrategy, gossip/RPC, consistency and safe node lifecycle.
3. **Section 12 – Daily DBA Operations:** make a health snapshot/runbook and practice interpreting each command.
4. **Sections 13–15 – Maintenance, Backup/Restore and PITR:** close the live CommitLog archiving and restore-validation gaps.
5. **Sections 16–17 – Monitoring and Performance:** prove dashboard/alert coverage and run controlled production-like scenarios.
6. **Sections 1–9 – Fundamentals, Architecture, Modeling and CQL:** perform systematic concept revision and targeted labs alongside the operational work; focus on gaps discovered by the assessments.
7. **Section 18 – Upgrade/Migration:** separate Cassandra 5.x/K8ssandra/cloud lab after 4.1.12 topics and recovery validation are complete.

## Progress tracking

Each section will be marked **Not started**, **In progress**, **Lab completed**, or **Validated** only when the relevant evidence exists. A concept discussion alone does not count as a completed practical lab. A successful one-off command does not prove production readiness.

Record:
- date and section;
- objective and prerequisites;
- node(s), version and topology;
- commands run and redacted outputs;
- errors and root-cause analysis;
- before/after validation;
- rollback/recovery notes;
- interview questions and answers;
- next action.

## Source attribution

This roadmap is based on the uploaded six-page document *Apache Cassandra DBA Master Program*. Its original section titles and subject coverage are preserved in the linked source syllabus. The VJCLAB mappings, sequence recommendations, version boundaries and project progress notes are adaptations to this project's recorded environment and are not claimed to be text from the program PDF.
