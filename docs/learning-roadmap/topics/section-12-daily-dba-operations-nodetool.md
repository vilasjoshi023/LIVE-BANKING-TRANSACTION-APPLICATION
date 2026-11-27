# Section 12 – Daily DBA Operations (Nodetool)

**Master Program source section:** 12  
**Tracking status:** Commands used during previous troubleshooting; standard daily runbook to be built.

## Source syllabus topics

- nodetool commands: status, ring, tablestats, tpstats
- Node lifecycle: bootstrap, decommission, replace
- Hotspot detection (toppartitions)

## Learning objective

Build a repeatable daily health-check routine and interpret Cassandra operational signals.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Capture nodetool status, info, describecluster, tpstats, compactionstats, tablestats, gcstats and netstats.
2. Compare nodes and record timestamp, node state, load, pending work, GC and dropped-message deltas.
3. Review toppartitions availability and safe invocation for the installed release before a bounded hotspot exercise.
4. Create a daily DBA summary that flags trends rather than treating one snapshot as an incident.
5. Use existing VJCLAB activity records as prior observations.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] Timestamped health snapshot from each node.
- [ ] Interpretation table with normal, warning and escalation conditions.
- [ ] Daily DBA report template.

## Interview checkpoint

- What does UN mean?
- Why is one nodetool output insufficient for RCA?
- What does tpstats tell you about queue pressure?

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
