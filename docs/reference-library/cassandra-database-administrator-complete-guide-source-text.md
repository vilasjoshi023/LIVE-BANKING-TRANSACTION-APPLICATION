# Cassandra Database Administrator Complete Guide – searchable text transcription

> Source: user-provided PDF (62 pages). This Markdown file preserves extracted page text and page references for repository search. It does not reproduce the original PDF layout or embedded graphics. Use the source PDF for exact visual formatting.


## Source PDF page 1

                             APACHE CASSANDRA
                               DATABASE ADMINISTRATOR


       Beginner-to-advanced concepts • Practical cluster operations • Production troubleshooting •
                                        Interview preparation




       01 Fundamentals                                                      02 Core Operations
       Architecture, installation, CQL and data modeling                    nodetool, topology, compaction and repair




       03 Reliability                                                       04 Performance
       Backup, restore, replication and node lifecycle                      JVM, latency, tombstones and capacity




       05 Security & Monitoring                                             06 Automation & Incidents
       Roles, TLS, JMX, Prometheus and Grafana                              Bash, Python, Ansible and runbooks




 Lab baseline
 Primary examples: Apache Cassandra 4.1.x • Linux/CentOS Stream 9 • 3-node lab • cqlsh • nodetool • JMX •
 Prometheus/Grafana


 Version discipline: Cassandra 4.1.x is used as the main practical baseline. The guide flags version-sensitive areas; validate
 every command, configuration option and upgrade procedure against the exact deployed release. Cassandra 5.x behavior may
 differ.


 Safety note: Use isolated lab nodes. Do not experiment with decommission, replace, repair, cleanup, snapshot deletion or data-directory operations
 on production without a reviewed runbook and backup.




Cassandra Database Administrator | Practical Learning Guide                                                                                  Page 1

## Source PDF page 2

 01 Cassandra DBA Roadmap
 How to use this guide

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Learn Cassandra from the distributed-systems                      Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       fundamentals through cluster operations, data modeling,           relevant to this topic. Confirm command support with the
       repair, backup, monitoring, security, automation and              exact release and local help output.
       production incident response. Perform labs on isolated
       VMs.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 2

## Source PDF page 3

 02 Introduction to Apache Cassandra
 What Cassandra is designed for

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Apache Cassandra is a distributed wide-column NoSQL               Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       database designed for high availability and horizontal            relevant to this topic. Confirm command support with the
       scalability. It distributes data across nodes and avoids a        exact release and local help output.
       single master for normal read/write operations.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 3

## Source PDF page 4

 03 Cassandra Architecture
 Peer-to-peer and ring concepts

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Cassandra nodes are peers. Data is distributed using              Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       partitioning and replication. Understand cluster, data            relevant to this topic. Confirm command support with the
       center, rack, node, token, vnode, gossip, coordinator and         exact release and local help output.
       replica.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 4

## Source PDF page 5

 04 Cluster, Data Center and Rack
 Topology-aware design

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       A cluster contains one or more data centers. Racks                Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       represent failure domains. Configure accurate snitch and          relevant to this topic. Confirm command support with the
       rack/DC metadata so replica placement and consistency             exact release and local help output.
       behave as intended.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 5

## Source PDF page 6

 05 Node Roles and Responsibilities
 Coordinator and replica nodes

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Any node can coordinate a client request. Replica nodes           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       store the relevant partition. Learn coordinator, seed node,       relevant to this topic. Confirm command support with the
       bootstrap node, joining node, replacement node and                exact release and local help output.
       decommissioned node.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 6

## Source PDF page 7

 06 Installation Prerequisites
 Linux, Java, storage and networking

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check supported Java version for the exact Cassandra              Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       release, Linux limits, disk layout, time synchronization,         relevant to this topic. Confirm command support with the
       DNS, firewall and ownership. Avoid mixing package and             exact release and local help output.
       tarball installation conventions.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 7

## Source PDF page 8

 07 Install Cassandra 4.1.x
 Lab installation workflow

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use the official repository or release archive for the            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       selected version. Verify package signatures/checksums             relevant to this topic. Confirm command support with the
       where provided, configure paths and service user, then            exact release and local help output.
       start one node and validate with nodetool status.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 8

## Source PDF page 9

 08 Cassandra Configuration
 Understand cassandra.yaml

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Review cluster_name, listen_address, rpc_address,                 Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       seeds, endpoint_snitch, data_file_directories,                    relevant to this topic. Confirm command support with the
       commitlog_directory, saved_caches_directory,                      exact release and local help output.
       num_tokens and authenticator/authorizer settings.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                              Page 9

## Source PDF page 10

 09 Directory Structure and Data Files
 Where Cassandra stores information

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Understand data directories, commit log, saved caches,            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       hints, logs and configuration. Inspect actual paths from          relevant to this topic. Confirm command support with the
       cassandra.yaml and service configuration; do not                  exact release and local help output.
       assume every installation uses /var/lib/cassandra.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 10

## Source PDF page 11

 10 Starting, Stopping and Service Control
 Operate nodes safely

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use systemctl status/start/stop/restart cassandra where           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       package-managed. For tarball deployments use the                  relevant to this topic. Confirm command support with the
       documented scripts and service manager. Check logs                exact release and local help output.
       and nodetool status after every operation.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 11

## Source PDF page 12

 11 CQL Fundamentals
 Cassandra Query Language

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Learn CREATE KEYSPACE, CREATE TABLE, INSERT,                      Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       SELECT, UPDATE and DELETE. CQL resembles SQL                      relevant to this topic. Confirm command support with the
       but Cassandra data modeling is query-driven and does              exact release and local help output.
       not provide relational joins or arbitrary ad hoc querying.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 12

## Source PDF page 13

 12 Keyspaces and Replication
 Define data placement

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       A keyspace defines replication strategy and replication           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       factor. Prefer NetworkTopologyStrategy for production             relevant to this topic. Confirm command support with the
       multi-DC designs. SimpleStrategy is for simple                    exact release and local help output.
       single-DC/testing scenarios, not production multi-DC.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 13

## Source PDF page 14

 13 Replication Factor
 Copies of each partition

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       RF defines the number of replicas for each data center.           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       Choose RF based on availability, consistency, storage             relevant to this topic. Confirm command support with the
       cost and failure-domain design. RF=3 is common in                 exact release and local help output.
       many production patterns but is not universal.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 14

## Source PDF page 15

 14 Partition Keys and Clustering Columns
 Design tables around queries

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       The partition key determines data distribution and replica        Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       placement. Clustering columns determine ordering within           relevant to this topic. Confirm command support with the
       a partition. Design tables for known access patterns and          exact release and local help output.
       avoid unbounded partitions.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 15

## Source PDF page 16

 15 Data Types and Collections
 Model application records

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Learn text, int, bigint, timestamp, uuid, timeuuid, decimal,      Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       boolean, blob, list, set, map, tuple and user-defined             relevant to this topic. Confirm command support with the
       types. Use collections carefully; large or frequently             exact release and local help output.
       mutated collections can create operational problems.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 16

## Source PDF page 17

 16 Primary Keys and Query Patterns
 Avoid relational modeling assumptions

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       A Cassandra primary key consists of partition key and             Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       optional clustering columns. Queries generally need the           relevant to this topic. Confirm command support with the
       partition key. Model separate tables for separate query           exact release and local help output.
       patterns rather than relying on joins.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 17

## Source PDF page 18

 17 Consistency Levels
 Read/write consistency trade-offs

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Learn ONE, TWO, THREE, QUORUM, ALL,                               Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       LOCAL_QUORUM, EACH_QUORUM, LOCAL_ONE and                          relevant to this topic. Confirm command support with the
       SERIAL. For a single DC, quorum math often uses R + W             exact release and local help output.
       > RF for strong overlap, while multi-DC semantics need
       careful local/global interpretation.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 18

## Source PDF page 19

 18 Read Path
 How Cassandra serves reads

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       A coordinator routes a read to replicas. Understand               Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       memtables, SSTables, bloom filters, partition                     relevant to this topic. Confirm command support with the
       summaries/indexes, caches, read repair behavior by                exact release and local help output.
       version and digest comparisons. Use tracing and metrics
       to diagnose latency.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 19

## Source PDF page 20

 19 Write Path
 Commit log, memtable and SSTable

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       A write is acknowledged according to consistency level            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       after required replica processing. Data is recorded in the        relevant to this topic. Confirm command support with the
       commit log and memtable, then flushed to immutable                exact release and local help output.
       SSTables. Understand durability and write amplification.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 20

## Source PDF page 21

 20 Commit Log and Memtables
 Durability and in-memory writes

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       The commit log supports recovery after a crash;                   Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       memtables accumulate writes before flush. Monitor                 relevant to this topic. Confirm command support with the
       commit log disk usage, flush activity and memory                  exact release and local help output.
       pressure. Never delete active commit log files manually.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 21

## Source PDF page 22

 21 SSTables and Compaction
 Immutable storage files

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       SSTables are immutable sorted files. Compaction                   Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       merges SSTables, removes obsolete data where safe                 relevant to this topic. Confirm command support with the
       and affects disk, CPU and I/O. Understand compaction              exact release and local help output.
       throughput, pending tasks and disk headroom.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 22

## Source PDF page 23

 22 Compaction Strategies
 STCS, LCS and TWCS

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       SizeTieredCompactionStrategy is common for                        Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       write-heavy/general workloads;                                    relevant to this topic. Confirm command support with the
       LeveledCompactionStrategy targets read efficiency with            exact release and local help output.
       more write amplification;
       TimeWindowCompactionStrategy fits time-series/TTL
       patterns when designed correctly.

       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 23

## Source PDF page 24

 23 Tombstones and TTL
 Deletion markers and read cost

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Deletes and expired TTL data create tombstones that               Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       remain until compaction and grace-period conditions               relevant to this topic. Confirm command support with the
       permit removal. Avoid excessive tombstones, very short            exact release and local help output.
       TTL patterns and unsafe tombstone_gc_grace_seconds
       changes.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 24

## Source PDF page 25

 24 Hints and Hint Replay
 Temporary replica unavailability

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Hints can help deliver missed mutations when a replica            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       returns, within configured limits. Hints are not a substitute     relevant to this topic. Confirm command support with the
       for repair. Monitor hint storage and replay behavior after        exact release and local help output.
       node outages.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 25

## Source PDF page 26

 25 Gossip and Failure Detection
 How nodes learn cluster state

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Gossip exchanges node state and metadata. Failure                 Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       detection is based on observations and thresholds, not a          relevant to this topic. Confirm command support with the
       definitive network truth. Investigate network, GC pauses          exact release and local help output.
       and node health before assuming a node is permanently
       dead.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 26

## Source PDF page 27

 26 Snitches and Topology
 Replica placement awareness

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Snitches map nodes to racks and data centers.                     Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       Understand GossipingPropertyFileSnitch and                        relevant to this topic. Confirm command support with the
       cloud/topology-aware snitches supported by the selected           exact release and local help output.
       release. Incorrect topology can undermine fault
       tolerance.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 27

## Source PDF page 28

 27 Tokens and Vnodes
 Distribute partitions across nodes

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       The partitioner hashes partition keys into tokens. Vnodes         Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       assign multiple token ranges per node to distribute               relevant to this topic. Confirm command support with the
       ownership. Learn token ownership, bootstrap streaming             exact release and local help output.
       and balancing implications.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 28

## Source PDF page 29

 28 nodetool Essentials
 Daily command reference

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Practice nodetool status, info, version, describecluster,         Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       ring, tpstats, compactionstats, tablestats, cfstats where         relevant to this topic. Confirm command support with the
       supported, netstats, gcstats and statusbinary. Confirm            exact release and local help output.
       command support in your Cassandra version.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 29

## Source PDF page 30

 29 Cluster Health Checks
 Assess node and cluster state

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check UN status, node load, ownership, gossip, native             Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       transport, thread pools, compactions, dropped                     relevant to this topic. Confirm command support with the
       messages, disk, JVM and logs. A node showing UN                   exact release and local help output.
       alone does not prove full application health.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 30

## Source PDF page 31

 30 Repair Concepts
 Anti-entropy and replica consistency

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Repair compares replica data and streams differences.             Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       Understand incremental versus full repair behavior for            relevant to this topic. Confirm command support with the
       your version, repair scope, repair scheduling, validation         exact release and local help output.
       and the role of gc_grace_seconds.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 31

## Source PDF page 32

 31 Run nodetool repair
 Repair safely in production

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Plan repair by keyspace/table and node/DC scope.                  Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       Monitor streaming, compaction and disk load. Avoid                relevant to this topic. Confirm command support with the
       launching overlapping repairs indiscriminately. Confirm           exact release and local help output.
       repair completion and review logs/metrics.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 32

## Source PDF page 33

 32 Backup and Restore
 Snapshots and commit log archiving

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Cassandra backups commonly use snapshots plus                     Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       commit log archiving for point-in-time recovery designs.          relevant to this topic. Confirm command support with the
       Understand snapshot size, hard links, SSTable files,              exact release and local help output.
       schema capture, consistency and off-node copies.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 33

## Source PDF page 34

 33 Snapshots with nodetool
 Create and manage snapshots

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use nodetool snapshot with a clear tag and                        Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       keyspace/table scope. Inspect snapshot directories,               relevant to this topic. Confirm command support with the
       record metadata, copy data to protected backup storage            exact release and local help output.
       and remove snapshots only after retention and backup
       verification.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 34

## Source PDF page 35

 34 Restore Procedures
 Recover tables and nodes

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Restore SSTables and schema according to the selected             Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       recovery scenario and version documentation.                      relevant to this topic. Confirm command support with the
       Distinguish table restore, node replacement, full-cluster         exact release and local help output.
       recovery and point-in-time recovery. Always test in an
       isolated environment.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 35

## Source PDF page 36

 35 JVM and Garbage Collection
 Heap, pauses and memory pressure

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Understand heap sizing, young/old generation behavior             Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       for the chosen JVM, GC pauses and off-heap memory.                relevant to this topic. Confirm command support with the
       Monitor GC logs, nodetool gcstats, process RSS and                exact release and local help output.
       container/host limits.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 36

## Source PDF page 37

 36 Performance Monitoring
 Latency, throughput and saturation

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Track read/write latency, request rate, pending tasks,            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       dropped messages, compaction backlog, disk latency,               relevant to this topic. Confirm command support with the
       heap, GC pauses, cache hit behavior and coordinator               exact release and local help output.
       load. Compare trends to a known baseline.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 37

## Source PDF page 38

 37 Thread Pools and Dropped Messages
 Find overloaded stages

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use nodetool tpstats and version-appropriate metrics to           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       inspect pending, active and blocked tasks. Dropped                relevant to this topic. Confirm command support with the
       messages indicate work not processed in time; identify            exact release and local help output.
       the stage and root cause before tuning queues.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 38

## Source PDF page 39

 38 Linux Operations for Cassandra
 OS-level DBA checks

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use top, free -h, vmstat, iostat, sar, df -hT, df -i, lsblk,      Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       lsof, ss and journalctl. Check disk latency, inode                relevant to this topic. Confirm command support with the
       exhaustion, memory pressure, file descriptors and                 exact release and local help output.
       network errors.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 39

## Source PDF page 40

 39 Security: Authentication and Authorization
 Protect client and administrative access

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Understand authenticator, authorizer, roles, permissions,         Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       password policy and least privilege. Validate behavior            relevant to this topic. Confirm command support with the
       against the Cassandra version and avoid leaving default           exact release and local help output.
       credentials enabled.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 40

## Source PDF page 41

 40 TLS and Encryption
 Secure client and internode traffic

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Configure client-to-node and internode encryption with            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       trusted certificates, correct SANs, expiry monitoring and         relevant to this topic. Confirm command support with the
       protected private keys. Plan certificate rotation and test        exact release and local help output.
       node-to-node trust before production rollout.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 41

## Source PDF page 42

 41 Audit Logging
 Record database access events

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Define audit scope, retention, secure log storage and             Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       access controls. Audit logging adds overhead and must             relevant to this topic. Confirm command support with the
       be sized and monitored. Verify the implementation and             exact release and local help output.
       configuration supported by the deployed edition/version.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 42

## Source PDF page 43

 42 Multi-Data-Center Design
 Locality, RF and consistency

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Design NetworkTopologyStrategy RF per DC, seed                    Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       strategy, client locality and LOCAL_QUORUM behavior.              relevant to this topic. Confirm command support with the
       Understand inter-DC traffic, replication latency, failover        exact release and local help output.
       assumptions and operational ownership.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 43

## Source PDF page 44

 43 Adding a Node
 Bootstrap and streaming

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Prepare hardware, network, configuration and topology.            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       Add a node using the documented bootstrap procedure;              relevant to this topic. Confirm command support with the
       monitor streaming, disk, compactions and load                     exact release and local help output.
       distribution. Validate status and ownership after
       completion.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 44

## Source PDF page 45

 44 Replacing and Removing Nodes
 Decommission, replace and rebuild

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Distinguish decommissioning a healthy node, replacing a           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       failed node and rebuilding a node. Follow exact                   relevant to this topic. Confirm command support with the
       version-specific steps; verify token ownership, streaming         exact release and local help output.
       and replica availability before proceeding.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 45

## Source PDF page 46

 45 Node Down Incident
 Diagnose before recovery action

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check host reachability, service state, logs, disk,               Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       memory, GC, network and gossip. Determine whether                 relevant to this topic. Confirm command support with the
       the node is temporarily unavailable or permanently lost.          exact release and local help output.
       Avoid unsafe remove-node operations before failure
       assessment.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 46

## Source PDF page 47

 46 High Read Latency Incident
 Investigate read path and data model

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check coordinator and replica latency, partition size,            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       tombstones, SSTable count, compaction backlog, disk               relevant to this topic. Confirm command support with the
       latency, cache behavior and query patterns. Use tracing           exact release and local help output.
       selectively and compare with baseline.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 47

## Source PDF page 48

 47 High Write Latency Incident
 Investigate write path

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check commit log sync, disk latency, memtable flushes,            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       coordinator pressure, replica availability, consistency           relevant to this topic. Confirm command support with the
       level, GC and dropped messages. Determine whether                 exact release and local help output.
       latency is client, coordinator or replica-side.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 48

## Source PDF page 49

 48 Pending Compactions Incident
 Restore maintenance capacity

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Inspect nodetool compactionstats, disk throughput,                Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       SSTable count, compaction strategy and free space. Find           relevant to this topic. Confirm command support with the
       why compaction cannot keep up; do not blindly increase            exact release and local help output.
       compaction throughput without checking I/O headroom.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 49

## Source PDF page 50

 49 Tombstone Overload Incident
 Diagnose scans and deletion patterns

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Review tombstone warnings, query restrictions,                    Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       TTL/deletion patterns, partition size and compaction. Fix         relevant to this topic. Confirm command support with the
       data model/query behavior and plan repair/compaction              exact release and local help output.
       carefully; do not lower grace periods casually.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 50

## Source PDF page 51

 50 Disk Full Incident
 Protect data and node stability

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check df -hT, df -i, du on known directories, snapshots,          Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       commit logs, hints and SSTable growth. Do not manually            relevant to this topic. Confirm command support with the
       delete live SSTables or commit logs. Use documented               exact release and local help output.
       cleanup and capacity procedures.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 51

## Source PDF page 52

 51 Authentication Failure Incident
 Troubleshoot access safely

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check role existence, grants, authenticator configuration,        Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       password validity, client auth settings, TLS and logs.            relevant to this topic. Confirm command support with the
       Avoid reverting to AllowAllAuthenticator as a production          exact release and local help output.
       workaround.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 52

## Source PDF page 53

 52 Repair and Streaming Incident
 Diagnose slow or failed repair

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Inspect repair logs, nodetool netstats, streaming state,          Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       disk, network, pending compactions and node                       relevant to this topic. Confirm command support with the
       availability. Confirm repair scope and whether another            exact release and local help output.
       repair or bootstrap operation is active.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 53

## Source PDF page 54

 53 Prometheus and Grafana
 Build Cassandra observability

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use a compatible JMX exporter or supported metrics                Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       integration. Collect node health, latency, compaction,            relevant to this topic. Confirm command support with the
       thread pool, dropped messages, JVM, disk and repair               exact release and local help output.
       metrics. Protect JMX and exporter endpoints.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 54

## Source PDF page 55

 54 JMX and Remote Management
 Operate management interfaces securely

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Understand JMX ports, authentication, authorization, TLS          Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       and exporter access. Bind management interfaces                   relevant to this topic. Confirm command support with the
       appropriately and firewall them. Never expose                     exact release and local help output.
       unauthenticated JMX publicly.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 55

## Source PDF page 56

 55 Ansible for Cassandra
 Automate controlled operations

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Use inventories, templates, variables and handlers for            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       repeatable configuration. Store secrets securely, use             relevant to this topic. Confirm command support with the
       staged rollout and validate one node at a time. Avoid             exact release and local help output.
       automation that restarts an entire cluster simultaneously.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 56

## Source PDF page 57

 56 Bash and Python DBA Automation
 Health checks and reporting

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Automate nodetool status parsing, disk checks, service            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       state, backup verification and metrics reporting. Use             relevant to this topic. Confirm command support with the
       timeouts, structured logs, error handling and explicit exit       exact release and local help output.
       codes.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 57

## Source PDF page 58

 57 Capacity Planning
 Forecast nodes, disks and throughput

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Measure compressed and uncompressed data,                         Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       replication factor, compaction temporary space,                   relevant to this topic. Confirm command support with the
       snapshots, commit logs, hints and growth. Include                 exact release and local help output.
       repair/streaming headroom and failure capacity in
       estimates.



       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 58

## Source PDF page 59

 58 Rolling Restart and Maintenance
 Preserve cluster availability

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Check cluster health, repair status, backups, workload            Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       and maintenance window. Restart one node at a time,               relevant to this topic. Confirm command support with the
       wait for it to return UN and validate before moving to the        exact release and local help output.
       next node.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 59

## Source PDF page 60

 59 Upgrade Planning
 Version compatibility and rolling upgrades

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Read release notes and upgrade documentation for                  Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       source and target versions. Check Java, SSTable                   relevant to this topic. Confirm command support with the
       compatibility, features, drivers, schema, repair state and        exact release and local help output.
       rollback limits. Test on a representative cluster first.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 60

## Source PDF page 61

 60 Cassandra 4.1 and 5.x Differences
 Version-aware operations

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Do not assume commands, defaults, metrics, storage                Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       behavior or features are identical across major releases.         relevant to this topic. Confirm command support with the
       Check the exact release documentation and run nodetool            exact release and local help output.
       help on each target version.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 61

## Source PDF page 62

 61 Production DBA Runbook
 Operational checklist and readiness

       LEARNING OBJECTIVE Understand the concept, perform the practical check and explain the DBA impact.



       1. Core concept                                                   2. Commands / configuration

       Daily: node status, disk, latency, compactions, dropped           Use nodetool, cqlsh, Cassandra YAML and Linux utilities
       messages, backups and alerts. Weekly: repair progress,            relevant to this topic. Confirm command support with the
       growth, GC and security. Monthly: capacity, upgrades,             exact release and local help output.
       DR restore evidence and access review.




       3. Practical lab                                                  4. Validation

       Perform the task on the 3-node lab one node or operation          Check nodetool status, logs, relevant metrics, client
       at a time. Record commands, outputs, node state and               connectivity and data correctness. A node being UN does
       any errors.                                                       not alone prove application health.




       5. Production precaution                                          6. Interview checkpoint

       Check RF, consistency level, topology, repair state,              Explain the design choice, failure mode, monitoring
       backup, disk headroom and impact before making                    signal, safe remediation and how you prove the cluster is
       changes. Use an approved runbook.                                 healthy again.




       DBA PRACTICE CHECK
       Can you perform this task from memory, explain the output, identify the risk and describe how you would validate it in
       production?



 Key takeaway: Cassandra operations are distributed-systems operations. Preserve replica consistency, understand topology, protect data and
 validate every node-level change.




Cassandra Database Administrator | Practical Learning Guide                                                                             Page 62