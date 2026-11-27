# Apache Cassandra DBA Master Program – source syllabus

> Source: user-provided `Apache Cassandra DBA Master Program.pdf` (6 pages). This transcription preserves the source document's section names and listed topics. It is a curriculum outline, not a guarantee of specific training outcomes or certification.

## Program overview

The source describes a practical, production-oriented learning program for distributed database administration. It progresses from Cassandra and NoSQL fundamentals through architecture, real-time data modeling, performance, high availability, troubleshooting, installation, configuration, security, monitoring and optimization. It also introduces real-time processing patterns for IoT, event-driven systems and large-scale distributed applications.

## Comprehensive curriculum

### Section 1: NoSQL Fundamentals & Apache Cassandra Overview
- What is NoSQL?
- Types of NoSQL Databases
- CAP vs PACELC
- BASE vs ACID
- Apache Cassandra Overview
- Cassandra vs RDBMS
- Modern use cases
- Real-world adopters

### Section 2: Installation & Environment Setup
- Install Cassandra (Binary / Package)
- Single-node & multi-node setup
- cassandra.yaml basics
- OS tuning (ulimits, disk, memory)
- cqlsh basics (CREATE / INSERT / SELECT)
- nodetool (status, ring)

### Section 3: Cassandra Architecture
- Peer-to-peer architecture
- Ring & token distribution
- Nodes, DCs, clusters
- Gossip protocol (overview)
- Coordinator node
- Replication strategies
- Consistency levels (real scenarios)

### Section 4: Cassandra Internals (Read & Write Path)
- Write path (CommitLog → Memtable → SSTable)
- Read path (Cache → Bloom Filter → SSTables)
- Tombstones & GC basics
- Compaction overview (STCS, LCS, UCS)

### Section 5: Data Modeling - Fundamentals
- Query-driven design
- Partition vs Clustering key
- Primary key design
- Avoid hotspots & large partitions

### Section 6: Data Modeling - Advanced
- Time-series modeling
- Bucketing strategies
- Denormalization
- Handling large partitions

### Section 7: Cassandra Query Language (CQL) - Basics
- CQL Overview (DDL, DML, DCL and differences from SQL)
- CRUD operations with best practices for partition keys and clustering keys
- TTL & collections

### Section 8: Cassandra Query Language (CQL) - Advanced & Best Practices
- Batches (good vs bad)
- Prepared statements
- LWT (when to avoid)
- Query tracing & Consistency levels in queries

### Section 9: Indexing & Query Optimization
- Primary key indexing
- Secondary index limits
- SAI (Cassandra 5.x)
- Query anti-patterns

### Section 10: Security and Access Control
- Authentication & RBAC
- Roles & permissions
- TLS encryption
- Audit logging
- Security best practices

### Section 11: Multi-Node Cluster Setup and Operations
- Initializing a cluster (3 nodes) with proper seed nodes
- Single DC vs Multi-DC setup using NetworkTopologyStrategy
- Gossip and RPC configuration
- Testing consistency levels and data distribution
- Node lifecycle: Bootstrap, Decommission, Replace, Move, Removenode

### Section 12: Daily DBA Operations (Nodetool)
- nodetool commands: status, ring, tablestats, tpstats
- Node lifecycle: bootstrap, decommission, replace
- Hotspot detection (toppartitions)

### Section 13: Repair & Maintenance
- Incremental repair
- Cleanup, flush, compaction
- Cassandra Reaper (automation)
- Maintenance best practices

### Section 14: Backup & Restore
- Snapshots & incremental backups
- Commit log backup
- Restore strategies
- Medusa overview

### Section 15: Point-in-Time Recovery (PITR)
- PITR concepts
- Commit log archiving
- Recovery scenarios
- Validation

### Section 16: Monitoring & Observability
- Metrics (latency, throughput, compaction)
- Logs (system.log, gc.log)
- Alerting strategies

### Section 17: Performance Tuning & Troubleshooting
- JVM tuning (G1GC / ZGC)
- Heap sizing
- Disk & I/O optimization
- Slow query troubleshooting
- GC issues

### Section 18: Upgrade, Migration & Modern Deployments
- Rolling upgrades (4.x → 5.x)
- SSTable upgrades
- dsbulk / sstableloader
- Intro to Kubernetes (K8ssandra)
- Cloud Cassandra overview

## Program objectives stated in the source

The source states that learners should gain practical knowledge and hands-on experience to install, configure, secure, monitor and troubleshoot Cassandra clusters, and be prepared to administer, optimize and maintain enterprise-grade Cassandra databases.

It describes the intended audience as DBAs, IT professionals, system administrators, developers, data engineers, DevOps engineers and cloud professionals.

## Source notes

- The source says the technical content may change without prior notice.
- The source says detailed notes, reference guides and practical resources are intended to support learning.
- The trainer profile and academy website are reproduced as program-source claims, not independently verified endorsements.
