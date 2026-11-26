# Cassandra DBA Beginner-to-Advanced Practical Workbook – searchable text transcription

> Source: user-provided PDF (28 pages). This Markdown file preserves extracted page text and page references for repository search. It does not reproduce the original PDF layout or embedded graphics. Use the source PDF for exact visual formatting.


## Source PDF page 1

                CASSANDRA DATABASE
                   ADMINISTRATOR
         Beginner-to-Advanced Practical
                   Workbook

A step-by-step learning path for installation, data modelling, cluster operations, backup and
             recovery, monitoring, production troubleshooting and interviews.




                             Practical lab baseline
 CentOS Stream 9 • Apache Cassandra 4.1.12 • Three-node cluster • Linux shell • cqlsh •
                                    nodetool




  Designed as a hands-on DBA training workbook. Work through the modules in order,
    execute the lab tasks, record your results, and only then move to the next level.




                        Version 1.0 | Prepared 12 November 2026

## Source PDF page 2

 How to use this workbook
 This is a guided lab, not a command catalogue. Follow the sequence. Do not run destructive commands on a production
 cluster or on a lab that contains data you need.
●    Read: understand the concept in plain language first.
●    Build: perform the exact lab steps and record your hostnames, IP addresses and outputs.
●    Validate: use the verification commands after each change.
●    Explain: answer the checkpoint questions aloud as if you were in a DBA interview.
●    Operate safely: take a snapshot or backup before exercises that modify or remove data.

 Lab assumptions: The examples use three Linux VMs named cassandra1, cassandra2 and cassandra3. Replace the
 sample IPs with your actual lab addresses. The examples assume a private, trusted lab network. Production deployments
 need security, capacity, monitoring, change control and tested recovery procedures.

 Important: Cassandra configuration and operational behaviour can vary by release and packaging. This workbook
 targets Apache Cassandra 4.1.x (including 4.1.12). Confirm paths and command options against the exact package
 installed. Never copy settings blindly between Cassandra 3.x, 4.1.x and 5.x.


 Learning roadmap
    Stage                Modules                        Outcome

    Beginner             1–5                            Understand Cassandra, Linux prerequisites, installation, service control and CQL.

    Intermediate         6–10                           Design data models, consistency, replication, health checks and routine operations.

    Advanced             11–15                          Repair, backup/restore, performance, JVM, monitoring and security.

    Production DBA       16–19                          Failure handling, maintenance, capacity, change control and incident runbooks.

    Interview readiness 20                              Scenario-based answers, command drills and a practical assessment.




 Contents
    1. Cassandra fundamentals and architecture

    2. Lab design and Linux prerequisites

    3. Install Java and Cassandra 4.1.x

    4. Configure and build a three-node cluster

    5. cqlsh and CQL fundamentals

    6. Data modelling: keys, partitions and clustering

    7. Replication, consistency and read/write behaviour

    8. Node health and essential nodetool operations

    9. Routine cluster operations

    10. Hints, gossip, snitches and topology

    11. Repair, compaction and tombstones

    12. Backup and restore

    13. Performance troubleshooting

    14. JVM, memory, disk and Linux diagnostics




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                                    Page 2

## Source PDF page 3

    15. Monitoring with JMX, Prometheus and Grafana

    16. Security and access control

    17. Production incident playbooks

    18. Maintenance, scaling and upgrades

    19. DBA daily/weekly/monthly runbooks

    20. Interview preparation and final practical assessment




Cassandra DBA Beginner-to-Advanced Practical Workbook          Page 3

## Source PDF page 4

 1. Cassandra fundamentals and architecture
 1.1 What is Cassandra?
 Apache Cassandra is a distributed NoSQL database designed to store data across multiple nodes. Instead of depending
 on one central server, nodes cooperate as peers. Data is distributed using partition keys and replicated according to the
 keyspace replication strategy.

 Think of a cluster as a team of storage servers. A request can be served by different nodes, and copies of data can exist
 on multiple nodes. This supports availability and horizontal scale, but it also means the DBA must understand
 partitioning, replication, consistency, repair and failure handling.

 1.2 Core architecture
    Component             Plain-language meaning                               DBA responsibility

    Node                  One Cassandra server process                         Service health, disk, memory, logs, capacity

    Cluster               A group of cooperating nodes                         Topology, availability, upgrades, monitoring

    Data centre (DC)      A logical group of nodes, often aligned to a site/region
                                                                                 Replication and failure-domain design

    Rack                  A failure-domain grouping within a DC                Rack-aware replica placement

    Keyspace              Namespace and replication configuration              Choose correct replication strategy and RF

    Table                 Rows organised by a primary key                      Model queries and prevent hot partitions

    Partition             Rows sharing the same partition key                  Control partition size and distribution

    SSTable               Immutable on-disk table file                         Compaction, disk capacity, backup



 1.3 Cassandra write path – simplified
●     The coordinator receives the client request. It may be any node the client contacts.
●     The coordinator identifies the replicas responsible for the partition.
●     Replicas append the mutation to the commit log for durability and update the memtable in memory.
●     Acknowledgements are returned when the requested consistency level is satisfied.
●     Memtables are later flushed to immutable SSTables on disk.
●     Compaction merges SSTables and removes obsolete data when safe.

 1.4 Cassandra read path – simplified
●     The coordinator routes the read to replicas based on the partition key and consistency level.
●     Replicas consult in-memory structures and relevant SSTables, using indexes and filters to locate data.
●     The coordinator reconciles replica responses and may trigger read repair behaviour depending on the operation and
      version settings.
●     Poor partition design, too many SSTables, tombstones, disk latency or replica inconsistency can increase read
      latency.

 Checkpoint
●     Why is Cassandra called peer-to-peer?
●     What is the difference between a node, cluster, DC and rack?
●     Why are SSTables immutable?
●     What does the coordinator do?




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                         Page 4

## Source PDF page 5

●    Why does a good Cassandra data model start with the query?


 2. Lab design and Linux prerequisites
 2.1 Three-node lab topology
    VM                         Example private IP                   Role

    cassandra1                 192.168.62.131                       Seed candidate and regular data node

    cassandra2                 192.168.62.132                       Regular data node

    cassandra3                 192.168.62.133                       Regular data node


 Use the actual IP addresses from your VMs. Keep all nodes on the same private lab network. A seed node is used for
 contact information during gossip startup; it is not a master and does not own all writes.

 2.2 Set hostnames and name resolution
    # Run on each VM with its own hostname
    sudo hostnamectl set-hostname cassandra1
    hostnamectl

    # Add the same mapping on all three VMs
    sudo vi /etc/hosts
    192.168.62.131 cassandra1
    192.168.62.132 cassandra2
    192.168.62.133 cassandra3

    # Validate name resolution and reachability
    getent hosts cassandra1 cassandra2 cassandra3
    ping -c 2 cassandra2

 On cassandra2 and cassandra3, set their own hostname accordingly. Confirm that each host resolves all three names
 consistently.

 2.3 Operating-system baseline checks
    cat /etc/centos-release
    uname -r
    lscpu
    free -h
    df -hT
    lsblk
    ip -br address
    timedatectl
    ulimit -n

 Record CPU, RAM, swap, filesystem type, free disk, network interface and time synchronisation. Cassandra is sensitive
 to disk latency, memory pressure, file descriptor limits and network stability.

 2.4 Network ports
    Port               Purpose                                             Exposure guidance

    7000               Inter-node internode communication (unencrypted)    Private cluster network only

    7001               Encrypted internode communication when configured   Private cluster network only

    9042               Native transport / CQL clients                      Only approved application and admin networks

    7199               JMX management                                      Restrict to trusted admin/monitoring hosts; secure JMX

    22                 SSH administration                                  Restrict to approved administrators


 Do not expose Cassandra ports to the public internet. Do not disable the firewall as a generic fix. Create narrowly scoped
 rules for the actual cluster subnet and required client/monitoring hosts.

 Lab task


Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                           Page 5

## Source PDF page 6

●    Confirm all three VMs can resolve each other's hostnames.
●    Confirm time is synchronised on all nodes.
●    Record free disk space and RAM on every VM.
●    Create a change log with date, node, change, operator and validation result.


 3. Install Java and Cassandra 4.1.x
 3.1 Confirm Java requirement
 Cassandra 4.1 supports specific Java runtime versions. For a controlled 4.1.12 lab, use a Java version supported by the
 exact Cassandra 4.1 release documentation and your package. Java 11 is a conservative baseline commonly used for
 Cassandra 4.1 deployments.
    java -version
    rpm -qa | grep -E 'java|openjdk' | sort


 3.2 Install a supported Java runtime
    # Example for CentOS Stream 9 where the package is available
    sudo dnf install -y java-11-openjdk java-11-openjdk-headless
    java -version

 If the package is unavailable in your enabled repositories, check repository configuration and the supported vendor
 package options. Do not download an arbitrary JDK from an untrusted mirror.

 3.3 Obtain Cassandra 4.1.12
 Use the official Apache Cassandra download/archive distribution or an organisation-approved internal repository. Verify
 the downloaded archive checksum or signature using the verification material published for that release.
    # Example workflow after obtaining the approved archive
    cd /opt
    sudo tar -xzf apache-cassandra-4.1.12-bin.tar.gz
    sudo ln -sfn /opt/apache-cassandra-4.1.12 /opt/cassandra
    sudo chown -R root:root /opt/apache-cassandra-4.1.12
    /opt/cassandra/bin/cassandra -v

 The archive filename and download URL depend on the official distribution source. Verify the checksum/signature before
 installation. Do not run a production service as root.

 3.4 Create the service account and directories
    sudo groupadd --system cassandra
    sudo useradd --system --gid cassandra --home-dir /var/lib/cassandra \\
      --shell /sbin/nologin cassandra

    sudo mkdir -p /var/lib/cassandra/{data,commitlog,saved_caches,hints}
    sudo mkdir -p /var/log/cassandra
    sudo chown -R cassandra:cassandra /var/lib/cassandra /var/log/cassandra

 If the account or group already exists, inspect it with id cassandra before creating it again. Keep software binaries
 root-owned and writable data/log directories owned by the Cassandra service account.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                    Page 6

## Source PDF page 7

 3.5 Create a systemd service
   sudo vi /etc/systemd/system/cassandra.service

   [Unit]
   Description=Apache Cassandra
   After=network-online.target
   Wants=network-online.target

   [Service]
   Type=forking
   User=cassandra
   Group=cassandra
   Environment=JAVA_HOME=/usr
   Environment=CASSANDRA_HOME=/opt/cassandra
   ExecStart=/opt/cassandra/bin/cassandra -p /run/cassandra/cassandra.pid
   PIDFile=/run/cassandra/cassandra.pid
   Restart=on-failure
   LimitNOFILE=100000
   TimeoutStartSec=180

   [Install]
   WantedBy=multi-user.target

 Create the runtime directory with suitable ownership using a systemd RuntimeDirectory setting or a tmpfiles rule. Validate
 the service unit against the exact Cassandra startup script and packaging. Some packaged installations provide their own
 unit; do not overwrite it without review.
   sudo systemctl daemon-reload
   sudo systemctl cat cassandra
   sudo systemctl enable cassandra


 3.6 First-start validation (single node only)
   sudo systemctl start cassandra
   sudo systemctl status cassandra --no-pager
   sudo journalctl -u cassandra -n 100 --no-pager
   tail -n 100 /var/log/cassandra/system.log
   /opt/cassandra/bin/nodetool status

 For this first validation, use a temporary single-node configuration or keep the other nodes stopped until cluster
 configuration is ready. Confirm the process is healthy before proceeding.

 Common installation issues
   Symptom                                    Likely checks

   Service exits immediately                  journalctl, system.log, Java version, YAML indentation, permissions

   Permission denied                          Check ownership of data, commitlog, saved_caches and log directories

   Address already in use                     Check ss -lntp; identify old Cassandra process before restart

   Java not found                             Check JAVA_HOME and systemd environment

   Cannot write PID file                      Check runtime directory exists and is writable by service account




 4. Configure and build a three-node cluster
 4.1 Configuration files
 The primary configuration is cassandra.yaml. The exact path depends on installation method; for the archive layout it is
 usually under /opt/cassandra/conf/. Edit the file on each node, changing node-specific values carefully.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                  Page 7

## Source PDF page 8

 4.2 Configure each node
    # Shared settings in cassandra.yaml on all three nodes
    cluster_name: 'VJ_CASSANDRA_LAB'
    num_tokens: 16
    endpoint_snitch: GossipingPropertyFileSnitch

    seed_provider:
      - class_name: org.apache.cassandra.locator.SimpleSeedProvider
        parameters:
          - seeds: "192.168.62.131"

    # Node-specific examples:
    # cassandra1:
    listen_address: 192.168.62.131
    rpc_address: 192.168.62.131

    # cassandra2:
    # listen_address: 192.168.62.132
    # rpc_address: 192.168.62.132

    # cassandra3:
    # listen_address: 192.168.62.133
    # rpc_address: 192.168.62.133

    # Keep native_transport_port at 9042 unless intentionally changed.

 Do not paste all three listen_address examples into one YAML file. Each node must have exactly one correct
 listen_address and rpc_address. Never use 0.0.0.0 as listen_address. rpc_address controls the client interface;
 broadcast settings may be required in NAT or multi-interface networks.

 4.3 Set DC and rack
    # /opt/cassandra/conf/cassandra-rackdc.properties
    dc=DC1
    rack=RACK1

 For a simple lab, all three nodes can use DC1 but should ideally be placed in distinct rack labels only if the lab is
 modelling separate failure domains. Do not claim physical rack diversity when all VMs share one host.

 4.4 Start nodes in a controlled sequence
    # On all nodes: validate config, ownership and network first
    grep -E 'cluster_name|num_tokens|listen_address|rpc_address|seeds|endpoint_snitch' \\
      /opt/cassandra/conf/cassandra.yaml
    namei -l /var/lib/cassandra
    ss -lntp | grep -E '7000|7199|9042'

    # Start seed candidate first
    sudo systemctl start cassandra
    sudo systemctl status cassandra --no-pager

    # Then start node 2, validate; then node 3, validate
    sudo systemctl start cassandra


 4.5 Validate membership
    /opt/cassandra/bin/nodetool status
    /opt/cassandra/bin/nodetool describecluster
    /opt/cassandra/bin/nodetool gossipinfo

 Expected nodetool status should show three nodes with status UN (Up/Normal). Verify the DC, rack, ownership and host
 IDs. Ownership percentages can look unusual in a small vnode lab; do not use them alone as a health indicator.

 If a node joins with the wrong cluster name, wrong DC/rack, duplicate IP, stale data directory or incompatible
 schema/version, stop and investigate. Do not delete system tables or wipe data directories as a first troubleshooting step.

 4.6 Cluster build acceptance checklist
●    All three nodes report UN in nodetool status.
●    All nodes show the intended DC and rack labels.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                    Page 8

## Source PDF page 9

●    Cluster name and Cassandra release are consistent.
●    No repeating errors in system.log.
●    CQL port 9042 is reachable only from intended client hosts.
●    A test keyspace and table can be created and queried.


 5. cqlsh and CQL fundamentals
 5.1 Connect to CQL
    /opt/cassandra/bin/cqlsh 127.0.0.1 9042
    DESCRIBE CLUSTER;
    DESCRIBE KEYSPACES;

 Run cqlsh locally first. For remote connections, confirm native transport is enabled, the node listens on the intended
 interface, firewall rules allow the client, and authentication settings are correct.

 5.2 Create a keyspace
    CREATE KEYSPACE dba_training
    WITH replication = {
      'class': 'NetworkTopologyStrategy',
      'DC1': 3
    }
    AND durable_writes = true;

    DESCRIBE KEYSPACE dba_training;
    USE dba_training;

 NetworkTopologyStrategy is the standard choice for production and multi-DC designs. The replication factor (RF) must
 be set per DC. In a three-node, single-DC lab, RF=3 places three replicas for each partition.

 5.3 Create a table and run basic operations
    CREATE TABLE employee_by_id (
       employee_id uuid PRIMARY KEY,
       employee_name text,
       department text,
       created_at timestamp
    );

    INSERT INTO employee_by_id
    (employee_id, employee_name, department, created_at)
    VALUES (uuid(), 'Anita Rao', 'DBA', toTimestamp(now()));

    SELECT * FROM employee_by_id;

    UPDATE employee_by_id
    SET department = 'Database Engineering'
    WHERE employee_id = <paste-the-uuid-returned-by-your-query>;

    DELETE FROM employee_by_id
    WHERE employee_id = <paste-the-uuid>;

 Cassandra is not a relational database. A primary key is mandatory. Avoid designing tables around arbitrary ad hoc
 filtering. Build tables for known access patterns.

 5.4 Schema inspection and safe practice
    DESCRIBE KEYSPACE dba_training;
    DESCRIBE TABLE dba_training.employee_by_id;
    SELECT keyspace_name, table_name
    FROM system_schema.tables
    WHERE keyspace_name = 'dba_training';

 CQL statements that delete data, drop schema or truncate tables are destructive. Confirm the keyspace/table, take a
 backup when appropriate, and use an approved change window in production.

 Exercise


Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                     Page 9

## Source PDF page 10

●    Create a keyspace with RF=3 using NetworkTopologyStrategy.
●    Create a table with a UUID primary key.
●    Insert five rows and query them by primary key.
●    Describe the keyspace and table.
●    Explain why a query by a non-key column may not be supported efficiently.


 6. Data modelling: keys, partitions and clustering
 6.1 Primary key structure
 A Cassandra primary key consists of a partition key and optional clustering columns. The partition key decides which
 node replicas store the partition. Clustering columns sort rows within that partition.
    CREATE TABLE orders_by_customer (
      customer_id uuid,
      order_date date,
      order_id timeuuid,
      status text,
      total decimal,
      PRIMARY KEY ((customer_id), order_date, order_id)
    ) WITH CLUSTERING ORDER BY (order_date DESC, order_id DESC);


 6.2 Design from the query
    Requirement                                         Model implication

    Get orders for one customer                         customer_id is the partition key

    Newest orders first                                 Use clustering order aligned to query

    Get one order by id                                 Include enough primary-key columns to identify it

    Search by status across all customers               Create a separate query table or use an appropriate search system; do not assume a relation



 6.3 Avoid hot and oversized partitions
●    Avoid a single constant partition key for high-volume traffic.
●    Avoid unbounded time-series partitions. Add a time bucket such as day or month where appropriate.
●    Estimate rows and bytes per partition using expected write volume and retention.
●    Test skew: a few very active tenants can create hot partitions even when total cluster load looks moderate.
●    Do not choose a partition key solely because it is unique; choose it to distribute load and support queries.

 6.4 Example: time-bucketed events
    CREATE TABLE events_by_device_day (
      device_id text,
      event_day date,
      event_time timeuuid,
      event_type text,
      payload text,
      PRIMARY KEY ((device_id, event_day), event_time)
    ) WITH CLUSTERING ORDER BY (event_time DESC);

 This lets an application retrieve one device's events for a given day. The application must query each relevant day bucket
 for wider time ranges.

 Checkpoint
●    Explain partition key versus clustering key.
●    Why can a large partition be a problem?




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                        Page 10

## Source PDF page 11

●    How can you distribute a high-volume time-series workload?
●    Why should a Cassandra table usually serve a specific query pattern?


 7. Replication, consistency and read/write behaviour
 7.1 Replication factor
 RF is the number of replicas of each partition within a data centre. With RF=3 in a three-node DC, each partition has
 three replicas. RF is not the same as the number of nodes in every possible topology.

 7.2 Consistency levels
    Consistency level          Simplified behaviour                                      Typical consideration

    ONE                        One replica responds                                      Lower latency; weaker read/write acknowledgement guarantee

    QUORUM                     A majority of replicas in the relevant scope respond      Common balance for RF=3

    LOCAL_QUORUM               A quorum in the coordinator's local DC responds           Common for multi-DC applications

    ALL                        All required replicas respond                             Strong acknowledgement requirement but lower availability

    ANY                        A write can be acknowledged by a hint in applicable cases Does not mean a replica has applied the write


 For RF=3, quorum is 2. A common quorum intersection rule is R + W > RF for overlapping replica sets, but the actual
 consistency guarantees depend on the operation, topology, consistency level and Cassandra version.

 7.3 Demonstrate consistency with cqlsh
    CONSISTENCY;
    CONSISTENCY QUORUM;
    CONSISTENCY LOCAL_QUORUM;

 Run controlled tests only in the lab. Observe what happens when one node is stopped and compare writes/reads at ONE,
 QUORUM and ALL. Restore the node and validate recovery. Do not run outage experiments against production.

 7.4 Multi-DC fundamentals
 In a multi-DC cluster, define RF independently for each DC with NetworkTopologyStrategy. Applications commonly use
 LOCAL_QUORUM to keep request coordination local and avoid cross-DC latency for normal operations. Cross-DC
 consistency and failover design must be tested, not assumed.

 Interview checkpoint
●    For RF=3, how many acknowledgements are needed for QUORUM?
●    What is the difference between QUORUM and LOCAL_QUORUM?
●    Does RF=3 mean three copies on every node?
●    Why can ALL reduce availability?
●    What does R + W > RF help reason about?




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                            Page 11

## Source PDF page 12

 8. Node health and essential nodetool operations
 8.1 Essential commands
    Command                                         What it tells you

    nodetool status                                 Node state, DC, rack, load and ownership

    nodetool info                                   Node-level information and uptime

    nodetool describecluster                        Cluster name, snitch, schema versions and DC information

    nodetool tpstats                                Thread-pool activity and pending tasks

    nodetool compactionstats                        Current compactions and pending compaction work

    nodetool tablestats                             Table-level statistics

    nodetool proxyhistograms                        Coordinator latency histograms

    nodetool gcstats                                Garbage collection statistics

    nodetool netstats                               Streaming and network activity

    nodetool cfstats / tablestats                   Table statistics; command availability/output can vary by release



 8.2 Build a health snapshot
    date
    hostname -f
    /opt/cassandra/bin/nodetool status
    /opt/cassandra/bin/nodetool info
    /opt/cassandra/bin/nodetool tpstats
    /opt/cassandra/bin/nodetool compactionstats
    /opt/cassandra/bin/nodetool gcstats
    /opt/cassandra/bin/nodetool netstats
    df -hT
    free -h
    iostat -xz 1 5

 Take the snapshot on each node and compare trends. A single command output is not enough to diagnose a
 performance incident.

 8.3 Interpret node states
    State                 Meaning / response

    UN                    Up and Normal; expected steady state

    DN                    Down and Normal; node is not reachable/available

    UJ                    Up and Joining; joining/streaming is in progress

    UL                    Up and Leaving; node removal is in progress

    UM                    Up and Moving; token movement is in progress



 Practice
●     Run each health command on all three nodes.
●     Save outputs with timestamps.
●     Identify the node with highest disk usage and compare its compaction activity.
●     Explain why UN alone does not prove the cluster is healthy.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                   Page 12

## Source PDF page 13

 9. Routine cluster operations
 9.1 Start, stop and restart
    sudo systemctl start cassandra
    sudo systemctl stop cassandra
    sudo systemctl restart cassandra
    sudo systemctl status cassandra --no-pager
    sudo journalctl -u cassandra -n 100 --no-pager

 In production, do not restart all nodes together. Follow a rolling procedure, one node at a time, with health validation and
 an agreed abort condition.

 9.2 Drain before planned stop
 Drain stops accepting new writes and flushes memtables before a planned shutdown. Use it for controlled maintenance
 where appropriate.
    sudo -u cassandra /opt/cassandra/bin/nodetool drain
    sudo systemctl stop cassandra

 After restart, verify node state, logs, schema agreement and application connectivity before proceeding to another node.

 9.3 Flush and snapshot
    # Flush a keyspace/table's memtables to SSTables
    nodetool flush dba_training

    # Take a named snapshot
    nodetool snapshot -t pre_change_20261112 dba_training

    # List snapshots
    nodetool listsnapshots

 A snapshot is a point-in-time set of hard-linked SSTable files. It is not automatically an off-host backup and it does not by
 itself prove recoverability.

 9.4 Schema agreement
    nodetool describecluster
    nodetool gossipinfo

 If nodes disagree on schema version, investigate schema changes, node connectivity and logs. Avoid repeated schema
 changes while agreement is unresolved.

 9.5 Safe rolling restart sequence
●    Confirm cluster is healthy and all nodes are UN.
●    Check no major repair, streaming or compaction activity is in a risky state.
●    Notify stakeholders and confirm application retry behaviour.
●    Drain and stop one node.
●    Perform the approved maintenance and start the node.
●    Wait for UN, check logs, schema agreement, client traffic and metrics.
●    Proceed to the next node only after the previous node is stable.
●    Stop the change if availability, latency or errors breach the agreed threshold.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                    Page 13

## Source PDF page 14

 10. Hints, gossip, snitches and topology
 10.1 Gossip
 Gossip is Cassandra's peer-to-peer mechanism for exchanging node state and membership information. It helps nodes
 learn about failures and topology. Gossip is not a replacement for application health checks or monitoring.

 10.2 Hinted handoff
 When a replica is temporarily unavailable, a coordinator may store a hint so the mutation can be replayed when that
 replica returns, subject to configuration and limits. Hints are a recovery aid, not a substitute for repair.

 10.3 Snitches
 A snitch tells Cassandra which nodes belong to which racks and data centres. GossipingPropertyFileSnitch reads local
 DC/rack settings and propagates topology information. Incorrect DC/rack configuration can lead to incorrect replica
 placement.

 10.4 Validate topology
    cat /opt/cassandra/conf/cassandra-rackdc.properties
    nodetool status
    nodetool describecluster
    nodetool gossipinfo


 Interview checkpoint
●    What problem does gossip solve?
●    What is hinted handoff and what are its limits?
●    Why does rack awareness matter?
●    Why is a seed node not a master node?


 11. Repair, compaction and tombstones
 11.1 Why repair matters
 Repair synchronises replica data and helps resolve inconsistencies caused by missed writes, downtime, hints expiry or
 other events. Repair is a routine operational responsibility. It is not a command to run blindly during a high-load incident.

 11.2 Preview and run a primary-range repair
    # Check available options on the installed release
    nodetool help repair

    # Run a primary-range repair for a keyspace
    nodetool repair -pr dba_training

 Run the repair according to an explicit schedule and capacity plan. In a multi-node cluster, ensure the repair strategy
 covers the intended token ranges and tables. For a simple three-node lab, run primary-range repair node by node and
 validate progress.

 Repair can generate substantial disk, network and CPU load. Do not run overlapping full repairs across all nodes as a
 quick fix. Understand incremental versus full repair semantics for the installed release and your repair tooling.

 11.3 Compaction
 Compaction merges SSTables, improves read efficiency and purges obsolete cells/tombstones when safe. Strategy
 choice depends on workload.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                    Page 14

## Source PDF page 15

    Strategy              Typical workload fit                                  Key consideration

    STCS                  Write-heavy/general workloads with similarly sized SSTables
                                                                                 Can create temporary disk-space pressure during large compactions

    LCS                   Read-heavy workloads where predictable read amplification
                                                                               Morematters
                                                                                    write/compaction I/O and space considerations

    TWCS                  Time-series or TTL-heavy data with time-window lifecycle
                                                                                 Requires disciplined timestamp/TTL patterns and window sizing



 11.4 Tombstones
 Deletes and TTL expiry create tombstones. Cassandra must retain tombstones long enough to prevent deleted data from
 reappearing from replicas that were offline. Large tombstone volumes can increase read work and cause warnings or
 failures.
    nodetool tablestats dba_training
    nodetool compactionstats
    grep -iE 'tombstone|compaction|dropped' /var/log/cassandra/system.log | tail -n 50


 11.5 Troubleshooting high tombstones
●    Identify the exact table and query pattern; inspect warnings and table statistics.
●    Review TTL and delete patterns, including range deletes and frequent updates.
●    Check whether partitions are oversized or queries scan too many rows.
●    Check repair health and whether any replica has been offline beyond relevant grace periods.
●    Do not lower gc_grace_seconds as a quick performance fix; understand the resurrection risk and repair guarantees
     first.
●    Fix the data model or write pattern, then plan remediation and compaction safely.


 12. Backup and restore
 12.1 Backup principles
●    A backup must be stored off the database node or on independent storage.
●    Capture schema as well as SSTable data.
●    Define RPO and RTO before choosing a backup method.
●    Use a consistent naming convention and retention policy.
●    Monitor backup completion, file size and copy integrity.
●    Perform scheduled restore tests. A backup that has never been restored is unproven.

 12.2 Create a snapshot
    # Flush first if your backup procedure requires it
    nodetool flush dba_training

    # Snapshot a keyspace
    nodetool snapshot -t dba_training_20261112 dba_training

    # Inspect snapshot locations and sizes
    nodetool listsnapshots
    find /var/lib/cassandra/data/dba_training -path '*/snapshots/*' -type f -ls

 The exact data directory layout depends on the configured data_file_directories and table ID. Inspect cassandra.yaml
 and use the actual table directory; do not assume a fixed path.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                            Page 15

## Source PDF page 16

 12.3 Copy snapshot off-host
    # Example only: replace paths and remote backup host
    sudo rsync -aH --numeric-ids \\
      /var/lib/cassandra/data/dba_training/ \\
      backupuser@backuphost:/backup/cassandra/node1/dba_training/

    # Record checksums for transferred files
    find /backup/cassandra/node1/dba_training -type f -print0 | \\
      sort -z | xargs -0 sha256sum > /backup/cassandra/node1/SHA256SUMS

 For a production backup, coordinate snapshots across nodes, preserve required metadata and schema, and use a
 supported backup platform/process. Protect backup credentials and encrypt backup data at rest and in transit.

 12.4 Restore strategy overview
 Restore method depends on the failure scope and backup format. For loading SSTables into an existing cluster,
 sstableloader is commonly used after creating the matching schema. For node replacement or full-cluster disaster
 recovery, follow a tested procedure for the exact topology, version and backup tooling.
    # Inspect the loader options for this release
    /opt/cassandra/bin/sstableloader --help

    # Typical shape; use the correct table directory and contact node
    /opt/cassandra/bin/sstableloader -d 192.168.62.131 \\
      /path/to/backup/keyspace/table-<table-id>

 Never copy snapshot SSTables into a live table directory and improvise a restore. Never delete live data directories to
 test recovery. Restore into an isolated test cluster first, verify schema and data, and document the exact recovery steps.

 12.5 Restore-test checklist
●    Provision an isolated restore target with compatible Cassandra version and schema.
●    Confirm backup inventory, checksums, schema and table metadata.
●    Restore using the approved method.
●    Validate row counts, sample records, application queries and consistency.
●    Measure elapsed recovery time against RTO.
●    Record missing objects, permissions, errors and corrective actions.


 13. Performance troubleshooting
 13.1 Start with evidence
 Do not begin by changing heap, compaction strategy or consistency level. Establish the symptom, scope, start time,
 affected nodes, affected tables and recent changes.

    Symptom                           First evidence to collect

    High read latency                 proxyhistograms, table stats, tombstones, SSTable count, disk latency, query pattern

    High write latency                commit log disk latency, dropped messages, thread pools, GC, network and replica availability

    Pending compactions               compactionstats, disk free space, throughput, SSTable generation rate

    Dropped messages                  tpstats, logs, CPU, GC pauses, overload and network

    Uneven node load                  partition distribution, hot keys, token ownership, client routing

    Timeouts                          coordinator logs, replica state, consistency level, network, queue saturation




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                                 Page 16

## Source PDF page 17

 13.2 First-response command bundle
    date
    nodetool status
    nodetool tpstats
    nodetool compactionstats
    nodetool proxyhistograms
    nodetool gcstats
    nodetool netstats
    iostat -xz 1 10
    vmstat 1 10
    free -h
    df -hT
    ss -s
    tail -n 200 /var/log/cassandra/system.log


 13.3 High read latency – workflow
●    Confirm which application query and table are affected; obtain latency percentiles and error rates.
●    Check coordinator histograms and compare all nodes.
●    Inspect table SSTable counts, tombstone warnings, partition sizes and compaction backlog.
●    Check disk await/utilisation and filesystem free space.
●    Review query predicates and partition-key distribution.
●    Check GC pauses, CPU saturation and thread-pool pending tasks.
●    Make one controlled change at a time and compare before/after metrics.

 13.4 High write latency – workflow
●    Check commit log device latency and disk saturation.
●    Check write-stage pending tasks and dropped messages.
●    Check replica availability and consistency level.
●    Check GC pauses, CPU steal and network retransmits.
●    Review batch usage, partition hotspots and write amplification.
●    Do not lower consistency level or increase timeouts as a substitute for root-cause analysis.

 13.5 Pending compactions – workflow
●    Record pending task count and whether it is increasing or decreasing.
●    Check free disk space and temporary space required by compaction.
●    Check disk throughput, latency and competing processes.
●    Review compaction strategy and write rate.
●    Avoid forcing major compaction as a generic fix; it can consume substantial disk and I/O.


 14. JVM, memory, disk and Linux diagnostics
 14.1 Memory basics
 Cassandra uses JVM heap and substantial off-heap/native memory, plus operating-system page cache. Do not assign all
 VM RAM to the Java heap. On small lab VMs, use conservative settings and avoid running other memory-heavy
 services.
    free -h
    ps -eo pid,comm,rss,vsz,%mem --sort=-rss | head
    cat /proc/meminfo | head -n 20




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                          Page 17

## Source PDF page 18

 14.2 JVM and GC checks
    nodetool gcstats
    jcmd <java_pid> VM.flags
    jcmd <java_pid> GC.heap_info
    jstat -gcutil <java_pid> 1000 10

 Use the correct Cassandra Java process PID. Tool availability depends on the installed JDK and permissions. Correlate
 GC pause duration/frequency with application latency and CPU/memory pressure.

 14.3 Disk and filesystem
    df -hT
    df -ih
    du -sh /var/lib/cassandra/*
    iostat -xz 1 10
    lsblk -f
    lsof +L1

 A full data volume can stop writes or destabilise a node. Check inode exhaustion and deleted-but-open files, not only df
 output. Keep adequate free space for compaction and operational recovery.

 14.4 Linux process and network checks
    ps -ef | grep -i cassandra
    top -H -p <java_pid>
    vmstat 1 10
    sar -n DEV 1 10
    ss -lntp
    ss -s
    dmesg -T | tail -n 50


 Common interpretation
    Observation                                         Potential meaning

    High iowait and high device await                   Storage latency or saturation

    Repeated long GC pauses                             Heap pressure, allocation pressure or JVM tuning issue

    Swap activity under load                            Memory pressure; Cassandra latency may degrade

    High CPU with pending tasks                         CPU saturation or overloaded stages

    High retransmits / drops                            Network path or host network issue

    Low free disk                                       Compaction and write safety risk




 15. Monitoring with JMX, Prometheus and Grafana
 15.1 Monitoring layers
●    Cluster: node state, schema agreement, DC/rack, load and availability.
●    Database: read/write latency, timeouts, dropped messages, pending tasks, compaction and repair.
●    JVM: heap, GC pause, threads and process health.
●    Host: CPU, memory, swap, disk latency, free space, network and file descriptors.
●    Application: request rate, p95/p99 latency, errors, retries and connection pool health.

 15.2 JMX security
 Cassandra exposes management metrics through JMX. JMX is powerful and must not be exposed openly. Restrict
 network access, use authentication and TLS where supported by the deployment, and manage credentials securely.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                Page 18

## Source PDF page 19

 15.3 Prometheus JMX exporter concept
 A Java agent can expose selected JMX metrics in Prometheus format. The exporter configuration maps MBean attributes
 to metric names. Validate the exporter version and Java compatibility before deploying.
    # Illustrative JVM agent pattern; paths and ports are environment-specific
    -javaagent:/opt/jmx_prometheus_javaagent.jar=7070:/etc/cassandra/jmx-exporter.yml

    # Validate exporter endpoint locally
    curl -s http://127.0.0.1:7070/metrics | head


 15.4 Grafana dashboards and alerts
    Metric family                          Example alert condition (set thresholds from baseline)

    Node availability                      Expected node is not UN for longer than agreed threshold

    Read/write latency                     p95/p99 exceeds service objective

    Dropped messages                       Non-zero sustained increase

    Pending compactions                    Backlog grows continuously

    Disk capacity                          Free space below operational reserve

    GC pauses                              Pause time or frequency breaches baseline

    Repair freshness                       Repair schedule is overdue


 Build alerts from service objectives and historical baselines. Avoid alerting on a single noisy sample. Every alert should
 have an owner, severity, runbook and escalation path.


 16. Security and access control
 16.1 Authentication and authorization
 Authentication verifies who is connecting. Authorization determines what that identity may do. Production clusters should
 use centrally managed identities where supported by the organisation's design, least privilege and periodic access
 review.

 16.2 Lab user and role example
    # In cqlsh, after enabling and validating the chosen authenticator/authorizer:
    CREATE ROLE app_reader
    WITH LOGIN = true
    AND PASSWORD = 'Use-A-Unique-Lab-Secret'
    AND SUPERUSER = false;

    GRANT SELECT ON KEYSPACE dba_training TO app_reader;
    LIST ROLES;
    LIST ALL PERMISSIONS OF app_reader;

 The example password is illustrative only. Do not reuse it. Authentication/authorization configuration must be planned
 and tested carefully; enabling it without creating and validating an administrative role can lock out operators.

 16.3 Security checklist
●     Enable supported authentication and authorization.
●     Use least-privilege application roles; avoid superuser for applications.
●     Restrict CQL, JMX and internode ports at the network layer.
●     Use TLS for client and internode traffic where required.
●     Rotate credentials and protect secrets in an approved vault.
●     Enable audit logging where required and protect log access.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                   Page 19

## Source PDF page 20

●    Patch supported OS, JVM and Cassandra releases through change control.
●    Review service account permissions and file ownership.


 17. Production incident playbooks
 17.1 Node is DOWN
 Triage
    nodetool status
    ping -c 3 cassandra2
    ssh cassandra2
    sudo systemctl status cassandra --no-pager
    sudo journalctl -u cassandra -n 200 --no-pager
    tail -n 200 /var/log/cassandra/system.log
    df -hT
    free -h
    ss -lntp

 Determine whether the failure is process, host, network, disk, memory, JVM or configuration related. Check whether
 other nodes can reach the failed node and whether the failed node can reach peers.

 Recovery guardrails
●    Do not wipe the data directory to make the node start.
●    Do not run cleanup, decommission or removenode without confirming the node's actual state and recovery plan.
●    Check logs for commit log corruption, disk full, bind errors, OOM kill or incompatible configuration.
●    If restart is safe, start the node and monitor bootstrap/recovery, streaming and status.
●    After recovery, assess repair requirements and verify application behaviour.

 17.2 Disk almost full
●    Identify the full mount and largest directories: df -hT, du -xhd1, df -i.
●    Check whether compaction is consuming temporary space.
●    Check snapshots and backup copies; do not delete them until retention and restore requirements are verified.
●    Add capacity or reclaim only approved files using a documented plan.
●    Do not manually delete live SSTables, commit logs or system files.
●    After remediation, validate free space, compaction and node health.

 17.3 High tombstone warnings
●    Identify affected table and query from logs and application traces.
●    Review TTL, delete patterns, partition size and query scan scope.
●    Check repair status and replica downtime history.
●    Do not reduce gc_grace_seconds without a verified repair and deletion-safety design.
●    Plan data-model correction and monitor tombstone scans after deployment.

 17.4 Pending compactions growing
●    Capture compactionstats repeatedly to establish trend.
●    Check disk space, disk latency, CPU and write rate.
●    Identify compaction strategy and SSTable generation rate.
●    Review recent bulk loads, repairs, schema changes or workload spikes.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                 Page 20

## Source PDF page 21

●    Throttle or reschedule workload only through an approved operational decision.

 17.5 Authentication failure
●    Confirm the exact endpoint, username, keyspace and client authentication configuration.
●    Check whether the role exists and has LOGIN permission.
●    Review authorisation grants and server logs.
●    Validate client TLS settings and certificate chain if TLS is enabled.
●    Use the approved privileged recovery path; do not disable security as a first response.

 17.6 Incident communication template
    Incident:
    Start time / timezone:
    Business impact:
    Affected applications / keyspaces / tables:
    Affected nodes / DC:
    Symptoms and error rates:
    Recent changes:
    Evidence collected:
    Actions taken and results:
    Current risk:
    Next update time:
    Root cause:
    Preventive actions:



 18. Maintenance, scaling and upgrades
 18.1 Add a node
 Adding a node changes token ownership and triggers streaming. Plan capacity, network, disk headroom, rack/DC
 placement and application impact. Use the release-specific supported procedure and monitor bootstrap progress.
    nodetool status
    nodetool netstats
    nodetool compactionstats


 18.2 Decommission a node
 Decommission is for a node that is healthy and can stream its data to remaining replicas. It is not the same as removing a
 permanently lost node. Confirm RF, remaining capacity and topology before proceeding.

 Never run decommission on a node simply because it is down. A permanently failed node may require a different
 documented recovery workflow. Validate the exact procedure for the installed Cassandra release.

 18.3 Replace a failed node
 Node replacement requires correct identity and topology handling, a compatible version and a controlled
 bootstrap/replacement workflow. Preserve the old node's host ID and token context as required by the release-specific
 procedure. Do not improvise by copying system tables or changing tokens.

 18.4 Upgrade planning
●    Read release notes and upgrade documentation for source and target versions.
●    Confirm supported upgrade path; check Java, OS and SSTable compatibility.
●    Review deprecated configuration and changed defaults.
●    Take and validate backups; test rollback and restore.
●    Check cluster health, repair status, schema agreement and free disk.
●    Upgrade one node at a time using the documented rolling sequence.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                Page 21

## Source PDF page 22

●     Validate node state, logs, metrics, application traffic and compatibility after each node.
●     Do not upgrade all nodes at once.

 18.5 Change approval checklist
    Control                          Evidence

    Scope                            Nodes, DCs, keyspaces, applications and versions

    Risk                             Availability, data, capacity, security and compatibility

    Pre-check                        Cluster status, backup, repair, disk, latency and alerts

    Execution                        Exact commands, order, owner and timestamps

    Abort criteria                   Clear thresholds and rollback decision owner

    Post-check                       UN nodes, schema agreement, app tests, metrics and logs




 19. DBA daily, weekly and monthly runbooks
 19.1 Daily checks
●     Check all expected nodes are UN and in the correct DC/rack.
●     Review read/write latency, error rates and dropped messages.
●     Review pending compactions and streaming activity.
●     Check disk free space, inode use, memory, swap and GC.
●     Review critical errors and warnings in system.log.
●     Confirm backup jobs completed and off-host copies exist.
●     Check alerts, incidents and application feedback.

 19.2 Weekly checks
●     Review repair completion/freshness against the repair plan.
●     Review capacity trends and growth rate.
●     Review slow queries, hot partitions and large partitions.
●     Review role grants, authentication failures and audit events.
●     Review snapshots and retention; verify backup inventory.
●     Review monitoring gaps and noisy alerts.

 19.3 Monthly/quarterly checks
●     Perform a restore test and record RTO/RPO results.
●     Review Cassandra, JVM and OS patch status.
●     Review capacity forecast and hardware/cloud limits.
●     Review topology, RF, DC/rack design and disaster recovery.
●     Review access, secrets rotation and TLS certificate expiry.
●     Run an incident simulation and update operational runbooks.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                              Page 22

## Source PDF page 23

 19.4 Daily health report shell script
    #!/usr/bin/env bash
    set -u
    CASSANDRA_HOME=/opt/cassandra
    OUT="/var/tmp/cassandra_health_$(hostname -s)_$(date +%Y%m%d_%H%M%S).txt"

    {
      echo "=== Cassandra DBA Health Report ==="
      date
      hostname -f
      echo
      echo "=== nodetool status ==="
      "$CASSANDRA_HOME/bin/nodetool" status
      echo
      echo "=== tpstats ==="
      "$CASSANDRA_HOME/bin/nodetool" tpstats
      echo
      echo "=== compactionstats ==="
      "$CASSANDRA_HOME/bin/nodetool" compactionstats
      echo
      echo "=== gcstats ==="
      "$CASSANDRA_HOME/bin/nodetool" gcstats
      echo
      echo "=== filesystem ==="
      df -hT
      echo
      echo "=== memory ==="
      free -h
    } > "$OUT" 2>&1

    chmod 600 "$OUT"
    echo "Report written to $OUT"

 Run first as the Cassandra administrator interactively. Confirm nodetool authentication/JMX configuration and output.
 Add cron or a scheduler only after validating permissions, log retention and alerting. A report file is not monitoring unless
 it is collected, evaluated and acted upon.

 19.5 Operational handover
●       Cluster diagram, host inventory, DC/rack map and ports.
●       Cassandra/JVM/OS versions and configuration management source.
●       Keyspaces, RF, critical tables and application owners.
●       Backup schedule, storage location, retention and restore procedure.
●       Repair schedule and last successful completion.
●       Monitoring dashboards, alert thresholds and escalation contacts.
●       Known risks, capacity forecast, maintenance calendar and open incidents.


 20. Interview preparation and final practical assessment
 20.1 Core interview questions with model answers
 1. What is Cassandra?
 A distributed, peer-to-peer NoSQL database designed for high availability and horizontal scale. Data is partitioned and
 replicated across nodes.

 2. Is there a master node?
 No single master coordinates all writes. Any node can act as coordinator for a request.

 3. What is a partition key?
 The part of the primary key used to determine partition placement in the cluster.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                    Page 23

## Source PDF page 24

 4. What is a clustering column?
 A primary-key column that controls ordering of rows within a partition.

 5. What is RF?
 Replication factor: the number of replicas maintained for each partition in a data centre.

 6. What is QUORUM for RF=3?
 A majority, which is two replicas.

 7. What is a coordinator?
 The node that receives a client request and coordinates the required replica interactions.

 8. What is a commit log?
 An append-only durability mechanism used to recover acknowledged mutations after a crash.

 9. What is a memtable?
 An in-memory structure that accumulates writes before being flushed to SSTables.

 10. What is an SSTable?
 An immutable on-disk representation of table data.

 11. Why is compaction needed?
 It merges SSTables, controls read amplification and can purge obsolete data when safe.

 12. What is a tombstone?
 A deletion/expiry marker retained so replicas can learn that data was removed.

 13. What is hinted handoff?
 A temporary mechanism to replay mutations to a replica that was unavailable, within configured limits.

 14. What is repair?
 A process that synchronises replica data for token ranges and helps resolve inconsistencies.

 15. What does nodetool status show?
 Node state, DC/rack, load, ownership and host information.

 16. What does UN mean?
 Up and Normal.

 17. What is a seed node?
 A contact point used during gossip startup; it is not a master or a special data owner.

 18. Why use NetworkTopologyStrategy?
 It lets you set replication factor per data centre and is appropriate for topology-aware deployments.

 19. How do you investigate read latency?
 Start with query scope, histograms, table/tombstone/SSTable stats, compaction, disk latency, GC, CPU and replica
 health.

 20. What is the danger of lowering gc_grace_seconds?
 If replicas miss deletes and repair does not protect the data, deleted values may be resurrected.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                               Page 24

## Source PDF page 25

 21. How do you restart a production cluster?
 Use a validated rolling restart: one node at a time, with health and application checks between nodes.

 22. What do you check when disk is full?
 Mount and inode usage, data/commitlog/snapshot/backup sizes, compaction temporary space and deleted-open files.
 Never delete live SSTables manually.

 23. Is a snapshot a complete backup strategy?
 Not by itself. It must be copied off-host, include schema/metadata as needed, be retained securely and be restore-tested.

 24. How do you handle a down node?
 Establish host/process/network/disk/JVM cause, inspect logs, recover without wiping data, then assess streaming and
 repair.

 25. What is a hot partition?
 A partition receiving disproportionate traffic or data, causing uneven load and latency.

 20.2 Scenario-based interview answers
 Scenario A: Application reports high read latency
 Answer framework: I would confirm the affected query, table, time window and latency percentile first. Then I would
 compare node-level proxy histograms, inspect table statistics and tombstone warnings, check SSTable/compaction
 backlog, disk latency, GC pauses and thread-pool queues. I would validate partition-key design and query predicates,
 correlate with recent changes, and apply one controlled remediation at a time. I would not immediately change heap or
 consistency level.

 Scenario B: One node is down
 Answer framework: I would check nodetool status from healthy nodes, then validate host reachability, service status,
 journal/system logs, disk, memory and listening ports on the failed host. I would identify whether the issue is
 infrastructure, process, configuration or data-related. I would recover the node using the documented procedure, avoid
 wiping data, monitor streaming and verify UN status and application behaviour.

 Scenario C: Pending compactions are increasing
 Answer framework: I would trend compactionstats, check disk headroom, disk throughput/latency, CPU and write rate,
 and identify whether a bulk load, repair or workload spike preceded the backlog. I would assess the compaction strategy
 and capacity. I would avoid forcing major compaction without a capacity and impact assessment.

 Scenario D: Tombstone warnings
 Answer framework: I would identify the exact table and query, review TTL/delete patterns, partition sizes and scan
 scope, then check repair freshness and replica downtime. I would not lower gc_grace_seconds as a shortcut. I would
 propose a data-model or write-pattern correction and a safe remediation plan.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                               Page 25

## Source PDF page 26

 20.3 Practical command drill
    Task                                      Command / expected result

    Check node state                          nodetool status → expected nodes UN

    Check cluster metadata                    nodetool describecluster

    Check thread pools                        nodetool tpstats

    Check compaction                          nodetool compactionstats

    Check GC                                  nodetool gcstats

    Check network/streaming                   nodetool netstats

    Create snapshot                           nodetool snapshot -t <tag> <keyspace>

    Check snapshots                           nodetool listsnapshots

    Flush keyspace                            nodetool flush <keyspace>

    Check service logs                        journalctl -u cassandra; system.log



 20.4 Final practical assessment
●    Build a three-node Cassandra 4.1.x cluster and show all nodes UN.
●    Create a keyspace using NetworkTopologyStrategy with RF=3.
●    Create two tables designed for two different query patterns and justify the keys.
●    Insert, update, query and delete sample data.
●    Capture a health snapshot from all nodes and explain the outputs.
●    Perform a controlled single-node stop/start in the lab and observe consistency behaviour.
●    Take a snapshot, copy it off-host and complete a restore test in an isolated environment.
●    Run a primary-range repair in a controlled lab window and explain its scope.
●    Diagnose a simulated read-latency or disk-pressure scenario using evidence.
●    Present a production change plan and a five-minute incident update.

 20.5 Self-assessment scorecard
    Competency                        Beginner                         Working DBA                       Production-ready

    Architecture and CQL              Can explain terms                Can build and query tables        Can defend data model and consistency design

    Cluster operations                Can start/stop lab node          Can run health checks and routine tasks
                                                                                                          Can execute controlled maintenance and recove

    Backup/restore                    Understands snapshots            Can take/copy/validate backup     Can meet tested RPO/RTO

    Troubleshooting                   Collects basic logs              Correlates nodetool and Linux metrics
                                                                                                          Leads evidence-based incident response

    Security/monitoring               Knows key concepts               Can configure lab controls        Operates least privilege, alerts and audit

    Interview communication           Defines concepts                 Explains commands and examples Explains trade-offs, risk and incident ownership




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                               Page 26

## Source PDF page 27

 Appendix A. Safe command reference
    Purpose                                   Command

    Node state                                nodetool status

    Node information                          nodetool info

    Cluster description                       nodetool describecluster

    Thread pools                              nodetool tpstats

    Compaction activity                       nodetool compactionstats

    Table stats                               nodetool tablestats

    Coordinator latency                       nodetool proxyhistograms

    GC stats                                  nodetool gcstats

    Streaming/network                         nodetool netstats

    Gossip state                              nodetool gossipinfo

    Flush                                     nodetool flush <keyspace>

    Snapshot                                  nodetool snapshot -t <tag> <keyspace>

    List snapshots                            nodetool listsnapshots

    Repair help                               nodetool help repair

    Primary range repair                      nodetool repair -pr <keyspace>

    Drain                                     nodetool drain




 Appendix B. Production safety rules
●       Never run destructive commands without a reviewed change, backup and rollback plan.
●       Never delete live SSTables, commit logs or system tables manually.
●       Never wipe a node's data directory as a generic startup fix.
●       Never run all-node restart, repair or compaction operations without a capacity-aware plan.
●       Never expose CQL/JMX/internode ports publicly.
●       Never treat a successful snapshot command as proof of recoverability.
●       Always capture before/after evidence and communicate impact.
●       Always validate against the exact Cassandra version and deployment packaging.


 Appendix C. Recommended study sequence
    Week               Focus                                             Deliverable

    1                  Modules 1–5                                       Working single node, then three-node cluster and CQL basics

    2                  Modules 6–10                                      Two query-driven data models; consistency and nodetool health report

    3                  Modules 11–15                                     Repair lab, backup/restore test, performance evidence and monitoring design

    4                  Modules 16–20                                     Security checklist, incident simulations, runbooks and mock interview


 The objective is not to memorise commands. The objective is to understand what each command changes or measures,
 what healthy output looks like, what risk it introduces, and how you would prove the cluster is safe afterwards.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                                 Page 27

## Source PDF page 28

 End of workbook — Use this as the core practical curriculum. For production deployments, supplement it with the official
 documentation for the exact Cassandra release, your organisation's platform standards and tested operational procedures.




Cassandra DBA Beginner-to-Advanced Practical Workbook                                                                       Page 28