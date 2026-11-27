# Section 04 – Cassandra Internals (Read & Write Path)

**Master Program source section:** 4  
**Tracking status:** Some operational diagnostics already performed; internals module to be completed systematically.

## Source syllabus topics

- Write path (CommitLog → Memtable → SSTable)
- Read path (Cache → Bloom Filter → SSTables)
- Tombstones & GC basics
- Compaction overview (STCS, LCS, UCS)

## Learning objective

Understand how mutations become durable SSTables and how reads reconcile data from memory and disk.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Draw the write path from client to coordinator, replicas, CommitLog, memtable, flush and SSTable.
2. Inspect commit-log, data and saved-cache directory configuration without modifying files.
3. Use nodetool tablestats and compactionstats to observe SSTable counts and pending compactions.
4. Review Bloom filters, key cache, row cache and read-path troubleshooting concepts.
5. Compare STCS, LCS and TWCS/UCS conceptually; verify the strategy configured on the banking table.
6. Use statistics and logs to understand tombstone symptoms; do not lower gc_grace_seconds as an exercise.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Read-path and write-path diagrams.
- [ ] Sanitized table/compaction statistics.
- [ ] Compaction-strategy comparison and tombstone RCA worksheet.

## Interview checkpoint

- Why is the CommitLog append performed before acknowledging a write?
- What does a Bloom filter tell Cassandra?
- Why can tombstones make reads expensive?

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
