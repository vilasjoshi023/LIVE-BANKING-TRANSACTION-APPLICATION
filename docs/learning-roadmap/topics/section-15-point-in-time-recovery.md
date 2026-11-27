# Section 15 – Point-in-Time Recovery (PITR)

**Master Program source section:** 15  
**Tracking status:** Archive preparation partly completed; live archiving and end-to-end PITR are not enabled or proven.

## Source syllabus topics

- PITR concepts
- Commit log archiving
- Recovery scenarios
- Validation

## Learning objective

Understand the archive/replay chain needed to recover a keyspace to a selected point in time.

## VJCLAB practical plan

The following exercises are project-specific adaptations of the source topics. They are plans, not claims of completed work.

1. Draw relationship between base snapshot, archived CommitLog segments, timestamps and target recovery time.
2. Review CommitLog archive configuration on all nodes; live archive/restore configuration remains empty.
3. Review archive script dummy-file tests and identified no-overwrite hardening requirement.
4. Design isolated restore: restore base data, replay segments only up to target time and validate records.
5. Define checksum, schema, row-count and application-query acceptance checks; do not claim PITR success until end-to-end recovery succeeds.

## Evidence and acceptance checklist

Record the date, Cassandra version, node(s), commands, sanitized outputs and validation result for each item.

- [ ] PITR sequence diagram and recovery runbook.
- [ ] Archive segment inventory and checksum manifest.
- [ ] Isolated recovery results with measured RPO/RTO.

## Interview checkpoint

- What is required in addition to a snapshot for PITR?
- Why must archive handling avoid overwriting files?
- How do you validate a recovered point in time?

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
