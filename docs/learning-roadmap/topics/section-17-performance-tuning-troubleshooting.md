# Section 17 – Performance Tuning & Troubleshooting

**Master Program source section:** 17  
**Tracking status:** Slow-query workload and diagnostic snapshots partly completed; scenario-based RCA track remains in progress.

## Source syllabus topics

- JVM tuning (G1GC / ZGC)
- Heap sizing
- Disk & I/O optimization
- Slow query troubleshooting
- GC issues

## Learning objective

Use evidence-driven troubleshooting to isolate query, JVM, disk, queue, compaction and data-model bottlenecks.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Re-run bounded 100-query workload only after monitoring/authentication maintenance is complete and approved.
2. Compare partition-key lookups with bounded account-filter anti-pattern; record sample size, warm-up, percentiles and rows returned.
3. Collect tpstats, compactionstats, gcstats, tablestats and Linux vmstat/iostat/free/df evidence.
4. Analyze read/write latency, pending compactions, tombstones, hot partitions and GC pauses using RCA worksheets.
5. Study heap and G1GC/ZGC concepts; verify compatibility with Cassandra 4.1.12 and installed JDK before any JVM option change.
6. Change one variable at a time and compare under the same workload.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Performance baseline with run metadata and percentiles.
- [ ] Scenario RCA worksheets and before/after measurements.
- [ ] JVM tuning proposal with compatibility evidence.

## Interview checkpoint

- How do you distinguish disk bottleneck from GC pressure?
- What evidence supports a hot-partition RCA?
- Why should timeouts not be increased as the first response?

## Safety and version controls

- Current learning baseline: CentOS Stream 9 and Apache Cassandra 4.1.12 on VJCLAB.
- Use synthetic data and bounded queries. Never expose credentials, password hashes, .env values, SSH keys or customer information.
- Do not perform destructive operations, node lifecycle changes, service restarts, repair, cleanup, major compactions, security changes or upgrades without a separate pre-check and maintenance plan.
- For Cassandra 5.x or modernization subjects, use a separate compatible test environment. Do not apply 5.x-only features to the current 4.1.12 cluster.
- Update this page only when execution evidence exists; a planned exercise is not a completed lab.

## Session log

| Date | Activity | Result/evidence | Status |
|---|---|---|---|
|  |  |  | Not started |
