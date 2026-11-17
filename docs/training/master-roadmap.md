# Master Roadmap – Beginner to Ultra-Legend Database Engineer

## Phase 0 – Computer, Linux and network literacy
- CPU, cores, threads, RAM, cache, virtual memory, swap, filesystem, inode, block device and process.
- VM/hypervisor, virtual NIC, virtual disk, snapshots, resource overcommit and host contention.
- Shell navigation, files, permissions, links, ownership, ACLs, umask and sudo.
- Processes, signals, threads, services, systemd, journals and exit codes.
- DNS, IPv4/CIDR, routing, ARP, TCP handshake, sockets, bind addresses, ports, MTU and TLS.
- Linux storage: partitions, LVM, XFS/ext4, mount points, IOPS, latency and throughput.
- Security basics: SSH keys, firewall zones/rules, SELinux, patching and least privilege.

**Gate:** Produce a Linux inventory and network/port map for all three lab VMs.

## Phase 1 – Database and distributed-systems foundations
- Database types; RDBMS vs NoSQL; OLTP vs OLAP; transactions and data consistency.
- CAP trade-offs, availability, partition tolerance, eventual consistency and quorum.
- Replication factor, coordinator, replica, partition, token, datacenter, rack and failure domain.
- Read/write consistency levels and quorum calculation.
- Data modelling for known query patterns.

**Gate:** Explain RF=3, QUORUM and LOCAL_QUORUM and calculate acknowledgement requirements during a node outage.

## Phase 2 – Cassandra installation and operations
- Cassandra versions, Java compatibility, installation options and directory layout.
- cassandra.yaml; cluster name, seed provider, listen/broadcast addresses, native transport, snitch, tokens, data and commit-log directories.
- cassandra-rackdc.properties, JVM options, service users and permissions.
- Cluster startup, schema agreement, gossip, health, graceful drain and shutdown.
- nodetool status/info/describecluster/gossipinfo/getendpoints/tpstats.
- Topology changes: bootstrap, replace, decommission, removenode, rebuild and DC changes, with version-specific safeguards.

**Gate:** Build and validate a disposable three-node cluster from a written runbook.

## Phase 3 – Cassandra internals
- Write path: coordinator, replica mutation, commit-log append, memtable update, acknowledgement and flush.
- Read path: coordinator, replica selection, memtables/SSTables, bloom filters, index/summary, caches, tombstone filtering and reconciliation.
- Commit-log segments, sync modes, durability trade-offs, segment recycling and startup replay.
- SSTable components and metadata; memtable lifecycle and flush.
- Compaction: STCS, LCS, TWCS and version-dependent alternatives; backlog, space amplification, throughput and headroom.
- Gossip, failure detection, hinted handoff, repair streaming, read repair concepts and messaging/thread pools.
- Tombstones, TTL, grace period, repair dependency and zombie resurrection risk.
- Heap/off-heap, caches, compression, bloom filters and JVM GC.

**Gate:** Explain a real write/read flow and support the explanation with nodetool, metrics and log observations.

## Phase 4 – CQL and data modelling
- CQL types, tables, keyspaces, partition/clustering keys and clustering order.
- Query-first modelling, partition sizing, bucketing, hot partitions and denormalisation.
- INSERT/UPDATE/DELETE, upsert semantics, TTL, timestamps, batches and LWT/Paxos.
- Collections, static columns, counters, indexes, SAI, materialised views and CDC; validate feature support against Cassandra 4.1.12.
- Query tracing, paging, schema agreement and safe migrations.
- Account-history, date-bucket and transaction lookup patterns.

**Gate:** Model at least four query patterns, create tables in a disposable keyspace and validate supported queries.

## Phase 5 – Python application and driver engineering
- Python packages, virtual environments, imports, logging, exceptions, test structure and dependency pinning.
- Cassandra driver Cluster/Session lifecycle, contact points, local DC, load balancing, pooling and prepared statements.
- Consistency, timeouts, retries, speculation, idempotence, async/concurrency, paging and backpressure.
- Application correctness: synthetic data, Decimal amounts, transaction IDs, idempotency keys, duplicate prevention and reconciliation.
- Structured logs, request IDs, health checks, graceful shutdown and metrics.

**Gate:** Build a bounded, idempotent transaction load generator with success/failure accounting and percentile metrics.

## Phase 6 – Daily operations and observability
- Cluster health, schema agreement, gossip, thread pools, dropped messages, GC, compaction, table stats and proxy histograms.
- Linux and Cassandra logs; service lifecycle; runbooks and change validation.
- Node Exporter, JMX Exporter, Prometheus, Grafana, metrics labels and cardinality.
- Dashboards for CPU, memory, disk, network, heap, GC, read/write latency, counts, compaction, SSTables, dropped messages and app success/errors.
- Alert thresholds based on observed baselines; runbook links and alert recovery.

**Gate:** Produce a daily DBA report and demonstrate an alert from trigger to recovery.

## Phase 7 – HA, failure and repair
- Failure domains, coordinator/replica behavior, consistency under node loss, hints and hint windows.
- Repair preview/full/incremental, primary ranges, local repair, scheduling, repair validation and resource impact.
- Node outage, process crash, disk full, network partition, failed streaming, seed loss and DC failure.
- Bootstrap, replace, decommission and node removal.

**Gate:** Complete approved fault injection in a disposable environment with pre-checks, recovery and data validation.

## Phase 8 – Backup, restore and PITR
- Snapshots, hard links, manifests, schema, per-node snapshot time differences and consistency limitations.
- Backup staging, independent/offsite storage, checksums, encryption, retention, immutable copies and access control.
- sstableloader, schema compatibility, restore validation and reconciliation.
- Commit Log archive/restore commands, segment lifecycle, failure/retry behavior, precision and target-time recovery.
- RPO/RTO, recovery sequence, dependency map and regular restore drills.

**Gate:** Restore a defined recovery point in an isolated environment, compare data and measure RTO/RPO.

## Phase 9 – Performance engineering and capacity
- Workload profiles, request rate, concurrency, throughput, percentiles, queueing and saturation.
- Benchmark methodology: warm-up, fixed test conditions, repeated runs, variance and valid measurement boundaries.
- Slow reads/writes, hot partitions, large partitions, tombstones, query shape and read amplification.
- Compaction backlog, pending flushes, SSTable count, disk latency/IOPS, network, streaming and repair contention.
- JVM heap, GC pauses, CPU, memory pressure, off-heap and thread-pool saturation.
- Driver pool, retries, speculation, consistency and client-side timeouts.
- Capacity: growth, RF overhead, compaction headroom, repair/restore reserve and node replacement.

**Gate:** Complete a controlled before/after performance RCA and a documented capacity model.

## Phase 10 – Security, automation and governance
- Roles, authentication, authorization, least privilege, TLS, certificates and rotation.
- Secrets management, audit, SSH, firewall, JMX isolation, data classification and synthetic data.
- Bash/Python automation, locking, atomic writes, retries, idempotence and structured logs.
- Ansible roles/playbooks/vault; Terraform state/modules/plans; CI/CD, lint/test/release and change controls.
- systemd timers, cron, logrotate, patching and configuration drift.

**Gate:** Deploy a tested idempotent operational script with negative tests, rollback and a peer-review checklist.

## Phase 11 – Upgrade and migration engineering
- Version/release notes, supported Java, compatibility, schema/SSTable formats and driver compatibility.
- Rolling upgrade planning, maintenance windows, mixed-version constraints, pre-checks, post-checks and rollback limitations.
- Data migration, dual writes, backfill, validation, cutover and fallback.
- Capacity/network implications of streaming and migration.

**Gate:** Rehearse upgrade or migration in a disposable cluster and produce an approved runbook.

## Phase 12 – Multi-DC, cloud and Kubernetes
- NetworkTopologyStrategy, rack/DC placement, LOCAL_QUORUM, EACH_QUORUM, cross-DC latency and WAN partitions.
- DC addition/removal, repair, rebuild and disaster recovery across regions.
- Cloud networking, private subnets, IAM, storage performance, backup and monitoring.
- Containers, Kubernetes stateful workloads, persistent volumes, operators, probes, resource limits and scheduling.
- Managed NoSQL trade-offs, cost models, shared responsibility and cloud DR.

**Gate:** Present and defend a two-DC architecture with failure-domain, consistency, cost and DR trade-offs.

## Phase 13 – Expert and ultra-legend leadership
- Deep Cassandra internals and consistency anomalies.
- Incident command, SLI/SLO, error budgets, postmortems, on-call and toil reduction.
- Architecture decision records, capacity reviews, risk/change governance and vendor escalation.
- Mentoring, standard operating procedures and operational maturity.
- End-to-end capstone: architect, build, secure, monitor, benchmark, fail, recover and hand over the synthetic banking platform.

**Gate:** Demonstrate the platform under normal and failure conditions, show evidence, explain trade-offs and hand over repeatable runbooks.
