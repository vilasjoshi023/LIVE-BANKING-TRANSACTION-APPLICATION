# Curriculum Completion Matrix

Status definitions: **Complete** = practical result and validation evidenced; **In Progress** = some work has been executed; **Planned** = not yet demonstrated. Reading this curriculum alone does not change status.

| ID | Learning area | Current status | Evidence / next action |
|---|---|---|---|
| LNX-01 | Linux VM inventory and basic commands | In Progress | Three-VM environment exists; maintain current inventory |
| LNX-02 | Files, permissions, processes, systemd and logs | In Progress | Used in lab operations; complete structured exercises |
| NET-01 | TCP/IP, bind addresses and ports | In Progress | Localhost/private-IP troubleshooting documented |
| NET-02 | firewalld and SELinux RCA | In Progress | Port 9100 and Grafana SELinux cases documented |
| CAS-01 | Cassandra install/version and 3-node cluster | Complete (lab scope) | 4.1.12 on all three; latest recorded status 3/3 UN |
| CAS-02 | Cassandra architecture and write/read internals | In Progress | Concepts documented; deeper command-correlated labs pending |
| CAS-03 | Gossip, snitch, tokens, replication | In Progress | dc1/rack1, GossipingPropertyFileSnitch, Murmur3, 16 tokens |
| CQL-01 | Keyspace and banking table design | Complete (current model) | banking_stream and bank_transactions created |
| CQL-02 | Advanced query-first data modelling | Planned | Design account-history and additional access patterns |
| PY-01 | Python driver connectivity | Complete (lab scope) | /opt/banking-app connects to three contact points |
| PY-02 | Prepared insert and synthetic workload | Complete (lab scope) | Python generator/inserter and performance reporting |
| PY-03 | Idempotency, bounded concurrency and robust retry | Planned | Implement and test safely |
| MON-01 | Node Exporter/JMX Exporter/Prometheus | Complete (observed baseline) | Seven targets UP in prior validation |
| MON-02 | Grafana DBA dashboard | In Progress | Core panels confirmed; some panels unconfirmed |
| MON-03 | Custom metrics collector | In Progress | Manual run verified; scheduled timer not confirmed |
| HA-01 | Controlled one-node outage workload | Complete (one lab exercise) | 1,000/1,000 writes succeeded at LOCAL_QUORUM |
| HA-02 | Hints, repair preview and incremental repair | Complete (specified scope) | Preview and repair successful; not all keyspaces/tables |
| BAK-01 | Snapshots on three nodes | Complete (lab scope) | Same tag separately on all three |
| BAK-02 | Staged backup checksums | In Progress | LAB1/LAB2 passed; LAB3 comparison pending |
| BAK-03 | SSTableLoader restore | Complete (scoped validation) | 3,000 source/restored rows for one date; samples matched |
| BAK-04 | Independent/offsite backup and retention | Planned | Design separate failure domain and retention |
| PITR-01 | Commit Log archive script v2.0 | In Progress | Deployed and dummy-tested; no real segments |
| PITR-02 | No-clobber, retry and PITR recovery | Planned | Harden and test in isolated environment |
| PERF-01 | Application performance measurements | In Progress | Historical TPS/latency records exist; controlled protocol pending |
| PERF-02 | Cassandra bottleneck RCA | Planned | Run measured read/write, GC, compaction and disk diagnosis labs |
| CAP-01 | Capacity model | Planned | Derive from measured row size/growth and headroom |
| SEC-01 | Authentication, roles and least privilege | Planned | Disposable role exercise |
| SEC-02 | TLS, certificates, audit and secrets | Planned | Dedicated isolated lab |
| AUTO-01 | Start/stop lifecycle scripts | In Progress | Scripts exist; stop verification quoting issue documented |
| AUTO-02 | Shell/Python automation quality | In Progress | Archive and metrics scripts exist; negative/concurrency tests pending |
| AUTO-03 | Ansible/Terraform/CI | Planned | Build reproducible test environment |
| UPG-01 | Rolling upgrade rehearsal | Planned | Disposable cluster only |
| DC-01 | Multi-datacenter design/operations | Planned | Architecture and failure drill |
| K8S-01 | Kubernetes/operator operations | Planned | Separate environment |
| SRE-01 | SLO, incident command and postmortem | Planned | Define service objectives and run incident simulation |
| CAPSTONE | Expert end-to-end platform delivery | Planned | Architecture, operations, security, performance, DR and handover |

## Evidence update protocol
For every status change, link the dated activity file, exact validation output or runbook. Keep one activity entry per actual work date. Never mark a theoretical topic Complete merely because its documentation was added.
