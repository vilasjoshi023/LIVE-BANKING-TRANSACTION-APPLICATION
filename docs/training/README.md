# VJCLAB Database Engineering Curriculum

## Mission

Build practical capability from absolute beginner to senior/lead Cassandra DBA and database platform engineer using the Live Banking Transaction Application.

This repository is both a training path and an evidence register. It does **not** claim every listed subject has already been implemented. The current hands-on environment is a three-node CentOS Stream 9 VMware lab running Cassandra 4.1.12. Advanced modules may require a separate disposable environment, more memory/storage or cloud infrastructure.

## Learning levels

| Level | Capability | Progress gate |
|---|---|---|
| L0 – Beginner | Understand Linux, networking, files, processes and databases | Navigate Linux, inspect services and explain the lab |
| L1 – Foundation DBA | Install/configure Cassandra, operate CQL and verify cluster health | Repeatable installation and health checklist |
| L2 – Working DBA | Operate schema, Python driver, monitoring and routine maintenance | Successful workloads, dashboard checks and routine triage |
| L3 – Production DBA | Diagnose failure, repair, backup/restore, secure and tune | Evidence-backed RCA and recovery runbooks |
| L4 – Senior DBA | Capacity, multi-DC, upgrades, automation and change governance | Architecture and rollback plans tested in a suitable environment |
| L5 – Expert | Cassandra internals, JVM/OS interactions, consistency and failure modes | Explain hypotheses with measurements, traces and logs |
| L6 – Ultra-legend | Design resilient database platforms, own incidents/SLOs and lead operational practice | End-to-end capstone, DR rehearsal, security review and handover |

The “ultra-legend” name is a learning tier, not an external certification. Mastery requires practical, repeatable evidence.

## Curriculum sequence

1. Linux, storage, systemd, networking and security basics.
2. Database fundamentals, distributed systems and Cassandra orientation.
3. Cassandra installation, topology, architecture and internals.
4. CQL, query-first schema design and schema evolution.
5. Python driver and banking transaction application engineering.
6. Monitoring, daily DBA operations, dashboards and alerting.
7. Availability, node failure, repair and topology operations.
8. Snapshots, backup, restore, Commit Log archiving and PITR.
9. Performance engineering, benchmarking and capacity planning.
10. Security, governance, access control and encryption.
11. Shell/Python automation, Ansible, Terraform and CI/CD.
12. Upgrades, migrations, compatibility and rollback.
13. Multi-datacenter, cloud and Kubernetes operations.
14. Expert architecture, incident command, SRE and capstone.

## Files

- [Master roadmap](master-roadmap.md)
- [Lab safety and evidence rules](lab-safety-and-evidence.md)
- [Practical lab catalogue](hands-on-lab-catalog.md)
- [Completion matrix](completion-matrix.md)
- Modules:
  - [01 Linux and networking](modules/01-linux-networking.md)
  - [02 Cassandra architecture and operations](modules/02-cassandra-architecture-operations.md)
  - [03 CQL and data modelling](modules/03-cql-data-modelling.md)
  - [04 Python driver and banking application](modules/04-python-driver-application.md)
  - [05 Monitoring and observability](modules/05-monitoring-observability.md)
  - [06 HA, backup, recovery and PITR](modules/06-ha-backup-recovery-pitr.md)
  - [07 Performance and capacity](modules/07-performance-capacity.md)
  - [08 Security and governance](modules/08-security-governance.md)
  - [09 Automation, upgrades and platforms](modules/09-automation-upgrades-platforms.md)
  - [10 Expert scenarios and capstone](modules/10-expert-scenarios-capstone.md)

## Teaching contract for every lesson

1. Explain it in simple language before introducing jargon.
2. Explain why a DBA needs it and what can fail in production.
3. Show the data flow or system flow.
4. Give exact commands/code, explain key options and identify the target VM/user.
5. Give expected output and explain deviations.
6. Work one practical action at a time; review the user's result before continuing.
7. Include validation, safety controls and rollback/stop criteria.
8. Capture real output, RCA, performance observations and next steps.
9. Update the daily activity entry after the actual work session.
10. Mark Complete only after execution and validation evidence.

## Current baseline

Already completed in the current lab: three-node Cassandra 4.1.12 cluster, banking keyspace/table, Python synthetic transaction insert workload, initial monitoring stack, custom metrics collection script (manual run), controlled one-node outage insert test, scoped repair preview and repair, snapshot/restore exercise, snapshot automation, Commit Log archive script v2.0 deployment and dummy-file tests.

Use [project history](../project-history/project-from-start-to-current.md) for the details and caveats. Advanced modules are targets, not completed work.

## Resource-aware execution

The VMs have approximately 3–3.5 GiB RAM each. Do not overlap expensive repair, compaction, restore, upgrade or load tests. Use a disposable cluster for destructive or high-risk exercises. Keep the deferred VJC9LAB3 account cleanup untouched unless explicitly requested.
