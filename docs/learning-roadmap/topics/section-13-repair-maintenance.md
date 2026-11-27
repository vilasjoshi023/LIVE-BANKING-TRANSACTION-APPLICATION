# Section 13 – Repair & Maintenance

**Master Program source section:** 13  
**Tracking status:** Repair preview/incremental repair and compaction observation partly completed; runbook to extend.

## Source syllabus topics

- Incremental repair
- Cleanup, flush, compaction
- Cassandra Reaper (automation)
- Maintenance best practices

## Learning objective

Plan repair and maintenance while controlling streaming, disk, CPU and network impact.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Review prior repair preview and sequential incremental repair results.
2. Inspect nodetool repair help and design a schedule covering intended token ranges/tables.
3. Practice flush and compaction inspection; distinguish observation from forcing major compaction.
4. Study cleanup impact after topology changes and identify when cleanup is required.
5. Evaluate Cassandra Reaper as a repair orchestration option; defer deployment until resources and compatibility are reviewed.
6. Define maintenance prechecks, workload windows, abort thresholds and post-checks.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Repair coverage/history record.
- [ ] Maintenance plan and rollback/abort criteria.
- [ ] Reaper evaluation note.

## Interview checkpoint

- What does repair reconcile?
- What is the difference between repair and compaction?
- Why can cleanup create significant I/O and streaming load?

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
