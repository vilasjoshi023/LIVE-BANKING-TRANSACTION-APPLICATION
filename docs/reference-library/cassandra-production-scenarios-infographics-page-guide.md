# Cassandra Production Scenarios – Infographic Page Guide

> Source: user-provided image-based PDF `cassandra performance tuning with solutions's.pdf` (9 pages). The PDF pages are full-page infographics and did not expose a searchable text layer. This guide records the visible page headings, diagrams and key points as a page-by-page index; it is not a verbatim transcription of every small label.

## Page 1 – Cassandra DBA production experience

Overview infographic titled **Cassandra DBA – Production Experience: Common Issues, Root Cause Analysis & Resolutions**. It combines a common-issues list, frequently used Cassandra DBA commands, a quick health-check flow, issue-by-issue investigation and resolution summaries, capacity-planning examples and a senior DBA interview answer.

The quick health-check flow is:
1. Check cluster health with `nodetool status`.
2. Check key metrics such as table statistics, compactions and topology.
3. Check system health with OS/disk/heap tools.
4. Identify the root cause.
5. Implement a controlled fix.
6. Monitor and validate stable recovery.

The issue summary covers read/write latency, pending compactions, tombstones, JVM GC, hot partitions, disk full, node down, timeouts, repair/streaming/bootstrap failures, schema disagreement, high CPU and capacity planning.

## Page 2 – Cassandra capacity planning: proactive approach

Explains capacity planning as forecasting storage and resource demand before disks become full. The page illustrates daily storage growth, reviewing CPU utilization, heap usage and read/write throughput, calculating future storage requirements, and acting before a critical threshold is reached.

The example flow is:
- Track day-by-day storage growth.
- Review storage, CPU, heap, read throughput and write throughput.
- Calculate remaining free space and days until capacity is exhausted.
- Treat approximately 75–80% utilization as a planning/decision threshold in the example, not as a universal Cassandra limit.
- Request capacity, add nodes, stream/rebalance data and validate the cluster after expansion.

It also explains why new nodes must be rebalanced: adding a node does not instantly move existing data. The page includes an interviewer prompt about knowing when to add Cassandra nodes.

## Page 3 – Disk usage 95% (almost full)

Production scenario: a monitoring alert reports a Cassandra node disk at approximately 95% use. The page explains why disk headroom is required for SSTables, commit logs, snapshots, hints and other operational files.

The investigation flow includes:
- Check filesystem usage with `df -h`.
- Locate large directories with `du`.
- Identify data, commit-log, hints, saved-cache, log and snapshot usage.
- Inspect snapshots and verify their age/retention before any removal.
- Confirm whether rapid data growth or old snapshots are responsible.
- Treat disk saturation as a serious operational risk because writes, flushes and compactions need storage capacity.

The remediation choices illustrated are removing only verified obsolete snapshots, extending storage, and capacity planning/node expansion. The page emphasizes verification and before/after comparisons.

## Page 4 – Pending compactions high (from 5 to 500)

Explains that compaction merges immutable SSTables, and that pending tasks represent work waiting for compaction executors. A growing backlog can increase disk I/O contention and impact read/write latency.

Investigation includes:
- `nodetool compactionstats` to capture pending and active compaction work.
- Repeated observations to establish whether the queue is increasing.
- `iostat -x 1` to check device utilization and await.
- Correlating write volume, SSTable creation, disk throughput and compaction capacity.

The RCA flow connects heavy write traffic, more SSTables, compaction backlog, disk contention and read/write latency. Suggested remedies include resolving a storage bottleneck, reviewing compaction strategy, adjusting compaction throughput within the capacity of the disk/CPU, and adding capacity where sustained workload exceeds the platform. The page cautions against treating concurrent compaction changes as a generic fix.

## Page 5 – Hot partition (data skew)

Shows how a partition key determines the token and replica placement for a partition. A low-cardinality or skewed key can direct a disproportionate share of requests to one node while other nodes remain relatively idle.

Illustrated symptom: one Cassandra node at approximately 95% CPU while other nodes have much lower utilization.

The investigation/re-design flow is:
- Check cluster health first.
- Compare node CPU and request distribution.
- Review the table's partition key and cardinality.
- Identify whether a small set of partition keys receives a disproportionate request volume.
- Redesign the data model to distribute writes/reads (the infographic uses alternative key examples and time-bucketing concepts).
- Re-test routing and CPU distribution after the model change.

The key takeaway is that Cassandra does not automatically split one oversized/hot partition across multiple nodes simply because the cluster has more nodes.

## Page 6 – JVM garbage collection causing latency spikes

Explains Cassandra's JVM runtime and heap usage, including objects created while servicing reads/writes and the impact of garbage-collection pauses.

The symptom is intermittent application latency spikes. The investigation includes:
- `nodetool gcstats`.
- JVM/GC monitoring and heap-usage trends.
- Reviewing GC logs and correlating pause timing with application latency.
- Checking large queries/partitions and excessive object creation.

The page connects rising heap pressure and long GC pauses with slow or stalled request processing. The resolution examples include reviewing heap/GC configuration for the deployed Cassandra/JDK release, using the configured collector appropriately, reducing unnecessary object churn, and improving query/partition design. It emphasizes verifying latency and GC metrics after tuning.

## Page 7 – Cassandra tombstone issue

Illustrates that Cassandra deletes and TTL expiry create tombstones rather than immediately erasing data. Tombstones are retained to protect replica consistency and prevent deleted data from reappearing when an offline replica returns.

The investigation includes application `ReadTimeoutException`, table statistics and tombstones per slice. Causes illustrated include frequent DELETE operations and very short TTLs. The page explains the grace-period concept and that compaction can remove tombstones only when Cassandra's safety conditions are met.

Resolution points include reviewing delete/TTL patterns with developers, avoiding unnecessary short TTLs, designing query-friendly partitions, querying only required data and allowing safe compaction. Lowering `gc_grace_seconds` is not presented as a casual performance fix; replica repair and data-resurrection risk must be considered.

## Page 8 – High write latency (20–30 ms to 1–2 seconds)

Production scenario focused on slow inserts during peak hours. The write-path diagram follows application → coordinator → commit log → memtable → acknowledgement, followed by flush to SSTable and compaction.

The diagnostic flow includes:
- `nodetool tpstats` for mutation-stage pending work.
- `nodetool compactionstats` for compaction backlog.
- `iostat -x 1` for disk utilization/await.
- Checking commit-log and storage contention.

The RCA links queued writes, pending compactions and saturated disks. The infographic's capacity remedy includes adding a node, streaming/rebalancing data and reviewing compaction configuration. It presents before/after comparisons to show write latency recovering after the underlying bottleneck is resolved.

## Page 9 – High read latency (50 ms to 2–3 seconds)

Production scenario focused on read latency spikes. Its troubleshooting sequence is:
1. Check cluster health with `nodetool status`.
2. Check table statistics with `nodetool tablestats`.
3. Check compaction state with `nodetool compactionstats`.
4. Check disk performance using `iostat -x 1`.
5. Correlate latency, SSTables per read, pending compactions and disk utilization.
6. Verify the root cause before applying a fix.

The infographic's example RCA connects too many SSTables and compaction backlog with disk saturation and slow reads. Suggested actions include increasing compaction throughput when the storage subsystem has headroom, reviewing whether the compaction strategy matches the workload, and moving heavy maintenance/repair/major compaction/bulk-load operations outside peak hours. The example describes read latency returning to approximately 60–80 ms after tuning.

## Source-use note

Thresholds and before/after figures in these infographics are illustrative examples from the supplied PDF, not measured results from the VJCLAB environment and not production SLAs. Validate every proposed setting against the deployed Cassandra version, table workload, disk capacity and operational baseline.
